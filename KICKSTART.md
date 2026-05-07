# Instagram-Autopilot — Setup-Kit für deinen eigenen Account

> Du baust dir einen Instagram-Account, der **täglich um 18:00 automatisch postet** — ohne dass du am Mac sein musst. Carousels + Reels werden via AI generiert (kie.ai), getextet, ge-branded und über GitHub Actions zur richtigen Zeit live gestellt. Setup ~3 Stunden, danach läuft's wochenlang allein.
>
> Dieses Doc ist die Grundlage. Lies Teil 1, fülle Teil 2 aus, kopier Teil 3 in Claude Code (oder Claude.ai mit File-Access). Claude führt dich durch den Rest.

---

## TEIL 1 — Was du bekommst

### Was die Pipeline macht
1. Du planst Content-Pillars + Hooks (28 Tage).
2. AI generiert Carousels (NanoBanana Pro Pro 2K-Bilder + Text-Overlay) und Reels (Seedance 2 Cinematic B-Roll + deutsche Stimme via macOS `say` + Untertitel via PIL + ffmpeg).
3. Assets landen als statische Files im GitHub-Repo.
4. `queue.jsonl` definiert: an welchem Datum wird welches Asset mit welcher Caption gepostet.
5. GitHub Actions Cron triggert täglich `scheduler.py`, der über die Meta Graph API postet — Reel oder Carousel je nach Eintrag.
6. Status wird zurück ins Repo committed.

### Tech-Stack (musst du nicht im Detail können — Claude führt dich durch)
- Python 3 + PIL (Pillow) + ffmpeg + macOS `say`
- Meta Graph API (Instagram + Facebook)
- GitHub Actions (kostenlose Cron-Jobs)
- kie.ai (NanoBanana Pro für Bilder, Seedance 2 für Reels)
- Google Fonts (Playfair Display, Inter — kostenlos)

### Kosten (alles, was du wirklich zahlst)
| Posten | Kosten |
|---|---|
| Instagram-Account | gratis |
| Facebook-Page | gratis |
| Meta Developer App | gratis |
| GitHub | gratis (privat oder public) |
| kie.ai für 4 Wochen Content | **~$15–25** (1 Reel/Woche + 22 Carousels) |
| ggf. ElevenLabs für bessere Stimme | gratis (10k Zeichen/Mo) bis $5/Mo |

**Gesamt:** ~$15–25 pro Monat für Volle-Pipeline-Content.

---

## TEIL 2 — Dein Brand-Briefing (vor dem Prompt ausfüllen)

Beantworte diese Fragen ehrlich. Je klarer das Briefing, desto besser läuft die Pipeline. Trag's direkt in den Claude-Prompt unten ein.

### A) Account-Basics
- **IG-Handle (gewünscht):** `@_______`
- **FB-Page-Name:** `_______`
- **E-Mail für Meta Developer App:** `_______@_______`

### B) Audience & Niche
- **Niche / Thema:** (z.B. "Mindset für deutschsprachige Männer", "Heritage-Streetwear", "Stoizismus-Quotes")
- **Zielgruppe:** Alter, Geschlecht, Land, Lebensphase
- **Was diese Audience nachts wachhält:** 1–3 Pain Points
- **Was sie geheim wünscht:** 1–3 Desires

### C) Brand-Stimme
- **Tonalität:** (z.B. "konfrontativ-stoisch, ruhige Härte" / "warm-cinematic-poetic" / "lustig-sarkastisch-Boomer-spöttisch")
- **Anrede:** du / Sie / niemanden (Aphorisma-Stil)
- **Sprache primär:** Deutsch / Englisch / Mix

### D) Content-Pillars (6 Stück, je 10–25% Volumen)
Pillar = wiederkehrendes Thema mit eigenem emotionalem Trigger. Beispiel aus dem Referenz-Brand:
1. *Die Montagslüge* (Hard-Truth-Konfrontation)
2. *Komfort tötet* (Discipline-as-Religion)
3. *Verschwendetes Potenzial* (Mortality-Reframe)
4. *Vater-Sohn* (Generational-Identity)
5. *Quiet Power* (Stoiker-Aesthetic)
6. *Frame Shifts* (Mental Models)

