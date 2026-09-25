from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from common.protocol import (
    PROTOCOL_VERSION,
    ProtocolError,
    VelocityLimits,
    make_message,
    validate_cmd_vel,
    validate_common_message,
)


@dataclass
class SessionResult:
    outbound: list[dict[str, Any]] = field(default_factory=list)
    command: dict[str, float] | None = None
    command_is_fresh: bool = False
    heartbeat: bool = False
    stop: bool = False
    close_connection: bool = False


class JetsonProtocolSession:
    """Pure per-connection protocol state for the Jetson TCP endpoint."""

    def __init__(self, limits: VelocityLimits):
        self.limits = limits
        self.hello_ok = False
        self._out_seq = 0

    def _next(self, message_type: str, **fields: Any) -> dict[str, Any]:
        self._out_seq += 1
        return make_message(message_type, self._out_seq, **fields)

    def make_outbound(self, message_type: str, **fields: Any) -> dict[str, Any]:
        """Create an outbound message using this connection epoch sequence."""
        return self._next(message_type, **fields)

    def _error(self, code: str, message: str, *, close: bool = False) -> SessionResult:
        return SessionResult(
            outbound=[self._next("ERROR", code=code, message=message)],
            close_connection=close,
        )

    def handle(self, message: dict[str, Any], now: float) -> SessionResult:
        del now  # caller owns monotonic safety timing; sender timestamp is diagnostic only
        try:
            validate_common_message(message)
        except ProtocolError as exc:
            return self._error("INVALID_MESSAGE", str(exc))

        message_type = message["type"]
        if message_type == "HELLO":
            version = message.get("protocol_version")
            role = message.get("role")
            if version != PROTOCOL_VERSION:
                return self._error(
                    "PROTOCOL_VERSION_MISMATCH",
                    f"expected {PROTOCOL_VERSION}, got {version!r}",
                    close=True,
                )
            if role != "desktop":
                return self._error("INVALID_ROLE", "HELLO role must be desktop", close=True)
            self.hello_ok = True
            return SessionResult(
                outbound=[
                    self._next(
                        "HELLO_ACK",
                        protocol_version=PROTOCOL_VERSION,
                        role="jetson",
                    )
                ]
            )

        if not self.hello_ok:
            return self._error("HELLO_REQUIRED", "HELLO must be accepted before other messages")

        if message_type == "HEARTBEAT":
            return SessionResult(
                outbound=[self._next("HEARTBEAT_ACK")],
                heartbeat=True,
            )
        if message_type == "CMD_VEL":
            try:
                normalized = validate_cmd_vel(message, self.limits)
            except ProtocolError as exc:
                return self._error("INVALID_COMMAND", str(exc))
            return SessionResult(
                command={
                    "linear_x": normalized["linear_x"],
                    "linear_y": normalized["linear_y"],
                    "angular_z": normalized["angular_z"],
                },
                command_is_fresh=True,
            )
        if message_type == "STOP":
            return SessionResult(stop=True)

        return self._error("UNEXPECTED_MESSAGE", f"desktop cannot send {message_type}")
