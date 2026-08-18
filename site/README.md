# site

**Site-wide code, pasted once into Squarespace — not per page, not a Code Block.**

Code Injection needs a **Core plan or higher**. If the site isn't on one, read
"Do you actually need to upgrade?" below before paying for it — there's a free
path that covers most of the ground.

```
site/
└── header-injection.html   # Settings → Advanced → Code Injection → HEADER
```

## Do you actually need to upgrade?

Code Injection is a paid tier on Squarespace — **Core plan or higher**. Before
paying for it, check two things, because there's a good chance the answer is
"no upgrade needed" or "not worth it."

**1. You may already have it.** Putting JavaScript in a Code Block is the *same*
premium tier as Code Injection (Core and up). `pages/home.html` contains a
`<script>` — the hero parallax. So: open the live home page and scroll. **If the
hero photo drifts more slowly than the page, the site is already on Core or
higher, Code Injection is already included, and there is nothing to buy.**
(Check Settings → Billing to confirm.) If the photo is locked to the page, the
plan is below Core and the script is being stripped.

**On this site, as of the last check:** scripts in Code Blocks run — the
JSON-LD pasted into the `/contact` block is present in the live page source —
while the Code Injection panel is locked. See "If you have Code Blocks but not
Code Injection" below.

**2. If you are below Core, the upgrade probably isn't worth it for this.**
Structured data is a small part of local search. In rough order of impact:

| Lever | Cost | Where |
| --- | --- | --- |
| A complete, active **Google Business Profile** | free | This is the big one for "speech therapy near me" — hours, photos, services, reviews, Q&A |
| **Business Information settings** filled in | free | Settings → Business Information — feeds Squarespace's own generated markup |
| **Readable NAP text on the page** | free | `pages/contact.html` — done |
| **This JSON-LD** | Core plan | Adds specialty, service area, languages, and the GBP link |

The JSON-LD is a refinement on top of the first three, not a substitute for
them. It's worth having; it is not worth doubling the hosting bill for on its
own. If the plan gets upgraded later for other reasons, it's a two-minute paste.

### Working with Squarespace instead of around it

Whatever the plan, fill in **Settings → Business Information** completely —
name, address, phone, hours. Squarespace generates its own structured data from
those fields, and that generated markup can't be edited or removed. Filling the
panel in is what turns that block from a near-empty stub into a useful one, and
it's free on every plan.

Use exactly the values in the table further down. Watch the address field in
particular: it likes to normalise `Ste` to `Suite`, which breaks the character-
for-character match with the Google Business Profile.

