"""
Desktop Organizer — sorts loose desktop files into category folders.
Nothing is ever deleted. Every move is logged to data/organizer_log.json,
and "undo organize" reverses the last session exactly.
"""
import json
import shutil
import time
from pathlib import Path

from config import Config

CATEGORIES = {
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md",
                  ".ppt", ".pptx", ".xls", ".xlsx", ".csv", ".epub"},
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp",
               ".ico", ".tiff", ".heic"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm",
               ".m4v"},
    "Music": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp",
             ".h", ".cs", ".json", ".xml", ".yml", ".yaml", ".sql", ".sh",
             ".bat", ".ps1", ".ipynb"},
    "Installers": {".exe", ".msi", ".msix", ".dmg", ".pkg"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"},
    "Shortcuts": {".lnk", ".url", ".webloc"},
}
SKIP_NAMES = {"desktop.ini", "thumbs.db", ".gitkeep"}


def _category_for(path):
    ext = path.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"


def _unique_dest(dest):
    if not dest.exists():
        return dest
    stem, suffix = dest.stem, dest.suffix
    i = 1
    while True:
        cand = dest.with_name(f"{stem} ({i}){suffix}")
        if not cand.exists():
            return cand
        i += 1


def _load_log():
    try:
        if Config.ORGANIZER_LOG.exists():
            return json.loads(Config.ORGANIZER_LOG.read_text(encoding="utf-8"))
    except Exception:
        pass
    return []


def _save_log(log):
    try:
        Config.ORGANIZER_LOG.write_text(
            json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def organize(ctx):
    desktop = Config.DESKTOP_PATH
    if not desktop.exists():
        return "I can't see your desktop, sir."

    category_dirs = set(CATEGORIES.keys()) | {"Other", "Projects", "JARVIS"}
    moves = []
    counts = {}

    try:
        for item in list(desktop.iterdir()):
            if item.is_dir():
                continue                      # never touch folders
            if item.name.lower() in SKIP_NAMES:
                continue
            cat = _category_for(item)
            dest_dir = desktop / cat
            try:
                dest_dir.mkdir(exist_ok=True)
                dest = _unique_dest(dest_dir / item.name)
                shutil.move(str(item), str(dest))
                moves.append({"src": str(item), "dst": str(dest)})
                counts[cat] = counts.get(cat, 0) + 1
            except Exception:
                continue
    except Exception as exc:
        return f"The scan failed, sir: {exc}."

    if not moves:
        return "Your desktop is already tidy, sir. Nothing to organize."

    log = _load_log()
    log.append({
        "session_id": f"org_{int(time.time())}",
        "time": time.time(),
        "moves": moves,
    })
    _save_log(log)

    parts = [f"Organized {len(moves)} files, sir."]
    for cat, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        parts.append(f"{cat}: {n}.")
    parts.append("Say 'undo organize' if you'd like it all back.")
    return " ".join(parts)


def undo(ctx):
    log = _load_log()
    if not log:
        return "There's nothing to undo, sir."
    session = log.pop()
    restored, failed = 0, 0
    for mv in reversed(session.get("moves", [])):
        try:
            src, dst = Path(mv["src"]), Path(mv["dst"])
            if dst.exists() and not src.exists():
                shutil.move(str(dst), str(src))
                restored += 1
            elif dst.exists() and src.exists():
                # original spot taken — leave file where it is
                failed += 1
        except Exception:
            failed += 1
    _save_log(log)
    if restored == 0 and failed == 0:
        return "Nothing from the last session needed moving back, sir."
    msg = f"Restored {restored} file{'s' if restored != 1 else ''} to the desktop, sir."
    if failed:
        msg += f" {failed} couldn't be moved back."
    return msg


# ---------------------------------------------------------------------------
# Skill dispatch entry
# ---------------------------------------------------------------------------
def handle(intent, ctx):
    skill = intent.get("skill")
    if skill == "desktop.organize":
        return organize(ctx)
    if skill == "desktop.undo":
        return undo(ctx)
    return None
