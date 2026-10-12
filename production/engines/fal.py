"""fal.ai adapter — CODE-COMPLETE, KEY-GATED, UNTESTED.

Status: key_gated. Needs FAL_API_KEY in ~/workspace/viraldesk/.env.
AI video generation is region-blocked on this machine, so live calls were
never attempted; the request construction below is built from fal.ai's public
queue API shape and MUST be verified against the live docs before the first
paid run (model ids change fast).

Capabilities (from fal.ai model pages, Oct 2026):
  - text-to-video: yes (Veo 3.1, Kling 3.0, Wan 3.0...)
  - image-to-video: yes
  - character reference: via input image(s); ref images must be PUBLIC URLs —
    fal cannot read files off this machine (morning setup step, see README)
  - billing: prepaid credits (valid 365 days); FAILED generations are NOT billed
  - approx cost for one 35s ViralDesk video (6 scenes x 5s clips):
      Kling 3.0 Standard silent  $0.084/s -> ~$2.50
      Veo 3.1 Fast silent         $0.10/s  -> ~$3.00
      Veo 3.1 Standard w/ audio  $0.40/s  -> ~$12.00
    (verify live pricing on the model page before spending)

Design: each scene becomes one short clip (image-to-video from the scene
keyframe is cheapest and most controllable); clips are then post-produced
with the SAME voiceover/caption/branding pipeline as the stills engine, so
the output contract (1080x1920 H.264+AAC+faststart) holds for every engine.
"""
from __future__ import annotations

import json
import os
import time
import urllib.request

from engine_base import (
    EngineNotAvailable,
    FinalVideo,
    ProductionEngine,
    ProductionJob,
    load_dotenv,
    verify_output,
)

FAL_QUEUE = "https://queue.fal.run"


class FalEngine(ProductionEngine):
    name = "fal"
    status = "key_gated"
    capabilities = {
        "text_to_video": True,
        "image_to_video": True,
        "character_reference": "via input image(s) — must be PUBLIC URLs",
        "max_duration_s": "8-15 per clip (model-dependent); scenes stitched in post",
        "audio": "model-dependent (Veo = native audio option)",
        "billing": "prepaid credits; failed generations NOT billed",
    }

    def _key(self) -> str:
        return load_dotenv().get("FAL_API_KEY", "")

    def validate_config(self) -> list:
        problems = []
        if not self._key():
            problems.append("FAL_API_KEY not set in ~/workspace/viraldesk/.env — engine is key-gated")
        return problems

    def _scene_payload(self, job: ProductionJob, scene) -> dict:
        """Exact JSON body that WOULD be POSTed for one scene clip."""
        model = self.config.get("model", "fal-ai/veo3/fast")
        ref_url = self.config.get("CHARACTER_REF_URL", "")
        payload = {
            "prompt": (
                f"{scene.visual} "
                "Vertical 9:16. Smooth natural motion, no text or words rendered in-frame. "
                f"Character consistency: match the person in the reference image. Duration ~{int(scene.duration_s)}s."
            ),
            "aspect_ratio": self.config.get("aspect_ratio", "9:16"),
            "duration": f"{int(scene.duration_s)}s",
        }
        if ref_url:
            payload["image_url"] = ref_url  # image-to-video: cheapest + most controllable
        return {"method": "POST", "url": f"{FAL_QUEUE}/{model}",
                "headers": {"Authorization": "Key <REDACTED>", "Content-Type": "application/json"},
                "json": payload}

    def dry_run(self, job: ProductionJob) -> dict:
        return {
            "engine": self.name,
            "status": self.status,
            "sent": False,  # dry run NEVER sends
            "note": "UNTESTED adapter — verify model id + payload against fal.ai docs before first paid run.",
            "key_present": bool(self._key()),
            "per_scene_requests": [self._scene_payload(job, s) for s in job.scenes],
            "post_production": "clips -> stills-engine post pipeline (voiceover, captions, branding, 1080x1920 H.264+AAC+faststart)",
            "problems": self.validate_config(),
        }

    # ------------------------------------------------------------- live path
    def _post(self, url: str, body: dict) -> dict:
        req = urllib.request.Request(
            url, data=json.dumps(body).encode(),
            headers={"Authorization": f"Key {self._key()}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())

    def _get(self, url: str) -> dict:
        req = urllib.request.Request(url, headers={"Authorization": f"Key {self._key()}"})
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())

    def generate(self, job: ProductionJob) -> FinalVideo:
        problems = self.validate_config()
        if problems:
            raise EngineNotAvailable(f"fal engine key-gated: {problems}")
        # UNTESTED live path — runs only when a key exists (it does not tonight).
        clips = []
        for s in job.scenes:
            spec = self._scene_payload(job, s)
            sub = self._post(spec["url"], spec["json"])
            status_url = sub.get("status_url") or sub.get("response_url")
            video_url = None
            t0 = time.time()
            while time.time() - t0 < self.config.get("poll_timeout_s", 600):
                st = self._get(status_url)
                if st.get("status") == "COMPLETED":
                    video_url = (st.get("video") or {}).get("url")
                    break
                if st.get("status") in ("FAILED", "CANCELLED"):
                    raise RuntimeError(f"fal generation failed for scene {s.id}: {st}")
                time.sleep(10)
            if not video_url:
                raise RuntimeError(f"fal generation timed out for scene {s.id}")
            clips.append(video_url)
        # Post-production (voiceover/captions/branding/encode) reuses the stills
        # pipeline so the output contract is identical across engines.
        raise EngineNotAvailable(
            "UNTESTED: live fal path reached (key present) but clip post-production "
            "wiring is not finished. Clips downloaded: " + ", ".join(clips[:2]) + "..."
        )
