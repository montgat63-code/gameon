"""Connection and device state contracts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ConnectionState(StrEnum):
    NO_DEVICE = "no_device"
    UNAUTHORIZED = "unauthorized"
    DEVICE_READY = "device_ready"
    SCRCPY_STARTING = "scrcpy_starting"
    VIDEO_READY = "video_ready"
    CONTROL_READY = "control_ready"
    STREAMING = "streaming"
    RECOVERING = "recovering"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class DeviceInfo:
    serial: str
    state: str
    model: str = ""
    transport: str = "usb"


@dataclass(frozen=True, slots=True)
class DeviceSession:
    device: DeviceInfo | None = None
    state: ConnectionState = ConnectionState.NO_DEVICE
    message: str = ""

    @property
    def control_ready(self) -> bool:
        return self.state in {
            ConnectionState.CONTROL_READY,
            ConnectionState.STREAMING,
        }
