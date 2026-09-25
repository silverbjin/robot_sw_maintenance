from __future__ import annotations

import json
import math
import time
from dataclasses import dataclass
from typing import Any

PROTOCOL_VERSION = "1.0"
DEFAULT_MAX_LINE_BYTES = 65536
KNOWN_TYPES = {
    "HELLO",
    "HELLO_ACK",
    "HEARTBEAT",
    "HEARTBEAT_ACK",
    "CMD_VEL",
    "STOP",
    "STATE",
    "SCAN_HEALTH",
    "ERROR",
}


class ProtocolError(ValueError):
    """Raised when an NDJSON frame or gateway message is invalid."""


@dataclass(frozen=True)
class VelocityLimits:
    linear_x: float
    linear_y: float
    angular_z: float


class NDJSONBuffer:
    """Incrementally frame UTF-8 newline-delimited JSON objects from TCP bytes."""

    def __init__(self, max_line_bytes: int = DEFAULT_MAX_LINE_BYTES):
        if max_line_bytes <= 0:
            raise ValueError("max_line_bytes must be > 0")
        self.max_line_bytes = int(max_line_bytes)
        self._buffer = bytearray()

    def feed(self, data: bytes) -> list[dict[str, Any]]:
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes")
        self._buffer.extend(data)
        messages: list[dict[str, Any]] = []

        while True:
            newline = self._buffer.find(b"\n")
            if newline < 0:
                if len(self._buffer) > self.max_line_bytes:
                    self._buffer.clear()
                    raise ProtocolError("line too long")
                break

            if newline > self.max_line_bytes:
                del self._buffer[: newline + 1]
                raise ProtocolError("line too long")

            raw = bytes(self._buffer[:newline])
            del self._buffer[: newline + 1]
            if not raw.strip():
                continue

            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise ProtocolError("invalid UTF-8") from exc
            try:
                obj = json.loads(text)
            except json.JSONDecodeError as exc:
                raise ProtocolError("invalid JSON") from exc
            if not isinstance(obj, dict):
                raise ProtocolError("JSON line must be an object")
            messages.append(obj)

        return messages


def encode_message(message: dict[str, Any]) -> bytes:
    if not isinstance(message, dict):
        raise TypeError("message must be a dict")
    try:
        text = json.dumps(message, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise ProtocolError(f"message is not JSON-safe: {exc}") from exc
    return (text + "\n").encode("utf-8")


def make_message(message_type: str, seq: int, **fields: Any) -> dict[str, Any]:
    if not isinstance(message_type, str) or not message_type:
        raise ProtocolError("type must be a non-empty string")
    if isinstance(seq, bool) or not isinstance(seq, int) or seq < 0:
        raise ProtocolError("seq must be a non-negative integer")
    return {"type": message_type, "seq": seq, "timestamp": time.time(), **fields}


def make_state_message(
    seq: int,
    *,
    odom: dict[str, Any] | None,
    imu: dict[str, Any] | None,
    voltage: float | None,
    voltage_backup: float | None,
) -> dict[str, Any]:
    return make_message(
        "STATE",
        seq,
        odom=odom,
        imu=imu,
        voltage=voltage,
        voltage_backup=voltage_backup,
    )


def _is_finite_number(value: Any) -> bool:
    return not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(float(value))


def validate_common_message(message: dict[str, Any], *, require_known_type: bool = True) -> dict[str, Any]:
    if not isinstance(message, dict):
        raise ProtocolError("message must be an object")
    message_type = message.get("type")
    if not isinstance(message_type, str) or not message_type:
        raise ProtocolError("missing or invalid type")
    if require_known_type and message_type not in KNOWN_TYPES:
        raise ProtocolError(f"unknown message type: {message_type}")
    seq = message.get("seq")
    if isinstance(seq, bool) or not isinstance(seq, int) or seq < 0:
        raise ProtocolError("missing or invalid seq")
    timestamp = message.get("timestamp")
    if not _is_finite_number(timestamp):
        raise ProtocolError("missing or invalid timestamp")
    return message


def _validated_velocity_field(message: dict[str, Any], name: str, limit: float) -> float:
    value = message.get(name)
    if not _is_finite_number(value):
        raise ProtocolError(f"{name} must be a finite number")
    numeric = float(value)
    if abs(numeric) > float(limit):
        raise ProtocolError(f"{name} exceeds configured limit {limit}")
    return numeric


def validate_cmd_vel(message: dict[str, Any], limits: VelocityLimits) -> dict[str, Any]:
    validate_common_message(message)
    if message.get("type") != "CMD_VEL":
        raise ProtocolError("expected CMD_VEL")
    normalized = dict(message)
    normalized["linear_x"] = _validated_velocity_field(message, "linear_x", limits.linear_x)
    normalized["linear_y"] = _validated_velocity_field(message, "linear_y", limits.linear_y)
    normalized["angular_z"] = _validated_velocity_field(message, "angular_z", limits.angular_z)
    return normalized
