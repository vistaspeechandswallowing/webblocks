# webblocks

HTML code blocks for Squarespace. Three areas:

- **`blocks/`** — reusable single-purpose blocks, one self-contained file each,
  with a browsable gallery to preview and copy them.
- **`site/`** — site-wide code that's pasted once into Squarespace's Code
  Injection rather than into any page — currently the practice's JSON-LD.
  See [`site/README.md`](site/README.md).
- **`pages/`** — full-page compositions, **one code block per page**. Each page
  builds all its sections on a single shared container and spacing scale, so
  spacing stays visually consistent across screen sizes. This is where pages get
  migrated to going forward — see [`pages/README.md`](pages/README.md).

**Live gallery:** https://vistaspeechandswallowing.github.io/webblocks/

## Structure

```
webblocks/
├── index.html          # Gallery: previews every block and copies its code
├── blocks.json         # Manifest listing each block (title, description, tags)
├── blocks/             # Reusable single-purpose blocks
│   ├── _template.html      # Starting point for a new block
│   └── hello-banner.html   # Example block
├── pages/              # Full-page compositions (one code block per page)
│   ├── custom-css.css      # Complete site Custom CSS — paste once into Squarespace
│   ├── _template.html      # Starting point for a new page
│   └── home.html           # The Home page
└── site/               # Site-wide code injection (pasted once, not per page)
    └── header-injection.html  # MedicalBusiness JSON-LD → Code Injection → Header
```

## Why two areas?

A page made of many separate code blocks can't enforce its own spacing — each
block is sealed off from the others, so the only shared authority is whatever
Squarespace puts between them, which drifts on large screens. Composing a whole
page as **one** block puts every section on the same container and the same
clamped vertical rhythm, defined once. `pages/` is that approach; `blocks/`
remains handy for one-off drop-ins.

## Adding a new block

1. Copy `blocks/_template.html` to `blocks/your-block-name.html`.
2. Build your block. Keep it self-contained: markup + a scoped `<style>` block
   in the one file. Scope every CSS class under a unique `.wb-your-block-name`
   prefix so styles never leak into the rest of the Squarespace page.
3. Add an entry to `blocks.json`:
   ```json
   {
     "file": "blocks/your-block-name.html",
     "title": "Your Block Name",
     "description": "One line about what it does.",
     "tags": ["hero", "cta"]
   }
   ```
4. Commit and push.

## Using a block in Squarespace

Open the gallery (see below), click **Copy** on the block you want, then paste it
into a Squarespace **Code Block**. Each file is ready to paste as-is.

## Previewing the gallery

Because `index.html` fetches `blocks.json`, open it through a local server rather
than a `file://` URL:

```bash
python3 -m http.server
# then visit http://localhost:8000
```

### Live preview via GitHub Pages (optional)

To get a hosted gallery URL, enable GitHub Pages for this repo:
**Settings → Pages → Build and deployment → Source: Deploy from a branch →
Branch: `main` / root**. The gallery will then be live at
`https://vistaspeechandswallowing.github.io/webblocks/`.
