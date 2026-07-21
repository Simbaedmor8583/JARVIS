"""
JARVIS desktop (GUI) entry point.

Launches the PySide6 window first, then loads the assistant backend in the
background with staged status updates. Console output appears only when
launched with --debug. Normal mode opens a graphical window with no console.

    python desktop_main.py            # GUI, no console output
    python desktop_main.py --debug    # GUI + console diagnostics
"""
import argparse
import sys


def _parse_args(argv=None):
    p = argparse.ArgumentParser(description="JARVIS desktop GUI")
    p.add_argument("--debug", action="store_true", help="console diagnostics")
    p.add_argument("--skip-model-preload", action="store_true",
                   help="skip background model preload for faster startup")
    p.add_argument("--voice-diagnostic", action="store_true",
                   help="log live wake-word score/level/fps diagnostics")
    p.add_argument("--start-voice", action="store_true",
                   help="begin listening immediately after startup")
    return p.parse_args(argv)


def main(argv=None):
    args = _parse_args(argv)

    from PySide6.QtCore import Qt, QTimer
    from PySide6.QtWidgets import QApplication, QSystemTrayIcon

    from config import ensure_dirs
    from core.settings import SettingsStore
    from gui import styles
    from gui.workers import GuiController
    from gui.main_window import MainWindow
    from gui.settings_window import SettingsWindow
    from gui.tray import TrayIcon

    ensure_dirs()

    app = QApplication(sys.argv[:1])
    app.setApplicationName("JARVIS")
    app.setQuitOnLastWindowClosed(False)   # live in tray after window closes

    settings = SettingsStore()
    app.setStyleSheet(styles.theme_stylesheet(
        bool(settings.get("reduce_motion", False))
    ))

    # ---- startup status ------------------------------------------------
    def startup_status(msg):
        window.current_status.setText(f"Status: {msg}")
        window.status_chip.setText(msg.upper())

    # ---- controller + window ---------------------------------------------
    gui_controller = GuiController(skip_preload=args.skip_model_preload,
                                   debug=args.debug)
    gui_controller.controller.voice_diagnostic = args.voice_diagnostic
    gui_controller.controller.attach_settings(settings)
    window = MainWindow(gui_controller, settings)
    window.showMaximized()
    startup_status("Starting JARVIS")

    # ---- tray --------------------------------------------------------------
    tray = TrayIcon(app)
    tray.show()

    # ---- settings window ------------------------------------------------------
    # Keep a persistent reference so the dialog is never garbage-collected.
    app_state = {"settings_window": None}

    def open_settings():
        from voice import audio_log
        audio_log.log("Settings button clicked")
        try:
            dlg = app_state.get("settings_window")
            if dlg is None:
                dlg = SettingsWindow(
                    settings, gui_controller=gui_controller, parent=window
                )
                app_state["settings_window"] = dlg
                audio_log.log("Settings window created")
            dlg._load()               # refresh from current config each open
            dlg._populate_devices()
            audio_log.log("Settings loaded")
            dlg.show()
            dlg.raise_()
            dlg.activateWindow()
            audio_log.log("Settings window shown")
        except Exception as exc:
            audio_log.log_error(f"Settings error: {exc}", exc)
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(window, "Settings", f"Could not open settings: {exc}")

    window.settingsRequested.connect(open_settings)
    tray.settingsRequested.connect(open_settings)

    # ---- minimize / close-to-tray -------------------------------------------
    def minimize_to_tray():
        window.hide()
        tray.notify("JARVIS", "Still running in the system tray, sir.")

    window.minimizeRequested.connect(minimize_to_tray)

    def show_window():
        window.showNormal()
        window.raise_()
        window.activateWindow()

    tray.openRequested.connect(show_window)

    # ---- voice / mute / logs from tray ---------------------------------------
    tray.startVoiceRequested.connect(window._on_start_voice)
    tray.stopVoiceRequested.connect(window._on_stop_voice)
    tray.logsRequested.connect(window._on_logs)

    def tray_mute():
        window.btn_mute.setChecked(not window.btn_mute.isChecked())
        window._on_mute(window.btn_mute.isChecked())

    tray.muteRequested.connect(tray_mute)

    # ---- staged background startup ---------------------------------------------
    stages = [
        "Loading configuration", "Loading microphone", "Loading Whisper",
        "Loading wake word", "Loading Piper", "Loading browser support",
        "Loading assistant backend",
    ]

    def run_startup():
        for msg in stages:
            # marshal to GUI thread via the bridge status signal
            gui_controller.bridge.statusChanged.emit(msg)
        gui_controller.controller.preload_models()
        gui_controller.controller.start_capability_scan()
        gui_controller.bridge.statusChanged.emit("Ready")
        gui_controller.bridge.registry.emit(gui_controller.registry_items())

    gui_controller.run_async(run_startup)

    # speak the greeting only once the GUI is visible
    def greet():
        try:
            from main import greeting
            gui_controller.speak(greeting())
        except Exception:
            pass

    QTimer.singleShot(1200, greet)

    if args.start_voice or settings.get("start_voice_automatically", False):
        QTimer.singleShot(2000, window._on_start_voice)

    # ---- shutdown ----------------------------------------------------------
    def full_exit():
        startup_status("Powering down")
        try:
            gui_controller.shutdown()
        except Exception:
            pass
        tray.hide()
        app.quit()

    window.exitRequested.connect(full_exit)
    tray.exitRequested.connect(full_exit)

    # intercept window close -> minimize to tray
    original_close = window.closeEvent

    def close_event(event):
        if settings.get("minimize_to_tray", True) and QSystemTrayIcon.isSystemTrayAvailable():
            event.ignore()
            minimize_to_tray()
        else:
            full_exit()

    window.closeEvent = close_event

    exit_code = app.exec()
    try:
        gui_controller.shutdown()
    except Exception:
        pass
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
