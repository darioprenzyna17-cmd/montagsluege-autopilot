# montagsluege-autopilot

Auto-Posting-Pipeline für Instagram `@montagsluege`.

## Wie es funktioniert

GitHub Actions triggert täglich um **18:00 MEZ** (`scheduler.py`).
Der Scheduler:
1. Prüft, ob heute schon gepostet wurde → ja: skip
2. Sucht in `queue.jsonl` den Eintrag mit `date == heute, status == pending`
3. Postet je nach `format` ein Reel oder Carousel via Instagram Graph API
4. Markiert den Eintrag als `posted` (oder `failed` mit Error)
5. Committed `queue.jsonl` zurück ins Repo

## Queue-Format

`queue.jsonl` — eine Zeile pro Tag, JSON-Object:

```json
{"date": "2026-05-03", "format": "carousel", "pillar": "montagsluege", "image_urls": ["https://...slide1.png", "https://...slide2.png"], "caption": "Hook + Tiefe + CTA", "status": "pending"}
{"date": "2026-05-04", "format": "reel", "pillar": "vater-sohn", "video_url": "https://...reel.mp4", "caption": "...", "status": "pending"}
```

## Secrets

Im Repo unter `Settings → Secrets and variables → Actions`:

- `META_IG_BUSINESS_ACCOUNT_ID` — Instagram Business Account ID
- `META_PAGE_ACCESS_TOKEN` — Page Access Token (Long-Lived)

## Manuell triggern

Bei `Actions → Daily Post → Run workflow` kannst du den Scheduler sofort
laufen lassen — z.B. zum Testen oder wenn der Cron einen Tag verpasst hat.

## Lokal testen

```bash
export META_IG_BUSINESS_ACCOUNT_ID=...
export META_PAGE_ACCESS_TOKEN=...
python3 scheduler.py
```
