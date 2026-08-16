"""Lightweight dark gaming theme."""

from __future__ import annotations


DARK_GAMING_STYLE = """
QMainWindow, QWidget {
    background: #0b1020;
    color: #e8eefc;
    font-size: 13px;
}
QLabel#connectionStatus {
    background: #111a30;
    border: 1px solid #22345c;
    border-radius: 8px;
    padding: 10px 12px;
    color: #8ce6c0;
}
QFrame#videoHost {
    background: #050812;
    border: 1px solid #293d6a;
    border-radius: 12px;
}
QFrame#sidePanel {
    background: #10182b;
    border: 1px solid #22345c;
    border-radius: 10px;
}
QLabel#panelTitle {
    color: #69b7ff;
    font-size: 15px;
    font-weight: 700;
}
QLabel#videoPlaceholder {
    color: #7183a8;
    font-size: 16px;
}
QSplitter::handle {
    background: #1d2b4a;
}
"""
