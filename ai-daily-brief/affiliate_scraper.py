"""AI Tools Affiliate - Build content for affiliate site and product reviews."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
from datetime import datetime
from firecrawl import FirecrawlApp
from config import FIRECRAWL_API_KEY, GEMINI_API_KEY, GEMINI_MODEL

# AI Tools Sources
TOOLS_SOURCES = [
    "https://www.producthunt.com/categories/artificial-intelligence",
    "https://alternativeTo/category/artificial-intelligence/",
    "https://www.g2.com/categories/artificial-intelligence",
    "https://www.capterra.com/artificial-intelligence-software/",
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
            "content": markdown[:5000]
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

Hãy phân tích tool sau và tạo content tiếng Việt cho affiliate:

URL: {tool_info['url']}

Nội dung:
{tool_info['content'][:3000]}

Trả về JSON:
{{
  "name": "Tên tool",
  "tagline": "Tagline ngắn",
  "description": "Mô tả 2-3 câu bằng tiếng Việt",
  "features": ["Tính năng 1", "Tính năng 2", "Tính năng 3"],
  "pricing": "Giá (nếu có)",
  "pros": ["Điểm mạnh 1", "Điểm mạnh 2"],
  "cons": ["Điểm yếu 1", "Điểm yếu 2"],
  "affiliate_angle": "Góc tiếp cận affiliate: tại sao người dùng nên mua/sử dụng"
}}

Trả về JSON hợp lệ, không có markdown."""

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

Chào mừng bạn đến với bài tổng hợp các AI tools hàng đầu tháng này!

Trong bài viết này, mình sẽ giới thiệu những công cụ AI tốt nhất giúp bạn:
- Tăng năng suất công việc
- Tự động hóa các tác vụ lặp đi lặp lại
- Tạo content nhanh chóng
- Phát triển business hiệu quả

---

"""

    for i, tool in enumerate(tools, 1):
        if not tool:
            continue

        post += f"""## {i}. {tool.get('name', 'AI Tool')}

**Tagline:** {tool.get('tagline', '')}

**Mô tả:** {tool.get('description', '')}

### Tính năng nổi bật:
"""
        for feature in tool.get('features', []):
            post += f"- {feature}\n"

        post += f"""
### 💰 Giá:
{tool.get('pricing', 'Liên hệ website')}

### ✅ Ưu điểm:
"""
        for pro in tool.get('pros', []):
            post += f"- {pro}\n"

        post += f"""
### ❌ Nhược điểm:
"""
        for con in tool.get('cons', []):
            post += f"- {con}\n"

        post += f"""
### 🎯 Tại sao nên dùng:
{tool.get('affiliate_angle', '')}

**[Xem chi tiết →]({tool.get('url', '#')})**

---
"""

    post += """
## Kết luận

Các AI tools trên đây là những lựa chọn tốt nhất hiện nay. Tùy vào nhu cầu của bạn, hãy chọn công cụ phù hợp nhất nhé!

**Disclaimer**: Các link trong bài viết là affiliate links. Mình sẽ nhận commission khi bạn mua qua link của mình - không tốn thêm chi phí cho bạn.

---

*Bài viết được cập nhật: {datetime.now().strftime('%d/%m/%Y')}*
"""

    return post


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
        if tool_info:
            analyzed = analyze_tool_with_ai(tool_info)
            if analyzed:
                tools.append(analyzed)
                print(f"  ✓ {analyzed.get('name', 'Unknown')}")

    if not tools:
        print("No tools extracted.")
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
    print(f"Total tools: {len(tools)}")


if __name__ == "__main__":
    run_affiliate_scraper()
