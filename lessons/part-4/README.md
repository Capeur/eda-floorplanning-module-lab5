# Lab 05 · Part 4 animated lesson: Too wide: turn a block (EN + FR)

Animated lesson built with the `lesson-animator` skill (floorplan scene). The lesson page sits next to video
part 4 and does not replace it. Same layout, colours and pacing as Parts 1-3 (`lessons/part-1/` to `lessons/part-3/`).

## Inputs
| Input | Value |
|---|---|
| Teacher clone | `../eda-learning-lab5-fp` (read only) |
| EN transcript | `../eda-learning-lab5-fp/courses/learn_floorplanning/module02-03-bstar-tree/transcript.md` |
| FR transcript | `i18n/fr/module02-03-bstar-tree/transcript.md` |
| Slides | transcript slides 20-24: 18 sentences in English, 19 in French (FR splits the last question in two) |
| Lesson plan | module `UPGRADE_NOTES.md` §12, "Part 4 — Too wide: turn a block" |
| Lab data | `bstar_check.py --json` → `build/lessons/bstar-check.json` (made in Part 1; outline 10 × 8, blocks A-E, 11 named trees) |
| Voices | EN `en-US-AndrewMultilingualNeural`, FR `fr-FR-RemyMultilingualNeural`, `--rate=-4%`, cache `.cache/voice` |
| Output | `docs/lessons/part-4/` and `docs/fr/lessons/part-4/` (`--fonts site_src/fonts --storage-key lab05-lesson-speed`) |

## Scenes (anchor words EN / FR)
Starts where Part 3 stopped: the chain `rotate_start` (every child a left child), no block placed, "next door"
labels on every link. The first move (the drops) is keyed on the first *three / trois* of sentence 20.2.

| Slide | Scene | Main changes |
|---|---|---|
| 20 | Answer to Part 3: it does not fit | A, B, C, D drop 0.55 s apart from *three / trois*; counter "row width" counts 3, 5, 7, 10 (green); equation 3 + 2 + 2 + 3 = 10 built on *three, two, two, three, ten / trois, deux, deux, trois, dix*; E ringed on *waiting / attend* |
| 21 | Sticking out | E drops on *lands / arrive* to (10, 0): the zone outside the outline is hatched red, width 12 (red); badge "sticks out of the 10 × 8 outline" on *sticks / dépasse*; "Legal / Valide" term card on *legal / valide*; stamp "not legal / pas valide" on *not legal / pas valide* |
| 22 | The only way to fail | tree faded; tags "✓ never overlap" on *overlap / chevauchent*, "✗ sticking out" on *sticking / dépasser*; amber skyline on *skyline / horizon* |
| 23 | Turn a block | dims in every block; "Turn / Rotation" term card on *turn / tourner*; D ringed on *side / côté*; tree becomes `rotate_after` on *Turn D / tournez*: D turns 90° (3 × 1 → 1 × 3), E slides to x = 8, width 12 → 10 (green), badge turns to "fits the 10 × 8 outline" |
| 24 | Three small changes + pause and guess | tree back to `golden`; card Turn / Swap / Move built on *three, swap, leaf / trois, échanger, feuille*; A and C ringed on *swap*, leaf E on *leaf / feuille*; bounding box on *floorplan / plan*, counter "box area" 27 on *score*; question card "Can any tree beat 27 squares? What is the smallest box?" (no / down to 23 / 24), auto-pause |

Departures from the §12 plan: no ghost E outside the outline in 20.3 (E is ringed in the tree instead); the turn
happens on *Turn D* (23.2), not on the first *turn* (23.1), which gets the term card; E slides with the turn
instead of in 23.3; 24.2 rings A and C instead of showing golden/lift thumbnails; 24.3 rings the leaf E with no
arrow; the score counter does not flicker. The block dims are hidden from the turn on: the engine draws a
turned block as its unturned rectangle rotated 90°, so its dims label would still read "3×1" (the headline says
"D: 3 × 1 → 1 × 3"). Every reply of the question gives the answer (yes, 6 × 4 = 24 with 1 wasted square),
which Part 5 then shows. "Many trees beat 27" is from the checker's stats (216 legal trees below 27), which the
engine cannot check, so no count is shown.

