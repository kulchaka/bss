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
