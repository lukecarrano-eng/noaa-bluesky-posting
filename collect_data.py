"""Collect public posts from NOAA's Bluesky accounts and save the raw JSON.

Needs no key. Run from the repo root:  python collect_data.py
"""
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests


HEADERS = {"User-Agent": "WebDataScience/1.0 (luca2147@colorado.edu)"}
BASE = "https://public.api.bsky.app/xrpc"
ACCOUNTS = ["nws.noaa.gov", "climate.noaa.gov", "noaacomms.noaa.gov"]
CUTOFF = "2026-01-01T00:00:00Z"   # stop paging once posts are older than this
PAUSE = 1.0                        # seconds between requests
RAW_DIR = Path("local_data/raw")


def get(endpoint, params):
    r = requests.get(f"{BASE}/{endpoint}", params=params, headers=HEADERS, timeout=30)
    r.raise_for_status()
    time.sleep(PAUSE)
    return r.json()


def collect_profiles():
    data = get("app.bsky.actor.getProfiles", {"actors": ACCOUNTS})
    (RAW_DIR / "profiles.json").write_text(json.dumps(data, indent=1))
    print("saved profiles for", len(data["profiles"]), "accounts")


def collect_feed(actor):
    pages = []
    cursor = None
    while True:
        params = {"actor": actor, "limit": 100, "filter": "posts_no_replies"}
        if cursor:
            params["cursor"] = cursor
        page = get("app.bsky.feed.getAuthorFeed", params)
        pages.append(page)

        times = [i["post"]["record"]["createdAt"] for i in page["feed"] if "reason" not in i]
        cursor = page.get("cursor")
        if not cursor or (times and min(times) < CUTOFF):
            break
    (RAW_DIR / f"feed_{actor}.json").write_text(json.dumps(pages))
    print(actor, ":", len(pages), "pages saved")


if __name__ == "__main__":
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    collected_at = datetime.now(timezone.utc).isoformat()
    (RAW_DIR / "collected_at.txt").write_text(collected_at)
    print("collection started", collected_at)
    collect_profiles()
    for acct in ACCOUNTS:
        try:
            collect_feed(acct)
        except requests.HTTPError as e:
            print("skipped", acct, ":", e)
    print("done")
