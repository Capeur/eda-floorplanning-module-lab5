# Lab 05 · Part 1 animated lesson: A tree is a recipe (EN + FR)

Animated lesson built with the `lesson-animator` skill (floorplan scene). The lesson page sits next to video
part 1 and does not replace it.

## Inputs
| Input | Value |
|---|---|
| Teacher clone | `../eda-learning-lab5-fp` (read only) |
| EN transcript | `../eda-learning-lab5-fp/courses/learn_floorplanning/module02-03-bstar-tree/transcript.md` |
| FR transcript | `i18n/fr/module02-03-bstar-tree/transcript.md` |
| Slides | transcript slides 1-7 (= PDF pages 1-7), 23 sentences in each language |
| Lesson plan | module `UPGRADE_NOTES.md` §12, "Part 1 — A tree is a recipe" |
| Lab data | `bstar_check.py --json` → `build/lessons/bstar-check.json` (outline 10 × 8, blocks A-E, 11 named trees) |
| Voices | EN `en-US-AndrewMultilingualNeural`, FR `fr-FR-RemyMultilingualNeural`, `--rate=-4%`, cache `.cache/voice` |
| Output | `docs/lessons/part-1/` and `docs/fr/lessons/part-1/` (`--fonts site_src/fonts --storage-key lab05-lesson-speed`) |

## Scenes (anchor words EN / FR)
| Slide | Scene | Main changes |
|---|---|---|
| 1 | Hook | empty `golden` tree beside the empty 10 × 8 outline; all nodes ringed on the second *tree / arbre*; the `best` tree drops all five blocks on *find / trouverez* ("the tightest picture"; no number shown) |
| 2 | The blocks | tree faded, zoom on the floor; "Block" card; all five ringed on *named / nommés*; "3×2" dims on *width / largeur* |
| 3 | Floorplan and outline | zoom out, blocks glide into the looser `lift` pack; glossary Floorplan / Outline; empty space hatched from *tighter / Plus*; blocks glide to `best` on *packed / serrés* ("tighter → smaller chip") |
| 4 | The B*-tree | floor faded, blocks removed, `golden` tree hollow; glossary B*-tree, Node, Root, Children; rings: all → A (root) → B (left child) → D (right child) |
| 5 | The corner | floor back; A drops into the corner on *corner / coin*, "(0, 0)"; tags x → right, y ↑ up |
| 6 | Next door and upstairs | link labels: A–B on *next door / côté*, + A–D on *upstairs / étage*, all links on *names / noms*; tags "solid line = next door", "dashed line = upstairs" |
| 7 | Pause and guess | "3×2" on A (*three / trois*), B ringed (*B*); tree faded; question card "Where does B's left edge go?" (x = 3 / x = 0 / x = 2), auto-pause |

Departures from the §12 plan: the engine has no "tray" of loose blocks, so slides 1-3 use real packs (`best`,
then `lift` → `best` for "tighter"). The outline is always drawn, and its "10 × 8" goes in the headline. Part 1
ends with only A placed, so B's position stays the guess (answered by Part 2).

## Claims (checked by the engine)
`golden`: walk ABCED, A at (0, 0), B at (3, 0) (the answer), A 3 wide and 2 tall, legal; `lift` legal; `best` legal.

## Commands (from the site repo; PYTHONDONTWRITEBYTECODE=1)
```bash
SK=~/.claude/skills/lesson-animator; CL=../eda-learning-lab5-fp; SB=lessons/part-1/storyboard.json
TR_en=$CL/courses/learn_floorplanning/module02-03-bstar-tree/transcript.md
TR_fr=i18n/fr/module02-03-bstar-tree/transcript.md
python3 $CL/courses/learn_floorplanning/module02-03-bstar-tree/examples/bstar_check.py --json > build/lessons/bstar-check.json

# draft (silent, estimated words): build/lessons/draft.sh does this for en and fr, then check_lesson.py
python3 $SK/scripts/draft_timing.py --transcript $TR_en --slides 1-7 --lang en --storyboard $SB --repo $CL \
    --out-audio build/lessons/draft/draft-en.m4a --out-timing build/lessons/draft/timing-en.json

# voice (run in your own terminal; finished sentences are cached in .cache/voice)
python3 $SK/scripts/voice_build.py --transcript $TR_en --slides 1-7 --lang en --voice en-US-AndrewMultilingualNeural \
    --rate=-4% --storyboard $SB --repo $CL --workdir .cache/voice \
    --out-audio build/lessons/part-1/lesson-en.m4a --out-timing build/lessons/part-1/timing-en.json
python3 $SK/scripts/voice_build.py --transcript $TR_fr --slides 1-7 --lang fr --voice fr-FR-RemyMultilingualNeural \
    --rate=-4% --storyboard $SB --repo $CL --workdir .cache/voice \
    --out-audio build/lessons/part-1/lesson-fr.m4a --out-timing build/lessons/part-1/timing-fr.json

# build + check
python3 $SK/scripts/build_lesson.py --storyboard $SB --timing build/lessons/part-1/timing-en.json \
    --audio build/lessons/part-1/lesson-en.m4a --lang en --out docs/lessons/part-1 --fonts site_src/fonts \
    --storage-key lab05-lesson-speed --data build/lessons/bstar-check.json
python3 $SK/scripts/build_lesson.py --storyboard $SB --timing build/lessons/part-1/timing-fr.json \
    --audio build/lessons/part-1/lesson-fr.m4a --lang fr --out docs/fr/lessons/part-1 --fonts site_src/fonts \
    --storage-key lab05-lesson-speed --data build/lessons/bstar-check.json
python3 $SK/scripts/check_lesson.py docs/lessons/part-1/index.html docs/fr/lessons/part-1/index.html --sheets build/lessons/part-1/check
```

## Results
- Draft (2026-11-02, silent audio, estimated words): claims 3/3; 11 checker trees re-packed, all equal;
  0 errors, 0 warnings in EN and FR. EN about 107 s, FR about 117 s (23 sentences each, 21.6 s of pauses).
  Script per frame on a CPU slowed 6×: median 0.8 ms, 95 % under 1.7 ms.
- Voice build (2026-11-02, words exact): EN 115.3 s, FR 111.8 s; claims 3/3; 11 checker trees all equal;
  0 errors, 0 warnings in EN and FR. Contact sheets: `build/lessons/part-1/check/sheet-{en,fr}.png`.
- Site: `~/eda-venv/bin/python build_site.py --repo ../eda-learning-lab5-fp` (the system python has no
  `markdown`) puts "Interactive lesson" / "Leçon interactive" under video part 1; the lede links back to
  `../../index.html#video`. `tools/test_site.py` (with `python3 -m http.server 8090 --directory docs` running):
  197 checks, 0 failed, including the 8 lesson-part-1 checks in each language.
