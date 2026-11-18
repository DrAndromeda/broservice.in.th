#!/usr/bin/env python3
"""Regenerate sitemap.xml from the pages themselves (canonical URL + hreflang alternates).
Usage (repo root): python3 tools/build_sitemap.py [YYYY-MM-DD lastmod]"""
import re, glob, sys, datetime, os
lastmod = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
old = open("sitemap.xml", encoding="utf-8").read() if os.path.exists("sitemap.xml") else ""
meta = {m.group(1): (m.group(2), m.group(3)) for m in re.finditer(r"<url>\s*<loc>(.*?)</loc>.*?<changefreq>(.*?)</changefreq>\s*<priority>(.*?)</priority>", old, re.S)}
pages = []
for f in sorted(glob.glob("**/index.html", recursive=True), key=lambda p: (p.count("/"), p)):
    t = open(f, encoding="utf-8").read()
    robots = re.search(r'<meta name="robots" content="([^"]*)"', t)
    if robots and "noindex" in robots.group(1): continue
    c = re.search(r'<link rel="canonical" href="([^"]+)"', t).group(1)
    alts = re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', t)
    pages.append((c, alts))
pages.sort(key=lambda x: (x[0] != "https://broservice.in.th/", x[0].count("/"), x[0]))
out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for c, alts in pages:
    cf, pr = meta.get(c, ("yearly", "0.3") if c.endswith(("/privacy/", "/about/")) else ("monthly", "0.7"))
    out += ["  <url>", f"    <loc>{c}</loc>", f"    <lastmod>{lastmod}</lastmod>", f"    <changefreq>{cf}</changefreq>", f"    <priority>{pr}</priority>"]
    out += [f'    <xhtml:link rel="alternate" hreflang="{l}" href="{u}"/>' for l, u in alts]
    out.append("  </url>")
out.append("</urlset>")
open("sitemap.xml", "w", encoding="utf-8").write("\n".join(out) + "\n")
print(len(pages), "urls written")
