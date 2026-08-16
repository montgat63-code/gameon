"""Central area reserved for the official Scrcpy native window."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class VideoHost(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("videoHost")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(self)
        self.message = QLabel("No device connected\nOfficial Scrcpy view will appear here")
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message.setObjectName("videoPlaceholder")
        layout.addWidget(self.message)

    def set_status(self, text: str) -> None:
        self.message.setText(text)
