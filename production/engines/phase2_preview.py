"""Phase 2 Preview Studio adapter — PENDING.

This slot lets the Phase 2 Preview Studio pipeline (built overnight into
../previews/) become a swappable production engine the moment it lands —
no code change needed, it is already registered in engines.yaml.

Activation rule: if ../previews/pipeline.py exists and exposes
`run_preview(job_dict) -> {"video_path": ...}`, this adapter delegates to it
and then runs the shared output-contract verification. Until then it reports
`pending` and refuses to generate.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

from engine_base import (
    EngineNotAvailable,
    FinalVideo,
    ProductionEngine,
    ProductionJob,
    verify_output,
)

PREVIEWS_DIR = Path(__file__).resolve().parent.parent / "previews"
PIPELINE_PY = PREVIEWS_DIR / "pipeline.py"


class Phase2PreviewEngine(ProductionEngine):
    name = "phase2_preview"
    status = "pending"
    capabilities = {
        "text_to_video": False,
        "image_to_video": False,
        "character_reference": "via the Phase 2 pipeline's own keyframe step",
        "note": "fast/cheap preview path promoted to an engine once pipeline.py lands",
    }

    def _pipeline(self):
        if not PIPELINE_PY.exists():
            return None
        spec = importlib.util.spec_from_file_location("vd_preview_pipeline", PIPELINE_PY)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def validate_config(self) -> list:
        if not PIPELINE_PY.exists():
            return [f"pending: {PIPELINE_PY} not present yet (Phase 2 build in progress)"]
        mod = self._pipeline()
        if not hasattr(mod, "run_preview"):
            return ["pending: previews/pipeline.py must expose run_preview(job_dict)"]
        return []

    def dry_run(self, job: ProductionJob) -> dict:
        return {
            "engine": self.name,
            "status": self.status,
            "sent": False,
            "pipeline_present": PIPELINE_PY.exists(),
            "problems": self.validate_config(),
        }

    def generate(self, job: ProductionJob) -> FinalVideo:
        problems = self.validate_config()
        if problems:
            raise EngineNotAvailable(f"phase2_preview engine pending: {problems}")
        mod = self._pipeline()
        result = mod.run_preview(job.__dict__)  # -> {"video_path": ...}
        verified = verify_output(result["video_path"])
        if not verified["ok"]:
            raise RuntimeError(f"Phase 2 pipeline output failed the contract: {verified['checks']}")
        import os
        return FinalVideo(
            video_path=result["video_path"],
            caption_path=result.get("caption_path", ""),
            duration_s=verified["duration_s"],
            size_bytes=os.path.getsize(result["video_path"]),
            engine=self.name,
            verified=verified,
            notes=["produced via Phase 2 Preview Studio pipeline"],
        )
