"""AI Tools Affiliate - Build content for affiliate site and product reviews."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
from datetime import datetime
from firecrawl import FirecrawlApp
from config import FIRECRAWL_API_KEY, GEMINI_API_KEY, GEMINI_MODEL

# Telegram config
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# AI Tools Sources - Thêm nhiều nguồn hơn
TOOLS_SOURCES = [
    # FutureTools - AI Tools Directory
    "https://www.futuretools.io/",

    # There's AI For That
    "https://theresanaiforthat.com/",

    # AI Tools Directory
    "https://aitoolsdirectory.com/",

    # TopAI - AI Tools
    "https://topai.tools/",

    # SaaS AI Tools
    "https://saas-ai-tools.com/",
]


def extract_tool_info(url: str, app: FirecrawlApp) -> dict:
    """Extract tool information from URL."""
    try:
        result = app.scrape_url(url, params={"formats": ["markdown"]})

        if isinstance(result, dict):
            markdown = result.get('markdown', '')
        else:
            markdown = result.markdown if hasattr(result, 'markdown') else ''

        return {
            "url": url,
            "content": markdown[:8000]
        }
    except Exception as e:
        print(f"Error extracting {url}: {e}")
        return None


def analyze_tool_with_ai(tool_info: dict) -> dict:
    """Analyze tool and generate affiliate content."""
    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)

        prompt = f"""Bạn là chuyên gia viết content affiliate về AI tools.

Hãy phân tích tool/website sau và tạo content tiếng Việt cho affiliate:

URL: {tool_info['url']}

Nội dung:
{tool_info['content'][:4000]}

Trả về JSON:
{{
  "name": "Tên tool/website",
  "tagline": "Tagline ngắn",
  "description": "Mô tả 2-3 câu bằng tiếng Việt",
  "features": ["Tính năng 1", "Tính năng 2", "Tính năng 3"],
  "pricing": "Giá (nếu có, VD: $19/tháng)",
  "pros": ["Điểm mạnh 1", "Điểm mạnh 2"],
  "cons": ["Điểm yếu 1"],
  "affiliate_angle": "Góc tiếp cận affiliate: tại sao người dùng nên dùng"
}}

Chỉ trả về JSON hợp lệ, không có markdown."""

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[{"role": "user", "parts": [{"text": prompt}]}]
        )

        import json
        text = response.text.strip()
        # Remove markdown blocks
        if text.startswith("```"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]

        return json.loads(text.strip())

    except Exception as e:
        print(f"Error analyzing tool: {e}")
        return None


def generate_affiliate_post(tools: list) -> str:
    """Generate affiliate blog post."""

    post = f"""# 🔥 Tổng Hợp AI Tools Hàng Đầu - {datetime.now().strftime('%B %Y')}

## Giới thiệu

Chào mừng bạn đến với bài tổng hợp các AI tools hàng đầu!

Trong bài viết này, mình sẽ giới thiệu những công cụ AI tốt nhất giúp bạn:
- 🚀 Tăng năng suất công việc
- 🤖 Tự động hóa các tác vụ lặp đi lặp lại
- ✍️ Tạo content nhanh chóng
- 💼 Phát triển business hiệu quả

---

"""

    for i, tool in enumerate(tools, 1):
        if not tool:
            continue

        name = tool.get('name', 'AI Tool')
        tagline = tool.get('tagline', '')
        description = tool.get('description', '')
        pricing = tool.get('pricing', 'Liên hệ website')
        url = tool.get('url', '#')

        post += f"""## {i}. {name}

**Tagline:** {tagline}

**Mô tả:** {description}

### 🎯 Tính năng nổi bật:
"""
        for feature in tool.get('features', [])[:5]:
            post += f"- {feature}\n"

        post += f"""
### 💰 Giá:
{pricing}

### ⭐ Đánh giá:
"""
        for pro in tool.get('pros', []):
            post += f"- ✅ {pro}\n"

        for con in tool.get('cons', []):
            post += f"- ⚠️ {con}\n"

        post += f"""
