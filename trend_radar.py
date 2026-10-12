#!/usr/bin/env python3
"""ViralDesk Trend Radar — per niche, per run: 5 trending blog topics +
5 trending social videos, ALL decoded automatically.

Backend only (no UI). Phone UI will render one sub-tab per niche later.

Sources — public endpoints only, NO api keys:
  * Reddit via Arctic Shift public API (posts: title/score/comments/url).
    (reddit.com JSON is 403 from here; old.reddit is blocked.)
  * YouTube search pages parsed from ytInitialData (title/views/url);
    every video URL validated via the oEmbed endpoint — no dead links.
  * Google Trends is NOT used: pytrends is broken in this env
    (urllib3 method_whitelist incompatibility) and the direct Trends API
    returns 429 from this IP. Velocity is measured as engagement-per-hour
    from Reddit/YouTube instead — documented in the run log.

Scoring (transparent, 0-100):
    score = velocity (0-40) + engagement (0-40) + freshness (0-20)
  * velocity:   engagement-per-hour, log-scaled (what's accelerating NOW)
  * engagement: log-scaled upvotes/comments (Reddit) or views (YouTube)
  * freshness:  recency of post/video

Decode:
  * social video -> links table + decoder.decode -> prompts table
    (hook, format, beats, caption formula, master prompt) + trend_decodes row
  * blog topic   -> decoder.decode_topic (why trending, intent, 3 headlines,
    article blueprint, angle) + trend_decodes row

Usage:
    python trend_radar.py --niche all|health|news|finance|history
"""
import argparse
import difflib
import hashlib
import json
import math
import os
import re
import sys
import time
import urllib.parse
from datetime import datetime, timezone

import requests
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db  # noqa: E402
import decoder  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(HERE, "trends.yaml")
CACHE_DIR = os.path.join(HERE, "trends", "cache")
REPORTS_DIR = os.path.join(HERE, "trends", "reports")
RUN_LOG = os.path.join(HERE, "trends", "run-log.md")

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

_last_req_ts = 0.0
_run_stats = {"sources": {}, "failures": []}


def log(msg):
    print(f"[trend-radar] {msg}", flush=True)


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------- cache ----
def _cache_get(key, ttl_hours):
    path = os.path.join(CACHE_DIR, hashlib.sha1(key.encode()).hexdigest() + ".json")
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        if time.time() - payload["ts"] > ttl_hours * 3600:
            return None
        return payload["data"]
    except Exception:
        return None


def _cache_set(key, data):
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, hashlib.sha1(key.encode()).hexdigest() + ".json")
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"ts": time.time(), "data": data}, f)
    except Exception:
        pass


# ------------------------------------------------------- polite fetching ---
def polite_get(url, min_interval=0.0, params=None, headers=None, timeout=20,
               allow_redirects=True):
    global _last_req_ts
    wait = min_interval - (time.time() - _last_req_ts)
    if wait > 0:
        time.sleep(wait)
    h = {"User-Agent": UA}
    if headers:
        h.update(headers)
    r = requests.get(url, params=params, headers=h, timeout=timeout,
                     allow_redirects=allow_redirects)
    _last_req_ts = time.time()
    r.raise_for_status()
    return r


def record_source(name, items=0, failed=False, note=""):
    s = _run_stats["sources"].setdefault(name, {"calls": 0, "items": 0, "failed": 0})
    s["calls"] += 1
    s["items"] += items
    if failed:
        s["failed"] += 1
        _run_stats["failures"].append(f"{name}: {note}")


# ------------------------------------------------------------- db layer ----
def init_db():
    # All tables now live in db.py (Turso-ready: remote when TURSO_URL/TURSO_TOKEN
    # are set, local sqlite otherwise). One call each.
    db.init_db()
    db.init_trends_tables()


