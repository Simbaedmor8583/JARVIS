"""
Music & Media — interactive YouTube playback through the shared browser.

"play music"          -> asks what you're in the mood for, then plays it
"play <song/artist>"  -> goes straight to playback
"pause / resume / next / mute the music / stop the music"
Playback happens in a registered browser tab, so "close it" also works.
"""
import time
from urllib.parse import quote_plus

from config import Config


# ---------------------------------------------------------------------------
# Playback
# ---------------------------------------------------------------------------
def _youtube_search_url(query):
    suffix = Config.MUSIC_SEARCH_SUFFIX.strip()
    q = f"{query} {suffix}".strip()
    return "https://www.youtube.com/results?search_query=" + quote_plus(q)


def _dismiss_consent(page):
    """Best-effort: clear YouTube/GDPR consent overlays."""
    candidates = [
        "button[aria-label*='Accept all']",
        "button[aria-label*='Accept the use']",
        "button[aria-label*='Agree']",
        "button:has-text('Accept all')",
        "button:has-text('I agree')",
    ]
    for sel in candidates:
        try:
            el = page.query_selector(sel)
            if el and el.is_visible():
                el.click()
                page.wait_for_timeout(800)
                return True
        except Exception:
            continue
    return False


def _click_first_video(page, ctx):
    """Click the first real video result. Returns True if playback started."""
    selectors = [
        "ytd-video-renderer a#video-title",
        "ytd-video-renderer a#thumbnail",
        "a#video-title-link",
        "ytd-rich-item-renderer a#thumbnail",
    ]
    try:
        page.wait_for_selector(
            "ytd-video-renderer, ytd-rich-item-renderer, a#video-title-link",
            timeout=15000,
        )
    except Exception:
        pass
    _dismiss_consent(page)
    for sel in selectors:
        try:
            els = page.query_selector_all(sel)
            for el in els[:6]:
                try:
                    if el.is_visible():
                        el.click()
                        return True
                except Exception:
                    continue
        except Exception:
            continue
    return False


def play(query, ctx):
    query = (query or "").strip()
    if not query:
        return ask_preference(ctx)

    url = _youtube_search_url(query)
    page = ctx.browser.open_site(url, name=f"Music: {query}")
    if page is None:
        try:
            import webbrowser
            webbrowser.open(url)
            return f"Playing {query} on YouTube, sir."
        except Exception:
            return "I couldn't reach YouTube, sir."

    if _click_first_video(page, ctx):
        ctx.state["music_query"] = query
        ctx.state["music_tab_name"] = f"Music: {query}"
        return f"Playing {query} on YouTube, sir."

    # Fallback: pyautogui click near the first result
    try:
        import pyautogui
        time.sleep(1.5)
        pyautogui.click(x=400, y=400)
        ctx.state["music_query"] = query
        ctx.state["music_tab_name"] = f"Music: {query}"
        return f"Playing {query} on YouTube, sir."
    except Exception:
        return (f"I opened the YouTube results for {query}, but couldn't "
                f"start playback automatically. One click should do it, sir.")


def ask_preference(ctx):
    """Interactive flow: ask what to play, answer arrives as next utterance."""
    ctx.speaker.speak(
        "Certainly, sir. What are you in the mood for — "
        "a genre, an artist, or a specific song?")
    ctx.pending = {"kind": "music_choice"}
    return None


# ---------------------------------------------------------------------------
# Controls
# ---------------------------------------------------------------------------
def _find_music_page(ctx):
    """Locate the live music tab through the registry."""
    name = ctx.state.get("music_tab_name")
    entries = ctx.registry.find_by_name(name) if name else []
    if not entries:
        entries = ctx.registry.find_by_name("music")
    if not entries:
        entries = ctx.registry.find_by_name("youtube")
    for e in entries:
        page = e.get("_page")
        if page is not None:
            try:
                if not page.is_closed():
                    return page
            except Exception:
                continue
    return None


def control(action, ctx):
    page = _find_music_page(ctx)

    if action == "stop":
        if page is not None:
            try:
                page.close()
            except Exception:
                pass
        ctx.state.pop("music_tab_name", None)
        ctx.state.pop("music_query", None)
        return "Music stopped, sir."

    if page is not None:
        try:
            page.bring_to_front()
        except Exception:
            pass
        try:
            if action in ("pause", "resume"):
                page.keyboard.press("k")
                return "Paused." if action == "pause" else "Resuming."
            if action == "next":
                page.keyboard.press("Shift+N")
                return "Skipping ahead."
            if action == "mute":
                page.keyboard.press("m")
                return "Music muted."
        except Exception:
            pass

    # Fallback: OS media keys
    try:
        import pyautogui
        if action in ("pause", "resume"):
            pyautogui.press("playpause")
            return "Done."
        if action == "next":
            pyautogui.press("nexttrack")
            return "Skipping ahead."
        if action == "mute":
            pyautogui.press("volumemute")
            return "Muted."
    except Exception:
        pass
    return "I can't find an active music tab, sir."


# ---------------------------------------------------------------------------
# Skill dispatch entry
# ---------------------------------------------------------------------------
def handle(intent, ctx):
    skill = intent.get("skill")
    params = intent.get("params", {}) or {}

    if skill == "media.play_music":
        return play(params.get("query", ""), ctx)
    if skill == "media.control":
        return control(params.get("action", "pause"), ctx)
    return None
