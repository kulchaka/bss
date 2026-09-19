# BSS — Precision in motion

Approved direction: graphite/silver cinematic light, scroll-driven tachometer and sequential gears, a matching lit hero photograph, tactile buttons and service cards. Preserve typography and booking prototype boundaries.

Implementation checkpoints:
1. Atmospheric silver light: layered gradients, gentle movement, pointer response, no overlay blocking content.
2. Scroll instrument: original BSS dial inspired by automotive instruments, RPM rise and gear drop, compact mobile version, decorative semantics.
3. Hero lighting: image edit preserving composition, user-controlled headlight state and hover preview, original asset fallback.
4. Interactions: silver button sweep, card lighting and shallow perspective, keyboard focus parity.

Every checkpoint is committed independently. Reduced-motion mode removes spatial/continuous motion; hidden tabs pause animations. No new runtime framework. Verify desktop/mobile layout, dialogs, filtering, keyboard and motion preferences.

## Smooth motion refinement — 2026-09-19
References reviewed:
- https://www.osmo.supply/collection — Masked Window Page Transition, Progressive Blur, and Curved Wipe Page Transition as examples of paced transitions.
- https://reactbits.dev/animations/animated-content — coordinated content entry.
- https://tympanus.net/Tutorials/PageRevealEffects/ — layered page reveal reference.
These are inspiration, not imported components. A matching ready-made BMW theme transition was not found. Implementation is original vanilla JS/CSS.

Theme changes use a 760ms full-page crossfade via View Transitions; incoming car assets are decoded ahead of the snapshot with bounded waits. Older browsers receive a simpler surface/color transition. Reduced motion switches directly. Entrance animations settle before capture to prevent offset text ghosts. Warm-up on focus/hover reduces the first-switch delay.

Content uses small 24px reveals, subtle 3px blur, paired 85ms card stagger, slower image easing, 420ms native-details height animation with interruptible closing/opening and keyboard support. No scroll hijacking or new framework.