### 🎁 Link affiliate / Xem chi tiết:
👉 [Xem tại đây →]({url})

---

"""

    post += f"""
## 💡 Kết luận

Các AI tools trên đây là những lựa chọn tốt nhất hiện nay. Tùy vào nhu cầu của bạn, hãy chọn công cụ phù hợp nhất nhé!

---
🔄 **Cập nhật lần cuối:** {datetime.now().strftime('%d/%m/%Y')}

*Disclaimer: Bài viết có thể chứa affiliate links. Mình nhận commission khi bạn mua qua link của mình - không tốn thêm chi phí cho bạn.*
"""

    return post


def send_telegram_notification(tools: list, filename: str):
    """Send affiliate report to Telegram."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram not configured, skipping notification")
        return

    # Build message
    date = datetime.now().strftime("%d/%m/%Y")
    message = f"🤖 <b>AI Tools Affiliate - {date}</b>\n\n"
    message += f"📦 Tổng hợp: <b>{len(tools)} tools</b>\n\n"

    # Top 5 tools
    message += "🔥 <b>Top Tools:</b>\n"

    for i, tool in enumerate(tools[:5], 1):
        name = tool.get('name', 'Unknown')[:40]
        tagline = tool.get('tagline', '')[:50]
        message += f"{i}. <b>{name}</b>\n"
        message += f"   {tagline}\n"

    message += f"\n📄 <a href='https://github.com/ainear/ai-daily-brief/blob/main/{filename}'>Xem chi tiết →</a>\n"
    message += f"\n⏰ Generated: {datetime.now().strftime('%H:%M')}"

    # Send
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        response = requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        })
        if response.json().get("ok"):
            print("✅ Telegram notification sent!")
        else:
            print(f"❌ Telegram error: {response.json()}")
    except Exception as e:
        print(f"❌ Telegram error: {e}")


def run_affiliate_scraper():
    """Main function to run affiliate scraper."""
    print("=== AI Tools Affiliate Scraper ===\n")

    if not FIRECRAWL_API_KEY:
        print("Error: FIRECRAWL_API not set")
        return

    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not set")
        return

    app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

    # Extract tools
    print("Step 1: Extracting tools from sources...")
    tools = []

    for source in TOOLS_SOURCES:
        print(f"Extracting: {source}")
        tool_info = extract_tool_info(source, app)
        if tool_info and tool_info.get('content'):
            print(f"  ✓ Extracted, analyzing...")
            analyzed = analyze_tool_with_ai(tool_info)
            if analyzed:
                tools.append(analyzed)
                print(f"  ✓ {analyzed.get('name', 'Unknown')}")
        else:
            print(f"  ✗ Failed to extract")

    if not tools:
        print("No tools extracted. Trying alternative sources...")

        # Fallback: Try more general AI news sites
        alt_sources = [
            "https://news.ycombinator.com/",
            "https://www.producthunt.com/",
        ]

        for source in alt_sources:
            print(f"Alternative: {source}")
            tool_info = extract_tool_info(source, app)
            if tool_info and tool_info.get('content'):
                analyzed = analyze_tool_with_ai(tool_info)
                if analyzed:
                    tools.append(analyzed)
                    print(f"  ✓ {analyzed.get('name', 'Unknown')}")

    if not tools:
        print("No tools extracted. Please check sources.")
        return

    print(f"\nStep 2: Generated {len(tools)} tool reviews")

    # Generate post
    print("Step 3: Generating affiliate post...")
    post = generate_affiliate_post(tools)

    # Save
    os.makedirs("affiliate", exist_ok=True)
    filename = f"affiliate/ai-tools-{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(post)

    print(f"\n✅ Saved to: {filename}")

    # Send to Telegram
    send_telegram_notification(tools, filename)

    print(f"Total tools: {len(tools)}")


if __name__ == "__main__":
    run_affiliate_scraper()
