# AI Daily Brief Generator - Tài liệu Dự án

## Mục tiêu

Tạo script Python chạy daily để generate Vietnamese AI opportunity briefing từ 4 RSS feeds, sử dụng:
- **Firecrawl** - Extract content từ articles
- **AI API** (OpenAI mặc định, Gemini fallback) - Analyze và generate insights
- Output: Markdown report trong thư mục `reports/`

---

## Việc đã làm

### 1. Cấu trúc Project

Tạo các file trong `/Users/gray/vivu/firecralw/ai-daily-brief/`:

```
ai-daily-brief/
├── main.py                 # Entry point
├── config.py               # Configuration (URLs, API keys, settings)
├── rss_fetcher.py          # RSS fetch & filter (24h, keywords, max 15)
├── firecrawl_extractor.py  # Firecrawl SDK integration
├── analyzer.py             # AI analysis (OpenAI/Gemini)
├── consolidator.py         # Report generation
├── requirements.txt        # Dependencies
├── run.sh                 # Shell wrapper script
└── reports/               # Output directory
```

### 2. Chi tiết từng Module

#### `config.py`
- 4 RSS feed URLs: TechCrunch AI, VentureBeat AI, MIT Technology Review, Y Combinator
- Keywords filter: ai, agent, automation, llm, startup, funding, model
- Limits: 15 articles/day, 24h timeframe
- API config: OpenAI (default), Gemini (fallback)

#### `rss_fetcher.py`
- Fetch và parse RSS feeds bằng `feedparser`
- Filter theo thời gian (24h) và keywords
- Remove duplicates, limit 15 articles
- Return list: {title, url, published_date}

#### `firecrawl_extractor.py`
- Sử dụng Firecrawl SDK để extract content
- Chỉ lấy main content, bỏ nav/ads/footer
- Return markdown content

#### `analyzer.py`
- **OpenAI** (mặc định): model `gpt-4o`
- **Gemini** (fallback): model `gemini-1.5-flash`
- Prompt phân tích tiếng Việt, trả về JSON với:
  - summary, opportunities, key_insight, actionable

#### `consolidator.py`
- Merge all analyzed articles
- Generate report với:
  - Top 3 opportunities
  - Emerging trends
  - 5 actionable directions
  - Recommendation for 3 hours

#### `main.py`
- Orchestrate all modules
- Handle errors gracefully
- Save to `reports/ai-daily-brief-{DATE}.md`

### 3. API Configuration

| API | Biến môi trường | Model |
|-----|------------------|-------|
| Firecrawl | `FIRECRAWL_API` | - |
| OpenAI | `OPENAI_API_KEY` | gpt-4o |
| Gemini | `GEMINI_API_KEY` | gemini-1.5-flash |

**Thứ tự ưu tiên:** OpenAI → Gemini (fallback)

---

## Kết quả

### Trạng thái hiện tại

- **Code**: ✅ Hoàn thành
- **Dependencies**: ✅ Cài đặt được
- **Chạy thử**: ✅ **Chạy thành công!**

### Các lỗi đã fix trong quá trình dev

1. **FIRECRAWL_API_KEY** → đổi thành `FIRECRAWL_API` trong config.py (vì biến môi trường trong .zshenv là `FIRECRAWL_API`)
2. **Firecrawl API v2** → sửa code dùng `params={}` thay vì positional args
3. **Firecrawl response** → xử lý dict response thay vì object (API v2 trả về dict)
4. **Gemini model cũ** → đổi sang OpenAI làm primary (vì gemini-2.0-flash không còn available)

### Report đã tạo

- File: `reports/ai-daily-brief-2026-02-26.md`
- 12 bài viết AI từ TechCrunch
- Bao gồm: Top 3 cơ hội, xu hướng, 5 hành động cụ thể, chi tiết từng bài

---

## Cách sử dụng

### 1. Cài đặt

```bash
cd /Users/gray/vivu/firecralw/ai-daily-brief
pip install -r requirements.txt
```

### 2. Set API Keys

Thêm vào `.zshrc` hoặc `.zshenv`:
```bash
export FIRECRAWL_API="fc-xxx"  # Firecrawl API key
export OPENAI_API_KEY="sk-xxx"  # OpenAI API key
export GEMINI_API_KEY="AIzaSy..."  # Gemini API key (optional)
```

### 3. Chạy script

```bash
python3 main.py
# hoặc
./run.sh
```

### 4. Cron job (6 AM daily)

```bash
crontab -e
# Thêm dòng:
0 6 * * * /Users/gray/vivu/firecralw/ai-daily-brief/run.sh >> /Users/gray/vivu/firecralw/ai-daily-brief/cron.log 2>&1
```

### 5. Output

Report sẽ được lưu tại:
```
reports/ai-daily-brief-YYYY-MM-DD.md
```

---

## Dependencies

```
feedparser==6.0.11
firecrawl-py==1.6.1
google-genai==0.1.0
openai==1.58.1
python-dateutil==2.9.0
```
