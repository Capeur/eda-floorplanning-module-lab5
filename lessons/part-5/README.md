# Lab 05 · Part 5 animated lesson: The tightest floorplan, your turn (EN + FR)

Animated lesson built with the `lesson-animator` skill (v4.1, floorplan scene). The lesson page sits next to video
part 5 and does not replace it. Same layout, colours and pacing as Parts 1-4 (`lessons/part-1/` to `lessons/part-4/`).
This is the last part: its question card gives the answer itself (there is no part 6).

## Inputs
| Input | Value |
|---|---|
| Teacher clone | `../eda-learning-lab5-fp` (read only) |
| EN transcript | `../eda-learning-lab5-fp/courses/learn_floorplanning/module02-03-bstar-tree/transcript.md` |
| FR transcript | `i18n/fr/module02-03-bstar-tree/transcript.md` |
| Slides | transcript slides 25-31 (PDF pages 25-32; transcript slide 29 = PDF pages 29-30, the bash code is PDF page 30): 29 sentences in English, 30 in French (FR splits the first sentence in two) |
| Lesson plan | module `UPGRADE_NOTES.md` §12, "Part 5 — The tightest floorplan, your turn", and §13 "Part 5 answers its own closing question" |
| Lab data | `bstar_check.py --json` → `build/lessons/bstar-check.json` (made in Part 1; outline 10 × 8, blocks A-E, 11 named trees) |
| Voices | EN `en-US-AndrewMultilingualNeural`, FR `fr-FR-RemyMultilingualNeural`, `--rate=-4%`, cache `.cache/voice` |
| Output | `docs/lessons/part-5/` and `docs/fr/lessons/part-5/` (`--fonts site_src/fonts --storage-key lab05-lesson-speed`) |

## Scenes (anchor words EN / FR)
Starts where Part 4 stopped: the `golden` tree, every block placed, bounding box 9 × 3 and the "box area" counter at 27.
The first move (the tree becomes `best`) is keyed on *best trees / meilleurs arbres* (sentence 25.2, 7.6 s into the EN draft).

| Slide | Scene | Main changes |
|---|---|---|
| 25 | Answer to Part 4: yes, down to 24 | equation "27 → 24" built on *twenty-seven, twenty-four / vingt-sept, vingt-quatre*; tree becomes `best` with no block placed on *best trees / meilleurs arbres*; A, D, C, E drop 0.55 s apart on *places A / place A* with walk badges ①-④ in step; B ringed on *B comes / B vient* |
| 26 | B is lifted by the skyline | amber skyline on *skyline / horizon*; D ringed on *top of D / haut de D*; B drops onto D on *lands / arrive*, "(4, 1)" on *equals one / égal un*; bounding box 6 × 4 and green counter 24 on *box / boîte*; the one wasted square hatched on *one square / seule case* |
| 27 | Why not 23? | tree faded; tags built on *twenty-three, one square thick, too thick, twenty-four* (FR *vingt-trois, épais, trop épais, vingt-quatre*): "23 squares, nothing wasted?", "= a strip 1 square thick", "✗ B is 2 × 3: too thick", "✓ 24 is the best possible"; B ringed and block sizes shown on *Block B / bloc B* |
| 28 | Browser lab track | blocks taken away at the scene change, then dropped again on *drop / tomber* with the skyline; tree faded on *challenges / défis* with the tag "The challenges check your tree"; thumbnails `lift` "Lift D" on *Lift / Soulevez*, `rotate_after` "Make the row fit" on *row / rangée*; bounding box and counter 24 on the floor on *reach / atteignez* |
| 29 | Python track (PDF page 30 = the code slide) | floor and tree stay; one short tag "Python track: your packer vs the checker" (*Python*, *compares / compare*), no code on the stage; walk badges on *rules / règles*; (x, y) of every block on *answer / réponses* |
| 30 | Remember | grid faded; card "Left child / Right child / Walk" with link labels and walk badges (*next door, upstairs, Walk / côté, étage, Parcourez*); tree faded on *drops / tombe*: card "Drop / Score / Check", skyline, bounding box + wasted square + counter 24, badge "fits the 10 × 8 outline" on *outline / contour* |
| 31 | Your turn + pause and guess (answered) | headline "Your turn" built on *browser, Python, checklist, quiz*; "Sequence pair" term card on *sequence / paire*; question card "Can two lists of names describe our best floorplan, with 24 squares?" with auto-pause after *squares? / vingt-quatre ?*; after the answer, card "Yes: two lists are enough" built on *Yes, sequence, next lab / Oui, paire, prochain lab* |

Departures from the §12 plan: 25.1 shows "27 → 24" as an equation card over the golden picture (no counter tween,
since the counter follows the tree on screen); 27.2 states the one-square-thick strip as a tag instead of drawing a
strip running off the panel; 27.3 rings B and shows the block sizes instead of a bump and a red ✗ on B; 28 shows only
the two challenges that need a different tree (lift, row) as thumbnails; the third ("reach 24") is the floor itself
(bounding box + counter 24); a third thumbnail did not fit without covering block C or running off the stage. 29
shows no terminal or code (as asked): a tag, walk badges and coordinates. 30 uses two recap cards (tree rules over
the faded floor, then floor rules over the faded tree) instead of one icon per line. Every reply of the question gives the answer
(two lists can give exactly this 6 × 4 = 24 floorplan: the sequence pair, next lab), which the voice then says.

