"""Consolidator Module - Generate final report from analyzed articles."""

from datetime import datetime
from typing import List, Dict
import os

from config import REPORTS_DIR


def generate_report(analyzed_articles: List[Dict]) -> str:
    """Generate final Markdown report from analyzed articles."""
    if not analyzed_articles:
        return "# AI Daily Brief\n\nNo articles analyzed."

    # Extract all opportunities
    all_opportunities = []
    for article in analyzed_articles:
        all_opportunities.extend(article.get("opportunities", []))

    # Get top 3 opportunities (most common)
    opportunity_counts = {}
    for opp in all_opportunities:
        opp_lower = opp.lower()
        opportunity_counts[opp_lower] = opportunity_counts.get(opp_lower, 0) + 1

    sorted_opportunities = sorted(
        opportunity_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )
    top_3_opportunities = [opp[0].title() for opp in sorted_opportunities[:3]]

    # Extract key insights
    insights = [a.get("key_insight", "") for a in analyzed_articles if a.get("key_insight")]
    emerging_trends = extract_trends(insights)

    # Extract actionable items
    actionables = [a.get("actionable", "") for a in analyzed_articles if a.get("actionable")]
    actionable_directions = actionables[:10]  # Tăng lên 10

    # Generate recommendation
    recommendation = generate_recommendation(analyzed_articles)

    # Build report
    report = f"""# AI Daily Brief - {datetime.now().strftime('%Y-%m-%d')}

## Tổng quan
- Số bài viết phân tích: {len(analyzed_articles)}
- Nguồn: TechCrunch, VentureBeat, MIT Tech Review, Hacker News, Dev.to, Google AI, OpenAI, Meta AI, Microsoft AI, Product Hunt, và nhiều nguồn khác...

---

## Top 3 Cơ hội

{format_list(top_3_opportunities)}

---

## Xu hướng nổi bật

{format_list(emerging_trends)}

---

## 10 Hướng hành động cụ thể

{format_numbered_list(actionable_directions)}

---

## Khuyến nghị cho 3 giờ tới

{recommendation}

---

## Chi tiết bài viết

"""

    for i, article in enumerate(analyzed_articles, 1):
        report += f"""### {i}. {article.get('title', 'N/A')}

**Tóm tắt:** {article.get('summary', 'N/A')}

**Key Insight:** {article.get('key_insight', 'N/A')}

**Hành động:** {article.get('actionable', 'N/A')}

[Đọc bài viết]({article.get('url', '#')})

---

"""

    return report


def extract_trends(insights: List[str]) -> List[str]:
    """Extract emerging trends from insights using simple clustering."""
    # Simple keyword-based trend extraction
    trend_keywords = {
        "agent": "AI Agents",
        "automation": "Automation",
        "llm": "LLM Developments",
        "startup": "Startup Funding",
        "model": "New AI Models",
        "product": "AI Products",
        "research": "Research Breakthroughs"
    }

    trend_counts = {k: 0 for k in trend_keywords.keys()}

    for insight in insights:
        insight_lower = insight.lower()
        for key in trend_counts:
            if key in insight_lower:
                trend_counts[key] += 1

    trends = [
        trend_keywords[k]
        for k, v in sorted(trend_counts.items(), key=lambda x: x[1], reverse=True)
        if v > 0
    ]

    return trends[:5] if trends else ["AI Developments"]


def generate_recommendation(articles: List[Dict]) -> str:
    """Generate recommendation for next 3 hours."""
    if not articles:
        return "Không có đủ dữ liệu để đưa ra khuyến nghị."

    # Get most recent article with actionable item
    for article in articles:
        if article.get("actionable"):
            return article.get("actionable", "Tiếp tục theo dõi các xu hướng AI mới nhất.")

    return "Tập trung vào việc tìm hiểu về AI Agents và automation trong workflow."


def format_list(items: List[str]) -> str:
    """Format list as Markdown bullet points."""
    if not items:
        return "- Chưa có thông tin"
    return "\n".join(f"- {item}" for item in items)


def format_numbered_list(items: List[str]) -> str:
    """Format list as Markdown numbered list."""
    if not items:
        return "1. Chưa có thông tin"
    return "\n".join(f"{i+1}. {item}" for i, item in enumerate(items))


def save_report(report: str, reports_dir: str = REPORTS_DIR) -> str:
    """Save report to file."""
    os.makedirs(reports_dir, exist_ok=True)

    filename = f"ai-daily-brief-{datetime.now().strftime('%Y-%m-%d')}.md"
    filepath = os.path.join(reports_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)

    return filepath


if __name__ == "__main__":
    # Test
    test_articles = [
        {
            "title": "AI Startup Raises $100M",
            "url": "https://example.com/1",
            "summary": "AI startup raises massive funding",
            "opportunities": ["AI Products", "Automation"],
            "key_insight": "Investors are bullish on AI",
            "actionable": "Explore AI partnership opportunities"
        }
    ]
    report = generate_report(test_articles)
    print(report)