## Claims (checked by the engine)
`rotate_start`: walk ABCDE; widths 3, 2, 2, 3, 2, D 1 tall; D (7, 0), E (10, 0); box 12 × 3; does not fit.
`rotate_after` (D turned): D 1 wide and 3 tall at (7, 0), E (8, 0); box 10 × 3; fits.
`golden`: box 9 × 3 = 27, 4 wasted (23 covered, the hint's number); legal.
`best`: box 6 × 4 = 24, 1 wasted; legal (the question's answer).

## Commands (from the site repo; PYTHONDONTWRITEBYTECODE=1, PY=~/eda-venv/bin/python)
```bash
PY=~/eda-venv/bin/python; SK=~/.claude/skills/lesson-animator; CL=../eda-learning-lab5-fp; SB=lessons/part-4/storyboard.json
TR_en=$CL/courses/learn_floorplanning/module02-03-bstar-tree/transcript.md
TR_fr=i18n/fr/module02-03-bstar-tree/transcript.md

# draft (silent, estimated words): draft_timing + build for en and fr, then check_lesson.py
bash build/lessons/part-4/draft.sh

# voice (run in your own terminal; finished sentences are cached in .cache/voice)
$PY $SK/scripts/voice_build.py --transcript $TR_en --slides 20-24 --lang en --voice en-US-AndrewMultilingualNeural \
    --rate=-4% --storyboard $SB --repo $CL --workdir .cache/voice \
    --out-audio build/lessons/part-4/lesson-en.m4a --out-timing build/lessons/part-4/timing-en.json
$PY $SK/scripts/voice_build.py --transcript $TR_fr --slides 20-24 --lang fr --voice fr-FR-RemyMultilingualNeural \
    --rate=-4% --storyboard $SB --repo $CL --workdir .cache/voice \
    --out-audio build/lessons/part-4/lesson-fr.m4a --out-timing build/lessons/part-4/timing-fr.json

# build + check
$PY $SK/scripts/build_lesson.py --storyboard $SB --timing build/lessons/part-4/timing-en.json \
    --audio build/lessons/part-4/lesson-en.m4a --lang en --out docs/lessons/part-4 --fonts site_src/fonts \
    --storage-key lab05-lesson-speed --data build/lessons/bstar-check.json
$PY $SK/scripts/build_lesson.py --storyboard $SB --timing build/lessons/part-4/timing-fr.json \
    --audio build/lessons/part-4/lesson-fr.m4a --lang fr --out docs/fr/lessons/part-4 --fonts site_src/fonts \
    --storage-key lab05-lesson-speed --data build/lessons/bstar-check.json
$PY $SK/scripts/check_lesson.py docs/lessons/part-4/index.html docs/fr/lessons/part-4/index.html --sheets build/lessons/part-4/check
```

## Results
- Draft (2026-11-02, silent audio, estimated words): claims 4/4; 11 checker trees re-packed, all equal;
  0 errors, 0 warnings in EN and FR. EN about 80 s (18 sentences, 16.5 s of pauses), FR about 93 s
  (19 sentences, 17.8 s of pauses). Script per frame on a CPU slowed 6×: median 1.0 ms, 95 % under 1.9 ms.
  Contact sheets: `build/lessons/part-4/draft/check/sheet-{en,fr}.png`.
- Voice build (2026-11-02, words exact): EN 90.3 s, FR 87.0 s; claims 4/4; 11 checker trees all equal;
  0 errors, 0 warnings in EN and FR. The first move (A drops on *three / trois*) comes 4.5 s (EN) / 4.1 s (FR) in.
  Contact sheets: `build/lessons/part-4/check/sheet-{en,fr}.png`.
- Site: `~/eda-venv/bin/python build_site.py --repo ../eda-learning-lab5-fp` links "Interactive lesson" /
  "Leçon interactive" under video parts 1-4. `tools/test_site.py` (with `python3 -m http.server 8090
  --bind 127.0.0.1 --directory docs` running): 233 checks, 0 failed, including the 6 lesson-part-4 checks in each
  language (log: `build/lessons/part-4/test_site.log`).
