#!/usr/bin/env python3
"""Content audit: FAQPage JSON-LD must match the visible FAQ exactly, markup must be balanced,
every page needs one <h1>, a <main> landmark and no heading-level skips. Run from repo root:
python3 tools/audit_content.py"""
import re, json, glob, html, sys
from html.parser import HTMLParser

def norm(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()
problems = []

class H(HTMLParser):
    VOID = {"meta", "link", "img", "br", "hr", "input", "source", "area", "base", "col", "embed", "param", "track", "wbr"}
    def __init__(s): super().__init__(); s.st = []; s.err = []
    def handle_starttag(s, t, a):
        if t not in s.VOID: s.st.append(t)
    def handle_endtag(s, t):
        if t in s.VOID: return
        if t in s.st:
            while s.st and s.st[-1] != t: s.err.append("unclosed <%s> line %d" % (s.st.pop(), s.getpos()[0]))
            s.st.pop()
        else: s.err.append("stray </%s> line %d" % (t, s.getpos()[0]))

for f in sorted(glob.glob("**/*.html", recursive=True)):
    t = open(f, encoding="utf-8").read()
    h = H(); h.feed(t)
    for e in h.err + ["unclosed <%s>" % x for x in h.st if x not in ("html", "body", "head")]:
        problems.append(f + ": markup " + e)
    if f.endswith("404.html"): continue
    body = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    if len(re.findall(r"<h1\b", body)) != 1: problems.append(f + ": h1 count != 1")
    if "<main" not in body: problems.append(f + ": no <main> landmark")
    lv = []
    for m in re.finditer(r"<h([1-6])\b([^>]*)>", body):
        a = re.search(r'aria-level="(\d)"', m.group(2)); lv.append(int(a.group(1)) if a else int(m.group(1)))
    if any(b - a > 1 for a, b in zip(lv, lv[1:])): problems.append(f + ": heading level skip %s" % lv[:12])
    js = []
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        j = json.loads(m)
        if j.get("@type") == "FAQPage":
            js += [(norm(x["name"]), norm(x["acceptedAnswer"]["text"])) for x in j["mainEntity"]]
    if js:
        vis = [(norm(q), norm(a)) for q, a in re.findall(r'<summary>(.*?)</summary><div class="faq-answer"><p>(.*?)</p></div>', t, re.S)]
        if not vis:
            seg = t[t.find("Frequently Asked"):t.find("Order Now on WhatsApp")]
            vis = [(norm(q), norm(a)) for q, a in re.findall(r"<h3>(.*?)</h3>\s*<p>(.*?)</p>", seg, re.S)]
        if sorted(vis) != sorted(js): problems.append("%s: FAQPage JSON-LD (%d) does not match visible FAQ (%d)" % (f, len(js), len(vis)))
print("content audit:", len(problems), "problems")
for p in problems: print(" ", p)
sys.exit(1 if problems else 0)
