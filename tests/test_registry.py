from core.registry import SessionRegistry
from skills.system_control import close_thing


def test_close_recent_closes_newest(tmp_path):
    order = []
    registry = SessionRegistry(tmp_path / "registry.json")
    registry.open_item("app", "First", closer=lambda: order.append("first"))
    registry.open_item("app", "Second", closer=lambda: order.append("second"))
    result = registry.close_recent()
    assert result["entry"]["name"] == "Second"
    assert order == ["second"]


def test_close_by_name_fuzzy_matches(tmp_path):
    closed = []
    registry = SessionRegistry(tmp_path / "registry.json")
    registry.register("browser_tab", "YouTube Music", closer=lambda: closed.append(True))
    results = registry.close_by_name("youtub")
    assert len(results) == 1
    assert results[0]["closed"] is True
    assert closed == [True]


def test_close_all_uses_reverse_order(tmp_path):
    order = []
    registry = SessionRegistry(tmp_path / "registry.json")
    for name in ("one", "two", "three"):
        registry.register("app", name, closer=lambda value=name: order.append(value))
    registry.close_all()
    assert order == ["three", "two", "one"]
    assert registry.get_status() == []


def test_close_everything_reports_empty_registry(tmp_path):
    registry = SessionRegistry(tmp_path / "registry.json")
    ctx = type("Context", (), {"registry": registry})()
    assert close_thing("__all__", ctx) == "There's nothing open at the moment, sir."


def test_previous_runtime_entries_are_not_owned_after_restart(tmp_path):
    path = tmp_path / "registry.json"
    first = SessionRegistry(path)
    first.register("app", "Notepad", pid=12345)
    second = SessionRegistry(path)
    assert second.get_status() == []
    assert second.close_all() == []
