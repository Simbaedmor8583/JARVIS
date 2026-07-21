"""File search and open helpers."""
import os

from skills.system_control import _search_files


def search(name):
    return _search_files((name or "").strip())


def search_and_open(name, ctx=None):
    path = search(name)
    if path is None:
        return None
    os.startfile(str(path))
    if ctx is not None:
        ctx.registry.register(
            "document", path.name, window_title=path.stem, extra={"path": str(path)}
        )
    return path
