#!/usr/bin/env python3
"""Asset/link audit: broken links and assets, paths escaping the root, JSON-LD validity, metadata lengths, image dimensions. Run from repo root: python3 tools/audit_assets.py"""
import re,os,glob,json
from urllib.parse import urlparse,urljoin
from collections import Counter,defaultdict
pages=sorted(f for f in glob.glob("**/*.html",recursive=True))
bad=defaultdict(list); 
def chk(p,l):
    if not l or l.startswith(("mailto:","tel:","#","javascript:","data:")): return
    pu=urlparse(l)
    if pu.scheme in("http","https"):
        if pu.netloc not in("broservice.in.th",): return
        path=pu.path
    elif pu.scheme: return
    else: path=urlparse(urljoin("/"+p,l)).path
    # clamp: detect escaping root
    if l.startswith("../") and l.count("../")>p.count("/"): bad["escapes-root"].append(f"{p}: {l}")
    fs=path.lstrip("/")
    if fs=="" or fs.endswith("/"): fs+="index.html"
    if not os.path.exists(fs) and not os.path.isdir(fs.rstrip("/")): bad["broken"].append(f"{p}: {l}")
for p in pages:
    t=open(p,encoding="utf-8").read()
    for m in re.finditer(r'<(?:a|link|script|img|source|meta)\b[^>]*?\b(?:href|src|content)="([^"]*)"',t):
        v=m.group(1)
        if re.match(r'^(\.|/|https://broservice)',v) and not v.startswith("//"): chk(p,v)
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>',t,re.S):
        try: json.loads(m.group(1))
        except Exception as e: bad["bad-jsonld"].append(f"{p}: {e}")
    ti=re.search(r"<title>(.*?)</title>",t,re.S); de=re.search(r'name="description" content="([^"]*)"',t)
    if ti and len(ti.group(1))>70: bad["title>70"].append(f"{p}: {len(ti.group(1))}")
    if de and (len(de.group(1))>170 or len(de.group(1))<70): bad["desc-len"].append(f"{p}: {len(de.group(1))}")
    if "<img" in t:
        for im in re.findall(r"<img\b[^>]*>",t):
            if "width=" not in im or "height=" not in im: bad["img-no-dims"].append(f"{p}: {im[:80]}")
    if not re.search(r'<a [^>]*target="_blank"[^>]*rel=',t) and 'target="_blank"' in t: bad["blank-no-rel"].append(p)
    if "http://" in t.replace("http://www.sitemaps","").replace('xmlns="http://www.w3.org',""): bad["http-ref"].append(p)
for k,v in bad.items():
    print(f"## {k}: {len(v)}")
    for x in v[:8]: print("  ",x)
import subprocess

import sys; sys.exit(1 if any(bad[k] for k in ("broken","escapes-root","bad-jsonld","img-no-dims","http-ref")) else 0)
