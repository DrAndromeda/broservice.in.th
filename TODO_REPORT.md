# BroService.in.th — TODO Report

Date: 2026-11-17 · Base commit: `ee7435f` · Rollback branch: `backup/2026-11-17-pre-improvements`
Scope: repository changes only. **Nothing has been deployed and nothing was checked on the live site.**
Replaces `TO-DO_2026-11-12.md` (removed). The full original specification stays available in git history (`git show cc77f19:TO-DO_2026-11-12.md`).

## How to re-run the checks

```
python3 tools/audit_seo.py       # titles, descriptions, H1, canonical, hreflang reciprocity, sitemap, noindex, links
python3 tools/audit_assets.py    # broken links/assets, paths above root, JSON-LD validity, image sizes, metadata lengths
python3 tools/audit_content.py   # FAQ JSON-LD == visible FAQ, markup balance, one H1, <main>, heading levels
xmllint --noout sitemap.xml
```

Result at the end of this work: `audit_seo` 76 pages / 72 sitemap URLs / 0 issues; `audit_content` 0 problems (40 FAQ pages match exactly); `audit_assets` 0 broken links, 0 JSON-LD errors, 0 missing image sizes (the only output is informational: 404 pages and short Hebrew descriptions); sitemap valid XML.
Baseline at the start (first audit): 81 issues.

---

## 1. Finished

### Phase 1 — Baseline audit
- [x] Inspected all pages, language folders, assets and shared assumptions; wrote re-runnable audit scripts in `tools/`.
- [x] Inventory: 72 indexable pages (18 EN service/area/utility pages × 4 languages, with differing slugs for phone repair and flowers) + 4 localized 404 pages.
- [x] Sitemap compared with real pages page by page; broken links, orphans, wrong canonicals and invalid hreflang found and fixed (list below).
- [x] Accidental noindex / robots blocks checked: only the four 404 pages are noindex and disallowed, as intended.

### Phase 2 — Brand, design, experience
- [x] Design tokens documented in `assets/css/common.css` (colours, spacing, radius, content width, tap target, breakpoints).
- [x] Colour contrast fixed with measured ratios: brand orange `#e88800` was 2.64:1 on white and white-on-orange buttons 2.64:1; WhatsApp button 1.98:1; Telegram 3.89:1. Light content areas now use `#9c5400` (5.7:1 on white, 4.9:1 on the page grey), WhatsApp `#0b7f43` (5.1:1), Telegram `#0077b3` (4.9:1). Header and footer keep the brand orange (6.9:1 on dark). Breadcrumb grey `#888` (3.2:1) → `#595959`.
- [x] Sticky contact bar can no longer cover content (bottom padding when the bar exists).
- [x] Images: alt text corrected where wrong (homepage card), width/height on all images, WebP + 400px/800px variants generated with `<picture>` (JPEG kept as fallback and original; 516 KB JPEG → 363 KB WebP at 800 px, 104 KB at 400 px).
- [x] Reduced-motion support; consistent focus outline.

### Phase 3 — Navigation, language, responsive
- [x] Language switchers: 60 of 69 pages were wrong (homepage or wrong language); every item now goes to the equivalent page, on all 72 pages (drawer and top switcher).
- [x] Logo and "Home" links on RU/TH/HE pages went to the English homepage; now go to the language homepage.
- [x] Mobile menu: `aria-expanded`/`aria-controls`, Escape closes, focus moves into and back out of the drawer (`assets/js/a11y.js`); aria-label on the unlabeled menu button.
- [x] Menus remain usable without JavaScript (`assets/css/noscript.css`); FAQs use native `<details>` (no JS).
- [x] RTL: Hebrew phone numbers, emails, prices and hours isolated with `<bdi>`; RTL rules for FAQ, breadcrumbs, lists on the new Hebrew page.
- [x] Tap targets ≥44 px on touch layouts; tables scroll instead of overflowing on small screens.
- [x] 29 favicon links 404'd and 177 links used more `../` than the folder depth; all fixed.

