"""ViralDesk Phase 1 — link fetchers (read-only). Never invent metrics."""
import json
import os
import re
import subprocess
import sys
from urllib.parse import urlparse

IG_ACCOUNT_ID = "17841421963314094"  # @nasimclinic (linked Instagram account)


def _ytdlp_bin():
    """Resolve the yt-dlp executable: prefer the venv's, fall back to PATH."""
    here = os.path.join(os.path.dirname(sys.executable), "yt-dlp")
    return here if os.path.isfile(here) else "yt-dlp"


def _run(cmd, timeout=60):
    """Run a CLI, return (ok, stdout, stderr)."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0, r.stdout, r.stderr[-500:] if r.stderr else ""
    except subprocess.TimeoutExpired:
        return False, "", "timed out"
    except Exception as e:  # noqa: BLE001
        return False, "", str(e)[:200]


def detect_platform(url: str) -> str:
    host = urlparse(url).netloc.lower()
    path = urlparse(url).path.lower()
    if "facebook.com" in host or "fb.watch" in host or "fb.com" in host:
        return "facebook"
    if "instagram.com" in host:
        return "instagram"
    if "youtube.com" in host or "youtu.be" in host:
        return "youtube"
    if "tiktok.com" in host:
        return "tiktok"
    if "t.me" in host or "telegram.me" in host:
        return "telegram"
    if "/share/" in path and "facebook" in url:
        return "facebook"
    return "unknown"


def _base(url, platform):
    return {
        "url": url, "canonical_url": url, "platform": platform,
        "author": None, "post_date": None, "caption": None,
        "views": None, "likes": None, "comments": None, "shares": None,
        "transcript": None, "description": None,
        "fetch_status": "failed", "fetch_error": "",
    }


# ---------------- Facebook ----------------
def fetch_facebook(url: str) -> dict:
    rec = _base(url, "facebook")
    canon = url
    if "/share/" in url:
        ok, out, err = _run(["facebook-cli", "link-sharing", "decode-url", "--url", url])
        if not ok:
            rec["fetch_error"] = f"share-link decode failed: {err}"
            return rec
        try:
            canon = json.loads(out).get("original_url") or ""
        except Exception:  # noqa: BLE001
            canon = ""
        if not canon:
            rec["fetch_error"] = "share link decoded to empty URL"
            return rec
    rec["canonical_url"] = canon
    ok, out, err = _run(["facebook-cli", "post", "read", "--url", canon])
    if not ok:
        rec["fetch_error"] = f"post read failed: {err}"
        return rec
    try:
        data = json.loads(out)
        posts = data.get("posts", [])
        if not posts:
            rec["fetch_error"] = "post read returned no posts"
            return rec
        p = posts[0]
    except Exception as e:  # noqa: BLE001
        rec["fetch_error"] = f"could not parse post read: {e}"
        return rec

    rec["author"] = p.get("owner_name") or p.get("username")
    pc = p.get("post_created_at") or {}
    rec["post_date"] = pc.get("user_local") or pc.get("utc")
    rec["caption"] = p.get("post_caption")
    rec["transcript"] = p.get("video_transcript")
    post_id = p.get("post_id")

    # Reactions -> likes (total). Views/comments/shares are not exposed here; leave null.
    if post_id:
        ok2, out2, err2 = _run(["facebook-cli", "post", "reactions", "read", "--post-id", str(post_id)])
        if ok2:
            try:
                s = json.loads(out2).get("summary", {})
                rec["likes"] = s.get("total_count")
            except Exception:  # noqa: BLE001
                pass
    rec["fetch_status"] = "ok"
    return rec


# ---------------- Instagram ----------------
def fetch_instagram(url: str) -> dict:
    rec = _base(url, "instagram")
    ok, out, err = _run([
        "instagram-cli", "post", "--account-id", IG_ACCOUNT_ID, "--url", url,
    ])
    if not ok:
        rec["fetch_error"] = f"instagram post fetch failed: {err}"
        return rec
    try:
        data = json.loads(out)
        posts = data.get("posts", [])
        if not posts:
            rec["fetch_error"] = "instagram returned no post data"
            return rec
        p = posts[0]
    except Exception as e:  # noqa: BLE001
        rec["fetch_error"] = f"could not parse instagram response: {e}"
        return rec
    rec["author"] = p.get("username") or p.get("author_name")
    pc = p.get("post_created_at") or {}
    rec["post_date"] = pc.get("user_local") or pc.get("utc")
    rec["caption"] = p.get("post_caption")
    # likes/comments may be present; views are not exposed per-post. Never invent.
    if isinstance(p.get("likes"), int):
        rec["likes"] = p["likes"]
    if isinstance(p.get("comments"), int):
        rec["comments"] = p["comments"]
    rec["fetch_status"] = "ok"
    return rec


# ---------------- YouTube (yt-dlp) ----------------
def fetch_youtube(url: str) -> dict:
    rec = _base(url, "youtube")
    ok, out, err = _run(
        [_ytdlp_bin(), "--dump-json", "--no-download", "--no-playlist",
         "--socket-timeout", "60", "--retries", "2", url], timeout=120
    )
    if not ok:
        rec["fetch_error"] = f"yt-dlp metadata failed: {err}"
        return rec
    try:
        m = json.loads(out)
    except Exception as e:  # noqa: BLE001
        rec["fetch_error"] = f"could not parse yt-dlp output: {e}"
        return rec
    rec["author"] = m.get("uploader") or m.get("channel")
    rec["post_date"] = m.get("upload_date")  # YYYYMMDD
    rec["caption"] = m.get("title")
    rec["description"] = (m.get("description") or "")[:2000]
    for k, dst in (("view_count", "views"), ("like_count", "likes"), ("comment_count", "comments")):
        if isinstance(m.get(k), int):
            rec[dst] = m[k]
    # Best-effort transcript: automatic captions only, short timeout.
    ok2, out2, _ = _run(
        [_ytdlp_bin(), "--skip-download", "--write-auto-subs", "--sub-langs", "en.*",
         "--sub-format", "vtt", "--print", "requested_subtitles.en", url],
        timeout=45,
    )
    if ok2 and out2.strip().startswith("{"):
        try:
            subs = json.loads(out2)
            # subs is a dict of lang -> track info; we only note availability
            rec["transcript"] = None  # full text needs a download; description used instead
        except Exception:  # noqa: BLE001
            pass
    rec["fetch_status"] = "ok"
    return rec


# ---------------- Stubs ----------------
def fetch_tiktok(url: str) -> dict:
    rec = _base(url, "tiktok")
    rec["fetch_error"] = (
        "TikTok fetch not supported yet: TikTok offers no free public oEmbed/metadata "
        "endpoint for arbitrary video URLs. To unblock: add a TikTok API key "
        "(TIKTOK_API_KEY in .env) via the TikTok Research/Display API with an approved "
        "app, or run yt-dlp with logged-in browser cookies (fragile). URL saved; "
        "paste metrics manually if needed."
    )
    return rec


def fetch_telegram(url: str) -> dict:
    rec = _base(url, "telegram")
    rec["fetch_error"] = (
        "Telegram fetch not supported yet: reading a channel post needs a Telegram "
        "Bot token (for public channels, get one from @BotFather) or a user API "
        "session. To unblock: set TELEGRAM_BOT_TOKEN in .env (bot must be admin of "
        "the channel, or the channel must be public). URL saved; metrics can be "
        "pasted manually."
    )
    return rec


def fetch_link(url: str) -> dict:
    platform = detect_platform(url)
    fn = {
        "facebook": fetch_facebook,
        "instagram": fetch_instagram,
        "youtube": fetch_youtube,
        "tiktok": fetch_tiktok,
        "telegram": fetch_telegram,
    }.get(platform)
    if not fn:
        rec = _base(url, platform)
        rec["fetch_error"] = f"unsupported platform for URL: {url}"
        return rec
    return fn(url)
