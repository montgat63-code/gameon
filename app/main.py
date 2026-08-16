"""GameMaster application entry point."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from app_shell import build_application_window


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("GameMaster")
    app.setOrganizationName("GameMaster")
    window = build_application_window()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