**Deine 6:**
1. _______
2. _______
3. _______
4. _______
5. _______
6. _______

### E) Visueller Stil
- **Stimmung:** (z.B. "monochrom dunkelblau-grau, ein einziger warmer Highlight, melancholisch, slow-motion B-Roll" / "Bauhaus-clean, Primärfarben, Editorial" / "Pastell, weich, Sommer")
- **Was niemals gezeigt wird:** (z.B. "keine Personen / Gesichter, keine Logos außer eigenes Wasserzeichen, keine Sättigung > 30%")
- **Motiv-Bibliothek (5–10 wiederkehrende Settings):**

### F) Typografie & Fonts
- **Headline-Font:** (z.B. Playfair Display Black / Cormorant Garamond / Inter)
- **CTA-Font:** (z.B. Inter Bold / Space Grotesk)
- **Brand-Mark unten rechts:** `@yourhandle` in welchem Font?

### G) Posting-Setup
- **Cadence:** 1 / 2 / 3 Posts pro Tag
- **Tageszeit:** Default 18:00 MEZ (= 16:00 UTC). Anders gewünscht?
- **Format-Mix:** z.B. 80% Carousel + 20% Reel? Reine Reels? Nur Carousels?

### H) Konten, die du brauchst
- [ ] Instagram-Account (Business oder Creator)
- [ ] Facebook-Account (für Page-Erstellung)
- [ ] GitHub-Account
- [ ] kie.ai-Account mit Guthaben (~$20)
- [ ] macOS-Laptop mit Homebrew, Python 3 (ffmpeg installiert Claude)

---

## TEIL 3 — Der Claude-Prompt (Copy-Paste)

> Kopier den gesamten Block unten in eine neue Claude-Code- oder Claude.ai-Session. Erst die Platzhalter `<...>` mit deinen Antworten aus Teil 2 ersetzen.

