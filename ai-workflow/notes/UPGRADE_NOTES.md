# UPGRADE_NOTES — Lab 05 · B*-tree floorplan representation

Stage 1 (audit) done on 2026-10-30. Nothing outside this file was edited. `git status` still shows only this new file.
All numbers below come from running code (node on `platform/assets/floorplanning-core.js`, python on `courses/learn_floorplanning/common`, headless Chromium on the real lab page). Commands are at the end (§9).

## 0. Inputs

| Input | Value |
|---|---|
| Course | `learn_floorplanning` |
| Module dir | `courses/learn_floorplanning/module02-03-bstar-tree` |
| Tool dir | `platform/tools/bstar-tree` (files: `index.html`, `bstar-tree.js`) |
| Lab number | **Lab 05** (`platform/courses/learn_floorplanning/labs/bstar-tree/index.html`; module number 02-03 does not equal the lab number) |
| Teacher clone | this folder `eda-learning-lab5-fp`, on `main`, no branch, nothing committed |
| Site repo | `../eda-floorplanning-module-lab5` (does not exist yet; Stage 5 copies `../eda-partitioning-module-lab3`) |
| Shared code used read-only | `courses/learn_floorplanning/common/{pack,goldens,metrics,solvers}.py`, `platform/assets/{floorplanning-core,floorplanning-lab,clustering-ui}.js`, `platform/tools/algorithm-walkthrough/floorplanning-algos.js` |

