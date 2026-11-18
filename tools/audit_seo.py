#!/usr/bin/env python3
"""SEO / structure audit: titles, descriptions, H1, canonical, hreflang reciprocity, sitemap coverage, noindex, internal links. Run from repo root: python3 tools/audit_seo.py"""
import re,os,sys,glob
from html.parser import HTMLParser
from urllib.parse import urlparse,urljoin
ROOT=os.getcwd(); BASE="https://broservice.in.th"
pages=sorted(glob.glob("**/*.html",recursive=True))
def url_of(p):
    if p.endswith("index.html"): return BASE+"/"+p[:-10]
    return BASE+"/"+p
class P(HTMLParser):
    def __init__(s):
        super().__init__();s._t=None;s.d=dict(title="",desc=None,h1=[],canon=None,hl={},robots=None,links=[],imgs=[],lang=None,dir=None,ld=0,viewport=False,alts_missing=0)
    def handle_starttag(s,t,a):
        a=dict(a)
        if t=="html": s.d["lang"]=a.get("lang");s.d["dir"]=a.get("dir")
        if t=="title": s._t="title"
        if t=="h1": s._t="h1";s.d["h1"].append("")
        if t=="meta":
            n=(a.get("name") or "").lower()
            if n=="description": s.d["desc"]=a.get("content")
            if n=="robots": s.d["robots"]=a.get("content")
            if n=="viewport": s.d["viewport"]=True
        if t=="link":
            r=a.get("rel","")
            if r=="canonical": s.d["canon"]=a.get("href")
            if r=="alternate" and a.get("hreflang"): s.d["hl"][a["hreflang"]]=a.get("href")
        if t=="a" and a.get("href"): s.d["links"].append(a["href"])
        if t=="img":
            s.d["imgs"].append(a.get("src"))
            if not a.get("alt") and a.get("alt")!="" : s.d["alts_missing"]+=1
        if t=="script" and a.get("type")=="application/ld+json": s.d["ld"]+=1
    def handle_endtag(s,t):
        if t in("title","h1"): s._t=None
    def handle_data(s,x):
        if s._t=="title": s.d["title"]+=x
        elif s._t=="h1": s.d["h1"][-1]+=x
info={}
for p in pages:
    h=P(); h.feed(open(p,encoding="utf-8").read()); info[p]=h.d
sm=re.findall(r"<loc>(.*?)</loc>",open("sitemap.xml").read())
issues=[]
def I(p,m): issues.append(f"{p}: {m}")
smset=set(sm)
for p,d in info.items():
    u=url_of(p); is404=p.endswith("404.html")
    if not d["title"].strip(): I(p,"no title")
    if not is404:
        if not d["desc"]: I(p,"no meta description")
        if len(d["h1"])!=1: I(p,f"h1 count {len(d['h1'])}")
        if d["canon"]!=u: I(p,f"canonical {d['canon']} != {u}")
        if u not in smset: I(p,"not in sitemap")
        if d["robots"] and "noindex" in d["robots"]: I(p,"noindex but indexable")
        # hreflang reciprocity
        for l,href in d["hl"].items():
            tp=urlparse(href).path.lstrip("/"); tp=tp+"index.html" if tp.endswith("/") or tp=="" else tp
            if tp not in info: I(p,f"hreflang {l} -> missing file {href}"); continue
            back=info[tp]["hl"]
            if not any(urlparse(v).path==urlparse(u).path for v in back.values()): I(p,f"hreflang {l} {href} not reciprocal")
        if "x-default" not in d["hl"]: I(p,"no x-default")
        if u not in d["hl"].values() and d["hl"]: I(p,"hreflang lacks self")
    else:
        if not d["robots"] or "noindex" not in d["robots"]: I(p,"404 lacks noindex")
    if not d["viewport"]: I(p,"no viewport")
    if not d["lang"]: I(p,"no lang")
    if p.startswith("he/") and d["dir"]!="rtl": I(p,"he page without dir=rtl")
    if d["alts_missing"]: I(p,f"{d['alts_missing']} imgs missing alt")
    if d["ld"]==0 and not is404: I(p,"no JSON-LD")
    for l in d["links"]+d["imgs"]:
        if not l or l.startswith(("mailto:","tel:","#","javascript:","https://wa.me","https://t.me")): continue
        if l.startswith("//") : continue
        pu=urlparse(l)
        if pu.scheme in("http","https"):
            if pu.netloc not in("broservice.in.th","www.broservice.in.th"): continue
            path=pu.path
        else:
            path=urlparse(urljoin("/"+p,l)).path
        fs=path.lstrip("/")
        if fs=="" or fs.endswith("/"): fs+="index.html"
        if not os.path.exists(fs):
            if os.path.isdir(fs.rstrip("/")) : continue
            I(p,f"broken link {l}")
for u in sm:
    fs=urlparse(u).path.lstrip("/"); fs=fs+"index.html" if fs.endswith("/") or fs=="" else fs
    if not os.path.exists(fs): I("sitemap",f"{u} no file")
print(len(pages),"pages;",len(sm),"sitemap urls;",len(issues),"issues")
from collections import Counter
t=Counter(d["title"].strip() for d in info.values()); 
for k,v in t.items():
    if v>1: print("DUP TITLE",v,k)
for i in issues: print(i)
sys_exit = __import__("sys").exit; sys_exit(1 if issues else 0)
