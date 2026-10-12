"""Stills engine — WORKING NOW (no key, no GPU, no AI video-gen needed).

Pipeline per scene:
  keyframe (agent-generated via media pipeline, locked character ref attached)
    -> PIL branding (logo upper-left ALWAYS, presenter overlay optional,
       on-screen text lower-third)
    -> Ken Burns motion (ffmpeg zoompan) -> scene MP4
  + end card (PIL-designed, name/qualification/phone/address)
  + AI voiceover per scene (tts CLI) padded to scene duration
  -> concat -> phone-safe encode (H.264 baseline + AAC + faststart)
  -> ffprobe verification against the output contract.

Keyframes are an explicit INPUT to the engine (job scenes carry `keyframe`
paths). They are generated agent-side with the locked character reference
attached to every generation call, then handed to the engine — this keeps the
deterministic assembly (this file) separate from the generative step.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from engine_base import (
    EngineNotAvailable,
    FinalVideo,
    ProductionEngine,
    ProductionJob,
    Scene,
    has_faststart,
    verify_output,
)

W, H = 1080, 1920
FPS = 30
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
TTS_CLI = "/opt/hatch/bin/tts"


# ------------------------------------------------------------------ PIL bits

def _font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def cover_resize(img: Image.Image, w: int = W, h: int = H) -> Image.Image:
    """Resize to cover w×h (crop overflow)."""
    img = img.convert("RGB")
    scale = max(w / img.width, h / img.height)
    img = img.resize((int(img.width * scale) + 1, int(img.height * scale) + 1), Image.LANCZOS)
    x = (img.width - w) // 2
    y = (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))


def wrap_lines(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont,
               max_w: int) -> list:
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines or [""]


def composite_logo(base: Image.Image, branding: dict) -> Image.Image:
    """Paste the EXACT logo file upper-left. The image model NEVER draws it."""
    ov = branding.get("overlays", {})
    logo_path = os.path.expanduser(branding["logo_path"])
    logo = Image.open(logo_path).convert("RGBA")
    lw = ov.get("logo_width_px", 200)
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    m = ov.get("logo_margin_px", 36)
    base.paste(logo, (m, m), logo)
    return base


def composite_presenter(base: Image.Image, branding: dict) -> Image.Image:
    """Circular presenter photo + name/qualification, upper-right."""
    ov = branding.get("overlays", {})
    if not ov.get("show_presenter_overlay", True):
        return base
    photo_path = os.path.expanduser(branding.get("presenter_photo", ""))
    if not photo_path or not os.path.exists(photo_path):
        return base
    d = ov.get("presenter_diameter_px", 200)
    m = ov.get("presenter_margin_px", 36)
    photo = Image.open(photo_path).convert("RGB")
    photo = cover_resize(photo, d, d)
    mask = Image.new("L", (d, d), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, d, d), fill=255)
    ring = Image.new("RGBA", (d + 12, d + 12), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse((0, 0, d + 12, d + 12),
                                 fill=(214, 31, 44, 255))  # accent ring
    base = base.convert("RGBA")
    base.paste(ring, (W - m - d - 6, m - 6), ring)
    base.paste(photo, (W - m - d, m), mask)

    draw = ImageDraw.Draw(base)
    name_f = _font(FONT_BOLD, 34)
    qual_f = _font(FONT_REG, 28)
    # name + qualification stacked under the photo, right aligned
    tx = W - m
    ty = m + d + 14
    for txt, fnt, col in ((branding.get("presenter_name", ""), name_f, "white"),
                          (branding.get("qualification", ""), qual_f, (230, 235, 245))):
        tw = draw.textlength(txt, font=fnt)
        draw.text((tx - tw, ty), txt, font=fnt, fill=col,
                  stroke_width=1, stroke_fill="black")
        ty += fnt.size + 8
    return base.convert("RGB")


def composite_onscreen_text(base: Image.Image, lines: list) -> Image.Image:
    """Lower-third caption block: wrapped, centered, readable on any background."""
    if not lines:
        return base
    base = base.convert("RGBA")
    draw = ImageDraw.Draw(base)
    font = _font(FONT_BOLD, 62)
    max_w = W - 160
    wrapped = []
    for ln in lines:
        wrapped.extend(wrap_lines(draw, ln, font, max_w))
    wrapped = wrapped[:3]  # never more than 3 lines
    line_h = font.size + 18
    block_h = line_h * len(wrapped) + 56
    y0 = H - block_h - 200  # clear of platform UI at the very bottom
    box = Image.new("RGBA", (W - 80, block_h), (0, 0, 0, 150))
    bdraw = ImageDraw.Draw(box)
    bdraw.rounded_rectangle((0, 0, W - 80, block_h), radius=28, fill=(0, 0, 0, 150))
    base.alpha_composite(box, (40, y0))
    draw = ImageDraw.Draw(base)
    y = y0 + 28
    for ln in wrapped:
        tw = draw.textlength(ln, font=font)
        draw.text(((W - tw) / 2, y), ln, font=font, fill="white",
                  stroke_width=2, stroke_fill="black")
        y += line_h
    return base.convert("RGB")


def build_end_card(branding: dict, headline: list, duration_s: float) -> Image.Image:
    """PIL-designed end card: logo, CTA, name + qualification, phone, address."""
    top = tuple(int(branding["colors"]["primary"].lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    bot = (6, 22, 52)
    card = Image.new("RGB", (W, H))
    px = card.load()
    for y in range(H):
        t = y / H
        px_col = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        for x in range(W):
            px[x, y] = px_col
    card = composite_logo(card, branding)
    draw = ImageDraw.Draw(card)
    # headline
    hf = _font(FONT_BOLD, 84)
    y = 560
    for ln in headline:
        tw = draw.textlength(ln, font=hf)
        draw.text(((W - tw) / 2, y), ln, font=hf, fill="white",
                  stroke_width=2, stroke_fill="black")
        y += hf.size + 24
    # divider
    draw.rectangle((W // 2 - 120, y + 10, W // 2 + 120, y + 16), fill=(214, 31, 44))
    y += 70
    # name / qualification / phone / address
    for txt, size, col in (
        (branding.get("presenter_name", ""), 56, "white"),
        (branding.get("qualification", ""), 40, (200, 210, 225)),
        (branding.get("phone", ""), 72, (214, 31, 44)),
    ):
        f = _font(FONT_BOLD, size)
        tw = draw.textlength(txt, font=f)
        draw.text(((W - tw) / 2, y), txt, font=f, fill=col,
                  stroke_width=1, stroke_fill="black")
        y += size + 26
    af = _font(FONT_REG, 32)
    for addr in branding.get("address_lines", []):
        tw = draw.textlength(addr, font=af)
        draw.text(((W - tw) / 2, y), addr, font=af, fill=(180, 190, 205))
        y += 52
    return card


# ------------------------------------------------------------- ffmpeg / audio

def run(cmd: list, **kw) -> subprocess.CompletedProcess:
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd[:4])}...\n{r.stderr[-1500:]}")
    return r


KENBURNS = {
    # N = frame count; input is upscaled 2x for smooth zoom
    "zoom_in":  "scale=2160:3840,zoompan=z='1+0.12*on/{N}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={N}:s=1080x1920:fps=30",
    "zoom_out": "scale=2160:3840,zoompan=z='1.12-0.12*on/{N}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={N}:s=1080x1920:fps=30",
    "pan_right": "scale=2160:3840,zoompan=z='1.15':x='(iw-iw/zoom)*on/{N}':y='ih/2-(ih/zoom/2)':d={N}:s=1080x1920:fps=30",
    "pan_left":  "scale=2160:3840,zoompan=z='1.15':x='(iw-iw/zoom)*(1-on/{N})':y='ih/2-(ih/zoom/2)':d={N}:s=1080x1920:fps=30",
}


def ken_burns(still_png: str, out_mp4: str, duration_s: float, motion: str):
    n = max(1, int(round(duration_s * FPS)))
    vf = KENBURNS.get(motion, KENBURNS["zoom_in"]).format(N=n)
    run(["ffmpeg", "-y", "-loop", "1", "-i", still_png,
         "-vf", vf, "-frames:v", str(n),
         "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
         out_mp4])


def synth_voiceover(text: str, lang: str, out_mp3: str, timeout: int = 180):
    """AI voiceover via tts CLI. Previews/first-drafts only — finals use the
    owner's real recorded voiceover (drop the file in as voiceover_file)."""
    run([TTS_CLI, "speak", "--language", lang, "--output", out_mp3,
         "--text-stdin"], input=text, timeout=timeout)


