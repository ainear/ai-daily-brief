"""Main entry point for AI Daily Brief Generator."""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rss_fetcher import fetch_all_articles
from firecrawl_extractor import extract_articles_batch
from analyzer import analyze_articles
from consolidator import generate_report, save_report
from config import FIRECRAWL_API_KEY, GEMINI_API_KEY, OPENAI_API_KEY


def main():
    """Main execution flow."""
    print("=== AI Daily Brief Generator ===\n")

    # Check API keys
    if not FIRECRAWL_API_KEY:
        print("Error: FIRECRAWL_API_KEY not set")
        print("Please set the environment variable:")
        print("  export FIRECRAWL_API_KEY=your_api_key")
        sys.exit(1)

    if not GEMINI_API_KEY and not OPENAI_API_KEY:
        print("Error: No AI API key set")
        print("Please set one of:")
        print("  export GEMINI_API_KEY=your_api_key")
        print("  export OPENAI_API_KEY=your_api_key")
        sys.exit(1)

    # Step 1: Fetch RSS articles
    print("Step 1: Fetching RSS articles...")
    articles = fetch_all_articles()
    print(f"Found {len(articles)} articles\n")

    if not articles:
        print("No articles found. Exiting.")
        sys.exit(0)

    # Step 2: Extract content with Firecrawl
    print("Step 2: Extracting content with Firecrawl...")
    urls = [a["url"] for a in articles]
    extracted = extract_articles_batch(urls)
    print(f"Extracted {len(extracted)} articles\n")

    # Merge extracted content with original articles
    for article in articles:
        for ext in extracted:
            if article["url"] == ext["url"]:
                article["markdown"] = ext.get("markdown", "")
                break

    # Filter to only articles with content
    articles_with_content = [a for a in articles if a.get("markdown")]

    if not articles_with_content:
        print("No content extracted. Exiting.")
        sys.exit(0)

    # Step 3: Analyze with AI (Gemini default, OpenAI fallback)
    print("Step 3: Analyzing articles...")
    analyzed = analyze_articles(articles_with_content)
    print(f"Analyzed {len(analyzed)} articles\n")

    if not analyzed:
        print("No articles analyzed. Exiting.")
        sys.exit(0)

    # Step 4: Generate and save report
    print("Step 4: Generating report...")
    report = generate_report(analyzed)
    filepath = save_report(report)
    print(f"Report saved to: {filepath}\n")

    print("=== Complete ===")
    print(f"Report: {filepath}")


if __name__ == "__main__":
    main()
