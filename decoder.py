"""ViralDesk Phase 1 — heuristic Viral Decoder.

Deterministic (no LLM calls): extracts hook, format, beat structure, caption
formula and virality drivers from a saved link's caption/transcript/metrics,
then renders a reusable, versioned MASTER PROMPT with [SLOT] placeholders for
the owner's own characters, branding and niche.
"""
import re

# ---------- helpers ----------
def _sentences(text):
    parts = re.split(r"(?<=[.!?…\n])\s+", (text or "").strip())
    return [p.strip() for p in parts if p.strip()]


def _first_n_words(text, n=18):
    return " ".join((text or "").split()[:n])


# ---------- hook ----------
def extract_hook(link):
    cap = (link.get("caption") or "").strip()
    tr = (link.get("transcript") or "").strip()
    if cap:
        s = _sentences(cap)
        hook = s[0] if s else cap[:140]
        return hook[:160]
    if tr:
        return _first_n_words(tr, 18) + "…"
    return "(no caption or transcript captured — hook unknown)"


# ---------- format classification ----------
_FORMATS = [
    ("skit", ["pov", "roleplay", "role play", "me:", "when you", "nobody:", "acting", "character", "skit", "comedy skit"]),
    ("demo / build-in-public", ["i built", "i made", "watch me", "screen", "app", "software", "tool", "here's how i", "let me show"]),
    ("explainer", ["how to", "why ", "myth", "fact", "tips", "explained", "reasons", "what happens", "did you know", "tutorial"]),
    ("reaction", ["react", "reacts", "watching", "wait for it", "wait till", "his reaction", "her reaction"]),
    ("testimonial / review", ["review", "honest", "i tried", "before and after", "results", "rating"]),
    ("listicle", ["top 5", "top 3", "3 ways", "5 ways", "things you", "signs you"]),
    ("hot-take / debate", ["unpopular opinion", "nobody talks about", "stop doing", "you're wrong", "myth vs"]),
    ("motivation", ["mindset", "discipline", "nobody will", "quote", "remember this"]),
]

_BEATS = {
    "skit": [
        "0–3s HOOK: relatable setup line, character already in motion",
        "3–10s ESCALATION: the situation gets worse/funnier, quick cuts",
        "10–20s TWIST/PAYOFF: punchline or ironic reversal",
        "20–30s TAG: callback to the hook + follow CTA",
    ],
    "demo / build-in-public": [
        "0–3s HOOK: bold outcome claim on screen ('I built X in Y hours')",
        "3–10s PROOF: screen recording / live demo, no talking head",
        "10–20s HOW: 2–3 concrete steps shown, not told",
        "20–30s ITERATION: 'change anything by just asking' moment",
        "30–35s CTA: comment trigger ('want the link? comment X')",
    ],
    "explainer": [
        "0–3s HOOK: question or myth stated as fact-on-screen",
        "3–8s STAKES: why the viewer should care (one line)",
        "8–25s CORE: 3 tight points, one visual per point",
        "25–30s PROOF: study/statistic/example on screen",
        "30–35s CTA: direct question + follow prompt",
    ],
    "reaction": [
        "0–3s HOOK: the moment about to happen, teased",
        "3–15s BUILD: original clip plays, reactor visible",
        "15–25s REACTION: genuine response, replay of key second",
        "25–30s TAKE: one-line verdict + comment question",
    ],
    "testimonial / review": [
        "0–3s HOOK: result first ('I lost X in Y days')",
        "3–12s BEFORE: the problem, relatable framing",
        "12–25s JOURNEY: what was tried, honest pros/cons",
        "25–35s VERDICT: would/wouldn't recommend + CTA",
    ],
    "listicle": [
        "0–3s HOOK: number promise ('3 signs of X')",
        "3–25s LIST: one item per 5–7s, numbered on screen",
        "25–30s BONUS: one extra item as retention reward",
        "30–35s CTA: 'save this' + follow",
    ],
    "hot-take / debate": [
        "0–3s HOOK: contrarian statement, no hedging",
        "3–12s CASE: 2 arguments, fast evidence",
        "12–25s NUANCE: the 'but' that makes it credible",
        "25–35s DEBATE CTA: polarizing question in comments",
    ],
    "motivation": [
        "0–3s HOOK: painful truth, one sentence",
        "3–15s STORY: personal or observed anecdote",
        "15–28s REFRAME: the lesson, stated plainly",
        "28–35s CTA: identity statement ('be the person who…')",
    ],
}


