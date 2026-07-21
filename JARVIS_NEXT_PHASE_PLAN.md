# JARVIS Next Phase Plan

## Generated: July 19, 2026 18:26

---

## PRIORITY 1: FIX REMAINING PACKAGED PARITY GAPS

### 1.1 Fix 4 existing test failures
- test_llm_sanitizes_key_in_error: Update assertion for new error format
- test_extract_json_from_prose_and_nested_strings: Move to Router tests
- test_extract_json_repairs_trailing_commas: Move to Router tests
- test_speaker_falls_back_to_piper: Add EDGE_TTS_ENABLED=True to test

### 1.2 Confirmation routing
- Log shows "[agent] confirmation required but no handler: dangerous"
- Wire Agent.confirm() through ControllerBridge to GUI dialog

### 1.3 Live validation of all CONNECTED BUT NOT LIVE VERIFIED features
- Settings save/load roundtrip
- Test Connection button
- Browser YouTube search
- Voice pipeline end-to-end

### 1.4 Test cleanup
- Remove test_llm.py (dead tests for nonexistent extract_json)
- Add test_llm.py tests for actual public methods

---

## PRIORITY 2: ADD MISSING DESKTOP FUNDAMENTALS

### 2.1 File operations skill
- Create folder
- Create file
- Rename file
- Copy file
- Move file
- Delete to trash
- Undo support

### 2.2 Screen understanding
- OCR / text reading from screen
- Window content awareness
- Visual region detection

### 2.3 Complete Office integration
- Live Office COM testing
- Create Word doc with multiple paragraphs
- Excel with formulas
- PowerPoint with multiple slides
- Safe save/close flow

---

## PRIORITY 3: SAFETY AND PERMISSIONS

### 3.1 Permission system
- Action categories (safe, needs-confirm, dangerous, forbidden)
- Per-session user consent
- Deny-by-default for dangerous actions
- Consent persistence

### 3.2 Tool allowlist
- Define which tools are safe for autonomous use
- Allowlist for Hermes sandbox mode
- Graduated access levels

### 3.3 Confirmation completion
- Wire confirmation dialog through GUI
- Add timeout auto-deny
- Add "remember for session" option

---

## PRIORITY 4: HERMES INTEGRATION (behind feature flag)

### 4.1 Foundation (Phase A)
- ToolAllowlist
- PermissionScope
- Structured action schema
- Confirmation routing

### 4.2 Core (Phase B)
- Dynamic SkillRegistry
- HermesTool wrappers
- Sandbox mode
- Capability health checks

### 4.3 Expansion (Phase C)
- Checkpoint/rollback
- Memory schema
- Gradual tool access
- Autonomous workflows

---

## PRIORITY 5: ADVANCED INTELLIGENCE

### 5.1 Dynamic capability registry
- Self-test framework
- Health API
- Capability introspection

### 5.2 Advanced memory
- Structured recall
- Context persistence across sessions
- Learning from past interactions

### 5.3 Autonomous workflows
- Scheduled tasks
- Trigger-based actions
- Multi-session continuity

---

## RANKED ORDER (FULL LIST)

| Rank | Item | Category |
|------|------|----------|
| 1 | Fix test_llm_sanitizes_key_in_error assertion | P1: Test fix |
| 2 | Remove/fix dead test_llm.py tests | P1: Test fix |
| 3 | Fix test_speaker_falls_back_to_piper test | P1: Test fix |
| 4 | Wire confirmation routing through GUI | P1: Bug fix |
| 5 | Live validation: Settings save/load | P1: Validation |
| 6 | Live validation: Test Connection button | P1: Validation |
| 7 | Live validation: Browser YouTube search | P1: Validation |
| 8 | Live validation: Voice pipeline | P1: Validation |
| 9 | Create file operations skill (create/copy/move/delete) | P2: Missing |
| 10 | Add screen OCR/reading | P2: Missing |
| 11 | Live Office COM testing | P2: External |
| 12 | Create structured action schema | P3: Safety |
| 13 | Implement ToolAllowlist | P3: Safety |
| 14 | Implement PermissionScope | P3: Safety |
| 15 | Complete confirmation flow | P3: Safety |
| 16 | Add dynamic SkillRegistry | P4: Hermes |
| 17 | Create HermesTool wrappers | P4: Hermes |
| 18 | Implement sandbox mode | P4: Hermes |
| 19 | Add capability health checks | P4: Hermes |
| 20 | Add checkpoint/rollback | P4: Hermes |
| 21 | Add structured memory schema | P5: Advanced |
| 22 | Add autonomous workflow support | P5: Advanced |
| 23 | Add self-test framework | P5: Advanced |
| 24 | Add scheduled tasks | P5: Advanced |
