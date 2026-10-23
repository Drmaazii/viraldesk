
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

## Run 2026-10-15T05:33:32+00:00 (289s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261015-0528.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261015-0528.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261015-0528.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261015-0528.md
- sources:
  - reddit(arctic): 14 calls, 350 items, 0 failed
  - youtube: 12 calls, 116 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures: none
- scoring: score = velocity(0-40) + engagement(0-40) + freshness(0-20)
  velocity = engagement-per-hour log-scaled (Reddit: (upvotes+2*comments)/age_h; YouTube: views/age_h)
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-10-16T05:25:49+00:00 (297s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261016-0520.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261016-0520.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261016-0520.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261016-0520.md
- sources:
  - reddit(arctic): 14 calls, 300 items, 2 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/Health: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/worldnews: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
- scoring: score = velocity(0-40) + engagement(0-40) + freshness(0-20)
  velocity = engagement-per-hour log-scaled (Reddit: (upvotes+2*comments)/age_h; YouTube: views/age_h)
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-10-17T05:20:15+00:00 (292s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261017-0515.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261017-0515.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261017-0515.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261017-0515.md
- sources:
  - reddit(arctic): 14 calls, 325 items, 1 failed
  - youtube: 12 calls, 117 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/AskHistorians: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
- scoring: score = velocity(0-40) + engagement(0-40) + freshness(0-20)
  velocity = engagement-per-hour log-scaled (Reddit: (upvotes+2*comments)/age_h; YouTube: views/age_h)
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-10-18T05:23:57+00:00 (278s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261018-0519.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261018-0519.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261018-0519.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261018-0519.md
- sources:
  - reddit(arctic): 14 calls, 325 items, 1 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/worldnews: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
- scoring: score = velocity(0-40) + engagement(0-40) + freshness(0-20)
  velocity = engagement-per-hour log-scaled (Reddit: (upvotes+2*comments)/age_h; YouTube: views/age_h)
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-10-19T05:41:08+00:00 (305s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261019-0536.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261019-0536.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261019-0536.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261019-0536.md
- sources:
  - reddit(arctic): 14 calls, 350 items, 0 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures: none
- scoring: score = velocity(0-40) + engagement(0-40) + freshness(0-20)
  velocity = engagement-per-hour log-scaled (Reddit: (upvotes+2*comments)/age_h; YouTube: views/age_h)
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-10-20T05:43:06+00:00 (350s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261020-0537.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261020-0537.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261020-0537.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261020-0537.md
- sources:
  - reddit(arctic): 14 calls, 300 items, 2 failed
  - youtube: 13 calls, 110 items, 1 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - youtube: 'health tips': HTTPSConnectionPool(host='www.youtube.com', port=443): Read timed out.
  - reddit(arctic): r/personalfinance: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/historymemes: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
- scoring: score = velocity(0-40) + engagement(0-40) + freshness(0-20)
  velocity = engagement-per-hour log-scaled (Reddit: (upvotes+2*comments)/age_h; YouTube: views/age_h)
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-10-21T05:44:04+00:00 (287s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261021-0539.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261021-0539.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261021-0539.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261021-0539.md
- sources:
  - reddit(arctic): 14 calls, 300 items, 2 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/personalfinance: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/Bitcoin: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
- scoring: score = velocity(0-40) + engagement(0-40) + freshness(0-20)
  velocity = engagement-per-hour log-scaled (Reddit: (upvotes+2*comments)/age_h; YouTube: views/age_h)
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-10-22T05:45:03+00:00 (293s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261022-0540.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261022-0540.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261022-0540.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261022-0540.md
- sources:
  - reddit(arctic): 14 calls, 325 items, 1 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/pakistan: 500 Server Error: Internal Server Error for url: https://arctic-shift.photon-reddit.com/api/posts/se
- scoring: score = velocity(0-40) + engagement(0-40) + freshness(0-20)
  velocity = engagement-per-hour log-scaled (Reddit: (upvotes+2*comments)/age_h; YouTube: views/age_h)
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-10-23T05:44:44+00:00 (267s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=0 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261023-0540.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261023-0540.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261023-0540.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261023-0540.md
- sources:
  - reddit(arctic): 14 calls, 125 items, 9 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/Health: 500 Server Error: Internal Server Error for url: https://arctic-shift.photon-reddit.com/api/posts/se
  - reddit(arctic): r/loseit: 500 Server Error: Internal Server Error for url: https://arctic-shift.photon-reddit.com/api/posts/se
  - reddit(arctic): r/AskDocs: 500 Server Error: Internal Server Error for url: https://arctic-shift.photon-reddit.com/api/posts/se
  - reddit(arctic): r/pakistan: 500 Server Error: Internal Server Error for url: https://arctic-shift.photon-reddit.com/api/posts/se
  - reddit(arctic): r/CryptoCurrency: 500 Server Error: Internal Server Error for url: https://arctic-shift.photon-reddit.com/api/posts/se
  - reddit(arctic): r/Bitcoin: 500 Server Error: Internal Server Error for url: https://arctic-shift.photon-reddit.com/api/posts/se
  - reddit(arctic): r/history: 500 Server Error: Internal Server Error for url: https://arctic-shift.photon-reddit.com/api/posts/se
  - reddit(arctic): r/AskHistorians: 500 Server Error: Internal Server Error for url: https://arctic-shift.photon-reddit.com/api/posts/se
  - reddit(arctic): r/historymemes: 500 Server Error: Internal Server Error for url: https://arctic-shift.photon-reddit.com/api/posts/se
- scoring: score = velocity(0-40) + engagement(0-40) + freshness(0-20)
  velocity = engagement-per-hour log-scaled (Reddit: (upvotes+2*comments)/age_h; YouTube: views/age_h)
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API
