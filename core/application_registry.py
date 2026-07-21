"""Discoverable Windows application registry used by deterministic routing."""
import os
import shutil
import winreg
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class ApplicationEntry:
    canonical_name: str
    aliases: tuple[str, ...] = ()
    executable_candidates: tuple[str, ...] = ()
    app_user_model_id: str | None = None
    start_menu_entry: str | None = None
    process_names: tuple[str, ...] = ()
    window_title_patterns: tuple[str, ...] = ()
    launch_method: str = "executable"
    close_method: str = "window"
    installed: bool = False
    executable_path: str | None = None

    def to_dict(self):
        return asdict(self)


DEFAULT_APPLICATIONS = (
    ApplicationEntry("notepad", ("notepad",), ("notepad.exe",), process_names=("notepad.exe",), window_title_patterns=("Notepad",)),
    ApplicationEntry("calculator", ("calculator", "calc"), ("calc.exe",), process_names=("CalculatorApp.exe", "calc.exe"), window_title_patterns=("Calculator",)),
    ApplicationEntry("file explorer", ("file explorer", "explorer"), ("explorer.exe",), process_names=("explorer.exe",), window_title_patterns=("File Explorer",)),
    ApplicationEntry("microsoft word", ("word", "microsoft word"), ("winword.exe",), process_names=("WINWORD.EXE",), window_title_patterns=("Word",)),
    ApplicationEntry("microsoft excel", ("excel", "microsoft excel"), ("excel.exe",), process_names=("EXCEL.EXE",), window_title_patterns=("Excel",)),
    ApplicationEntry("microsoft powerpoint", ("powerpoint", "microsoft powerpoint"), ("powerpnt.exe",), process_names=("POWERPNT.EXE",), window_title_patterns=("PowerPoint",)),
    ApplicationEntry("microsoft outlook", ("outlook", "microsoft outlook"), ("outlook.exe",), process_names=("OUTLOOK.EXE",), window_title_patterns=("Outlook",)),
    ApplicationEntry("microsoft onenote", ("onenote", "microsoft onenote"), ("onenote.exe",), process_names=("ONENOTE.EXE",), window_title_patterns=("OneNote",)),
    ApplicationEntry("microsoft edge", ("edge", "microsoft edge"), ("msedge.exe",), process_names=("msedge.exe",), window_title_patterns=("Edge",)),
    ApplicationEntry("google chrome", ("chrome", "google chrome"), ("chrome.exe",), process_names=("chrome.exe",), window_title_patterns=("Chrome",)),
    ApplicationEntry("settings", ("settings",), ("SystemSettings.exe",), app_user_model_id="windows.immersivecontrolpanel_cw5n1h2txyewy!microsoft.windows.immersivecontrolpanel", process_names=("SystemSettings.exe",), window_title_patterns=("Settings",), launch_method="uri"),
    ApplicationEntry("task manager", ("task manager",), ("taskmgr.exe",), process_names=("Taskmgr.exe",), window_title_patterns=("Task Manager",)),
    ApplicationEntry("paint", ("paint",), ("mspaint.exe",), process_names=("mspaint.exe",), window_title_patterns=("Paint",)),
    ApplicationEntry("snipping tool", ("snipping tool",), ("SnippingTool.exe",), process_names=("SnippingTool.exe",), window_title_patterns=("Snipping Tool",)),
    ApplicationEntry("terminal", ("terminal", "windows terminal"), ("wt.exe",), process_names=("WindowsTerminal.exe",), window_title_patterns=("Terminal",)),
    ApplicationEntry("powershell", ("powershell",), ("powershell.exe",), process_names=("powershell.exe",), window_title_patterns=("PowerShell",)),
    ApplicationEntry("command prompt", ("command prompt", "cmd"), ("cmd.exe",), process_names=("cmd.exe",), window_title_patterns=("Command Prompt",)),
    ApplicationEntry("control panel", ("control panel",), ("control.exe",), process_names=("control.exe",), window_title_patterns=("Control Panel",)),
    ApplicationEntry("media player", ("media player",), ("Microsoft.Media.Player.exe", "wmplayer.exe"), process_names=("Microsoft.Media.Player.exe", "wmplayer.exe"), window_title_patterns=("Media Player",)),
)


