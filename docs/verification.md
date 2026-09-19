# UI verification

Checked locally in the Codex browser, 2026-09-15.

- Desktop at 1280 × 720; mobile at 390 × 844 and narrow layout at 320 × 740.
- Document width matches viewport; no horizontal page overflow in those checks.
- Local fonts and all generated images load successfully. Final website uses WebP exports: hero 88,374 bytes, detail 156,568 bytes, versus 3,705,764 bytes for the original PNG pair.
- Service filters show the correct two matching panels and update `aria-pressed` and the result count.
- Service dialog correctly displays the selected service. Booking preselects the same service.
- Required-field validation prevents an empty request. Filled demo details produce the correct preview without a network submission.
- Escape closes the dialog and restores focus to the originating service card. A booking launched from mobile navigation restores focus to the menu button.
- Mobile navigation opens, follows section anchors and closes after selection.
- Process details open and show their associated content.
- Browser error/warning log empty during the UI checks.
- JavaScript syntax checked with `node --check` for the application and server.
- Reduced-motion behavior checked in CSS/JS: no parallax, tilt, spatial reveals or loader animation. OS-level reduced-motion emulation was not exercised.

Still outside this prototype: a live booking endpoint, verified service catalogue and contact data, actual workshop/team imagery, final vector logo, production hosting and cross-browser/device performance audit. Clipboard success/failure paths are implemented; clipboard access was not invoked during testing to avoid replacing the user's clipboard.

## Motion pass — 2026-09-19
- JavaScript syntax checks pass for server, app, and motion layer.
- Headless Chrome: headlights toggle and aria-pressed, scrolling into gear 03, service filtering, service/booking dialogs and Escape, mobile menu, live reduced-motion preference. No page errors.
- Viewport overflow checked at 320, 390, 768 and 1440 CSS pixels. Corrected ambient layer overflow and mobile image alignment.
- Visually inspected desktop hero (lit state), service section, and mobile hero. Both hero frames retain matching element bounds on mobile.
- Reduced motion hides the decorative instrument and removes continuous/spatial animation. Optional image failure preserves original hero.
- The tachometer is an illustrative scroll instrument, not vehicle telemetry. The booking flow remains a demo.

## Light edition — 2026-09-19
- Added porcelain/silver surfaces, graphite text, blue CTA, original dark photographic cards, adapted instrument and form colors.
- Chrome checks passed: light/dark toggle, URL preview, saved theme across reload/navigation, booking request preview, no page errors.
- No horizontal overflow at 320, 390, 768 and 1024; visually inspected 1440 desktop hero/services/dialog and 390 mobile hero.
- Only the appearance preference is saved in localStorage. Storage exceptions are caught; the switch remains usable without persistence. The default remains dark, and ?theme=light opens a direct light preview.

## Daylight photography — 2026-09-19
- Replaced all four photographic placements in light mode with the new G20 hero/detail series, plus a separate lit hero state. Dark mode retains its existing assets.
- Verified loaded image sources after four consecutive theme switches, with headlights enabled; no stale hidden lighting layer and no browser errors.
- Re-ran light/dark persistence, booking preview, and responsive overflow checks at 320/390/768/1024. Visually inspected desktop hero, service cards, and mobile hero.

## Smooth motion refinement — 2026-09-19
Chrome passed: dark/light transitions in both directions, enabled headlights, accordion opening/closing by mouse and keyboard, interrupted accordion animation, reduced-motion behavior, simulated missing View Transitions API fallback, mobile booking dialog, and no horizontal overflow. No page errors. Inspected transition midpoint; settled entrance animation before snapshots to avoid text offset ghosting. Syntax and whitespace checks pass.
