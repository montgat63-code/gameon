"""Official Scrcpy process lifecycle.

This module intentionally does not implement Scrcpy's private protocol.
"""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass(frozen=True, slots=True)
class ScrcpyConfig:
    max_size: int = 1280
    video_bit_rate: str = "8M"
    max_fps: int = 60
    no_audio: bool = True
    stay_awake: bool = False


class OfficialScrcpySession:
    def __init__(
        self,
        executable: str | os.PathLike[str],
        adb_path: str | os.PathLike[str],
        on_log: Callable[[str], None] | None = None,
    ) -> None:
        self.executable = Path(executable)
        self.adb_path = Path(adb_path)
        self.on_log = on_log or (lambda _line: None)
        self.process: subprocess.Popen[str] | None = None

    @property
    def running(self) -> bool:
        return self.process is not None and self.process.poll() is None

    def command(self, serial: str, config: ScrcpyConfig | None = None) -> list[str]:
        cfg = config or ScrcpyConfig()
        command = [
            str(self.executable),
            "--serial",
            serial,
            "--max-size",
            str(cfg.max_size),
            "--video-bit-rate",
            cfg.video_bit_rate,
            "--max-fps",
            str(cfg.max_fps),
        ]
        if cfg.no_audio:
            command.append("--no-audio")
        # Deliberately do not pass stay_awake; it can require protected Android settings.
        return command

    def start(self, serial: str, config: ScrcpyConfig | None = None) -> None:
        if self.running:
            return
        env = os.environ.copy()
        env["PATH"] = f"{self.adb_path.parent}{os.pathsep}{env.get('PATH', '')}"
        self.process = subprocess.Popen(
            self.command(serial, config),
            cwd=str(self.executable.parent),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )

    def stop(self) -> None:
        process = self.process
        self.process = None
        if process is None or process.poll() is not None:
            return
        process.terminate()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=3)
