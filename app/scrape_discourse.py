#!/usr/bin/env python3
# app/scrape_discourse_requests.py

import os
import json
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

# ─── Configuration ─────────────────────────────────────────────────────────────
BASE_URL     = "https://discourse.onlinedegree.iitm.ac.in"
SEARCH_URL   = f"{BASE_URL}/search.json"
CATEGORY_ID  = "34"
COOKIE       = os.getenv("DISCOURSE_COOKIE", "")
HEADERS      = {
    "User-Agent": "Mozilla/5.0",
    "Cookie":      COOKIE
}
START_DATE   = datetime(2025, 1,  1, tzinfo=timezone.utc)
END_DATE     = datetime(2025, 4, 14, tzinfo=timezone.utc)
OUTPUT_FILE  = "app/data/discourse_posts.json"
# ────────────────────────────────────────────────────────────────────────────────

def fetch_topics_via_search():
    """
    Page through search.json to get every topic in the category
    created in our date window.
    """
    topics = []
    page   = 0
    # build the Discourse search query
    q = (
        f"category:{CATEGORY_ID} "
        f"after:{START_DATE.strftime('%Y-%m-%d')} "
        f"before:{END_DATE.strftime('%Y-%m-%d')}"
    )

    while True:
        resp = requests.get(
            SEARCH_URL,
            headers=HEADERS,
            params={"q": q, "page": page}
        )
        resp.raise_for_status()
        data  = resp.json()
        batch = data.get("topics") or data.get("topic_list", {}).get("topics", [])
        if not batch:
            break

        for t in batch:
            topics.append({
                "id":    str(t["id"]),
                "slug":  t["slug"],
                "title": t["title"]
            })

        page += 1

    return topics

def fetch_posts_for_topic(slug, tid):
    """
    Given a topic slug and ID, fetch its JSON and extract all posts.
    """
    url  = f"{BASE_URL}/t/{slug}/{tid}.json"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()

    posts = []
    for p in data.get("post_stream", {}).get("posts", []):
        posts.append({
            "post_number": p["post_number"],
            "username":    p["username"],
            "html":        p["cooked"]
        })

    return {
        "topic_id": int(tid),
        "slug":      slug,
        "title":     data.get("title", ""),
        "url":       f"{BASE_URL}/t/{slug}/{tid}",
        "posts":     posts
    }

def main():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    print("➤ Searching for topics…")
    topics = fetch_topics_via_search()
    print(f"  • Found {len(topics)} topics between {START_DATE.date()} and {END_DATE.date()}")

    export = []
    for t in topics:
        print(f"  ↳ #{t['id']} {t['title']}")
        export.append(fetch_posts_for_topic(t["slug"], t["id"]))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(export, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(export)} topics to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
