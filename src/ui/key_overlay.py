"""Transparent key overlay contract."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel


class KeyOverlay(QLabel):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("keyOverlay")
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setText("")

    def set_labels(self, labels: list[str]) -> None:
        self.setText("  ".join(labels))
