# Lab 05 · Part 3 animated lesson: The skyline and the score (EN + FR)

Animated lesson built with the `lesson-animator` skill (floorplan scene). The lesson page sits next to video
part 3 and does not replace it. Same layout, colours and pacing as Parts 1 and 2 (`lessons/part-1/`, `lessons/part-2/`).

## Inputs
| Input | Value |
|---|---|
| Teacher clone | `../eda-learning-lab5-fp` (read only) |
| EN transcript | `../eda-learning-lab5-fp/courses/learn_floorplanning/module02-03-bstar-tree/transcript.md` |
| FR transcript | `i18n/fr/module02-03-bstar-tree/transcript.md` |
| Slides | transcript slides 13-19, 20 sentences in each language |
| Lesson plan | module `UPGRADE_NOTES.md` §12, "Part 3 — The skyline and the score" |
| Lab data | `bstar_check.py --json` → `build/lessons/bstar-check.json` (made in Part 1; outline 10 × 8, blocks A-E, 11 named trees) |
| Voices | EN `en-US-AndrewMultilingualNeural`, FR `fr-FR-RemyMultilingualNeural`, `--rate=-4%`, cache `.cache/voice` |
| Output | `docs/lessons/part-3/` and `docs/fr/lessons/part-3/` (`--fonts site_src/fonts --storage-key lab05-lesson-speed`) |

## Scenes (anchor words EN / FR)
Starts where Part 2 stopped: `golden` tree, all five blocks placed. The first move (the swap) is keyed on
*swapped / échangés* in sentence 13.2, several seconds into the audio.

| Slide | Scene | Main changes |
|---|---|---|
| 13 | Answer to Part 2: one square higher | D ringed with its (0, 2) on the golden floor; "y = 2 → y = 3" on *higher / haut*; tree becomes `lift` and the floor empties on *swapped / échangés*; C ringed on *root / racine*, A on *takes / prend*; C, B, A, E drop 0.55 s apart on *C, B*, with "next door" link labels |
| 14 | The skyline | tree faded; zoom on the floor on *city / ville*; amber skyline and the "Skyline" term card on *skyline / horizon*; D flies out and falls onto the skyline on *drops / tombe* |
| 15 | Why D stops at 3 | dims in every block; C and B ringed on *hangs / passe*; B and D on *tall / haut*; counter "y of D" = 3 and (0, 3) on *stops / arrête*; C ringed and "a hole of 2 empty squares above C" on *hole / trou* |
| 16 | The bounding box | zoom out, tree back to `golden`; thumbnails "first tree" / "swapped tree" on the empty top of the floor; bounding box and "Bounding box" term card on *bounding / boîte*; counter "box area" 27 on *twenty / vingt* |
| 17 | Wasted space | all five blocks ringed on *cover / couvrent*; equation 23 covered + 4 empty = 27 built on *twenty, four, wasted / vingt, quatre, perdues*; the 4 holes hatched on *empty / vides*; counter "wasted squares" 4 (green) on *fewer / moins* |
| 18 | One swap, a new score | tree back to `lift` with the box and hatch on: counter counts 4 → 13 (red); "9 × 4 = 36", "13 wasted" on *thirty, thirteen / trente, treize*; A and C ringed on *swap / échange*; thumbnails 9 × 3 = 27 and 9 × 4 = 36 on *twenty / vingt*, the first marked "better / meilleur" on *better / meilleur* |
| 19 | Pause and guess | tree becomes the chain `rotate_start`, floor empty (only the outline), "next door" labels on every link from *left / gauche*; question card "Every child is a left child: does this long row fit inside the outline?" (yes / no, it sticks out / exactly), auto-pause |

Departures from the §12 plan: the engine has no ghost block or silhouette, so 14.1 is a zoom on the floor (tree
faded) and D falls once, on *drops / tombe* (14.3), instead of hanging at the top until 15.2; slide 15 then
explains the landing (rings, "y of D", hole tag). The hole is a tag, not a hatch: the `wasted` hatch shows every
wasted square of the box, which is the point of slides 17-18. 18.2 rings A and C instead of toggling the two trees.
The chain in 19.1 is drawn with no block placed (placing it would answer the question). Every reply of the
question gives the answer (12 wide, the outline is 10, E sticks out), which Part 4 then shows block by block.