### Phase 4 — Content and multilingual
- [x] **Flower delivery translated** into RU (`ru/dostavka-tsvetov-koh-phangan/`), TH and HE (`…/flower-delivery-koh-phangan/`), using only facts from the English page; added to sitemap, hreflang, switchers, footers.
- [x] Phone-repair pages in all four languages cleaned of handyman leftovers (wrong breadcrumb, hero photo, FAQ and Service schema); the Thai page's English menus and footer replaced with Thai.
- [x] Thai/Hebrew property-rental pages showed a phone-repair H1; fixed.
- [x] Thai "Thong Sala" normalized to ท้องศาลา (was "ท้อง Sala" etc.); Hebrew Thong Sala, Koh Phangan, Haad Rin, Srithanu spellings normalized.
- [x] Broken markup already in the repo repaired: mangled footer link on 13 English pages, missing `<h2>` on the homepage, stray `</li><li>` in the phone card; stray unclosed `<style>` tag (broke the first CSS rule) on 7 pages; "Step" counter hard-coded in English on translated pages.
- [x] Homepage: flower card added; footer service lists on every page now link to phone repair, flower delivery and property rental in that language (several of these pages had almost no inbound links).
- [x] **Privacy page** in four languages (`/privacy/`, `/ru/privacy/`, `/th/privacy/`, `/he/privacy/`), written only from what the site actually does (no analytics/cookies of its own, Google Fonts and Google Map, contact via messengers); linked from every footer and `llms.txt`.
- [x] Contact pages: real `tel:` link (the phone line previously pointed at Telegram), "what to include in your request" checklist in four languages, accessible title on the map iframe.
- [x] Opening-hours format unified (`8:00–20:00`); contact buttons labelled by their real destination ("Call" buttons that opened Telegram now say Telegram).

### Phase 5 — SEO, local SEO, GEO, structured data
- [x] Canonical, `og:url` and JSON-LD URL are self-referencing on every page (TH/HE location pages pointed at English).
- [x] hreflang rebuilt from one cluster map: reciprocal, with `x-default`, no missing targets (malformed `hreflang="hreflang=…"` removed; wrong language codes fixed).
- [x] Sitemap regenerated: 72 canonical pages, `lastmod`, and `xhtml:link` hreflang alternates; 404 pages excluded.
- [x] One stable business entity `@id` (`https://broservice.in.th/#localbusiness`) with identical name, URL, phone, email, area, hours and `sameAs` on every page; Service blocks reference it as provider.
- [x] FAQPage markup now equals the visible FAQ exactly on all 40 FAQ pages (previously many pages had FAQ JSON-LD with no visible FAQ, or mismatched counts).
- [x] BreadcrumbList regenerated from the visible breadcrumb trail on 68 pages; handyman breadcrumb and Service schema removed from phone-repair pages.
- [x] Open Graph complete (`og:locale` + alternates, image size and alt); `twitter:image:alt`.
- [x] `llms.txt` updated (flower delivery, privacy); robots.txt reviewed (sitemap URL correct, nothing important blocked).
- [x] Trailing-slash policy: all internal URLs end in `/` (enforcement rule written in `deploy/htaccess.recommended`).

### Phase 6 — Performance, accessibility, security
- [x] LCP: hero images no longer lazy-loaded, `fetchpriority="high"` on 32 pages; below-the-fold images lazy with `decoding="async"`.
- [x] Skip-to-content link and `<main>` landmark on every page; heading hierarchy has no level skips (footer headings and contact cards carry `aria-level`); homepage "View Service" links have unique accessible names.
- [x] `rel="noopener"` on all `target="_blank"` links; `Referrer-Policy` meta on every page.
- [x] Secrets scan: none found; no analytics or tracking scripts, no cookies set by site code, no mixed content, no forms.
- [x] Server hardening prepared in `deploy/htaccess.recommended` (security headers incl. CSP matched to the actual assets, compression, caching, one-hop HTTPS/host redirect, no directory listing, blocks `.md/.py/.sh` files). **Prepared, not applied.**

### Phase 7 — Conversion
- [x] Same contact actions on every page (sticky bar on mobile, header and footer links); labels match destinations; checklist of what to send when requesting a service.

### Phase 8/9 — Technical and handoff
- [x] Rollback branch created; deployment manifest and rollback steps below; audit scripts and exact commands recorded.