def audio_duration(path: str) -> float:
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", path])
    return float((r.stdout or "0").strip())


def concat_files(paths: list, list_file: str, out: str, is_video: bool):
    with open(list_file, "w") as f:
        for p in paths:
            f.write(f"file '{p}'\n")
    if is_video:
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file,
             "-c", "copy", out])
    else:
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file,
             "-c:a", "aac", "-b:a", "128k", out])


# ------------------------------------------------------------------- engine

class StillsEngine(ProductionEngine):
    name = "stills"
    status = "working"
    capabilities = {
        "text_to_video": False,
        "image_to_video": False,
        "character_reference": "attached to every keyframe generation (locked refs, agent-side)",
        "max_duration_s": 180,
        "audio": "AI voiceover (tts CLI); pre-recorded owner VO supported per scene",
        "resolution": "1080x1920",
    }

    # ---------------------------------------------------------- validation
    def validate_config(self) -> list:
        problems = []
        for tool in ("ffmpeg", "ffprobe"):
            if not shutil.which(tool):
                problems.append(f"missing binary: {tool}")
        if not os.path.exists(TTS_CLI):
            problems.append(f"missing tts CLI: {TTS_CLI}")
        for f in (FONT_BOLD, FONT_REG):
            if not os.path.exists(f):
                problems.append(f"missing font: {f}")
        try:
            import PIL  # noqa
        except ImportError:
            problems.append("missing Python PIL")
        return problems

    # ------------------------------------------------------------- dry run
    def dry_run(self, job: ProductionJob) -> dict:
        total = sum(s.duration_s for s in job.scenes) + job.end_card.get("duration_s", 0)
        return {
            "engine": self.name,
            "status": self.status,
            "sent": False,
            "plan": [
                {
                    "scene": s.id,
                    "duration_s": s.duration_s,
                    "motion": s.motion,
                    "keyframe": s.keyframe or "(MISSING — generate via media pipeline first)",
                    "voiceover_chars": len(s.voiceover or ""),
                    "voiceover_src": "pre-recorded file" if s.voiceover_file else f"tts CLI ({s.voiceover_lang})",
                    "presenter_overlay": s.include_presenter,
                    "onscreen_lines": len(s.onscreen_text),
                }
                for s in job.scenes
            ],
            "end_card_s": job.end_card.get("duration_s", 0),
            "total_s": round(total, 1),
            "branding_injected": {
                "logo": job.branding.get("logo_path"),
                "presenter": job.branding.get("presenter_name"),
                "phone": job.branding.get("phone"),
                "character_refs": job.character_refs,  # locked refs — on every generation
            },
            "output_contract": "1080x1920 H.264 baseline + AAC + faststart, <25MB",
        }

    # ------------------------------------------------------------ generate
    def generate(self, job: ProductionJob) -> FinalVideo:
        problems = self.validate_config()
        if problems:
            raise EngineNotAvailable(f"stills engine not ready: {problems}")
        t0 = time.time()
        notes = []
        outdir = Path(job.output_dir)
        workdir = outdir / f"job_{job.prompt_id}_v{job.prompt_version}_{int(t0)}"
        (workdir / "scenes").mkdir(parents=True, exist_ok=True)

        branding = job.branding
        scene_mp4s, audio_segs = [], []

        for i, s in enumerate(job.scenes):
            # 1. keyframe -> branded still (PIL)
            kf = s.keyframe
            if not kf or not os.path.exists(os.path.expanduser(kf)):
                raise EngineNotAvailable(
                    f"Scene {s.id}: keyframe missing ({kf}). Generate it via the media "
                    "pipeline with the locked character reference attached, then re-run."
                )
            still = cover_resize(Image.open(os.path.expanduser(kf)))
            still = composite_logo(still, branding)
            if s.include_presenter:
                still = composite_presenter(still, branding)
            still = composite_onscreen_text(still, s.onscreen_text)
            still_path = str(workdir / "scenes" / f"{s.id}_branded.png")
            still.save(still_path)

            # 2. voiceover (pre-recorded wins; else TTS) -> fit scene duration
            vo_src = s.voiceover_file or ""
            vo_raw = str(workdir / "scenes" / f"{s.id}_vo_raw.mp3")
            if not vo_src and s.voiceover:
                try:
                    synth_voiceover(s.voiceover, s.voiceover_lang, vo_raw)
                    vo_src = vo_raw
                    notes.append(f"scene {s.id}: AI voiceover ({s.voiceover_lang})")
                except Exception as e:
                    # Flaky TTS backend must never kill a production run:
                    # the scene goes out silent-but-captioned, and the note
                    # tells the operator exactly what happened.
                    notes.append(f"scene {s.id}: AI voiceover FAILED ({type(e).__name__}) — "
                                 "scene rendered silent with burned-in captions")
            elif vo_src:
                notes.append(f"scene {s.id}: owner pre-recorded voiceover")
            dur = s.duration_s
            if vo_src and os.path.exists(os.path.expanduser(vo_src)):
                vd = audio_duration(os.path.expanduser(vo_src))
                if vd > dur:
                    dur = round(vd + 0.4, 1)  # never clip the voice
                    notes.append(f"scene {s.id}: extended to {dur}s to fit voiceover")

            # 3. Ken Burns -> scene mp4 (exact duration)
            mp4 = str(workdir / "scenes" / f"{s.id}.mp4")
            ken_burns(still_path, mp4, dur, s.motion)
            scene_mp4s.append(mp4)

            # 4. audio segment padded to scene duration
            aseg = str(workdir / "scenes" / f"{s.id}_a.m4a")
            if vo_src and os.path.exists(os.path.expanduser(vo_src)):
                run(["ffmpeg", "-y", "-i", os.path.expanduser(vo_src),
                     "-af", f"apad=whole_dur={dur}", "-t", str(dur),
                     "-c:a", "aac", "-b:a", "128k", aseg])
            else:
                run(["ffmpeg", "-y", "-f", "lavfi", "-i",
                     f"anullsrc=r=44100:cl=stereo:d={dur}",
                     "-t", str(dur), "-c:a", "aac", "-b:a", "128k", aseg])
            audio_segs.append(aseg)

        # 5. end card
        ec = job.end_card or {}
        if ec:
            card = build_end_card(branding, ec.get("headline", [""]), ec.get("duration_s", 4))
            card_path = str(workdir / "scenes" / "endcard.png")
            card.save(card_path)
            ec_mp4 = str(workdir / "scenes" / "endcard.mp4")
            ken_burns(card_path, ec_mp4, ec.get("duration_s", 4), "zoom_in")
            scene_mp4s.append(ec_mp4)
            ec_vo = str(workdir / "scenes" / "endcard_vo_raw.mp3")
            if ec.get("voiceover"):
                try:
                    synth_voiceover(ec["voiceover"], job.scenes[0].voiceover_lang if job.scenes else "ur", ec_vo)
                    ec_a = str(workdir / "scenes" / "endcard_a.m4a")
                    run(["ffmpeg", "-y", "-i", ec_vo, "-af",
                         f"apad=whole_dur={ec.get('duration_s', 4)}",
                         "-t", str(ec.get("duration_s", 4)),
                         "-c:a", "aac", "-b:a", "128k", ec_a])
                    audio_segs.append(ec_a)
                    notes.append("end card: AI voiceover")
                except Exception as e:
                    notes.append(f"end card: AI voiceover FAILED ({type(e).__name__}) — silent")
                    ec_a = str(workdir / "scenes" / "endcard_a.m4a")
                    run(["ffmpeg", "-y", "-f", "lavfi", "-i",
                         f"anullsrc=r=44100:cl=stereo:d={ec.get('duration_s', 4)}",
                         "-t", str(ec.get("duration_s", 4)),
                         "-c:a", "aac", "-b:a", "128k", ec_a])
                    audio_segs.append(ec_a)
            else:
                ec_a = str(workdir / "scenes" / "endcard_a.m4a")
                run(["ffmpeg", "-y", "-f", "lavfi", "-i",
                     f"anullsrc=r=44100:cl=stereo:d={ec.get('duration_s', 4)}",
                     "-t", str(ec.get("duration_s", 4)),
                     "-c:a", "aac", "-b:a", "128k", ec_a])
                audio_segs.append(ec_a)

        # 6. concat + final phone-safe encode
        v_all = str(workdir / "video_all.mp4")
        a_all = str(workdir / "audio_all.m4a")
        concat_files(scene_mp4s, str(workdir / "vlist.txt"), v_all, is_video=True)
        concat_files(audio_segs, str(workdir / "alist.txt"), a_all, is_video=False)

        final_mp4 = str(outdir / f"viraldesk_p{job.prompt_id}_v{job.prompt_version}_{self.name}.mp4")
        run(["ffmpeg", "-y", "-i", v_all, "-i", a_all,
             "-c:v", "libx264", "-profile:v", "baseline", "-level", "3.0",
             "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "20",
             "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
             "-movflags", "+faststart", "-shortest", final_mp4])

        caption_path = str(outdir / f"viraldesk_p{job.prompt_id}_v{job.prompt_version}_caption.txt")
        Path(caption_path).write_text(job.caption or "", encoding="utf-8")

        # 7. verify against the output contract — never declare success otherwise
        verified = verify_output(final_mp4)
        if not verified["ok"]:
            raise RuntimeError(f"Output contract FAILED: {verified['checks']}")
        notes.append(f"ffprobe verification passed: {verified['checks']}")

        elapsed = round(time.time() - t0, 1)
        notes.append(f"engine wall-clock: {elapsed}s (keyframes excluded — generated agent-side)")
        return FinalVideo(
            video_path=final_mp4,
            caption_path=caption_path,
            duration_s=verified["duration_s"],
            size_bytes=os.path.getsize(final_mp4),
            engine=self.name,
            verified=verified,
            notes=notes,
        )
