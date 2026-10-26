# Siteflare

SEO + AI-readiness audits. One Vercel project: a static frontend (`index.html`) and a Python API (`api/`).

```
index.html          frontend (no build step)
api/index.py        FastAPI app: POST /api/audit, GET /api/health
api/_audit.py       the audit engine (your original code, ported)
vercel.json         routes /api/* to the function, 120s timeout
requirements.txt
dev.py              local dev server
```

## Deploy to Vercel

1. Push this folder to a new GitHub repo.
2. In Vercel: **Add New → Project → import the repo**. Framework preset: **Other**. No build command needed.
3. Under **Settings → Environment Variables**, add:
   - `ACCESS_KEY`: any long random string. This stops strangers from using your deployment. The site asks for it once and remembers it in your browser.
   - `BROWSERLESS_TOKEN`: a free API key from browserless.io. This powers the "raw vs rendered" check (worth 10 points). Without it, that check shows as *skipped*.
4. Deploy, then redeploy after adding env vars.

CLI alternative: `npm i -g vercel && vercel` from this folder, then `vercel env add ACCESS_KEY` and `vercel env add BROWSERLESS_TOKEN`, then `vercel --prod`.

## Run locally

```
pip install -r requirements.txt uvicorn
python dev.py            # http://localhost:8000
```
Locally, if `playwright` is installed and no `BROWSERLESS_TOKEN` is set, the rendered check uses a local Chromium (`pip install playwright && playwright install chromium`).

## Changes from the original backend

- **Playwright → Browserless in production.** Vercel functions can't run Chromium, so the rendered page is fetched from Browserless's `/content` API.
- **Bug fix: bot UA table.** `result["bots"][bot_name] = bot_result` was indented inside the `except`, so only errors were recorded and the firewall check never saw a blocked bot. Bot requests now also run in parallel.
- **Bug fix: security strengths.** Every security header added "HSTS enabled". Each header now gets its own line.
- **Copyright year** is compared against the current year instead of a hardcoded 2026.
- **Sitemap fetch** follows redirects (`/sitemap.xml` → `/sitemap_index.xml` is common).
- Typo: "deteced" → "detected".

Score maxima: AI readiness 35, SEO 25, Performance 15, Content & social 15, Accessibility 10, Security & tracking 5 (capped at 100).
