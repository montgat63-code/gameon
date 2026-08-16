from profile_store import GameProfile, ProfileStore


def test_profile_round_trip(tmp_path) -> None:
    store = ProfileStore(tmp_path)
    original = GameProfile(
        name="PUBG Mobile",
        display={"max_size": 1280, "max_fps": 60},
        bindings={"W": {"kind": "key", "action": "forward"}},
    )
    path = store.save(original)
    loaded = store.load("PUBG Mobile")
    assert path.name == "PUBG_Mobile.json"
    assert loaded.name == original.name
    assert loaded.display == original.display
    assert loaded.bindings == original.bindings
