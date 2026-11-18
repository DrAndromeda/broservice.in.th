# BroService.in.th — TODO Report

Dates: 2026-11-17 / 2026-11-18 · Base commit `ee7435f` · Rollback branch `backup/2026-11-17-pre-improvements`
Scope: **repository changes only. Nothing is deployed.** The full original specification stays in git history (`git show cc77f19:TO-DO_2026-11-12.md`); this file replaces `TO-DO_2026-11-12.md`.

## How to re-run the checks (from the repo root)

```
python3 tools/audit_seo.py        # titles, descriptions, H1, canonical, hreflang reciprocity, sitemap, noindex, links
python3 tools/audit_content.py    # FAQ JSON-LD == visible FAQ, markup balance, one H1, <main>, heading levels
python3 tools/audit_assets.py     # broken links/assets, paths above root, JSON-LD parse, image sizes, metadata lengths
python3 tools/validate_jsonld.py  # every JSON-LD block against the schema.org vocabulary (downloads it once)
python3 tools/page_weight.py      # first-view transfer per page vs a 250 KB budget
python3 tools/build_sitemap.py    # regenerate sitemap.xml (canonical + hreflang alternates) from the pages
xmllint --noout sitemap.xml
```

**Results at the end of this work:** 80 HTML files, 76 indexable pages (19 per language × 4) + 4 localized 404 pages; `audit_seo` 0 issues; `audit_content` 0 problems (all FAQ pages: visible FAQ == FAQPage JSON-LD); `audit_assets` 0 broken links/assets; `validate_jsonld` 0 problems; `page_weight` average first view 20.8 KB, heaviest 32.3 KB, 0 pages over budget; sitemap valid, 76 URLs with hreflang alternates. First audit at the start: 81 issues.

**Browser verification (headless Chrome against a local server, every page, JS-measured):** all 76 indexable pages loaded in headless Chrome at 320, 375, 768, 1024, 1280 and 1920 px (plus an earlier sweep at 360/390/430/1440): 0 horizontal overflow, 0 broken images, exactly one `<h1>` and one `<main>` on every page; text contrast measured on ~10,000 text elements at 375 px and ~8,800 at 1280 px: 0 failures after the last fix (the EN flower page nav button); tap-target scan: only the visually-hidden skip link is below size; interaction tests in EN/RU/TH/HE (menu open/Escape/focus, FAQ toggle, keyboard logo, labelled icons) and the consent banner all pass; all first-view requests are same-origin. The RU/TH/HE contact pages were tested with their external OpenStreetMap iframe removed (it cannot load in the sandbox); their layout passes.

---

## 1. Finished

### Foundations (Phases 0–1, 8–9)
- [x] Rollback branch, re-runnable audit tools, deployment proposal (`deploy/htaccess.recommended`), manifest and rollback steps (section 5).
- [x] Baseline audit of every page; repo structure, sitemap, links, hreflang, noindex/robots checked.

### SEO, structure, structured data (Phase 5)
- [x] Self-referencing canonical, `og:url`, JSON-LD URLs on every page; reciprocal hreflang with `x-default`; no references to missing pages.
- [x] Sitemap regenerated from the pages (`tools/build_sitemap.py`), 404 pages excluded, hreflang alternates, `lastmod`.
- [x] One stable business entity (`#localbusiness`) with identical details site-wide; Service blocks reference it; schema-valid (no `inLanguage` on Service).
- [x] FAQPage JSON-LD equals the visible FAQ exactly on all FAQ pages (many pages previously had FAQ JSON-LD with no visible FAQ); BreadcrumbList generated from the visible trail (single-item homepage breadcrumb removed).
- [x] Open Graph/Twitter metadata complete (locale + alternates, image size/alt; phone/flower pages use their own illustration).
- [x] `llms.txt` updated; robots.txt reviewed.

