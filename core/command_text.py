"""Speech-command normalization that removes common false starts conservatively."""
import re


NOISE_PREFIXES = (
    "window",
    "server",
    "microsoft no",
    "open window",
)


def cleanup_command(text):
    value = re.sub(r"\s+", " ", (text or "").strip())
    if not value:
        return ""
    changed = True
    while changed:
        changed = False
        cleaned = re.sub(r"^(?:uh|um|erm|hmm)[, ]+", "", value, flags=re.I)
        if cleaned != value:
            value = cleaned
            changed = True
        low = value.lower()
        for prefix in NOISE_PREFIXES:
            if low == prefix:
                return ""
            if low.startswith(prefix + " "):
                value = value[len(prefix):].lstrip(" ,.-")
                changed = True
                break
    words = value.split()
    while len(words) >= 2 and words[0].lower() == words[1].lower():
        words.pop(0)
    value = " ".join(words)
    return value.strip()
