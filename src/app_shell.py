"""Application shell kept independent from device and Scrcpy services."""

from __future__ import annotations

from PySide6.QtWidgets import QMainWindow

from ui.main_window import MainWindow


class AppShell(MainWindow):
    pass


def build_application_window() -> QMainWindow:
    return AppShell()
