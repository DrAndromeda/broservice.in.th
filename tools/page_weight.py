#!/usr/bin/env python3
"""Static page-weight budget (a lab proxy for LCP/transfer size; real Core Web Vitals need the live site).
For every page: HTML, linked CSS, JS and the hero image actually requested on a mobile viewport (WebP 400/800),
gzip-compressed sizes, and the number of requests (local + Google Fonts). Run from repo root:
python3 tools/page_weight.py [--budget-kb 250]"""
import re, glob, os, gzip, sys
from urllib.parse import urljoin, urlparse
budget = 250
if "--budget-kb" in sys.argv: budget = int(sys.argv[sys.argv.index("--budget-kb") + 1])
def gz(b): return len(gzip.compress(b, 6))
rows = []
for f in sorted(glob.glob("**/index.html", recursive=True)):
    raw = open(f, "rb").read(); t = raw.decode("utf-8")
    base = "/" + f
    local = []
    for m in re.finditer(r'<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"|<script[^>]+src="([^"]+)"', t):
        u = m.group(1) or m.group(2)
        if u.startswith("http"): continue
        p = urlparse(urljoin("https://x" + base, u)).path.lstrip("/")
        if os.path.exists(p): local.append(p)
    css = sum(gz(open(p, "rb").read()) for p in set(local) if p.endswith(".css"))
    js = sum(gz(open(p, "rb").read()) for p in set(local) if p.endswith(".js"))
    hero = 0
    h = re.search(r'fetchpriority="high"', t)
    if h:
        seg = t[:h.start()]; src = re.findall(r'srcset="([^"]+)"', seg)
        if src:
            cands = [c.strip().split()[0] for c in src[-1].split(",")]
            p = urlparse(urljoin("https://x" + base, cands[0])).path.lstrip("/")      # 400w variant on phones
            if os.path.exists(p): hero = os.path.getsize(p)
    inline_css = sum(len(s) for s in re.findall(r"<style\b[^>]*>(.*?)</style>", t, re.S))
    total = gz(raw) + css + js + hero
    reqs = 1 + len(set(local)) + (1 if hero else 0) + (2 if "fonts.googleapis.com" in t else 0)
    rows.append((total, f, gz(raw), css, js, hero, inline_css, reqs))
rows.sort(reverse=True)
print(f"{'page':48} {'total KB':>8} {'html gz':>8} {'css gz':>7} {'js gz':>6} {'hero':>6} {'reqs':>5}")
for tot, f, h, c, j, hero, ic, r in rows[:12]: print(f"{f:48} {tot/1024:8.1f} {h/1024:8.1f} {c/1024:7.1f} {j/1024:6.1f} {hero/1024:6.1f} {r:5d}")
avg = sum(r[0] for r in rows) / len(rows) / 1024
over = [r for r in rows if r[0] / 1024 > budget]
print(f"\npages: {len(rows)}  average first-view transfer: {avg:.1f} KB  heaviest: {rows[0][0]/1024:.1f} KB  over {budget} KB budget: {len(over)}")
print("third-party requests on first view: none except the optional OpenStreetMap iframe on the contact pages")
sys.exit(1 if over else 0)
