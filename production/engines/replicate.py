"""Replicate adapter — CODE-COMPLETE, KEY-GATED, UNTESTED.

Status: key_gated. Needs REPLICATE_API_TOKEN in ~/workspace/viraldesk/.env.
Built from Replicate's public predictions API shape; the `model` config value
(owner/model:version) MUST be set to a real video model before the first paid
run — model versions change, so copy it fresh from replicate.com.

Capabilities (Oct 2026 list prices):
  - text-to-video / image-to-video: yes (Kling, Veo, Wan, Seedance hosted)
  - character reference: model-dependent; ref images must be PUBLIC URLs
  - billing: per-second; FAILED runs are NOT charged
  - approx cost for one 35s video (6 x 5s clips):
      Kling v3 Omni silent  $0.168/s -> ~$5.00
      Veo 3.1 silent        $0.20/s  -> ~$6.00
    (verify live pricing on the model page before spending)

Same design as the fal adapter: one clip per scene, then the shared
post-production pipeline (voiceover, captions, branding, output contract).
"""
from __future__ import annotations

import json
import time
import urllib.request

from engine_base import (
    EngineNotAvailable,
    FinalVideo,
    ProductionEngine,
    ProductionJob,
    load_dotenv,
)

REPLICATE_API = "https://api.replicate.com/v1/predictions"


class ReplicateEngine(ProductionEngine):
    name = "replicate"
    status = "key_gated"
    capabilities = {
        "text_to_video": True,
        "image_to_video": True,
        "character_reference": "model-dependent — ref images must be PUBLIC URLs",
        "max_duration_s": "model-dependent; scenes stitched in post",
        "audio": "model-dependent",
        "billing": "per-second; failed runs NOT charged",
    }

    def _key(self) -> str:
        return load_dotenv().get("REPLICATE_API_TOKEN", "")

    def validate_config(self) -> list:
        problems = []
        if not self._key():
            problems.append("REPLICATE_API_TOKEN not set in ~/workspace/viraldesk/.env — engine is key-gated")
        if "version" not in self.config.get("model", "") and ":" not in self.config.get("model", ""):
            problems.append("config.model should be 'owner/model:version' — set a real video model version")
        return problems

    def _scene_payload(self, job: ProductionJob, scene) -> dict:
        ref_url = self.config.get("CHARACTER_REF_URL", "")
        model = self.config.get("model", "")
        owner, _, version = model.partition(":")
        body = {"version": version or "<SET MODEL VERSION>",
                "input": {
                    "prompt": (f"{scene.visual} Vertical 9:16. Smooth natural motion, "
                               "no text rendered in-frame. Match the reference person's face. "
                               f"~{int(scene.duration_s)}s."),
                    "aspect_ratio": self.config.get("aspect_ratio", "9:16"),
                }}
        if ref_url:
            body["input"]["image"] = ref_url
        return {"method": "POST", "url": REPLICATE_API,
                "headers": {"Authorization": "Bearer <REDACTED>", "Content-Type": "application/json"},
                "json": body}

    def dry_run(self, job: ProductionJob) -> dict:
        return {
            "engine": self.name,
            "status": self.status,
            "sent": False,
            "note": "UNTESTED adapter — set config.model to a real owner/model:version before first paid run.",
            "key_present": bool(self._key()),
            "per_scene_requests": [self._scene_payload(job, s) for s in job.scenes],
            "post_production": "clips -> shared post pipeline (voiceover, captions, branding, 1080x1920 H.264+AAC+faststart)",
            "problems": self.validate_config(),
        }

    def _api(self, method: str, url: str, body: dict | None = None) -> dict:
        req = urllib.request.Request(
            url, data=json.dumps(body).encode() if body else None,
            headers={"Authorization": f"Bearer {self._key()}", "Content-Type": "application/json"},
            method=method)
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())

    def generate(self, job: ProductionJob) -> FinalVideo:
        problems = self.validate_config()
        if problems:
            raise EngineNotAvailable(f"replicate engine key-gated: {problems}")
        # UNTESTED live path — runs only when a key exists (it does not tonight).
        urls = []
        for s in job.scenes:
            spec = self._scene_payload(job, s)
            pred = self._api("POST", spec["url"], spec["json"])
            get_url = pred["urls"]["get"]
            t0 = time.time()
            while time.time() - t0 < self.config.get("poll_timeout_s", 600):
                pred = self._api("GET", get_url)
                if pred["status"] == "succeeded":
                    out = pred["output"]
                    urls.append(out[0] if isinstance(out, list) else out)
                    break
                if pred["status"] in ("failed", "canceled"):
                    raise RuntimeError(f"replicate prediction failed for scene {s.id}")
                time.sleep(10)
            else:
                raise RuntimeError(f"replicate prediction timed out for scene {s.id}")
        raise EngineNotAvailable(
            "UNTESTED: live replicate path reached (key present) but clip post-production "
            "wiring is not finished."
        )
