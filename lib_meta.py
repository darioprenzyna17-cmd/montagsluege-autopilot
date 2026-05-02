"""Helpers für Instagram Graph API — Posting + Status-Polling."""
import json
import os
import time
import urllib.parse
import urllib.request

GRAPH = "https://graph.facebook.com/v21.0"


def env(name):
    val = os.environ.get(name)
    if not val:
        raise RuntimeError(f"Missing env var: {name}")
    return val


def post_form(url, body):
    req = urllib.request.Request(
        url,
        data=urllib.parse.urlencode(body).encode("utf-8"),
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def get_json(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def wait_for_finished(container_id, token, timeout_min=10):
    """Pollt bis status_code == FINISHED. Wirft RuntimeError bei ERROR."""
    deadline = time.time() + timeout_min * 60
    last = None
    while time.time() < deadline:
        st = get_json(
            f"{GRAPH}/{container_id}?fields=status_code,status&access_token={token}"
        )
        code = st.get("status_code")
        if code != last:
            print(f"  [container {container_id}] {code} — {st.get('status', '')}")
            last = code
        if code == "FINISHED":
            return True
        if code == "ERROR":
            raise RuntimeError(f"Verarbeitung fehlgeschlagen: {st}")
        time.sleep(8)
    raise TimeoutError(f"container {container_id} nicht fertig nach {timeout_min}min")


def post_reel(video_url, caption):
    """Postet ein Reel via öffentlich zugängliche Video-URL."""
    ig_id = env("META_IG_BUSINESS_ACCOUNT_ID")
    token = env("META_PAGE_ACCESS_TOKEN")

    print(f"  → Reel-Container erstellen …")
    create = post_form(
        f"{GRAPH}/{ig_id}/media",
        {
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "access_token": token,
        },
    )
    cid = create.get("id")
    if not cid:
        raise RuntimeError(f"create failed: {create}")
    print(f"  ← container_id: {cid}")

    wait_for_finished(cid, token)

    print(f"  → Veröffentlichen …")
    pub = post_form(
        f"{GRAPH}/{ig_id}/media_publish",
        {"creation_id": cid, "access_token": token},
    )
    media_id = pub.get("id")
    if not media_id:
        raise RuntimeError(f"publish failed: {pub}")

    info = get_json(f"{GRAPH}/{media_id}?fields=permalink&access_token={token}")
    return media_id, info.get("permalink")


def post_carousel(image_urls, caption):
    """Postet ein Carousel mit 2–10 Bildern."""
    if not (2 <= len(image_urls) <= 10):
        raise ValueError(f"Carousel braucht 2–10 Bilder, hat {len(image_urls)}")

    ig_id = env("META_IG_BUSINESS_ACCOUNT_ID")
    token = env("META_PAGE_ACCESS_TOKEN")

    print(f"  → {len(image_urls)} Child-Container erstellen …")
    children = []
    for i, url in enumerate(image_urls, 1):
        c = post_form(
            f"{GRAPH}/{ig_id}/media",
            {
                "image_url": url,
                "is_carousel_item": "true",
                "access_token": token,
            },
        )
        cid = c.get("id")
        if not cid:
            raise RuntimeError(f"child {i} failed: {c}")
        children.append(cid)
        print(f"    [{i}/{len(image_urls)}] {cid}")

    print(f"  → Carousel-Container erstellen …")
    parent = post_form(
        f"{GRAPH}/{ig_id}/media",
        {
            "media_type": "CAROUSEL",
            "children": ",".join(children),
            "caption": caption,
            "access_token": token,
        },
    )
    pid = parent.get("id")
    if not pid:
        raise RuntimeError(f"parent failed: {parent}")
    print(f"  ← parent: {pid}")

    wait_for_finished(pid, token, timeout_min=3)

    print(f"  → Veröffentlichen …")
    pub = post_form(
        f"{GRAPH}/{ig_id}/media_publish",
        {"creation_id": pid, "access_token": token},
    )
    media_id = pub.get("id")
    if not media_id:
        raise RuntimeError(f"publish failed: {pub}")

    info = get_json(f"{GRAPH}/{media_id}?fields=permalink&access_token={token}")
    return media_id, info.get("permalink")


def media_posted_today():
    """True wenn @montagsluege heute schon gepostet hat (Idempotenz)."""
    from datetime import datetime, timezone
    ig_id = env("META_IG_BUSINESS_ACCOUNT_ID")
    token = env("META_PAGE_ACCESS_TOKEN")
    feed = get_json(
        f"{GRAPH}/{ig_id}/media?fields=timestamp&limit=5&access_token={token}"
    )
    today = datetime.now(timezone.utc).date()
    for item in feed.get("data", []):
        ts = item.get("timestamp", "")
        try:
            d = datetime.fromisoformat(ts.replace("Z", "+00:00")).date()
            if d == today:
                return True
        except Exception:
            continue
    return False
