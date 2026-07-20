# webblocks

HTML code blocks for Squarespace. Every reusable block we build lives here — one
self-contained HTML file per block, with a browsable gallery to preview and copy them.

**Live gallery:** https://vistaspeechandswallowing.github.io/webblocks/

## Structure

```
webblocks/
├── index.html          # Gallery: previews every block and copies its code
├── blocks.json         # Manifest listing each block (title, description, tags)
└── blocks/
    ├── _template.html      # Starting point for a new block
    └── hello-banner.html   # Example block
```

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
