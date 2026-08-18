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
`blocks/contact-details.html` carries no schema of its own — putting it in both
places would mean two copies to keep in sync.

### Before it goes live

Three values are placeholders and must be filled in:

| Placeholder | Where to get it |
| --- | --- |
| `"image": "[LOGO URL NEEDED]"` | Absolute `https://` URL of the logo or a building/team photo |
| `geo.latitude` / `geo.longitude` | Read off the Google Business Profile map pin |
| `sameAs: ["[GBP LISTING URL NEEDED]"]` | The public Google Business Profile listing URL |

Don't ship a bracketed placeholder. If a value isn't available yet, **delete
that property** — an absent property is valid, a `"[…]"` string is not.

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

### Facts that must match `blocks/contact-details.html`

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
