
## Run 2026-10-12T02:28:53+00:00 (20s) — niches: health
- decoded: health=5 blog + 5 videos
- reports: /home/hatch/workspace/viraldesk/trends/reports/health-20261012-0228.md
- sources:
  - reddit(arctic): 4 calls, 75 items, 1 failed
  - youtube: 3 calls, 29 items, 0 failed
  - video_validate: 5 calls, 5 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/nutrition: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
- scoring: score = velocity(0-40) + engagement(0-40) + freshness(0-20)
  velocity = engagement-per-hour log-scaled (Reddit: (upvotes+2*comments)/age_h; YouTube: views/age_h)
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-10-12T02:30:20+00:00 (64s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/hatch/workspace/viraldesk/trends/reports/health-20261012-0229.md, /home/hatch/workspace/viraldesk/trends/reports/news-20261012-0229.md, /home/hatch/workspace/viraldesk/trends/reports/finance-20261012-0229.md, /home/hatch/workspace/viraldesk/trends/reports/history-20261012-0229.md
- sources:
  - reddit(arctic): 14 calls, 350 items, 0 failed
  - youtube: 12 calls, 119 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures: none
- scoring: score = velocity(0-40) + engagement(0-40) + freshness(0-20)
  velocity = engagement-per-hour log-scaled (Reddit: (upvotes+2*comments)/age_h; YouTube: views/age_h)
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-10-14T05:48:13+00:00 (300s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261014-0543.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261014-0543.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261014-0543.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261014-0543.md
- sources:
  - reddit(arctic): 14 calls, 325 items, 1 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/stocks: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
- scoring: score = velocity(0-40) + engagement(0-40) + freshness(0-20)
  velocity = engagement-per-hour log-scaled (Reddit: (upvotes+2*comments)/age_h; YouTube: views/age_h)
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API
