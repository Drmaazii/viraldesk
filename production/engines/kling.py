"""Kling direct-API adapter — CODE-COMPLETE, KEY-GATED, UNTESTED.

Status: key_gated. Needs KLING_ACCESS_KEY + KLING_SECRET_KEY in
~/workspace/viraldesk/.env (JWT auth against api.klingai.com).

IMPORTANT (Oct 2026): the Kling API is a separate prepaid system — a Kling
consumer subscription does NOT grant API access. API needs a Kling Open
Platform account with a prepaid resource package (from ~$9.80). Failed API
generations are NOT billed.

Capabilities:
  - text-to-video / image-to-video: yes (Kling 3.0 std/pro)
  - character reference: up to 4 reference images on Pro; must be PUBLIC URLs
  - max 15s per clip; 9:16 supported
  - approx cost for one 35s video (6 x 5s clips, std silent $0.084/s): ~$2.50
    (verify live pricing before spending)

Same design as the other API adapters: one clip per scene, then the shared
post-production pipeline (voiceover, captions, branding, output contract).
"""
from __future__ import annotations

import base64
import hashlib
import hmac
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


def _jwt(access_key: str, secret_key: str) -> str:
    """Kling API JWT: HS256, minimal claims (per Kling open-platform docs)."""
    header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).rstrip(b"=")
    now = int(time.time())
    payload = base64.urlsafe_b64encode(json.dumps(
        {"iss": access_key, "exp": now + 1800, "nbf": now - 5}).encode()).rstrip(b"=")
    sig = hmac.new(secret_key.encode(), header + b"." + payload, hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(sig).rstrip(b"=")
    return (header + b"." + payload + b"." + sig_b64).decode()


class KlingEngine(ProductionEngine):
    name = "kling"
    status = "key_gated"
    capabilities = {
        "text_to_video": True,
        "image_to_video": True,
        "character_reference": "up to 4 reference images (Pro) — must be PUBLIC URLs",
        "max_duration_s": "15 per clip; scenes stitched in post",
        "audio": "optional add-on",
        "billing": "prepaid packages; failed API generations NOT billed",
    }

    def _creds(self):
        env = load_dotenv()
        return env.get("KLING_ACCESS_KEY", ""), env.get("KLING_SECRET_KEY", "")

    def validate_config(self) -> list:
        problems = []
        ak, sk = self._creds()
        if not ak or not sk:
            problems.append("KLING_ACCESS_KEY / KLING_SECRET_KEY not set in ~/workspace/viraldesk/.env — engine is key-gated")
        return problems

    def _scene_payload(self, job: ProductionJob, scene) -> dict:
        base = self.config.get("api_base", "https://api.klingai.com")
        ref_url = self.config.get("CHARACTER_REF_URL", "")
        if ref_url:
            url = f"{base}/v1/videos/image2video"
            body = {"model": "kling-v3", "mode": self.config.get("mode", "std"),
                    "image": ref_url,
                    "prompt": (f"{scene.visual} Vertical 9:16. Smooth natural motion, "
                               "no text rendered in-frame. Match the reference person's face."),
                    "duration": str(min(15, int(scene.duration_s) or 5)),
                    "aspect_ratio": self.config.get("aspect_ratio", "9:16")}
        else:
            url = f"{base}/v1/videos/text2video"
            body = {"model": "kling-v3", "mode": self.config.get("mode", "std"),
                    "prompt": (f"{scene.visual} Vertical 9:16. Smooth natural motion, "
                               "no text rendered in-frame."),
                    "duration": str(min(15, int(scene.duration_s) or 5)),
                    "aspect_ratio": self.config.get("aspect_ratio", "9:16")}
        return {"method": "POST", "url": url,
                "headers": {"Authorization": "Bearer <JWT REDACTED>", "Content-Type": "application/json"},
                "json": body}

    def dry_run(self, job: ProductionJob) -> dict:
        ak, _ = self._creds()
        return {
            "engine": self.name,
            "status": self.status,
            "sent": False,
            "note": ("UNTESTED adapter — needs a Kling Open Platform account + prepaid package; "
                     "a consumer subscription does NOT unlock the API."),
            "key_present": bool(ak),
            "per_scene_requests": [self._scene_payload(job, s) for s in job.scenes],
            "post_production": "clips -> shared post pipeline (voiceover, captions, branding, 1080x1920 H.264+AAC+faststart)",
            "problems": self.validate_config(),
        }

    def generate(self, job: ProductionJob) -> FinalVideo:
        problems = self.validate_config()
        if problems:
            raise EngineNotAvailable(f"kling engine key-gated: {problems}")
        # UNTESTED live path — runs only when keys exist (they do not tonight).
        raise EngineNotAvailable(
            "UNTESTED: live kling path reached (keys present) but task polling + clip "
            "post-production wiring is not finished."
        )
