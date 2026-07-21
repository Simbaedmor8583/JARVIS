# JARVIS Capability Registry Report

Date: 2026-07-20

## Result

- Registry: `core/capability_registry.py`.
- Health engine: `core/capability_health.py`.
- GUI page: `gui/capabilities_page.py`.
- Capabilities discovered: 163.
- Working: 142.
- Requires login: 21.
- Missing: 0.
- Broken: 0.
- Unassigned permissions: 0.
- Health scan error: none.

The login-required records are Gmail/email and WhatsApp operations that cannot be asserted connected without an authenticated user session.

## Commands

`/help`, `/skills`, `/status`, `/capabilities`, and `/selftest` all returned registry-backed responses in source typed mode.

`/skills` and `/capabilities` are generated only from discovered registry records, not directly from the tool allowlist.

## Health Semantics

The registry reports WORKING, CONNECTED, DISABLED, REQUIRES_CONFIGURATION, REQUIRES_LOGIN, BROKEN, MISSING, or DEGRADED. Import and health-check failures degrade individual records rather than preventing startup.

System metrics returned WORKING. CPU, RAM, disk, network counters, and Python thread count were available. Unsupported GPU, VRAM, and temperature values remain `Unavailable` rather than being invented.

## Hermes

Hermes remains disabled and absent by instruction. Remaining Hermes blockers are installation, planner/orchestrator integration, capability health registration, signal wiring, tests, and packaged dependency validation.

