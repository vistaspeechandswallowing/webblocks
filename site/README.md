# site

**Site-wide code, pasted once into Squarespace — not per page, not a Code Block.**

```
site/
└── header-injection.html   # Settings → Advanced → Code Injection → HEADER
```

## `header-injection.html`

Holds the practice's `MedicalBusiness` JSON-LD. It's site-wide on purpose: the
markup describes the *business*, not a page, so it should be present on every
URL rather than only on `/contact`. That's also why
`pages/contact.html` carries no schema of its own — putting it in both
places would mean two copies to keep in sync.

### Before it goes live

One value is still a placeholder:

| Placeholder | Where to get it |
| --- | --- |
| `sameAs: ["[GBP LISTING URL NEEDED]"]` | The public Google Business Profile listing URL |

Don't ship a bracketed placeholder. If a value isn't available yet, **delete
that property** — an absent property is valid, a `"[…]"` string is not.

### Image URLs

Images come from the [`webimages`](https://github.com/vistaspeechandswallowing/webimages)
repo, served through jsDelivr and **pinned to a commit** — the same workflow
`pages/home.html` uses for its photos:

```
https://cdn.jsdelivr.net/gh/vistaspeechandswallowing/webimages@<commit-sha>/<file>
```

Two ways to get that wrong:

- A `github.com/…/blob/…` link is a **web page**, not an image. It renders the
  file inside GitHub's UI and will not load in an `<img>` or satisfy a
  structured-data image property.
- `raw.githubusercontent.com/…` does return the bytes, but GitHub serves it
  with `Content-Security-Policy: sandbox`, no CDN in front, and explicitly not
  as a production asset host. Fine for a quick check; not for the live site.

Pin to a **commit SHA**, never a branch. A branch URL changes meaning whenever
the repo changes, and jsDelivr caches branch URLs for only 7 days — so a
branch-pinned image can change or go stale under you. Commit-pinned URLs are
cached permanently.

Filenames with spaces work (`VSS%20Logo.png`), but the `%20` is easy to break
when a URL is copied by hand or pasted into a validator. Prefer hyphenated
lowercase names (`vss-logo.png`) for anything new.

### `logo` vs. `image`

They're different properties and both are set:

- **`logo`** — the wordmark. This is what it's for.
- **`image`** — Google's LocalBusiness guidance wants a *photo of the business*
  here: the premises, the team, the practitioner at work. A 2.5:1 wordmark is a
  poor fit and won't crop well into a 1:1 / 4:3 / 16:9 result card. The logo is
  standing in so the property isn't empty — **replace it with a real photo**
  when there is one.

### The Squarespace-generated block

Squarespace emits its own `LocalBusiness` JSON-LD from **Settings → Business
Information**, and there's no switch to turn it off. Ours sits alongside it.
Two JSON-LD blocks on a page is legal and search engines reconcile them, but
they must not *disagree*:

- Leave the Business Information fields blank, **or** fill them in with exactly
  the values in `header-injection.html` (same street string, same phone).
- Squarespace's block is the narrower type (`LocalBusiness`); ours is the more
  specific `MedicalBusiness`, which is a subtype of it — no conflict there.
- Watch the address in particular. Squarespace's address widget likes to
  normalise `Ste` to `Suite`; if it does, the two blocks disagree and the
  Google Business Profile match is lost.

### Facts that must match `pages/contact.html`

The street address, phone, and hours appear in both files. They are the same
facts and must be identical — a divergence is a bug, not a variation:

| Fact | Value |
| --- | --- |
| Street | `8850 W 58th Ave Ste 201` (never "Suite") |
| City / state / ZIP | Arvada, CO 80002 |
| Phone | `+17205099640`, displayed as (720) 509-9640 |
| Hours | Mon–Sat, 09:00–17:00 |

`blocks/footer.html` shows the same address and phone; keep it in step too.

### Validating

Paste the contents of the `<script>` tag into the
[Rich Results Test](https://search.google.com/test/rich-results) (Code tab) or
the [Schema Markup Validator](https://validator.schema.org/) after filling in
the placeholders. Do the check again on the live URL once it's installed, so
Squarespace's own block is in the picture.
