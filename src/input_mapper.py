"""Input mapping contracts independent from transport implementation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class InputKind(StrEnum):
    KEY = "key"
    TOUCH = "touch"
    SWIPE = "swipe"


@dataclass(frozen=True, slots=True)
class MappedAction:
    kind: InputKind
    action: str
    payload: dict[str, Any]


class InputMapper:
    def __init__(self) -> None:
        self._enabled = False
        self._bindings: dict[str, MappedAction] = {}

    @property
    def enabled(self) -> bool:
        return self._enabled

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = bool(enabled)

    def set_bindings(self, bindings: dict[str, MappedAction]) -> None:
        self._bindings = dict(bindings)

    def map_key(self, key: str) -> MappedAction | None:
        if not self._enabled:
            return None
        return self._bindings.get(key)
