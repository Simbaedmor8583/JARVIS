"""Settings store load/save tests."""
from core.settings import SettingsStore, DEFAULTS


def test_defaults_present(tmp_path):
    store = SettingsStore(tmp_path / "config.json")
    data = store.as_dict()
    for key in ("microphone_device", "wake_threshold", "whisper_model",
                "openrouter_model", "minimize_to_tray", "reduce_motion"):
        assert key in data


def test_save_and_reload(tmp_path):
    path = tmp_path / "config.json"
    store = SettingsStore(path)
    store.set("wake_threshold", 0.7)
    store.set("reduce_motion", True)
    store.save()
    reloaded = SettingsStore(path)
    assert reloaded.get("wake_threshold") == 0.7
    assert reloaded.get("reduce_motion") is True


def test_update_ignores_unknown_keys(tmp_path):
    store = SettingsStore(tmp_path / "config.json")
    store.update({"wake_threshold": 0.9, "not_a_real_key": "x"})
    assert store.get("wake_threshold") == 0.9
    assert "not_a_real_key" not in store.as_dict()


def test_unknown_key_raises(tmp_path):
    store = SettingsStore(tmp_path / "config.json")
    try:
        store.set("bogus", 1)
        assert False, "expected KeyError"
    except KeyError:
        pass


def test_no_api_key_in_defaults():
    blob = " ".join(DEFAULTS.keys()).lower()
    assert "api" not in blob and "key" not in blob