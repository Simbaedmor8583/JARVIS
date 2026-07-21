# JARVIS Next Actions

## Priority 1: Critical Fixes (Packaged Build)

### 1. Fix Playwright PermissionError in packaged build
**File:** skills/browser.py
**Issue:** [WinError 5] Access is denied when launching Playwright subprocess from packaged build.
**Fix:** Run packaged build as administrator, or configure Playwright browser paths to use system-installed Chromium/Edge with proper permissions.

### 2. Fix torch circular import in packaged build
**File:** rain/router.py and JARVIS-GUI.spec
**Issue:** cannot import name 'export' from partially initialized module 'torch'
**Fix:** Exclude 	orch.export module from the build, or add 	orch.export to hidden imports with proper ordering.

### 3. Fix sklearn resource missing in packaged build
**File:** JARVIS-GUI.spec
**Issue:** sklearn\\utils\\_repr_html\\estimator.css not found in packaged build.
**Fix:** Add sklearn data files to the spec's datas list.

### 4. Disable Edge TTS or make it non-blocking
**File:** oice/speaker.py
**Issue:** Edge TTS returns HTTP 403 on every attempt. Each speak() call wastes 2-3 seconds trying Edge before falling back to Piper.
**Fix:** Cache the failure state so Edge TTS is only tried once per session, or add a config flag to disable Edge TTS.

## Priority 2: API Key Configuration

### 5. Set up OpenRouter API key
**File:** .env (create from .env.example)
**Action:** Set OPENROUTER_API_KEY=sk-or-your-key-here with a real key.
**Impact:** Enables ALL cloud features: conversation, drafting, research, news briefings, email composition, Excel/PowerPoint generation.

## Priority 3: Live Verification

### 6. Test voice pipeline end-to-end
**Action:** Launch packaged build, verify microphone enumeration, wake word detection, speech recognition, TTS output.
**Success criteria:** Say "Hey Jarvis" → hear "Yes, sir?" → "Open Notepad" → Notepad opens → JARVIS speaks confirmation.

### 7. Test browser automation
**Action:** Verify Playwright works in source mode, then in packaged build.
**Success criteria:** "Open YouTube" → YouTube opens in browser.

### 8. Test Office automation
**Action:** Verify Word, Excel, PowerPoint COM automation works.
**Success criteria:** "Create a Word document about AI" → document opens in Word.

## Priority 4: Feature Completion

### 9. Implement file rename/move/copy/delete
**Files:** core/desktop_agent.py or new skills/file_ops.py
**Action:** Add pyautogui+shell file operations.

### 10. Implement screen reading (OCR)
**Action:** Add pytesseract or Windows OCR via UI Automation to read screen content.

### 11. Implement dynamic capability registry
**File:** core/registry.py or new core/capability_registry.py
**Action:** Create a registry that JARVIS can query to know its own capabilities.

## Priority 5: Quality

### 12. Add retry logic to OpenRouter calls
**File:** rain/llm.py
**Action:** Add exponential backoff retry (3 attempts) to chat() method.

### 13. Add real hardware tests
**Files:** 	ests/
**Action:** Add integration tests using real microphone, speaker, mouse, keyboard, and browser.

### 14. Create .env file
**Action:** Copy .env.example to .env and configure.

### 15. Read screen text (OCR)
**Action:** Add tesseract or Windows OCR for reading screen content.

