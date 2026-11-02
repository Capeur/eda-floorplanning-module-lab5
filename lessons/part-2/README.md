# Lab 05 · Part 2 animated lesson: Walking the tree (EN + FR)

Animated lesson built with the `lesson-animator` skill (floorplan scene). The lesson page sits next to video
part 2 and does not replace it. Same layout, colours and pacing as Part 1 (`lessons/part-1/`).

## Inputs
| Input | Value |
|---|---|
| Teacher clone | `../eda-learning-lab5-fp` (read only) |
| EN transcript | `../eda-learning-lab5-fp/courses/learn_floorplanning/module02-03-bstar-tree/transcript.md` |
| FR transcript | `i18n/fr/module02-03-bstar-tree/transcript.md` |
| Slides | transcript slides 8-12 (= PDF pages 8-12), 13 sentences in each language |
| Lesson plan | module `UPGRADE_NOTES.md` §12, "Part 2 — Walking the tree" |
| Lab data | `bstar_check.py --json` → `build/lessons/bstar-check.json` (made in Part 1; outline 10 × 8, blocks A-E, 11 named trees) |
| Voices | EN `en-US-AndrewMultilingualNeural`, FR `fr-FR-RemyMultilingualNeural`, `--rate=-4%`, cache `.cache/voice` |
| Output | `docs/lessons/part-2/` and `docs/fr/lessons/part-2/` (`--fonts site_src/fonts --storage-key lab05-lesson-speed`) |

## Scenes (anchor words EN / FR)
Starts where Part 1 stopped: `golden` tree, A placed at (0, 0), link labels on.

| Slide | Scene | Main changes |
|---|---|---|
| 8 | B goes next door (answers Part 1) | B flies out of its node and lands on *next door / côté*, ringed; headline "x = 3" on *three / trois*, "= 0 + 3" on *wide / large*, "y = 0" on *floor / sol*; counter x of B (3), then y of B (0); "(3, 0)" |
| 9 | The walk order | floor faded; "Walk order" card on *walk / parcours*; rings: A (*node / nœud*) → B, C, E (*left / gauche*) → D (*right / droit*); walk badges 1-5 on *goes / donne* |
| 10 | C and E | floor back; C on *next door / côté* (counter x of C = 5), E on *lands / arrive* (x of E = 7); dims in each block and A, B, C ringed from *three / trois*; equation 3 + 2 + 2 = 7 built on *three, plus, plus, makes / trois, plus, plus, font* |
| 11 | D goes upstairs | D ringed on *back / revient*, A ringed on *like / comme* ("x = 0, like A"); D drops onto A on *top / pose*; counter y of D = 2; "(0, 2)" |
| 12 | Pause and guess | counter "blocks placed" 5 on *placed / placés*; "fits the 10 × 8 outline" badge on *outline / contour*; A and C ringed on *swap / échange*; tree faded; question card "Swap A and C: does D still land at y = 2?" (yes / higher / lower), auto-pause |

Departures from the §12 plan: the engine has no ghost block, so D drops on *top / pose* (sentence 11.3) and
sentence 11.2 only rings D and A. The walk "path" is the walk badges 1-5 plus the rings of 9.2. The outline does
not flash green; the legal badge says it fits. Every reply of the question gives the answer (D lands at y = 3,
one square higher), which Part 3 then shows.

## Claims (checked by the engine)
`golden`: walk ABCED; A (0, 0), B (3, 0), C (5, 0), E (7, 0), D (0, 2); A 3 wide and 2 tall, B and C 2 wide; legal.
`lift` (golden with A and C swapped): D at (0, 3), B 3 tall (the question's answer).

## Commands (from the site repo; PYTHONDONTWRITEBYTECODE=1, PY=~/eda-venv/bin/python)
```bash
PY=~/eda-venv/bin/python; SK=~/.claude/skills/lesson-animator; CL=../eda-learning-lab5-fp; SB=lessons/part-2/storyboard.json
TR_en=$CL/courses/learn_floorplanning/module02-03-bstar-tree/transcript.md
TR_fr=i18n/fr/module02-03-bstar-tree/transcript.md
# only if missing:
$PY $CL/courses/learn_floorplanning/module02-03-bstar-tree/examples/bstar_check.py --json > build/lessons/bstar-check.json

# draft (silent, estimated words): build/lessons/part-2/draft.sh does draft_timing + build for en and fr, then check_lesson.py
bash build/lessons/part-2/draft.sh

# voice (run in your own terminal; finished sentences are cached in .cache/voice)
$PY $SK/scripts/voice_build.py --transcript $TR_en --slides 8-12 --lang en --voice en-US-AndrewMultilingualNeural \
    --rate=-4% --storyboard $SB --repo $CL --workdir .cache/voice \
    --out-audio build/lessons/part-2/lesson-en.m4a --out-timing build/lessons/part-2/timing-en.json
$PY $SK/scripts/voice_build.py --transcript $TR_fr --slides 8-12 --lang fr --voice fr-FR-RemyMultilingualNeural \
    --rate=-4% --storyboard $SB --repo $CL --workdir .cache/voice \
    --out-audio build/lessons/part-2/lesson-fr.m4a --out-timing build/lessons/part-2/timing-fr.json

# build + check
$PY $SK/scripts/build_lesson.py --storyboard $SB --timing build/lessons/part-2/timing-en.json \
    --audio build/lessons/part-2/lesson-en.m4a --lang en --out docs/lessons/part-2 --fonts site_src/fonts \
    --storage-key lab05-lesson-speed --data build/lessons/bstar-check.json
$PY $SK/scripts/build_lesson.py --storyboard $SB --timing build/lessons/part-2/timing-fr.json \
    --audio build/lessons/part-2/lesson-fr.m4a --lang fr --out docs/fr/lessons/part-2 --fonts site_src/fonts \
    --storage-key lab05-lesson-speed --data build/lessons/bstar-check.json
$PY $SK/scripts/check_lesson.py docs/lessons/part-2/index.html docs/fr/lessons/part-2/index.html --sheets build/lessons/part-2/check
```

## Results
- Draft (2026-11-02, silent audio, estimated words): claims 2/2; 11 checker trees re-packed, all equal;
  0 errors, 0 warnings in EN and FR. EN about 68 s, FR about 73 s (13 sentences each, 12.2 s of pauses).
  Script per frame on a CPU slowed 6×: median 0.9 ms, 95 % under 1.8 ms.
  Contact sheets: `build/lessons/part-2/draft/check/sheet-{en,fr}.png`.
- Voice build (2026-11-02, words exact): EN 79.5 s, FR 72.8 s; claims 2/2; 11 checker trees all equal;
  0 errors, 0 warnings in EN and FR. In English "next door" is said 0.35 s into the audio, so B drops at
  `@next8+0.3` (the starting state needs 0.55 s). Contact sheets: `build/lessons/part-2/check/sheet-{en,fr}.png`.
- Site: `~/eda-venv/bin/python build_site.py --repo ../eda-learning-lab5-fp` links "Interactive lesson" /
  "Leçon interactive" under video parts 1 and 2. `tools/test_site.py` (with `python3 -m http.server 8090
  --bind 127.0.0.1 --directory docs` running): 209 checks, 0 failed, including the 6 lesson-part-2 checks in each
  language (log: `build/lessons/part-2/test_site.log`).
