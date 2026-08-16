"""Reusable side panel widget."""

from __future__ import annotations

from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class SidePanel(QFrame):
    def __init__(self, title: str, body: str = "") -> None:
        super().__init__()
        self.setObjectName("sidePanel")
        layout = QVBoxLayout(self)
        heading = QLabel(title)
        heading.setObjectName("panelTitle")
        layout.addWidget(heading)
        self.body = QLabel(body)
        self.body.setWordWrap(True)
        layout.addWidget(self.body)
        layout.addStretch(1)

    def set_body(self, text: str) -> None:
        self.body.setText(text)