---

## 2. Implemented in code, not verified visually or on devices

The code is written, but I could not render pages (the browser tool cannot open local files and starting a local server was blocked in this environment). Please open these before deploying:

- Contrast changes (scoped CSS variables in `main`, literal colour replacements in 50 style rules and 92 inline styles) — check orange text/buttons on every page type, and that nothing on a dark background became too dark.
- `<picture>` wrapping and image sizes on the homepages and service pages.
- Hebrew pages: RTL FAQ, `<bdi>` isolation, new flower and privacy pages.
- Mobile drawer behaviour with `a11y.js` (both template variants), at 320–1920 px.
- New FAQ accordion styling (`<details>`) against the old button accordion.

---

## 3. Not possible from the repository (real blockers)

| Item | Why it cannot be done here |
|---|---|
| Core Web Vitals measurement (LCP < 2.5 s, INP < 200 ms, CLS < 0.1) | Needs the deployed site and a measurement tool; spec requires measured, not estimated, numbers. |
| Schema.org Validator / Google Rich Results Test | External online tools. Local JSON-LD parsing and structural consistency are checked (0 errors). |
| Live crawl of every sitemap URL, HTTP status, redirect chains, HTTPS/host/trailing-slash behaviour, real 404 status | Requires the production server. |
| Effective live `robots.txt` including Cloudflare-managed rules | Requires fetching production behind Cloudflare. |
| Production deployment, Search Console / Bing submission, monitoring | Needs owner approval and account access. |
| Analytics / advertising pixels | Needs owner-supplied IDs and a consent decision; adding a script without them would be a no-op or non-compliant. |
| Real photos: phone repair, flower delivery, a distinct electrician photo | Spec forbids unrelated images; no suitable photos exist in the repo. Currently the electrician and plumber photos are the same file (`electrician.jpg` = `plumber.jpg`, identical checksum); the phone-repair card shows a resort photo with an honest alt text. |
| Service pages of 1,000–1,500 words, pricing tables with dates/conditions, distinct local content per area, About page | Need verified operational facts (scope, exclusions, current prices, history, team). The spec forbids inventing them. |
| Consolidating the 21 per-template inline `<style>` blocks into shared stylesheets | The variants differ in small ways; unifying them safely needs visual regression testing, which is not possible here. Shared tokens and an accessibility layer were added instead. |
| Testing on real iOS/Android devices and at the ten listed widths | Needs physical devices or a rendering browser. |
| Contact-flow tests with an authorised test destination | None provided; the site has no forms. |
| Native-speaker review of Thai/Hebrew terms | Needs a human reviewer (see list in section 4). |

---

## 4. Owner decisions and review needed

- **Unverified claims already on the site** (not changed by me): "Reply within 24 hours" and "Quick response via our bot" on the contact pages; "Warranty on all work" site-wide; "Available 8:00–20:00, 7 days" (used for the structured-data opening hours). Confirm or remove.
- **Map pin on the contact page** is an embedded Google Maps location marker; the spec says not to imply a physical office or branch. Confirm it is intended.
- **Price tables** have no "as of" date or conditions; flower prices carry an "approximate" note, others do not.
- **Thai/Hebrew terminology for native review:** Thai place names still vary (`หาดริ้น`/`หาดริน`, `ช่อลกลำ`/`เฉลกหลำ`); Hebrew uses `קוה פנגן` and Latin-script area labels in footers; new privacy/flower/FAQ text was written without a native reviewer.
- **Privacy page** states what the site technically does; it contains no legal-entity name or postal address because none exists in the repo. Have it reviewed if a legal notice is required.
- **Credentials:** an earlier commit (`ee7435f`) published the SSH host, port, user and key path in this repository's history; treat them as exposed and rotate if appropriate.

---

## 5. Deployment manifest (for when you approve)

Upload to `public_html/broservice.in.th/` (preserve folders):
`index.html`, `404.html`, `robots.txt`, `llms.txt`, `sitemap.xml`, every `*/index.html` (including `ru/`, `th/`, `he/`, `privacy/`, `flower-delivery-koh-phangan/`, …), the `*/404.html` files, and `assets/` (`css/`, `js/`, `images/`).
**Do not upload:** `TODO_REPORT.md`, `tools/`, `deploy/`, `.git`, any `.md/.py/.sh` file.

