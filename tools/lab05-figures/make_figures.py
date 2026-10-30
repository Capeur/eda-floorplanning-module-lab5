#!/usr/bin/env python3
"""Draw the explanation figures of the floorplanning Lab 05 (B*-tree) slides, in English or French.

Each figure is tall (680 x 820 CSS px, saved at 2x): the B*-tree on top, the 10 x 8 outline below.
Step figures are the same picture with fewer blocks placed (same size, so the slide does not jump).

    blocks-1, blocks          the five blocks on squared paper; then the empty outline, 10 by 8   [2, 3]
    tree-golden               the golden tree: root, left child, right child                      [4]
    rule-1, rule              A in the corner with x and y; then "next door" and "upstairs"       [5, 6]
    pause-b                   A is 3 wide and 2 tall; where does B go?                            [7]
    lift-1, lift-2, lift      A and C swapped: four blocks; the skyline and D dropping; D on B    [13-15]
    golden-box-1, golden-box  bounding box 9 x 3 = 27; then the 4 wasted squares                  [16, 17]
    lift-box                  the swapped tree: 9 x 4 = 36, 13 wasted                             [18]
    chain-1, chain-2, chain   every child a left child: empty; 3+2+2+3 = 10; E sticks out, 12      [19-21]
    chain-check               no overlap, but it sticks out                                       [22]
    turn                      D turned: the row is 10 wide, legal                                 [23]
    best-1, best              a best tree before B; B lifted onto D, 6 x 4 = 24, 1 wasted          [25, 26]

(slide numbers of transcript.md in brackets). Every position, box and count comes from facts.json
(facts.py, from the module checker); the drawing code is bstar-draw.js, shared with the walkthrough
frames. Colour by block id (A blue, then B, C, D, E in the paper palette), left link solid, right
link dashed, y up from the lower-left corner.

    python3 make_figures.py --module <module dir>                       # English, into <module>/assets
    python3 make_figures.py --module <module dir> --lang fr --out DIR   # French labels, into DIR
    python3 make_figures.py --module <module dir> --only best.png       # one figure
Needs Playwright + Chromium; no server (the drawing code is inlined into the page).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
F = json.loads((HERE / "facts.json").read_text())
SC = {s["id"]: s for s in F["scenes"]}
COLORS = F["colors"]
W, H, TREE_H = 680, 820, 300
PX = 26

TEXT = {
    "en": {
        "root": "root", "left_child": "left child", "right_child": "right child",
        "next_door": "next door", "upstairs": "upstairs", "skyline": "skyline", "hole": "hole",
        "blocks": "blocks: {n}", "wasted": "wasted: {n}", "sticks_out": "sticks out by {n}",
        "not_legal": "not legal", "legal": "legal", "no_overlap": "no overlap ✓",
        "sticking_out": "sticks out ✗",
    },
    "fr": {
        "root": "racine", "left_child": "enfant gauche", "right_child": "enfant droit",
        "next_door": "à côté", "upstairs": "à l'étage", "skyline": "ligne d'horizon",
        "hole": "trou", "blocks": "blocs : {n}", "wasted": "cases perdues : {n}", "sticks_out": "dépasse de {n}",
        "not_legal": "non valide", "legal": "valide", "no_overlap": "aucun chevauchement ✓",
        "sticking_out": "dépasse ✗",
    },
}


def step(scene: str, block: str) -> dict:
    return next(s for s in SC[scene]["steps"] if s["id"] == block)


def walk(scene: str, k: int) -> list[str]:
    return SC[scene]["walk"][:k]


def build(lang: str) -> dict[str, dict]:
    T = TEXT[lang]
    g, lift, chain, turn, best = (SC[i] for i in ("golden", "lift", "rotate_start", "rotate_after", "best"))
    times = "×"

    def box(sc):
        return f"{sc['bbox'][0]} {times} {sc['bbox'][1]} = {sc['area']}"

    used = sum(m["w"] * m["h"] for m in F["modules"])
    dim = lambda a, b, y, t, **kw: {"type": "hdim", "x1": a, "x2": b, "y": y, "text": t, **kw}  # noqa: E731
    vdim = lambda a, b, x, t: {"type": "vdim", "y1": a, "y2": b, "x": x, "text": t}  # noqa: E731
    text = lambda x, y, t, **kw: {"type": "text", "x": x, "y": y, "text": t, **kw}  # noqa: E731

    # the tray: the five blocks laid out on squared paper, two rows, centred over the outline
    mods = {m["id"]: m for m in F["modules"]}
    tray, gap = [], 0.8
    for row, y0 in ((["A", "B", "C"], 2.6), (["D", "E"], 0.0)):
        x = (F["outline"]["w"] - (sum(mods[i]["w"] for i in row) + gap * (len(row) - 1))) / 2
        for i in row:
            tray.append({"id": i, "x": x, "y": y0, "w": mods[i]["w"], "h": mods[i]["h"]})
            x += mods[i]["w"] + gap

    a, b_, d5 = step("golden", "A"), step("golden", "B"), step("lift", "D")
    assert (b_["x"], a["w"], a["h"]) == (3, 3, 2)
    c4 = chain["steps"][3]
    widths4 = " + ".join(str(s["w"]) for s in chain["steps"][:4]) + f" = {c4['x'] + c4['w']}"
    e5 = chain["steps"][4]
    over = e5["x"] + e5["w"] - F["outline"]["w"]
    bB = step("best", "B")

    figs: dict[str, dict] = {
        "blocks-1.png": {"scene": "golden", "tray": tray, "floor": {"k": 0, "outline": False}},
        "blocks.png": {"scene": "golden", "tray": tray, "floor": {"k": 0, "annotations": [
            dim(0, F["outline"]["w"], -0.6, str(F["outline"]["w"])),
            vdim(0, F["outline"]["h"], -0.6, str(F["outline"]["h"]))]}},
        "tree-golden.png": {"scene": "golden", "tree": {"placed": [], "rootLabel": T["root"], "linkLabelFrom": "A",
                                                       "linkLabels": {"left": T["left_child"], "right": T["right_child"]}},
                            "floor": {"k": 0}},
        "rule-1.png": {"scene": "golden", "tree": {"placed": ["A"], "highlight": ["A"], "rootLabel": T["root"]},
                       "floor": {"k": 1, "annotations": [
                           {"type": "arrow", "x1": 0, "y1": -0.75, "x2": 4, "y2": -0.75, "text": "x", "tx": 4.5, "ty": -0.75},
                           {"type": "arrow", "x1": -0.75, "y1": 0, "x2": -0.75, "y2": 4, "text": "y", "tx": -0.75, "ty": 4.6}]}},
        "rule.png": {"scene": "golden", "tree": {"placed": ["A"], "linkLabelFrom": "A",
                                                 "linkLabels": {"left": T["next_door"], "right": T["upstairs"]}},
                     "floor": {"k": 1, "annotations": [
                         {"type": "arrow", "x1": a["w"] + 0.15, "y1": 1, "x2": a["w"] + 2.4, "y2": 1,
                          "text": T["next_door"], "tx": a["w"] + 0.2, "ty": 1.7, "align": "left"},
                         {"type": "arrow", "x1": 0.6, "y1": a["h"] + 0.15, "x2": 0.6, "y2": a["h"] + 2.3,
                          "dashed": True, "text": T["upstairs"], "tx": 0.95, "ty": a["h"] + 1.3, "align": "left"}]}},
        "pause-b.png": {"scene": "golden", "tree": {"placed": ["A"], "highlight": ["B"], "marks": {"B": "?"}},
                        "floor": {"k": 1, "annotations": [
                            dim(0, a["w"], -0.6, str(a["w"])), vdim(0, a["h"], -0.6, str(a["h"])),
                            text(a["w"] + 1, 1, "?", size=2.2)]}},
        "lift-1.png": {"scene": "lift", "tree": {"placed": walk("lift", 4)}, "floor": {"k": 4}},
        "lift-2.png": {"scene": "lift", "tree": {"placed": walk("lift", 4), "highlight": ["D"]},
                       "floor": {"k": 4, "skyline": True, "falling": True,
                                 "skylineLabel": {"text": T["skyline"], "x": 6.5, "y": 2.75}}},
        "lift.png": {"scene": "lift", "tree": {"placed": walk("lift", 5)},
                     "floor": {"hole": True, "annotations": [
                         text(d5["x"] + d5["w"] + 1.4, d5["y"] + 0.5, f"y = {d5['y']}"),
                         text(1, 2.5, T["hole"], color="#b91c1c", size=0.9)]}},
        "golden-box-1.png": {"scene": "golden", "tree": {"placed": walk("golden", 5)}, "floor": {"bbox": {"text": box(g)}}},
        "golden-box.png": {"scene": "golden", "tree": {"placed": walk("golden", 5)},
                           "floor": {"bbox": {"text": box(g)}, "wasted": True, "annotations": [
                               text(0.3, 6.4, T["blocks"].format(n=used), align="left"),
                               text(0.3, 5.4, T["wasted"].format(n=g["wasted"]), align="left", color="#475569")]}},
        "lift-box.png": {"scene": "lift", "tree": {"placed": walk("lift", 5)},
                         "floor": {"bbox": {"text": box(lift)}, "wasted": True, "annotations": [
                             text(0.3, 6.4, f"{g['area']} → {lift['area']}", align="left"),
                             text(0.3, 5.4, T["wasted"].format(n=lift["wasted"]), align="left", color="#475569")]}},
        "chain-1.png": {"scene": "rotate_start", "tree": {"placed": []}, "floor": {"k": 0}},
        "chain-2.png": {"scene": "rotate_start", "tree": {"placed": walk("rotate_start", 4), "highlight": ["E"]},
                        "floor": {"k": 4, "annotations": [dim(0, c4["x"] + c4["w"], -0.6, widths4)]}},
        "chain.png": {"scene": "rotate_start", "tree": {"placed": walk("rotate_start", 5)},
                      "floor": {"annotations": [
                          dim(0, chain["bbox"][0], -0.6, str(chain["bbox"][0])),
                          text(12.3, 3.9, T["sticks_out"].format(n=over), color="#b91c1c", align="right"),
                          text(12.3, 3.0, T["not_legal"], color="#b91c1c", align="right")]}},
        "chain-check.png": {"scene": "rotate_start", "tree": {"placed": walk("rotate_start", 5)},
                            "floor": {"skyline": True, "annotations": [
                                text(0.3, 6.4, T["no_overlap"], color="#15803d", align="left"),
                                text(0.3, 5.4, T["sticking_out"], color="#b91c1c", align="left")]}},
        "turn.png": {"scene": "rotate_after", "tree": {"placed": walk("rotate_after", 5), "rotated": turn["rotated"]},
                     "floor": {"annotations": [dim(0, turn["bbox"][0], -0.6, str(turn["bbox"][0])),
                                               text(0.3, 5.4, T["legal"], color="#15803d", align="left")]}},
        "best-1.png": {"scene": "best", "tree": {"placed": walk("best", 4), "highlight": ["B"]},
                       "floor": {"k": 4, "skyline": True, "falling": True}},
        "best.png": {"scene": "best", "tree": {"placed": walk("best", 5)},
                     "floor": {"bbox": {"text": box(best)}, "wasted": True, "annotations": [
                         text(bB["x"] + bB["w"] + 0.3, bB["y"] + 0.5, f"y = {bB['y']}", align="left"),
                         text(0.3, 6.4, T["wasted"].format(n=best["wasted"]), align="left", color="#475569")]}},
    }
    assert lift["wasted"] == 13 and over == 2 and widths4 == "3 + 2 + 2 + 3 = 10"
    return figs


PAGE = """<!doctype html><html><head><meta charset="utf-8">
<style>body{margin:0;background:#fff} canvas{display:block}</style></head><body>
<canvas id="c" width="%(W)d" height="%(H)d" style="width:%(W)dpx;height:%(H)dpx"></canvas>
<script type="module">
%(DRAW)s
window.render = (spec) => {
  const cv = document.getElementById("c");
  const dpr = window.devicePixelRatio || 1;
  cv.width = %(W)d * dpr; cv.height = %(H)d * dpr;
  const ctx = cv.getContext("2d");
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.fillStyle = "#ffffff"; ctx.fillRect(0, 0, %(W)d, %(H)d);
  const top = { x: 0, y: 0, w: %(W)d, h: %(TREE_H)d };
  const bottom = { x: 0, y: %(TREE_H)d, w: %(W)d, h: %(H)d - %(TREE_H)d };
  const px = spec.px, colors = spec.colors, extentW = 12.4;
  const margins = { l: px * 3.2, r: px * 0.6, t: px * 1.6, b: px * 3.0 };
  const fl = drawFloor(ctx, bottom, spec.scene, { ...spec.floor, colors, px, extentW, margins });
  if (spec.tree) drawTree(ctx, { x: 50, y: 4, w: %(W)d - 100, h: %(TREE_H)d - 8 }, spec.scene, { ...spec.tree, colors, px });
  if (spec.tray) {
    const empty = { outline: spec.scene.outline, steps: [], rotated: [] };
    drawFloor(ctx, { ...top, h: top.h + 6 }, empty, { outline: false, tray: spec.tray, colors, px, extentW,
      scale: fl.s, margins: { ...margins, t: 4, b: 0 } });
  }
  window.done = true;
};
window.ready = true;
</script></body></html>"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--module", type=Path, required=True)
    ap.add_argument("--lang", choices=sorted(TEXT), default="en")
    ap.add_argument("--out", type=Path, help="output folder (default: <module>/assets)")
    ap.add_argument("--only", help="one figure name, e.g. best.png")
    args = ap.parse_args()
    out = args.out or args.module / "assets"
    out.mkdir(parents=True, exist_ok=True)
    figs = build(args.lang)
    if args.only:
        figs = {args.only: figs[args.only]}
    draw = (HERE / "bstar-draw.js").read_text(encoding="utf-8")
    html = PAGE % {"W": W, "H": H, "TREE_H": TREE_H, "DRAW": draw}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        page.set_content(html)
        page.wait_for_function("window.ready === true")
        for name, spec in figs.items():
            full = {**spec, "scene": SC[spec["scene"]], "colors": COLORS, "px": PX}
            page.evaluate("window.done = false")
            page.evaluate("spec => window.render(spec)", full)
            page.wait_for_function("window.done === true")
            page.locator("#c").screenshot(path=str(out / name))
            print("wrote", out / name)
        browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