## Claims (checked by the engine)
`golden`: D (0, 2); box 9 × 3 = 27, 4 wasted (so 23 covered); legal.
`lift`: walk CBAED; C (0, 0), D (0, 3); D 3 wide, B 3 tall at x = 2, C 2 tall (the 2-square hole above C);
box 9 × 4 = 36, 13 wasted; legal.
`rotate_start` (the chain): walk ABCDE; widths 3, 2, 2, 3, 2; E at x = 10; box 12 × 3; does not fit (the question's answer).

## Commands (from the site repo; PYTHONDONTWRITEBYTECODE=1, PY=~/eda-venv/bin/python)
```bash
PY=~/eda-venv/bin/python; SK=~/.claude/skills/lesson-animator; CL=../eda-learning-lab5-fp; SB=lessons/part-3/storyboard.json
TR_en=$CL/courses/learn_floorplanning/module02-03-bstar-tree/transcript.md
TR_fr=i18n/fr/module02-03-bstar-tree/transcript.md

# draft (silent, estimated words): draft_timing + build for en and fr, then check_lesson.py
bash build/lessons/part-3/draft.sh

# voice (run in your own terminal; finished sentences are cached in .cache/voice)
$PY $SK/scripts/voice_build.py --transcript $TR_en --slides 13-19 --lang en --voice en-US-AndrewMultilingualNeural \
    --rate=-4% --storyboard $SB --repo $CL --workdir .cache/voice \
    --out-audio build/lessons/part-3/lesson-en.m4a --out-timing build/lessons/part-3/timing-en.json
$PY $SK/scripts/voice_build.py --transcript $TR_fr --slides 13-19 --lang fr --voice fr-FR-RemyMultilingualNeural \
    --rate=-4% --storyboard $SB --repo $CL --workdir .cache/voice \
    --out-audio build/lessons/part-3/lesson-fr.m4a --out-timing build/lessons/part-3/timing-fr.json

# build + check
$PY $SK/scripts/build_lesson.py --storyboard $SB --timing build/lessons/part-3/timing-en.json \
    --audio build/lessons/part-3/lesson-en.m4a --lang en --out docs/lessons/part-3 --fonts site_src/fonts \
    --storage-key lab05-lesson-speed --data build/lessons/bstar-check.json
$PY $SK/scripts/build_lesson.py --storyboard $SB --timing build/lessons/part-3/timing-fr.json \
    --audio build/lessons/part-3/lesson-fr.m4a --lang fr --out docs/fr/lessons/part-3 --fonts site_src/fonts \
    --storage-key lab05-lesson-speed --data build/lessons/bstar-check.json
$PY $SK/scripts/check_lesson.py docs/lessons/part-3/index.html docs/fr/lessons/part-3/index.html --sheets build/lessons/part-3/check
```

## Results
- Draft (2026-11-02, silent audio, estimated words): claims 3/3; 11 checker trees re-packed, all equal;
  0 errors, 0 warnings in EN and FR. EN about 94 s, FR about 108 s (20 sentences each, 19.2 s of pauses).
  Script per frame on a CPU slowed 6×: median 1.1 ms, 95 % under 2.1 ms.
  Contact sheets: `build/lessons/part-3/draft/check/sheet-{en,fr}.png`.
- Voice build (2026-11-02, words exact): EN 108.0 s, FR 101.2 s; claims 3/3; 11 checker trees all equal;
  0 errors, 0 warnings in EN and FR. The first move (the swap, on *swapped / échangés*) comes about 3 s in.
  Contact sheets: `build/lessons/part-3/check/sheet-{en,fr}.png`.
- Site: `~/eda-venv/bin/python build_site.py --repo ../eda-learning-lab5-fp` links "Interactive lesson" /
  "Leçon interactive" under video parts 1, 2 and 3. `tools/test_site.py` (with `python3 -m http.server 8090
  --bind 127.0.0.1 --directory docs` running): 221 checks, 0 failed, including the 6 lesson-part-3 checks in each
  language (log: `build/lessons/part-3/test_site.log`).