## Claims (checked by the engine)
`golden`: D (0, 2); box 9 × 3 = 27, 4 wasted (23 covered); legal.
`best`: walk ADCEB; A (0, 0), D (3, 0), C (0, 2), E (2, 2), B (4, 1); B 2 wide and 3 tall; box 6 × 4 = 24, 1 wasted (23 covered); legal.
`lift`: D (0, 3) (D higher than in `golden`); legal. `rotate_start`: 12 × 3, not legal; `rotate_after`: 10 × 3, legal (the long row made to fit).

Numbers the engine cannot check, checked elsewhere:
- "five thousand and forty trees" (29.4, spoken only, not shown): the checker JSON's `stats.trees` = 5040 (5! orders × 42 tree shapes).
- "twenty-three squares only make a rectangle one square thick": 23 is prime, so the only rectangles are 1 × 23 and 23 × 1.
- "two lists are enough" (31): module notes §12, `common/pack.py pack_sequence_pair` over all 120 × 120 sequence pairs: smallest box 24, and 2 pairs give exactly the `best` pack.

## Commands (from the site repo; PYTHONDONTWRITEBYTECODE=1, PY=~/eda-venv/bin/python)
```bash
PY=~/eda-venv/bin/python; SK=~/.claude/skills/lesson-animator; CL=../eda-learning-lab5-fp; SB=lessons/part-5/storyboard.json
TR_en=$CL/courses/learn_floorplanning/module02-03-bstar-tree/transcript.md
TR_fr=i18n/fr/module02-03-bstar-tree/transcript.md

# draft (silent, estimated words): draft_timing + build for en and fr, then check_lesson.py
bash build/lessons/part-5/draft.sh

# voice (run in your own terminal; finished sentences are cached in .cache/voice)
$PY $SK/scripts/voice_build.py --transcript $TR_en --slides 25-31 --lang en --voice en-US-AndrewMultilingualNeural \
    --rate=-4% --storyboard $SB --repo $CL --workdir .cache/voice \
    --out-audio build/lessons/part-5/lesson-en.m4a --out-timing build/lessons/part-5/timing-en.json
$PY $SK/scripts/voice_build.py --transcript $TR_fr --slides 25-31 --lang fr --voice fr-FR-RemyMultilingualNeural \
    --rate=-4% --storyboard $SB --repo $CL --workdir .cache/voice \
    --out-audio build/lessons/part-5/lesson-fr.m4a --out-timing build/lessons/part-5/timing-fr.json

# build + check
$PY $SK/scripts/build_lesson.py --storyboard $SB --timing build/lessons/part-5/timing-en.json \
    --audio build/lessons/part-5/lesson-en.m4a --lang en --out docs/lessons/part-5 --fonts site_src/fonts \
    --storage-key lab05-lesson-speed --data build/lessons/bstar-check.json
$PY $SK/scripts/build_lesson.py --storyboard $SB --timing build/lessons/part-5/timing-fr.json \
    --audio build/lessons/part-5/lesson-fr.m4a --lang fr --out docs/fr/lessons/part-5 --fonts site_src/fonts \
    --storage-key lab05-lesson-speed --data build/lessons/bstar-check.json
$PY $SK/scripts/check_lesson.py docs/lessons/part-5/index.html docs/fr/lessons/part-5/index.html --sheets build/lessons/part-5/check
```

## Skill fix made for this part
Transcript slide 29 ends with a fenced bash block that holds a blank line. `lessonlib.slide_sentences` split the
slide on blank lines before the speech cleaner removed fences, so half of the code ("```bash # print every correct
answer python3 examples or bstar_check.py --show") was glued to the last spoken sentence and would have been sent to
the voice. `~/.claude/skills/lesson-animator/scripts/lessonlib.py` now drops whole code blocks from a slide before
splitting it. Slides 1-24 give the same sentences as before (checked with a diff).

## Results
- Draft (2026-11-02, silent audio, estimated words): claims 5/5; 11 checker trees re-packed, all equal;
  0 errors, 0 warnings in EN and FR. EN about 134 s (29 sentences, 26.7 s of pauses), FR about 156 s
  (30 sentences, 27.3 s of pauses). Script per frame on a CPU slowed 6×: median 1.0 ms, 95 % under 1.9 ms.
  Contact sheets: `build/lessons/part-5/draft/check/sheet-{en,fr}.png`.
- Voice build (2026-11-02, words exact): EN 148.8 s, FR 147.8 s; claims 5/5; 11 checker trees all equal;
  0 errors, 0 warnings in EN and FR. The first move (tree → `best` on *best trees / meilleurs arbres*) comes
  8.5 s (EN) / 8.4 s (FR) in; the question card stops at 140.0 s (EN) / 138.4 s (FR).
  edge-tts often answered "NoAudioReceived" during the EN run (a different sentence each time, the service, not
  the text); rerunning the same command in a loop finished it from the cache.
  Contact sheets: `build/lessons/part-5/check/sheet-{en,fr}.png`.
- Site: `~/eda-venv/bin/python build_site.py --repo ../eda-learning-lab5-fp` links "Interactive lesson" /
  "Leçon interactive" under video parts 1-5. `tools/test_site.py` (with `python3 -m http.server 8090
  --bind 127.0.0.1 --directory docs` running): 245 checks, 0 failed, including the 6 lesson-part-5 checks in each
  language (log: `build/lessons/part-5/test_site.log`).
