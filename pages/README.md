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
├── swallow-study.html  # The Swallow Study page
└── …               # More pages land here as they're migrated
```

## The system — three tiers

Styling is split by how widely it's used, so nothing is duplicated across pages:

1. **Tokens** — values (width, spacing, palette: `--vss-max`, `--vss-section-y`,
   `--vss-blue`, …). In `custom-css.css`.
2. **Shared components** — the reusable building blocks every page is made of:
   `.vss-page` (+ full-bleed breakout), `.vss-container`, `.vss-band`, `.vss-btn`,
   `.vss-hero`, `.vss-badge`, `.vss-card`, `.vss-h2`, `.vss-pagehead`,
   `.vss-meta`, `.vss-article`, `.vss-prose`, `.vss-h2--sub`, `.vss-checklist`,
   `.vss-infocard`, `.vss-quote`, `.vss-section-cta`. Also in `custom-css.css`.

   **Home vs. interior pages:** `.vss-band--hero` (full-bleed photo + parallax)
   is the *home page's* opener and should stay unique to it. Every other page
   opens with `.vss-band--pagehead` — title, lede, and meta row on a soft tint
   — so sub-pages read as sub-pages. See `swallow-study.html`.
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

1. Delete the page's old separate code blocks **and** any native text blocks
   whose content now lives inside this composition.
2. New Section → content width **Wide/Full**, background **none** (each band
   carries its own).
3. In the section's **Design** tab (the Fluid Engine editor):
   - **Fill Screen** → **off**. Left on, it holds the section at a fraction of
     the viewport and — with centered alignment — pads our block out on both
     sides.
   - **Alignment** → top.
   - **Gap** and **Row Count** don't matter for these sections; see below.
4. Paste the page's `.html` into one Code Block.
5. Make sure `custom-css.css` is in Design → Custom CSS (only needed once, site-wide).

### Why the gaps happened (and what fixes them)

**A Fluid Engine section doesn't take its height from its content — it takes it
from its grid.** The Design panel's Row Count becomes a fixed track list, e.g.
`grid-template-rows: repeat(103, minmax(24px, auto))`, and the code block is
placed across a fixed span of those rows. Each row is at least 24px whether or
not anything is in it. Our markup is fluid, so its real height changes as text
reflows — meaning the reserved height and the true height match at about *one*
viewport width and drift apart everywhere else:

- reserved > content → empty rows below the block = **the gap**
- reserved < content → content spills past the section

That's also why the gap moved around with screen size rather than being a
constant. Note what it is **not**: the section's own padding measures
`calc(1vmax / 10)` — roughly 2px. Zeroing padding was never going to help, and
an earlier version of these instructions chased exactly that dead end (along
with asking for a "Section padding = 0" control that Fluid Engine doesn't have).

The fix in `custom-css.css` (end of section 2) collapses the track list to a
single `auto` row and pins the block to it, so the grid measures our content and
Squarespace sizes the section from it. Row Count then stops mattering. The rules
are guarded by `:has(.vss-page)` — confirmed working in Squarespace's CSS
compiler — so only sections holding one of our page compositions are affected.

**Header clearance** is carried by the page itself, not by the section:
`.vss-band--pagehead` has its own top padding, sized by the
`--vss-header-clear` / `--vss-header-clear-sm` tokens in section 1. If a page
title ever sits too close to (or under) the header, those two values are the
dial. The home hero is exempt on purpose — it runs full-bleed under the header.

## Previewing locally

The files are self-contained. To eyeball one, concatenate the tokens and the
page into a throwaway HTML file and open it, e.g.:

```bash
{ echo '<style>'; cat pages/custom-css.css; echo '</style>'; cat pages/home.html; } > /tmp/preview.html
```
