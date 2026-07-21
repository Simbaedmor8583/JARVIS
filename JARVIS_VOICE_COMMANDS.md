# JARVIS Voice Commands

## Command Groups By Skill

### System Control
| Command | Fast Lane | Router Skill | Working |
|---------|-----------|-------------|---------|
| Stop / Stop talking / Shut up / Be quiet | Yes | system.stop_speech | Yes |
| Volume up / Louder | Yes | system.volume | Yes |
| Volume down / Quieter | Yes | system.volume | Yes |
| Mute / Mute the sound | Yes | system.volume | Yes |
| Unmute / Unmute the sound | Yes | system.volume | Yes |
| Take a screenshot | Yes | system.screenshot | Yes |
| Lock the computer / Lock the PC | Yes | system.lock | Yes |
| Cancel the shutdown / Abort shutdown | Yes | system.shutdown | Yes |
| Restart the computer / Reboot | Yes | system.shutdown | Yes |
| Sleep / Put the computer to sleep | Yes | system.shutdown | Yes |
| Shut down / Power off / Turn off PC | Yes | system.shutdown | Yes |
| Battery status / System status / Status report | Yes | system.status | Yes |

### Smalltalk (no model, instant)
| Command | Fast Lane | Router Skill | Working |
|---------|-----------|-------------|---------|
| What time is it | Yes | smalltalk (time) | Yes |
| What is the date / What day is it | Yes | smalltalk (date) | Yes |
| Hello Jarvis / Good morning/afternoon/evening | Yes | smalltalk (greeting) | Yes |
| Thanks Jarvis / Thank you | Yes | smalltalk (thanks) | Yes |
| How are you / How are you doing | Yes | smalltalk (howareyou) | Yes |
| Goodbye / Good night Jarvis | Yes | smalltalk (goodbye) | Yes |

### Music/Media
| Command | Fast Lane | Router Skill | Working |
|---------|-----------|-------------|---------|
| Play music | Yes | media.play_music | Source only |
| Play [song/artist] | Yes | media.play_music | Source only |
| Pause / Pause the music | Yes | media.control | Source only |
| Resume / Continue the music | Yes | media.control | Source only |
| Next / Skip / Next song | Yes | media.control | Source only |
| Mute the music | Yes | media.control | Source only |
| Stop the music | Yes | media.control | Source only |

### Open/Close
| Command | Fast Lane | Router Skill | Working |
|---------|-----------|-------------|---------|
| Open [app/file/folder/site] | No | app.open | Yes |
| Close it / Close that / Close this | Yes | app.close | Yes |
| Close everything / Close everything you opened | Yes | app.close | Yes |
| Close the browser | Yes | browser.close | Source only |
| Close YouTube / Close [named item] | Yes | app.close | Yes |
| Open the browser | Yes | browser.open | Source only |
| Open YouTube | No | browser.open_site | Source only |
| Open Google / Gmail / GitHub / [any known site] | No | browser.open_site | Source only |

### Voice Not in Router (go through fast lane)
| Command | Fast Lane | Router Skill | Working |
|---------|-----------|-------------|---------|
| Search YouTube for [query] | Yes | browser.search_youtube | Source only |
| Create a Word document about [topic] | Yes | word.write | Yes |
| Create an Excel spreadsheet about [topic] | Yes | excel.create | Source only |
| Create a PowerPoint about [topic] | Yes | ppt.create | Source only |
| Create a research report about [topic] | Yes | research.create_report | Yes |
| Find file [name] | Yes | app.search_file | Source only |
| Search for [query] | Yes | web.search | Source only |
| Check my email | Yes | email.check | Needs login |
| Read email from [name] | No | email.read | Needs login |
| Latest news / What's the news | Yes | news.latest | Source only |
| [topic] news / Technology news | Yes | news.topic | Source only |
| Tell me more about the [ordinal] one | No | news.more | Source only |
| Save the news | Yes | news.save | Source only |
| Organize my desktop | Yes | desktop.organize | Source only |
| Undo organize / Undo the organization | Yes | desktop.undo | Source only |
| Remember that [fact] | No | chat (remember) | Yes |
| Open WhatsApp / Read messages from [contact] | No | whatsapp.* | Needs login |
| Let's research [topic] / Do research on [topic] | No | research.start | Needs API key |

## Commands Documented but NOT in Routing
N/A - All documented commands in README have corresponding routes.

## Skills With No Voice Commands
- coder/codex_builder: Has route for "codex.build" but no natural voice command pattern
- window_control: Routes for window.front/minimize/maximize/restore exist but no dedicated user-facing voice commands (used as sub-actions)

## Commands That Would Fail in Packaged Build
- All browser-dependent commands (open browser, open YouTube, search YouTube, play music, check email, open website)
- All Edge TTS speech output (each utterance wastes 2-3s on failed edge-tts attempt)
- Router model (Qwen) - torch circular import in packaged build
- Wake word - sklearn resource missing in packaged build