Note: `common/` is at `courses/learn_floorplanning/common`, not at the repo root (the audit script's "common" is this folder).

## 1. What exists today (short)

- Transcript: 12 sections / 13 slides, **342 spoken words (~2.3 min)** (audit counts 534 words incl. code and headings). Lint: 4 problems (3 bullets that get cut, 1 "left/right" slash).
- The five step captions (slides 4–8) are copied from the walkthrough viewer (`floorplanning-algos.js`, shared, read-only) and `assets/steps/*.png` are rectangle-only screenshots: **the learner never sees the tree**.
- `EXAMPLES.md`: 136 words, the pseudocode is 6 lines, three placeholder lines ("Change one knob", "Scale the instance slightly", "Note tying the run"). No checker script, `examples/` holds only `tiny_modules.json`.
- `quiz.json`: 4 items, all about the golden only; q1, q2 and q4 are trivially true.
- Browser lab: 10 challenges, **all pass from one button click** (§4).
- Golden instance: outline 10×8, modules A 3×2 (soft), B 2×3, C 2×2, D 3×1, E 2×2, tree `A(left: B→C→E, right: D)`.

## 2. Golden cross-check table

JS = `packBstar(GOLDEN_BSTAR)` from `floorplanning-core.js` (node). PY = `pack_bstar(GOLDEN_BSTAR, MODULES)` from `common/pack.py`. "Stated in" = where the number appears in the module.

| Quantity | Stated in | JS | PY | Verdict |
|---|---|---|---|---|
| A at (0,0), 3×2 | transcript s4, STEPS, quiz q1, EXAMPLES GOLDEN, lab `a-origin` | (0,0) | (0,0) | OK |
| B at (3,0), 2×3 (`B.x = A.x + A.w`) | transcript s5, STEPS, lab `b-right` | (3,0) | (3,0) | OK |
| C at (5,0) | STEPS metrics | (5,0) | (5,0) | OK (hard-coded string in the walkthrough, correct) |
| E at (7,0) | STEPS metrics | (7,0) | (7,0) | OK (same) |
| D at (0,2), 3×1 | STEPS metrics (computed) | (0,2) | (0,2) | OK |
| `D.y >= A.h` | EXAMPLES, transcript s3/s6, STEPS, lab `d-above` | 2 ≥ 2 | 2 ≥ 2 | True, but **always an equality here** (§3 H2) |
| Left chain `A.left = B→C→E` | quiz q3, transcript s5 | yes | yes | OK |
| Legal in 10×8 | transcript s7, quiz q4, lab `legal` | true | true | OK |
| Bounding box | **not stated anywhere** | 9×3 = 27 | 9×3 = 27 | New number to teach |
| Σ module area | common comment | 23 | 23 | OK |
| Outline deadspace / density | common comment, JSON note | 57 / 0.2875 | 57 / 0.2875 | OK (but see H9) |
| Bounding-box deadspace | not stated | 27 − 23 = **4** | 4 | New number |
| `GOLDEN_PACK` constant vs packer output | both languages | equal numerically | equal numerically | OK (JSON strings differ only by key order and int/float) |
| `cost(golden)` | (not used in this lab) | 35.7 | 35.7 | agree |
| JS vs PY, **all 5040 labelled trees** on A–E | — | — | — | **0 mismatches** (x, y of every module); 4680 legal on both |
| `common/test_solvers.py` | — | — | prints OK | but it only asserts legality of the B* golden, no coordinates |

Conclusion: no wrong golden number. The risks are the unstated rules and the weak checks (§3, §4), not arithmetic.

## 3. Hidden problems and vague rules

**H1. The golden tree never uses the contour.** In the golden pack every module has y = 0 except D, and D's footprint x∈[0,3) only covers A. So "the contour" gives the same answer as "parent's top edge" and as "y = 2 typed by hand". Checked over all 5040 trees: 360 contain a right child lifted above its parent's top and 254 a left child lifted off the floor; the golden has neither. Nothing in the module can tell a real contour from a shortcut.

**H2. What `D.y >= A.h` really means.** The packer sets `y = max(contour height over [x, x+w))`. For a right child this is `≥ parent.y + parent.h` (not `parent.h`; the two coincide only because A.y = 0), and the child's x equals the parent's x. In the golden it is exactly equal, so the "≥" is never tested (D at y = 5 would also pass the lab). Fix: state it as "y = tallest skyline under my footprint", and show a tree where it is strictly greater (see example E1: swap A and C, D lands at y = 3 instead of 2, leaving a 2×1 hole).

**H3. Traversal order is not written anywhere.** The code is preorder: place the node, then its **whole left subtree**, then its right child. If the right child is placed first, 1764 of the 5040 trees give different coordinates (e.g. `A(B(C(-,E),D),-)`: bounding box 7×5 left-first, 7×8 right-first). The golden is identical either way, so no current test can catch a learner who gets the order wrong. The pseudocode line "update horizontal contour after each place" also does not say what the contour is.

**H4. Left child "right-of" does not mean "same y".** The left child's x is `parent.x + parent.w`, its y comes from the contour. In the golden all are at y = 0 so this looks like "same row". Counter-case already in the shared files: `SOFT_A_PACK` is produced by tree `A(B(C(-,D(E,-)),-),-)` with A turned to 2×3: E is the left child of D (y = 2) but lands at y = 0 because nothing is under it. The pseudocode gives no y rule for left children.

**H5. Swap / rotate / move are mentioned but do not exist.** Transcript slide 7 and STEPS step 4 say "Perturbing the tree — swap, rotate, move — will feed simulated annealing". Searching `common/`, `floorplanning-core.js`, the lab and the tool: there is **no tree operation at all**. `saSwap` in `floorplanning-core.js` swaps the (x,y) of two finished rectangles (not tree nodes) and is not used here; applied to the golden (A↔C) it makes the pack illegal. `packBstar(tree, modules)` has no rotation flag; rotation is only possible by passing a modified `modules` list. Single operations on the golden tree never shrink the bounding box: the 10 swaps give ≥ 27 (four keep exactly 27: C↔E, B↔C, B↔E, A↔D), all 5 single rotations give ≥ 27, leaf moves of D or E give ≥ 27. So the golden is a poor start for "an operation improves the result"; the extra examples start elsewhere (§5).

**H6. `W`/`H` vs `w`/`h`.** `examples/tiny_modules.json` (and `common/tiny_modules.json`, identical) has `"outline": {"W": 10, "H": 8}`. `common/goldens.OUTLINE`, `common/metrics.py` and `floorplanning-core.js` use lowercase `w`/`h`. Doing the natural thing (`is_legal_packing(pack, load_tiny_modules()["outline"])`) raises `KeyError: 'w'` (reproduced). The module-local JSON can be fixed or normalised; `common/` cannot be edited.

**H7. Soft module A is unused and almost meaningless.** `soft: true, aspect_min 0.5, aspect_max 2.0`, area 6. Integer shapes of area 6: 1×6, 2×3, 3×2, 6×1; with aspect w/h in [0.5, 2] only **2×3 and 3×2** are allowed, i.e. "soft" = "A may be turned". `packBstar` ignores `soft`; `bstar-tree.js` does not use `allowSoftToggle`; nothing in the transcript mentions it. Best treated as a rotation (§7 Q2).

**H8. Challenges (see §4):** all 10 pass from one click on "Pack B*-tree"; the tree is hard-coded (`GOLDEN_BSTAR`), there is no tree view and no way to change it; the intro text says "You can also place manually — challenges prefer the B* packer result" but manual placement can never pass (the `ran` flag is only set by the button); editing after the button does not cancel `ran`.

**H9. "Deadspace" has two meanings.** CHECKLIST and the JSON note use outline deadspace (80 − 23 = 57, density 0.2875), which never changes with the tree. What distinguishes trees is **bounding-box area** (golden 27, wasted 4). Legality is also a weak score: **4680 of 5040 trees are legal**, **no tree ever overlaps** (0 of 5040; B*-trees cannot overlap by construction), and the 360 illegal ones all stick out of the outline (120 too wide, 240 too tall).

**H10. Is 27 good?** Among the 4680 legal trees, 216 have a smaller bounding box than the golden; 8 reach **24 = 6×4**, which is optimal (the area sum 23 is prime, so no rectangle of area 23 can hold the 3-high module B). With rotations: 138,480 legal (tree, rotation) combinations, 1488 reach 24. The golden is "legal and tidy", not "best". Never claimed in the module, but a learner will ask.

**H11. Smaller issues.**
- `EXAMPLES.md` says "Use `examples/tiny_modules.json` and `../../common/solvers.py`": the path is wrong (from the module dir it is `../common/solvers.py`; `../../common` does not exist).
- README advertises `./scripts/module.sh 02-03 --check`; the script only checks that files exist and prints "`--check` placeholder: implement goldens when solvers land".
- `pack_bstar` returns x, y as floats (`3.0`) but w, h as ints; JS returns ints. It silently overwrites duplicate ids and raises `KeyError`/`TypeError` on an unknown id or a missing module; there is no tree validation.
- `pack_hierarchical()` takes no arguments and returns hard-coded numbers (not our lab).
- `common/__pycache__` is present and **99 files named `__pycache__` are tracked by git** (teacher list).
- The README "Live" link points to another GitHub organisation's Pages site (teacher list).
- Line endings: `quiz.json`, `README.md`, `CHECKLIST.md` are CRLF; `transcript.md`, `EXAMPLES.md`, `STEPS.md` are LF. Keep each file's style when rewriting.
- `STEPS.md` / transcript s4–s8 captions come from `floorplanning-algos.js` (shared): "keeping the tree geometry honest", "Contour heights track the skyline so later modules sit tightly" (never exercised, see H1).

### Vague rules to write exactly in Stage 2

| Vague today | Exact rule to write |
|---|---|
| "left = right-of, right = above" | Left child: `x = parent.x + parent.w`. Right child: `x = parent.x`. Both: `y = skyline height under [x, x+w)`. |
| "D.y ≥ A.h" | `y = max skyline height over [x, x+w)`; for a right child this is ≥ `parent.y + parent.h`. |
| "update contour after each place" | Contour = for every x the top edge of what is already placed; placing a block raises it to `y + h` over `[x, x+w)`. |
| (order unstated) | Preorder: node, whole left subtree, then right child. |
| "legal" | Inside the outline and no interior overlap (touching edges allowed). |
| "deadspace" | Always say which: outline deadspace `W·H − Σwh` (57) or bounding-box deadspace `bbW·bbH − Σwh` (golden 4). |
| "swap, rotate, move" | swap = exchange two module names in the tree (shape stays); rotate = exchange a module's w and h; move = cut a leaf and attach it to a free child slot (§7 Q4). |
| "root = lower-left" | Origin bottom-left, y grows upward (the drawing code flips y). Sizes are written w×h ("three by two" = w 3, h 2; "ten by eight" = W 10, H 8). |

## 4. Challenges: which pass from one click

Run in headless Chromium against the real page (`/tools/bstar-tree/`), for each of the 10 challenges: Start, then the action, then Check.

| Action before Check | Result |
|---|---|
| none | all 10 fail |
| **one click on "Pack B*-tree"** | **all 10 PASS**: `run-pack`, `a-origin`, `b-right`, `d-above`, `five`, `legal`, `c-placed`, `e-placed`, `nonneg`, `no-reveal` |
| Pack, then "Clear" (empty workspace) | `run-pack` PASS and `nonneg` PASS (empty pack: `every()` is vacuously true); the other 8 fail |
| only "Reveal golden (study)" | all 10 fail (good; `ran` is false) |
| place the five modules by hand | cannot pass anything (nothing but the button sets `ran`) |

So: the lab teaches nothing the button does not do, two challenges pass on an empty workspace, and the tree cannot be edited. Stage 4 replaces it (§6, Stage 4).

## 5. What to teach (high-school level)

**Concepts (3, plus one safety fact)**
1. **A tree is a recipe for stacking boxes.** Root in the lower-left corner. Left child = next door, to the right of its parent. Right child = upstairs, on top of the parent, same left edge. (Mnemonic: "left means next door, right means upstairs": the names are counter-intuitive, say so.)
2. **The skyline decides the height.** Each box falls until it touches the highest thing under it. So `D.y ≥ parent top` and a tall neighbour can lift a box and leave a hole. Boxes are placed in a fixed walk order (node, left subtree, right child).
3. **Change the recipe, change the picture.** Swap two names, turn one box, move a leaf: the same five boxes give a different bounding box. Score = bounding-box area (golden 27; best possible 24).
4. *Safety fact (said once, in part 5):* any tree gives a packing with no overlaps; the only way to fail is to stick out of the 10×8 box (360 of 5040 trees do).

**Extra example trees** (each verified with `pack_bstar`, positions listed as name (x,y)).

| Id | Tree (`id(left,right)`, `-` = empty) | Result | The one idea that flips |
|---|---|---|---|
| E1 `lift` | `C(B(A(E,-),-),D)` = golden with **A and C swapped** | C (0,0), B (2,0), A (4,0), E (7,0), **D (0,3)**; bbox 9×4 = 36, legal. D sits on B's shoulder (B is 3 high), `D.y = 3 > C.top = 2`, a 2×1 hole above C | The contour lifts a block; `D.y ≥ parent top` is a strict inequality here (golden: 27 → 36) |
| E2 `swap` | start `A(B(C(D,-),-),E)`; fix = swap **D ↔ E** (gives the golden) | start: A (0,0), B (3,0), C (5,0), D (7,0), E (0,2); bbox 10×4 = 40, wasted 17. After swap: golden, bbox 9×3 = 27, wasted 4 | One swap removes 13 units of bounding box (40 → 27) |
| E3 `rotate` | chain `A(B(C(D(E,-),-),-),-)` (every box a left child) | width 3+2+2+3+2 = **12 > 10**, E at (10,0): **illegal**. Turn D to 1×3: D (7,0) 1×3, E (8,0): bbox 10×3 = 30, **legal** | One rotation flips illegal → legal |
| (bonus, no new data) `best` | `A(D,C(E(B,-),-))` | bbox 6×4 = 24: D (3,0), C (0,2), E (2,2), **B (4,1) lifted onto D** | Optimum needs the contour; the "stretch" target (≤ 25: 216 trees) |

Also usable for free in part 3: `SOFT_A_PACK` tree `A(B(C(-,D(E,-)),-),-)` with A turned 2×3 shows "a left child falls to the floor" (H4).

**Video parts (5, target 1,100–1,300 spoken words, ~7–8 min; each opens with a hook, ends with a "pause and guess" answered at the start of the next part)**

| # | Title | Hook | Content (each idea once) | Pause and guess → answer | Animated lesson (tree + rectangles) |
|---|---|---|---|---|---|
| 1 | A tree is a recipe | "Five boxes, a corner of a table and one tree that says where each box goes. Can you build the picture from the tree?" | root in the corner (A 3×2 at (0,0)); left child = next door (B at x = 3); right child = upstairs (D, same left edge) | "B is A's left child. Where is B's left edge?" → x = 3 = A.x + A.w | Tree panel left (nodes grey), rectangle panel right. Node lights up, box drops in; A→B arrow labelled "next door", A→D "upstairs". |
| 2 | Walking the tree and running out of room | "Make every child a left child and the row sticks out of the table. By how much?" | walk order (node, left subtree, right child) with ①②③ badges; left chain B, C, E at x = 3, 5, 7; widths add up | "All five as left children: how wide is the row?" → 12, sticks out by 2 | Badges appear in walk order; running width counter; red overflow past x = 10 (this is E3 before the fix). Click a child's side (left/right) to try. |
| 3 | The skyline | "D goes on top of A. What if a taller box is next door?" | skyline = highest edge under the box; D at y = 2 = A.h in the golden; then E1 | "Swap A and C. Does D land at 2 or 3?" → 3: B is 3 high and sticks under D | Skyline polyline drawn live; D slides down until it touches; golden vs E1 side by side; hole shaded. Drag-to-swap A and C. |
| 4 | Swap two names | "Same five boxes, 5,040 possible trees. This one wastes 17 squares; swap two names and it wastes 4." | E2 start (bbox 10×4 = 40), score = bounding-box area; one swap → golden (27) | "Which two names would you swap?" → D and E | Two panels, bbox outline drawn and area counter; click two nodes to swap and watch the boxes fly; counter 40 → 27. |
| 5 | Turn it, move it, score it | "Is 27 the best? Could 23 ever be reached?" | rotate D to fit (E3: 12 → 10, illegal → legal); move = cut a leaf, paste it elsewhere (one sentence); safety fact; best 24 (6×4), 23 is prime; link to simulated annealing and the lab | "Can any tree beat 27? What is the smallest possible area?" → yes (216 trees); 24, never 23 | Rotate click on D; counter shows legal flip; bbox shrinks to 24 on the `best` tree with B lifted onto D; "your turn" card pointing to the lab. |

Part boundaries (slide ranges and PDF pages): see §12 (Stage 3). The parts were re-planned there to use at most four example trees.

## 6. Plan for stages 2–5, with "lessons for every part"

**Stage 2 — content and goldens (Sonnet).**
- `examples/bstar_check.py`: reference implementation with the exact rules of §3 (preorder, skyline, left/right x rules, y from skyline, lower-left origin, integers); functions `pack_bstar`, `bounding_box`, `legality`, `swap`, `rotate`, `move_leaf`, tree validation (each module exactly once); golden table (golden, E1, E2 start+result, E3 before/after, `best`, the 5040-tree statistics: 4680 legal, 0 overlaps, 120 too wide, 240 too tall, 8 at area 24); `--show`, `--impl my.py`, `--json` (dump every example's positions: Stage 3 figures and Stage 7 lessons read this file so no number is typed by hand), a **reversed-input check** (module list reversed and ids shuffled give the same pack), and a **`--vs-node`** check that runs `packBstar` from `floorplanning-core.js` on the same trees (Stage 1 found 0 mismatches over 5040). Wrong-implementation switches that must FAIL: right child placed before left subtree (needs a tree where order matters, e.g. `A(B(C(-,E),D),-)` 7×5 vs 7×8), left child forced to parent's y, `y = parent.h` shortcut (fails on E1), no contour update.
- `examples/bstar_trees.json`: golden + E1/E2/E3/`best` with expected positions, bbox, legality and the "idea" sentence. Lowercase `w`/`h` keys; the checker also normalises `W`/`H` so the shared JSON works.
- `EXAMPLES.md` rewritten with the exact rules, the table above and tasks that use the numbers (no placeholders); `quiz.json` 7–8 numeric items (D.y in golden = 2; D.y after A↔C = 3; chain width 12; golden bbox area 27; area after D↔E swap; does rotating D make the chain legal; smallest possible area 24 not 23; "can a B*-tree overlap?" false); `CHECKLIST.md`, `README.md` (fix `../common` path, drop the placeholder `module.sh` claim), `assets/_demo.sh`.
- Done when all PASS and a deliberately wrong `--impl` FAILs.

**Stage 3 — five-part script and figures (Opus).**
- `transcript.md` already in the 5 parts of §5, ~240 words each, repetition rules respected (each idea once where taught, once in the recap), lint clean (Stage 1 findings to avoid: bullets > 80 chars get cut, "left/right" slash).
- Figures (tall) show **tree and rectangles side by side**, with the skyline drawn: golden, E1 (hole shaded), E2 start/after, E3 before/after, `best`. Step figures (later parts hidden). Scripts in `../tools/lab05-figures/` with `run_all.sh` and a README. Figure numbers read from `bstar_check.py --json`.
- The 5 walkthrough frames in `assets/steps/` (rectangle-only today) are redrawn with the teacher's capture script against a scratch copy of the viewer; the shared `floorplanning-algos.js` captions stay as they are (teacher list).
- Record slide ranges and PDF pages for the five parts.

**Stage 4 — interactive lab (Opus).**
- Split `bstar-tree-lab-model.js` (pure; imports `packBstar` from `floorplanning-core.js`, rotation by passing a modified `modules` list) and `bstar-tree.js` (UI). The learner **sees and edits the tree** (SVG tree with a parent + side dropdown per box, swap and rotate buttons) next to the rectangles and the skyline.
- 8–10 challenges that check what the learner built, recomputed from the learner's tree on every Check (no `ran` flag): build the golden tree; predict D.y (type a number) before packing; make D land at y = 3 (E1); make the chain legal with one rotation (E3); fix the E2 start with one swap; reach bounding box ≤ 27; beat the golden (≤ 25); reach 24 (stretch). Editing after Pack invalidates the pack. Nothing passes on page load, from Pack alone, from Reveal or on an empty workspace.
- Tests: model vs checker (node), Playwright positive and negative cases (page load, Pack only, empty workspace, edit after Pack, Reveal, wrong swap), colour checks (the group of the first module name is blue), recapture the lab screenshot the deck uses.

**Stage 5 — site repo (Sonnet).**
- Copy `../eda-partitioning-module-lab3` (fresh `git init -b main`, no old history, no `docs/`, no `.cache/`) to `../eda-floorplanning-module-lab5`, set `PARTS` to 5, translate to `i18n/fr/`, French figures and frames (French term proposal: "arbre B*", skyline = "ligne d'horizon"/"profil", bounding box = "boîte englobante", deadspace = "espace perdu"). Media commands are given to the user to run. Then build and run `tools/test_site.py` and `tools/test_lab_site.py`, reading both language lines.

**Lessons for every part (Stage 7, `lesson-animator`; storyboard written in Stage 3 alongside the script).**
Every part gets one lesson page built from the same checker JSON: left panel = tree (nodes numbered in walk order), right panel = 10×8 outline with rectangles, skyline polyline, live counters (position of the box being placed, running width, bounding-box area, legal yes/no). Auto-pause at each "pause and guess" with the answer revealed on resume; EN and FR from one storyboard.

| Part | Lesson content | Click-to-try |
|---|---|---|
| 1 | golden tree builds box by box; arrows labelled "next door" and "upstairs" | click a node to see its (x, y) and why |
| 2 | walk badges ①–⑤, running width, overflow of the all-left chain (E3 before) | switch a child between left and right and watch the row |
| 3 | skyline sweep, D sliding down, golden then E1, hole shaded | drag A and C to swap, guess D.y |
| 4 | E2 start, bounding box and area counter 40 → 27 | click any two nodes to swap, counter updates, target 27 |
| 5 | E3 rotate (illegal → legal), `best` tree at 24, "your turn" | rotate any box; try to beat 27 |

## 7. Open questions (each with a recommended answer)

1. **Which deadspace do we teach?** Outline deadspace (57) is constant; bounding-box area is what trees change. *Recommend:* teach bounding-box area and "wasted squares inside the box" as the score; print outline deadspace once, labelled, because the checklist asks for it.
2. **Soft module A.** *Recommend:* keep A as a plain 3×2 module and mention once that A may be turned to 2×3 (the only other allowed shape); no "soft/aspect" vocabulary in the video; the checker keeps the fields but only validates the two shapes.
3. **How is rotation represented?** *Recommend:* a module-level `rotated` set kept outside the tree; the checker and lab swap w and h in the `modules` list before calling `pack_bstar` / `packBstar`. This works with the shared packers unchanged.
4. **What does "move" mean?** *Recommend:* leaf move only (cut a leaf, attach it to a free left or right slot of another node); internal-node deletion is out of scope. One sentence in the video, one quiz item, one lab button.
5. **Write the traversal order (preorder, left subtree before right child) as the official rule?** It is what the code does and what the B*-tree literature uses. *Recommend:* yes, and add the order-sensitive golden (`A(B(C(-,E),D),-)`), because today no test would catch a wrong order. Please confirm this is the teacher's intent.
6. **Replace the 10 one-click challenges?** *Recommend:* yes, replace them with the build-and-predict set of Stage 4 (the old ids are not referenced anywhere I read; the site's challenge test will be rewritten anyway).
7. **Tree editor UI: drag and drop or dropdowns?** *Recommend:* dropdowns (parent, side) plus swap and rotate buttons: simpler to test and works on touch screens.
8. **How many parts?** *Recommend:* 5 (as in Lab 03), ~1:30 each.
9. **Spoken name.** *Recommend:* "B-star tree" in the script and subtitles (the TTS reads it correctly), "B*-tree" in text and figures, "arbre B*" in French.
10. **`tiny_modules.json` W/H.** The shared file cannot be edited. *Recommend:* new module files use `w`/`h`, the checker accepts both, and the mismatch goes on the teacher list.
11. **Keep the verification scripts?** The Stage 1 scripts (node/python cross-check, 5040-tree search, Playwright click test) are in the session scratchpad, which is temporary. *Recommend:* copy them to `../tools/lab05-notes/` (outside every repo); Stage 2's `bstar_check.py` supersedes them. I did not write there because you asked to edit nothing else — say yes and I will.

### 7b. Decisions taken on the open questions (approved)

- **(a) Traversal rule (Q5).** The official rule is **preorder with the left subtree before the right child: place the node, then its whole left subtree, then its right child.** It is written in `EXAMPLES.md`, implemented in the checker (`bstar_check.py`, with the order-sensitive golden `A(B(C(-,E),D),-)`: 7×5 correct, 7×8 if the right child goes first) and spoken in the transcript (part 2). "The rule was unwritten" goes on the teacher list (§8).
- **(b) Challenges (Q6, Q7).** The 10 one-click challenges are replaced by build-and-predict ones, with a tree editor in the tool folder (`platform/tools/bstar-tree/`). Nothing passes on page load, after Clear, from a preset or from the Reveal button; every Check recomputes from the learner's tree (§6, Stage 4). The dropdown editor (parent + side per block, swap and rotate buttons) stays the recommended UI.
- **(c) Check scripts (Q11).** Copied from the scratchpad to `../tools/lab05-notes/` with a `README.md` (run from the clone root). Re-run from there after the copy: tree count 5040, 4680 legal, order test 1764, node vs python 0 mismatches, E1–E3 results unchanged. (`pw_lab.py` was copied but not re-run.)
- **(d) Rotation (Q2, Q3, replaces the earlier "A may be turned" wording).** **Any block may turn 90 degrees (its w and h swap).** The "soft" flag and the aspect range are **not taught** (no mention in script, quiz, lab or lessons; the checker ignores the fields). The goal **"reach 24" is without rotation** (8 of 5040 trees); rotation is used for **E3 (make the chain fit the outline)**. Consequences: the checker's `rotate` works on any block; the lab challenge "reach 24" must reject any rotated block, and the E3 challenge accepts exactly the rotation set that makes the pack legal; a rotated block stays visible as rotated (label or marker) in figures and lessons.
- **(e) All other open questions keep their recommended answers:** Q1 teach bounding-box area as the score and print outline deadspace once, labelled; Q4 "move" = leaf move only; Q8 five parts; Q9 spoken "B-star tree", written "B*-tree", French "arbre B*"; Q10 new module files use `w`/`h`, checker accepts both.

## 8. Teacher list (to carry to the Stage 6 hand-off, not fixable by us)

- **The traversal rule (preorder, left subtree before right child) was unwritten** in the transcript, EXAMPLES and walkthrough; the code does it, no golden depends on it.

- `tiny_modules.json` uses `W`/`H` while `goldens.OUTLINE`, `metrics.py` and the JS use `w`/`h`.
- `common/test_solvers.py` only asserts legality of the B*, Polish and sequence-pair goldens, never coordinates; nothing checks JS ↔ Python sync (we found them equal for B*).
- `saSwap` swaps rectangles, not tree nodes, and breaks legality; the transcript and walkthrough say "swap, rotate, move" with no such functions anywhere.
- The shared lab shell says "challenges prefer the B* packer result" while only the button can pass; bstar challenge `nonneg` passes on an empty pack; there is no tree view.
- 99 `__pycache__` files are tracked in git; `common/__pycache__` exists.
- `scripts/module.sh --check` is a placeholder; README "Live" link points to another organisation's Pages site.
- `courses/learn_floorplanning/scripts/` contains generators (`deepen_content.py`, `generate_tools.py`, `scaffold_course.py`, `parity_audit.py`, `build_all_media.sh`, `capture_all_walkthroughs.sh`). I did not read or run them: **do not run them on this module** (Lab 03's enrich script rewrote transcripts with wrong claims).

## 9. Commands used (reproduce Stage 1 numbers)

```bash
export PYTHONDONTWRITEBYTECODE=1
python3 ~/.claude/skills/lab-upgrade/scripts/audit_lab.py . learn_floorplanning module02-03-bstar-tree bstar-tree
python3 ~/.claude/skills/lab-upgrade/scripts/lint_transcript.py courses/learn_floorplanning/module02-03-bstar-tree/transcript.md
python3 courses/learn_floorplanning/common/test_solvers.py
# scratchpad scripts (temporary): golden_node.mjs / golden_py.py (golden), explore*.py (5040 trees, swaps,
# rotations, order test, examples), all_node.mjs (node vs python on 5040 trees), examples_check.py (E1–E3),
# pw_lab.py (headless Chromium on /tools/bstar-tree/ served by `python3 -m http.server --directory platform`)
```

Status: Stage 1 finished; waiting for approval or answers to §7 before Stage 2.

---

## 10. Approved decisions (appended after Stage 1 review)

1. **Lesson engine gets a floorplan scene.** The `lesson-animator` engine has no floorplan scene today. It is built separately, after Stage 2, so it can read the checker's `--json` output (positions, skyline, counters). Stage 3 does not wait for it, but the storyboard written in Stage 3 targets that scene.
2. **Order of work:** Stages 1–5, then an animated lesson for every part (the "Lessons for every part" table in §6, i.e. the former optional Stage 7), then Stage 6 (final check and hand-off). Stage 6 therefore also covers the lessons.
3. **One fixed colour per block everywhere, and fixed link styles.**
   - Colour by **module id**, same in figures, deck, lab, lessons and site: A blue, then B, C, D, E in the palette order. Source palette: `PAPER_PALETTE` in `floorplanning-core.js` (`drawFloorplan(..., {paper: true})`): A `#1d4ed8` blue, B `#0f6b5c`, C `#b45309`, D `#7c3aed`, E `#be123c`.
   - Tree links: **left child = solid line, right child = dashed line**, in every tree drawing (figures, lab, lessons). Legend: solid = "next door", dashed = "upstairs".
   - Two traps found while reading the shared code (not fixed there, worked around in our files): (a) the non-paper palette used by the lab canvas starts with teal for A (`PALETTE`, `#2a6f6a`), so the lab must use the paper palette or its own drawing; (b) `drawFloorplan` picks the colour from the **index in the sorted list of placed ids**, so a partial pack (e.g. only B and D placed) shifts every colour. Our figures, lab and lessons key the colour to the module id (a fixed id → colour map), never to the index.
4. **Stage 3 writes each part so it can become a lesson.** Rules for the script: one picture per sentence (every sentence maps to one state of the scene: which node lights up, which box moves, which counter changes); the key words are actually spoken (every word shown on screen as a label or counter, such as "next door", "upstairs", "skyline", "bounding box", is said aloud in that sentence, so word-timed highlighting works); no sentence refers to something that is not on screen at that moment. Each part's storyboard lists, per sentence, the scene state and the spoken key words. Lint and the repetition rules still apply.

Status: Stage 1 approved with the decisions above and those of §7b. Next: Stage 2 (content and goldens).

---

## 11. Stage 2 — content and goldens (done 2026-10-30)

Files touched, all inside the module folder (plus one helper outside every repo): `examples/bstar_check.py`, `examples/{golden,lift,order,floor,swap,rotate,move,best}.json`, `examples/wrong/{right_first,no_contour}.py`, `EXAMPLES.md` (LF), `quiz.json`, `CHECKLIST.md`, `README.md` (all three CRLF, as before), `assets/_demo.sh`; `../tools/lab05-notes/ok_impl.py`. `common/`, `examples/tiny_modules.json`, `platform/` untouched (`git status` shows only these files). No `__pycache__` was created (checked after a run without `PYTHONDONTWRITEBYTECODE`).

### Verify

```bash
export PYTHONDONTWRITEBYTECODE=1
cd courses/learn_floorplanning/module02-03-bstar-tree
python3 examples/bstar_check.py                                        # 61 PASS, 0 FAIL, 0 SKIP
python3 examples/bstar_check.py --vs-node                              # PASS: floorplanning-core.js packBstar, 5040 trees + 11 example scenes
python3 examples/bstar_check.py --impl examples/wrong/right_first.py   # 25 PASS, 4 FAIL, exit 1
python3 examples/bstar_check.py --impl examples/wrong/no_contour.py    # 24 PASS, 5 FAIL, exit 1
python3 examples/bstar_check.py --impl ../../../../tools/lab05-notes/ok_impl.py   # 29 PASS (independent unit-column skyline, shares no code)
python3 examples/bstar_check.py --json > bstar.json                    # data for figures and lessons
bash assets/_demo.sh
```

### What the checker is

- **Reference** (`pack_bstar`, `bounding_box`, `legality`, `swap`, `rotate`, `move_leaf`, `leaf_moves`, `parse_tree`/`fmt_tree`, `tree_problems`, `all_trees`, `stats`, `ops_table`, `legal_rotations`); the rule is in the module docstring (preorder, left subtree before right child, skyline, `x` rules, `y` = highest skyline under the footprint, bottom-left origin, integers).
- **Learner API** (`--impl`): `pack_bstar`, `bounding_box`, `is_legal`, `swap`, `rotate`, `move_leaf`; 29 checks, SKIP for functions not defined, a crash counts as FAIL. Includes: reversed module list, input not mutated, swap/rotate involution, `move_leaf` refuses a non-leaf and a taken slot, and **all 5040 labelled trees** compared with the reference (this line catches both wrong packers).
- **Reference-only checks** (32): the 8 example files agree with the reference (expected positions, boxes, `then` operations, `derived_from`); reference == `common/pack.py` `pack_bstar` on all 5040 trees (read-only import); the stats table; the ops tables; the x/y rules on all 5040 trees; 7x8 right-first box; chain widths 12 and 10; area sum 23 is prime; deadspace 57 vs 4.
- **W/H**: `load_modules()` reads `examples/tiny_modules.json` and accepts `W/H` or `w/h`; the soft fields are ignored (decision 7b-d). Any block may turn 90 degrees; rotation is applied to the module list before packing (`with_rotated`), the tree never changes.
- **`--json`** keys: `colors` (A..E fixed hex), `outline`, `modules`, `scenes[]` (`golden, lift, order, floor, swap_start, swap_after, rotate_start, rotate_after, move_start, move_after, best`), `relations[]` (op + args between scenes), `stats`, `ops`, `chain_legal_rotations`. Each scene: `tree` (text), `tree_nested`, `walk` (preorder ids), `rotated`, `modules` (after rotation), `pack`, `bbox`, `area`, `wasted`, `legal`, `outside`, `outline_deadspace`, and `steps[]` with `k, id, parent, side, x, y, w, h, supported_by` (ids or `["floor"]`), `hole_under` (empty squares between skyline and block), `contour` (merged `[x1, x2, height]` after this placement) and `bbox` after this placement. Stage 3 figures and the lessons read this file; no number is typed by hand.

### Numbers (all printed by the checker)

| Item | Value |
|---|---|
| golden `A(B(C(E,-),-),D)` | A(0,0) B(3,0) C(5,0) D(0,2) E(7,0); 9x3 = 27; wasted 4; legal |
| lift `C(B(A(E,-),-),D)` (golden with A,C swapped) | D (0,3) held up by B, hole 2; 9x4 = 36; wasted 13 |
| order `A(B(C(-,E),D),-)` | D (3,4) held up by E; 7x5 = 35 (right first: 7x8) |
| floor `A(B(C(-,D(E,-)),-),-)`, A turned | = `SOFT_A_PACK` of `common/goldens.py`; D (4,2) overhangs C (hole 2), E (7,0) |
| swap start `A(B(C(D,-),-),E)` | 10x4 = 40, wasted 17; `swap(D,E)` gives the golden (27). Of 10 swaps only this reaches 27; next best `swap(A,D)` = 30 |
| rotate chain `A(B(C(D(E,-),-),-),-)` | 12x3, E (10,0), illegal. D turned: 10x3 = 30, wasted 7, legal. 12 of 32 turn-sets are legal; the only single turn is D |
| move `move_leaf(D,B,right)` on the swap start | `A(B(C,D),E)`, 7x4 = 28, wasted 5 (D (3,3), held up by B, hole 1). Best single move is 28 (two moves); best single turn 32 |
| best `A(D,C(E(B,-),-))` | 6x4 = 24, wasted 1, B (4,1) lifted onto D; 8 trees reach 24 (listed in `best.json` and EXAMPLES.md) |
| golden, one operation | none improves: 10 swaps / 5 turns / 8 moves all >= 27 (4 / 2 / 1 keep 27) |
| 5040 trees | 4680 legal; 0 overlap; 120 too wide, 240 too tall; 216 legal trees beat 27; best area 24; **1764** differ if right child first; **2714** differ without the skyline; 360 trees with a right child above its parent's top; 254 with a left child above its parent's y |

All Stage 1 numbers were reproduced (5040, 4680, 360, 254, 1764, 216, 8 at 24, 120/240, swaps/turns/moves of the golden).

### Proof the checker catches wrong code

| `--impl` | Golden lines | FAIL lines |
|---|---|---|
| `wrong/right_first.py` (right child before left subtree) | PASS (golden, bbox, legal) | `lift`, `order`, `best`, all 5040 trees (**1764** differ; first `A(-,B(-,C(E,D)))`) |
| `wrong/no_contour.py` (y from the parent: left = parent.y, right = parent.y + parent.h) | PASS | `lift`, `floor`, `order`, `best`, all 5040 trees (**2714** differ) |
| `ok_impl.py` (different algorithm, no shared code) | PASS | none (29 PASS) |
| empty file | n/a | 0 PASS, 0 FAIL, 29 SKIP |

Takeaway for the script: **the golden tree alone cannot tell a right packer from either wrong one**, which is why Parts 2 and 3 use `order`, `lift` and `floor`. `floor` is the only example `right_first` gets right and `no_contour` gets wrong; `order` and `lift` catch both.

### Quiz (8 items, `passing_score` 0.67 kept)

q1 D.y after swapping A,C = 3 · q2 E.x = 7 · q3 left child same y? false (floor) · q4 right-first same pack? false (1764) · q5 which single turn fits the chain: D · q6 which swap gives 27: D,E · q7 can one operation beat the golden? false · q8 smallest area: 24. Every answer was recomputed with the packer (see the commands above); not a hand calculation.

### Decisions taken in Stage 2

- Example `expect` blocks are written from the reference by `--write-examples` and checked on every run; the global counts are pinned in `GOLDEN` (checked against `common/pack.py` and the JS packer). Idea sentences in the JSON are the only hand-written text.
- Two extra example trees beyond the Stage 1 plan: `floor` (left child falls to the floor, = `SOFT_A_PACK`) and `move` (the leaf-move example on the swap start). `best.json` also lists all 8 area-24 trees.
- The wrong packers live in `examples/wrong/` (shipped, referenced from EXAMPLES.md) so a learner can see what FAIL looks like.
- The README "Live" link still points to another organisation's Pages site (teacher list, left unchanged). The old `module.sh --check` claim and the wrong `../../common` path are removed.
- `CHECKLIST.md` Track B wording follows the Stage 4 plan (build golden, D at y = 3, chain fix with one rotation, swap, move, beat 27, stretch 24); **re-read it when the lab exists** and adjust to the real challenges.
- Terminology fixed for the script: "next door" (left child), "upstairs" (right child), "skyline" (= contour, say "skyline" aloud), "bounding box", "wasted squares" for bounding-box deadspace, "outline deadspace 57" said once.

### Open questions

1. `ok_impl.py` sits in `../tools/lab05-notes/` (outside every repo), not in the module, so it does not ship as an answer. Say if you want it in `examples/wrong/` renamed, or dropped.
2. `lift` also fails right-first, so it is a second order-sensitive example (as well as `order`). Fine for the script, but "order" is then not the only reason to say "left subtree first". Keep both?

Status: Stage 2 finished. Next: Stage 3 (beginner script in 5 parts and figures), reading `--json`.

---

## 12. Stage 3 — five-part script, figures and frames (done 2026-10-30)

Files touched in the module: `transcript.md` (rewritten, LF), `outline.yaml`, `slides.md`, `slides.pptx`, `slides.pdf`, `build.log` (pipeline outputs), `assets/STEPS.md` (rewritten by the teacher's capture script, put back to CRLF), `assets/steps/01-next-door.png … 05-done.png` (new), the old frames `01-root, 02-left-chain, 03-right-d, 04-legal, 05-takeaway.png` **deleted** (git shows `D`; the site's walkthrough page must use the new names), 19 figures `assets/*.png`, `assets/real-shell.png` + `.txt`, `README.md` (file tree, CRLF kept). Nothing outside the module folder changed (`git status`); no `__pycache__` was created. No audio or video was built.

Outside every repo: `../tools/lab05-figures/` = `facts.py`, `bstar-draw.js`, `make_figures.py` (`--lang fr`), `patch_walkthrough.py`, `capture_fr_frames.py`, `run_all.sh`, `README.md` (generated there: `facts.json`, `steps.json`, `wt-platform/`).

### Verify

```bash
export PYTHONDONTWRITEBYTECODE=1
bash ../tools/lab05-figures/run_all.sh                 # from the test2 folder: facts (all spoken numbers asserted), frames, STEPS.md CRLF, 19 figures, shell
S=.cursor/skills/module-slides/scripts; M=courses/learn_floorplanning/module02-03-bstar-tree; PY=~/eda-venv/bin/python
$PY ~/.claude/skills/lab-upgrade/scripts/lint_transcript.py $M  # 32 slides, 1184 words (~7.9 min), Problems: 0
$PY $S/transcript_to_outline.py $M && $PY $S/build_pptx.py $M
$PY $S/verify_clip.py $M && $PY $S/verify_transcript_consistency.py $M      # OK, OK
bash $S/pptx_to_pdf.sh $M/slides.pptx && pdfinfo $M/slides.pdf | grep Pages  # 32
```

Every PDF page was looked at (50 dpi contact sheets): bullets complete, no cut sentence, every figure and frame present, title subtitle on one line. A small script also checked that the 5 frame captions and titles in `STEPS.md` equal the spoken text and titles of slides 8-12.

### Part boundaries (for Stage 5 `PARTS`; PDF page = transcript slide until slide 29, then +1 for the code slide)

| Part | Title | Transcript slides | PDF pages | Words | Time at 150 wpm | Opens with | Ends with "Pause and guess" |
|---|---|---|---|---|---|---|---|
| 1 | A tree is a recipe | 1-7 | 1-7 | 261 | 1:44 | hook: "Five blocks, one frame, and a tree that says where each block goes." | where does B's left edge go? |
| 2 | Walking the tree (walkthrough block) | 8-12 | 8-12 | 188 | 1:15 | answer: "B goes next door, at x equals three" | swap A and C: does D still land at y = 2? |
| 3 | The skyline and the score | 13-19 | 13-19 | 232 | 1:33 | answer: "No: D lands one square higher." | will the all-left-children row fit in the outline? |
| 4 | Too wide: turn a block | 20-24 | 20-24 | 204 | 1:22 | answer: "No, it will not fit." | can any tree beat 27, and what is the smallest box? |
| 5 | The tightest floorplan, your turn | 25-31 | 25-32 (30 = bash code slide) | 299 | 2:00 | answer: "Yes: many trees beat twenty-seven, and the best need only twenty-four" | can two lists describe our best floorplan (24)? → next lab |

Total 1,184 spoken words, 31 transcript slides, 32 PDF pages. The Part 5 teaser was checked with the course solver: `common/pack.py pack_sequence_pair` over all 120 x 120 sequence pairs gives a smallest box of 24 (16 pairs), and 2 pairs give exactly the `best` pack (positions equal), so the answer is yes.

### Examples used in the video (at most four, as asked)

| Tree | Used for | Slides |
|---|---|---|
| `golden` `A(B(C(E,-),-),D)` | learn the rule (frames), then the bounding box 9x3 = 27, 4 wasted | 4-12, 16-17 |
| `lift` `C(B(A(E,-),-),D)` (golden with A and C swapped) | the skyline: D lifted to y = 3 by B, hole of 2; also **the swap** (27 → 36) | 13-15, 18 |
| `rotate` chain `A(B(C(D(E,-),-),-),-)` | changing the tree changes the picture: all left children = a row 12 wide, E sticks out by 2, not legal; turn D → 10 wide, legal | 19-23 |
| `best` `A(D,C(E(B,-),-))` | the 24 target: B lifted onto D at y = 1, 6x4 = 24, 1 wasted; 23 impossible | 25-27 |

Decision: **rotate rather than swap** for the third tree. Reasons: `lift` already is one swap of the golden (so swap is shown with its score, 27 → 36, without a fifth tree); the chain is the only example where a tree fails (sticks out), which makes "legal" and "never an overlap" concrete; and its widths add up to numbers a beginner can follow (3+2+2+3 = 10, then 12). `swap.json`, `order.json`, `floor.json`, `move.json` stay in EXAMPLES.md (quiz q6 on the D,E swap therefore refers to EXAMPLES, not to the video). "Move a leaf" is one sentence on a text slide (24), with no packed example.

### Terms (each defined once, where it is first used)

floorplan (3), block (2), outline (3), B*-tree spoken "B-star tree" (4), node and root (4), left child and right child (4, then 6 "next door" and "upstairs"), x and y from the lower-left corner (5), walk order (9), skyline (14, a city seen from far away + a Tetris piece dropping), hole (15), bounding box (16), wasted space (17), legal (21), turn (23), leaf (24).

### Repetition check (scan of the transcript; slide numbers)

- "next door" defined on 6; used to place blocks on 8, 10, 13, 20; recap 30. "upstairs" 6, 11 (placing D), 30. "same left edge" 6 and recap 30 only (slide 11 now says "starts at x equals zero, like A").
- "the widths add up" only on 10 (slide 20 now says "three, two, two and three make ten").
- skyline: taught on 14; used on 22 (why no overlap), 26 (B lifted), 28 (lab), recap 30. Bounding box: 16 and recap. Wasted: 17, then the numbers on 18 and 26, the 23 argument on 27, recap.
- Never an overlap: 22 and recap. Legal: 21 (defined), 23 (legal again).
- One "Pause and guess" per part, at its end (7, 12, 19, 24, 31).

### Figures (tall 680x820 CSS px, 2x) and step figures

`blocks-1 → blocks` (2-3), `tree-golden` (4), `rule-1 → rule` (5-6), `pause-b` (7), `lift-1 → lift-2 → lift` (13-15), `golden-box-1 → golden-box` (16-17), `lift-box` (18), `chain-1 → chain-2 → chain → chain-check` (19-22), `turn` (23), `best-1 → best` (25-26). Each step figure is the next figure with fewer blocks placed or fewer layers (same size, same scale: the floor panel always spans x = 0 to 12.4 so nothing jumps). Slides average 38 words (~15 s), with a new picture on every slide except the three text slides 24, 27, 28.
Drawing rules (also in the figures README): colour by block id (A blue, B, C, D, E in the paper palette), never by index; left link solid, right link dashed; y up from the lower-left corner; only spoken numbers are written on a figure; a node not placed yet is a coloured ring, a placed one is filled.
Frames: the 5 frames now draw the tree next to the floorplan (`drawBstarFrame` in a scratch copy of the viewer); 940x468 (the teacher's original frames were 940x456; the 12 px come from the CSS override used for Lab 03).

### Lesson plans (one line = one sentence = one scene state; for the `lesson-animator` floorplan scene)

Notation: tree = scene id from `--json`; k = blocks placed (in walk order); SKY = skyline drawn; BOX = bounding box drawn; anchors = words shown on screen and spoken in that sentence (word-timed highlight).

**Part 1 — A tree is a recipe** (golden)

| # | Sentence (short) | Scene | Anchors |
|---|---|---|---|
| 1.1 | Five blocks, one frame, and a tree… | tray of 5 blocks, empty outline, golden tree faded | five blocks, frame, tree |
| 1.2 | Can you build the picture from the tree alone? | tree lights up | picture, tree |
| 1.3 | …you will find the tightest picture of all | outline pulses | tightest |
| 2.1 | A chip is made of… blocks | tray only (outline hidden) | blocks |
| 2.2 | Ours has five blocks, named A to E | letters pop A→E | A, E |
| 2.3 | …squared paper, count each width and height | inner grid of each block flashes | width, height |
| 3.1 | A floorplan says where each block sits | outline fades in under the tray | floorplan |
| 3.2 | …a frame called the outline | outline border thickens | outline |
| 3.3 | ten squares wide and eight squares tall | dimension lines "10", "8" | ten, eight |
| 3.4 | The tighter…, the smaller the chip | tray blocks slide closer together | tighter |
| 4.1 | …a recipe instead: a B-star tree | golden tree drawn (nodes = coloured rings) | B-star tree |
| 4.2 | Each block is one node | each tray block shrinks into its node | node |
| 4.3 | The top node, A, is called the root | "root" label on A | root |
| 4.4 | …a left child and a right child | labels on A–B (solid) and A–D (dashed) | left child, right child |
| 5.1 | The root goes in the lower-left corner | A drops into the corner, k = 1 | lower-left corner |
| 5.2 | x counts squares to the right, y counts up | axis arrows x, y | x, y |
| 6.1 | A left child goes next door… | arrow from A's right side "next door"; A–B link labelled | next door |
| 6.2 | A right child goes upstairs… same left edge | arrow up from A "upstairs"; A–D link labelled | upstairs, same left edge |
| 6.3 | The names sound backwards… | both labels blink | left, next door, right, upstairs |
| 6.4 | solid line = next door, dashed = upstairs | A–B solid and A–D dashed pulse | solid, dashed |
| 7.1 | A is three squares wide and two tall | dims "3", "2" on A | three, two |
| 7.2 | B is A's left child | B highlighted in the tree | B, left child |
| 7.3 | Pause and guess: where does B's left edge go? | "?" next to B; **auto-pause** | B's left edge |

**Part 2 — Walking the tree** (golden; the 5 walkthrough frames)

| # | Sentence (short) | Scene | Anchors |
|---|---|---|---|
| 8.1 | B goes next door, at x = 3: A starts at 0 and is 3 wide | B drops at x = 3, k = 2; dim "3"; counter x = 0 + 3 = 3 | next door, x equals three |
| 8.2 | Nothing is under B, …floor, y = 0 | floor line under B glows (no skyline yet); counter y = 0 | floor, y equals zero |
| 9.1 | …one at a time, in a fixed walk order | walk path runs over the tree | walk order |
| 9.2 | Place a node, then its left side, only then its right child | A, then B-C-E chain, then D highlighted in turn | node, left side, right child |
| 9.3 | So the walk goes A, B, C and E, and D comes last | walk list "A, B, C, E, D" | A, B, C, E, D |
| 10.1 | C… next door to B, x = 5 | C drops, k = 3; counter x = 5 | C, next door, five |
| 10.2 | E… next door to C, x = 7 | E drops, k = 4; counter x = 7 | E, seven |
| 10.3 | The widths simply add up: 3 + 2 + 2 = 7 | dim "3 + 2 + 2 = 7" | three, two, seven |
| 11.1 | …the walk comes back to D, A's right child | walk arrow back to A, D highlighted | right child |
| 11.2 | D goes upstairs… x = 0, like A | D ghost above A at x = 0 | upstairs, x equals zero |
| 11.3 | It sits on top of A, at y = 2 | D lands, k = 5; counter y = 2 | top of A, y equals two |
| 12.1 | All five placed, every one inside the outline | outline flashes green | inside the outline |
| 12.2 | Pause and guess: swap A and C, does D still land at y = 2? | A and C nodes wiggle; **auto-pause** | swap A and C, y equals two |

**Part 3 — The skyline and the score** (lift, then golden)

| # | Sentence (short) | Scene | Anchors |
|---|---|---|---|
| 13.1 | No: D lands one square higher | answer card over the golden picture | one square higher |
| 13.2 | …A and C swapped: C is the root, A takes C's old place | tree nodes A and C swap places (lift tree), k = 0 | C, root, A |
| 13.3 | C, B, A and E still go next door | lift k = 1→4 one by one | C, B, A, E, next door |
| 14.1 | …picture the blocks as a city, seen from far away | blocks dim to silhouettes on a sky background | city |
| 14.2 | The top edge… is the skyline | SKY draws left to right, label | skyline |
| 14.3 | A new block drops from the sky, like a Tetris piece… | D ghost at the top falls toward SKY | drops, Tetris, touches the skyline |
| 15.1 | D is three wide, …over C and part of B | D footprint x 0-3 shaded on SKY | three wide, C, B |
| 15.2 | B is three tall, so it stops D at y = 3 | D lands, k = 5; B glows; counter y = 3 | three tall, y equals three |
| 15.3 | …a hole of two empty squares above C | 2 hole cells hatched, label "hole" | hole, two |
| 16.1 | So which floorplan is better? | golden and lift side by side (k = 5 both) | better |
| 16.2 | …the bounding box: the smallest rectangle around all the blocks | BOX on golden | bounding box |
| 16.3 | nine wide and three tall: twenty-seven squares | label "9 × 3 = 27" | nine, three, twenty-seven |
| 17.1 | The five blocks cover twenty-three squares | blocks glow, "blocks: 23" | twenty-three |
| 17.2 | The other four… empty: that is wasted space | 4 cells hatched, "wasted: 4" | four, wasted space |
| 17.3 | Fewer wasted squares means a tighter floorplan | wasted counter pulses | fewer wasted squares |
| 18.1 | The swapped tree needs a box nine by four: 36, 13 wasted | BOX + hatch on lift, "9 × 4 = 36", "wasted: 13" | nine by four, thirty-six, thirteen |
| 18.2 | So one swap of two names changed the picture and the score | golden ↔ lift toggle | one swap, picture, score |
| 18.3 | Twenty-seven became thirty-six: the first tree is better | "27 → 36"; tick on golden | twenty-seven, thirty-six, first tree |
| 19.1 | …a tree where every child is a left child | chain tree drawn (all solid links), empty outline | left child |
| 19.2 | Pause and guess: will this long row fit inside the outline? | **auto-pause** | long row, outline |

**Part 4 — Too wide: turn a block** (rotate chain)

| # | Sentence (short) | Scene | Anchors |
|---|---|---|---|
| 20.1 | No, it will not fit | answer card, chain k = 0 | not fit |
| 20.2 | Every block goes next door: three, two, two and three make ten | A, B, C, D drop, k = 1→4; running width 3, 5, 7, 10; dim "3 + 2 + 2 + 3 = 10" | next door, three, two, ten |
| 20.3 | The outline is already full, and E is still waiting | E highlighted in the tree, ghost outside | outline, E |
| 21.1 | E lands at x = 10, so the row is twelve squares wide | E placed, k = 5; dim "12" | x equals ten, twelve |
| 21.2 | E sticks out of the outline by two squares | E red border, "sticks out by 2" | sticks out, two |
| 21.3 | A floorplan is legal only when every block is inside the outline | outline highlighted | legal, inside the outline |
| 21.4 | So this row is not legal | "not legal" | not legal |
| 22.1 | Notice that the blocks never overlap | "no overlap ✓" | never overlap |
| 22.2 | Each block drops onto the skyline… | SKY drawn | drops, skyline |
| 22.3 | …sticking out is the only way to fail | "sticks out ✗" | sticking out |
| 23.1 | We can turn a block on its side, …width and height swap | D rotates in place (3x1 → 1x3), ↻ badge (rotate_after modules) | turn, width, height |
| 23.2 | Turn D, and it becomes one wide and three tall | D dims "1" and "3" | one wide, three tall |
| 23.3 | Now the row is ten wide, …fits exactly, legal again | E slides from x = 10 to 8; dim "10"; "legal" | ten, fits, legal |
| 24.1 | Turning is one of three small changes | card: turn / swap / move, turn ticked | three small changes |
| 24.2 | You can also swap two names, as we did with A and C | golden ↔ lift thumbnails | swap, A and C |
| 24.3 | Or move a leaf, a block with no children, to a free spot | golden tree: leaf E outlined, dotted arrow to a free slot (no new pack shown) | move a leaf, no children, free spot |
| 24.4 | Each change gives a new floorplan, with a new score | score counter flickers | new floorplan, new score |
| 24.5 | Pause and guess: can any tree beat 27, smallest box? | "27 ?"; **auto-pause** | twenty-seven, smallest box |

**Part 5 — The tightest floorplan, your turn** (best)

| # | Sentence (short) | Scene | Anchors |
|---|---|---|---|
| 25.1 | Yes: many trees beat 27, the best need only 24 | counter "27 → 24" | twenty-seven, twenty-four |
| 25.2 | Here is one of the best trees | best tree drawn, k = 0 | best trees |
| 25.3 | Its walk places A, D, C and E, and B comes last | k = 1→4 one by one, SKY on, B highlighted | A, D, C, E, B |
| 26.1 | Under B, the skyline is the top of D, so B lands at y = 1 | B ghost falls onto D, k = 5; "y = 1" | skyline, top of D, y equals one |
| 26.2 | It fills the gap, …six wide and four tall: 24 squares | BOX, "6 × 4 = 24" | six, four, twenty-four |
| 26.3 | Only one square is wasted | 1 cell hatched, "wasted: 1" | one square |
| 27.1 | Could a box of 23 squares, with nothing wasted, hold all five? | "23" over the best picture | twenty-three, nothing wasted |
| 27.2 | Twenty-three squares only make a rectangle one square thick | a 1-thick strip of 23 squares runs off the panel | one square thick |
| 27.3 | Block B is too thick for that, so 24 is the best possible | B bumps the strip, red ✗; "24" badge | B, too thick, twenty-four |
| 28.1-28.4 | Browser lab: edit the tree…; lift D higher, make the long row fit, reach 24 | lab card (Stage 4 screenshot), three challenge chips with lift, chain, best thumbnails | browser lab, skyline, lift D higher, long row, twenty-four |
| 29.1-29.4 | Implement track… all five thousand and forty trees | terminal lines appear (real-shell) | packer, exact rules, checker, five thousand and forty |
| 30.1-30.6 | Remember (one line each) | one icon per line: next-door arrow, upstairs arrow, walk path, SKY, BOX, outline | the recap words |
| 31.1-31.4 | Your turn…; sequence pair; Pause and guess: can two lists describe our best floorplan? | track cards, then "two lists" teaser over the best picture; **auto-pause** (answered in the next lab) | browser lab, Python, checklist, quiz, sequence pair, two lists, twenty-four |

Known exceptions to "every word on screen is spoken": the viewer chrome of the frames ("B*-TREE", "Step 1 / 5 · next-door · module02-03-bstar-tree", "Explanation"), the slide footer, and the terminal and code slides (29-30). The lessons do not show these.

### Decisions taken in Stage 3

- Third example = `rotate` chain, swap shown through `lift` (above). The video uses exactly four trees.
- Slide 6 title is "Left is next door, right is upstairs": a title starting with "Next" makes the teacher's `prose_to_bullets.py` replace the bullets with "Complete the quiz for this part" + one sentence (found on the first PDF; `lint_transcript.py` does not flag it). Worth adding to the skill's pipeline-gotchas.
- Figures are drawn by our own `bstar-draw.js` (canvas, same palette and font family as `drawFloorplan(..., {paper: true})`), not by `drawFloorplan`, because `drawFloorplan` colours by index (a partial pack shifts colours) and has no tree. The frames use the same code inside the scratch viewer, so slides and frames match.
- The real-shell screenshot shows the reference passing, then `--impl wrong/right_first.py` caught (4 FAIL), matching slide 29 ("then run it on your own file").
- Browser lab slide (28) has no picture yet: Stage 4 recaptures `assets/lab-starter.png` from the new lab; then add `![Browser lab starter](assets/lab-starter.png)` to slide 28 and rebuild (it becomes a full-slide image, the text stays spoken).
- French: `make_figures.py --lang fr` and `capture_fr_frames.py` work (19 figures and 5 frames written to the scratchpad as a test); the French labels and frame captions are a first draft for Stage 5.

### Teacher list (add to §8)

- `floorplanning-algos.js` `bstar-tree` block still holds the old frame text ("Left children go right-of; right children go above via the contour", "Perturbing the tree — swap, rotate, move — will feed simulated annealing later"); the new text is in `assets/STEPS.md`. The viewer draws rectangles only (no tree), and `drawFloorplan` colours blocks by index in the sorted list of placed ids, so a block changes colour between frames when fewer blocks are placed.
- The old frame files `01-root.png … 05-takeaway.png` were replaced by `01-next-door.png … 05-done.png` (step ids changed); any page that links the old names must follow `STEPS.md`.

### Open questions

1. Stage 2's two open questions are still open (`ok_impl.py` location; keep `lift` as a second order-sensitive example — the video now uses `lift` only for the skyline and the swap).
2. Part 5 is the longest (2:00 at 150 wpm, the upper limit). If the voice runs slower than 150 wpm, the lab and implement slides (28-29) can lose one sentence each.

Status: Stage 3 finished (no audio). Next: Stage 4 (interactive lab), then add the lab screenshot to slide 28 and rebuild the deck.

---

## 13. Stage 3 follow-up (2026-10-30, after review)

### Stage 2 open questions, answered
1. `ok_impl.py` stays in `../tools/lab05-notes/` (outside every repo, not shipped with the module).
2. Keep both examples: `lift` = the skyline example, `order` = the walk-order example (both stay in EXAMPLES.md and the checker; the video uses only `lift`).

### Walkthrough frames back to the teacher's names
The 5 frames keep the **teacher's file names**, which come from the step ids of the shared `floorplanning-algos.js`: `01-root.png, 02-left-chain.png, 03-right-d.png, 04-legal.png, 05-takeaway.png`, now with the new pictures (tree + floorplan). `patch_walkthrough.py` uses those ids; `01-next-door … 05-done.png` are removed, so git now shows the five frames as **modified** (`M`), not deleted, and the §12 teacher-list line about renamed frames no longer applies. `STEPS.md` (CRLF), `transcript.md` image paths and `slides.md` match; a check confirmed the captions, titles and image names of `STEPS.md` equal slides 8-12. `capture_fr_frames.py` writes the same names.
Side effect: the viewer banner of each frame shows the step id ("Step 2 / 5 · left-chain"), which does not always describe the frame (frame 2 is the walk order, frame 3 the left chain, frame 4 D upstairs, frame 5 the end). It is viewer chrome, not spoken.

| Frame | File (teacher's name) | Content |
|---|---|---|
| 1 | `01-root.png` | B goes next door, at x = 3 |
| 2 | `02-left-chain.png` | The walk: A, B, C, E, then D |
| 3 | `03-right-d.png` | C and E go next door |
| 4 | `04-legal.png` | D goes upstairs, on A |
| 5 | `05-takeaway.png` | Five blocks placed |

### Part 5 answers its own closing question
Slide 31 now ends: "Pause and guess: can two lists describe our best floorplan, with twenty-four squares? Yes: two lists are enough. That's the sequence pair, in the next lab." (checked in §12: 2 sequence pairs give exactly the best pack). The slide has 6 sentences, all 6 shown as bullets. Lesson plan line 31: after the auto-pause, the answer card "Yes: two lists are enough" appears (anchors: yes, two lists, sequence pair, next lab).

Updated numbers: Part 5 = slides 25-31, PDF 25-32, **313 words, 2:05** at 150 wpm (limit 2:10). Total **1,198 words** (~8.0 min); other parts unchanged (261, 188, 232, 204). Deck: 32 slides, 32 PDF pages, pages 8-12 and 32 looked at again.

### Teacher list (add to §8)
- **Don't rerun `courses/learn_floorplanning/scripts/capture_all_walkthroughs.sh` on module02-03** (it overwrites the frames and injects the old captions into `transcript.md`): it runs `capture_algorithm_walkthrough.py <module> --inject-transcript` for module02-03 against the teacher's viewer, which still has the old rectangle-only frames and old text.

### Verify (all run after the change)
```bash
export PYTHONDONTWRITEBYTECODE=1
bash ../tools/lab05-figures/run_all.sh        # facts.py: "all spoken numbers checked"; frames 01-root ... 05-takeaway
$PY ~/.claude/skills/lab-upgrade/scripts/lint_transcript.py $M   # 32 slides, 1198 words, Problems: 0
$PY $S/transcript_to_outline.py $M && $PY $S/build_pptx.py $M && $PY $S/verify_clip.py $M && $PY $S/verify_transcript_consistency.py $M
bash $S/pptx_to_pdf.sh $M/slides.pptx         # 32 pages
```

---

## 14. Stage 4 — interactive browser lab (done 2026-10-30)

Files touched. Tool folder: `platform/tools/bstar-tree/` = `bstar-tree-lab-model.js` (new, pure), `bstar-tree-strings.js` (new, every UI word), `bstar-tree.js` (rewritten, UI), `index.html` (lead sentence + local `<style>`), `tests/` (new: `test_model_vs_checker.py`, `model_dump.mjs`, `test_lab_playwright.py`). Module: `transcript.md` (slide 28 gets `![Browser lab starter](assets/lab-starter.png)`), `assets/lab-starter.png` (new), `CHECKLIST.md` Track B (rewritten to the 9 real challenges, CRLF kept), `README.md` (file tree line, CRLF kept), pipeline outputs (`outline.yaml`, `slides.md`, `slides.pptx`, `slides.pdf`, `build.log`). Outside every repo: `../tools/lab05-figures/capture_lab.py` + README section. `common/`, `platform/assets/*` untouched; `git status` shows only the two allowed folders; no `__pycache__` created. No audio or video built.

### Verify

```bash
export PYTHONDONTWRITEBYTECODE=1
python3 platform/tools/bstar-tree/tests/test_model_vs_checker.py          # 185 PASS, 0 FAIL (~20 s, needs node)
~/eda-venv/bin/python platform/tools/bstar-tree/tests/test_lab_playwright.py   # 110 ok: 9 positive, 82 negative, 15 colour, 4 page (~30 s; serves platform/ itself, or --url)
python3 -m http.server 8080 --directory platform & python3 ../tools/lab05-figures/capture_lab.py --module courses/learn_floorplanning/module02-03-bstar-tree
S=.cursor/skills/module-slides/scripts; M=courses/learn_floorplanning/module02-03-bstar-tree; PY=~/eda-venv/bin/python
$PY $S/transcript_to_outline.py $M && $PY $S/build_pptx.py $M && $PY $S/verify_clip.py $M && $PY $S/verify_transcript_consistency.py $M
bash $S/pptx_to_pdf.sh $M/slides.pptx      # 32 pages; lint: 1198 words, Problems: 0
```

### Architecture

- **Model** (`bstar-tree-lab-model.js`, no DOM): `parseTree/fmtTree/preorder`, `swap`, `rotate`/`withRotated`, `moveLeaf`, `leafMoves`, `allTrees` mirror `bstar_check.py` (same refusal order for `moveLeaf`); packing = `packBstar` of `floorplanning-core.js` (read-only import) on a module list with turned blocks' w and h exchanged; `score`, `legality`, `skyline` (final contour, merged). Learner state: `place[id] = {parent: null|"root"|id, side}`, `rotated`, `base` (what the tree was loaded from: `empty`, a preset, or `reveal`), `packed {sig, pack}`, `seen` (sigs packed since Start), `guess {value, sig, blind}`, `ops`. `readTree` turns the menus into a tree plus problems (`no-root`, `two-roots`, `slot-twice`, `parent-out`, `cut-off`) and the loose blocks. Any tree or turn change wipes the pack's sig, so even an edit-and-undo needs a new Pack. Messages and Check reasons are codes; no words in the model.
- **UI** (`bstar-tree.js`): shared `createChallengeLab` chrome (read-only); the shared canvas is hidden and replaced by two SVGs side by side: the tree (in-order layout as in the figures, left link solid, right link dashed, walk-order badges, "root" tag, ↻ for turned blocks, loose blocks as rings) and the floor (10x8 grid with ticks, blocks with unit squares, red border when sticking out, yellow skyline, dashed bounding box with "W × H = area"). Below: a Parent + Side menu per block, Swap names, Turn block, Move leaf, "Guess D.y" box, and the numbers (tree text, walk, positions, box, wasted, legal, outline deadspace 57 labelled, made from, changes since, guess). After a failed Check, a "Check:" line says why. One column layout (the views need the width); phone 390 px has no sideways scroll.
- **Colours**: our fixed id → colour map (`COLORS` = the checker's), never `drawFloorplan`'s index colours; tested by pixel on a partial pack (only B and D) and after a swap.
- **Strings**: all learner text in `bstar-tree-strings.js` (`T`), one literal per line, unique; plus `index.html` (title, eyebrow, h1, lead, skip link) and the shared chrome of `clustering-ui.js` (already in Lab 03's `lab_strings.py`). The tests use element ids and the status class `pass`, so they run unchanged on the French copy.

### Challenges (all recomputed from the learner's tree on every Check)

Common gate: never from `base = reveal`; the tree must come from the challenge's Start tree (or from Clear where allowed); the tree must be valid and packed after the last change.

| Id | Level | Start | Passes when | Unique answers (checked in Node) |
|---|---|---|---|---|
| `build-golden` | Intro | empty | all five, no turn, tree = `A(B(C(E,-),-),D)` | 1 of 5040 |
| `d-at-3` | Intro | golden (or Clear) | legal, D.y = 3 | 372 trees |
| `predict-dy` | Practice | `order` | tree unchanged, guess saved before this tree was ever packed or revealed since Start, guess = D.y (4) | only 4 of 0-8 |
| `chain-turn` | Practice | `chain` | tree unchanged, exactly one turned block, legal | only {D} of 32 turn sets |
| `fix-swap` | Practice | `swap` (40) | no turn, tree = one swap of the start, legal, area ≤ 27 | only D,E of 10 |
| `move-leaf` | Practice | `swap` (40) | no turn, tree = one leaf move of the start, legal, area ≤ 28 | `D B right`, `D E left` (= checker ops n_best 2) |
| `reach-27` | Practice | `chain` (or Clear) | all five, legal, area ≤ 27 | 348 trees |
| `beat-27` | Stretch | golden (or Clear) | all five, legal, area < 27 (turns allowed) | 216 trees without turns (= checker legal_below[27]); 208 are 5x5, 8 are 6x4 |
| `reach-24` | Stretch | golden (or Clear) | all five, no turn, legal, area ≤ 24 | the 8 `best_trees`; 1480 (tree, turn set) pairs reach 24 with a turn, none passes |

Presets: Golden, A and C swapped (`lift`), Walk-order tree (`order`), Long row (`chain`), Bad tree (40) (`swap`), Clear tree. Reveal (study) loads and packs the running challenge's answer (golden when none) with `base = reveal`.

### Tests

- `test_model_vs_checker.py` (185 lines): all 5040 trees × 32 turn sets = 161,280 packs equal to `pack_bstar`; score, walk, 10 swaps, 50 `(leaf, parent, side)` moves incl. refusals, `leaf_moves`, `rotate` for all 32 sets; every `--json` scene (pack, box, wasted, legal, skyline, walk, outline deadspace) and its 4 relations; lab trees = `examples/*.json`; colours = checker COLORS; chain legal turn sets = checker (12); per challenge 15-16 model scenarios (positive, load, Pack only, Clear, Clear + Pack, Reveal, Reveal + Pack, Reveal + edits + Pack, wrong, edit after Pack (reason must be "stale"), swap twice after Pack, each of 5 presets + Pack; predict: guess after Pack, guess-edit-guess, guess after Reveal); the exhaustive answer counts of the table above. Mutation proof: letting a non-leaf move → 1 FAIL; letting edits keep the pack → 18 FAIL. Removing only the reveal gate is not caught, because the start-tree gate already rejects a revealed tree (two guards; the reveal one gives the clearer message).
- `test_lab_playwright.py` (110 cases): per challenge 1 positive done with the real menus and buttons (`reach-24` and `reach-27` through the Parent/Side menus, a slot shared by two blocks for a moment) and 9 negatives (Start + Check, Clear, Clear + Pack, Pack only, Reveal, Reveal + Pack, wrong answer, edit after Pack = turn B twice, the closest preset + Pack) + "guess after Pack"; 15 colour cases (5 tree nodes by attribute and pixel, 5 floor blocks by pixel, partial pack B and D keep their colours, after swap A,C the corner block is C amber, links solid/dashed, shared canvas hidden); page: 9 challenges, Check disabled before Start, 9/9 cleared, no console error or failed request.

### Deck

`assets/lab-starter.png` = the "Tree and floorplan" panel at 2x (1880x1156) after the `d-at-3` challenge passes (swap A,C: D at y = 3 on B, hole above C, 9 × 4 = 36). A first whole-page shot (1280x1080, as in Lab 03) was too small to read on the 16:9 slide. Slide 28 is now an image slide; rebuilt outline, pptx, PDF: 32 pages, verify scripts OK, lint 0 problems, 1198 words; page 28 looked at.

### For Stage 5

- `lab_strings.py` for this lab: `LAB = "tools/bstar-tree/"`; entries for `index.html` (lang, title, skip link, eyebrow, h1, lead), every literal of `bstar-tree-strings.js` (`STR = LAB + "bstar-tree-strings.js"`), and Lab 03's shared-chrome block for `assets/clustering-ui.js` (reusable as is). The panel headings "Graph" / "Reference / metrics" of the shared chrome are overwritten by `T.panelLeft/panelRight`, so they need no entry for this lab (but keep them if the shared block is copied whole).
- Run both tests on the French copy: `test_lab_playwright.py --url http://127.0.0.1:8090/fr/tools/bstar-tree/index.html` (ids and the `pass` class, no English words). `test_lab_site.py` of the template must be rewritten for this lab (its node clicks are Lab 03's).
- French lab screenshot: `capture_lab.py --url .../fr/... --out $SITE/i18n/fr/module02-03-bstar-tree/assets/lab-starter.png`.
- `build_site.py` copies the tool without `tests/` (as in Lab 03): check it also copies `bstar-tree-strings.js` and `bstar-tree-lab-model.js`.

### Teacher list (add to §8)

- `createChallengeLab` (shared) names the left panel "Graph" and the right "Reference / metrics" for every lab, floorplanning included; our tool overwrites both headings at render time.
- `floorplanning-lab.js` `createInteractiveFloorplanLab` (used by the old tool) is no longer used by `bstar-tree`; its "Reveal golden" and `ran`-flag pattern is the one-click problem of §4.

### Open questions

1. `predict-dy` asks about the walk-order tree (D.y = 4, held up by E), not the golden (D.y = 2, its parent's top): a guess of "parent's top" (3) fails, which is the point, but it is the hardest Practice item. Keep, or move it after `d-at-3` as Stretch?
2. `fix-swap` and `move-leaf` check the resulting tree (one swap / one leaf move away from the start), not the button used: rebuilding the golden by the menus also passes `fix-swap`. Fine for learning (same tree), or require the Swap button?

Status: Stage 4 finished. Next: Stage 5 (site repo EN + FR).

### Decisions on the Stage 4 open questions (2026-10-30)

1. **`predict-dy` stays in Practice.** Its hint now gives two hints in order, in one text (the shared chrome has one "Show hint" text, escaped, no line break): "1. Which blocks are placed before D? Count them in walk order. 2. E is placed before D, and part of E is under D." A wrong guess gives the Check line "Your guess is not where D lands. Look again at the blocks placed before D, then press Start and guess before you pack.": no number. The model's `guess-wrong` result no longer carries D.y either. CHECKLIST Track B no longer prints the answer ("…and got it right").
2. **Swap and move checks stay result-based** (the tree must be one swap / one leaf move from the Start tree, whatever buttons made it). Reworded: titles "Fix the bad tree. One swap is enough." and "One leaf move is enough: 40 → 28."; the prompts say "One swap of two names is enough…" and "One leaf move is enough: …"; CHECKLIST: "Fixed the bad tree (40): one swap is enough (27), and one leaf move is enough (28)".

Tests after the change: `test_model_vs_checker.py` 185 PASS; `test_lab_playwright.py` **111 ok** (new case: the wrong-guess Check line contains no digit; no other case reads these texts, the tests use ids). Slide 28's screenshot shows only the tree and floor panel, so it was not recaptured.

Walkthrough frames confirmed: `assets/steps/` holds exactly `01-root.png, 02-left-chain.png, 03-right-d.png, 04-legal.png, 05-takeaway.png` (git `M`), and `assets/STEPS.md` (CRLF), `transcript.md` and `slides.md` reference those five names; nothing references `01-next-door … 05-done` any more (only the §12 history above).

Status: Stage 4 finished and reviewed. Next: Stage 5 (site repo EN + FR).

---

## 15. Stage 5 — site repo EN + FR (2026-10-30, paused before the French media)

Site repo: `../eda-floorplanning-module-lab5` (fresh `git init -b main`, nothing committed, no `docs/` content yet, no `.cache/` copied). Made with `rsync` from `../eda-partitioning-module-lab3` (no `.git`, `docs`, `.cache`, `__pycache__`, old French module, `lab03-figures`), then every lab-specific place changed. The teacher clone was only read (plus `git status`: still only the two allowed folders).

### Changed places
`build_site.py` (docstring, `FR_MODULE`, `MODULE_REL`, `TOOL_REL`/`TOOL`/`STRINGS_JS`, **`PARTS = [(1,7),(8,12),(13,19),(20,24),(25,32)]`**, `copy_lab` destination, `other_lab` links, French strings module copy + shape check, lesson links, lessons kept across the rebuild) · `make_fr_media.py` (`FR_DIR`, `MODULE_REL`, `FOOTER = "learn_floorplanning — 03 arbre B*"`) · `site_src/player.js` (`lab05-speed`) · `site_src/index.html.tmpl` (tool hrefs) · `site_src/page.css` (`.lesson-link`, comment) · `i18n/strings.py` (EN + FR: title, crumb, lead, 5 part titles, lab text for the 9 challenges, 10 example files, footers, `lesson_link`, `parts_note_lessons`) · `.gitignore` (French media folder, `build/`) · `README.md` · `tools/test_site.py` · `tools/test_lab_site.py` (rewritten) · `tools/strings_shape.mjs` (new) · `tools/lab05-figures/` (snapshot of `../tools/lab05-figures`, without generated files). Removed from the copy: `WHAT_CHANGED.md` (Lab 03's; Stage 6 writes this lab's) and `ai-workflow/` (the Lab 03 story and copies of the skills: say if you want it in this repo too).

### French content (all in `i18n/fr/`)
- `module02-03-bstar-tree/transcript.md`: 31 slides, same image paths as the English one (checked by script), lint **0 problems**, 1,313 spoken words (French is wordier: about 8.8 min at 150 wpm). Title shortened to "Plan de masse par arbre B*" (the long one wrapped over the subtitle on slide 1). Spoken "arbre B-étoile". Terms as listed in the request; "valide" for legal, "placer" for pack.
- French deck checked offline in a scratch copy (teacher pipeline, nothing written to the repo): 32 pages, every page looked at; code slide = page 30 ("Parcours implémentation — à essayer").
- `module02-03-bstar-tree/assets/`: 19 French figures (`make_figures.py --lang fr`; label "cases perdues : n" instead of "perdu : n"), 5 French frames (`capture_fr_frames.py`, now also swaps the viewer's own "Step"/"Explanation" for "Étape"/"Explication"), French `lab-starter.png` (captured from a scratch build of the French lab, so slide 28 is right the first time). `real-shell.png` (program output, English) is copied by `make_fr_media.py`.
- `EXAMPLES.md`, `quiz.json` (same 8 answers, checked), `walkthrough-steps.json` (captions and titles equal the French slides 8-12, checked by script).
- Lab: `bstar-tree-strings.js` = full French copy; `build_site.py` replaces the English file with it in `docs/fr/tools/bstar-tree/` after `tools/strings_shape.mjs` confirmed the same keys, sub-keys and function arities (fails the build otherwise). `lab_strings.py` keeps only `index.html` (lang, title, skip link, eyebrow, h1, lead) and the shared chrome of `clustering-ui.js` (Lab 03's block, unchanged).

### Decisions
- `examples/wrong/` is **not** in the downloads list (the notes only say it ships in the module); `EXAMPLES.md` (both languages) still shows the two `--impl examples/wrong/...` commands, which run in the course repository as the implement text says. Test: `examples/wrong/` is not published.
- Downloads list (10): `tiny_modules.json`, `golden, lift, order, floor, swap, rotate, move, best .json`, `bstar_check.py`.
- Lessons prepared, none built: a lesson link under a part only when `docs/lessons/part-N/index.html` (or `docs/fr/lessons/...`) exists; `build_site.py` moves both `lessons` folders aside and back around its `rmtree` (a crashed run leaves them in `.cache/lessons-keep` and the next run restores them); the parts note adds a sentence only when a lesson exists. `test_site.py` checks every lesson page present (link and note, no console error, no external request, audio 200, link back to `#video`, `window.__lesson.errors` empty, `window.__lesson.floorplan.dataChecked` = number of scenes of `bstar_check.py --json`, 11). **Assumption to confirm in Stage 7:** the floorplan scene exposes `window.__lesson.floorplan.dataChecked`; the engine has no floorplan scene yet.
- The French lab screenshot comes from a scratch build of the French lab (`copy_lab` + `translate_lab` into a temp folder), not from `docs/fr`, to avoid running the French audio twice.

### Verified before the media run (scratch trial build of the site, FR deck without video)
- `build_site.py` runs end to end (EN stale-video warning as expected: the module still holds the old 13-slide English video, Stage 6 rebuilds it).
- `tools/test_lab_site.py` on that build: **en 116 ok, 0 FAIL; fr 116 ok, 0 FAIL** (9 positive, 82 negative, 15 colour, 10 page). A French word put back into English made the French line FAIL (mutation check).
- Lesson link and rebuild survival checked with fake lesson pages in the scratch copy.

### Waiting for the user
```bash
cd ~/Documents/3A/SJTU/VLSI_Mort/test2/eda-floorplanning-module-lab5
PYTHONDONTWRITEBYTECODE=1 ~/eda-venv/bin/python make_fr_media.py --repo ../eda-learning-lab5-fp
```
(VPN on, 10-30 min.) Then: `python3 build_site.py --repo ../eda-learning-lab5-fp`, serve `docs/` on 8090, run `tools/test_site.py` and `tools/test_lab_site.py`, read both language lines. English parts need the Stage 6 English media (`narrate_clips.sh`).

Teacher list (add to §8): the Lab 03 site template ships `ai-workflow/` and a lab-specific `WHAT_CHANGED.md` that every new site repo must delete.

- 2026-10-31: lesson-animator v4 installed. The lesson check in the site repo's `tools/test_site.py` now also requires `window.__lesson.floorplan.dataDiffer == 0` (engine and checker agree on every scene), next to `dataChecked == 11`. Syntax-checked only; it runs when a lesson page exists.

- 2026-10-31: both media runs done (EN and FR: 31 mp3, 32 timings, 32-page PDF). `~/eda-venv/bin/python build_site.py --repo ../eda-learning-lab5-fp` built docs/ (75.7 MB; parts EN 1:35 1:05 1:25 1:13 2:02, FR 1:35 1:04 1:28 1:15 2:09; the part-start frame check passed). Use the venv python: the system python has no `markdown`.
  Results: `tools/test_site.py` 185 checks, 0 failed (en 88 / fr 88 language rows); `tools/test_lab_site.py` EN 116 ok 0 FAIL, FR 116 ok 0 FAIL. Lesson checks skipped (no lesson pages yet). Playback of the H.264 parts and "next part starts by itself" still to be checked by the user in Firefox/Chrome, 1.5x, once per language.

---

## 16. Stage 6 — final check and hand-off (2026-11-02)

- Teacher clone: `git status` shows changes only in `courses/learn_floorplanning/module02-03-bstar-tree/` and `platform/tools/bstar-tree/`; no `__pycache__`; branch `main`, nothing committed. Module `video.mp4` = 1920x1080 H.264, 441.0 s; `audio/` = 31 slide mp3 + `full.mp3` + `slide_timings.json` (32 entries); `slides.pdf` = 32 pages (all of 2026-10-31 01:10-01:15, newer than `transcript.md`).
- Site `../eda-floorplanning-module-lab5`: `build_site.py --repo ../eda-learning-lab5-fp` (venv python) built `docs/` (88.9 MB; parts EN 1:35 1:05 1:25 1:13 2:02, FR 1:35 1:04 1:28 1:15 2:09); served on 127.0.0.1:8090 and stopped. `tools/test_site.py` 245 checks, 0 failed (en 118, fr 118, static 9; lessons 1-5 in both languages ok). `tools/test_lab_site.py` EN 116 ok 0 FAIL, FR 116 ok 0 FAIL.
- Teacher-side tests rerun: `bstar_check.py` 61 PASS; `--vs-node` PASS; wrong packers 25 PASS/4 FAIL and 24 PASS/5 FAIL; `ok_impl.py` 29 PASS; `test_model_vs_checker.py` 185 PASS; `test_lab_playwright.py` 111 ok.
- `WHAT_CHANGED.md` written in the site repo; its README section on lessons updated (lessons exist now).
- Correction to the teacher list: 99 tracked `.pyc` files are spread over the whole repository (23 in `.cursor/skills/module-slides/scripts`, 4 in `learn_floorplanning/common`, ...), not 99 under `common/__pycache__`.
- This file copied to `../tools/lab05-notes/UPGRADE_NOTES.md` and deleted from the module.
- Still for the user: play a video part (H.264) in Firefox/Chrome at 1.5x per language; commit and push the site repo; Pages on main `/docs`.