```
Hi Claude. Ich will einen vollautomatischen Instagram-Content-Account
aufbauen — täglich um 18:00 MEZ automatisch posten, Pipeline läuft komplett
in der Cloud, ich muss nicht am Mac sein.

## Architektur (Referenz)
Bau alles analog zu diesem Repo: https://github.com/darioprenzyna17-cmd/montagsluege-autopilot

Komponenten:
- `scheduler.py` (Tagesläufer, idempotent — postet einen Eintrag pro Tag)
- `lib_meta.py` (Instagram Graph API: Reel + Carousel)
- `.github/workflows/post-daily.yml` (Cron 16:00 UTC)
- `gen_carousel.py` (NanoBanana Pro 2K Bilder + PIL Text-Overlay)
- `gen_reel_v2.py` (Seedance B-Roll + macOS `say` + PIL Subs + ffmpeg overlay)
- `rerender_carousel.py` (gratis Re-Overlay nach Brand-Änderung)
- `BRAND.md` (Locked Style Guide)
- `queue.jsonl` (Datum → Format → Asset-URLs → Caption)
- `assets/carousels/<slug>/slide-N.png` (gerenderte Slides + slide-N-base.png als textfreie Originale)
- `assets/reels/<slug>/reel.mp4` (final composited)
- `assets/fonts/` (Playfair + Inter als TTF — werden bei Generierung referenziert, nicht von System geladen)

## Mein Account-Setup
- Gewünschter IG-Handle: <@meinhandle>
- FB-Page-Name: <Mein Brand>
- E-Mail Meta Developer: <meine@mail>

## Mein Brand-Briefing
- Niche: <was machst du>
- Zielgruppe: <wer schaut zu>
- Pain Points: <1–3>
- Desires: <1–3>
- Tonalität: <wie klingst du>
- Anrede: <du / Sie>
- Sprache: <Deutsch / Englisch / Mix>

## Meine 6 Content-Pillars
1. <Pillar 1 Name + 1-Satz-Erklärung>
2. <Pillar 2>
3. <Pillar 3>
4. <Pillar 4>
5. <Pillar 5>
6. <Pillar 6>

## Mein visueller Stil
- Stimmung: <z.B. monochrom dunkelblau-grau, melancholisch, slow-motion>
- Was nie gezeigt wird: <Personen / Logos / etc.>
- Motiv-Bibliothek: <5–10 wiederkehrende Settings>

## Meine Brand-Fonts
- Headlines: <Font-Name>
- CTAs: <Font-Name>
- Brand-Mark: <@handle> in welchem Font

## Posting-Setup
- Cadence: <1 / 2 / 3 Posts/Tag>
- Default-Uhrzeit: <18:00 MEZ oder anders>
- Format-Mix: <z.B. 22 Carousels + 6 Reels in 28 Tagen>

## Was ich schon habe
- macOS mit Homebrew, Python 3
- (ffmpeg installierst du via brew falls fehlt)
- Tokens / API-Keys reiche ich nach, wenn du fragst:
  - Meta App-ID + Secret
  - Meta Page-Access-Token (Long-Lived)
  - GitHub PAT
  - kie.ai API-Key

## Mein Budget
- $<Betrag> für Monat 1 (~$15–25 Empfehlung für 4 Wochen Content)

## Wie du arbeiten sollst
1. **Setup-Phase:** Walk mich step-by-step durch:
   a) Instagram → Business/Creator umstellen
   b) Facebook-Page erstellen + IG verknüpfen (über Meta Business Suite)
   c) Meta Developer App erstellen ("Andere" → "Business" → Use Case "Messaging und Content auf Instagram verwalten" → API-Einrichtung mit FACEBOOK-Login, NICHT Instagram-Login)
   d) Permissions konfigurieren (instagram_basic, instagram_content_publish, instagram_manage_insights, pages_show_list, pages_read_engagement, business_management)
   e) Long-Lived Token via Graph API Explorer generieren → mit App-Secret tauschen → Page-Access-Token ableiten
   f) GitHub-Repo erstellen, Secrets setzen, alles pushen

2. **Brand-Lock-Phase:** Schreibe `BRAND.md` mit meinem Briefing → Fonts via GitHub raw runterladen.

3. **Test-Phase:** Generiere **1 Carousel + 1 Reel** als Style-Test (Cost ~$2). Ich review, du iterierst, bis Vibe sitzt.

4. **Batch-Phase:** Generiere Woche 1 (5–7 Assets) → push ins Repo → Queue für 7 Tage.

5. **Live-Phase:** Trigger Workflow manuell für ersten Post → verifiziere → ab da läuft Cron.

6. **Iteration:** Pro Woche Insights ziehen (`fetch_insights.py`), Pillars mit ø Reach < 500 nach 5 Posts killen.

## Wie du sprichst
- Direkt, ehrlich. Kein Coaching-Sprech.
- Eine Frage nach der anderen — wirklich antworten lassen.
- Wenn meine Brand-Decisions unklug sind → benenne es. Einmal sagen, dann
  ausführen wie verlangt.
- Vor jedem $-Output: Cost-Estimate auf den Tisch.
- Faceless ist okay (AI-Avatar oder Text-on-B-Roll), aber: Mentor-Verkauf
  braucht Gesicht. Wenn ich Mentoring/High-Ticket plane, push back.

## Wichtige Fallstricke (kenn die vorher)
1. **Meta Page-Token läuft nach 60 Tagen ab** — wir brauchen Reminder oder
   Renewal-Routine. Wenn der Token tot ist, postet die Pipeline NICHTS und
   gibt HTTP 400 "Session has been invalidated".
2. **kie.ai Credits können mitten im Batch ausgehen** — vor jedem Batch
   Balance prüfen.
3. **Homebrew ffmpeg hat oft kein drawtext** (libfreetype fehlt) — deshalb
   nutzen wir overlay-Filter mit PIL-gerenderten PNGs statt drawtext.
4. **Repo muss public sein** — sonst können IG Graph API die raw.githubusercontent
   URLs nicht fetchen (Token-Auth funktioniert nicht für Graph API media-Calls).
5. **JSON-Captions brauchen Unicode-Quotes** (U+201E + U+201C oder einfache '),
   sonst zerschießen ASCII " die queue.jsonl.

## Erster Schritt
Lass uns bei (1a) anfangen — schreib mir was ich auf dem Handy in der IG-App
klicken muss, damit der Account auf Creator/Business umgestellt ist. Geh dann
weiter zu (1b).

Wenn ich an einer Stelle hänge oder unsicher bin, frag nach. Wenn du Cost
ausgibst (kie.ai), zeig vorher die Schätzung. Don't guess my budget.
```

