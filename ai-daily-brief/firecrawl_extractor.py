"""Firecrawl Extractor Module - Extract structured content from articles."""

from typing import Dict, Optional
from firecrawl import FirecrawlApp

from config import FIRECRAWL_API_KEY


def extract_article_content(url: str) -> Optional[Dict]:
    """Extract structured content from a URL using Firecrawl."""
    if not FIRECRAWL_API_KEY:
        print("Warning: FIRECRAWL_API_KEY not set")
        return None

    try:
        app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

        # Scrape with markdown format for better content extraction
        result = app.scrape_url(
            url,
            params={
                "formats": ["markdown"]
            }
        )

        if not result:
            return None

        # Handle both dict and object responses
        if isinstance(result, dict):
            markdown = result.get('markdown', '')
        else:
            markdown = result.markdown if hasattr(result, 'markdown') else ""

        # Extract key information
        content = {
            "url": url,
            "markdown": markdown,
            "content_length": len(markdown) if markdown else 0
        }

        return content

    except Exception as e:
        print(f"Error extracting {url}: {e}")
        return None


def extract_articles_batch(urls: list) -> list:
    """Extract content from multiple URLs."""
    results = []

    for url in urls:
        print(f"Extracting: {url}")
        content = extract_article_content(url)
        if content:
            results.append(content)

    return results


if __name__ == "__main__":
    # Test with a sample URL
    test_url = "https://techcrunch.com/2024/01/01/ai-startup-raises-funding/"
    result = extract_article_content(test_url)
    print(result)
