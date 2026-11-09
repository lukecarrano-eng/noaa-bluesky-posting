"""Turn the raw Bluesky JSON into one tidy table of posts.

Run from the repo root:  python clean_data.py
"""
import json
from pathlib import Path

import pandas as pd

RAW_DIR = Path("local_data/raw")
CLEAN_DIR = Path("local_data/clean")
START = pd.Timestamp("2026-01-01", tz="UTC")
TZ = "America/New_York"
ACCOUNTS = ["nws.noaa.gov", "climate.noaa.gov", "noaacomms.noaa.gov"]


def load_posts():
    rows = []
    n_reposts = 0
    for acct in ACCOUNTS:
        path = RAW_DIR / f"feed_{acct}.json"
        if not path.exists():
            print("no raw file for", acct)
            continue
        pages = json.loads(path.read_text())
        for page in pages:
            for item in page["feed"]:
                if "reason" in item:       # reposts and pinned posts
                    n_reposts += 1
                    continue
                post = item["post"]
                rec = post["record"]
                rows.append({
                    "uri": post["uri"],
                    "handle": post["author"]["handle"],
                    "created_at": rec.get("createdAt"),
                    "text": rec.get("text", ""),
                    "embed_type": rec.get("embed", {}).get("$type", "none"),
                    "likes": post.get("likeCount"),
                    "reposts": post.get("repostCount"),
                    "replies": post.get("replyCount"),
                    "quotes": post.get("quoteCount"),
                })
    return pd.DataFrame(rows), n_reposts


def clean(df):
    report = {"rows_loaded": len(df)}

    df = df.drop_duplicates(subset="uri")
    report["after_dropping_duplicates"] = len(df)

    df["created_at"] = pd.to_datetime(df["created_at"], format="ISO8601", errors="coerce", utc=True)
    df = df.dropna(subset=["created_at"])
    report["after_dropping_bad_dates"] = len(df)

    df = df[df["created_at"] >= START]
    report["after_date_filter"] = len(df)

    for col in ["likes", "reposts", "replies", "quotes"]:
        df[col] = df[col].fillna(0).astype(int)

    local = df["created_at"].dt.tz_convert(TZ)
    df["created_local"] = local.dt.strftime("%Y-%m-%d %H:%M:%S")
    df["month"] = local.dt.strftime("%Y-%m")
    df["weekday"] = local.dt.day_name()
    df["hour"] = local.dt.hour
    df["text_length"] = df["text"].str.len()
    df["has_media"] = df["embed_type"].isin(["app.bsky.embed.images", "app.bsky.embed.video"])
    df["embed_type"] = df["embed_type"].str.replace("app.bsky.embed.", "", regex=False)
    df["created_at"] = df["created_at"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    cols = ["uri", "handle", "created_at", "created_local", "month", "weekday", "hour",
            "text", "text_length", "embed_type", "has_media",
            "likes", "reposts", "replies", "quotes"]
    df = df[cols].sort_values(["handle", "created_at"]).reset_index(drop=True)
    return df, report


if __name__ == "__main__":
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    raw_df, n_skipped = load_posts()
    print("reposts/pinned skipped:", n_skipped)
    clean_df, report = clean(raw_df)
    for k, v in report.items():
        print(f"{k}: {v}")
    print()
    print(clean_df.groupby("handle").size().rename("posts").to_string())

    clean_df.to_csv(CLEAN_DIR / "posts_clean.csv", index=False)

    # small sample that goes in the repo: 10 posts per account, no raw JSON
    sample = clean_df.groupby("handle").head(10)
    sample.to_csv("data/sample_posts_clean.csv", index=False)
    print("\nsaved", len(clean_df), "rows to local_data/clean/posts_clean.csv and", len(sample), "to data/sample_posts_clean.csv")
