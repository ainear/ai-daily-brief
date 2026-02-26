"""Configuration for AI Daily Brief Generator."""

import os

# RSS Feed URLs - Multiple sources
RSS_FEED_URLS = [
    # AI News
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
    "https://www.ycombinator.com/blog/rss",

    # Tech Giants
    "https://feeds.feedburner.com/blogspot/tNnQi",  # Google AI Blog
    "https://openai.com/blog/rss.xml",
    "https://ai.meta.com/feed/",

    # Programming & Dev
    "https://dev.to/feed",
    "https://stackoverflow.blog/feed/",
    "https://css-tricks.com/feed/",

    # Mobile & Frontend
    "https://flutter.dev/blog/feed.atom",
    "https://medium.com/feed/dartlang",
    "https://syntax.fm/rss",
    "https://podcast.jsjiejie.com/",

    # Vietnamese Tech
    "https://techcrunch.com/feed/",
]

# Keywords to filter articles - Expanded
KEYWORDS = [
    # AI Core
    "ai", "artificial intelligence", "machine learning", "ml",
    "agent", "agentic", "agents", "automation", "llm", "llms",
    "gpt", "openai", "gemini", "claude", "deepseek", "minimax", "glm",

    # AI Products & Tools
    "mcp", "model context protocol", "opencode", "cursor", "windsurf",
    "vibe coding", "vibe", "figma", "stitch",

    # Mobile & Frontend
    "flutter", "dart", "react", "vue", "svelte", "nextjs", "nuxt",
    "typescript", "javascript", "mobile", "ios", "android",

    # Backend
    "backend", "api", "rest", "graphql", "database",

    # Startup & Funding
    "startup", "funding", "series a", "series b", "venture", "vc",
    "acquisition", "ipo", "launch", "release", "announce",

    # Companies
    "google", "microsoft", "apple", "amazon", "meta", "nvidia",
    "anthropic", "xai", "mistral", "stability ai",
]

# Limits
MAX_ARTICLES = 30  # Tăng lên 30 bài
HOURS_BACK = 12  # Giới hạn trong 12 giờ gần nhất

# API Configuration - Gemini default, OpenAI fallback
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o"

# Output directory
REPORTS_DIR = "reports"