### Navigation, language, RTL (Phase 3)
- [x] Language switchers lead to the equivalent page on all 76 pages; logo/home links on RU/TH/HE go to their own homepage.
- [x] Mobile menu: `aria-expanded`/`aria-controls`, Escape closes, focus moves in and back; works without JS (`noscript.css`); FAQs use `<details>`.
- [x] Hebrew: numbers, prices, phones and hours isolated with `<bdi>`; RTL rules for FAQ/lists/breadcrumbs; no horizontal overflow (a skip-link bug that created 9999 px of scroll in RTL was found and fixed).
- [x] No layout overflow, clipped content or broken images at 320, 360, 375, 390, 430, 768, 1024, 1280, 1440 and 1920 px (see browser verification above).

### Content and multilingual (Phase 4)
- [x] Flower delivery translated into RU/TH/HE; About (`/about/`) and Privacy (`/privacy/`) pages in four languages; contact page has a real `tel:` link and a "what to include in your request" checklist.
- [x] Nine service pages × 4 languages gained five practical sections each (what is included, who needs it, how to prepare, what affects the price, when another specialist is needed) and extra FAQs — written only from page facts and generic guidance, no new prices/claims.
- [x] RU/TH/HE service pages and homepages brought to parity with EN (price tables with identical prices/units, "Why choose", process steps, service cards, 6 homepage FAQs); phone-repair FAQ prices aligned with the page's own table; dated price notes under every price table; property-rental card added to all homepages.
- [x] Removed an unverifiable "reviews / we'll connect you with past customers" block from RU/TH/HE homepages; replaced half-translated place names (TH/HE); fixed wrong H1s on TH/HE property-rental pages; repaired markup damage already in the repo (mangled footer links, missing `<h2>`, stray `<style>`, duplicate FAQ on the EN homepage).

### Design, accessibility, performance (Phases 2, 6)
- [x] **Contrast measured in a real browser** on every page and fixed: brand orange text/buttons, WhatsApp/Telegram buttons, breadcrumb and helper greys, drawer separators, footer text (all pass WCAG AA on the pages tested).
- [x] Tap targets ≥ 24 px on all viewports (WCAG 2.2 SC 2.5.8) and ≥ 44 px on touch layouts; keyboard-operable logo; labelled icon-only social links; skip link; `<main>` landmark; no heading-level skips; unique accessible names on homepage "View Service" links; visible focus; reduced-motion support.
- [x] Fonts self-hosted (Inter, Open Sans; nine subset files by `unicode-range`) — verified: every first-view request is same-origin, no third-party host.
- [x] Identical inline CSS moved into 11 shared cacheable stylesheets (≈ 600 KB less HTML across 67 pages); design tokens in `assets/css/common.css`.
- [x] Images: WebP + 400/800 px, `<picture>`, width/height everywhere, LCP hero not lazy and `fetchpriority="high"`; original photos kept; clearly-illustrative graphics for plumber, electrician, phone repair and flowers (the "plumber/electrician" photo was a hammer and nails; original kept in `assets/images/original/`).
- [x] Map replaced by an OpenStreetMap **area** map without a pin (no implied office); privacy text and proposed CSP updated.
- [x] Security hygiene: no secrets, no analytics/cookies by default, no mixed content, `rel="noopener"`, referrer policy, server hardening prepared (`deploy/htaccess.recommended`: CSP matched to real assets, compression, caching, one-hop HTTPS/host, no directory listing).

### Conversion and analytics (Phase 7)
- [x] Same contact actions on every page; labels match destinations; request checklist.
- [x] **Consent-gated analytics implemented** (`assets/js/config.js` + `consent-analytics.js`, GA4 and Meta Pixel): fully inert until IDs are set, honours Do Not Track/GPC, localized banner, privacy pages switch wording automatically. Tested in a browser: banner appears only when configured; no tracker loads before consent or after decline; inert when unconfigured.

---

## 2. Not possible from the repository (physically blocked)

