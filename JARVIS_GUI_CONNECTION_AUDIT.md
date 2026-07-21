# JARVIS GUI Connection Audit

## Main Window Buttons

| Control | Qt Object Name | Signal | Handler | Controller Method | Backend Method | Skill | Status | Working | Error Handling |
|---------|---------------|--------|---------|-------------------|----------------|-------|--------|---------|---------------|
| Start Voice | btn_start | clicked | _on_start_voice | gc.start_voice() | controller.start_voice() | N/A | Connected | Yes | QMessageBox on failure |
| Stop Voice | btn_stop | clicked | _on_stop_voice | gc.stop_voice() | controller.stop_voice() | N/A | Connected | Yes | Status message |
| Mute | btn_mute | toggled | _on_mute | gc.mute/unmute_speech() | speech.mute()/unmute() | N/A | Connected | Yes | None |
| Browser | btn_browser | clicked | _skill_browser | gc.run_async(work) | ctx.browser.ensure() | browser.open | Connected | Source only | Logged |
| Files | btn_files | clicked | _skill_files | gc.run_async(work) | os.startfile | app.open | Connected | Source only | Logged |
| Logs | btn_logs | clicked | _on_logs | os.startfile(logs_folder) | N/A | N/A | Connected | Yes | Logged |
| Settings | btn_settings | clicked | _on_settings | settingsRequested.emit() | N/A | N/A | Connected | Yes | QMessageBox |
| Stop Task | btn_stoptask | clicked | _on_stop_task | gc.stop_task() | controller.stop_task() | N/A | Connected | Yes | Logged |
| Minimize | btn_min | clicked | _on_minimize | minimizeRequested.emit() | N/A | N/A | Connected | Yes | None |
| Exit | btn_exit | clicked | _on_exit | exitRequested.emit() | controller.shutdown() | N/A | Connected | Yes | None |
| Send | btn_send | clicked | _on_send | gc.submit_text(text) | controller.handle_text() | N/A | Connected | Yes | Logged |
| Close Selected | btn_close_selected | clicked | _on_close_selected | gc.submit_text(close X) | controller.handle_text() | app.close | Connected | Yes | None |
| Bring Front | btn_bring_front | clicked | _on_bring_front | gc.submit_text(bring X) | controller.handle_text() | window.front | Connected | Yes | None |
| Close All | btn_close_all | clicked | _on_close_all | gc.submit_text(close everything) | controller.handle_text() | app.close | Connected | Yes | QMessageBox confirm |

## Skills Tab Buttons

| Control | Label | Handler | Backend Method | Skill | Status | Working |
|---------|-------|---------|----------------|-------|--------|---------|
| btn_test_openrouter | Test OpenRouter | _skill_test_openrouter | llm.test_connection() | N/A | Connected | Source only |
| btn_screenshot | Screenshot | _skill_screenshot | agent.screenshot() | system.screenshot | Connected | Source only |
| btn_read_screen | Read Screen | _skill_read_screen | agent.active_window_title() | N/A | Connected | Yes |
| btn_word_report | Word Report | _skill_word_report | word_skill.write_document() | word.write | Connected | Source only |
| btn_youtube | YouTube Search | _skill_youtube_search | controller.handle_text(search youtube) | browser.search_youtube | Connected | Source only |
| btn_organize | Organize Desktop | _skill_organize | controller.handle_text(organize desktop) | desktop.organize | Connected | Source only |
| btn_news_refresh | Refresh News | _skill_news_refresh | news_service.headlines() | news.latest | Connected | Source only |
| btn_news_read | Read News | _skill_news_read | news_service.read_headline() | N/A | Connected | Source only |
| btn_news_open | Open Article | _skill_news_open | controller.handle_text(open URL) | browser.open_site | Connected | Broken (browser) |
| btn_news_save | Save News | _skill_news_save | controller.handle_text(save news) | news.save | Connected | Source only |

## Tray Menu Actions

| Action | Signal | Handler | Connected | Working |
|--------|--------|---------|-----------|---------|
| Open JARVIS | openRequested | show_window() | Yes | Yes |
| Start Voice | startVoiceRequested | window._on_start_voice() | Yes | Source only |
| Stop Voice | stopVoiceRequested | window._on_stop_voice() | Yes | Source only |
| Mute Speech | muteRequested | tray_mute() | Yes | Yes |
| Open Logs | logsRequested | window._on_logs() | Yes | Yes |
| Settings | settingsRequested | open_settings() | Yes | Yes |
| Exit | exitRequested | full_exit() | Yes | Yes |

## Controls With No Working Handler

| Control | Issue |
|---------|-------|
| btn_browser (in packaged build) | Playwright PermissionError WinError 5 - Access denied |
| btn_news_open (packaged) | Depends on browser which fails in packaged build |
| btn_youtube (packaged) | Depends on browser which fails in packaged build |
| btn_read_screen | Only reads window title, not actual screen content |
| Edge TTS (all) | HTTP 403 on every request - wastes 2-3s per utterance |
