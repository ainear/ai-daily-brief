"""RSS Fetcher Module - Fetch and filter articles from RSS feeds."""

import feedparser
from datetime import datetime, timedelta
from dateutil import parser as date_parser
from typing import List, Dict, Optional

from config import RSS_FEED_URLS, KEYWORDS, MAX_ARTICLES, HOURS_BACK


def is_recent(published_date: str, hours_back: int = HOURS_BACK) -> bool:
    """Check if article was published within the last N hours."""
    try:
        parsed_date = date_parser.parse(published_date)
        cutoff = datetime.now(parsed_date.tzinfo) - timedelta(hours=hours_back)
        return parsed_date >= cutoff
    except Exception:
        return False


def matches_keywords(title: str, keywords: List[str]) -> bool:
    """Check if title contains any of the keywords (case-insensitive)."""
    title_lower = title.lower()
    return any(keyword.lower() in title_lower for keyword in keywords)


def fetch_feed(url: str) -> List[Dict]:
    """Fetch and parse a single RSS feed."""
    try:
        feed = feedparser.parse(url)
        articles = []

        for entry in feed.entries:
            title = entry.get("title", "")
            link = entry.get("link", "")
            published = entry.get("published", entry.get("updated", ""))

            if not title or not link:
                continue

            if matches_keywords(title, KEYWORDS) and is_recent(published):
                articles.append({
                    "title": title,
                    "url": link,
                    "published_date": published
                })

        return articles
    except Exception as e:
        print(f"Error fetching feed {url}: {e}")
        return []


def fetch_all_articles() -> List[Dict]:
    """Fetch articles from all RSS feeds, filter by date and keywords."""
    all_articles = []

    for url in RSS_FEED_URLS:
        articles = fetch_feed(url)
        all_articles.extend(articles)

    # Remove duplicates based on URL
    seen_urls = set()
    unique_articles = []
    for article in all_articles:
        if article["url"] not in seen_urls:
            seen_urls.add(article["url"])
            unique_articles.append(article)

    # Sort by published date (most recent first)
    unique_articles.sort(
        key=lambda x: date_parser.parse(x["published_date"]),
        reverse=True
    )

    # Limit to MAX_ARTICLES
    return unique_articles[:MAX_ARTICLES]


if __name__ == "__main__":
    articles = fetch_all_articles()
    print(f"Found {len(articles)} articles")
    for a in articles:
        print(f"  - {a['title']}")
