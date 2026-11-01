# Trend Radar staleness fix — 2026-11-01

Approved by Maaz in chat ("Fix", 2026-11-01) after he spotted that the
daily WhatsApp digest kept repeating the same topics for days.

## The problem (verified)

- The health item "America low key easier to lose weight than
  Italy/Southern Europe" ("245 upvotes, 47 comments in ~8h") topped
  EVERY health report from 2026-10-26 to 2026-11-01 with frozen counts.
- The same evergreen weight-loss transformation videos (19.0M / 17.9M
  lifetime views) recurred daily.
- Reports had also ballooned: `health-20261101-0703.md` lists
  "Blog topics (100)" / "Social videos (100)" — the writer re-ranked
  the niche's entire decoded history, even duplicating one video
  title at #1 and #5 of the same report.

## What changed

### `trend_radar.py`

1. **Hard freshness gate** — new `_select_blog_topics()`: tier 1 =
   posts with `age_h <= 24` (news niche `<= 12`, from
   `news_freshness_gate_hours`) that are not suppressed, in score
   order. Fallback fills any shortfall with the **youngest** remaining
   posts regardless of score — the only path by which a gated-out or
   recently-shown post can return. Because the fallback is strictly
   youngest-first, a post older than 72h is picked only once every
   younger alternative has been used (code comment says so).
2. **Cross-run suppression** — new `load_recently_shown()` /
   `_is_suppressed()` / `_recent_report_paths()`: before selecting,
   the radar parses the previous 3 days' report files for the niche
   (3 most recent distinct filename dates before today) and collects
   the first 5 `### N. <title>` entries under `## Blog topics` and
   `## Social videos` — i.e. exactly what the digest showed. Keys are
   normalised with the existing `_norm_key()`; near-duplicate titles
   (difflib ratio > 0.9) also count as shown. Blog rows now carry
   `_age_h`; video candidates are re-ordered by new
   `_rank_video_candidates()` (fresh + unseen → older unseen →
   youngest of the recently-shown) before URL validation.
3. **Rebalanced Reddit score** — `score_reddit_post()`: velocity 40
   (unchanged) + engagement **30** (was 40, log scale kept) +
   freshness **30** (was 20) decaying over **72h** (was 168h).
   Total stays 0–100, tuple shape unchanged.
4. **YouTube scoring** — `score_youtube_video()`: led by
   **views-per-day** (velocity 50, log-scaled) instead of raw lifetime
   views; engagement (lifetime views) cut to 20; freshness 30 with a
   14-day decay; unknown age keeps the neutral treatment (freshness
   15, effective age 72h). Videos with a known age ≤ 14 days are
   preferred via the candidate ranking above. URL validation
   (oEmbed) untouched.
5. **Companion fix (necessary)** — `write_niche_report(...,
   trend_ids)` now lists **this run's picks only**;
   `decode_and_store()` returns the run's trend IDs and `main()`
   passes them through (also for the console TOP PICKS). Previously
   the report re-ranked all decoded history by score, so the digest —
   which reads the top of the newest report — would have kept
   repeating all-time high scorers even with perfect selection
   rotation. Per-item report format is unchanged.

### `trends.yaml` (settings)

- `blog_freshness_gate_hours: 24`, `news_freshness_gate_hours: 12`
- `suppression_days: 3`
- `video_fresh_days: 14`

## Suppression mechanism + why it survives GitHub Actions

