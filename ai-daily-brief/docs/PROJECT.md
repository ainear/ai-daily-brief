# AI Daily Brief - Tài liệu Dự án

## Mục tiêu

Tạo hệ thống tự động tổng hợp tin tức AI và công nghệ mỗi ngày:
- **Input**: Tin tức từ 25+ RSS feeds (AI, Tech, Mobile, Startup...)
- **Xử lý**: AI (Gemini) phân tích và việt hóa nội dung
- **Output**: Báo cáo tiếng Việt gửi qua Telegram + lưu GitHub

---

## Việc đã làm

### 1. Thiết lập Project

```
ai-daily-brief/
├── main.py                 # Entry point
├── config.py               # RSS URLs, Keywords, API config
├── rss_fetcher.py          # Fetch & filter RSS
├── firecrawl_extractor.py  # Extract article content
├── analyzer.py             # AI analysis (Gemini/OpenAI)
├── consolidator.py         # Generate markdown report
├── telegram_notifier.py    # Send to Telegram
├── requirements.txt
└── reports/               # Output reports
```

### 2. Cấu hình RSS Feeds (25+ nguồn)

- **AI News**: TechCrunch AI, VentureBeat AI, MIT Tech Review
- **Tech Giants**: Google AI Blog, OpenAI, Meta AI, Microsoft AI, NVIDIA
- **Programming**: Hacker News, Dev.to, CSS-Tricks, JavaScript Weekly
- **Mobile/Frontend**: Flutter, Dart, React, Vue
- **Startup**: Product Hunt, TechCrunch Startups

### 3. Keywords (100+ từ khóa)

- AI: agent, agentic, automation, llm, gpt, openai, gemini, claude, deepseek...
- Tools: mcp, cursor, windsurf, vibe coding, figma, stitch
- Mobile: flutter, dart, swift, kotlin, react native
- Startup: funding, venture, acquisition, launch
- Tech: google, microsoft, apple, amazon, meta, nvidia...

### 4. API Integration

| Service | API Key | Status |
|---------|---------|--------|
| Firecrawl | `FIRECRAWL_API` | ✅ Extract content |
| Gemini | `GEMINI_API_KEY` | ✅ Analyze (model: gemini-2.5-flash) |
| OpenAI | `OPENAI_API_KEY` | ✅ Fallback |
| Telegram | `TELEGRAM_BOT_TOKEN` | ✅ Send notification |

### 5. GitHub Actions Automation

```yaml
# Chạy 3 lần/ngày
- 7:00 AM Vietnam
- 12:00 PM Vietnam
- 7:00 PM Vietnam
```

**Workflow**:
1. Checkout code
2. Install dependencies
3. Run main.py (fetch → extract → analyze → generate)
4. Commit & push report to GitHub
5. Send to Telegram

### 6. Telegram Bot

- Gửi báo cáo tự động sau mỗi lần chạy
- Format: HTML với link, tiếng Việt
- Hiển thị: Top 10 tin nổi bật + tổng số bài

---

## Kết quả

### Hiện tại

| Metric | Giá trị |
|--------|---------|
| Số bài/lần | 50-70 bài |
| Thời gian lấy bài | 48 giờ |
| Lần chạy/ngày | 3 lần |
| Telegram | ✅ Hoạt động |
| GitHub | ✅ Auto commit |

### Links

- **GitHub Repo**: https://github.com/ainear/ai-daily-brief
- **Reports**: https://github.com/ainear/ai-daily-brief/tree/main/ai-daily-brief/reports

### Các lỗi đã fix trong quá trình phát triển

1. **FIRECRAWL_API_KEY** → `FIRECRAWL_API` (tên biến trong .zshenv)
2. **Firecrawl API v2** → Sử dụng `params={}` thay vì positional args
3. **Firecrawl response** → Xử lý dict thay vì object
4. **Gemini model cũ** → Đổi sang `gemini-2.5-flash`
5. **GitHub Actions push** → Thêm `permissions: contents: write`

---

## Tính năng bổ sung: Affiliate & Product Reviews

### AI Tools Affiliate Scraper

Script riêng để tạo content cho affiliate site và product reviews:

```bash
python3 affiliate_scraper.py
```

**Output:** `affiliate/ai-tools-YYYY-MM-DD.md`

**Nguồn thu thập:**
- FutureTools.io
- There's AI For That
- AI Tools Directory
- TopAI.tools

**Tính năng:**
- ✅ Thu thập thông tin AI tools
- ✅ Phân tích với Gemini AI
- ✅ Tạo content tiếng Việt cho affiliate
- ✅ Xuất markdown blog post

---

## Hướng dẫn sử dụng

### Chạy thủ công

```bash
# Local
cd ai-daily-brief
python3 main.py

# GitHub Actions
gh workflow run daily-brief.yml --repo ainear/ai-daily-brief
```

### Cấu hình thêm

Chỉnh sửa `config.py`:
- `MAX_ARTICLES`: Số bài tối đa
- `HOURS_BACK`: Giờ lấy bài quá khứ
- `RSS_FEED_URLS`: Thêm nguồn RSS
- `KEYWORDS`: Thêm từ khóa lọc

### Secrets trong GitHub

Vào Settings → Secrets and variables → Actions:
- `FIRECRAWL_API`
- `GEMINI_API_KEY`
- `OPENAI_API_KEY`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

---

## Công nghệ sử dụng

- **Language**: Python 3.11
- **RSS Parsing**: feedparser
- **Content Extraction**: Firecrawl
- **AI Analysis**: Google Gemini 2.5 Flash
- **Notifications**: Telegram Bot API
- **CI/CD**: GitHub Actions
- **Host**: GitHub

---

## Cập nhật gần nhất

- **2026-02-26**: Tăng lên 100 bài, 48 giờ, 3 lần/ngày
- **2026-02-26**: Thêm Telegram notification
- **2026-02-26**: Đổi sang Gemini 2.5 Flash
- **2026-02-26**: Mở rộng RSS feeds và keywords