To see what Squarespace is currently emitting, run the live URL through the
[Rich Results Test](https://search.google.com/test/rich-results) and read the
detected items. That's also the only way to know what our block would be adding
on top, rather than guessing.

### If you have Code Blocks but not Code Injection

**This is the situation the site is actually in:** scripts inside Code Blocks
run, but Settings → Advanced → Code Injection is locked behind an upgrade.

That combination is almost certainly a **legacy plan**, not a loophole.
Squarespace's own documentation says Code Injection is available on "Core, Plus,
Advanced, and some legacy billing plans" — note *some*. Older plans bundled
these features differently than the current lineup does, and a site that has
been on the same plan for a while keeps the old bundle. The two gates are
enforced in different places (one locks a settings panel, the other filters
block content), so they don't have to agree.

Practical read: don't treat working Code Blocks as something to hide, but don't
build anything load-bearing on them either. A grandfathered bundle is stable
until the plan is migrated or renewed onto the current lineup, and then it
isn't. That's an argument for the layering this repo already uses, not against
using Code Blocks:

- **The readable text on `/contact` is the durable layer.** It is ordinary HTML,
  works on every plan, and is what a person actually reads. If everything else
  vanished tomorrow, the address, hours, and service area are still on the page.
- **The JSON-LD is the enhancement.** Nice to have, and it can go away without
  taking anything visible with it.

#### Putting the JSON-LD in a Code Block

JSON-LD does **not** have to be in the `<head>` — Google reads structured data
anywhere in the document. Body placement is a documented, supported position,
not a workaround.

1. Get the tag without this file's comment header:

   ```bash
   python3 tools/paste.py site/header-injection.html | pbcopy
   ```

   (Copying the raw file works too, but pastes ~3.5KB of notes into the live
   page along with it. See the top-level README.)
2. Paste it at the **end** of the `/contact` Code Block, after the closing
   `</div>` of `.vss-page`. It renders nothing, so its position doesn't affect
   the layout.
3. Confirm it survived: view source on the live page and search for
   `MedicalClinic`, then run the URL through the
   [Rich Results Test](https://search.google.com/test/rich-results).

Step 3 is not optional. If the plan ever stops allowing scripts in Code Blocks,
the tag will be stripped **silently** — the page will look completely normal
with the markup gone. Re-check after any plan change.

Two things not to do:

- **Don't copy the JSON into `pages/contact.html` in this repo.** It stays in
  `header-injection.html`, as one copy, whichever box it gets pasted into. The
  day the plan gains Code Injection, it moves to the head with no edits and no
  reconciling of two versions that drifted apart.
- **Don't paste it onto several pages.** A Code Block lives on one page, so this
  is no longer site-wide markup — and duplicating it across pages means
  maintaining copies of the business's address. `/contact` is the page these
  facts belong to; one copy there is the right trade.

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

### The Squarespace-generated blocks

Squarespace emits **three** JSON-LD blocks of its own and there is no switch to
turn them off. Ours sits alongside them — several JSON-LD blocks on a page is
valid, and search engines reconcile them. Verified from the live page:

| Block | What it carries |
| --- | --- |
| `WebSite` | url, name, logo image |
| `Organization` | legalName, address as one string, email, telephone, **`sameAs`** |
| `LocalBusiness` | address as one string, image, name, `openingHours` |

Filling in Business Information is what put content in them — before that they
were near-empty stubs. So the free path really does work, and what our block
adds on top is the part Squarespace can't express: a structured `PostalAddress`,
`geo` coordinates, `medicalSpecialty`, `areaServed`, and `knowsLanguage`.

Types don't collide either: Squarespace's is the broad `LocalBusiness`, ours is
`MedicalClinic`, which sits below it in the same family
(`MedicalClinic` → `MedicalBusiness` → `LocalBusiness`).

#### Fix the placeholder social links

Squarespace's `Organization` block ships with **demo** social accounts still in
it:

```json
"sameAs": ["http://facebook.com/squarespace",
           "http://instagram.com/squarespace",
           "http://twitter.com/squarespace"]
```

That is markup on the practice's own site telling Google the practice *is*
Squarespace's Facebook, Instagram, and Twitter. `sameAs` means "these are the
same entity" — it's the exact property we're careful about adding correctly, and
here it's pointing at a stranger.

Fix it in **Settings → Social Links**: remove the placeholder accounts, or
replace them with the practice's real profiles. Do this before worrying about
adding our own `sameAs`.

#### Values that differ harmlessly

Not every difference between their blocks and ours is a bug:

- **Phone format.** Theirs is `(720) 509-9640`, ours is `+17205099640`. Same
  number; the E.164 form is the one schema.org prefers, and Google parses both.
- **Address shape.** Theirs is one newline-joined string, ours is a structured
  `PostalAddress`. The street text is identical (`8850 W 58th Ave Ste 201`),
  which is what matters — that's why we keep that string exact.
- **Coordinates.** Squarespace derives its own map pin from the address
  (`39.8017574, -105.0963765`) which is a few metres off the pin in our `geo`
  (`39.801726, -105.096340`). At that distance it makes no practical
  difference; don't churn either one to match.

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

#### The Business Information panel and the address

The panel's **Physical Location** field is a Google Places lookup ("powered by
Google") and it *displays* the address in Google's expanded form — "8850 West
58th Avenue, Ste 201". Don't be alarmed by that: what Squarespace actually
stores and emits is the canonical string,

```
8850 W 58th Ave Ste 201
```

confirmed in the `LocalBusiness` and `Organization` markup on the live page. The
expansion is display-only.

What still matters: it kept `Ste` un-expanded. If the field is ever re-entered
and comes back as `Suite`, that's the one to catch — it breaks the
character-for-character match with the Google Business Profile.

#### Hours

The panel takes hours per day, so all six rows read `09:00 - 17:00` and Sunday
is `Closed`. That matches `openingHoursSpecification` exactly (Monday–Saturday,
opens 09:00, closes 17:00, no Sunday).

There is nowhere in the panel for **"by appointment only"** — it only accepts
times. That qualifier lives on the page (`pages/contact.html`), which is the
reason the page carries its own hours rather than deferring to this panel.

Worth re-reading the six rows after typing them: a stray character at the end of
a single day's field (`09:00 - 17:00x`) is nearly invisible in the panel and
makes that one day's hours unparseable.

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
