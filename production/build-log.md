# ViralDesk Phase 3 — build log (overnight 2026-10-12)

## What was built
`~/workspace/viraldesk/production/` — pluggable production engine.

- `engines.yaml` — engine registry. Swap engines with `default_engine:` or
  `produce.py --engine <name>`. **No code changes needed** (locked requirement).
- `branding.yaml` — locked branding: name, qualification, phone 0317 7788426,
  exact address block, logo path, locked character refs, colors, overlay layout
  rules. Injected automatically into every generation; never hardcoded in prompts.
- `engine_base.py` — `ProductionEngine` interface (`validate_config`,
  `dry_run`, `generate`), `ProductionJob` (REFUSES to build with empty
  `character_refs` — locked rule enforced in code), `FinalVideo`,
  `verify_output()` — ffprobe + moov/mdat faststart check against the
  non-negotiable output contract (1080x1920, H.264 baseline, yuv420p, AAC,
  faststart, <25MB).
- `produce.py` — CLI: `--list-engines`, `--validate`, `--dry-run`, `--engine`.
- `engines/stills.py` — **WORKING**: keyframes (agent-generated, locked ref
  attached to every call) -> PIL branding (logo upper-left from exact file,
  presenter photo+name upper-right, on-screen text lower-third) -> Ken Burns
  (ffmpeg zoompan, 4 motion types) -> AI voiceover (tts CLI, per-scene;
  pre-recorded owner VO wins when `voiceover_file` set; TTS failure degrades
  to silent-but-captioned instead of crashing the run) -> end card
  (PIL-designed: logo, CTA, name+qualification, phone, address) -> concat ->
  phone-safe encode -> ffprobe verification.
- `engines/fal.py`, `engines/replicate.py`, `engines/kling.py` — **code-complete,
  KEY-GATED, UNTESTED**. Read keys ONLY from `~/workspace/viraldesk/.env`
  (never logged; `dry_run()` redacts). `dry_run()` builds the exact request
  payload that WOULD be sent, without sending. `generate()` raises
  `EngineNotAvailable` when the key is missing (it is, tonight) — not one
  network call was attempted, not one cent spent.
- `engines/phase2_preview.py` — pending adapter slot; auto-activates when
  `../previews/pipeline.py` lands (sibling Phase 2 build).
- `.env.example` — extended with `FAL_API_KEY`, `REPLICATE_API_TOKEN`,
  `KLING_ACCESS_KEY`, `KLING_SECRET_KEY` (placeholders only).
- `jobs/job-muse-ai-reel-v1.json` — test job derived from master prompt
  id 1 (v1, Demo / Build-In-Public, 5 beats + end card).
- `README.md` — operator docs + morning decision list.

## Test run (stills engine, master prompt 1 v1) — PASSED
- Final: `finals/viraldesk_p1_v1_stills.mp4` (35.0s, 17.5MB) + caption .txt
- ffprobe verification: ALL 8 CHECKS PASSED (H.264, 1080x1920, yuv420p,
  Constrained Baseline, AAC, faststart moov-first, <25MB, duration OK)
- 5 keyframes generated via media pipeline, locked character ref
  (`maaz-face-reference.png`) attached to every call. Spot-checked 3 frames:
  logo upper-left (exact file), presenter photo + "Dr. Maaz Shahid /
  MBBS, MS (Urology)" upper-right on scene 1, on-screen text lower-third
  readable on all scenes, end card with name/qualification/phone 0317 7788426
  + both address lines.
- TTS: **Urdu (`--language ur`) failed twice** — backend returned truncated/
  empty audio (576 bytes) after 3 internal retries each time. English TTS
  verified working (3.1s, 25KB). Same flakiness as the UTI work.
  Decision: test build uses English voiceover + English on-screen text
  (coherent demo; master prompt allows English). Engine keeps full Urdu
  support + per-scene owner-VO override for real productions. Engine also
  hardened: TTS failure now degrades to silent-but-captioned instead of
  crashing the run.

## Per-engine status
| engine | status | tested |
|---|---|---|
| stills | working | end-to-end tonight (see below) |
| phase2_preview | pending | no (waits on sibling) |
| fal | key-gated | dry-run only (payload construction validated, never sent) |
| replicate | key-gated | dry-run only |
| kling | key-gated | dry-run only |

## Measured timings
- Keyframe generation (5x, media pipeline): ~2.5 min
- Stills engine wall-clock (6 scenes: 6x TTS + 6x Ken Burns + assembly + encode): 200s (~3.3 min)
- Total: job spec -> verified final MP4 in ~6 min, ~$0 (no paid APIs)

## Morning needs from Maaz (to unlock true AI video)
1. **Pick one engine**: `fal` recommended (one key, many models, prepaid credits
   valid 365 days, failed gens not billed) vs `replicate` vs `kling` (needs a
   separate Kling Open Platform account + prepaid package from ~$9.80 — a
   consumer subscription does NOT unlock the API).
2. **API key** -> paste into `~/workspace/viraldesk/.env` (NEVER chat).
3. **Public URL for the locked character ref** (`CHARACTER_REF_URL` in
   `engines.yaml`) — API engines can't read files off this machine.
4. **Budget per finished ~35s video** (Oct 2026 list prices, 6 scenes x 5s clips;
   verify live before spending — retakes multiply it):
   Kling 3.0 Std silent ~$2.50 (audio ~$3.80) · Veo 3.1 Fast silent ~$3.00
   (audio ~$4.50–6.00) · Veo 3.1 Std audio ~$12.00 · Replicate Kling Omni ~$5.00.
   NOTE: first paid run must verify the model id in the adapter against the
   provider's live docs — all three adapters are marked UNTESTED.
