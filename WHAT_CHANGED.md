# What changed: Lab 05, B*-tree floorplan representation

Module `courses/learn_floorplanning/module02-03-bstar-tree` and tool `platform/tools/bstar-tree` of
[yongfu-li/eda-learning](https://github.com/yongfu-li/eda-learning), upgraded in the teacher clone
`eda-learning-lab5-fp` (uncommitted, on `main`) and published by this site repo in English and French.
Lab number: **Lab 05** (the module number 02-03 is not the lab number).
Every number below was printed by running code on 2026-11-02 (checker, node, Playwright, the site tests).

## Before and after

| | Before | After |
|---|---|---|
| Script | 13 slides, 342 spoken words (2.3 min), no tree on any picture | 31 transcript slides (32 PDF pages), 1,198 spoken words in 5 parts of 1:05-2:02, each part opens with a hook and ends with a "Pause and guess" |
| Examples | 6-line pseudocode, 3 placeholder lines, no script | 8 example trees, a golden checker with exact written rules, 2 deliberately wrong packers |
| Quiz | 4 items, 3 trivially true | 8 items, every answer recomputed with the packer |
| Browser lab | 10 challenges, all passing from one click on "Pack B*-tree", fixed tree | tree editor, 9 challenges that check the tree the learner built, none passes on page load, Clear, a preset or Reveal |
| Pictures | rectangles only, the tree never shown | 19 figures + 5 walkthrough frames that draw the tree next to the floorplan, one colour per block everywhere |
| Site | none | EN + FR GitHub Pages site: 5 video parts with subtitles and speed control, 5 animated lessons, the lab |

## Concepts taught

1. **A tree is a recipe for stacking blocks.** Root in the lower-left corner. Left child = "next door" (`x = parent.x + parent.w`).
   Right child = "upstairs" (`x = parent.x`). Left link drawn solid, right link dashed.
2. **The skyline decides the height.** `y` = highest skyline under the block's footprint; so a right child sits at `y >= parent top`
   (strictly greater when a tall neighbour lifts it, leaving a hole). Blocks are placed in a fixed **walk order: the node,
   its whole left subtree, then its right child**.
3. **Change the recipe, change the picture.** Swap two names, turn a block (w and h exchange), move a leaf. The score is the
   **bounding-box area** (golden 9x3 = 27, 4 wasted; best possible 24 = 6x4; 23 is impossible because the area sum 23 is
   prime). Outline deadspace (57) is printed once and labelled, because it never changes with the tree.
4. Safety fact, said once: any tree gives a packing with no overlap; the only way to fail is to stick out of the 10x8 outline
   (360 of 5040 trees do).

## Files changed

### Teacher clone (only the two allowed folders; `git status` has nothing else, no `__pycache__`)

`courses/learn_floorplanning/module02-03-bstar-tree/`
- Rewritten: `transcript.md`, `EXAMPLES.md`, `quiz.json`, `CHECKLIST.md`, `README.md`, `assets/STEPS.md`.
- New: `examples/bstar_check.py` (965 lines), `examples/{golden,lift,order,floor,swap,rotate,move,best}.json`,
  `examples/wrong/{right_first,no_contour}.py`, `assets/_demo.sh`, 19 figures, `assets/real-shell.png` + `.txt`,
  `assets/lab-starter.png`.
- Rebuilt by the teacher's pipeline (not hand-edited): `outline.yaml`, `slides.md`, `slides.pptx`, `slides.pdf` (32 pages),
  `audio/` (31 slide mp3 + `full.mp3` + `slide_timings.json`, 32 entries), `frames/`, `video.mp4` (1920x1080 H.264, 441.0 s),
  `build.log`.
- Replaced pictures: the five `assets/steps/01-root.png ... 05-takeaway.png` keep the teacher's names, new content.
- Untouched: `examples/tiny_modules.json` (W/H kept as shipped; the checker accepts both spellings).

`platform/tools/bstar-tree/`
- New: `bstar-tree-lab-model.js` (583 lines, pure, no DOM), `bstar-tree-strings.js` (223 lines, every UI word),
  `tests/{test_model_vs_checker.py,model_dump.mjs,test_lab_playwright.py}`.
- Rewritten: `bstar-tree.js` (378 lines, UI), `index.html` (lead sentence, local style).

Not touched: `common/`, `platform/assets/*`, other modules, `.cursor/skills/module-slides/`.

### This site repo
`build_site.py` (`PARTS = [(1,7),(8,12),(13,19),(20,24),(25,32)]`), `make_fr_media.py`, `site_src/`, `i18n/strings.py`,
`i18n/fr/` (French transcript, 19 figures, 5 frames, deck, EXAMPLES, quiz, walkthrough captions, lab strings),
`tools/test_site.py`, `tools/test_lab_site.py`, `tools/strings_shape.mjs`, `tools/lab05-figures/` (figure scripts),
`lessons/part-1..5/` (storyboards + READMEs), `docs/` (the built site, EN + `docs/fr/`).
Outside every repo: `../tools/lab05-figures/` (figure scripts, `run_all.sh`), `../tools/lab05-notes/` (Stage 1 scripts,
`ok_impl.py`, and `UPGRADE_NOTES.md` after this hand-off).

## Figures

Tall 680x820 CSS px at 2x, drawn by our own `bstar-draw.js` from `bstar_check.py --json` (no number typed by hand; `facts.py`
asserts every spoken number). Colour by block id: A `#1d4ed8` blue, B `#0f6b5c`, C `#b45309`, D `#7c3aed`, E `#be123c`.

`blocks-1 -> blocks` · `tree-golden` · `rule-1 -> rule` · `pause-b` · `lift-1 -> lift-2 -> lift` ·
`golden-box-1 -> golden-box` · `lift-box` · `chain-1 -> chain-2 -> chain -> chain-check` · `turn` · `best-1 -> best` ·
`lab-starter` · `real-shell` (program output). Each `-N` figure is the next one with less drawn, so the picture changes
every 5-10 s. Five walkthrough frames (940x468): B next door at x = 3 · the walk A, B, C, E, D · C and E next door ·
D upstairs on A · five blocks placed. French versions of all of them are in `i18n/fr/`.

## The 9 challenges (all recomputed from the learner's tree on every Check)

| Id | Level | Start | Passes when |
|---|---|---|---|
| `build-golden` | Intro | empty | all five blocks, no turn, tree = `A(B(C(E,-),-),D)` (1 of 5040) |
| `d-at-3` | Intro | golden | legal and D.y = 3 (372 trees) |
| `predict-dy` | Practice | walk-order tree | tree unchanged, guess saved before the tree was packed or revealed, guess = D.y |
| `chain-turn` | Practice | long row | tree unchanged, exactly one turned block, legal (only D works) |
| `fix-swap` | Practice | bad tree (40) | one swap, no turn, legal, area <= 27 (only D,E) |
| `move-leaf` | Practice | bad tree (40) | one leaf move, no turn, legal, area <= 28 (`D B right`, `D E left`) |
| `reach-27` | Practice | long row | all five, legal, area <= 27 (348 trees) |
| `beat-27` | Stretch | golden | all five, legal, area < 27, turns allowed (216 trees without turns) |
| `reach-24` | Stretch | golden | all five, no turn, legal, area <= 24 (the 8 best trees) |

Never from `base = reveal`; any tree or turn change wipes the pack, so even an edit-and-undo needs a new Pack.
The old 10 challenges (`run-pack`, `a-origin`, `b-right`, `d-above`, `five`, `legal`, `c-placed`, `e-placed`, `nonneg`,
`no-reveal`) are gone: all passed after one click.

## Tests (run 2026-11-02)

| Test | Command | Result |
|---|---|---|
| Module checker | `python3 examples/bstar_check.py` | 61 PASS, 0 FAIL, 0 SKIP |
| Checker vs the shared JS packer | `... --vs-node` | `packBstar` agrees on all 5040 trees and 11 example scenes |
| Checker catches wrong code | `--impl examples/wrong/right_first.py` / `no_contour.py` | 25 PASS + 4 FAIL / 24 PASS + 5 FAIL (exit 1) |
| Independent implementation | `--impl ../../../../tools/lab05-notes/ok_impl.py` | 29 PASS (different algorithm, no shared code) |
| Model vs checker (Node) | `python3 platform/tools/bstar-tree/tests/test_model_vs_checker.py` | 185 PASS, 0 FAIL (161,280 packs = 5040 trees x 32 turn sets, all challenge scenarios) |
| Lab in Playwright (teacher clone) | `~/eda-venv/bin/python platform/tools/bstar-tree/tests/test_lab_playwright.py` | 111 ok, 0 FAIL (9 positive, 82 negative, 15 colour, 5 page) |
| Lab on the built site | `python3 tools/test_lab_site.py` | **EN 116 ok, 0 FAIL; FR 116 ok, 0 FAIL** (9 positive, 82 negative, 15 colour, 10 page) |
| Site | `python3 tools/test_site.py` | 245 checks, 0 failed (EN 118 rows, FR 118 rows, 9 static) |
| Lessons | inside `test_site.py` | 5 pages x 2 languages x 6 checks, all ok (no console error, 0 external requests, `errors` empty, `dataChecked` = 11 scenes, `dataDiffer` = 0, audio 200, link back to `#video`) |

The test Chromium cannot decode H.264, so the video parts are checked by HTTP status and subtitles, not by playing.
**Still to do by the user:** play a part in Firefox/Chrome at 1.5x in each language and see the next part start by itself.

## Part lengths

| Part | Title | PDF pages | EN words | EN video | FR video | EN lesson | FR lesson |
|---|---|---|---|---|---|---|---|
| 1 | A tree is a recipe | 1-7 | 261 | 1:35 | 1:35 | 1:55 | 1:52 |
| 2 | Walking the tree | 8-12 | 188 | 1:05 | 1:04 | 1:20 | 1:13 |
| 3 | The skyline and the score | 13-19 | 232 | 1:25 | 1:28 | 1:48 | 1:41 |
| 4 | Too wide: turn a block | 20-24 | 204 | 1:13 | 1:15 | 1:30 | 1:27 |
| 5 | The tightest floorplan, your turn | 25-32 | 313 | 2:02 | 2:09 | 2:29 | 2:28 |

Full English video 7:21 (441.0 s); English script 1,198 words, French 1,313 words. Part and lesson lengths from
`build_site.py` and `ffprobe` of the lesson audio.

## The five animated lessons

One interactive page per part, next to its video part (`docs/lessons/part-N/`, `docs/fr/lessons/part-N/`), built with the
`lesson-animator` floorplan scene: a B*-tree beside a floor of blocks that drop onto the skyline, word-timed text, zooms,
counters, an automatic "Pause and guess" at the end of the part, and click-to-try (swap, turn, move). English and French
come from one storyboard (`lessons/part-N/storyboard.json`); every tree is re-packed by the engine and compared with
`bstar_check.py --json` (11 scenes).

- Voices: **`en-US-AndrewMultilingualNeural`** (English) and **`fr-FR-RemyMultilingualNeural`** (French), `--rate=-4%`.
- Sentences per lesson, EN / FR: 23 / 23, 13 / 13, 20 / 20, 18 / 19, 29 / 30.
- Same block colours and the same solid/dashed links as the figures, the lab and the video.
- Building part 5 exposed a bug in the `lesson-animator` skill (not in the course): a fenced code block with a blank line in slide 29 was glued to the last spoken sentence and would have been sent to the voice. Fixed in the skill; slides 1-24 give the same sentences as before.

## Findings for the teacher

Bugs and gaps in shared or course-wide files that we could not fix (rule: only the module and tool folders are edited),
and the traps we worked around.

1. **The B*-tree walk order was unwritten.** The code does preorder: place the node, then its whole left subtree, then its
   right child. Nothing says so (transcript, EXAMPLES, walkthrough) and the golden is identical either way, so no test
   catches a wrong order. 1764 of the 5040 trees pack differently if the right child goes first (e.g. `A(B(C(-,E),D),-)`:
   7x5 correct, 7x8 right-first). We wrote the rule everywhere and added the order-sensitive examples. Please confirm it is the
   intended rule.
2. **`tiny_modules.json` uses `W`/`H`; `metrics.py`, `goldens.OUTLINE` and the JS use `w`/`h`.**
   `is_legal_packing(pack, load_tiny_modules()["outline"])` raises `KeyError: 'w'`. `common/tiny_modules.json` is identical.
   Our checker accepts both; new module files use `w`/`h`.
3. **`drawFloorplan` colours by the index of the placed ids** (sorted), so a partial pack shifts every colour (only B and D
   placed: B becomes the first colour). **The lab canvas palette also starts teal** (`PALETTE`, A = `#2a6f6a`), unlike
   `PAPER_PALETTE` (A blue). Our figures, frames, lab and lessons key the colour to the block id; tested by pixel.
4. **The shared `floorplanning-algos.js` captions are the old ones**, rectangle-only, and
   **`capture_all_walkthroughs.sh` must not be rerun on this module**: it runs `capture_algorithm_walkthrough.py
   --inject-transcript` for module02-03, overwriting the five frames and injecting the old captions into `transcript.md`.
   (Old text still there: "keeping the tree geometry honest", "Perturbing the tree - swap, rotate, move - will feed
   simulated annealing later".) The viewer also prints the step id in its banner ("Step 2 / 5 - left-chain"), which does not
   always describe the frame.
5. **A slide title starting with "Next" makes the builder replace its bullets** (`prose_to_bullets.py` turns the slide into
   "Complete the quiz for this part" + one sentence). Our slide 6 is titled "Left is next door, right is upstairs" for this
   reason.
6. **99 `.pyc` files are committed** in `__pycache__` folders (`git ls-files | grep -c __pycache__` = 99): 23 in
   `.cursor/skills/module-slides/scripts`, 4 under `courses/learn_floorplanning/common`, the rest in the other courses'
   `common/`. They should be removed and ignored.
7. **The README "Live" link points to another organisation's site**:
   `universal-verification-methodology.github.io/learning/tools/bstar-tree/`. Left unchanged.
8. **The `soft` flag of module A is unused**: `packBstar` ignores it, the old tool never called `allowSoftToggle`, and the
   aspect range 0.5-2 only allows 2x3 and 3x2. We teach "any block may turn 90 degrees" and do not mention soft modules.
9. **`saSwap` swaps rectangles, not tree nodes**, and breaks legality (A <-> C on the golden gives an illegal pack). The
   transcript and walkthrough say "swap, rotate, move" but no tree operation exists anywhere in `common/` or the JS. We wrote
   `swap`, `rotate`, `move_leaf` in the checker and the lab model.
10. **The old challenges all passed with one click** on "Pack B*-tree" (hard-coded tree `GOLDEN_BSTAR`, no tree view, no way to
    edit). `nonneg` also passed on an empty workspace (`every()` is vacuously true), manual placement could never pass, and the
    shell says "challenges prefer the B* packer result" while only the button sets `ran`. `createInteractiveFloorplanLab` is no
    longer used by this tool.

Smaller points:
- `common/test_solvers.py` only asserts that the B*, Polish and sequence-pair goldens are legal, never their coordinates;
  nothing checks JS <-> Python sync (we found `pack_bstar` and `packBstar` equal on all 5040 trees).
- `courses/learn_floorplanning/scripts/` holds generators (`deepen_content.py`, `generate_tools.py`, `scaffold_course.py`,
  `parity_audit.py`, `build_all_media.sh`, `capture_all_walkthroughs.sh`). We did not run them; do not run them on this module
  (in Lab 03 the enrich script rewrote transcripts with wrong claims).
- `scripts/module.sh --check` is a placeholder ("implement goldens when solvers land").
- `pack_bstar` returns `x`, `y` as floats and `w`, `h` as ints, silently overwrites duplicate ids, raises
  `KeyError`/`TypeError` on an unknown id and does no tree validation. `pack_hierarchical()` returns hard-coded numbers.
- `createChallengeLab` names its panels "Graph" and "Reference / metrics" for every lab, floorplanning included (our tool
  overwrites both headings).
- The old EXAMPLES.md pointed to `../../common/solvers.py`; from the module it is `../common/solvers.py` (fixed in ours).
- Line endings are mixed (`quiz.json`, `README.md`, `CHECKLIST.md`, `STEPS.md` CRLF; `transcript.md`, `EXAMPLES.md` LF);
  we kept each file's style.

## Rebuild and publish

```bash
# from this repo
~/eda-venv/bin/python build_site.py --repo ../eda-learning-lab5-fp     # the system python has no `markdown`
python3 -m http.server 8090 --directory docs &
python3 tools/test_site.py && python3 tools/test_lab_site.py
```
GitHub Pages: branch `main`, folder `/docs`.
