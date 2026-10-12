"""ViralDesk — Link Inbox + Viral Decoder + Prompt Library + Trend Radar.
Mobile-first: centered layout, big tap targets, minimal screens."""
import os

import streamlit as st

# Streamlit Cloud secrets -> env vars (db.py reads env lazily at connect time).
# Local dev: no secrets file needed; the app simply runs open.
for _k in ("TURSO_URL", "TURSO_TOKEN", "APP_PASSWORD"):
    try:
        if _k in st.secrets and st.secrets[_k]:
            os.environ[_k] = str(st.secrets[_k])
    except Exception:
        pass

import db
import fetchers
import decoder as vd

st.set_page_config(page_title="ViralDesk", page_icon="🎬", layout="centered",
                   initial_sidebar_state="collapsed")


def _auth_gate():
    """Password gate. Open when APP_PASSWORD is not set (local dev)."""
    want = os.environ.get("APP_PASSWORD", "")
    if not want:
        return True
    if st.session_state.get("vd_authed"):
        return True
    st.title("🔒 ViralDesk")
    st.caption("This desk is private — enter the password to continue.")
    pw = st.text_input("Password", type="password", key="vd_pw")
    if st.button("Unlock", key="vd_unlock"):
        if pw == want:
            st.session_state["vd_authed"] = True
            st.session_state.pop("vd_pw", None)
            st.rerun()
        else:
            st.error("Wrong password — try again.")
    return False


if not _auth_gate():
    st.stop()

db.init_db()
db.init_trends_tables()