Before: `tar czf ~/backup-broservice-$(date +%F).tgz -C ~/public_html broservice.in.th` on the server.
After: open the homepage, one page per language, `/privacy/`, `/sitemap.xml`, `/robots.txt`, a 404 URL (must return HTTP 404).
Rollback: restore the tarball, or `git checkout backup/2026-11-17-pre-improvements` and re-upload.
Merge `deploy/htaccess.recommended` into the live `.htaccess` only after review; enable the HSTS line last.

---

## Addendum — work completed after the sections above (2026-11-18)

**Supersedes the "Not possible" table where noted. Everything below is implemented in the repository; nothing is deployed.**

- **Content (all 4 languages):** 9 service pages gained five practical sections each plus extra FAQs; RU/TH/HE service pages now have the same price tables, "Why choose", process steps and claims as EN; RU/TH/HE homepages match EN (all service cards, sections, 6 FAQs); About pages (`/about/`) added; unverifiable "reviews" block removed from RU/TH/HE homepages; dated price notes under every price table; phone-repair FAQ prices aligned to the page's own price table.
- **Contrast/accessibility (measured in a real browser):** all text now passes WCAG AA on the pages tested; tap targets ≥24 px on all viewports and ≥44 px on touch; keyboard-operable logo; labelled social icons; FAQ accordions everywhere; no layout overflow or broken images at 320–1920 px on 76 pages; menu open/Escape/focus and FAQ toggles pass in EN/RU/TH/HE.
- **Performance/privacy:** fonts self-hosted (no third-party request on first view); identical inline CSS moved to 11 shared cacheable stylesheets (about 600 KB less HTML); WebP + responsive sizes; illustrations for plumber, electrician, phone repair, flowers (original hammer photo kept in `assets/images/original/`); map is now an OpenStreetMap area map without a pin. `tools/page_weight.py`: average first view 20.8 KB, heaviest 32.3 KB.
- **Analytics:** consent-gated loader implemented (`assets/js/config.js`, `consent-analytics.js`): fully inert until IDs are set; honours Do Not Track/GPC; privacy pages switch wording automatically. Tested: banner appears only when configured, no tracker loads before consent or after decline.
- **Structured data:** validated against the full schema.org vocabulary (`tools/validate_jsonld.py`): 0 problems.
- **Tools:** `tools/audit_seo.py`, `audit_content.py`, `audit_assets.py`, `validate_jsonld.py`, `page_weight.py`, `build_sitemap.py`. Final run: 76 pages, 0 SEO issues, 0 content problems, 0 JSON-LD problems.

**Still open (physically blocked or needs a human):**
- **Live site:** production returned HTTP 403 (origin "openresty", behind Cloudflare) from this network, so no live crawl, redirect, 404-status or Cloudflare-robots check was possible. The Cloudflare-managed live robots.txt differs from the repo's and has no `Sitemap:` line; fix in Cloudflare.
- **Unverified in the browser:** the RU/TH/HE contact pages (their external OpenStreetMap iframe stalls the headless test; EN contact page passes); final re-run of the full sweep after the last CSS/font changes was stopped before finishing.
- **Real Core Web Vitals, real iOS/Android devices, Google Rich Results Test, deployment, Search Console:** need the live site/devices/accounts.
- **Native-speaker review** of all new TH/HE/RU text (written by AI sub-agents; terms flagged by them include plumbing/electrical/AC vocabulary, "handyman", place-name transliterations, rental terms).
- **Owner decisions:** claims already on EN pages that cannot be verified (warranty on all work, trained staff, licensed technicians, verified listings/no agency fees, "reply within 24 hours"); response-time-by-area tables that exist only in RU/TH/HE (kept, not in EN); privacy page has no legal-entity name/address; real photos for phone repair, flowers, electrician; exposed SSH details in commit `ee7435f`.
- **Process incident:** several sub-agents ran `git stash` concurrently; the tree was checked and repaired afterwards (duplicate FAQs removed, lost edits redone). Review `git diff` before merging.
