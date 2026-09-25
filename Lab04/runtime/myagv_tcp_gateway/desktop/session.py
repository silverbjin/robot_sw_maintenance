from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from common.protocol import PROTOCOL_VERSION, ProtocolError, validate_common_message


class DesktopSessionState:
    """Connection-epoch command state; disconnected commands are intentionally dropped."""

    def __init__(self):
        self.connected = False
        self.hello_ok = False
        self._pending_command = None

    def on_connect(self) -> None:
        self.connected = True
        self.hello_ok = False
        self._pending_command = None

    def on_hello_ack(self) -> None:
        if self.connected:
            self.hello_ok = True
            self._pending_command = None

    def on_disconnect(self) -> None:
        self.connected = False
        self.hello_ok = False
        self._pending_command = None

    def set_command(self, linear_x: float, linear_y: float, angular_z: float) -> bool:
        if not (self.connected and self.hello_ok):
            return False
        self._pending_command = {
            "linear_x": float(linear_x),
            "linear_y": float(linear_y),
            "angular_z": float(angular_z),
        }
        return True

    def take_command_for_send(self):
        command = self._pending_command
        self._pending_command = None
        return command


@dataclass
class DesktopProtocolResult:
    hello_ack: bool = False
    heartbeat_ack: bool = False
    state_message: dict[str, Any] | None = None
    scan_health: dict[str, Any] | None = None
    error: str | None = None
    close_connection: bool = False


class DesktopProtocolSession:
    """Pure inbound protocol processor for the Desktop endpoint."""

    def handle(self, message: dict[str, Any]) -> DesktopProtocolResult:
        try:
            validate_common_message(message)
        except ProtocolError as exc:
            return DesktopProtocolResult(error=f"invalid_message: {exc}")

        message_type = message["type"]
        if message_type == "HELLO_ACK":
            if message.get("protocol_version") != PROTOCOL_VERSION:
                return DesktopProtocolResult(
                    error="protocol_version_mismatch",
                    close_connection=True,
                )
            if message.get("role") != "jetson":
                return DesktopProtocolResult(error="invalid_hello_role", close_connection=True)
            return DesktopProtocolResult(hello_ack=True)
        if message_type == "HEARTBEAT_ACK":
            return DesktopProtocolResult(heartbeat_ack=True)
        if message_type == "STATE":
            return DesktopProtocolResult(state_message=message)
        if message_type == "SCAN_HEALTH":
            return DesktopProtocolResult(scan_health=message)
        if message_type == "ERROR":
            code = str(message.get("code", "REMOTE_ERROR"))
            text = str(message.get("message", ""))
            return DesktopProtocolResult(error=f"{code}: {text}".rstrip())
        return DesktopProtocolResult(error=f"unexpected_message: {message_type}")