def classify_format(link):
    text = f"{link.get('caption') or ''}\n{link.get('transcript') or ''}".lower()
    best, best_hits = "explainer", 0
    for fmt, kws in _FORMATS:
        hits = sum(1 for k in kws if k in text)
        if hits > best_hits:
            best, best_hits = fmt, hits
    return best


# ---------- caption formula ----------
def caption_formula(link):
    cap = (link.get("caption") or "").strip()
    if not cap:
        return "No caption captured — formula unknown."
    lines = [l for l in cap.split("\n") if l.strip()]
    tags = re.findall(r"#\w+", cap)
    emoji = len(re.findall(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", cap))
    ends_q = cap.rstrip().endswith("?")
    parts = []
    parts.append(f"Opens with a {len(lines[0])}-character hook line")
    parts.append(f"{len(lines)} text blocks separated by line breaks")
    parts.append(f"{'Ends with a direct question (comment bait)' if ends_q else 'No closing question — consider adding one'}")
    parts.append(f"{len(tags)} hashtags" + (" (niche + broad mix)" if tags else ""))
    parts.append(f"{'Uses emoji accents' if emoji else 'No emoji — plain text style'}")
    return "; ".join(parts) + "."


# ---------- virality drivers ----------
_VIRAL_SIGNALS = [
    ("free", "price anchor 'FREE' — removes all friction"),
    ("secret", "'secret' framing — insider knowledge appeal"),
    ("mistake", "'mistake' framing — fear of doing it wrong"),
    ("stop", "'stop doing X' — pattern interrupt"),
    ("vs", "versus framing — tribal debate in comments"),
    ("how i", "first-person proof — 'how I did it' credibility"),
    ("in 24 hours", "time-boxed result — speed promise"),
    ("nobody", "'nobody talks about' — contrarian curiosity"),
    ("warning", "'warning' — loss-aversion hook"),
    ("?", "question in caption — comment bait"),
]

def virality_drivers(link):
    text = f"{link.get('caption') or ''}\n{link.get('transcript') or ''}".lower()
    drivers = [label for sig, label in _VIRAL_SIGNALS if sig in text]
    likes = link.get("likes") or 0
    comments = link.get("comments") or 0
    views = link.get("views") or 0
    metrics = []
    if likes:
        metrics.append(f"{likes:,} reactions banked")
    if comments and likes:
        ratio = comments / max(likes, 1)
        if ratio > 0.15:
            metrics.append("high comment-to-like ratio — debate-driven reach")
        elif comments > 0:
            metrics.append(f"{comments:,} comments — conversation signal")
    if views and likes:
        lr = likes / max(views, 1)
        metrics.append(f"{lr:.1%} like-to-view rate")
    elif views:
        metrics.append(f"{views:,} views")
    if not drivers and not metrics:
        drivers.append("drivers unclear from captured data — watch-time pattern likely")
    return drivers + metrics


# ---------- master prompt ----------
MASTER_TEMPLATE = """# MASTER PROMPT — {format_title} (v{version})
Recreate the viral format below with your own characters, topic and branding.
Source: {platform} post by {author} ({post_date}) — {likes_line}

## WHAT MADE THE ORIGINAL WORK
- **Hook (first 3 seconds):** "{hook}"
- **Format:** {format_title}
- **Emotional beat structure:**
{beats}
- **Caption formula:** {caption_formula}
- **Why it likely went viral:** {drivers}

## YOUR VERSION — FILL THE SLOTS
- **Niche:** [NICHE — e.g. urology health, family comedy]
- **Topic:** [TOPIC — one clear subject for this video]
- **Cast:** [CHARACTER_1 — locked reference face], [CHARACTER_2 — locked reference face]
- **Language:** [Urdu voiceover / Roman Urdu on-screen text / English]
- **Branding:** [BRAND NAME], colors [BRAND COLORS], logo upper-left, contact [PHONE] on end card
- **Address block (if local business):** [ADDRESS LINE 1 / ADDRESS LINE 2]

## BUILD RULES
1. Vertical 9:16, 25–40 seconds, 6 scenes max.
2. On-screen text carries every beat — viewer must get it on mute.
3. Scene 1 IS the hook: first 3 seconds decide everything. No intro logos, no greetings.
4. One idea per scene; hard cuts or 0.5s crossfades only.
5. End card (3s): name + qualification + phone + address block. Logo upper-left throughout.
6. Urdu text must be checked block-by-block against the English before export.
7. Phone-safe encode: H.264 baseline, yuv420p, AAC, faststart.

## DELIVERABLES
1. **Shot list** — 6 scenes: visual description + exact on-screen text + duration per scene.
2. **Voiceover script** (if any) — timed to scenes, in [LANGUAGE].
3. **Caption** — follow the source formula: {caption_formula_short}
4. **3 hook variants** — same format, different first-3-second lines, for A/B testing.
5. **Hashtags** — 8–12 real, actually-used tags for [NICHE] (never invent tags).

## QUALITY GATE
Nothing publishes without the owner's explicit YES on the finished video + caption together.
"""


def analyze(link):
    fmt = classify_format(link)
    beats = "\n".join(f"  {i+1}. {b}" for i, b in enumerate(_BEATS[fmt]))
    likes = link.get("likes")
    likes_line = f"{likes:,} reactions" if likes else "metrics unavailable"
    return {
        "hook": extract_hook(link),
        "format": fmt,
        "format_title": fmt.title(),
        "beats": _BEATS[fmt],
        "beats_text": beats,
        "caption_formula": caption_formula(link),
        "drivers": virality_drivers(link),
        "likes_line": likes_line,
    }


def render_master_prompt(link, analysis, version=1):
    cap_formula = analysis["caption_formula"]
    short = cap_formula.split(";")[0] + "."
    return MASTER_TEMPLATE.format(
        format_title=analysis["format_title"],
        version=version,
        platform=(link.get("platform") or "unknown").title(),
        author=link.get("author") or "unknown",
        post_date=link.get("post_date") or "unknown date",
        likes_line=analysis["likes_line"],
        hook=analysis["hook"].replace('"', "'"),
        beats=analysis["beats_text"],
        caption_formula=analysis["caption_formula"],
        drivers="; ".join(analysis["drivers"]),
        caption_formula_short=short,
    )


def decode(link, version=1):
    analysis = analyze(link)
    prompt = render_master_prompt(link, analysis, version)
    title = f"{analysis['format_title']}: {analysis['hook'][:60]}"
    return title, analysis, prompt


# ---------- alternative hooks ("similar hooks" / new angles on the same win) ----------
_HOOK_OPENERS = [
    "Stop scrolling — {h}",
    "{H} …here's what nobody tells you",
    "I tried this for 7 days: {h}",
    "3 reasons {h}",
    "{H} — myth or fact?",
]


def alternative_hooks(link, analysis=None):
    """5 fresh hook lines in the same viral format — new angles on the decoded win.

    Deterministic reframings of the extracted hook using proven opener patterns.
    These are starting angles to adapt, not copy-paste lines.
    """
    analysis = analysis or analyze(link)
    hook = (analysis.get("hook") or "").strip()
    if not hook or hook.startswith("(no caption"):
        topic = (link.get("niche_tags") or "this topic").split(",")[0].strip() or "this topic"
        hook = f"everything you thought you knew about {topic}"
    h = hook[0].lower() + hook[1:] if len(hook) > 1 else hook
    H = hook[0].upper() + hook[1:] if len(hook) > 1 else hook
    out = []
    for tmpl in _HOOK_OPENERS:
        line = tmpl.format(h=h.rstrip(".…!?"), H=H.rstrip(".…!?"))
        if line not in out:
            out.append(line)
    return out[:5]


# ================================================== TOPIC DECODER ======
# Blog-topic decode: the same "why did this win" treatment the video decoder
# gives reels, but for a trending topic -> article. Deterministic, no LLM.
# decode_topic(topic, context) -> (title, analysis, brief_markdown)

_INTENT_RULES = [
    ("health-action", ["symptom", "treatment", "cure", "remedy", "pain",
                       "disease", "dosage", "side effect"]),
    ("commercial", ["best", "top", "review", "vs", "price", "worth it",
                    "cheapest", "buy"]),
    ("news", ["breaking", "news", "update", "announced", "election",
               "today", "live"]),
    ("how-to", ["how to", "how do", "steps", "guide", "tutorial", "tips"]),
]


def _search_intent(topic):
    t = (topic or "").lower()
    for intent, words in _INTENT_RULES:
        if any(w in t for w in words):
            return intent
    if re.match(r"^(what|why|is|are|can|does|do|when)\b", t):
        return "informational"
    return "informational"


def _headline_variants(topic, niche, intent):
    """3 headlines in his voice, shaped by search intent."""
    base = topic.strip().rstrip("?.!")
    low = base.lower()
    if intent == "news":
        return [
            f"{base} — what happened",
            f"Why {low} matters",
            f"What happens next: {low}",
        ]
    if intent == "how-to":
        return [
            f"How to {low} (simple guide)",
            f"{base} — step by step",
            f"{base}: what actually works",
        ]
    if intent == "commercial":
        return [
            f"{base}: honest review",
            f"{base} — worth it?",
            f"{base} vs the alternatives",
        ]
    # informational / health-action: his proven question + myth-bust style
    return [
        f"{base}: myth or fact?",
        f"{base} — what you need to know",
        f"{low}: what does it mean for you?",
    ]


def _article_blueprint(topic, intent, niche):
    take_line = {
        "health": "Maaz's take — doctor's credential as the trust anchor "
                  "(YMYL)",
        "finance": "Analyst's take — numbers over hype, no financial advice, "
                   "educational framing",
        "news": "Why it matters — the context behind the headline",
        "history": "The deeper story — what the textbooks skip",
    }.get(niche, "Expert take — why this matters")
    return [
        "Hook intro (2-3 lines): the question everyone is asking right now",
        "What it actually is — plain-language, no jargon",
        "Why it's trending this week — the trigger event and the numbers",
        "What this means for you — practical takeaways",
        take_line,
        "FAQ — 3 short answers to the exact questions people search",
        "Soft CTA — follow for the next explainer",
    ]


def decode_topic(topic, context=None):
    """Decode a trending blog topic.

    context: dict with niche, why (numbers-based spike explanation),
             source, source_url, score.
    Returns (title, analysis, brief_markdown).
    """
    context = context or {}
    niche = context.get("niche", "")
    intent = _search_intent(topic)
    if niche == "news" and intent == "informational":
        intent = "news"  # in the news tab, fresh stories are news by default
    headlines = _headline_variants(topic, niche, intent)
    blueprint = _article_blueprint(topic, intent, niche)
    angle = {
        "informational": "Beginner-friendly explainer; own the definition "
                         "before bigger sites do.",
        "how-to": "Step-by-step guide; numbered steps rank and get shared.",
        "commercial": "Honest comparison; disclose no sponsorship, "
                      "keep editorial neutrality.",
        "health-action": "Symptoms/treatment framing with a clear "
                         "'see your doctor' line — educational, never "
                         "diagnosing.",
        "news": "Fast explainer while the story is hot; update the post "
                "as facts develop.",
    }.get(intent, "Beginner-friendly explainer.")
    analysis = {
        "topic": topic,
        "niche": niche,
        "why_trending": context.get("why", ""),
        "search_intent": intent,
        "headlines": headlines,
        "blueprint": blueprint,
        "suggested_angle": angle,
        "score": context.get("score", 0),
        "source": context.get("source", ""),
        "source_url": context.get("source_url", ""),
    }
    bp = "\n".join(f"  {i+1}. {b}" for i, b in enumerate(blueprint))
    hl = "\n".join(f"  {i+1}. {h}" for i, h in enumerate(headlines))
    brief = (
        f"# Topic brief: {topic}\n\n"
        f"Niche: {niche} | Intent: {intent} | "
        f"Trend score: {context.get('score', 0)}/100\n"
        f"Source: {analysis['source']} "
        f"({analysis['source_url'] or 'no direct link'})\n\n"
        f"## Why it's trending\n{analysis['why_trending'] or 'Spiking across monitored sources.'}\n\n"
        f"## 3 headline variants\n{hl}\n\n"
        f"## Article blueprint\n{bp}\n\n"
        f"## Suggested angle\n{angle}\n"
    )
    title = f"Topic [{intent}]: {topic[:60]}"
    return title, analysis, brief
