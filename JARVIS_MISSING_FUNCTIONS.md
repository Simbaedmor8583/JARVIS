# JARVIS Missing Functions

## Critical Missing Features

| Function | Impact | Effort | Priority |
|----------|--------|--------|----------|
| File rename | Cannot rename files on command | Medium | Medium |
| File move (standalone) | Cannot move files except via organizer | Medium | Medium |
| File copy | Cannot copy files | Medium | Medium |
| Delete to Trash | Cannot delete files | Medium | Medium |
| Read screen text (OCR) | Cannot read what's on screen | High | High |
| Visual element detection | Cannot find buttons/fields on screen | High | High |
| Error dialog reading | Cannot detect and respond to system dialogs | High | High |
| Web form filling | Cannot fill web forms | High | Medium |
| Web file download | Cannot download files from browser | Medium | Low |
| Microsoft Outlook | No email support via Outlook | Medium | Medium |
| Microsoft OneNote | No note-taking support | Medium | Low |
| Excel charts | Cannot create charts in spreadsheets | Medium | Low |
| PowerPoint slideshow | Cannot start presentation mode | Low | Low |
| Word tables | Cannot insert tables in documents | Low | Low |
| Word images | Cannot insert images in documents | Low | Low |
| PowerPoint images | Cannot insert images in slides | Low | Low |
| PowerPoint speaker notes | Cannot add speaker notes | Low | Low |
| Window move/resize | Cannot move or resize windows | Medium | Medium |
| Dynamic capability registry | JARVIS doesn't know what it can do | High | High |
| Retry logic for OpenRouter | No retry on API failure | High | High |
| Fallback model for OpenRouter | No fallback if kimi-k3 fails | High | Medium |
| Browser-to-Desktop bridge | Cannot drag content from browser to desktop | High | Low |

## Configuration Gaps

| Gap | Impact | Priority |
|-----|--------|----------|
| No .env file exists | OPENROUTER_API_KEY not set | Critical |
| No NEWS_API_KEY set | NewsAPI fallback unavailable | Low |
| No EMAIL_ADDRESS/PASSWORD | SMTP fallback unavailable | Medium |
| WhatsApp not linked | WhatsApp automation unavailable | Medium |
| Gmail not logged in | Gmail browser automation unavailable | Medium |

## Test Coverage Gaps

| Gap | Impact | Priority |
|-----|--------|----------|
| No real microphone test | Voice pipeline untested with real hardware | High |
| No real browser test | Browser automation untested | High |
| No real Office test | Office COM automation untested | Medium |
| No real mouse/keyboard test | DesktopAgent untested with real input | High |
| No packaged build test | Differences between source and package unknown | High |
| No real audio playback test | TTS untested with real speakers | Medium |