st.markdown(
    """
    <style>
    html, body, [class*="css"] { font-size: 18px; }
    .stButton > button { min-height: 56px; font-size: 19px; font-weight: 700;
                        width: 100%; border-radius: 12px; }
    .stTextInput > div > div > input, .stSelectbox > div > div { font-size: 18px;
                        min-height: 52px; }
    .stTabs [data-baseweb="tab"] { font-size: 18px; padding: 12px 8px; }
    .metric-badge { display:inline-block; background:#f0f2f6; border-radius:8px;
                    padding:4px 10px; margin:2px 4px 2px 0; font-size:15px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎬 ViralDesk")
st.caption("Link Inbox · Viral Decoder · Prompt Library · Trend Radar")

tab_inbox, tab_decode, tab_lib, tab_radar = st.tabs(
    ["📥 Inbox", "🔍 Decode", "📚 Library", "📡 Radar"])


def _badges(link):
    bits = []
    if link.get("platform"):
        bits.append(f"📌 {link['platform']}")
    if link.get("author"):
        bits.append(f"👤 {link['author']}")
    for k, icon in (("views", "👁"), ("likes", "❤️"), ("comments", "💬"), ("shares", "🔁")):
        v = link.get(k)
        if v is not None:
            bits.append(f"{icon} {v:,}")
    st.markdown(" ".join(f'<span class="metric-badge">{b}</span>' for b in bits),
                unsafe_allow_html=True)


# ---------------- INBOX ----------------
with tab_inbox:
    st.subheader("Add a viral link")
    url = st.text_input("Paste link", placeholder="facebook / instagram / youtube / tiktok / telegram URL",
                        key="inbox_url")
    niche = st.text_input("Niche tags (comma separated)", placeholder="e.g. health, family comedy",
                          key="inbox_niche")
    if st.button("⬇️ Fetch & Save", key="fetch_btn"):
        if not url.strip():
            st.warning("Paste a link first.")
        else:
            with st.spinner("Fetching link data…"):
                rec = fetchers.fetch_link(url.strip())
                rec["niche_tags"] = niche.strip()
                lid = db.save_link(rec)
            if rec["fetch_status"] == "ok":
                st.success(f"Saved #{lid} — {rec['platform']} · {rec.get('author') or 'unknown author'}")
            else:
                st.error(f"Saved #{lid} but fetch failed: {rec['fetch_error'][:220]}")

    with st.expander("✍️ Auto-fetch failed? Paste the text manually"):
        st.caption("Copy the caption + transcript from the post and paste here — the decode works the same.")
        m_author = st.text_input("Author / page name (optional)", key="manual_author")
        m_caption = st.text_area("Caption / title", key="manual_caption", height=100)
        m_transcript = st.text_area("Transcript / post text (optional)", key="manual_transcript", height=140)
        if st.button("💾 Save with manual text", key="manual_save_btn"):
            if not url.strip():
                st.warning("Paste the link above first.")
            elif not (m_caption.strip() or m_transcript.strip()):
                st.warning("Paste at least the caption or the transcript.")
            else:
                rec = fetchers.manual_record(url.strip(), m_author, m_caption, m_transcript)
                rec["niche_tags"] = niche.strip()
                lid = db.save_link(rec)
                st.success(f"Saved #{lid} — {rec['platform']} · manual text, ready to decode.")

    st.divider()
    st.subheader("Saved links")
    q = st.text_input("🔎 Search", placeholder="search url, caption, author, niche…", key="inbox_q")
    for link in db.list_links(search=q.strip()):
        status = "✅" if link["fetch_status"] == "ok" else "⚠️"
        with st.expander(f"{status} #{link['id']} · {link['platform']} · {(link.get('author') or '—')[:28]}"):
            _badges(link)
            st.caption(f"{link['url'][:90]}")
            if link.get("post_date"):
                st.caption(f"📅 {link['post_date']}")
            if link.get("caption"):
                st.write(link["caption"][:300] + ("…" if len(link["caption"]) > 300 else ""))
            if link.get("transcript"):
                st.caption("📝 transcript captured (" + str(len(link["transcript"])) + " chars)")
            if link.get("niche_tags"):
                st.caption(f"🏷️ {link['niche_tags']}")
            if link["fetch_status"] != "ok":
                st.warning("Fetch failed: " + (link.get("fetch_error") or "")[:300])


# ---------------- DECODE ----------------
with tab_decode:
    st.subheader("Decode a link into a master prompt")
    links = db.list_links()
    ok_links = [l for l in links if l["fetch_status"] == "ok"]
    if not ok_links:
        st.info("No decodable links yet — paste a link in the Inbox tab (or use the manual-text option there).")
    else:
        choice = st.selectbox(
            "Choose link",
            options=[l["id"] for l in ok_links],
            format_func=lambda i: next(
                f"#{l['id']} · {l['platform']} · {(l.get('author') or '—')[:24]}" for l in ok_links if l["id"] == i),
        )
        link = db.get_link(choice)
        _badges(link)
        if st.button("🧠 Decode → Master Prompt", key="decode_btn"):
            with st.spinner("Analyzing viral pattern…"):
                vers = db.prompt_versions(choice)
                title, analysis, prompt = vd.decode(link, version=len(vers) + 1)
                st.session_state["last_decode"] = (choice, title, analysis, prompt)
        if st.session_state.get("last_decode") and st.session_state["last_decode"][0] == choice:
            _, title, analysis, prompt = st.session_state["last_decode"]
            st.markdown(f"**Format:** {analysis['format_title']}")
            st.markdown(f"**🎣 Hook (first 3s):** {analysis['hook']}")
            with st.expander("🎣 Alternative hooks — similar angles on this win"):
                for i, ah in enumerate(vd.alternative_hooks(link, analysis), 1):
                    st.write(f"{i}. {ah}")
            with st.expander("📐 Beat structure"):
                for b in analysis["beats"]:
                    st.write("• " + b)
            with st.expander("✍️ Caption formula"):
                st.write(analysis["caption_formula"])
            with st.expander("🚀 Why it likely went viral"):
                for d in analysis["drivers"]:
                    st.write("• " + d)
            st.subheader("Master prompt")
            st.code(prompt, language="markdown")
            if st.button("💾 Save to library", key="save_prompt_btn"):
                pid = db.save_prompt(choice, title, analysis, prompt)
                st.success(f"Saved to library (prompt #{pid}, v{len(db.prompt_versions(choice))}).")
                st.session_state.pop("last_decode", None)


# ---------------- LIBRARY ----------------
with tab_lib:
    st.subheader("Master prompt library")
    prompts = db.list_prompts()
    if not prompts:
        st.info("Library is empty — decode a link first.")
    # group by link
    seen = {}
    for p in prompts:
        seen.setdefault(p["link_id"], []).append(p)
    for link_id, vers in seen.items():
        first = vers[0]
        with st.expander(f"📌 #{first['link_id']} · {first['link_platform']} · v{first['version']} — {first['title'][:60]}"):
            if len(vers) > 1:
                v = st.selectbox("Version", options=[x["version"] for x in vers],
                                 key=f"ver_{link_id}")
                p = next(x for x in vers if x["version"] == v)
            else:
                p = first
            a = p["analysis"]
            st.markdown(f"**🎣 Hook:** {a['hook']}")
            st.markdown(f"**Format:** {a['format_title']}")
            st.code(p["master_prompt"], language="markdown")
            st.caption(f"Source: {p['link_url'][:80]} · saved {p['created_at']}")


# ---------------- TREND RADAR (read-only) ----------------
# The radar itself runs on Muse's machine on a schedule and writes to the
# shared DB. This page only reads — it never fetches or decodes.
NICHES = [("health", "🏥 Health"), ("news", "📰 News"),
          ("finance", "💰 Finance"), ("history", "📜 History")]


def _render_blog_item(b):
    a = b.get("analysis") or {}
    with st.expander(f"📈 {b['topic'][:70]} · {b['score']:.0f} pts"):
        if a.get("why_trending"):
            st.write("**Why it's trending:** " + a["why_trending"])
        if a.get("search_intent"):
            st.caption(f"🎯 Search intent: {a['search_intent']}")
        heads = a.get("headlines") or []
        if heads:
            st.markdown("**Headline options:**")
            for h in heads:
                st.write("• " + h)
        bp = a.get("blueprint") or []
        if bp:
            with st.expander("📐 Article blueprint"):
                for i, step in enumerate(bp, 1):
                    st.write(f"{i}. {step}")
        if a.get("suggested_angle"):
            st.caption("💡 " + a["suggested_angle"])
        if b.get("source_url"):
            st.caption(f"🔗 {b['source_url'][:90]}")


def _render_video_item(v):
    a = v.get("analysis") or {}
    title = v.get("decode_title") or v["topic"]
    with st.expander(f"🎥 {title[:70]} · {v['score']:.0f} pts"):
        if a.get("hook"):
            st.markdown(f"**🎣 Hook:** {a['hook']}")
        if a.get("format_title"):
            st.markdown(f"**Format:** {a['format_title']}")
        beats = a.get("beats") or []
        if beats:
            with st.expander("📐 Beat structure"):
                for beat in beats:
                    st.write("• " + beat)
        if a.get("caption_formula"):
            st.caption("✍️ " + str(a["caption_formula"])[:300])
        mp = v.get("master_prompt") or ""
        if mp:
            with st.expander("📜 Master prompt"):
                st.code(mp, language="markdown")
        if v.get("source_url"):
            st.caption(f"🔗 {v['source_url'][:90]}")


with tab_radar:
    st.subheader("📡 Trend Radar")
    st.caption("Fresh trends per niche — decoded and ready to use. "
               "Updates automatically; this page is read-only.")
    niche_tabs = st.tabs([label for _, label in NICHES])
    for (niche, _), ntab in zip(NICHES, niche_tabs):
        with ntab:
            items = db.get_niche_items(niche)
            blogs = [i for i in items if i.get("kind") == "blog_topic"][:5]
            vids = [i for i in items if i.get("kind") == "social_video"][:5]
            if not items:
                st.info("No trends here yet — the radar hasn't delivered for this niche.")
                continue
            st.markdown("**✍️ Blog topics**")
            for b in blogs:
                _render_blog_item(b)
            st.markdown("**🎬 Social videos**")
            for v in vids:
                _render_video_item(v)
