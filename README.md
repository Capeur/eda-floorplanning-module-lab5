# Lab 05 — B*-tree floorplan · Floorplanning for EDA

A standalone, **bilingual (English / French)** GitHub Pages site for **Lab 05 (B*-tree floorplan representation)** of the
[Floorplanning for EDA course](https://github.com/yongfu-li/eda-learning) — a review build of the
upgraded lab, not yet merged into the course repository.

- English: `https://capeur.github.io/eda-floorplanning-module-lab5/`
- Français : `https://capeur.github.io/eda-floorplanning-module-lab5/fr/`

Each language has the narrated video in five parts with subtitles and a speed control, every slide as an image, the
five-frame walkthrough with its captions, PDF/PowerPoint downloads, the **interactive browser lab** (9 challenges that check
the tree you built), the Track A material, a quiz and the full transcript. A switch in every header (page and lab) jumps to
the other language at the same place.

Built from the Lab 03 template (`eda-partitioning-module-lab3`) with a fresh history.

## Layout

| Path | What |
|------|------|
| `build_site.py` | builds `docs/` (English) and `docs/fr/` (French); `PARTS` = PDF pages of the five video parts |
| `make_fr_media.py` | builds the French slides, narration and video with the course's own tools |
| `site_src/` | page template, CSS, quiz script, player script (speed key `lab05-speed`), self-hosted fonts |
| `i18n/strings.py` | all page text, English and French (part titles, lesson link text, example files list) |
| `i18n/fr/module02-03-bstar-tree/` | French narration (`transcript.md`), French figures and walkthrough frames, French deck |
| `i18n/fr/EXAMPLES.md`, `i18n/fr/quiz.json` | French Track A guide and quiz |
| `i18n/fr/walkthrough-steps.json` | French captions of the five walkthrough frames (the English ones are the course's `assets/STEPS.md`) |
| `i18n/fr/bstar-tree-strings.js` | French copy of the lab's strings module; the build checks it has exactly the same keys and functions (`tools/strings_shape.mjs`) |
| `i18n/fr/lab_strings.py` | French text of the lab page and of the shared challenge chrome (exact replacements; the build fails if they changed) |
| `tools/lab05-figures/` | the scripts that draw the figures, the walkthrough frames and the lab screenshot, English and French |
| `tools/test_site.py`, `tools/test_lab_site.py` | Playwright tests of the built site and of the lab's 9 challenges, in both languages |
| `docs/` | the built site served by GitHub Pages (main branch, `/docs`) |

English content comes from your `eda-learning` clone (Lab 05 upgrade applied); nothing in it is modified. The lab is
copied file by file (`platform/tools/bstar-tree/`, **without** its `tests/` folder) plus the shared
`platform/assets/` files it imports. `examples/wrong/` (the two deliberately wrong packers) stays in the course repository: the
page offers the checker, the blocks and the eight example trees, not the wrong packers.

## Rebuild

```bash
# English narration + video, in the course clone (needs internet)
cd ~/path/to/eda-learning-lab5-fp
bash .cursor/skills/module-slides/scripts/narrate_clips.sh \
  courses/learn_floorplanning/module02-03-bstar-tree

# French slides + narration + video, here (needs internet, LibreOffice, ffmpeg)
cd ~/path/to/eda-floorplanning-module-lab5
python3 make_fr_media.py --repo ../eda-learning-lab5-fp

# both sites
python3 build_site.py --repo ../eda-learning-lab5-fp
git add -A && git commit -m "Rebuild site" && git push
```

If an English `video.mp4` is older than the deck, `build_site.py` warns; if its audio timings do not match the number of
slides, it embeds the video without subtitles and warns that it is stale.

Preview: `python3 -m http.server 8090 --directory docs` → `http://127.0.0.1:8090/` and `/fr/`.

## Tests

```bash
python3 -m http.server 8090 --directory docs &
python3 tools/test_site.py          # page, walkthrough captions, five video parts, speed, quiz, switch, 0 external requests, any lesson page
python3 tools/test_lab_site.py      # the 9 challenges + colours: positive and negative cases, EN and FR
```

## Animated lessons (prepared, none built yet)

The `lesson-animator` skill builds one lesson page per video part into `docs/lessons/part-N/` (English) and
`docs/fr/lessons/part-N/` (French). `build_site.py` does not build them, but it keeps them across a rebuild (they are moved
aside and back) and adds an "Interactive lesson" / "Leçon interactive" link under a video part **only when that part's page
exists**; the parts note then also says so. `tools/test_site.py` checks every lesson page that is present: its link and
the note, no console error, no external request, audio answers 200, a link back to `#video`, `window.__lesson.errors` empty
and `window.__lesson.floorplan.dataChecked` equal to the number of scenes in `bstar_check.py --json`. With no lessons,
those checks only confirm that no link is shown. Commit `lessons/*/storyboard.json`, `docs/lessons` and `docs/fr/lessons`;
`build/` and `.cache/` stay ignored.

## French images

The French frames, figures and lab screenshot are made by `tools/lab05-figures/` (see its README), a snapshot
of `~/Documents/3A/SJTU/VLSI_Mort/test2/tools/lab05-figures/`:

```bash
# serve the scratch walkthrough viewer (8081, after patch_walkthrough.py); the lab screenshot comes from a served
# docs/ (8090) or from a scratch build of the French lab
python3 tools/lab05-figures/make_figures.py --module ../eda-learning-lab5-fp/courses/learn_floorplanning/module02-03-bstar-tree \
    --lang fr --out i18n/fr/module02-03-bstar-tree/assets
python3 tools/lab05-figures/capture_fr_frames.py --out i18n/fr/module02-03-bstar-tree/assets/steps
python3 tools/lab05-figures/capture_lab.py --url http://127.0.0.1:8090/fr/tools/bstar-tree/index.html \
    --out i18n/fr/module02-03-bstar-tree/assets/lab-starter.png
```

Rebuild the French deck (`make_fr_media.py`) and the site afterwards.

**Terminology (French):** *plan de masse* (floorplan), *bloc*, *contour* (outline), *arbre B\**, *enfant gauche / droit*,
*à côté* (next door), *à l'étage* (upstairs), *ligne d'horizon* (skyline), *boîte englobante* (bounding box), *cases perdues*
(wasted squares), *tourner*, *échanger*, *déplacer une feuille*, *ordre de parcours*, *valide* (legal), *placer* (pack).
*quiz* stays in English. Code, commands and program output stay in English.

## Credits

Course content, browser lab framework and media pipeline: the
[EDA Algorithms Platform](https://github.com/yongfu-li/eda-learning) (CC BY 4.0).
Lab 05 upgrade and French translation built for the course assignment.
