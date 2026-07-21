# JARVIS Backend Regression Audit

Date: July 17, 2026

| Command / Function | Expected skill | Actual skill | Visible Windows result | Error | Fix applied |
|---|---|---|---|---|---|
| Open my Downloads folder | app.open_folder | app.open_folder | Downloads opened in File Explorer | None | Windows known-folder resolver and post-launch registry |
| Open my Documents folder | app.open_folder | app.open_folder | Redirected Documents opened in File Explorer | None | Registry Shell Folders resolution |
| Open my Desktop folder | app.open_folder | app.open_folder | OneDrive Desktop opened in File Explorer | None | OneDrive-aware Desktop resolution |
| Open the JARVIS project folder | app.open_folder | app.open_folder | Project opened in File Explorer | None | Project aliases resolve to source directory |
| Open a real text file | app.open | app.open | File opened visibly in Notepad | None | Existing-path resolution and os.startfile |
| Open Notepad | app.open | app.open | Untitled Notepad window appeared | None | App Paths / executable resolver |
| Open Calculator | app.open | app.open | Calculator window appeared | None | App Paths / executable resolver |
| Open Microsoft Word | app.open | app.open | Word window appeared | None | Office App Paths resolution |
| Open YouTube | browser.open_site | browser.open_site | YouTube opened in persistent Edge profile | None | Edge-first Playwright launch |
| Search YouTube for Dangerous Minds song | browser.search_youtube | browser.search_youtube | Correct YouTube results URL and title appeared | None | Exact route and encoded YouTube search |
| Browser + YouTube + search compound command | 3-step plan | 3-step plan | Browser, YouTube, and results page opened in order | None | Deterministic command planner |
| Word + cognitive therapy research compound command | 6-step plan | 6-step plan | 10-source DOCX saved and opened in Word | None | Staged research planner and Bing RSS fallback |
| Create a Word document about cognitive therapy basics | word.write | word.write | 2,410-word DOCX saved and opened in Word | None after fix | Explicit httpx client repaired OpenRouter |
| Close it | app.close recent | app.close recent | Most recent test file closed | None | Registry close-most-recent path |
| Close Notepad | app.close named | app.close named | Registered Notepad process closed | None | Named registry close path |
| Close everything opened by JARVIS | app.close all | app.close all | Covered by registry regression tests | Not run against unrelated user windows | Existing reverse-order registry close retained |
| File search and open | app.search_file | app.search_file | Covered with resolver/search regression tests | No broad live disk scan in final run | Added exact file-search route |
| Play, pause, stop, next, mute music | media.* | media.* | Router and module preserved; browser media path imports and compiles | Not replayed during final run | Browser engine repaired underneath media skill |
| Volume controls | system.volume | system.volume | Existing pycaw implementation compiles and routes | Not changed to avoid altering user volume | Preserved existing implementation |
| Excel creation | excel.create | excel.create | Exact route and existing module compile | Not visibly rerun | Added deterministic route; implementation preserved |
| PowerPoint creation | ppt.create | ppt.create | Exact route and existing module compile | Not visibly rerun | Added deterministic route; implementation preserved |
| Gmail read/compose/reply | email.* | email.* | Existing browser/SMTP/IMAP module compiles | Account-dependent; not sent or read during audit | Persistent browser profile repaired |
| WhatsApp open/read/reply | whatsapp.* | whatsapp.* | Existing module compiles; open route is exact | Account-dependent; no message sent | Existing implementation preserved |
| News search/save | news.* | news.* | Existing module compiles and existing router tests pass | Not visibly rerun | Existing implementation preserved |
| Desktop organize/reverse | desktop.* | desktop.* | Existing module compiles and routes | Not run on live Desktop to avoid moving user files | Existing implementation preserved |
| Shutdown/restart/sleep | system.shutdown | system.shutdown | Confirmation and command paths compile and route | Deliberately not executed | Existing confirmation safeguards preserved |
| Conversation memory | chat | chat | Existing remember route and memory module compile | None in automated route coverage | Existing persistence preserved |

## Validation Summary

- Existing tests preserved: 47.
- Added backend regression tests: 17.
- Total passing tests: 64.
- All project Python files compile under Python 3.12.
- Visible source validation passed for folders, file, Notepad, Calculator, Word, Edge/Playwright, YouTube, YouTube search, close recent, close named, Word generation, and research generation.
- External account actions and destructive Windows power actions were not executed; they are reported as unverified live actions rather than false successes.
