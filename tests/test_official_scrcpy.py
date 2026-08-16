from official_scrcpy import OfficialScrcpySession, ScrcpyConfig


def test_official_command_uses_matching_client_without_protected_setting(tmp_path) -> None:
    session = OfficialScrcpySession(tmp_path / "scrcpy.exe", tmp_path / "adb.exe")
    command = session.command("ABC123", ScrcpyConfig(max_size=720, max_fps=30))
    assert command[0].endswith("scrcpy.exe")
    assert "--serial" in command
    assert "ABC123" in command
    assert "--max-size" in command
    assert "720" in command
    assert "--max-fps" in command
    assert "stay_awake=true" not in command
