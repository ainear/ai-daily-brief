"""Configuration for AI Daily Brief Generator."""

import os

# RSS Feed URLs - Multiple sources (verified working feeds)
RSS_FEED_URLS = [
    # AI News - TechCrunch
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://techcrunch.com/category/apps/feed/",

    # AI News - VentureBeat
    "https://venturebeat.com/category/ai/feed/",

    # MIT Tech Review
    "https://www.technologyreview.com/topic/artificial-intelligence/feed/",

    # Hacker News
    "https://news.ycombinator.com/rss",

    # Dev.to - Programming community
    "https://dev.to/feed",

    # Google AI Blog
    "https://blog.google/technology/ai/rss",

    # OpenAI Blog
    "https://openai.com/blog/rss.xml",

    # Meta AI
    "https://ai.meta.com/feed/",

    # Microsoft AI
    "https://blogs.microsoft.com/ai/feed/",

    # Flutter
    "https://medium.com/feed/flutter",

    # Product Hunt
    "https://www.producthunt.com/feed.atom",
]

# Keywords to filter articles - Expanded (more flexible)
KEYWORDS = [
    # AI Core
    "ai", "artificial intelligence", "machine learning",
    "agent", "agentic", "automation",
    "llm", "gpt", "openai", "gemini", "claude", "deepseek", "minimax", "glm",

    # AI Products & Tools
    "mcp", "cursor", "windsurf", "vibe", "figma",
    "opencode", "claude code", "devin",

    # Mobile
    "flutter", "dart", "swift", "kotlin", "react native", "mobile",

    # Frontend
    "react", "vue", "svelte", "typescript", "javascript", "frontend", "next.js", "nuxt",

    # Backend
    "backend", "api", "rest", "graphql", "database",

    # Startup & Funding
    "startup", "funding", "venture", "vc", "series a", "series b",
    "acquisition", "launch", "announcement",

    # Companies
    "google", "microsoft", "apple", "amazon", "meta", "nvidia",
    "anthropic", "xai", "mistral",
]

# Limits
MAX_ARTICLES = 30
HOURS_BACK = 24  # 24 hours

# API Configuration - Gemini default, OpenAI fallback
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o"

# Output directory
REPORTS_DIR = "reports"
