# GUI Theme Guide

## Current Theme

The active original theme uses dark graphite/black surfaces, cyan and blue status lighting, restrained amber warnings, red danger states, glass-style panels, Segoe UI/Consolas typography, and procedural QPainter graphics. It does not use copyrighted movie assets.

## State Colors

- Cyan: ready, listening, executing.
- Blue-white: speaking.
- Amber: loading, planning, recovery.
- Red: failure and dangerous actions.
- Dim graphite: idle or unavailable.

## Accessibility

- Reduced motion is available in Settings.
- Controls expose accessible names where state or search context matters.
- Keyboard focus follows native Qt behavior.
- No flashing effects are used.
- Unsupported values are textual, not color-only.

## Remaining Theme Work

Default is the only implemented palette. Midnight, Blueprint, Carbon, Glass, Aurora, and a dedicated high-contrast palette remain future work; adding them must change colors only and preserve behavior.

