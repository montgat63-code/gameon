"""Versioned JSON profile storage."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


CURRENT_SCHEMA = 1


@dataclass(slots=True)
class GameProfile:
    name: str
    schema: int = CURRENT_SCHEMA
    display: dict[str, Any] = field(default_factory=dict)
    bindings: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "name": self.name,
            "display": self.display,
            "bindings": self.bindings,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GameProfile":
        name = str(data.get("name", "Unnamed"))
        return cls(
            name=name,
            schema=int(data.get("schema", CURRENT_SCHEMA)),
            display=dict(data.get("display", {})),
            bindings=dict(data.get("bindings", {})),
            metadata=dict(data.get("metadata", {})),
        )


class ProfileStore:
    def __init__(self, directory: str | Path) -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def save(self, profile: GameProfile) -> Path:
        target = self.directory / f"{safe_name(profile.name)}.json"
        target.write_text(
            json.dumps(profile.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return target

    def load(self, name: str) -> GameProfile:
        source = self.directory / f"{safe_name(name)}.json"
        data = json.loads(source.read_text(encoding="utf-8"))
        return GameProfile.from_dict(data)

    def list_profiles(self) -> list[str]:
        return sorted(path.stem for path in self.directory.glob("*.json"))


def safe_name(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in "-_ " else "_" for ch in value)
    return cleaned.strip().replace(" ", "_") or "profile"
