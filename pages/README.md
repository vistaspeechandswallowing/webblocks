# pages

**Full-page compositions for Squarespace — one code block per page.**

This is the home for the newer approach: instead of scattering many small code
blocks across a Squarespace page (each an island with its own width and
spacing), each page here is a *single* self-contained code block that composes
all its sections on one shared container and one shared spacing rhythm. That's
what keeps spacing visually consistent across screen sizes — see the top-level
README for the reasoning.

The older, reusable single-purpose blocks still live in `../blocks/`. This
folder is where pages get migrated to, one at a time.

## What's here

```
pages/
├── custom-css.css  # The COMPLETE site Custom CSS — paste ONCE into Squarespace
├── _template.html  # Starting point for a new page composition
├── home.html       # The Home page
└── …               # More pages land here as they're migrated
```

## The system — three tiers

Styling is split by how widely it's used, so nothing is duplicated across pages:

1. **Tokens** — values (width, spacing, palette: `--vss-max`, `--vss-section-y`,
   `--vss-blue`, …). In `custom-css.css`.
2. **Shared components** — the reusable building blocks every page is made of:
   `.vss-page` (+ full-bleed breakout), `.vss-container`, `.vss-band`, `.vss-btn`,
   `.vss-hero`, `.vss-badge`, `.vss-card`, `.vss-h2`. Also in `custom-css.css`.
   Change the button (or any component) once here and **every page updates**.
3. **Page-specific** — anything unique to one page. Set it inline on the element
   in that page's `.html` (e.g. the hero's background photo in `home.html`).

Tiers 1 and 2 both live in **`custom-css.css`**, which is the complete Custom
CSS for the site (it also holds the global type tweaks and the native-form
styler). Paste the whole file **once** into **Design → Custom CSS**.

Because the components live in Custom CSS, the page `.html` files are essentially
**pure markup** — reuse the component classes; don't redeclare their CSS. The
tradeoff: a page block depends on `custom-css.css` being installed (a `.vss-btn`
won't style itself without it). That's a one-time paste, so it's fine.

## Migrating a page

1. Copy `_template.html` to `pages/your-page.html`.
2. Build each section as a `.vss-band` with a `.vss-container` inside. Reuse the
   shared button (`.vss-btn`), badge, card, etc. patterns from `home.html`.
3. Scope every class under a unique `.vss-<page>` prefix (or reuse the shared
   `vss-` component classes) so nothing leaks into the Squarespace UI.
4. Use the live site as the source of truth for copy, images, and links.

## Pasting a page into Squarespace

For the single-block approach to actually control spacing, the containing
Section must stop imposing its own grid and padding:

1. Delete the page's old separate code blocks **and** any native text blocks
   whose content now lives inside this composition.
2. New Section → **Full Bleed**, content width **Wide/Full**, Section
   **padding top & bottom = 0**, background **none** (each band carries its own).
3. Paste the page's `.html` into one Code Block.
4. Make sure `custom-css.css` is in Design → Custom CSS (only needed once, site-wide).

## Previewing locally

The files are self-contained. To eyeball one, concatenate the tokens and the
page into a throwaway HTML file and open it, e.g.:

```bash
{ echo '<style>'; cat pages/custom-css.css; echo '</style>'; cat pages/home.html; } > /tmp/preview.html
```
