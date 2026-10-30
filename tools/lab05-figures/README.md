# Lab 05 figures (floorplanning, B*-tree)

> Snapshot for the site repo of `~/Documents/3A/SJTU/VLSI_Mort/test2/tools/lab05-figures/` (the source of truth). `facts.json`, `steps.json` and `wt-platform/` are generated and not copied: run `facts.py` and `patch_walkthrough.py` first (they need the teacher clone `../eda-learning-lab5-fp`).


Scripts that draw the Stage 3 pictures of
`eda-learning-lab5-fp/courses/learn_floorplanning/module02-03-bstar-tree/assets/`.
They live outside the teacher clone on purpose; this folder is the source of truth (Stage 5 may copy it into the
site repo).

## Run everything

```bash
bash run_all.sh                      # teacher clone defaults to ../../eda-learning-lab5-fp
bash run_all.sh /path/to/clone       # or pass it
```

Needs: Python 3 with Playwright + Chromium, `curl`, the teacher clone (its `platform/` has the walkthrough
viewer). Port 8081 must be free. `PYTHONDONTWRITEBYTECODE=1` is set inside, so no `__pycache__` lands in the clone.

It writes only into the module's `assets/`: the 5 walkthrough frames in `steps/` + `STEPS.md` (CRLF), the 19
figures, and `real-shell.png` + `real-shell.txt`. Then rebuild the deck with the teacher's pipeline (commands in
the module's `UPGRADE_NOTES.md`, Stage 3).

## The files

| File | What it does |
|---|---|
| `facts.py <module>` | Runs `examples/bstar_check.py --json` and saves its whole output to `facts.json`, after checking every number the transcript speaks (positions, boxes, areas, wasted squares, 5040 trees). If the checker changes, this stops before a wrong picture is drawn. |
| `bstar-draw.js` | The one drawing code (canvas 2D) for the figures **and** the walkthrough frames: `drawTree`, `drawFloor`, `drawBstarFrame`. |
| `make_figures.py --module <module> [--lang fr] [--out DIR] [--only name.png]` | Draws the 19 figures (680x820 CSS px, saved 2x: tree on top, 10x8 outline below). No server: the drawing code is inlined into the page. `--lang fr` swaps the labels (`TEXT["fr"]`); numbers still come from `facts.json`. |
| `patch_walkthrough.py [--source <clone>/platform]` | Copies the platform to `wt-platform/` (first run), then in the copy only: replaces the `bstar-tree` block of `floorplanning-algos.js` with the 5 new frames (EN) and adds a `bstar-tree-fr` block (FR); copies `bstar-draw.js` next to it and makes `walkthrough.js` call `drawBstarFrame` for those steps; adds the CSS override that gives the teacher's frame shape (940x468). The three viewer files are copied fresh from the clone on every run, so reruns are safe. The teacher's viewer is never edited. |
| `capture_fr_frames.py --out DIR` | French frames (`?algo=bstar-tree-fr`), same names and size as the English ones. Serve `wt-platform/` on 8081 first. |
| `run_all.sh` | All of the above for English, plus the teacher's `capture_algorithm_walkthrough.py` and `capture_real_shell.py` with the options that were used. |

Generated here (safe to delete): `facts.json`, `steps.json` (the frame texts, EN and FR), `wt-platform/`.

## Drawing rules (decided in Stage 1, §10 of the notes)

- Colour by **block id**, never by index: A `#1d4ed8` blue, B `#0f6b5c`, C `#b45309`, D `#7c3aed`, E `#be123c`
  (`PAPER_PALETTE` order of `floorplanning-core.js`; read from `facts.json` → `colors`).
- Tree: left child to the lower left with a **solid** link ("next door"), right child to the lower right with a
  **dashed** link ("upstairs"). A node not placed yet is white with a ring in its colour; a placed node is filled;
  a highlighted node has a yellow halo and a black ring; a turned block has a ↻ badge.
- Floorplan: origin at the lower-left corner of the 10x8 outline, y going up; the panel always shows x from 0 to
  12.4 so the 12-wide row fits and nothing jumps between step figures. Skyline = thick yellow line with a dark edge;
  bounding box = dashed black rectangle; wasted squares = grey hatching; a hole under a lifted block = red hatching;
  a block outside the outline gets a red border; a dropping block is a faded ghost with a dashed arrow.
- Only numbers that the slide says aloud are written on a figure (block sizes are read from the squared paper).

## Change one picture

- Frame text: edit `FRAMES` in `patch_walkthrough.py` (EN and FR), then `run_all.sh`. Keep the caption equal to
  the slide's spoken text in `transcript.md` (slides 8-12).
- One figure: `python3 make_figures.py --module <module> --only best.png`, then rebuild the deck.

## French (Stage 5)

Output goes to the site repo, never to the teacher clone.

```bash
SITE=../eda-floorplanning-module-lab5; M=../eda-learning-lab5-fp/courses/learn_floorplanning/module02-03-bstar-tree
python3 make_figures.py --module $M --lang fr --out $SITE/i18n/fr/module02-03-bstar-tree/assets
python3 -m http.server 8081 --bind 127.0.0.1 --directory wt-platform &    # after patch_walkthrough.py
python3 capture_fr_frames.py --out $SITE/i18n/fr/module02-03-bstar-tree/assets/steps
```

The French labels and frame texts are a first draft written in Stage 3 (terms: arbre B*, racine, enfant
gauche/droit, à côté, à l'étage, ligne d'horizon, boîte englobante, perdu); Stage 5 reviews them with the French
transcript.

## Browser-lab screenshot (Stage 4, slide 28)

`capture_lab.py` runs the real lab (challenge "Lift D to y = 3": swap A and C, Pack, Check, must PASS) and saves
the "Tree and floorplan" panel at 2x as `assets/lab-starter.png`. It needs a server, so it is not in `run_all.sh`.

```bash
python3 -m http.server 8080 --directory ../eda-learning-lab5-fp/platform &
python3 capture_lab.py --module ../eda-learning-lab5-fp/courses/learn_floorplanning/module02-03-bstar-tree
# French (Stage 5), from the built site:
python3 -m http.server 8090 --directory $SITE/docs &
python3 capture_lab.py --url http://127.0.0.1:8090/fr/tools/bstar-tree/index.html --out $SITE/i18n/fr/module02-03-bstar-tree/assets/lab-starter.png
```
