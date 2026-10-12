#!/usr/bin/env python3
"""ViralDesk Production runner (Phase 3).

Usage:
  python produce.py --list-engines
  python produce.py --job jobs/job-muse-ai-reel-v1.json --engine stills
  python produce.py --job jobs/job-muse-ai-reel-v1.json --engine fal --dry-run
  python produce.py --job jobs/job-muse-ai-reel-v1.json --engine stills --validate

Engines are chosen in engines.yaml (default_engine) or via --engine.
No code changes are ever needed to swap engines.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine_base import (  # noqa: E402
    ProductionJob,
    Scene,
    get_engine,
    list_engines,
    load_branding,
    load_registry,
)

PROD_DIR = Path(__file__).resolve().parent


def load_job(path: Path, branding: dict, engine_name: str) -> ProductionJob:
    spec = json.loads(path.read_text(encoding="utf-8"))
    scenes = [Scene(**s) for s in spec["scenes"]]
    # resolve keyframe paths relative to the job file's dir (or absolute)
    jobdir = path.parent
    for s in scenes:
        if s.keyframe and not os.path.isabs(s.keyframe):
            cand = jobdir / s.keyframe
            alt = PROD_DIR / s.keyframe
            s.keyframe = str(cand if cand.exists() else alt)
        if s.voiceover_file and not os.path.isabs(s.voiceover_file):
            cand = jobdir / s.voiceover_file
            if cand.exists():
                s.voiceover_file = str(cand)
    refs = [os.path.expanduser(p) for p in spec.get(
        "character_refs", branding.get("character_refs", []))]
    return ProductionJob(
        prompt_id=spec.get("prompt_id", 0),
        prompt_version=spec.get("prompt_version", 1),
        title=spec.get("title", path.stem),
        scenes=scenes,
        character_refs=refs,          # locked refs — enforced non-empty by the dataclass
        branding=branding,
        output_dir=str(PROD_DIR / spec.get("output_dir", "finals")),
        end_card=spec.get("end_card", {}),
        caption=spec.get("caption", ""),
        engine=engine_name,
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="ViralDesk Production runner")
    ap.add_argument("--job", help="job spec JSON (jobs/*.json)")
    ap.add_argument("--engine", help="engine name (default: engines.yaml default_engine)")
    ap.add_argument("--list-engines", action="store_true")
    ap.add_argument("--validate", action="store_true", help="only validate the engine config")
    ap.add_argument("--dry-run", action="store_true", help="print the execution plan, run nothing")
    args = ap.parse_args()

    registry = load_registry()
    branding = load_branding()

    if args.list_engines or (not args.job and not args.list_engines):
        print("Registered production engines:")
        for e in list_engines(registry):
            print(f"  - {e['name']:15s} [{e['status']:10s}] {e['description']}")
        return 0

    engine_name = args.engine or registry.get("default_engine", "stills")
    engine = get_engine(engine_name, registry)
    print(f"Engine: {engine.name}  status={engine.status}")

    problems = engine.validate_config()
    if problems:
        print("Config problems:")
        for p in problems:
            print(f"  ! {p}")
    if args.validate:
        return 0 if not problems else 1

    job = load_job(Path(args.job), branding, engine_name)
    print(f"Job: {job.title}  (prompt {job.prompt_id} v{job.prompt_version}, "
          f"{len(job.scenes)} scenes, {len(job.character_refs)} locked character ref(s))")

    if args.dry_run:
        print(json.dumps(engine.dry_run(job), indent=2, ensure_ascii=False))
        return 0

    if problems:
        print("Refusing to generate: fix the config problems above (or pick another engine).")
        return 1

    result = engine.generate(job)
    print("\nFINAL VIDEO")
    print(f"  path:     {result.video_path}")
    print(f"  caption:  {result.caption_path}")
    print(f"  duration: {result.duration_s}s   size: {result.size_bytes / 1048576:.1f} MB")
    print(f"  verified: {result.verified['ok']}  {result.verified['checks']}")
    for n in result.notes:
        print(f"  note: {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
