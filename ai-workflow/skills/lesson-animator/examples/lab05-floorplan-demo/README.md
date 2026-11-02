# Example: floorplan scene, Lab 05 (B*-tree), engine demo, EN + FR

**This is a demo of the engine, not a lesson of the lab.** Its five short slides (`transcript-en.md`,
`transcript-fr.md`) are demo narration written to use every feature of the floorplan scene once. The real
lessons follow the module's five-part script (Stage 3) and its lesson plan in the module notes.

Data: the Lab 05 checker's `--json` (`examples/bstar_check.py --json`, Stage 2): outline 10 × 8, blocks
A 3×2, B 2×3, C 2×2, D 3×1, E 2×2, one colour per block, 11 named trees (`golden`, `lift`, `order`, `floor`,
`swap_start`, `swap_after`, `rotate_start`, `rotate_after`, `move_start`, `move_after`, `best`) with their packs.

## Scenes (anchor words EN / FR)
| Slide | Scene | Main changes |
|---|---|---|
| 1 | A tree is a recipe | grid faded while the tree is shown; A drops into the corner on *corner / coin* with "(0, 0)"; B on *next door / côté*; C and E on *follow / suivent*; D on *upstairs / étage*; "next door" / "upstairs" link labels; walk badges 1–5 |
| 2 | The skyline | zoom on the floor; skyline drawn on *orange*; D taken away, then falls again on *falls / tombe* and lands on A, "(0, 2)" |
| 3 | A taller neighbour | bounding box + counter 27; swap A ↔ C on *swap / échangeons* (names travel in the tree, blocks glide); B and D highlighted; D at 3; hole hatched; counter 36 in red |
| 4 | Turn a box | all-left chain `rotate_start`, 12 wide, red hatch outside the outline, "sticks out"; D turns 90° on *turn / tournez*; 10 wide, "fits" |
| 5 | Your turn | `best` tree (6 × 4 = 24, green) with the tree faded; thumbnails of golden (27) and lift (36); question "Can a tree beat 27?" |

## Commands (from a site repo; the skill in ~/.claude/skills/lesson-animator)
```bash
SK=~/.claude/skills/lesson-animator; EX=$SK/examples/lab05-floorplan-demo; CL=../eda-learning-lab5-fp
python3 $CL/courses/learn_floorplanning/module02-03-bstar-tree/examples/bstar_check.py --json > build/bstar-check.json
for L in en fr; do
  python3 $SK/scripts/draft_timing.py --transcript $EX/transcript-$L.md --slides 1-5 --lang $L --storyboard $EX/storyboard.json \
      --repo $CL --out-audio build/demo/draft-$L.m4a --out-timing build/demo/timing-$L.json
  python3 $SK/scripts/build_lesson.py --storyboard $EX/storyboard.json --timing build/demo/timing-$L.json \
      --audio build/demo/draft-$L.m4a --lang $L --out build/demo/$L --fonts site_src/fonts \
      --storage-key lab05-lesson-speed --data build/bstar-check.json
done
python3 $SK/scripts/check_lesson.py build/demo/en/index.html build/demo/fr/index.html --sheets build/demo/check
```
The audio is silent (draft timing): the page plays and checks like the real one. For a voice, replace
`draft_timing.py` with `voice_build.py --voice ... --rate=-4%`; the storyboard does not change.

## Results (2026-10-30, cloud, draft timing)
- Claims 5/5; the engine re-packed the checker's 11 trees: all equal. 0 errors, 0 warnings, EN and FR.
- Length with pauses: EN about 72 s, FR about 81 s (20 sentences each).
- Script per frame on a CPU slowed 6×: median 0.8 ms, 95 % under 2.7 ms.
- Try-it panel tested in Chromium: swap A ↔ C → 9 × 4 = 36; turn D → 9 × 5 = 45; move leaf E under B → 7 × 6 = 42;
  "Start again" → 27; each result equal to the course's `pack_bstar`.
- `record_mp4.py`: 6 s clip recorded.
