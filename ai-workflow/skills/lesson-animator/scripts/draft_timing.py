#!/usr/bin/env python3
"""Draft timing: write and check a storyboard BEFORE any voice exists (right after the script is written).

Word times are estimated from the text at a normal reading pace (about 2.6 words a second in English, a little
slower in French), the designed pauses are added (lessonlib.pause_plan), and the audio is silence of the same length.
The page plays, seeks and checks exactly like the real one; only the voice is missing. Replace it later with
voice_build.py (new voice, exact word times) or timing_from_vtt.py (the site's narration): the storyboard does not change.

  python3 draft_timing.py --transcript courses/<course>/<module>/transcript.md --slides 1-6 --lang en \
      --storyboard lessons/part-1/storyboard.json --repo <teacher clone> \
      --out-audio build/lessons/part-1/draft-en.m4a --out-timing build/lessons/part-1/draft-timing-en.json
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lessonlib import load_json, parse_range, pause_plan, slide_sentences  # noqa: E402

# seconds per character and per word, measured on the course voices at their default rate (rough on purpose)
PACE = {"en": (0.058, 0.07), "fr": (0.060, 0.075)}


def estimate(text: str, lang: str) -> tuple[list[dict], float]:
    per_char, per_word = PACE.get(lang, PACE["en"])
    t, words = 0.0, []
    for w in text.split():
        words.append({"w": w, "t": round(t, 3)})
        t += per_word + per_char * len(w)
        if w[-1:] in ",;:":
            t += 0.18
    return words, t


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--transcript", required=True, type=Path)
    ap.add_argument("--slides", required=True, help="transcript slide range of this part, e.g. 1-6")
    ap.add_argument("--lang", required=True)
    ap.add_argument("--storyboard", type=Path, help="for pause rules (pausing, pauses)")
    ap.add_argument("--repo", type=Path, help="teacher clone, to use its exact speech cleaner")
    ap.add_argument("--out-audio", required=True, type=Path)
    ap.add_argument("--out-timing", required=True, type=Path)
    a = ap.parse_args()

    first, last = parse_range(a.slides)
    sents = slide_sentences(a.transcript, first, last, a.repo)
    sb = load_json(a.storyboard) if a.storyboard else None
    gaps = pause_plan(sents, sb, a.lang)
    t, timing = 0.25, []
    for s, g in zip(sents, gaps):
        ws, d = estimate(s["text"], a.lang)
        timing.append({"slide": s["slide"], "text": s["text"], "start": round(t, 3), "end": round(t + d, 3), "pause_after": g,
                       "words": [{"w": w["w"], "t": round(t + w["t"], 3)} for w in ws]})
        t += d + g
    total = round(t, 3)
    a.out_audio.parent.mkdir(parents=True, exist_ok=True)
    a.out_timing.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", f"{total:.3f}",
                    "-c:a", "aac", "-b:a", "32k", str(a.out_audio)], check=True)
    out = {"lang": a.lang, "slides": [first, last], "source": "draft", "words": "estimated",
           "duration": total, "sentences": timing}
    a.out_timing.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{a.lang}: {len(sents)} sentences, about {total:.1f} s with {sum(gaps):.1f} s of pauses (draft: silent audio, estimated words)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
