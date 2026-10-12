# ViralDesk — Phase 1 (MVP)

All-in-One Viral Content Command Center. **Phase 1 = Link Inbox + Viral Decoder + versioned master-prompt library.** Phases 2–4 (Preview Studio, Production, Publisher) are not built yet.

## Run it

```bash
~/workspace/viraldesk/run.sh
# then open http://localhost:8501
```

First run creates `viraldesk.db` (SQLite) automatically. Python lives in `.venv/`
— nothing was installed system-wide.

## What works now

| Platform | Status | How |
|---|---|---|
| Facebook (posts, reels, share links) | ✅ working | `facebook-cli`: share-link decode → post read → reactions |
| Instagram (posts, reels) | ✅ working | `instagram-cli post --url` (linked @nasimclinic account) — likes/comments where exposed; views not exposed per-post |
| YouTube | ✅ working | `yt-dlp --dump-json` metadata (views/likes/comments/description); transcript best-effort |
| TikTok | ⚠️ stubbed | No free public metadata endpoint. **Unblock:** `TIKTOK_API_KEY` in `.env` (TikTok Research/Display API, approved app) or yt-dlp with logged-in cookies (fragile). Saved with fetch_error explaining this. |
| Telegram | ⚠️ stubbed | **Unblock:** `TELEGRAM_BOT_TOKEN` in `.env` (from @BotFather; bot must be channel admin or channel public). |

**Rule enforced in code:** metrics are never invented. Failed fetches are stored
with `fetch_status='failed'` and a plain-language `fetch_error` naming exactly
what would unblock them.

## The Viral Decoder

Deterministic heuristics (no LLM calls, no API cost):
- **Hook** — first sentence of caption, else first 18 words of transcript
- **Format** — keyword classification (skit, explainer, demo/build-in-public,
  reaction, testimonial, listicle, hot-take, motivation)
- **Beats** — per-format 4–5 beat structure with timing
- **Caption formula** — hook length, block count, question CTA, hashtag/emoji use
- **Why viral** — content signals (FREE, numbers, debate framing…) + metric
  ratios where available
- **Master prompt** — copy-paste template with `[SLOTS]` for niche, topic,
  locked character cast, branding, language; includes build rules (9:16,
  6 scenes, end card, phone-safe encode) and a quality gate. Saved **versioned**
  per link (v1, v2…) in the library.

Upgrade path: if an `OPENAI_API_KEY`/`ANTHROPIC_API_KEY` is later added to
`.env`, the decoder can call it for deeper analysis with the heuristic output
as fallback. Not wired yet — deliberate, to keep Phase 1 dependency-free.

## Files

- `app.py` — Streamlit dashboard (mobile-first)
- `db.py` — SQLite schema + helpers
- `fetchers.py` — platform fetchers + stubs
- `decoder.py` — analysis + master-prompt templates
- `run.sh` — launcher · `requirements.txt` · `.env.example`
