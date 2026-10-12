#!/usr/bin/env python3
"""
ViralDesk Phase 2 — Preview Studio pipeline.

Master-prompt scene spec (JSON) IN  -->  watchable preview MP4 + burned-in
captions + AI voiceover OUT. No manual steps between.

Usage:
    python3 preview_studio.py scenes.json --out previews/<name>.mp4

Scene spec format:
{
  "title": "run title",
  "logo": "/path/to/logo_transparent.png",
  "brand": {"name": "...", "qualification": "...", "phone": "...",
            "addr1": "...", "addr2": "..."},
  "scenes": [
    {"image": "assets/scene1.webp", "headline": "...", "sub": "...",
     "vo": "assets/vo1.mp3", "motion": "zoom_in|zoom_out|pan_right|static"},
    ...
    {"image": "assets/scene6.webp", "endcard": true,
     "vo": "assets/vo6.mp3", "motion": "static"}
  ]
}

Notes:
- Voiceover is AI TTS for PREVIEWS ONLY. Final production uses the owner's
  real recorded voice. This is logged, never hidden.
- No AI video generation anywhere: stills + Ken Burns motion only.
- Final encode: H.264 baseline profile, yuv420p, AAC, faststart.
  (H.264 level 3.0 cannot hold 1080p, so x264 picks the needed level
  automatically; profile baseline is what guarantees phone compatibility.)
"""

import argparse
import json
import math
import os
import subprocess
import sys
import time

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FPS = 30

FONT_HEAD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_BODY = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
FONT_URDU = "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Bold.ttf"


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(cmd)}\n{r.stderr[-2000:]}")
    return r