| Item | Reason |
|---|---|
| Live crawl, redirects, real 404 status, HTTPS/host behaviour, effective Cloudflare robots | Production answered **HTTP 403** (origin "openresty", behind Cloudflare) from this network, so nothing live could be fetched. Live robots.txt is Cloudflare-managed, differs from the repo's and has no `Sitemap:` line — fix in Cloudflare. |
| Real Core Web Vitals (LCP/INP/CLS) | Needs the deployed site and real timing; headless virtual time distorts timing. Replaced by static `tools/page_weight.py` (lab proxy). |
| Google Rich Results Test | External tool. Replaced by full local validation against schema.org (0 problems). |
| Testing on real iOS/Android devices | No devices; viewport sweep in headless Chrome only. |
| Native-speaker review of new TH/HE/RU text | Needs a human reviewer; text was written by AI sub-agents. Terms they flagged: plumbing/electrical/AC vocabulary (cartridge, breaker, coil, isolation valve), "handyman" (הנדימן / ช่างซ่อมทั่วไป / мастер на все руки), place-name transliterations (Chaloklum: ช่อลกลำ/เฉลกหลำ, צ'לוקלום), rental terms (deposit, inventory, digital nomads), Thai politeness particles. |
| Real photographs (phone repair, flowers, electrician) | None exist; illustrations are used instead. |
| Deployment, Search Console / Bing submission | Needs your approval and account access. |
| Analytics IDs, legal-entity details, owner-only facts | Not in the repo; analytics loader waits for IDs. |
| Contact-flow test with a real destination | No test destination provided; the site has no forms. |

---

## 3. Owner decisions needed

- **Claims already on EN pages that cannot be verified** (kept as found): "warranty on all work", "trained staff / eco-friendly", "licensed technicians", "verified listings, personally inspected", "no agency fees", "reply within 24 hours". RU/TH/HE now mirror EN's claims; confirm or remove everywhere.
- **Translation-only content kept** (not in EN): "response time by area" tables on RU/TH/HE service pages (Thong Sala/Srithanu same day, Haad Rin/Baan Tai same day–next day, Chaloklum next day), a few phone-repair extras ("call before noon, same day", "free diagnosis, warranty on every job" in TH/HE), allergy/product note in cleaning. Decide whether to add to EN or remove.
- **Price consistency:** the phone-repair FAQ previously quoted prices that contradicted the page's own table (e.g. screens ฿800–2,500 vs ฿2,500–15,000); it now follows the table — confirm the table is right.
- **Privacy page** states what the site technically does; it has no legal-entity name or postal address (none in the repo). Have it reviewed if a legal notice is required.
- **Credentials:** commit `ee7435f` published SSH host, port, user and key path in repository history; treat as exposed and rotate if appropriate.
- **Process incident:** several sub-agents ran `git stash` concurrently; the tree was checked and repaired afterwards (duplicate FAQs removed, lost edits redone). Review `git diff` before merging.

---

## 4. Deployment manifest (when approved)

Upload to `public_html/broservice.in.th/`: `index.html`, `404.html`, `robots.txt`, `llms.txt`, `sitemap.xml`, every `*/index.html` and `*/404.html`, and `assets/` (`css/`, `js/`, `fonts/`, `images/`).
**Do not upload:** `TODO_REPORT.md`, `tools/`, `deploy/`, `.git`, any `.md/.py/.sh` file.

Before: `tar czf ~/backup-broservice-$(date +%F).tgz -C ~/public_html broservice.in.th` on the server.
After: open the homepage, one page per language, `/about/`, `/privacy/`, `/sitemap.xml`, `/robots.txt`, a 404 URL (must return HTTP 404); run `python3 tools/audit_seo.py`-style checks against the live host.
Rollback: restore the tarball, or `git checkout backup/2026-11-17-pre-improvements` and re-upload.
Merge `deploy/htaccess.recommended` into the live `.htaccess` only after review; enable the HSTS line last. To enable analytics, set IDs in `assets/js/config.js`, update the privacy wording if needed, redeploy.