def save_trend(row):
    c = db.connect()
    cur = c.execute(
        """INSERT INTO trends
           (topic, niche, kind, source, source_url, score, velocity,
            engagement, freshness, fetched_at, status, created_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (row["topic"], row["niche"], row["kind"], row["source"],
         row.get("source_url", ""), row["score"], row["velocity"],
         row["engagement"], row["freshness"], row["fetched_at"],
         "new", now_iso()),
    )
    tid = cur.lastrowid
    c.commit()
    c.close()
    return tid


def save_decode(trend_id, kind, title, analysis, master_prompt,
                link_id=None, prompt_id=None):
    c = db.connect()
    cur = c.execute(
        """INSERT INTO trend_decodes
           (trend_id, kind, link_id, prompt_id, title, analysis_json,
            master_prompt, created_at)
           VALUES (?,?,?,?,?,?,?,?)""",
        (trend_id, kind, link_id, prompt_id, title,
         json.dumps(analysis, ensure_ascii=False), master_prompt, now_iso()),
    )
    did = cur.lastrowid
    c.execute("UPDATE trends SET status='decoded' WHERE id=?", (trend_id,))
    c.commit()
    c.close()
    return did


def get_niche_items(niche):
    """All decoded items for a niche: blog topics + videos with decodes."""
    return db.get_niche_items(niche)


# ============================================================ SOURCES ======
# ------------------------------------------------- Reddit (Arctic Shift)
ARCTIC = "https://arctic-shift.photon-reddit.com/api/posts/search"


def _norm_reddit_post(p):
    created = p.get("created_utc") or time.time()
    age_h = max(0.5, (time.time() - created) / 3600.0)
    return {
        "title": (p.get("title") or "").strip(),
        "score": p.get("score") or 0,
        "comments": p.get("num_comments") or 0,
        "age_h": age_h,
        "url": p.get("url") or "",
        "permalink_url": "https://www.reddit.com" + (p.get("permalink") or ""),
        "author": p.get("author") or "",
        "subreddit": p.get("subreddit") or "",
        "is_video": bool(p.get("is_video")),
        "selftext": (p.get("selftext") or "")[:500],
    }


def fetch_reddit(subreddits, per_sub, min_interval, timeout, ttl_hours):
    """Recent posts per subreddit via the public Arctic Shift API."""
    out = []
    for sub in subreddits:
        ck = f"arctic:{sub}:{per_sub}"
        cached = _cache_get(ck, ttl_hours)
        if cached is not None:
            out.extend(cached)
            record_source("reddit(arctic)", items=len(cached))
            continue
        try:
            r = polite_get(ARCTIC, min_interval=min_interval,
                           params={"subreddit": sub, "limit": str(per_sub),
                                   "sort": "desc"},
                           timeout=timeout)
            items = [_norm_reddit_post(p)
                     for p in (r.json().get("data") or [])]
            items = [i for i in items if i["title"]]
            _cache_set(ck, items)
            out.extend(items)
            record_source("reddit(arctic)", items=len(items))
        except Exception as e:
            record_source("reddit(arctic)", failed=True,
                          note=f"r/{sub}: {str(e)[:100]}")
            log(f"reddit r/{sub} failed: {e}")
    return out


# ------------------------------------------------------------- YouTube -----
def _extract_yt_initial_data(html):
    marker = "var ytInitialData ="
    i = html.find(marker)
    if i < 0:
        return None
    j = html.find("{", i)
    depth, k = 0, j
    in_str, esc = False, False
    while k < len(html):
        ch = html[k]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(html[j:k + 1])
                    except Exception:
                        return None
        k += 1
    return None


def _parse_views(text):
    if not text:
        return 0
    t = text.replace(" views", "").replace(",", "").strip().upper()
    m = re.match(r"^([\d.]+)\s*([KMB])?$", t)
    if not m:
        return 0
    n, suf = float(m.group(1)), m.group(2)
    return int(n * {"K": 1e3, "M": 1e6, "B": 1e9}.get(suf, 1))


def _parse_age_hours(text):
    if not text:
        return None
    m = re.match(r"(\d+)\s+(second|minute|hour|day|week|month|year)s?\s+ago",
                 text.lower())
    if not m:
        return None
    n, unit = int(m.group(1)), m.group(2)
    return n * {"second": 1/3600, "minute": 1/60, "hour": 1, "day": 24,
                "week": 168, "month": 730, "year": 8760}[unit]


def _yt_search_videos(query, max_results, timeout):
    r = polite_get("https://www.youtube.com/results", min_interval=1.0,
                   params={"search_query": query}, timeout=timeout)
    data = _extract_yt_initial_data(r.text)
    if not data:
        return []
    videos = []
    try:
        sections = (data["contents"]["twoColumnSearchResultsRenderer"]
                    ["primaryContents"]["sectionListRenderer"]["contents"])
        for sec in sections:
            for entry in sec.get("itemSectionRenderer", {}).get("contents", []):
                vr = entry.get("videoRenderer")
                if not vr:
                    continue
                title = "".join(x.get("text", "")
                                for x in vr.get("title", {}).get("runs", []))
                vid = vr.get("videoId", "")
                if not title or not vid:
                    continue
                vc = vr.get("viewCountText", {})
                views = _parse_views(vc.get("simpleText") or
                                     "".join(x.get("text", "")
                                             for x in vc.get("runs", [])))
                pt = (vr.get("publishedTimeText", {}) or {}).get("simpleText")
                owner = "".join(
                    x.get("text", "")
                    for x in vr.get("ownerText", {}).get("runs", []))
                videos.append({
                    "title": title,
                    "url": f"https://www.youtube.com/watch?v={vid}",
                    "video_id": vid,
                    "views": views,
                    "age_h": _parse_age_hours(pt),
                    "channel": owner,
                    "query": query,
                })
                if len(videos) >= max_results:
                    return videos
    except Exception as e:
        log(f"youtube page parse partial failure for '{query}': {e}")
    return videos


def fetch_youtube(queries, results_per_page, timeout, ttl_hours):
    out = []
    for q in queries:
        ck = f"yt_search:{q}"
        vids = _cache_get(ck, ttl_hours)
        if vids is None:
            try:
                vids = _yt_search_videos(q, results_per_page, timeout)
                _cache_set(ck, vids)
            except Exception as e:
                record_source("youtube", failed=True,
                              note=f"'{q}': {str(e)[:100]}")
                log(f"youtube search '{q}' failed: {e}")
                vids = []
        out.extend(vids)
        record_source("youtube", items=len(vids))
    return out


def validate_video_url(url, timeout=15):
    """oEmbed check: 200 + title = real, watchable, public video."""
    try:
        if "youtube.com/watch" in url or "youtu.be/" in url:
            r = polite_get("https://www.youtube.com/oembed",
                           params={"url": url, "format": "json"},
                           timeout=timeout)
            d = r.json()
            return bool(d.get("title")), d.get("title", "")
        if "v.redd.it" in url:
            r = polite_get(url, timeout=timeout, allow_redirects=True)
            ct = r.headers.get("Content-Type", "")
            return ("video" in ct or "octet" in ct), ""
    except Exception:
        pass
    return False, ""


# ================================================== SCORING / SELECT ======
def _eng_velocity(engagement, age_h):
    return engagement / max(age_h or 24, 1.0)


def score_reddit_post(p):
    eng = p["score"] + 2 * p["comments"]
    vel_raw = _eng_velocity(eng, p["age_h"])
    velocity = 40.0 * min(1.0, math.log10(1 + vel_raw) / 4.0)
    engagement = 40.0 * min(1.0, math.log10(1 + eng) / 5.0)
    freshness = 20.0 * max(0.0, 1.0 - p["age_h"] / 168.0)
    total = round(min(100.0, velocity + engagement + freshness), 1)
    return total, round(velocity, 1), round(engagement, 1), round(freshness, 1)


def score_youtube_video(v):
    eng = v["views"]
    age_h = v["age_h"] or 72
    vel_raw = _eng_velocity(eng, age_h)
    velocity = 40.0 * min(1.0, math.log10(1 + vel_raw) / 4.0)
    engagement = 40.0 * min(1.0, math.log10(1 + eng) / 7.0)
    freshness = (20.0 * max(0.0, 1.0 - age_h / 168.0)
                 if v["age_h"] else 10.0)
    total = round(min(100.0, velocity + engagement + freshness), 1)
    return total, round(velocity, 1), round(engagement, 1), round(freshness, 1)


def _norm_key(text):
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def dedupe(rows):
    merged = []
    for r in sorted(rows, key=lambda x: -x["score"]):
        key = _norm_key(r["topic"])
        if len(key) < 4:
            continue
        hit = None
        for m in merged:
            if key == m["_key"] or difflib.SequenceMatcher(
                    None, key, m["_key"]).ratio() > 0.88:
                hit = m
                break
        if hit:
            if r["source"] not in hit["source"]:
                hit["source"] += "+" + r["source"]
            if not hit.get("source_url") and r.get("source_url"):
                hit["source_url"] = r["source_url"]
        else:
            r["_key"] = key
            merged.append(r)
    for m in merged:
        m.pop("_key", None)
    return merged


def _is_video_link(url):
    u = (url or "").lower()
    return ("youtube.com/watch" in u or "youtu.be/" in u
            or "v.redd.it" in u)


def select_niche_items(niche_key, ncfg, settings, ttl_hours):
    """Fetch + score + select 5 blog topics and 5 validated social videos."""
    fetched_at = now_iso()
    timeout = settings["request_timeout"]

    reddit_posts = fetch_reddit(ncfg["subreddits"],
                                settings["reddit_posts_per_sub"],
                                settings["reddit_min_interval_secs"],
                                timeout, ttl_hours)
    yt_videos = fetch_youtube(ncfg["youtube_queries"],
                              settings["youtube_results_per_page"],
                              timeout, ttl_hours)

    # ---- blog topics: top Reddit discussions by engagement velocity ----
    blog_rows = []
    for p in reddit_posts:
        if _is_video_link(p["url"]):
            continue  # video links go to the video pool
        s, v, e, f = score_reddit_post(p)
        age = (f"{p['age_h']:.0f}h" if p["age_h"] < 48
               else f"{p['age_h']/24:.0f}d")
        up, cm = p["score"], p["comments"]
        blog_rows.append({
            "topic": p["title"], "niche": niche_key, "kind": "blog_topic",
            "source": "reddit", "source_url": p["permalink_url"],
            "score": s, "velocity": v, "engagement": e, "freshness": f,
            "fetched_at": fetched_at,
            "_why": (f"{up:,} upvote{'s' if up != 1 else ''}, "
                     f"{cm:,} comment{'s' if cm != 1 else ''} "
                     f"in ~{age} on r/{p['subreddit']}"),
        })
    blog_rows = dedupe(blog_rows)[:settings["blog_topics_per_niche"]]

    # ---- social videos: YouTube (validated) + Reddit video links -------
    vid_rows = []
    for vd in sorted(yt_videos, key=lambda x: -x["views"]):
        s, v, e, f = score_youtube_video(vd)
        vid_rows.append({
            "topic": vd["title"], "niche": niche_key, "kind": "social_video",
            "source": "youtube", "source_url": vd["url"],
            "score": s, "velocity": v, "engagement": e, "freshness": f,
            "fetched_at": fetched_at,
            "_channel": vd.get("channel", ""),
            "_views": vd["views"],
            "_why": f"{vd['views']:,} views" + (
                f" by {vd['channel']}" if vd.get("channel") else ""),
        })
    # Reddit posts that link straight to a video (backup pool)
    for p in reddit_posts:
        if _is_video_link(p["url"]):
            s, v, e, f = score_reddit_post(p)
            vid_rows.append({
                "topic": p["title"], "niche": niche_key, "kind": "social_video",
                "source": "reddit", "source_url": p["url"],
                "score": s, "velocity": v, "engagement": e, "freshness": f,
                "fetched_at": fetched_at,
                "_channel": f"r/{p['subreddit']}",
                "_views": 0,
                "_why": (f"r/{p['subreddit']}: {p['score']:,} "
                         f"upvote{'s' if p['score'] != 1 else ''}, "
                         f"{p['comments']:,} "
                         f"comment{'s' if p['comments'] != 1 else ''}"),
            })
    vid_rows = dedupe(vid_rows)

    # validate: keep only real, watchable URLs (no dead links)
    valid = []
    for row in vid_rows:
        ok, oembed_title = validate_video_url(row["source_url"], timeout)
        if ok:
            if oembed_title and len(row["topic"]) < 10:
                row["topic"] = oembed_title
            valid.append(row)
            record_source("video_validate", items=1)
        else:
            record_source("video_validate", failed=True,
                          note=row["source_url"][:80])
            log(f"dropping dead/unplayable video: {row['source_url'][:80]}")
        if len(valid) >= settings["social_videos_per_niche"]:
            break
    if len(valid) < settings["social_videos_per_niche"]:
        log(f"niche {niche_key}: only {len(valid)} validated videos "
            f"(wanted {settings['social_videos_per_niche']})")
    return blog_rows, valid[:settings["social_videos_per_niche"]]


# ===================================================== DECODE + STORE =====
def decode_and_store(niche_key, blog_rows, vid_rows):
    """Decode everything; store trend rows + decodes. Returns counts."""
    n_blog, n_vid = 0, 0
    for row in blog_rows:
        why = row.pop("_why", "")
        tid = save_trend(row)
        title, analysis, brief = decoder.decode_topic(row["topic"], {
            "niche": niche_key, "why": why, "source": row["source"],
            "source_url": row["source_url"], "score": row["score"]})
        save_decode(tid, "topic", title, analysis, brief)
        n_blog += 1
    for row in vid_rows:
        why = row.pop("_why", "")
        channel = row.pop("_channel", "")
        views = row.pop("_views", 0)
        tid = save_trend(row)
        link = {
            "url": row["source_url"],
            "canonical_url": row["source_url"],
            "platform": "youtube" if "youtube" in row["source"] else "reddit",
            "author": channel,
            "caption": row["topic"],
            "views": views,
            "description": f"Trend Radar pick — {why}",
            "niche_tags": f"{niche_key},trend-radar",
            "fetch_status": "trend",
        }
        link_id = db.save_link(link)
        link["id"] = link_id
        title, analysis, prompt = decoder.decode(link)
        prompt_id = db.save_prompt(link_id, title, analysis, prompt)
        save_decode(tid, "video", title, analysis, prompt,
                    link_id=link_id, prompt_id=prompt_id)
        n_vid += 1
        log(f"decoded video [{row['score']}] {row['topic'][:60]}")
    return n_blog, n_vid


# ============================================================ REPORTS =====
def _fmt_pct(n):
    return f"{n:,.0f}"


def write_niche_report(niche_key, label, run_stamp):
    items = get_niche_items(niche_key)
    blogs = [i for i in items if i["kind"] == "blog_topic"]
    vids = [i for i in items if i["kind"] == "social_video"]
    os.makedirs(REPORTS_DIR, exist_ok=True)
    path = os.path.join(REPORTS_DIR, f"{niche_key}-{run_stamp}.md")
    L = [f"# Trend Radar — {label}", f"_Run: {run_stamp} PKT_\n",
         f"## Blog topics ({len(blogs)})"]
    for i, b in enumerate(blogs, 1):
        a = b["analysis"]
        hl = "\n".join(f"  {j+1}. {h}" for j, h in enumerate(a["headlines"]))
        bp = "\n".join(f"  - {x}" for x in a["blueprint"])
        L += [
            f"\n### {i}. {b['topic']}",
            f"- Score: {b['score']}/100 (velocity {b['velocity']}, "
            f"engagement {b['engagement']}, freshness {b['freshness']})",
            f"- Source: {b['source']} — {b['source_url']}",
            f"- Why it's spiking: {a['why_trending']}",
            f"- Search intent: {a['search_intent']}",
            f"- Headlines:\n{hl}",
            f"- Article blueprint:\n{bp}",
            f"- Suggested angle: {a['suggested_angle']}",
        ]
    L.append(f"\n## Social videos ({len(vids)})")
    for i, v in enumerate(vids, 1):
        a = v["analysis"]
        beats = "\n".join(f"  {j+1}. {x}" for j, x in enumerate(a["beats"]))
        L += [
            f"\n### {i}. {v['topic']}",
            f"- URL: {v['source_url']}",
            f"- Score: {v['score']}/100 | Format: {a['format_title']}",
            f"- Hook: {a['hook']}",
            f"- Beats:\n{beats}",
            f"- Caption formula: {a['caption_formula']}",
            f"- Virality drivers: {'; '.join(a['drivers'])}",
            f"- Master prompt: stored in ViralDesk library "
            f"(prompt #{v['prompt_id']})",
        ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    return path


# ============================================================ RUN LOG =====
def append_run_log(niches, counts, report_paths, elapsed):
    lines = [
        f"\n## Run {now_iso()} ({elapsed:.0f}s) — niches: {', '.join(niches)}",
        "- decoded: " + ", ".join(
            f"{n}={b} blog + {v} videos" for n, (b, v) in counts.items()),
        "- reports: " + ", ".join(report_paths),
        "- sources:",
    ]
    for name, s in _run_stats["sources"].items():
        lines.append(f"  - {name}: {s['calls']} calls, {s['items']} items, "
                     f"{s['failed']} failed")
    if _run_stats["failures"]:
        lines.append("- failures (degraded gracefully):")
        lines.extend(f"  - {f}" for f in _run_stats["failures"][:20])
    else:
        lines.append("- failures: none")
    lines += [
        "- scoring: score = velocity(0-40) + engagement(0-40) + freshness(0-20)",
        "  velocity = engagement-per-hour log-scaled (Reddit: "
        "(upvotes+2*comments)/age_h; YouTube: views/age_h)",
        "- Google Trends: SKIPPED (pytrends broken in env: urllib3 "
        "method_whitelist incompatibility; direct API 429 from this IP)",
        "- reddit.com JSON: 403 from here; used Arctic Shift public API",
    ]
    with open(RUN_LOG, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    log(f"run log: {RUN_LOG}")


# ================================================================= CLI ====
def main():
    ap = argparse.ArgumentParser(description="ViralDesk Trend Radar")
    ap.add_argument("--niche", default="all",
                    choices=["all", "health", "news", "finance", "history"])
    args = ap.parse_args()
    t0 = time.time()

    cfg = load_config()
    settings = cfg["settings"]
    ttl = settings["cache_ttl_hours"]
    niches = list(cfg["niches"].keys()) if args.niche == "all" else [args.niche]

    init_db()
    counts, report_paths = {}, []
    run_stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
    for niche in niches:
        ncfg = cfg["niches"][niche]
        log(f"--- niche: {ncfg['label']} ({niche})")
        blog_rows, vid_rows = select_niche_items(niche, ncfg, settings, ttl)
        log(f"selected: {len(blog_rows)} blog topics, {len(vid_rows)} videos")
        nb, nv = decode_and_store(niche, blog_rows, vid_rows)
        counts[niche] = (nb, nv)
        rp = write_niche_report(niche, ncfg["label"], run_stamp)
        report_paths.append(rp)
        log(f"report: {rp}")

    append_run_log(niches, counts, report_paths, time.time() - t0)

    print("\n================ TOP PICKS ================")
    for niche in niches:
        items = get_niche_items(niche)
        print(f"\n### {cfg['niches'][niche]['label']}")
        for it in [i for i in items if i["kind"] == "blog_topic"][:3]:
            print(f"  [BLOG {it['score']}] {it['topic'][:80]}")
        for it in [i for i in items if i["kind"] == "social_video"][:3]:
            print(f"  [VIDEO {it['score']}] {it['topic'][:80]}")
    total = sum(b + v for b, v in counts.values())
    print(f"\ntotal decoded items: {total}")
    print("done.")


if __name__ == "__main__":
    main()
