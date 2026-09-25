from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SafetyState(str, Enum):
    DISCONNECTED = "DISCONNECTED"
    CONNECTED_STOPPED = "CONNECTED_STOPPED"
    ACTIVE = "ACTIVE"
    FAILSAFE_STOP = "FAILSAFE_STOP"


@dataclass(frozen=True)
class WatchdogDecision:
    stop_required: bool
    reason: str | None = None
    command_allowed: bool = False


class GatewayWatchdog:
    """Pure safety state machine. Time values are monotonic seconds from caller."""

    def __init__(self, heartbeat_timeout: float, command_timeout: float):
        if heartbeat_timeout <= 0 or command_timeout <= 0:
            raise ValueError("timeouts must be > 0")
        self.heartbeat_timeout = float(heartbeat_timeout)
        self.command_timeout = float(command_timeout)
        self.state = SafetyState.DISCONNECTED
        self.last_heartbeat: float | None = None
        self.last_command: float | None = None

    def on_connect(self, now: float) -> WatchdogDecision:
        self.state = SafetyState.CONNECTED_STOPPED
        self.last_heartbeat = float(now)
        self.last_command = None
        return WatchdogDecision(False, None)

    def on_heartbeat(self, now: float) -> WatchdogDecision:
        if self.state is not SafetyState.DISCONNECTED:
            self.last_heartbeat = float(now)
        return WatchdogDecision(False, None)

    def on_valid_command(self, now: float) -> WatchdogDecision:
        if self.state in (SafetyState.CONNECTED_STOPPED, SafetyState.ACTIVE):
            self.last_command = float(now)
            self.state = SafetyState.ACTIVE
            return WatchdogDecision(False, None, command_allowed=True)
        return WatchdogDecision(False, None, command_allowed=False)

    def on_stop(self, now: float) -> WatchdogDecision:
        if self.state is SafetyState.DISCONNECTED:
            return WatchdogDecision(False, None)
        self.last_command = None
        if self.state is not SafetyState.FAILSAFE_STOP:
            self.state = SafetyState.CONNECTED_STOPPED
        return WatchdogDecision(True, "explicit_stop")

    def on_disconnect(self, now: float) -> WatchdogDecision:
        was_connected = self.state is not SafetyState.DISCONNECTED
        self.state = SafetyState.DISCONNECTED
        self.last_heartbeat = None
        self.last_command = None
        return WatchdogDecision(was_connected, "disconnect" if was_connected else None)

    def tick(self, now: float) -> WatchdogDecision:
        now = float(now)
        if self.state is SafetyState.DISCONNECTED:
            return WatchdogDecision(False, None)
        if self.state is SafetyState.FAILSAFE_STOP:
            return WatchdogDecision(False, None)

        if self.last_heartbeat is None or now - self.last_heartbeat > self.heartbeat_timeout:
            self.state = SafetyState.FAILSAFE_STOP
            self.last_command = None
            return WatchdogDecision(True, "heartbeat_timeout")

        if self.state is SafetyState.ACTIVE:
            if self.last_command is None or now - self.last_command > self.command_timeout:
                self.state = SafetyState.FAILSAFE_STOP
                self.last_command = None
                return WatchdogDecision(True, "command_timeout")

        return WatchdogDecision(False, None)


class SessionState:
    """Minimal connection-epoch state used to prevent stale command replay."""

    def __init__(self):
        self.connected = False
        self.hello_ok = False
        self.pending_command = None

    def reset_for_connect(self) -> None:
        self.connected = True
        self.hello_ok = False
        self.pending_command = None

    def reset_for_disconnect(self) -> None:
        self.connected = False
        self.hello_ok = False
        self.pending_command = None

    def mark_hello_ok(self) -> None:
        if self.connected:
            self.hello_ok = True

    def record_command(self, command: dict) -> None:
        if self.connected:
            self.pending_command = dict(command)

    def clear_command(self) -> None:
        self.pending_command = None