---

## TEIL 4 — Häufige Stolpersteine (für deinen Kumpel)

### "Mein Token ist nach ein paar Tagen tot"
Facebook invalidiert Page-Tokens manchmal aus "Sicherheitsgründen". Lösung: bei jedem 60-Tage-Wechsel UND nach FB-Passwort-Change neuen Token via Graph API Explorer ziehen, GitHub Secret aktualisieren, lokale `.env` aktualisieren.

### "kie.ai sagt mitten im Batch: Credits insufficient"
Vor jedem Batch das Balance-Endpoint pingen:
```bash
curl -H "Authorization: Bearer $KIE_KEY" https://api.kie.ai/api/v1/chat/credit
```
Pro Carousel: ~$0.20–0.40. Pro Reel: ~$1.20–1.80. Plane mit 30% Puffer.

### "ffmpeg drawtext-Filter not found"
Homebrew baut ffmpeg ohne libfreetype. Lösung: PIL-PNGs als Overlay-Bilder rendern, dann via `overlay`-Filter compositen. Code-Vorlage in `gen_reel_v2.py` des Referenz-Repos.

### "IG Graph API gibt HTTP 400 beim Carousel-Post"
Häufige Ursachen:
- Token tot (siehe oben) — Fehlermeldung enthält dann "Session has been invalidated"
- Bild-URL nicht öffentlich erreichbar (Repo privat?) — Repo public stellen
- Bild > 8MB oder falsches Aspect-Ratio (1.91:1 bis 4:5)

### "Reels haben fake-klingende deutsche Stimme"
Seedance 2 ist primär EN/CN trainiert. Für Deutsch: macOS `say` (Stimme: `Reed`, `Eddy` oder `Rocko`) als Fallback. Output via ffmpeg auf stummes B-Roll mixen + PIL-Untertitel. Voll-Pipeline in `gen_reel_v2.py`.

### "Mein erster Post ist mein Test-Post"
Bevor Cron erstmals fired: in IG-App den Test-Post löschen. ODER ersten Post manuell triggern und nicht über Test-Caption "Test." schicken.

---

## TEIL 5 — Was du nach 30 Tagen erreichen kannst (realistisch)

| Effort | Reach in 30 Tagen | Kosten |
|---|---|---|
| 1 Carousel/Tag | 1–5k Follower (faceless mindset Niche) | ~$15 |
| 1 Carousel + 1 Reel/Wo | 3–10k | ~$25 |
| 2 Posts/Tag, davon 1 Reel/3-Tage | 5–15k bei 1 Viral-Hit | ~$50 |

**Voraussetzung Viralität:** ≥1 Reel mit 100k+ Views. Hängt vom Hook ab — nicht von Volumen allein.

---

## TEIL 6 — Was du NICHT von Claude erwarten solltest

- Claude kann **deinen IG-Profilbild nicht setzen** — das musst du im Handy machen.
- Claude kann **Test-Posts nicht via API löschen** (Meta erlaubt's nicht) — manuell in IG-App.
- Claude kann **kie.ai nicht für dich aufladen** — eigene Karte hinterlegen.
- Claude kann **keine FB-Passwort-Resets handeln** — bei Token-Invalidation hilft nur neu generieren.

---

**Viel Spaß. Wenn dein Kumpel hängt — Repo ist public, der Code ist die Doku. Bei Fragen: zeig ihm `STATUS.md` für die End-to-End-Sicht und `BRAND.md` als Style-Lock-Beispiel.**