class ApplicationRegistry:
    def __init__(self):
        self._entries = {entry.canonical_name: entry for entry in DEFAULT_APPLICATIONS}
        self._aliases = {}
        self.refresh()

    def refresh(self):
        start_menu = self._start_menu_shortcuts()
        self._aliases.clear()
        for entry in self._entries.values():
            path = self._find_executable(entry.executable_candidates)
            shortcut = self._find_shortcut(entry, start_menu)
            entry.executable_path = path
            entry.start_menu_entry = str(shortcut) if shortcut else None
            entry.installed = bool(path or shortcut or entry.launch_method == "uri")
            for alias in (entry.canonical_name, *entry.aliases):
                self._aliases[alias.lower()] = entry.canonical_name
        self._add_discovered_start_menu(start_menu)
        self._add_discovered_app_paths()
        return self.entries()

    def resolve(self, name):
        canonical = self._aliases.get((name or "").strip().lower())
        return self._entries.get(canonical) if canonical else None

    def entries(self):
        return list(self._entries.values())

    def installed_entries(self):
        return [entry for entry in self.entries() if entry.installed]

    @staticmethod
    def _start_menu_shortcuts():
        roots = (
            Path(os.environ.get("PROGRAMDATA", "")) / "Microsoft" / "Windows" / "Start Menu" / "Programs",
            Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "Start Menu" / "Programs",
        )
        shortcuts = {}
        for root in roots:
            try:
                for shortcut in root.rglob("*.lnk"):
                    shortcuts[shortcut.stem.lower()] = shortcut
            except OSError:
                continue
        return shortcuts

    @staticmethod
    def _find_shortcut(entry, shortcuts):
        for alias in (entry.canonical_name, *entry.aliases):
            if alias.lower() in shortcuts:
                return shortcuts[alias.lower()]
        return None

    @staticmethod
    def _find_executable(candidates):
        for candidate in candidates:
            direct = shutil.which(candidate)
            if direct:
                return direct
            for hive in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
                for key_name in (
                    rf"Software\Microsoft\Windows\CurrentVersion\App Paths\{candidate}",
                    rf"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths\{candidate}",
                ):
                    try:
                        with winreg.OpenKey(hive, key_name) as key:
                            value, _ = winreg.QueryValueEx(key, None)
                        if Path(value).exists():
                            return str(Path(value))
                    except OSError:
                        continue
        return None

    def _add_discovered_start_menu(self, shortcuts):
        known_aliases = set(self._aliases)
        for stem, shortcut in shortcuts.items():
            if stem in known_aliases or stem in self._entries:
                continue
            entry = ApplicationEntry(
                canonical_name=stem,
                aliases=(stem,),
                start_menu_entry=str(shortcut),
                process_names=(),
                window_title_patterns=(shortcut.stem,),
                launch_method="shortcut",
                installed=True,
            )
            self._entries[stem] = entry
            self._aliases[stem] = stem

    def _add_discovered_app_paths(self):
        roots = (
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\App Paths"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\App Paths"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths"),
        )
        for hive, root_name in roots:
            try:
                with winreg.OpenKey(hive, root_name) as root:
                    index = 0
                    while True:
                        try:
                            subkey_name = winreg.EnumKey(root, index)
                            index += 1
                        except OSError:
                            break
                        try:
                            with winreg.OpenKey(root, subkey_name) as subkey:
                                value, _ = winreg.QueryValueEx(subkey, None)
                            executable = Path(value)
                            if not executable.exists():
                                continue
                            stem = executable.stem.lower()
                            if stem in self._aliases:
                                continue
                            entry = ApplicationEntry(
                                canonical_name=stem,
                                aliases=(stem,),
                                executable_candidates=(executable.name,),
                                process_names=(executable.name,),
                                window_title_patterns=(executable.stem,),
                                installed=True,
                                executable_path=str(executable),
                            )
                            self._entries[stem] = entry
                            self._aliases[stem] = stem
                        except OSError:
                            continue
            except OSError:
                continue
