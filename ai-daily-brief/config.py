"""Configuration for AI Daily Brief Generator."""

import os

# RSS Feed URLs
RSS_FEED_URLS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
    "https://www.ycombinator.com/blog/rss"
]

# Keywords to filter articles
KEYWORDS = ["ai", "agent", "automation", "llm", "startup", "funding", "model"]

# Limits
MAX_ARTICLES = 15
HOURS_BACK = 24

# API Configuration - Gemini default, OpenAI fallback
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o"

# Output directory
REPORTS_DIR = "reports"
