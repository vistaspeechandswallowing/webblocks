# site

**Site-wide code, pasted once into Squarespace — not per page, not a Code Block.**

```
site/
└── header-injection.html   # Settings → Advanced → Code Injection → HEADER
```

## `header-injection.html`

Holds the practice's `MedicalClinic` JSON-LD. It's site-wide on purpose: the
markup describes the *business*, not a page, so it should be present on every
URL rather than only on `/contact`. That's also why
`pages/contact.html` carries no schema of its own — putting it in both
places would mean two copies to keep in sync.

### The one thing still missing: `sameAs`

`sameAs` is a list of other places on the web that are *this same business* —
its Google Business Profile, its Facebook page, its Yelp listing. It's how you
tell Google "the markup on this website and that listing over there describe one
practice, not two." Without it Google has to infer the connection from the name
and address matching, which usually works but isn't guaranteed.

The property is currently **left out** rather than left as a placeholder — an
absent property is valid, a `"[…]"` string is not. To add it:

1. Open [Google Maps](https://www.google.com/maps) and search for
   **Vista Speech & Swallowing**.
2. Click the practice's listing so its panel opens on the left.
3. Hit **Share** in that panel, then **Copy link**.
4. Paste it into `header-injection.html` as the last property, after
   `knowsLanguage` — and add a comma to the end of the `knowsLanguage` line,
   or the JSON breaks:

   ```json
     "knowsLanguage": ["English", "Spanish"],
     "sameAs": ["https://maps.app.goo.gl/…"]
   ```

The short `maps.app.goo.gl/…` link is fine. If you'd rather have the long form,
the address bar URL of the listing page works too. Run the validator (below)
afterwards to confirm nothing broke.

Worth adding the practice's other profiles to the same list as they appear —
Facebook, Instagram, Healthgrades, Psychology Today, the ASHA directory. Each
one is another confirmation that they're all the same practice.

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
- Squarespace's block is the broad type (`LocalBusiness`); ours is
  `MedicalClinic`, which sits below it in the same family
  (`MedicalClinic` → `MedicalBusiness` → `LocalBusiness`) — no conflict there,
  just more detail.
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

Two passes, and they check different things.

**1. The local validator — run this after every edit.**

```bash
python3 site/validate-schema.py
```

It checks the markup against the real schema.org vocabulary (downloaded once and
cached): that every property exists, that the type it's attached to actually
accepts it, that nested values are the right types, that URLs are URLs, and that
no placeholder survived. This is not busywork — its first run caught two bugs
that looked completely fine by eye:

- `medicalSpecialty` was on `MedicalBusiness`, which doesn't accept it. The type
  is now `MedicalClinic`, which does (and is more accurate anyway).
- the languages were on `availableLanguage`, which belongs to `ContactPoint`
  and `ServiceChannel` — not to an organization. They're on `knowsLanguage` now.

Both would have been **silently dropped** by anything reading the page rather
than reported as an error. That's the failure mode this catches.

**2. Google's own tools — run these on the live URL.**

The local validator knows the vocabulary, not Google's requirements for a rich
result. Once the markup is installed, run the
[Rich Results Test](https://search.google.com/test/rich-results) and the
[Schema Markup Validator](https://validator.schema.org/) against the real page,
which is also the only way to see our block and Squarespace's together.
