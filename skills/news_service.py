"""
NewsService - structured news access for the GUI panel + voice.

Wraps the existing skills/news.py RSS engine (no API key needed, cached,
never fabricates) and returns clean headline dicts for the GUI: title,
source, published time, summary and link. Failed sources are logged and
skipped so other feeds still load.
"""
import time

from voice import audio_log


class NewsService:
    def __init__(self, ctx):
        self.ctx = ctx
        self._headlines = []
        self._last_refresh = 0.0
        self._topic = "top"

    @property
    def last_refresh(self):
        return self._last_refresh

    def headlines(self, topic="top", limit=8, force=False):
        """Return a list of headline dicts for the GUI panel."""
        try:
            from skills import news as news_mod
        except Exception as exc:
            audio_log.log_error(f"[news] import failed: {exc}", exc)
            return []
        self._topic = topic
        try:
            entries = news_mod.fetch_headlines(topic, limit=limit)
        except Exception as exc:
            audio_log.log_error(f"[news] fetch failed for '{topic}': {exc}", exc)
            entries = []
        out = []
        for e in entries[:limit]:
            out.append({
                "title": e.get("title", ""),
                "source": e.get("source", ""),
                "published": e.get("published", ""),
                "summary": e.get("summary", e.get("title", "")),
                "link": e.get("link", ""),
            })
        self._headlines = out
        self._last_refresh = time.time()
        audio_log.log(f"[news] loaded {len(out)} headlines for '{topic}'")
        return out

    def cached(self):
        return list(self._headlines)

    def read_headline(self, index=0):
        """Speak one headline + summary through the shared speech service."""
        if not self._headlines:
            return "No headlines loaded yet, sir."
        if index < 0 or index >= len(self._headlines):
            return f"I only have {len(self._headlines)} stories, sir."
        item = self._headlines[index]
        text = f"{item['title']}. {item['summary']}"
        self.controller_speak(text)
        return text

    def controller_speak(self, text):
        speaker = getattr(self.ctx, "speaker", None)
        if speaker is not None:
            try:
                speaker.speak(text)
            except Exception:
                pass

    def last_refresh_str(self):
        if not self._last_refresh:
            return "never"
        return time.strftime("%H:%M:%S", time.localtime(self._last_refresh))