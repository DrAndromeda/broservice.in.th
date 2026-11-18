#!/usr/bin/env python3
"""Validate every JSON-LD block against the schema.org vocabulary (types, properties, domains)
plus the Google rich-result essentials for FAQPage and BreadcrumbList.
Usage (repo root): python3 tools/validate_jsonld.py [path/to/schemaorg-current-https.jsonld]
Without an argument the vocabulary is downloaded once from schema.org (public file)."""
import json, re, glob, sys, os, urllib.request

vp = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.environ.get("TMPDIR", "/tmp"), "schemaorg-current-https.jsonld")
if not os.path.exists(vp):
    urllib.request.urlretrieve("https://schema.org/version/latest/schemaorg-current-https.jsonld", vp)
G = {n["@id"]: n for n in json.load(open(vp, encoding="utf-8"))["@graph"]}
def ids(x):
    if x is None: return []
    return [i["@id"] for i in (x if isinstance(x, list) else [x])]
def sup(t):
    out, todo = set(), [t]
    while todo:
        c = todo.pop()
        if c in out: continue
        out.add(c); todo += ids(G.get(c, {}).get("rdfs:subClassOf"))
    return out
def tid(t): return "schema:" + t
PROPS = {}
for n in G.values():
    if n.get("@type") == "rdf:Property":
        for d in ids(n.get("schema:domainIncludes")): PROPS.setdefault(d, set()).add(n["@id"])
def allowed(t): 
    s = set()
    for c in sup(tid(t)): s |= PROPS.get(c, set())
    return s

errors = []
def walk(node, f, path="$"):
    if isinstance(node, list):
        for i, x in enumerate(node): walk(x, f, f"{path}[{i}]")
        return
    if not isinstance(node, dict): return
    t = node.get("@type")
    if t:
        types = t if isinstance(t, list) else [t]
        for ty in types:
            if tid(ty) not in G: errors.append(f"{f} {path}: unknown type {ty}"); continue
            ok = allowed(ty)
            for k, v in node.items():
                if k.startswith("@"): continue
                if "schema:" + k not in ok: errors.append(f"{f} {path}: property '{k}' not valid for {ty}")
    for k, v in node.items():
        if not k.startswith("@"): walk(v, f, f"{path}.{k}")

for f in sorted(glob.glob("**/*.html", recursive=True)):
    t = open(f, encoding="utf-8").read()
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try: j = json.loads(m)
        except Exception as e: errors.append(f"{f}: invalid JSON {e}"); continue
        walk(j, f)
        ty = j.get("@type")
        if ty == "FAQPage":
            if not j.get("mainEntity"): errors.append(f"{f}: FAQPage without mainEntity")
            for q in j.get("mainEntity", []):
                if q.get("@type") != "Question" or not q.get("name") or not q.get("acceptedAnswer", {}).get("text"):
                    errors.append(f"{f}: malformed FAQ question {q.get('name')}")
        if ty == "BreadcrumbList":
            items = j.get("itemListElement", [])
            if len(items) < 2 or [i.get("position") for i in items] != list(range(1, len(items) + 1)): errors.append(f"{f}: breadcrumb positions")
            for i in items:
                if not i.get("name") or not i.get("item"): errors.append(f"{f}: breadcrumb item missing name/item")
        if ty == "LocalBusiness":
            for k in ("name", "address", "telephone", "url"):
                if k not in j: errors.append(f"{f}: LocalBusiness missing {k}")
print("jsonld validation:", len(errors), "problems")
for e in errors[:40]: print(" ", e)
sys.exit(1 if errors else 0)
