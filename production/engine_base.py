"""ViralDesk Production — engine interface (Phase 3).

Every production engine implements ProductionEngine. Engines are selected
via engines.yaml — swapping engines never requires code changes.

LOCKED RULE enforced here: every ProductionJob MUST carry character_refs
(non-empty). The locked character reference is attached to every generation.
"""
from __future__ import annotations

import importlib
import json
import os
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path

import yaml

PROD_DIR = Path(__file__).resolve().parent
ENGINES_YAML = PROD_DIR / "engines.yaml"
BRANDING_YAML = PROD_DIR / "branding.yaml"
DOTENV = PROD_DIR.parent / ".env"


class EngineNotAvailable(RuntimeError):
    """Raised when an engine cannot run (missing key, region block, no GPU...)."""


class EngineNotTested(RuntimeError):
    """Raised when a key-gated engine is asked to spend money without a key."""


# ---------------------------------------------------------------- dataclasses

@dataclass
class Scene:
    id: str
    duration_s: float
    visual: str = ""                       # image/video prompt for this scene
    onscreen_text: list = field(default_factory=list)  # lines, Roman Urdu or English
    voiceover: str = ""                    # Urdu script for TTS (or owner's recorded VO path)
    voiceover_lang: str = "ur"
    voiceover_file: str = ""               # optional: pre-recorded audio, wins over TTS
    keyframe: str = ""                     # input still path (stills engine)
    motion: str = "zoom_in"                # zoom_in | zoom_out | pan_left | pan_right
    include_presenter: bool = False        # presenter photo+name overlay on this scene


@dataclass
class ProductionJob:
    prompt_id: int
    prompt_version: int
    title: str
    scenes: list                           # list[Scene]
    character_refs: list                   # REQUIRED — locked refs on every generation
    branding: dict
    output_dir: str
    end_card: dict = field(default_factory=dict)
    caption: str = ""
    engine: str = "stills"

    def __post_init__(self):
        if not self.character_refs:
            raise ValueError(
                "LOCKED RULE: character_refs must not be empty — "
                "the locked character reference is attached to every generation."
            )
        # expand ~ in ref paths so engines always get real paths
        self.character_refs = [os.path.expanduser(p) for p in self.character_refs]


@dataclass
class FinalVideo:
    video_path: str
    caption_path: str
    duration_s: float
    size_bytes: int
    engine: str
    verified: dict
    notes: list = field(default_factory=list)


# ------------------------------------------------------------------ interface

class ProductionEngine(ABC):
    """Base class every ViralDesk production engine must implement."""

    name = "base"
    status = "unknown"          # working | key_gated | pending | blocked
    capabilities: dict = {}    # text_to_video, image_to_video, character_reference, ...

    def __init__(self, config: dict):
        self.config = config or {}

    @abstractmethod
    def validate_config(self) -> list:
        """Return a list of problems (strings). Empty list = ready to run."""

    @abstractmethod
    def dry_run(self, job: ProductionJob) -> dict:
        """Build the full execution plan / API payload WITHOUT running or spending."""

    @abstractmethod
    def generate(self, job: ProductionJob) -> FinalVideo:
        """Run the engine end-to-end. Must verify output before returning."""


# ------------------------------------------------------------------- helpers

def load_dotenv(path: Path = DOTENV) -> dict:
    """Parse .env into a dict. Values are NEVER logged — callers must not print them."""
    out = {}
    if not path.exists():
        return out
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def load_registry(path: Path = ENGINES_YAML) -> dict:
    return yaml.safe_load(path.read_text())


def load_branding(path: Path = BRANDING_YAML) -> dict:
    return yaml.safe_load(path.read_text())


def get_engine(name: str, registry: dict | None = None) -> ProductionEngine:
    """Instantiate an engine by name from the registry (no code changes to swap)."""
    registry = registry or load_registry()
    entry = registry["engines"].get(name)
    if not entry:
        raise KeyError(f"Unknown engine '{name}'. Registered: {list(registry['engines'])}")
    mod = importlib.import_module(entry["module"])
    cls = getattr(mod, entry["class"])
    eng = cls(entry.get("config", {}))
    eng.status = entry.get("status", eng.status)
    eng.description = entry.get("description", "")
    return eng


def list_engines(registry: dict | None = None) -> list:
    registry = registry or load_registry()
    return [
        {"name": n, "status": e.get("status"), "description": (e.get("description") or "").strip()[:120]}
        for n, e in registry["engines"].items()
    ]


def ffprobe_json(path: str) -> dict:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path],
        capture_output=True, text=True, timeout=60,
    )
    return json.loads(r.stdout or "{}")


def has_faststart(path: str) -> bool:
    """True if the moov atom comes before mdat (streamable / phone-safe)."""
    with open(path, "rb") as f:
        head = f.read(8 * 1024 * 1024)  # atoms live near the head when faststart is set
    moov = head.find(b"moov")
    mdat = head.find(b"mdat")
    return moov != -1 and (mdat == -1 or moov < mdat)


# Output contract — NON-NEGOTIABLE (master spec Phase 3/4)
OUTPUT_CONTRACT = {
    "width": 1080,
    "height": 1920,
    "vcodec": "h264",
    "pix_fmt": "yuv420p",
    "acodec": "aac",
    "faststart": True,
    "max_size_mb": 25,
}


def verify_output(path: str) -> dict:
    """Verify a finished MP4 against the output contract. Returns dict with ok flag."""
    checks = {}
    info = ffprobe_json(path)
    streams = info.get("streams", [])
    v = next((s for s in streams if s.get("codec_type") == "video"), {})
    a = next((s for s in streams if s.get("codec_type") == "audio"), {})
    fmt = info.get("format", {})

    checks["vcodec_h264"] = v.get("codec_name") == "h264"
    checks["resolution_1080x1920"] = (v.get("width"), v.get("height")) == (1080, 1920)
    checks["pix_fmt_yuv420p"] = v.get("pix_fmt") == "yuv420p"
    checks["profile_baseline"] = "baseline" in (v.get("profile") or "").lower().replace("constrained ", "")
    checks["acodec_aac"] = a.get("codec_name") == "aac"
    checks["faststart_moov_first"] = has_faststart(path)
    size_mb = os.path.getsize(path) / (1024 * 1024)
    checks["size_under_25mb"] = size_mb <= OUTPUT_CONTRACT["max_size_mb"]
    checks["has_duration"] = float(fmt.get("duration", 0) or 0) > 0

    return {
        "ok": all(checks.values()),
        "checks": checks,
        "duration_s": round(float(fmt.get("duration", 0) or 0), 2),
        "size_mb": round(size_mb, 2),
        "video": {k: v.get(k) for k in ("codec_name", "profile", "width", "height", "pix_fmt", "avg_frame_rate")},
        "audio": {k: a.get(k) for k in ("codec_name", "sample_rate", "channels")},
    }
