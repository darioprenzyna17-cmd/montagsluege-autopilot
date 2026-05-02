"""
Tagesläufer für @montagsluege.

Wird einmal pro Tag von GitHub Actions aufgerufen. Liest queue.jsonl, sucht
heute's Eintrag, postet ihn, markiert ihn als posted, schreibt queue zurück.

Idempotent: prüft erst, ob heute schon gepostet wurde, bevor irgendwas läuft.
"""
import json
import sys
from datetime import date, datetime
from pathlib import Path

from lib_meta import post_reel, post_carousel, media_posted_today

QUEUE = Path(__file__).parent / "queue.jsonl"


def load_queue():
    if not QUEUE.exists():
        return []
    return [json.loads(line) for line in QUEUE.read_text().splitlines() if line.strip()]


def save_queue(entries):
    QUEUE.write_text("\n".join(json.dumps(e, ensure_ascii=False) for e in entries) + "\n")


def find_today(entries):
    today = date.today().isoformat()
    for e in entries:
        if e.get("date") == today and e.get("status", "pending") == "pending":
            return e
    return None


def main():
    print(f"=== Scheduler läuft: {datetime.now().isoformat(timespec='seconds')} ===")

    if media_posted_today():
        print("⏭  Heute wurde bereits gepostet — skip.")
        return 0

    entries = load_queue()
    today_entry = find_today(entries)
    if not today_entry:
        print(f"⏭  Kein pending Eintrag für {date.today().isoformat()} in queue.jsonl.")
        return 0

    print(f"📅 Heute: {today_entry.get('format')} | Pillar: {today_entry.get('pillar')}")
    fmt = today_entry["format"]
    caption = today_entry["caption"]

    try:
        if fmt == "reel":
            media_id, link = post_reel(today_entry["video_url"], caption)
        elif fmt == "carousel":
            media_id, link = post_carousel(today_entry["image_urls"], caption)
        else:
            raise ValueError(f"Unbekanntes Format: {fmt}")

        today_entry["status"] = "posted"
        today_entry["posted_at"] = datetime.now().isoformat(timespec="seconds")
        today_entry["media_id"] = media_id
        today_entry["permalink"] = link
        save_queue(entries)
        print(f"\n✅ LIVE: {link}")
        return 0

    except Exception as e:
        today_entry["status"] = "failed"
        today_entry["error"] = str(e)
        save_queue(entries)
        print(f"\n❌ Fehler: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
