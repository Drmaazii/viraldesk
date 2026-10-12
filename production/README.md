# ViralDesk Production — Phase 3 (Pluggable Production Engine)

Takes an approved master prompt (as a job spec in `jobs/`) and produces the
finished vertical MP4 + caption. Engines are **pluggable via `engines.yaml` —
no code changes needed to swap them.**

## Quick start

```bash
cd ~/workspace/viraldesk/production
python3 produce.py --list-engines
python3 produce.py --job jobs/job-muse-ai-reel-v1.json --engine stills --dry-run
python3 produce.py --job jobs/job-muse-ai-reel-v1.json --engine stills
```

## Engine status (2026-10-12, overnight build)

| Engine | Status | What it does | Needs from Maaz |
|---|---|---|---|
| `stills` | **WORKING** | Keyframes + Ken Burns motion + AI voiceover + burned-in captions + branding. No AI video-gen needed. | Nothing — runs today |
| `phase2_preview` | pending | Adapter slot for the Phase 2 Preview Studio pipeline (`../previews/pipeline.py`). Auto-activates when it lands. | Nothing |
| `fal` | key-gated (UNTESTED) | fal.ai aggregator → Veo / Kling / Wan via one key. Code-complete, dry-run validated, never sent (no key). | `FAL_API_KEY` + decision on model |
| `replicate` | key-gated (UNTESTED) | Replicate hosted video models. Code-complete, dry-run validated, never sent. | `REPLICATE_API_TOKEN` + `owner/model:version` |
| `kling` | key-gated (UNTESTED) | Kling direct API. Code-complete, dry-run validated, never sent. | Kling Open Platform account + prepaid package + `KLING_ACCESS_KEY`/`KLING_SECRET_KEY` |
| `comfyui` | blocked (slot only) | Self-hosted ComfyUI + Wan 2.2 on cloud GPU (master-spec Option A). | Cloud GPU rental (~$0.50–2.00/hr); no GPU here or on his laptop |

**Honest note:** AI video generation is region-blocked on this machine and there
is no GPU anywhere in the loop, so the three API adapters are code-complete
stubs with dry-run validation only. They will not spend a cent until a key
exists in `.env`.

## Output contract (every engine, non-negotiable)

1080×1920 vertical MP4 · H.264 (baseline) + AAC · faststart (moov first) ·
phone-safe (<25 MB). Every output is verified with `ffprobe` + a moov/mdat
atom check before the engine reports success — a failed check raises instead
of delivering a bad file.

## Locked rules enforced in code

- `engine_base.ProductionJob` **refuses** to build if `character_refs` is empty —
  the locked character reference is attached to every generation.
- Branding (name, qualification, phone **0317 7788426**, exact address block,
  logo file, colors) lives in `branding.yaml` — injected automatically, never
  hardcoded in prompts or code.
- The logo is composited from the **exact file** (`logo_transparent.png`) via
  PIL. The image model is instructed to leave the top-left corner empty and
  never draw the logo.
- API keys are read **only** from `~/workspace/viraldesk/.env` (see
  `.env.example`). They are never logged — `dry_run()` redacts them.

## Keyframes (stills engine input)

The stills engine takes keyframes as input (`scene.keyframe` paths). They are
generated agent-side via the media pipeline with the locked character ref
attached to every call, then handed to the engine — deterministic assembly
stays separate from the generative step. Prompts used for the test build are
in `jobs/job-muse-ai-reel-v1.json` (`visual` fields).

## Files

- `engines.yaml` — engine registry (swap engines here)
- `branding.yaml` — locked branding (edit values here, no code)
- `engine_base.py` — interface, job dataclasses, `verify_output()` contract check
- `produce.py` — CLI runner
- `engines/stills.py` — working engine
- `engines/fal.py`, `engines/replicate.py`, `engines/kling.py` — key-gated adapters
- `engines/phase2_preview.py` — pending adapter slot for the Phase 2 pipeline
- `jobs/` — job specs (one per master-prompt version)
- `assets/keyframes/` — generated keyframes for the test build
- `finals/` — finished MP4s + caption .txt files
- `build-log.md` — overnight build record (timings, what is key-gated, morning needs)

## Morning decisions needed (for true AI video)

1. **Pick one engine**: `fal` (recommended — one key, many models, prepaid, failed
   gens not billed) vs `replicate` vs `kling` (needs separate Open Platform account).
2. **Provide the API key** → paste into `~/workspace/viraldesk/.env` (never chat).
3. **Host the character reference publicly** — API engines need the locked face
   as a public URL (`CHARACTER_REF_URL` in `engines.yaml`), not a local file.
4. **Budget per finished 35s video** (Oct 2026 list prices, 6 scenes × 5s clips —
   verify live before spending; retakes multiply this):
   - Kling 3.0 Standard (silent): **~$2.50** · with audio ~$3.80
   - Veo 3.1 Fast (silent): **~$3.00** · with native audio ~$4.50–6.00
   - Veo 3.1 Standard (audio): **~$12.00**
   - Replicate Kling v3 Omni: **~$5.00** silent