def audio_duration(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", path])
    return float(r.stdout.strip())


def wrap_text(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def composite_scene(base_path, scene, logo_path, brand, out_path):
    """Base still -> 1080x1920 with logo, scrim, burned-in text (or end card)."""
    img = Image.open(base_path).convert("RGB")
    # cover-resize to 1080x1920
    scale = max(W / img.width, H / img.height)
    img = img.resize((int(img.width * scale + 0.5), int(img.height * scale + 0.5)),
                     Image.LANCZOS)
    x0 = (img.width - W) // 2
    y0 = (img.height - H) // 2
    img = img.crop((x0, y0, x0 + W, y0 + H))

    draw = ImageDraw.Draw(img, "RGBA")

    if scene.get("endcard"):
        # centered end card
        fh = ImageFont.truetype(FONT_HEAD, 76)
        fb = ImageFont.truetype(FONT_BODY, 52)
        fp = ImageFont.truetype(FONT_HEAD, 64)
        fa = ImageFont.truetype(FONT_BODY, 42)
        lines = [
            (brand["name"], fh, (255, 255, 255)),
            (brand["qualification"], fb, (230, 240, 255)),
            ("", fb, (255, 255, 255)),
            (brand["phone"], fp, (255, 210, 60)),
            ("", fb, (255, 255, 255)),
            (brand["addr1"], fa, (235, 235, 235)),
            (brand["addr2"], fa, (235, 235, 235)),
        ]
        y = 640
        for text, font, color in lines:
            if not text:
                y += 24
                continue
            tw = draw.textlength(text, font=font)
            draw.text(((W - tw) / 2, y), text, font=font, fill=color,
                      stroke_width=2, stroke_fill=(20, 30, 60))
            y += font.size + 22
    else:
        # bottom scrim for legibility
        scrim_h = int(H * 0.42)
        for yy in range(scrim_h):
            a = int(165 * (yy / scrim_h) ** 1.4)
            draw.rectangle([0, H - scrim_h + yy, W, H - scrim_h + yy + 1],
                           fill=(8, 14, 34, a))
        fh = ImageFont.truetype(FONT_HEAD, 66)
        fs = ImageFont.truetype(FONT_BODY, 46)
        max_w = W - 140
        head_lines = wrap_text(draw, scene["headline"], fh, max_w)
        sub_lines = wrap_text(draw, scene.get("sub", ""), fs, max_w)
        block_h = (len(head_lines) * (66 + 14) + len(sub_lines) * (46 + 12))
        y = H - 300 - block_h
        for ln in head_lines:
            tw = draw.textlength(ln, font=fh)
            draw.text(((W - tw) / 2, y), ln, font=fh, fill=(255, 255, 255),
                      stroke_width=3, stroke_fill=(10, 16, 40))
            y += 66 + 14
        y += 6
        for ln in sub_lines:
            tw = draw.textlength(ln, font=fs)
            draw.text(((W - tw) / 2, y), ln, font=fs, fill=(255, 224, 120),
                      stroke_width=2, stroke_fill=(10, 16, 40))
            y += 46 + 12

    # logo upper-left (never AI-rendered; composited from the real file)
    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        lw = 210
        lh = int(logo.height * lw / logo.width)
        logo = logo.resize((lw, lh), Image.LANCZOS)
        img.paste(logo, (44, 44), logo)

    img.save(out_path)
    return out_path


def kenburns(png_path, dur, motion, out_path):
    D = max(2, int(round(dur * FPS)))
    if motion == "zoom_out":
        z, x, y = (f"max(1.10-0.10*on/{D},1.0)",
                   "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)")
    elif motion == "pan_right":
        z, x, y = ("1.08", f"(iw-iw/zoom)*on/{D}", "ih/2-(ih/zoom/2)")
    elif motion == "static":
        z, x, y = (f"1+0.03*on/{D}",
                   "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)")
    else:  # zoom_in
        z, x, y = (f"min(1+0.10*on/{D},1.10)",
                   "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)")
    vf = (f"scale=2160:3840,zoompan=z='{z}':x='{x}':y='{y}'"
          f":d={D}:s={W}x{H}:fps={FPS}")
    run(["ffmpeg", "-y", "-loop", "1", "-framerate", str(FPS), "-i", png_path,
         "-vf", vf, "-frames:v", str(D),
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
         "-pix_fmt", "yuv420p", "-an", out_path])


def mux_av(video, audio, out_path):
    run(["ffmpeg", "-y", "-i", video, "-i", audio,
         "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
         "-shortest", out_path])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--out", required=True)
    ap.add_argument("--workdir", default="/tmp/viraldesk_preview")
    args = ap.parse_args()

    t_all = time.time()
    timings = {}
    base = os.path.dirname(os.path.abspath(args.spec))
    spec = json.load(open(args.spec))
    os.makedirs(args.workdir, exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)

    logo = spec.get("logo")
    if logo and not os.path.isabs(logo):
        logo = os.path.join(base, logo)
    brand = spec.get("brand", {})

    # 1. composite stills (logo + burned-in text)
    t = time.time()
    pngs, durs = [], []
    for i, sc in enumerate(spec["scenes"]):
        ip = sc["image"] if os.path.isabs(sc["image"]) else os.path.join(base, sc["image"])
        png = os.path.join(args.workdir, f"scene_final_{i}.png")
        composite_scene(ip, sc, logo, brand, png)
        pngs.append(png)
        vp = sc["vo"] if os.path.isabs(sc["vo"]) else os.path.join(base, sc["vo"])
        durs.append(audio_duration(vp) + 0.6)  # 0.6s tail pad
    timings["composite_stills"] = round(time.time() - t, 1)

    # 2. Ken Burns per scene
    t = time.time()
    kbs = []
    for i, (png, dur, sc) in enumerate(zip(pngs, durs, spec["scenes"])):
        kb = os.path.join(args.workdir, f"kb_{i}.mp4")
        kenburns(png, dur, sc.get("motion", "zoom_in"), kb)
        kbs.append(kb)
    timings["kenburns"] = round(time.time() - t, 1)

    # 3. mux voiceover per scene
    t = time.time()
    segs = []
    for i, (kb, sc) in enumerate(zip(kbs, spec["scenes"])):
        vp = sc["vo"] if os.path.isabs(sc["vo"]) else os.path.join(base, sc["vo"])
        seg = os.path.join(args.workdir, f"seg_{i}.mp4")
        mux_av(kb, vp, seg)
        segs.append(seg)
    timings["mux_audio"] = round(time.time() - t, 1)

    # 4. concat + final phone-safe encode
    t = time.time()
    lst = os.path.join(args.workdir, "concat.txt")
    with open(lst, "w") as f:
        for s in segs:
            f.write(f"file '{s}'\n")
    joined = os.path.join(args.workdir, "joined.mp4")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst,
         "-c", "copy", joined])
    run(["ffmpeg", "-y", "-i", joined,
         "-c:v", "libx264", "-profile:v", "baseline", "-pix_fmt", "yuv420p",
         "-crf", "23", "-preset", "medium",
         "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
         "-movflags", "+faststart", args.out])
    timings["concat_encode"] = round(time.time() - t, 1)

    size_mb = os.path.getsize(args.out) / 1e6
    if size_mb > 25:  # WhatsApp safety: re-encode smaller
        t = time.time()
        run(["ffmpeg", "-y", "-i", joined,
             "-c:v", "libx264", "-profile:v", "baseline", "-pix_fmt", "yuv420p",
             "-crf", "30", "-preset", "medium", "-vf", "scale=720:1280",
             "-c:a", "aac", "-b:a", "96k", "-ar", "44100",
             "-movflags", "+faststart", args.out])
        size_mb = os.path.getsize(args.out) / 1e6
        timings["size_retry"] = round(time.time() - t, 1)

    total_dur = sum(durs)
    timings["total_pipeline"] = round(time.time() - t_all, 1)
    print(json.dumps({
        "ok": True,
        "out": args.out,
        "size_mb": round(size_mb, 2),
        "video_secs": round(total_dur, 1),
        "scenes": len(segs),
        "timings_secs": timings,
    }, indent=2))


if __name__ == "__main__":
    main()
