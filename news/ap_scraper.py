#!/usr/bin/env python3
"""
AP (Associated Press) headline scraper using NewsAPI.org.

Usage:
    ./ap_scraper.py --api-key 284f7bbe0bde404cbc7469115a9d40ba
    ./ap_scraper.py  # reads NEWSAPI_KEY env var

Get a free key at https://newsapi.org/register (100 req/day free tier).
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

import requests

OUTPUT_FILE = "ap_news_headlines.json"
NEWSAPI_BASE = "https://newsapi.org/v2"
SOURCE_ID = "associated-press"
SOURCE_NAME = "Associated Press"


def fetch_top(api_key: str, page_size: int = 30) -> list[dict]:
    """Fetch top AP headlines from NewsAPI /top-headlines."""
    url = f"{NEWSAPI_BASE}/top-headlines"
    params = {
        "sources": SOURCE_ID,
        "pageSize": page_size,
        "apiKey": api_key,
    }
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    if data.get("status") != "ok":
        print(f"[error] NewsAPI returned: {data.get('message', data)}", file=sys.stderr)
        sys.exit(1)

    articles = data.get("articles", [])
    print(f"Fetched {len(articles)} {SOURCE_NAME} articles from /top-headlines.")
    return articles


def fetch_everything(api_key: str, page_size: int = 30) -> list[dict]:
    """Fallback: /everything endpoint filtered to AP domain."""
    url = f"{NEWSAPI_BASE}/everything"
    params = {
        "domains": "apnews.com",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": api_key,
    }
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    if data.get("status") != "ok":
        print(f"[error] NewsAPI returned: {data.get('message', data)}", file=sys.stderr)
        sys.exit(1)

    articles = data.get("articles", [])
    print(f"Fetched {len(articles)} {SOURCE_NAME} articles via /everything.")
    return articles


def normalize(article: dict) -> dict:
    """Clean and normalize a raw NewsAPI article into a tidy record."""
    title = (article.get("title") or "").strip()
    for suffix in (" - Reuters", " | Reuters", " - AP", " | AP", " - Associated Press"):
        if title.endswith(suffix):
            title = title[: -len(suffix)].strip()

    content = (article.get("content") or "").strip()
    content = re.sub(r"\s*\[\+\d+ chars\]$", "", content).strip()

    synopsis = (article.get("description") or "").strip() or content or ""

    return {
        "title": title,
        "synopsis": synopsis,
        "url": (article.get("url") or "").strip(),
        "published": (article.get("publishedAt") or "").replace("T", " ").replace("Z", " UTC"),
        "source": SOURCE_NAME,
    }


def save_json(articles: list[dict], output_path: str) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    payload = {
        "scraped": now,
        "source": SOURCE_NAME,
        "count": len(articles),
        "articles": [normalize(a) for a in articles],
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(articles)} articles to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=f"Scrape {SOURCE_NAME} headlines via NewsAPI.")
    parser.add_argument(
        "--api-key",
        default=os.environ.get("NEWSAPI_KEY", ""),
        help="NewsAPI key (or set NEWSAPI_KEY env var)",
    )
    parser.add_argument(
        "--output",
        default=OUTPUT_FILE,
        help=f"Output JSON file (default: {OUTPUT_FILE})",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=30,
        help="Number of articles to fetch (max 100 on free tier, default 30)",
    )
    parser.add_argument(
        "--everything",
        action="store_true",
        help="Use /everything endpoint instead of /top-headlines",
    )
    args = parser.parse_args()

    if not args.api_key:
        print(
            "Error: NewsAPI key required.\n"
            "  Set NEWSAPI_KEY env var or pass --api-key YOUR_KEY\n"
            "  Get a free key at https://newsapi.org/register",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Fetching up to {args.limit} {SOURCE_NAME} headlines from NewsAPI …")

    if args.everything:
        articles = fetch_everything(args.api_key, page_size=min(args.limit, 100))
    else:
        articles = fetch_top(args.api_key, page_size=min(args.limit, 100))
        if len(articles) < args.limit:
            print(f"Only {len(articles)} from /top-headlines, topping up with /everything …")
            extra = fetch_everything(
                args.api_key, page_size=min(args.limit - len(articles), 100)
            )
            seen_urls = {a["url"] for a in articles}
            for a in extra:
                if a["url"] not in seen_urls:
                    articles.append(a)
                    seen_urls.add(a["url"])
            articles = articles[: args.limit]

    save_json(articles, args.output)


if __name__ == "__main__":
    main()
