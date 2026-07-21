"""Reliable Windows target resolution for files, folders, apps, and websites."""
import os
import re
import shutil
import winreg
import ctypes
import uuid
from dataclasses import dataclass
from pathlib import Path

from config import Config
from skills.browser import KNOWN_SITES, normalize_url


@dataclass(frozen=True)
class WindowsTarget:
    kind: str
    name: str
    value: str


def _known_folder_path(guid_text):
    """Resolve a Windows Known Folder through SHGetKnownFolderPath."""
    try:
        guid = uuid.UUID(guid_text.strip("{}"))
        data = (ctypes.c_ubyte * 16).from_buffer_copy(guid.bytes_le)
        path_ptr = ctypes.c_wchar_p()
        result = ctypes.windll.shell32.SHGetKnownFolderPath(
            ctypes.byref(data), 0, None, ctypes.byref(path_ptr)
        )
        if result != 0 or not path_ptr.value:
            return None
        path = Path(path_ptr.value)
        ctypes.windll.ole32.CoTaskMemFree(path_ptr)
        return path if path.exists() else None
    except Exception:
        return None


def _registry_shell_folder(value_name):
    keys = (
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"),
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"),
    )
    for hive, key_name in keys:
        try:
            with winreg.OpenKey(hive, key_name) as key:
                value, _ = winreg.QueryValueEx(key, value_name)
                path = Path(os.path.expandvars(str(value))).expanduser()
                if path.exists():
                    return path
        except OSError:
            continue
    return None


def known_folders():
    home = Path.home()
    onedrive = Path(os.environ.get("OneDrive", home / "OneDrive"))
    candidates = {
        "desktop": _known_folder_path("{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}") or _registry_shell_folder("Desktop") or Config.DESKTOP_PATH,
        "documents": _known_folder_path("{FDD39AD0-238F-46AF-ADB4-6C85480369C7}") or _registry_shell_folder("Personal") or home / "Documents",
        "downloads": _known_folder_path("{374DE290-123F-4565-9164-39C4925E467B}") or _registry_shell_folder("{374DE290-123F-4565-9164-39C4925E467B}") or home / "Downloads",
        "pictures": _known_folder_path("{33E28130-4E1E-4676-835A-98395C3BC3BB}") or _registry_shell_folder("My Pictures") or home / "Pictures",
        "videos": _known_folder_path("{18989B1D-99B5-455B-841C-AB7C74E4DDFC}") or _registry_shell_folder("My Video") or home / "Videos",
        "music": _known_folder_path("{4BD8D571-6D19-48D3-BE97-422220080E43}") or _registry_shell_folder("My Music") or home / "Music",
        "recent files": _known_folder_path("{AE50C081-EBD2-438A-8655-8A092E34987A}") or Path(os.environ.get("APPDATA", home)) / "Microsoft" / "Windows" / "Recent",
        "startup": _known_folder_path("{B97D20BB-F46A-4C97-BA10-5E3608430854}") or Path(os.environ.get("APPDATA", home)) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup",
        "appdata": Path(os.environ.get("APPDATA", home / "AppData" / "Roaming")),
        "local appdata": Path(os.environ.get("LOCALAPPDATA", home / "AppData" / "Local")),
        "onedrive": onedrive,
        "user profile": home,
        "home": home,
        "project": Config.SOURCE_DIR,
        "jarvis project": Config.SOURCE_DIR,
        "jarvis": Config.SOURCE_DIR,
    }
    if (onedrive / "Desktop").exists():
        candidates["onedrive desktop"] = onedrive / "Desktop"
    return {key: Path(value) for key, value in candidates.items() if value and Path(value).exists()}


def clean_target_name(text):
    value = (text or "").strip().strip('"').strip("'")
    value = re.sub(r"^(?:my|the)\s+", "", value, flags=re.I)
    value = re.sub(r"\s+(?:folder|directory|file|application|app)$", "", value, flags=re.I)
    return value.strip()


def _app_path(executable):
    direct = shutil.which(executable)
    if direct:
        return direct
    exe_name = executable if executable.lower().endswith(".exe") else executable + ".exe"
    for hive in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
        for key_name in (
            rf"Software\Microsoft\Windows\CurrentVersion\App Paths\{exe_name}",
            rf"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths\{exe_name}",
        ):
            try:
                with winreg.OpenKey(hive, key_name) as key:
                    path, _ = winreg.QueryValueEx(key, None)
                    if Path(path).exists():
                        return path
            except OSError:
                continue
    return None


APP_EXECUTABLES = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "command prompt": "cmd.exe",
    "cmd": "cmd.exe",
    "powershell": "powershell.exe",
    "task manager": "taskmgr.exe",
    "terminal": "wt.exe",
    "windows terminal": "wt.exe",
    "file explorer": "explorer.exe",
    "settings": "SystemSettings.exe",
    "snipping tool": "SnippingTool.exe",
    "media player": "Microsoft.Media.Player.exe",
    "microsoft word": "winword.exe",
    "word": "winword.exe",
    "microsoft excel": "excel.exe",
    "excel": "excel.exe",
    "microsoft powerpoint": "powerpnt.exe",
    "powerpoint": "powerpnt.exe",
    "microsoft outlook": "outlook.exe",
    "outlook": "outlook.exe",
    "microsoft onenote": "onenote.exe",
    "onenote": "onenote.exe",
    "edge": "msedge.exe",
    "microsoft edge": "msedge.exe",
    "chrome": "chrome.exe",
    "google chrome": "chrome.exe",
}


def resolve_windows_target(raw_target, preferred_kind=None):
    original = (raw_target or "").strip()
    target = clean_target_name(original)
    low = target.lower()
    folders = known_folders()

    shell_targets = {
        "this pc": "shell:MyComputerFolder",
        "recycle bin": "shell:RecycleBinFolder",
        "network": "shell:NetworkPlacesFolder",
    }

    if low in shell_targets:
        return WindowsTarget("shell", target.title(), shell_targets[low])

    if low in folders:
        return WindowsTarget("folder", target.title(), str(folders[low]))
    if low in ("profile", "user", "user folder", "user profile folder") and "user profile" in folders:
        return WindowsTarget("folder", "User profile", str(folders["user profile"]))

    expanded = Path(os.path.expandvars(target)).expanduser()
    candidates = [expanded]
    if not expanded.is_absolute():
        candidates.extend((Config.SOURCE_DIR / expanded, Config.DESKTOP_PATH / expanded, Path.home() / expanded))
    for path in candidates:
        if path.exists():
            return WindowsTarget("folder" if path.is_dir() else "file", path.name, str(path.resolve()))

    app_key = re.sub(r"^(?:open|launch|start)\s+", "", low).strip()
    if preferred_kind not in (None, "app"):
        return None
    if app_key in APP_EXECUTABLES:
        executable = APP_EXECUTABLES[app_key]
        path = _app_path(executable)
        if path:
            return WindowsTarget("app", target, path)
        if executable in ("notepad.exe", "calc.exe", "mspaint.exe", "cmd.exe", "powershell.exe", "taskmgr.exe"):
            return WindowsTarget("app", target, executable)

    url = normalize_url(target)
    if url or low in KNOWN_SITES:
        return WindowsTarget("website", target, url or KNOWN_SITES[low])
    return None
