"""Analyzer Module - Analyze articles using Gemini API (default) with OpenAI fallback."""

import json
from typing import Dict, List, Optional

from config import GEMINI_API_KEY, GEMINI_MODEL, OPENAI_API_KEY, OPENAI_MODEL


SYSTEM_PROMPT = """Bạn là một chuyên gia phân tích AI và startup. Nhiệm vụ của bạn là phân tích các bài viết về AI và đưa ra insights có giá trị bằng TIẾNG VIỆT.

Hãy phân tích từng bài viết và trả về JSON với cấu trúc sau:
{
  "title": "Tiêu đề bài viết",
  "url": "URL bài viết",
  "summary": "Tóm tắt 2-3 câu về nội dung chính BẰNG TIẾNG VIỆT",
  "opportunities": ["Cơ hội 1", "Cơ hội 2", "Cơ hội 3"] - TẤT CẢ BẰNG TIẾNG VIỆT,
  "key_insight": "Insight quan trọng nhất từ bài viết BẰNG TIẾNG VIỆT",
  "actionable": "Hành động cụ thể có thể thực hiện BẰNG TIẾNG VIỆT"
}

QUAN TRỌNG: Tất cả nội dung text phải bằng TIẾNG VIỆT có dấu. Không trả về tiếng Anh.
Trả về JSON hợp lệ, không có markdown code blocks."""


USER_PROMPT_TEMPLATE = """Phân tích bài viết sau đây:

Tiêu đề: {title}
URL: {url}
Nội dung:
{content}

Trả về JSON với format đã chỉ định."""


def parse_json_response(text: str) -> Dict:
    """Parse JSON from response text, handling markdown blocks."""
    result_text = text.strip()

    # Handle potential markdown code blocks
    if result_text.startswith("```json"):
        result_text = result_text[7:]
    if result_text.startswith("```"):
        result_text = result_text[3:]
    if result_text.endswith("```"):
        result_text = result_text[:-3]

    return json.loads(result_text.strip())


def analyze_with_gemini(title: str, url: str, content: str) -> Optional[Dict]:
    """Analyze using Gemini API."""
    try:
        from google import genai

        client = genai.Client(api_key=GEMINI_API_KEY)

        user_prompt = USER_PROMPT_TEMPLATE.format(
            title=title,
            url=url,
            content=content[:8000]
        )

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[{"role": "user", "parts": [{"text": f"{SYSTEM_PROMPT}\n\n{user_prompt}"}]}]
        )

        result = parse_json_response(response.text)

        return {
            "title": result.get("title", title),
            "url": url,
            "summary": result.get("summary", ""),
            "opportunities": result.get("opportunities", []),
            "key_insight": result.get("key_insight", ""),
            "actionable": result.get("actionable", "")
        }

    except Exception as e:
        print(f"Gemini error for {url}: {e}")
        return None


def analyze_with_openai(title: str, url: str, content: str) -> Optional[Dict]:
    """Analyze using OpenAI API (fallback)."""
    try:
        from openai import OpenAI

        client = OpenAI(api_key=OPENAI_API_KEY)

        user_prompt = USER_PROMPT_TEMPLATE.format(
            title=title,
            url=url,
            content=content[:8000]
        )

        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            max_tokens=2000,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ]
        )

        result = parse_json_response(response.choices[0].message.content)

        return {
            "title": result.get("title", title),
            "url": url,
            "summary": result.get("summary", ""),
            "opportunities": result.get("opportunities", []),
            "key_insight": result.get("key_insight", ""),
            "actionable": result.get("actionable", "")
        }

    except Exception as e:
        print(f"OpenAI error for {url}: {e}")
        return None


def analyze_article(title: str, url: str, content: str) -> Optional[Dict]:
    """Analyze article - try Gemini first, if fails try OpenAI."""
    # Try Gemini first (default)
    if GEMINI_API_KEY:
        try:
            result = analyze_with_gemini(title, url, content)
            if result:
                print(f"  ✓ Gemini success")
                return result
        except Exception as e:
            print(f"  ✗ Gemini failed: {e}")

    # Fallback to OpenAI
    if OPENAI_API_KEY:
        try:
            result = analyze_with_openai(title, url, content)
            if result:
                print(f"  ✓ OpenAI success")
                return result
        except Exception as e:
            print(f"  ✗ OpenAI failed: {e}")

    print(f"Warning: No API available for {url}")
    return None


def analyze_articles(articles: List[Dict]) -> List[Dict]:
    """Analyze multiple articles."""
    analyzed = []

    for article in articles:
        title = article.get("title", "")
        url = article.get("url", "")
        content = article.get("markdown", "")

        if not content:
            continue

        print(f"Analyzing: {title}")
        result = analyze_article(title, url, content)

        if result:
            analyzed.append(result)

    return analyzed


if __name__ == "__main__":
    # Test
    test_article = {
        "title": "AI Startup Raises $100M",
        "url": "https://example.com",
        "markdown": "A new AI startup has raised $100M in Series B funding..."
    }
    result = analyze_article(
        test_article["title"],
        test_article["url"],
        test_article["markdown"]
    )
    print(result)
