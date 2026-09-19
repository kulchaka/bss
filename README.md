# BSS / Soft BMW Service Lviv

Responsive, local website UI based on brandbook v0.2. Vanilla HTML, CSS and JavaScript; no build step or package dependencies.

## Run

```sh
npm run dev
```

Open `http://127.0.0.1:4173`. The server binds to localhost and serves only `public/`. Use `PORT=4174 npm run dev` to change the port.

```sh
npm run check
```

## Files

- `public/index.html`: Ukrainian page, service and booking dialogs.
- `public/styles.css`: responsive layouts, local fonts, motion and reduced-motion support.
- `public/app.js`: service filters, dialogs, request preview, clipboard and subtle motion.
- `docs/ui-design.md`: design decisions, current scope and content to confirm.
- `docs/image-prompts.md`: exact built-in image generation prompts and asset paths.
- `brand/tokens.json`: accepted brand system with revised heading typeface.
- `output/pdf/BSS-brandbook-v0.2.pdf`: latest brandbook.

## Prototype boundaries

The booking form is a clearly labelled demo. It previews and copies a request, with no submission endpoint, analytics, local storage or booking confirmation. Verify proposed service/process copy with the business and add real contact details before release. Generated imagery is illustrative; it does not depict real BSS facilities or customer work. The page has `noindex, nofollow` while it is a prototype.

## Fonts

Unbounded SemiBold and IBM Plex Sans Regular/SemiBold are bundled locally. OFL licenses are included under `brand/assets/fonts/`.

## Themes

Use the sun/moon button in the header to switch between dark and light editions. The appearance preference is saved locally; booking data is not saved. Preview either theme directly with `/?theme=light` or `/?theme=dark`. `public/theme.js` applies the preference before styles paint; `public/theme.css` contains the light edition and theme control.
