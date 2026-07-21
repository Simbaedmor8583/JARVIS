"""
Office unsaved-changes detection and save/discard via COM automation.

Used by the GUI/controller before closing Microsoft Word, Excel, or
PowerPoint so the user can be asked whether to save, discard, or cancel
instead of losing work. Everything degrades gracefully to "unknown" when
the Office app is not running or COM is unavailable.
"""

# COM prog ids per supported office app
_PROGIS = {
    "word": "Word.Application",
    "microsoft word": "Word.Application",
    "winword": "Word.Application",
    "excel": "Excel.Application",
    "microsoft excel": "Excel.Application",
    "powerpoint": "PowerPoint.Application",
    "microsoft powerpoint": "PowerPoint.Application",
    "powerpnt": "PowerPoint.Application",
}


def _progid_for(name):
    return _PROGIS.get((name or "").strip().lower())


def is_office_app(name):
    return _progid_for(name) is not None


def _get_app(name):
    progid = _progid_for(name)
    if progid is None:
        return None
    try:
        import win32com.client
        return win32com.client.GetActiveObject(progid)
    except Exception:
        return None


def _documents(app, progid):
    try:
        if progid.startswith("Word"):
            return list(app.Documents)
        if progid.startswith("Excel"):
            return list(app.Workbooks)
        if progid.startswith("PowerPoint"):
            return list(app.Presentations)
    except Exception:
        return []
    return []


def has_unsaved_changes(name):
    """Return True/False when determinable, None when unknown."""
    app = _get_app(name)
    if app is None:
        return None
    progid = _progid_for(name)
    try:
        for doc in _documents(app, progid):
            try:
                if progid.startswith("Excel"):
                    if not doc.Saved:
                        return True
                elif not doc.Saved:
                    return True
            except Exception:
                continue
        return False
    except Exception:
        return None


def resolve_unsaved(name, choice):
    """
    Apply the user's decision for an Office app with unsaved work.
    choice: "save" | "discard" | "cancel"
    Returns a spoken result string.
    """
    app = _get_app(name)
    if app is None:
        return f"{name} is not running, sir."
    progid = _progid_for(name)
    docs = _documents(app, progid)
    if choice == "cancel":
        return f"Closing {name} cancelled, sir."
    try:
        for doc in docs:
            try:
                if choice == "save":
                    doc.Save()
                else:  # discard
                    doc.Close(SaveChanges=False)
            except Exception:
                continue
        if choice == "save":
            try:
                app.Quit()
            except Exception:
                pass
            return f"Saved and closed {name}, sir."
        try:
            app.Quit()
        except Exception:
            pass
        return f"Closed {name} without saving, sir."
    except Exception as exc:
        return f"I couldn't {choice} {name}: {exc}."