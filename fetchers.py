"""ViralDesk Phase 1 — link fetchers (read-only). Never invent metrics."""
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
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


# ---------------- oEmbed fallback (works on Streamlit Cloud, no keys) ----------------
_OEMBED_ENDPOINTS = {
    "youtube": "https://www.youtube.com/oembed?url=",
    "tiktok": "https://www.tiktok.com/oembed?url=",
}


def _oembed(platform: str, url: str):
    """Best-effort title/author via the platform's public oEmbed endpoint."""
    endpoint = _OEMBED_ENDPOINTS.get(platform)
    if not endpoint:
        return None
    try:
        req = urllib.request.Request(
            endpoint + urllib.parse.quote(url, safe=""),
            headers={"User-Agent": "Mozilla/5.0 (ViralDesk)"},
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8", "ignore"))
    except Exception:  # noqa: BLE001
        return None


def _oembed_fallback(rec: dict, url: str, what_for: str) -> dict:
    """Fill title/author from oEmbed when the primary fetcher can't run."""
    data = _oembed(rec["platform"], url)
    if not data or not data.get("title"):
        return rec
    rec["caption"] = data.get("title")
    rec["author"] = data.get("author_name")
    rec["description"] = (
        "Note: title/author via public oEmbed. Metrics and transcript are "
        f"unavailable here ({what_for}). Paste the caption/transcript manually "
        "in the Inbox for a full decode."
    )
    rec["fetch_status"] = "ok"
    return rec


# ---------------- Facebook ----------------
def fetch_facebook(url: str) -> dict:
    rec = _base(url, "facebook")
    canon = url
    if "/share/" in url:
        ok, out, err = _run(["facebook-cli", "link-sharing", "decode-url", "--url", url])
        if not ok:
            rec["fetch_error"] = ("facebook-cli not available on this host. "
                                  "Paste the caption/transcript manually in the Inbox for a full decode.")
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
        rec["fetch_error"] = ("facebook-cli not available on this host. "
                              "Paste the caption/transcript manually in the Inbox for a full decode.")
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
        rec["fetch_error"] = ("instagram-cli not available on this host. "
                              "Paste the caption/transcript manually in the Inbox for a full decode.")
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
        # yt-dlp missing/blocked (e.g. Streamlit Cloud) -> oEmbed fallback
        rec["fetch_error"] = f"yt-dlp metadata failed: {err}"
        return _oembed_fallback(rec, url, "yt-dlp is unavailable on this host")
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


# ---------------- TikTok (oEmbed; metrics need an API key) ----------------
def fetch_tiktok(url: str) -> dict:
    rec = _base(url, "tiktok")
    rec = _oembed_fallback(rec, url, "TikTok offers no free metrics endpoint")
    if rec["fetch_status"] == "ok":
        return rec
    rec["fetch_error"] = (
        "TikTok title lookup failed and metrics need a TikTok API key "
        "(TIKTOK_API_KEY in .env) via the TikTok Research/Display API with an "
        "approved app. URL saved; paste the caption/transcript manually in the "
        "Inbox for a full decode."
    )
    return rec


# ---------------- Telegram (stub: needs a bot token) ----------------
def fetch_telegram(url: str) -> dict:
    rec = _base(url, "telegram")
    rec["fetch_error"] = (
        "Telegram auto-fetch needs a bot token (TELEGRAM_BOT_TOKEN) even for public "
        "channels. URL saved; paste the post text manually in the Inbox for a full decode."
    )
    return rec


def manual_record(url: str, author: str = "", caption: str = "", transcript: str = "") -> dict:
    """Build a fetch_ok record from user-pasted text (used by the Inbox manual path)."""
    rec = _base(url.strip(), detect_platform(url.strip()))
    rec["author"] = author.strip() or None
    rec["caption"] = caption.strip() or None
    rec["transcript"] = transcript.strip() or None
    rec["description"] = "Text pasted manually in the Inbox."
    rec["fetch_status"] = "ok"
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
