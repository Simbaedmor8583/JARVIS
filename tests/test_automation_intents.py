import pytest

from brain.router import fast_lane
from core.action_manager import ActionManager
from core.automation_intents import classify_automation_intent, normalize_automation_text


@pytest.mark.parametrize(
    ("command", "skill"),
    [
        ("Launch Word", "app.open"),
        ("Bring up Excel", "app.open"),
        ("I need Power Point", "app.open"),
        ("Create a proposal about employee training", "office.create_document"),
        ("Make a monthly household budget in Excel", "office.create_spreadsheet"),
        ("Create a ten-slide presentation about AI education", "office.create_presentation"),
        ("Open Google Drive", "browser.open_site"),
        ("Search Google for artificial intelligence education", "web.search"),
        ("Find emails from UMPI", "website.gmail_search"),
        ("Find my graduation transcript in Drive", "website.drive_search"),
        ("Fill this form", "browser.fill_form"),
        ("Submit the application", "browser.submit_form"),
        ("Stop all actions", "system.emergency_stop"),
    ],
)
def test_automation_variants_map_to_registered_intents(command, skill):
    intent = classify_automation_intent(command)
    assert intent["skill"] == skill
    assert intent["skill"] in ActionManager.INTENT_ALLOWLIST


def test_transcription_corrections_are_normalized():
    assert normalize_automation_text("open microsoft world") == "open Microsoft Word"
    assert normalize_automation_text("make it in excell") == "make it in Excel"


def test_fast_lane_uses_automation_parser_without_replacing_existing_rules():
    assert fast_lane("Launch Microsoft Word")["skill"] == "app.open"
    assert fast_lane("mute the volume")["skill"] == "system.volume"


def test_real_browser_commands_use_dedicated_routes():
    assert fast_lane("Open browser.") == {"skill": "browser.open", "params": {}}
    assert fast_lane("Search Google for artificial intelligence education.") == {
        "skill": "web.search", "params": {"query": "artificial intelligence education"},
    }
    assert fast_lane("Play the first result.") == {
        "skill": "browser.youtube_play_first", "params": {},
    }


def test_sensitive_web_operations_require_confirmation():
    manager = ActionManager(type("Controller", (), {})())
    submit = manager.action_from_intent({"skill": "browser.submit_form", "params": {}})
    upload = manager.action_from_intent({"skill": "browser.upload", "params": {"target": "file.pdf"}})
    password_fill = manager.action_from_intent({
        "skill": "browser.fill_form", "params": {"fields": {"password": "private"}},
    })
    safe_fill = manager.action_from_intent({
        "skill": "browser.fill_form", "params": {"fields": {"city": "Dubai"}},
    })
    assert submit.requires_confirmation is True
    assert upload.requires_confirmation is True
    assert password_fill.requires_confirmation is True
    assert safe_fill.requires_confirmation is False


def test_new_actions_have_explicit_permission_scopes():
    manager = ActionManager(type("Controller", (), {})())
    assert manager.action_from_intent({"skill": "browser.read_page", "params": {}}).permission_scope == "SAFE_READ"
    assert manager.action_from_intent({"skill": "office.create_document", "params": {}}).permission_scope == "OFFICE_EDIT"
    assert manager.action_from_intent({"skill": "browser.submit_form", "params": {}}).permission_scope == "FORM_SUBMIT"
