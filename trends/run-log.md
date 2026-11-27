
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

## Run 2026-10-24T05:23:04+00:00 (317s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261024-0517.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261024-0517.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261024-0517.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261024-0517.md
- sources:
  - reddit(arctic): 14 calls, 225 items, 5 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/news: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/pakistan: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/personalfinance: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/CryptoCurrency: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/Bitcoin: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
- scoring: score = velocity(0-40) + engagement(0-40) + freshness(0-20)
  velocity = engagement-per-hour log-scaled (Reddit: (upvotes+2*comments)/age_h; YouTube: views/age_h)
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-10-25T05:39:10+00:00 (285s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261025-0534.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261025-0534.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261025-0534.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261025-0534.md
- sources:
  - reddit(arctic): 14 calls, 350 items, 0 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures: none
- scoring: score = velocity(0-40) + engagement(0-40) + freshness(0-20)
  velocity = engagement-per-hour log-scaled (Reddit: (upvotes+2*comments)/age_h; YouTube: views/age_h)
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-10-26T05:46:28+00:00 (279s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261026-0541.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261026-0541.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261026-0541.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261026-0541.md
- sources:
  - reddit(arctic): 14 calls, 350 items, 0 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures: none
- scoring: score = velocity(0-40) + engagement(0-40) + freshness(0-20)
  velocity = engagement-per-hour log-scaled (Reddit: (upvotes+2*comments)/age_h; YouTube: views/age_h)
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-10-27T05:57:51+00:00 (298s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261027-0553.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261027-0553.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261027-0553.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261027-0553.md
- sources:
  - reddit(arctic): 14 calls, 350 items, 0 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures: none
- scoring: score = velocity(0-40) + engagement(0-40) + freshness(0-20)
  velocity = engagement-per-hour log-scaled (Reddit: (upvotes+2*comments)/age_h; YouTube: views/age_h)
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-10-28T06:35:57+00:00 (218s) — niches: health, news, finance, history
- decoded: health=0 blog + 5 videos, news=0 blog + 5 videos, finance=0 blog + 5 videos, history=0 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261028-0632.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261028-0632.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261028-0632.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261028-0632.md
- sources:
  - reddit(arctic): 14 calls, 0 items, 14 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/Health: 500 Server Error: Internal Server Error for url: https://arctic-shift.photon-reddit.com/api/posts/se
  - reddit(arctic): r/loseit: 500 Server Error: Internal Server Error for url: https://arctic-shift.photon-reddit.com/api/posts/se
  - reddit(arctic): r/nutrition: 500 Server Error: Internal Server Error for url: https://arctic-shift.photon-reddit.com/api/posts/se
  - reddit(arctic): r/AskDocs: 500 Server Error: Internal Server Error for url: https://arctic-shift.photon-reddit.com/api/posts/se
  - reddit(arctic): r/worldnews: 500 Server Error: Internal Server Error for url: https://arctic-shift.photon-reddit.com/api/posts/se
  - reddit(arctic): r/news: 500 Server Error: Internal Server Error for url: https://arctic-shift.photon-reddit.com/api/posts/se
  - reddit(arctic): r/pakistan: 500 Server Error: Internal Server Error for url: https://arctic-shift.photon-reddit.com/api/posts/se
  - reddit(arctic): r/personalfinance: 500 Server Error: Internal Server Error for url: https://arctic-shift.photon-reddit.com/api/posts/se
  - reddit(arctic): r/CryptoCurrency: 500 Server Error: Internal Server Error for url: https://arctic-shift.photon-reddit.com/api/posts/se
  - reddit(arctic): r/stocks: 500 Server Error: Internal Server Error for url: https://arctic-shift.photon-reddit.com/api/posts/se
  - reddit(arctic): r/Bitcoin: 500 Server Error: Internal Server Error for url: https://arctic-shift.photon-reddit.com/api/posts/se
  - reddit(arctic): r/history: 500 Server Error: Internal Server Error for url: https://arctic-shift.photon-reddit.com/api/posts/se
  - reddit(arctic): r/AskHistorians: 500 Server Error: Internal Server Error for url: https://arctic-shift.photon-reddit.com/api/posts/se
  - reddit(arctic): r/historymemes: 500 Server Error: Internal Server Error for url: https://arctic-shift.photon-reddit.com/api/posts/se
- scoring: score = velocity(0-40) + engagement(0-40) + freshness(0-20)
  velocity = engagement-per-hour log-scaled (Reddit: (upvotes+2*comments)/age_h; YouTube: views/age_h)
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-10-29T06:46:04+00:00 (262s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261029-0641.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261029-0641.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261029-0641.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261029-0641.md
- sources:
  - reddit(arctic): 14 calls, 350 items, 0 failed
  - youtube: 12 calls, 119 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures: none
- scoring: score = velocity(0-40) + engagement(0-40) + freshness(0-20)
  velocity = engagement-per-hour log-scaled (Reddit: (upvotes+2*comments)/age_h; YouTube: views/age_h)
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-10-30T06:47:30+00:00 (285s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261030-0642.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261030-0642.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261030-0642.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261030-0642.md
- sources:
  - reddit(arctic): 14 calls, 350 items, 0 failed
  - youtube: 12 calls, 119 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures: none
- scoring: score = velocity(0-40) + engagement(0-40) + freshness(0-20)
  velocity = engagement-per-hour log-scaled (Reddit: (upvotes+2*comments)/age_h; YouTube: views/age_h)
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-10-31T06:37:44+00:00 (285s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261031-0633.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261031-0633.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261031-0633.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261031-0633.md
- sources:
  - reddit(arctic): 14 calls, 350 items, 0 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures: none
- scoring: score = velocity(0-40) + engagement(0-40) + freshness(0-20)
  velocity = engagement-per-hour log-scaled (Reddit: (upvotes+2*comments)/age_h; YouTube: views/age_h)
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-01T07:08:31+00:00 (288s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261101-0703.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261101-0703.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261101-0703.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261101-0703.md
- sources:
  - reddit(arctic): 14 calls, 350 items, 0 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures: none
- scoring: score = velocity(0-40) + engagement(0-40) + freshness(0-20)
  velocity = engagement-per-hour log-scaled (Reddit: (upvotes+2*comments)/age_h; YouTube: views/age_h)
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-01T17:42:05+00:00 (23s) — niches: health
- decoded: health=5 blog + 5 videos
- reports: /home/hatch/workspace/viraldesk/trends/reports/health-20261101-1741.md
- sources:
  - reddit(arctic): 4 calls, 100 items, 0 failed
  - youtube: 3 calls, 30 items, 0 failed
  - video_validate: 5 calls, 5 items, 0 failed
- failures: none
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-02T07:09:54+00:00 (300s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261102-0705.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261102-0705.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261102-0705.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261102-0705.md
- sources:
  - reddit(arctic): 14 calls, 350 items, 0 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures: none
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-03T07:33:27+00:00 (294s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261103-0728.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261103-0728.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261103-0728.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261103-0728.md
- sources:
  - reddit(arctic): 14 calls, 350 items, 0 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures: none
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-04T07:15:34+00:00 (295s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261104-0710.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261104-0710.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261104-0710.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261104-0710.md
- sources:
  - reddit(arctic): 14 calls, 350 items, 0 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures: none
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-05T07:42:53+00:00 (300s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261105-0738.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261105-0738.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261105-0738.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261105-0738.md
- sources:
  - reddit(arctic): 14 calls, 325 items, 1 failed
  - youtube: 12 calls, 100 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/worldnews: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-06T07:38:43+00:00 (287s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261106-0734.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261106-0734.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261106-0734.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261106-0734.md
- sources:
  - reddit(arctic): 14 calls, 350 items, 0 failed
  - youtube: 12 calls, 100 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures: none
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-07T06:51:38+00:00 (303s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261107-0646.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261107-0646.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261107-0646.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261107-0646.md
- sources:
  - reddit(arctic): 14 calls, 350 items, 0 failed
  - youtube: 12 calls, 118 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures: none
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-08T06:58:02+00:00 (314s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261108-0652.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261108-0652.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261108-0652.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261108-0652.md
- sources:
  - reddit(arctic): 14 calls, 350 items, 0 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures: none
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-09T07:38:44+00:00 (334s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261109-0733.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261109-0733.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261109-0733.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261109-0733.md
- sources:
  - reddit(arctic): 14 calls, 275 items, 3 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/AskDocs: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/worldnews: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/Bitcoin: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-10T08:02:05+00:00 (301s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261110-0757.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261110-0757.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261110-0757.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261110-0757.md
- sources:
  - reddit(arctic): 14 calls, 300 items, 2 failed
  - youtube: 12 calls, 110 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/personalfinance: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/history: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-11T07:31:55+00:00 (306s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261111-0726.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261111-0726.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261111-0726.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261111-0726.md
- sources:
  - reddit(arctic): 14 calls, 225 items, 5 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/Health: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/news: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/personalfinance: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/stocks: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/Bitcoin: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-12T07:59:44+00:00 (307s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261112-0754.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261112-0754.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261112-0754.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261112-0754.md
- sources:
  - reddit(arctic): 14 calls, 275 items, 3 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/worldnews: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/news: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/history: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-13T07:36:32+00:00 (297s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261113-0731.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261113-0731.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261113-0731.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261113-0731.md
- sources:
  - reddit(arctic): 14 calls, 225 items, 5 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/nutrition: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/worldnews: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/pakistan: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/CryptoCurrency: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/historymemes: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-14T07:21:01+00:00 (266s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261114-0716.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261114-0716.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261114-0716.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261114-0716.md
- sources:
  - reddit(arctic): 14 calls, 275 items, 3 failed
  - youtube: 12 calls, 104 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/nutrition: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/stocks: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/historymemes: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-15T07:31:57+00:00 (291s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261115-0727.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261115-0727.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261115-0727.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261115-0727.md
- sources:
  - reddit(arctic): 14 calls, 325 items, 1 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/CryptoCurrency: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-16T07:37:26+00:00 (279s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261116-0732.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261116-0732.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261116-0732.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261116-0732.md
- sources:
  - reddit(arctic): 14 calls, 300 items, 2 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/loseit: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/historymemes: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-17T08:50:04+00:00 (314s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261117-0844.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261117-0844.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261117-0844.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261117-0844.md
- sources:
  - reddit(arctic): 14 calls, 350 items, 0 failed
  - youtube: 12 calls, 90 items, 0 failed
  - video_validate: 23 calls, 20 items, 3 failed
- failures (degraded gracefully):
  - video_validate: https://v.redd.it/cnltvj1h242i1
  - video_validate: https://v.redd.it/mcx85p88k42i1
  - video_validate: https://v.redd.it/xh7mg2kli22i1
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-18T08:13:09+00:00 (287s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261118-0808.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261118-0808.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261118-0808.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261118-0808.md
- sources:
  - reddit(arctic): 14 calls, 300 items, 2 failed
  - youtube: 12 calls, 106 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/nutrition: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/pakistan: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-19T08:22:59+00:00 (291s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261119-0818.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261119-0818.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261119-0818.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261119-0818.md
- sources:
  - reddit(arctic): 14 calls, 275 items, 3 failed
  - youtube: 12 calls, 110 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/AskDocs: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/CryptoCurrency: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/stocks: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-20T08:03:41+00:00 (327s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261120-0758.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261120-0758.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261120-0758.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261120-0758.md
- sources:
  - reddit(arctic): 14 calls, 350 items, 0 failed
  - youtube: 12 calls, 115 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures: none
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-21T08:00:32+00:00 (308s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261121-0755.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261121-0755.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261121-0755.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261121-0755.md
- sources:
  - reddit(arctic): 14 calls, 350 items, 0 failed
  - youtube: 12 calls, 110 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures: none
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-22T07:45:53+00:00 (304s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261122-0740.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261122-0740.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261122-0740.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261122-0740.md
- sources:
  - reddit(arctic): 14 calls, 300 items, 2 failed
  - youtube: 12 calls, 110 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/AskDocs: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/AskHistorians: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-23T08:36:14+00:00 (313s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261123-0831.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261123-0831.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261123-0831.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261123-0831.md
- sources:
  - reddit(arctic): 14 calls, 350 items, 0 failed
  - youtube: 12 calls, 110 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures: none
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-24T10:42:48+00:00 (306s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261124-1037.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261124-1037.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261124-1037.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261124-1037.md
- sources:
  - reddit(arctic): 14 calls, 275 items, 3 failed
  - youtube: 12 calls, 100 items, 0 failed
  - video_validate: 21 calls, 20 items, 1 failed
- failures (degraded gracefully):
  - reddit(arctic): r/Health: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/personalfinance: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/CryptoCurrency: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - video_validate: https://www.youtube.com/watch?v=hz7ebSkY2_8
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-25T09:32:31+00:00 (264s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261125-0928.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261125-0928.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261125-0928.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261125-0928.md
- sources:
  - reddit(arctic): 14 calls, 325 items, 1 failed
  - youtube: 12 calls, 120 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/loseit: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-26T09:10:52+00:00 (289s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261126-0906.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261126-0906.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261126-0906.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261126-0906.md
- sources:
  - reddit(arctic): 14 calls, 300 items, 2 failed
  - youtube: 12 calls, 110 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/worldnews: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
  - reddit(arctic): r/Bitcoin: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API

## Run 2026-11-27T09:26:40+00:00 (299s) — niches: health, news, finance, history
- decoded: health=5 blog + 5 videos, news=5 blog + 5 videos, finance=5 blog + 5 videos, history=5 blog + 5 videos
- reports: /home/runner/work/viraldesk/viraldesk/trends/reports/health-20261127-0921.md, /home/runner/work/viraldesk/viraldesk/trends/reports/news-20261127-0921.md, /home/runner/work/viraldesk/viraldesk/trends/reports/finance-20261127-0921.md, /home/runner/work/viraldesk/viraldesk/trends/reports/history-20261127-0921.md
- sources:
  - reddit(arctic): 14 calls, 325 items, 1 failed
  - youtube: 12 calls, 90 items, 0 failed
  - video_validate: 20 calls, 20 items, 0 failed
- failures (degraded gracefully):
  - reddit(arctic): r/worldnews: 422 Client Error: Unprocessable Entity for url: https://arctic-shift.photon-reddit.com/api/posts/sea
- scoring (rebalanced 2026-11-01): Reddit = velocity(0-40) + engagement(0-30) + freshness(0-30, 72h decay); YouTube = views-per-day velocity(0-50) + engagement(0-20) + freshness(0-30, 14d decay)
- selection: freshness gate (blog <=24h, news <=12h), 3-day cross-run suppression parsed from recent reports, youngest-first fallback; reports list this run's picks only
- Google Trends: SKIPPED (pytrends broken in env: urllib3 method_whitelist incompatibility; direct API 429 from this IP)
- reddit.com JSON: 403 from here; used Arctic Shift public API
