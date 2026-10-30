#!/usr/bin/env python3
"""Put the Stage 3 B*-tree frames into a SCRATCH copy of the walkthrough viewer.

    python3 patch_walkthrough.py [--source <clone>/platform]

Copies <source> to ./wt-platform the first time (the teacher's viewer is never edited), then, in the copy only:
- replaces the "bstar-tree" block of tools/algorithm-walkthrough/floorplanning-algos.js with the 5 frames below
  (English), and adds a "bstar-tree-fr" block with the same frames in French (for capture_fr_frames.py);
- copies bstar-draw.js next to it and makes walkthrough.js draw a step that has `bstar` with drawBstarFrame
  (tree on the left, floorplan on the right, colour by block id, left link solid, right link dashed);
- adds a CSS override to index.html that restores the teacher's frame shape (940x456 for this lab).

Every position comes from facts.json (facts.py, from the module checker). The frame text is the spoken text
of transcript.md slides 8-12, so the deck, STEPS.md and the frames say the same thing.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
ap.add_argument("--source", type=Path, default=HERE.parents[1] / "eda-learning-lab5-fp/platform",
                help="a platform/ folder with tools/algorithm-walkthrough (default: ../../eda-learning-lab5-fp/platform)")
args = ap.parse_args()
WT_ROOT = HERE / "wt-platform"
if not WT_ROOT.is_dir():
    shutil.copytree(args.source, WT_ROOT, symlinks=True)
    print("copied", args.source, "->", WT_ROOT)
WT = WT_ROOT / "tools/algorithm-walkthrough"
for name in ("floorplanning-algos.js", "walkthrough.js", "index.html"):  # start each run from the teacher's files
    shutil.copy(args.source / "tools/algorithm-walkthrough" / name, WT / name)
F = json.loads((HERE / "facts.json").read_text())
SC = {s["id"]: s for s in F["scenes"]}
g = SC["golden"]
P = {st["id"]: st for st in g["steps"]}
assert g["walk"] == ["A", "B", "C", "E", "D"]
assert (P["B"]["x"], P["B"]["y"], P["C"]["x"], P["E"]["x"], P["D"]["x"], P["D"]["y"]) == (3, 0, 5, 7, 0, 2)
assert P["A"]["w"] + P["B"]["w"] + P["C"]["w"] == P["E"]["x"] == 7
assert all(st["x"] + st["w"] <= 10 and st["y"] + st["h"] <= 8 for st in g["steps"]) and g["legal"]


def hdim(x1, x2, y, text):
    return {"type": "hdim", "x1": x1, "x2": x2, "y": y, "text": text}


# The ids are the teacher's step ids in the shared floorplanning-algos.js (root, left-chain, right-d, legal,
# takeaway): the frame files keep the teacher's names 01-root.png ... 05-takeaway.png, with the new pictures.
# frame = (id, k blocks placed, highlighted nodes, floor annotations, text per language)
FRAMES = [
    ("root", 2, ["B"], [hdim(0, P["A"]["w"], -0.5, str(P["A"]["w"]))], {
        "en": dict(title="B goes next door, at x = 3",
                   caption="B goes next door, at x equals three: A starts at zero, and A is three wide. "
                           "Nothing is under B, so it rests on the floor, at y equals zero.",
                   bullets=["Next door to A", "x = 0 + 3 = 3", "On the floor: y = 0"],
                   metrics=["B at x = 3, y = 0"]),
        "fr": dict(title="B va à côté, en x = 3",
                   caption="B va à côté, en x égal trois : A commence à zéro, et A fait trois de large. "
                           "Rien n'est sous B, donc il repose sur le sol, en y égal zéro.",
                   bullets=["À côté de A", "x = 0 + 3 = 3", "Sur le sol : y = 0"],
                   metrics=["B en x = 3, y = 0"]),
    }),
    ("left-chain", 2, ["B", "C", "E"], [], {
        "en": dict(title="The walk: A, B, C, E, then D",
                   caption="We place the blocks one at a time, in a fixed walk order. Place a node, then everything "
                           "down its left side, and only then its right child. So the walk goes A, B, C and E, "
                           "and D comes last.",
                   bullets=["Place a node", "then everything down its left side", "only then its right child"],
                   metrics=["walk: A, B, C, E, D"]),
        "fr": dict(title="Le parcours : A, B, C, E, puis D",
                   caption="On place les blocs un par un, dans un ordre de parcours fixe. On place un nœud, puis "
                           "tout son côté gauche, et seulement ensuite son enfant droit. Le parcours donne donc "
                           "A, B, C et E, et D vient en dernier.",
                   bullets=["On place un nœud", "puis tout son côté gauche", "seulement ensuite son enfant droit"],
                   metrics=["parcours : A, B, C, E, D"]),
    }),
    ("right-d", 4, ["C", "E"], [hdim(0, P["E"]["x"], -0.5, "3 + 2 + 2 = 7")], {
        "en": dict(title="C and E go next door",
                   caption="C is B's left child, so it goes next door to B, at x equals five. E is C's left child, "
                           "so it lands next door to C, at x equals seven. The widths simply add up: three, plus "
                           "two, plus two, makes seven.",
                   bullets=["C at x = 5", "E at x = 7", "3 + 2 + 2 = 7"],
                   metrics=["C at x = 5", "E at x = 7"]),
        "fr": dict(title="C et E vont à côté",
                   caption="C est l'enfant gauche de B, donc il va à côté de B, en x égal cinq. E est l'enfant "
                           "gauche de C, donc il arrive à côté de C, en x égal sept. Les largeurs s'additionnent : "
                           "trois, plus deux, plus deux, font sept.",
                   bullets=["C en x = 5", "E en x = 7", "3 + 2 + 2 = 7"],
                   metrics=["C en x = 5", "E en x = 7"]),
    }),
    ("legal", 5, ["D"], [], {
        "en": dict(title="D goes upstairs, on A",
                   caption="The left side is done, so the walk comes back to D, A's right child. D goes upstairs, "
                           "so it starts at x equals zero, like A. It sits on top of A, at y equals two.",
                   bullets=["D: A's right child", "Upstairs: x = 0", "On top of A: y = 2"],
                   metrics=["D at x = 0, y = 2"]),
        "fr": dict(title="D monte à l'étage, sur A",
                   caption="Le côté gauche est fini, donc le parcours revient à D, l'enfant droit de A. D monte à "
                           "l'étage, donc il commence en x égal zéro, comme A. Il se pose sur A, en y égal deux.",
                   bullets=["D : enfant droit de A", "À l'étage : x = 0", "Sur A : y = 2"],
                   metrics=["D en x = 0, y = 2"]),
    }),
    ("takeaway", 5, [], [], {
        "en": dict(title="Five blocks placed",
                   caption="All five blocks are placed, and every one is inside the outline. Pause and guess: "
                           "if we swap A and C in the tree, does D still land at y equals two?",
                   bullets=["All five inside the outline", "Swap A and C:", "is D still at y = 2?"],
                   metrics=["all 5 placed"]),
        "fr": dict(title="Cinq blocs placés",
                   caption="Les cinq blocs sont placés, et chacun est dans le contour. Faites une pause et devinez : "
                           "si on échange A et C dans l'arbre, D arrive-t-il encore en y égal deux ?",
                   bullets=["Les cinq dans le contour", "On échange A et C :", "D est-il encore en y = 2 ?"],
                   metrics=["5 sur 5 placés"]),
    }),
]


def steps(lang: str) -> list[dict]:
    out = []
    for sid, k, hi, ann, text in FRAMES:
        t = text[lang]
        out.append({
            "id": sid, "title": t["title"], "caption": t["caption"], "bullets": t["bullets"], "metrics": t["metrics"],
            "bstar": {
                "scene": g, "colors": F["colors"], "px": 13,
                "tree": {"placed": g["walk"][:k], "highlight": hi},
                "floor": {"k": k, "extentW": 10.4, "annotations": ann,
                          "margins": {"l": 30, "r": 6, "t": 12, "b": 38}},
            },
        })
    return out


def block(key: str, title: str, lang: str) -> str:
    return (f'  "{key}": {{\n    title: "{title}",\n    module: "module02-03-bstar-tree",\n    kind: "floorplan",\n'
            f'    steps: {json.dumps(steps(lang), ensure_ascii=False)},\n  }},\n\n')


algos = WT / "floorplanning-algos.js"
src = algos.read_text(encoding="utf-8")
new, n = re.subn(r'  "bstar-tree": \{.*?(?=  "sequence-pair": \{)',
                 lambda _: block("bstar-tree", "B*-tree", "en") + block("bstar-tree-fr", "Arbre B*", "fr"),
                 src, count=1, flags=re.S)
assert n == 1
algos.write_text(new, encoding="utf-8")
shutil.copy(HERE / "bstar-draw.js", WT / "bstar-draw.js")
(HERE / "steps.json").write_text(json.dumps({lang: steps(lang) for lang in ("en", "fr")}, ensure_ascii=False, indent=1))
print("patched", algos)

wt = WT / "walkthrough.js"
js = 'import { drawBstarFrame } from "./bstar-draw.js";\n' + wt.read_text(encoding="utf-8")
old = '  if (pack.kind === "floorplan" || s.pack != null) {'
assert js.count(old) == 1
js = js.replace(old, '  if (s.bstar) {\n    drawBstarFrame(canvas, s);\n  } else ' + old.lstrip(), 1)
wt.write_text(js, encoding="utf-8")
print("patched", wt)

html_p = WT / "index.html"
css = ("  <style>/* scratch only: teacher's original frame shape for slides */ "
       ".walk-body{min-height:0} .walk-canvas-wrap canvas{height:320px;max-height:320px}</style>\n</head>")
html_p.write_text(html_p.read_text(encoding="utf-8").replace("</head>", css, 1), encoding="utf-8")
print("patched", html_p)
