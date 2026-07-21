from core.capability_health import (
    CapabilityHealth, DEGRADED, REQUIRES_CONFIGURATION,
    REQUIRES_LOGIN, WORKING,
)


def test_health_reports_working_for_builtin_skill():
    result = CapabilityHealth().check("system_control")
    assert result.status == WORKING


def test_health_reports_missing_configuration(monkeypatch):
    monkeypatch.setattr("core.capability_health.Config.OPENROUTER_API_KEY", "")
    result = CapabilityHealth().check("chat")
    assert result.status == REQUIRES_CONFIGURATION
    assert "OPENROUTER_API_KEY" in result.detail


def test_health_rejects_placeholder_openrouter_key(monkeypatch):
    monkeypatch.setattr(
        "core.capability_health.Config.OPENROUTER_API_KEY", "your_key_here"
    )
    result = CapabilityHealth().check("chat")
    assert result.status == REQUIRES_CONFIGURATION


def test_health_reports_login_requirement():
    result = CapabilityHealth().check("gmail")
    assert result.status == REQUIRES_LOGIN


def test_health_check_failure_is_degraded(monkeypatch):
    monkeypatch.setattr("core.capability_health.importlib.util.find_spec",
                        lambda name: None)
    result = CapabilityHealth().check("browser")
    assert result.status == DEGRADED
