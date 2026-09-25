from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GatewayConfig:
    gateway_port: int = 5000
    gateway_bind_host: str = "0.0.0.0"
    robot_ip: str = "127.0.0.1"
    heartbeat_period_sec: float = 0.5
    heartbeat_timeout_sec: float = 1.5
    command_timeout_sec: float = 0.75
    max_linear_x: float = 0.05
    max_linear_y: float = 0.05
    max_angular_z: float = 0.20
    state_period_sec: float = 0.2
    scan_health_period_sec: float = 1.0
    scan_stale_sec: float = 2.0
    reconnect_min_sec: float = 1.0
    reconnect_max_sec: float = 5.0
    socket_timeout_sec: float = 0.2
    max_line_bytes: int = 65536

    @classmethod
    def from_env(cls, path) -> "GatewayConfig":
        values = _read_env_file(Path(path))
        kwargs = {}
        int_fields = {"GATEWAY_PORT": "gateway_port", "MAX_LINE_BYTES": "max_line_bytes"}
        float_fields = {
            "HEARTBEAT_PERIOD_SEC": "heartbeat_period_sec",
            "HEARTBEAT_TIMEOUT_SEC": "heartbeat_timeout_sec",
            "COMMAND_TIMEOUT_SEC": "command_timeout_sec",
            "MAX_LINEAR_X": "max_linear_x",
            "MAX_LINEAR_Y": "max_linear_y",
            "MAX_ANGULAR_Z": "max_angular_z",
            "STATE_PERIOD_SEC": "state_period_sec",
            "SCAN_HEALTH_PERIOD_SEC": "scan_health_period_sec",
            "SCAN_STALE_SEC": "scan_stale_sec",
            "RECONNECT_MIN_SEC": "reconnect_min_sec",
            "RECONNECT_MAX_SEC": "reconnect_max_sec",
            "SOCKET_TIMEOUT_SEC": "socket_timeout_sec",
        }
        str_fields = {
            "GATEWAY_BIND_HOST": "gateway_bind_host",
            "ROBOT_IP": "robot_ip",
        }

        for env_name, attr in int_fields.items():
            if env_name in values:
                try:
                    kwargs[attr] = int(values[env_name])
                except ValueError as exc:
                    raise ValueError(f"{env_name} must be an integer") from exc
        for env_name, attr in float_fields.items():
            if env_name in values:
                try:
                    kwargs[attr] = float(values[env_name])
                except ValueError as exc:
                    raise ValueError(f"{env_name} must be numeric") from exc
        for env_name, attr in str_fields.items():
            if env_name in values:
                kwargs[attr] = values[env_name]

        cfg = cls(**kwargs)
        cfg._validate()
        return cfg

    def _validate(self) -> None:
        if not 1 <= self.gateway_port <= 65535:
            raise ValueError("GATEWAY_PORT must be in 1..65535")
        positive = {
            "HEARTBEAT_PERIOD_SEC": self.heartbeat_period_sec,
            "HEARTBEAT_TIMEOUT_SEC": self.heartbeat_timeout_sec,
            "COMMAND_TIMEOUT_SEC": self.command_timeout_sec,
            "MAX_LINEAR_X": self.max_linear_x,
            "MAX_LINEAR_Y": self.max_linear_y,
            "MAX_ANGULAR_Z": self.max_angular_z,
            "STATE_PERIOD_SEC": self.state_period_sec,
            "SCAN_HEALTH_PERIOD_SEC": self.scan_health_period_sec,
            "SCAN_STALE_SEC": self.scan_stale_sec,
            "RECONNECT_MIN_SEC": self.reconnect_min_sec,
            "RECONNECT_MAX_SEC": self.reconnect_max_sec,
            "SOCKET_TIMEOUT_SEC": self.socket_timeout_sec,
        }
        for name, value in positive.items():
            if value <= 0:
                raise ValueError(f"{name} must be > 0")
        if self.reconnect_max_sec < self.reconnect_min_sec:
            raise ValueError("RECONNECT_MAX_SEC must be >= RECONNECT_MIN_SEC")
        if self.max_line_bytes <= 0:
            raise ValueError("MAX_LINE_BYTES must be > 0")


def _read_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        raise FileNotFoundError(path)
    result: dict[str, str] = {}
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"invalid env line {lineno}: expected KEY=VALUE")
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError(f"invalid env line {lineno}: empty key")
        result[key] = value
    return result
