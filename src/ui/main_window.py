"""First usable GameMaster window around the official Scrcpy client."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from adb_manager import AdbManager
from official_scrcpy import OfficialScrcpySession, ScrcpyConfig
from key_overlay import KeyOverlay
from panels import SidePanel
from theme import DARK_GAMING_STYLE
from video_host import VideoHost


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("GameMaster")
        self.resize(1280, 800)
        self.setStyleSheet(DARK_GAMING_STYLE)
        self._root = Path(__file__).resolve().parents[2]
        self._tools = self._root / "tools" / "official-scrcpy"
        self._adb = AdbManager(self._tools / "adb.exe")
        self._scrcpy: OfficialScrcpySession | None = None
        self._zoom = 1.0
        self._build_ui()
        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self.refresh_devices)
        self._refresh_timer.start(2500)
        self.refresh_devices()

    def _build_ui(self) -> None:
        root = QWidget(self)
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(12, 12, 12, 12)

        toolbar = QHBoxLayout()
        self.device_combo = QComboBox()
        self.device_combo.setMinimumWidth(260)
        toolbar.addWidget(QLabel("Device"))
        toolbar.addWidget(self.device_combo)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_devices)
        toolbar.addWidget(self.refresh_button)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_scrcpy)
        toolbar.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_scrcpy)
        self.stop_button.setEnabled(False)
        toolbar.addWidget(self.stop_button)

        toolbar.addStretch(1)
        for text, delta in (("−", -0.1), ("100%", 0.0), ("+", 0.1)):
            button = QPushButton(text)
            button.clicked.connect(lambda _checked=False, d=delta: self.change_zoom(d))
            toolbar.addWidget(button)
        root_layout.addLayout(toolbar)

        self.status = QLabel("Ready — no device checked yet")
        self.status.setObjectName("connectionStatus")
        root_layout.addWidget(self.status)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.left_panel = SidePanel("Devices", "No device connected")
        splitter.addWidget(self.left_panel)

        center = QWidget()
        center_layout = QVBoxLayout(center)
        center_layout.setContentsMargins(0, 0, 0, 0)
        self.video_host = VideoHost()
        self.key_overlay = KeyOverlay()
        center_layout.addWidget(self.video_host, 1)
        center_layout.addWidget(self.key_overlay)
        splitter.addWidget(center)

        self.right_panel = SidePanel("Profiles", "No profile loaded")
        splitter.addWidget(self.right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 4)
        splitter.setStretchFactor(2, 1)
        root_layout.addWidget(splitter, 1)
        self.setCentralWidget(root)

    def refresh_devices(self) -> None:
        previous = self.device_combo.currentData()
        devices = self._adb.devices() if self._adb.is_available() else []
        self.device_combo.blockSignals(True)
        self.device_combo.clear()
        for device in devices:
            label = f"{device.model or device.serial} [{device.state}]"
            self.device_combo.addItem(label, device.serial)
        self.device_combo.blockSignals(False)
        if previous:
            index = self.device_combo.findData(previous)
            if index >= 0:
                self.device_combo.setCurrentIndex(index)
        if not devices:
            self.left_panel.set_body("No device detected\nConnect USB and enable USB debugging")
            if self._scrcpy is None:
                self.status.setText("Ready — no ADB device detected")
        else:
            self.left_panel.set_body("\n".join(f"{item.model or item.serial}: {item.state}" for item in devices))
            if self._scrcpy is None:
                self.status.setText("Device detected — press Start")

    def start_scrcpy(self) -> None:
        serial = self.device_combo.currentData()
        if not serial:
            self.status.setText("Cannot start: select an authorized device")
            return
        if self._scrcpy and self._scrcpy.running:
            return
        executable = self._tools / "scrcpy.exe"
        adb_path = self._tools / "adb.exe"
        if not executable.exists() or not adb_path.exists():
            self.status.setText("Missing official Scrcpy or ADB files")
            return
        self._scrcpy = OfficialScrcpySession(executable, adb_path, self._on_scrcpy_log)
        self._scrcpy.start(serial, ScrcpyConfig())
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.video_host.set_status("Official Scrcpy starting…")
        self.status.setText("Scrcpy starting — control is disabled until the official client is ready")

    def stop_scrcpy(self) -> None:
        if self._scrcpy:
            self._scrcpy.stop()
        self._scrcpy = None
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.video_host.set_status("Scrcpy stopped")
        self.status.setText("Ready")

    def change_zoom(self, delta: float) -> None:
        if delta == 0:
            self._zoom = 1.0
        else:
            self._zoom = max(0.5, min(2.0, round(self._zoom + delta, 2)))
        self.video_host.setProperty("zoom", self._zoom)
        self.video_host.set_status(f"Official Scrcpy view — zoom {self._zoom:.0%}")

    def _on_scrcpy_log(self, line: str) -> None:
        self.status.setText(line[-180:])

    def closeEvent(self, event) -> None:  # noqa: N802
        self.stop_scrcpy()
        event.accept()
