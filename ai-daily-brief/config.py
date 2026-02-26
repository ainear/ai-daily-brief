"""Configuration for AI Daily Brief Generator."""

import os

# RSS Feed URLs - Maximum sources
RSS_FEED_URLS = [
    # AI News - TechCrunch
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://techcrunch.com/category/apps/feed/",
    "https://techcrunch.com/category/startups/feed/",

    # AI News - VentureBeat
    "https://venturebeat.com/category/ai/feed/",
    "https://venturebeat.com/category/transform/feed/",

    # MIT Tech Review
    "https://www.technologyreview.com/topic/artificial-intelligence/feed/",
    "https://www.technologyreview.com/feed/",

    # Hacker News
    "https://news.ycombinator.com/rss",

    # Dev.to - Programming
    "https://dev.to/feed",

    # Google AI / Microsoft / Meta / OpenAI
    "https://blog.google/technology/ai/rss",
    "https://blogs.microsoft.com/ai/feed/",
    "https://ai.meta.com/feed/",
    "https://openai.com/blog/rss.xml",
    "https://www.anthropic.com/feed",

    # NVIDIA
    "https://blogs.nvidia.com/feed/",

    # Product Hunt
    "https://www.producthunt.com/feed.atom",

    # Flutter / Dart
    "https://medium.com/feed/flutter",
    "https://medium.com/feed/dartlang",

    # Javascript / Frontend
    "https://css-tricks.com/feed/",
    "https://javascriptweekly.com/rss",
    "https://frontendfoc.us/feed",

    # Backend / API
    "https://blog.postman.com/feed/",
    "https://www.prisma.io/feed",

    # Tech blogs in English
    "https://feeds.feedburner.com/TheNextWeb",
    "https://www.wired.com/feed/category/tech/latest/rss",
    "https://www.theverge.com/rss/index.xml",

    # AI newsletters
    "https://www.ben Thompson.com/stratechery/feed/",
    "https://stratechery.com/feed/",

    # Latoken / Crypto Tech
    "https://coindesk.com/feed",

    # AI Tools
    "https://www.futuretools.io/feed",
]

# Keywords to filter articles - Maximum coverage
KEYWORDS = [
    # AI Core
    "ai", "artificial intelligence", "machine learning", "deep learning",
    "agent", "agentic", "agents", "automation", "autonomous",
    "llm", "large language model", "gpt", "chatgpt",
    "openai", "gemini", "claude", "deepseek", "minimax", "glm", "qwen",
    "anthropic", "xai", "mistral", "stability ai", "cohere",

    # AI Products
    "mcp", "model context protocol",
    "cursor", "windsurf", "cline", "devin", "replit",
    "vibe coding", "vibe",
    "figma", "stitch", "bolt", "lovable",

    # Programming
    "programming", "developer", "engineer", "code", "coding",
    "python", "javascript", "typescript", "rust", "go", "golang",
    "react", "vue", "svelte", "angular", "nextjs", "nuxt",
    "flutter", "dart", "swift", "kotlin", "react native",

    # Mobile & Frontend
    "mobile", "ios", "android", "app", "application",
    "frontend", "front-end", "web", "website", "ui", "ux",
    "css", "html", "responsive",

    # Backend
    "backend", "back-end", "server", "api", "rest", "graphql",
    "database", "sql", "postgres", "mysql", "mongodb", "redis",
    "aws", "azure", "gcp", "cloud", "docker", "kubernetes",

    # Startup & Funding
    "startup", "funding", "venture", "vc", "series a", "series b", "series c",
    "seed", "angel", "ipo", "acquisition", "merge", "valuation",
    "launch", "release", "announce", "unveil",

    # Tech Giants
    "google", "microsoft", "apple", "amazon", "meta", "facebook", "nvidia",
    "tesla", "spacex", "twitter", "x.com", "tiktok", "bytedance",
    "tencent", "alibaba", "baidu", "huawei",

    # Tools
    "github", "gitlab", "bitbucket", "vscode", "jetbrains",
    "notion", "slack", "zoom", "discord", "telegram",

    # Trends
    "trending", "viral", "breaking", "exclusive", "analysis",
    "review", "tutorial", "how to", "guide",
]

# Limits
MAX_ARTICLES = 100  # Tăng lên 100 bài
HOURS_BACK = 24  # 24 hours

# API Configuration - Gemini default, OpenAI fallback
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o"

# Output directory
REPORTS_DIR = "reports"
