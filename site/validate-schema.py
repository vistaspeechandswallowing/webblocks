#!/usr/bin/env python3
"""Check the JSON-LD in header-injection.html against the real schema.org vocabulary.

    python3 site/validate-schema.py

Why this exists: the Rich Results Test is the final word, but it needs a public
URL and a browser. This catches the class of mistake that is easy to make and
invisible by eye — a property hung on a type that doesn't accept it. Both bugs
it found on its first run were exactly that:

  • medicalSpecialty is not valid on MedicalBusiness (it wants MedicalClinic,
    Hospital, Physician, or MedicalOrganization) — the type became MedicalClinic.
  • availableLanguage belongs to ContactPoint / ServiceChannel, not to an
    organization — the languages moved to knowsLanguage.

Both would have been silently ignored by consumers rather than reported as
errors, which is the worst way for markup to be wrong.

What it checks, for every node and nested node:
  • the @type exists in the vocabulary
  • every property exists, and the node's type is in that property's
    domainIncludes (walking the full subClassOf chain)
  • a nested node's type is in the property's rangeIncludes
  • properties whose range is URL actually got a URL
  • no unfilled "[PLACEHOLDER]" strings survived
  • an enumeration value (medicalSpecialty) is a real member

It does NOT check Google's own requirements — which properties Google wants for
a rich result is Google's business, so still run the Rich Results Test on the
live URL. See README.md.

Needs network: it downloads the schema.org vocabulary (~1.5MB) and caches it
next to this script as .schemaorg-cache.jsonld. Delete that file to refresh.
"""
import json, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, ".schemaorg-cache.jsonld")
# Pinned release. schema.org's own host blocks some networks, so the vocabulary
# is fetched from the project's GitHub repo instead — same file.
VOCAB = ("https://raw.githubusercontent.com/schemaorg/schemaorg/main/"
         "data/releases/29.2/schemaorg-current-https.jsonld")


def vocabulary():
    if not os.path.exists(CACHE):
        sys.stderr.write("fetching the schema.org vocabulary…\n")
        with urllib.request.urlopen(VOCAB) as r, open(CACHE, "wb") as f:
            f.write(r.read())
    graph = json.load(open(CACHE))["@graph"]
    return {node["@id"]: node for node in graph}


def ids(node, key):
    value = node.get(key, [])
    if isinstance(value, dict):
        value = [value]
    return [v["@id"] for v in value if isinstance(v, dict) and "@id" in v]


def ancestors(nodes, type_id, seen=None):
    """type_id plus every type it inherits from."""
    seen = seen if seen is not None else set()
    if type_id in seen:
        return seen
    seen.add(type_id)
    for parent in ids(nodes.get(type_id, {}), "rdfs:subClassOf"):
        ancestors(nodes, parent, seen)
    return seen


def check(nodes, obj, path, errors):
    type_name = obj.get("@type")
    type_id = "schema:" + str(type_name)
    if type_id not in nodes:
        errors.append(f"{path}: unknown type {type_name!r}")
        return 0
    inherited = ancestors(nodes, type_id)
    checked = 0

    for key, value in obj.items():
        if key.startswith("@"):
            continue
        checked += 1
        prop = nodes.get("schema:" + key)
        if prop is None:
            errors.append(f"{path}.{key}: not a schema.org property")
            continue

        domain = set(ids(prop, "schema:domainIncludes"))
        if not domain & inherited:
            allowed = ", ".join(sorted(d.split(":")[1] for d in domain))
            errors.append(
                f"{path}.{key}: not valid on {type_name} — "
                f"schema.org allows it on: {allowed}")

        range_ = set(ids(prop, "schema:rangeIncludes"))
        values = value if isinstance(value, list) else [value]
        for i, item in enumerate(values):
            where = f"{path}.{key}" + (f"[{i}]" if isinstance(value, list) else "")
            if isinstance(item, dict) and "@type" in item:
                item_id = "schema:" + item["@type"]
                if range_ and not (ancestors(nodes, item_id) & range_):
                    allowed = ", ".join(sorted(r.split(":")[1] for r in range_))
                    errors.append(
                        f"{where}: {item['@type']} is not an accepted value "
                        f"type — schema.org expects: {allowed}")
                checked += check(nodes, item, where, errors)
            elif isinstance(item, str):
                if item.startswith("[") and item.endswith("]"):
                    errors.append(f"{where}: unfilled placeholder {item!r}")
                elif ("schema:URL" in range_ and "schema:Text" not in range_
                        and not re.match(r"https?://", item)):
                    errors.append(f"{where}: expects a URL, got {item!r}")
                elif ("schema:" + item) in nodes and range_:
                    # An enumeration member (e.g. medicalSpecialty:
                    # SpeechPathology) — confirm it belongs to the right one.
                    member_of = nodes["schema:" + item].get("@type")
                    member_of = member_of if isinstance(member_of, str) else ""
                    if member_of and member_of not in range_:
                        errors.append(
                            f"{where}: {item!r} is a {member_of.split(':')[1]}, "
                            f"not one of "
                            f"{', '.join(sorted(r.split(':')[1] for r in range_))}")
    return checked


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        HERE, "header-injection.html")
    source = open(target).read()
    blocks = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', source, re.S)
    if not blocks:
        sys.exit(f"no JSON-LD found in {target}")

    nodes = vocabulary()
    errors, checked = [], 0
    for i, block in enumerate(blocks):
        try:
            data = json.loads(block)
        except json.JSONDecodeError as exc:
            errors.append(f"block {i}: invalid JSON — {exc}")
            continue
        checked += check(nodes, data, "$", errors)

    print(f"{target}: checked {checked} properties "
          f"in {len(blocks)} JSON-LD block(s)\n")
    for error in errors:
        print("  ERROR  " + error)
    if errors:
        print(f"\n{len(errors)} error(s)")
        sys.exit(1)
    print("No errors. Still run the Rich Results Test on the live URL.")


if __name__ == "__main__":
    main()
