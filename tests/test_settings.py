from diagnostics import summarize_failure
from settings_store import SettingsStore


def test_settings_round_trip(tmp_path) -> None:
    store = SettingsStore(tmp_path / "settings.json")
    store.save({"zoom": 1.25, "left_panel": True})
    assert store.load() == {"zoom": 1.25, "left_panel": True}


def test_failure_summary() -> None:
    message = summarize_failure("ADB", RuntimeError("device offline"))
    assert message == "ADB: RuntimeError: device offline"