Chosen: **parse the previous days' committed report files** — not a
separate seen-store. `.github/workflows/radar.yml` checks out the
repo fresh on every run and commits back **only** `trends/reports/`
and `trends/run-log.md` (`git add trends/reports/ trends/run-log.md`).
Report files are therefore the one piece of state guaranteed to exist
at selection time in Actions; a `trends/seen.json` would be wiped by
each fresh checkout unless the workflow also committed it (changing
the workflow's commit set was unnecessary risk). Locally the same
files exist, so behaviour is identical in both environments.

## Test (evidence)

- `python -m py_compile trend_radar.py` → **OK**; `trends.yaml`
  parses OK.
- Suppression loader unit check (health): loaded 10 unique keys from
  the 2026-10-29/30/31 reports; the frozen blog item, the fibre item,
  and the 3-month / 5-year / Amber Rachdi videos were all confirmed
  present in the suppression set.
- **Live local run** (repo `.venv`, real Arctic Shift + YouTube
  fetches, local sqlite DB): `python trend_radar.py --niche health`
  → exit 0 in ~23s, selected 5 blog + 5 videos, log line:
  "gate <=24h, 10 recently-shown keys suppressed". New report:
  `trends/reports/health-20261101-1741.md` (committed as evidence).

### Before → after (health niche)

Before — `health-20261101-0703.md`, from "Blog topics (100)":

| # | Blog topic | Video |
|---|-----------|-------|
| 1 | America low key easier to lose weight than Italy/Southern Europe (245 upvotes, ~8h — frozen since 26 Oct) | my 3 month weight loss TRANSFORMATION 🔥 (19.0M views) |
| 2 | I'm Realizing That Weight Loss Isn't Equal for Everyone…rant | 5 YEAR WEIGHTLOSS \| my transformation (17.9M views) |
| 3 | If fat is just stored energy, then why is it so hard to get rid of? | Casually Explained: Being Healthy |
| 4 | Just learned that 95% of Americans don't get our recommended amount of fiber… | Amber Rachdi's Stunning Weight Loss Transformation |
| 5 | If you don't lift weights in a high protein calorie deficit you will never lose… | my 3 month weight loss TRANSFORMATION 🔥 (duplicate of #1!) |

After — `health-20261101-1741.md`, "Blog topics (5)" / "Social videos (5)":

| # | Blog topic | Video |
|---|-----------|-------|
| 1 | Are walnuts the proven king of nuts over cashews, almonds, etc.? (9 upvotes, 23 comments, ~4h old) | INSANE Weight Loss Transformation 🔥 \| @down.with.del |
| 2 | I cannot lose weight to save my life. (~6h old) | One Health Hack From Every Type Of Doctor |
| 3 | Weight loss after "cheat" day (~5h old) | 3 Month Weight Loss Transformation 😳 |
| 4 | On a deficit and lifting 6 times a week. Staying at same weight? (~7h old) | 30kg Weight Loss Transformation |
| 5 | Am I going through body composition? (~6h old) | MY WEIGHT LOSS JOURNEY \| How I Transformed My Life In 6 Months |

All five "before" blog items and all four distinct "before" videos
are **absent** from the new report (string-checked). No item recurred
via the fallback path: every new blog pick is 4–7h old (inside the
24h gate), and the new videos won on views-per-day velocity
(scores 82.8–84.9).

## Commit / push

- Fix commit: `1d75595ec0ec512110de7df39b25f9249dfcf56b`
  (trend_radar.py, trends.yaml, trends/run-log.md, test report).
- This report is committed separately so it can cite that hash.
- Push: see git output at delivery time (both commits pushed together).

## Honest limits

- **Arctic Shift counts are archive snapshots** and still don't
  update; the fix rotates *selection*, it cannot refresh a frozen
  count. A genuinely still-trending post that returns via fallback
  may show the same "why it's spiking" numbers as before.
- **Fresh picks are younger but smaller**: gate-first selection
  surfaces early-stage posts (today's blog picks have 0–9 upvotes so
  far). On quiet days the digest will be thinner by design — that
  trade-off was stated when the fix was approved.
- Health niche tested live; news/finance/history share the same code
  path (news uses its 12h gate) but were not separately run locally.
  The next scheduled Actions run (all niches) is the full proof.
- Local test wrote to the local sqlite DB only (no TURSO env in the
  shell), so the app's cloud DB was not touched by the test.
