from adb_manager import parse_adb_devices


def test_parse_adb_devices_with_model() -> None:
    output = """List of devices attached
ABC123\tdevice product:foo model:Redmi_Note transport_id:1
"""
    devices = parse_adb_devices(output)
    assert len(devices) == 1
    assert devices[0].serial == "ABC123"
    assert devices[0].state == "device"
    assert devices[0].model == "Redmi Note"


def test_parse_adb_unauthorized_and_offline() -> None:
    output = """List of devices attached
A1\tunauthorized
B2\toffline
"""
    devices = parse_adb_devices(output)
    assert [(item.serial, item.state) for item in devices] == [
        ("A1", "unauthorized"),
        ("B2", "offline"),
    ]
