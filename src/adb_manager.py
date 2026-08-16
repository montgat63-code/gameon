"""Safe, testable ADB discovery layer."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

from device_state import DeviceInfo


@dataclass(frozen=True, slots=True)
class AdbResult:
    returncode: int
    stdout: str
    stderr: str


class AdbManager:
    def __init__(self, adb_path: str | os.PathLike[str] = "adb") -> None:
        self.adb_path = str(adb_path)

    def _run(self, *args: str, timeout: float = 8.0) -> AdbResult:
        completed = subprocess.run(
            [self.adb_path, *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
        return AdbResult(completed.returncode, completed.stdout, completed.stderr)

    def version(self) -> AdbResult:
        return self._run("version")

    def devices(self) -> list[DeviceInfo]:
        result = self._run("devices", "-l")
        return parse_adb_devices(result.stdout)

    def is_available(self) -> bool:
        try:
            return self.version().returncode == 0
        except (OSError, subprocess.SubprocessError):
            return False


def parse_adb_devices(output: str) -> list[DeviceInfo]:
    devices: list[DeviceInfo] = []
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("List of devices"):
            continue
        fields = line.split()
        if len(fields) < 2:
            continue
        serial, state = fields[0], fields[1]
        model = ""
        for field in fields[2:]:
            if field.startswith("model:"):
                model = field.removeprefix("model:").replace("_", " ")
                break
        devices.append(DeviceInfo(serial=serial, state=state, model=model))
    return devices
