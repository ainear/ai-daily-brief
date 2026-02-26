"""Telegram Notifier Module - Send AI Daily Brief to Telegram."""

import os
import requests
from datetime import datetime
from typing import List, Dict


# Telegram config from environment
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_to_telegram(report: str, analyzed_articles: List[Dict]) -> bool:
    """Send report to Telegram channel/chat."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set")
        return False

    # Build message
    message = build_telegram_message(analyzed_articles)

    # Send message
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
    )

    result = response.json()
    if result.get("ok"):
        print(f"✅ Report sent to Telegram")
        return True
    else:
        print(f"❌ Telegram error: {result.get('description')}")
        return False


def build_telegram_message(articles: List[Dict]) -> str:
    """Build Telegram message from analyzed articles."""

    date = datetime.now().strftime("%d/%m/%Y")
    message = f"🤖 <b>AI Daily Brief - {date}</b>\n\n"
    message += f"📊 {len(articles)} bài viết từ TechCrunch, VentureBeat, MIT Tech Review\n\n"

    # Top 3 Opportunities
    all_opportunities = []
    for article in articles:
        all_opportunities.extend(article.get("opportunities", []))
    unique_opps = list(set(all_opportunities))[:3]

    if unique_opps:
        message += "🎯 <b>Top 3 Cơ hội:</b>\n"
        for opp in unique_opps:
            message += f"• {opp}\n"
        message += "\n"

    # Top 10 articles (more content)
    message += "📰 <b>Tin nổi bật (Top 10):</b>\n\n"

    for i, article in enumerate(articles[:10], 1):
        title = article.get("title", "")[:60]
        summary = article.get("summary", "")[:100]
        url = article.get("url", "")

        message += f"<b>{i}. {title}</b>\n"
        message += f"{summary}...\n"
        message += f"<a href=\"{url}\">Đọc →</a>\n\n"

    # Show count
    if len(articles) > 10:
        message += f"📊 <i>Và {len(articles) - 10} bài viết khác...</i>\n\n"

    # Recommendation
    if articles and articles[0].get("actionable"):
        message += "⚡ <b>Khuyến nghị:</b>\n"
        message += f"{articles[0].get('actionable')}\n"

    message += f"\n⏰ Generated: {datetime.now().strftime('%H:%M')}"

    return message


if __name__ == "__main__":
    print("Telegram Notifier")
    print(f"Bot Token: {'✓ Set' if TELEGRAM_BOT_TOKEN else '✗ Missing'}")
    print(f"Chat ID: {'✓ Set' if TELEGRAM_CHAT_ID else '✗ Missing'}")

    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("\nTo use:")
        print("  export TELEGRAM_BOT_TOKEN='your_bot_token'")
        print("  export TELEGRAM_CHAT_ID='your_chat_id'")
