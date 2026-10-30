#!/usr/bin/env python3
"""Golden self-check for module02-03 B*-tree floorplan representation (Track A).

    python3 examples/bstar_check.py                    # check the reference
    python3 examples/bstar_check.py --show             # also print every pack, step by step
    python3 examples/bstar_check.py --impl my_bstar.py # check YOUR functions
    python3 examples/bstar_check.py --vs-node          # compare with packBstar in the browser lab's JS
    python3 examples/bstar_check.py --json > bstar.json  # trees, packs, contours: for figures and lessons

A tree is a nested dict like the course helpers use: {"id": "A", "left": {...}, "right": {...}}; a missing
child is a missing key. The short text form is `id(left,right)` with `-` for an empty child and a bare id for
a leaf: `A(B(C(E,-),-),D)`. `modules` is a list of {"id", "w", "h"}; `outline` is {"w", "h"}.
Your file may define any of:
    pack_bstar(tree, modules)            -> {id: {"x", "y", "w", "h"}}
    bounding_box(pack)                   -> (width, height) of the smallest box around all blocks
    is_legal(pack, outline)              -> True when every block is inside the outline and none overlap
    swap(tree, a, b)                     -> NEW tree with the names a and b exchanged (shape stays)
    rotate(modules, id)                  -> NEW module list where that block's w and h are exchanged
    move_leaf(tree, leaf, parent, side)  -> NEW tree: cut the leaf, hang it on parent's free "left" or "right" slot
Functions you have not written yet are reported as SKIP. Never change the tree or the list you are given.

THE RULE (written exactly, because the code of the course never wrote it down)
    Origin bottom-left, y grows upward. Sizes are w x h ("3 x 2" = w 3, h 2). Walk the tree in PREORDER:
    place the node, then its WHOLE left subtree, then its right child.
      root:         x = 0
      left child:   x = parent.x + parent.w     ("next door": right of the parent)
      right child:  x = parent.x                ("upstairs": same left edge as the parent)
      every block:  y = the highest skyline value over [x, x + w)   (it falls until it touches something)
    Skyline (contour) = for every x, the top edge of what is already placed (0 where nothing is).
    Placing a block raises the skyline to y + h over [x, x + w).
    Legal = inside the outline and no interior overlap (touching edges is allowed).
    Score = bounding-box area. Wasted squares = bounding-box area - sum of block areas.
    (Outline deadspace W*H - sum of block areas is a different number and never changes with the tree.)
Operations: swap = exchange two names in the tree; rotate = exchange one block's w and h; move = cut a leaf
and hang it on a free left or right slot of another node.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import itertools
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # do not leave __pycache__ in common/
HERE = Path(__file__).resolve().parent
COMMON = HERE.parents[1] / "common"
CORE_JS = HERE.parents[3] / "platform" / "assets" / "floorplanning-core.js"

# One fixed colour per block, everywhere (PAPER_PALETTE of floorplanning-core.js, keyed by id).
COLORS = {"A": "#1d4ed8", "B": "#0f6b5c", "C": "#b45309", "D": "#7c3aed", "E": "#be123c"}


# ---------------- trees: text form, validation, operations ----------------
def parse_tree(s):
    """`A(B(C(E,-),-),D)` -> nested dict. `-` is an empty child; a bare id is a leaf."""
    pos = 0

    def ident():
        nonlocal pos
        start = pos
        while pos < len(s) and (s[pos].isalnum() or s[pos] == "_"):
            pos += 1
        if start == pos:
            raise ValueError(f"expected a name at position {pos} of {s!r}")
        return s[start:pos]

    def child():
        nonlocal pos
        if s[pos] == "-":
            pos += 1
            return None
        return node()

    def node():
        nonlocal pos
        out = {"id": ident()}
        if pos < len(s) and s[pos] == "(":
            pos += 1
            left = child()
            if s[pos] != ",":
                raise ValueError(f"expected ',' at position {pos} of {s!r}")
            pos += 1
            right = child()
            if s[pos] != ")":
                raise ValueError(f"expected ')' at position {pos} of {s!r}")
            pos += 1
            if left:
                out["left"] = left
            if right:
                out["right"] = right
        return out

    tree = node()
    if pos != len(s):
        raise ValueError(f"extra text after position {pos} of {s!r}")
    return tree


def fmt_tree(t):
    """Nested dict -> the short text form (inverse of parse_tree)."""
    if t is None:
        return "-"
    if not t.get("left") and not t.get("right"):
        return t["id"]
    return f"{t['id']}({fmt_tree(t.get('left'))},{fmt_tree(t.get('right'))})"


def preorder(t):
    """Walk order: the node, its whole left subtree, then its right child. Returns ids."""
    if not t:
        return []
    return [t["id"]] + preorder(t.get("left")) + preorder(t.get("right"))


def tree_problems(tree, ids):
    """[] when every module appears exactly once and no unknown name appears, else a list of sentences."""
    seen = preorder(tree)
    out = [f"{i} appears {seen.count(i)} times" for i in sorted(set(seen)) if seen.count(i) > 1]
    out += [f"{i} is not in the tree" for i in sorted(ids) if i not in seen]
    out += [f"{i} is not a module" for i in sorted(set(seen)) if i not in ids]
    return out


def swap(tree, a, b):
    """New tree with the names a and b exchanged. The shape (who is whose left / right child) stays.

    Why: this is the cheapest move of simulated annealing; it never creates an invalid tree.
    """
    t = copy.deepcopy(tree)

    def walk(n):
        if not n:
            return
        if n["id"] == a:
            n["id"] = b
        elif n["id"] == b:
            n["id"] = a
        walk(n.get("left"))
        walk(n.get("right"))

    walk(t)
    return t


def rotate(modules, id_):
    """New module list where block `id_` is turned 90 degrees (its w and h are exchanged).

    The tree does not change; the same tree with a turned block is a different picture.
    """
    out = copy.deepcopy(list(modules))
    for m in out:
        if m["id"] == id_:
            m["w"], m["h"] = m["h"], m["w"]
    return out


def move_leaf(tree, leaf, parent, side):
    """New tree: cut `leaf` (a node with no children, not the root) and hang it on parent's free `side` slot.

    The slot is free after the cut (moving a leaf to the other side of its own parent is allowed).
    Raises ValueError for a non-leaf, the root, parent == leaf, or a slot that is taken.
    """
    if side not in ("left", "right"):
        raise ValueError("side must be 'left' or 'right'")
    t = copy.deepcopy(tree)
    if t["id"] == leaf:
        raise ValueError("the root cannot be moved")
    if leaf == parent:
        raise ValueError("a leaf cannot hang on itself")
    cut = [False]

    def remove(n):
        for s in ("left", "right"):
            c = n.get(s)
            if c and c["id"] == leaf:
                if c.get("left") or c.get("right"):
                    raise ValueError(f"{leaf} is not a leaf")
                del n[s]
                cut[0] = True
                return
            if c:
                remove(c)

    remove(t)
    if not cut[0]:
        raise ValueError(f"{leaf} is not in the tree")

    def attach(n):
        if n["id"] == parent:
            if n.get(side):
                raise ValueError(f"{parent}.{side} is taken")
            n[side] = {"id": leaf}
            return True
        return any(attach(n[s]) for s in ("left", "right") if n.get(s))

    if not attach(t):
        raise ValueError(f"{parent} is not in the tree")
    return t


def leaf_moves(tree):
    """Every legal single leaf move as (leaf, parent, side), in sorted order, excluding no-ops."""
    out = []
    leaves = [i for i in preorder(tree) if not _node(tree, i).get("left") and not _node(tree, i).get("right")]
    for leaf in sorted(leaves):
        if leaf == tree["id"]:
            continue
        for parent in sorted(preorder(tree)):
            for side in ("left", "right"):
                try:
                    new = move_leaf(tree, leaf, parent, side)
                except ValueError:
                    continue
                if fmt_tree(new) != fmt_tree(tree):
                    out.append((leaf, parent, side))
    return out


def _node(t, id_):
    if t["id"] == id_:
        return t
    for s in ("left", "right"):
        if t.get(s):
            r = _node(t[s], id_)
            if r:
                return r
    return None


def all_trees(ids):
    """Every labelled binary tree that uses each id exactly once (5 ids -> Catalan(5) * 5! = 5040)."""
    ids = sorted(ids)
    if not ids:
        yield None
        return
    for r in ids:
        rest = [i for i in ids if i != r]
        for k in range(len(rest) + 1):
            for left_ids in itertools.combinations(rest, k):
                right_ids = [i for i in rest if i not in left_ids]
                for lt in all_trees(list(left_ids)):
                    for rt in all_trees(right_ids):
                        n = {"id": r}
                        if lt:
                            n["left"] = lt
                        if rt:
                            n["right"] = rt
                        yield n


# ---------------- the reference packer ----------------
def pack_bstar(tree, modules, trace=None, _right_first=False, _contour=True):
    """Pack a B*-tree. The exact rule is in the module docstring (preorder, skyline).

    1. Walk in preorder: node, whole left subtree, then right child.
    2. x: root 0; left child parent.x + parent.w; right child parent.x.
    3. y: the highest skyline value over [x, x + w); raise the skyline to y + h over [x, x + w).
    Why: a block falls until it touches the highest thing under it, so a tall neighbour can lift it.

    `trace` (a list) receives one dict per placement: walk number, id, parent, side, x, y, w, h,
    the blocks that hold the new block up, the empty squares left under it, and the skyline and
    bounding box right after. `_right_first` and `_contour` exist only so the checker can count how
    many trees a wrong rule would get wrong; they are not part of the learner API.
    """
    by_id = {m["id"]: m for m in modules}
    pack = {}
    sky = []  # skyline segments [x1, x2, top, id], sorted, covering [0, widest x so far)

    def under(x1, x2):
        """(highest skyline value over [x1, x2), ids of the blocks whose top edge is that high)."""
        top, who = 0, []
        for s in sky:
            if s[1] > x1 and s[0] < x2:
                top = max(top, s[2])
        for s in sky:
            if s[1] > x1 and s[0] < x2 and s[2] == top and top > 0:
                who.append(s[3])
        return top, who

    def hole(x1, x2, y):
        """Empty squares between the skyline and the bottom of a block at height y."""
        area, covered = 0, 0
        for s in sky:
            if s[1] > x1 and s[0] < x2:
                width = min(s[1], x2) - max(s[0], x1)
                covered += width
                area += width * (y - s[2])
        return area + (x2 - x1 - covered) * y

    def raise_to(x1, x2, top, id_):
        nxt = []
        for s in sky:
            if s[1] <= x1 or s[0] >= x2:
                nxt.append(s)
            else:
                if s[0] < x1:
                    nxt.append([s[0], x1, s[2], s[3]])
                if s[1] > x2:
                    nxt.append([x2, s[1], s[2], s[3]])
        nxt.append([x1, x2, top, id_])
        nxt.sort(key=lambda s: s[0])
        sky[:] = nxt

    def merged():
        out = []
        for s in sky:
            if out and out[-1][2] == s[2] and out[-1][1] == s[0]:
                out[-1][1] = s[1]
            else:
                out.append([s[0], s[1], s[2]])
        return out

    def place(node, x, parent, side):
        m = by_id[node["id"]]
        if _contour:
            y, who = under(x, x + m["w"])
            gap = hole(x, x + m["w"], y)
        else:  # the wrong shortcut: look only at the parent
            p = pack.get(parent)
            y = 0 if p is None else (p["y"] if side == "left" else p["y"] + p["h"])
            who, gap = [], 0
        pack[node["id"]] = {"x": x, "y": y, "w": m["w"], "h": m["h"]}
        raise_to(x, x + m["w"], y + m["h"], node["id"])
        if trace is not None:
            bw = max(r["x"] + r["w"] for r in pack.values())
            bh = max(r["y"] + r["h"] for r in pack.values())
            trace.append({
                "k": len(trace) + 1, "id": node["id"], "parent": parent, "side": side,
                "x": x, "y": y, "w": m["w"], "h": m["h"],
                "supported_by": who if y > 0 else ["floor"], "hole_under": gap,
                "contour": merged() if _contour else None, "bbox": [bw, bh],
            })
        kids = [("left", node.get("left"), x + m["w"]), ("right", node.get("right"), x)]
        if _right_first:
            kids.reverse()
        for s, c, cx in kids:
            if c:
                place(c, cx, node["id"], s)

    if tree:
        place(tree, 0, None, "root")
    return pack


def bounding_box(pack):
    """(width, height) of the smallest box that holds every block: max(x + w), max(y + h)."""
    return (max(r["x"] + r["w"] for r in pack.values()), max(r["y"] + r["h"] for r in pack.values()))


def legality(pack, outline):
    """{"legal", "outside": ids sticking out, "overlaps": pairs}. Touching edges is not an overlap."""
    outside = sorted(i for i, r in pack.items()
                     if r["x"] < 0 or r["y"] < 0 or r["x"] + r["w"] > outline["w"] or r["y"] + r["h"] > outline["h"])
    ids = sorted(pack)
    overlaps = []
    for a, b in itertools.combinations(ids, 2):
        p, q = pack[a], pack[b]
        if not (p["x"] + p["w"] <= q["x"] or q["x"] + q["w"] <= p["x"]
                or p["y"] + p["h"] <= q["y"] or q["y"] + q["h"] <= p["y"]):
            overlaps.append((a, b))
    return {"legal": not outside and not overlaps, "outside": outside, "overlaps": overlaps}


def is_legal(pack, outline):
    return legality(pack, outline)["legal"]


def block_area(modules):
    return sum(m["w"] * m["h"] for m in modules)


def score(pack, modules, outline):
    """Everything a figure or a quiz item needs about one pack."""
    bw, bh = bounding_box(pack)
    leg = legality(pack, outline)
    return {
        "bbox": [bw, bh], "area": bw * bh, "wasted": bw * bh - block_area(modules),
        "legal": leg["legal"], "outside": leg["outside"], "overlaps": [list(p) for p in leg["overlaps"]],
    }


def pos_string(pack):
    return " ".join(f"{i}({r['x']},{r['y']})" for i, r in sorted(pack.items()))


# ---------------- the module file (W/H or w/h) ----------------
def load_modules():
    """(modules, outline) from examples/tiny_modules.json; the outline may use W/H or w/h."""
    data = json.loads((HERE / "tiny_modules.json").read_text(encoding="utf-8"))
    o = data["outline"]
    outline = {"w": o.get("w", o.get("W")), "h": o.get("h", o.get("H"))}
    modules = [{"id": m["id"], "w": m["w"], "h": m["h"]} for m in data["modules"]]
    return modules, outline


def with_rotated(modules, rotated):
    for i in rotated or []:
        modules = rotate(modules, i)
    return modules


# ---------------- examples (examples/*.json) ----------------
EXAMPLE_FILES = ["golden", "lift", "order", "floor", "swap", "rotate", "move", "best"]


def load_example(name):
    return json.loads((HERE / f"{name}.json").read_text(encoding="utf-8"))


def run_scene(tree_text, rotated, modules, outline, trace=None):
    tree = parse_tree(tree_text)
    mods = with_rotated(modules, rotated)
    pack = pack_bstar(tree, mods, trace)
    out = score(pack, mods, outline)
    out["pos"] = {i: [r["x"], r["y"]] for i, r in sorted(pack.items())}
    return out, pack, mods


def expect_of(tree_text, rotated, modules, outline):
    """The `expect` block that goes into an example file (written by --write-examples)."""
    e, _, _ = run_scene(tree_text, rotated, modules, outline)
    return {k: e[k] for k in ("pos", "bbox", "area", "wasted", "legal")}


def apply_op(tree, modules, op, args):
    """Apply one of the three operations. Returns (tree, modules)."""
    if op == "swap":
        return swap(tree, *args), modules
    if op == "rotate":
        return tree, rotate(modules, args[0])
    if op == "move":
        return move_leaf(tree, *args), modules
    raise ValueError(op)


# ---------------- statistics over all labelled trees ----------------
def stats(modules, outline):
    """Counts over the 5040 labelled trees on the five blocks (all from the reference packer)."""
    ids = [m["id"] for m in modules]
    n = legal = overlaps = too_wide = too_tall = 0
    right_first_differs = no_contour_differs = right_lifted = left_lifted = 0
    rows = []
    for t in all_trees(ids):
        n += 1
        p = pack_bstar(t, modules)
        s = score(p, modules, outline)
        if s["overlaps"]:
            overlaps += 1
        bw, bh = s["bbox"]
        too_wide += bw > outline["w"]
        too_tall += bh > outline["h"]
        legal += s["legal"]
        if pack_bstar(t, modules, _right_first=True) != p:
            right_first_differs += 1
        if pack_bstar(t, modules, _contour=False) != p:
            no_contour_differs += 1
        lifted_r = lifted_l = False
        for i in ids:
            nd = _node(t, i)
            for side in ("left", "right"):
                c = nd.get(side)
                if not c:
                    continue
                if side == "right" and p[c["id"]]["y"] > p[i]["y"] + p[i]["h"]:
                    lifted_r = True
                if side == "left" and p[c["id"]]["y"] > p[i]["y"]:
                    lifted_l = True
        right_lifted += lifted_r
        left_lifted += lifted_l
        rows.append((fmt_tree(t), s["area"], s["legal"]))
    legal_areas = sorted(a for _, a, lg in rows if lg)
    best = legal_areas[0]
    return {
        "trees": n, "legal": legal, "overlapping": overlaps, "too_wide": too_wide, "too_tall": too_tall,
        "best_area": best, "best_trees": sorted(t for t, a, lg in rows if lg and a == best),
        "legal_below": {a: sum(1 for x in legal_areas if x < a) for a in (27, 36, 40)},
        "right_first_differs": right_first_differs, "no_contour_differs": no_contour_differs,
        "right_child_lifted": right_lifted, "left_child_lifted": left_lifted,
    }


def ops_table(example, modules, outline):
    """What ONE operation can do to an example's tree: count, best bounding-box area, how many reach it.

    Looks at every swap of two names, every single rotation and every leaf move. `start` is the area before.
    """
    ex = load_example(example)
    t0, m0 = parse_tree(ex["tree"]), with_rotated(modules, ex.get("rotated"))
    ids = sorted(m["id"] for m in modules)
    start = score(pack_bstar(t0, m0), m0, outline)["area"]

    def row(areas):
        best = min(areas)
        return {"count": len(areas), "best": best, "n_best": areas.count(best), "same_as_start": areas.count(start)}

    res = {"start": start}
    res["swaps"] = row([score(pack_bstar(swap(t0, a, b), m0), m0, outline)["area"] for a, b in itertools.combinations(ids, 2)])
    res["rotations"] = row([score(pack_bstar(t0, rotate(m0, i)), rotate(m0, i), outline)["area"] for i in ids])
    res["moves"] = row([score(pack_bstar(move_leaf(t0, *mv), m0), m0, outline)["area"] for mv in leaf_moves(t0)])
    return res


def legal_rotations(tree_text, modules, outline):
    """Every set of turned blocks (of 32) that makes this tree legal: a list of sorted id lists."""
    t = parse_tree(tree_text)
    ids = sorted(m["id"] for m in modules)
    out = []
    for k in range(len(ids) + 1):
        for sub in itertools.combinations(ids, k):
            mods = with_rotated(modules, sub)
            if score(pack_bstar(t, mods), mods, outline)["legal"]:
                out.append(list(sub))
    return out


# ---------------- golden tables (pinned; checked against common/ and the browser JS) ----------------
GOLDEN = {
    # counts over the 5040 labelled trees on A to E (outline 10x8); the 8 best trees are also listed in best.json
    "stats": {
        "trees": 5040, "legal": 4680, "overlapping": 0, "too_wide": 120, "too_tall": 240,
        "best_area": 24,
        "legal_below": {27: 216, 36: 2352, 40: 2672},  # legal trees with a SMALLER box than 27 / 36 / 40
        "right_first_differs": 1764,   # trees whose pack changes if the right child is placed first
        "no_contour_differs": 2714,    # trees whose pack changes if y is read from the parent, not the skyline
        "right_child_lifted": 360,     # trees with a right child above its parent's top edge
        "left_child_lifted": 254,      # trees with a left child above its parent's y
    },
    # one operation on an example's tree: count, best area, how many reach it, how many leave the area unchanged
    "ops": {
        "golden": {"start": 27,
                   "swaps": {"count": 10, "best": 27, "n_best": 4, "same_as_start": 4},
                   "rotations": {"count": 5, "best": 27, "n_best": 2, "same_as_start": 2},
                   "moves": {"count": 8, "best": 27, "n_best": 1, "same_as_start": 1}},
        "swap": {"start": 40,
                 "swaps": {"count": 10, "best": 27, "n_best": 1, "same_as_start": 5},
                 "rotations": {"count": 5, "best": 32, "n_best": 1, "same_as_start": 2},
                 "moves": {"count": 8, "best": 28, "n_best": 2, "same_as_start": 1}},
    },
    # sets of turned blocks (of 32) that make the all-left chain legal
    "chain_legal_rotations": [
        ["D"], ["A", "D"], ["C", "D"], ["D", "E"], ["A", "B", "D"], ["A", "C", "D"], ["A", "D", "E"],
        ["C", "D", "E"], ["A", "B", "C", "D"], ["A", "B", "D", "E"], ["A", "C", "D", "E"], ["A", "B", "C", "D", "E"],
    ],
}


# ---------------- checks against the node packer and against common/ ----------------
def vs_node(modules, outline):
    if not CORE_JS.exists():
        print("SKIP  --vs-node: platform/assets/floorplanning-core.js not found")
        return 0
    ids = [m["id"] for m in modules]
    cases = [{"tree": t, "modules": modules} for t in all_trees(ids)]
    n_trees = len(cases)
    for name in EXAMPLE_FILES:  # also the rotated examples
        ex = load_example(name)
        for stage in [ex] + ([ex["then"]] if "then" in ex else []):
            cases.append({"tree": parse_tree(stage["tree"]), "modules": with_rotated(modules, stage.get("rotated"))})
    js = (
        f'import {{ packBstar }} from "{CORE_JS.as_uri()}";'
        'import fs from "node:fs";'
        "const cases = JSON.parse(fs.readFileSync(0, 'utf8'));"
        "console.log(JSON.stringify(cases.map((c) => packBstar(c.tree, c.modules))));"
    )
    try:
        res = subprocess.run(["node", "--input-type=module", "-e", js], input=json.dumps(cases),
                             capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"SKIP  --vs-node: node failed ({exc})")
        return 0
    theirs = json.loads(res.stdout)
    bad = []
    for c, p in zip(cases, theirs):
        mine = pack_bstar(c["tree"], c["modules"])
        if {i: (r["x"], r["y"], r["w"], r["h"]) for i, r in mine.items()} != \
           {i: (r["x"], r["y"], r["w"], r["h"]) for i, r in p.items()}:
            bad.append(fmt_tree(c["tree"]))
    ok = not bad
    print(f"{'PASS' if ok else 'FAIL'}  packBstar (floorplanning-core.js) agrees with the reference on "
          f"all {n_trees} trees and {len(cases) - n_trees} example scenes" + ("" if ok else f"\n        {len(bad)} differ, first: {bad[:3]}"))
    return 0 if ok else 1


def vs_common(modules, outline):
    """Reference vs courses/learn_floorplanning/common/pack.py on all 5040 trees (read only). Returns None for SKIP."""
    if not (COMMON / "pack.py").exists():
        return None
    sys.path.insert(0, str(COMMON))
    try:
        from pack import pack_bstar as common_pack  # type: ignore
    except Exception:
        return None
    finally:
        sys.path.remove(str(COMMON))
    bad = 0
    for t in all_trees([m["id"] for m in modules]):
        mine = pack_bstar(t, modules)
        theirs = common_pack(t, modules)
        if {i: (r["x"], r["y"], r["w"], r["h"]) for i, r in mine.items()} != \
           {i: (r["x"], r["y"], r["w"], r["h"]) for i, r in theirs.items()}:
            bad += 1
    return bad


# ---------------- --json for the figures and the lesson engine ----------------
def build_json(modules, outline):
    scenes = []
    for name in EXAMPLE_FILES:
        ex = load_example(name)
        stages = [("start" if "then" in ex else "main", ex)] + ([("after", ex["then"])] if "then" in ex else [])
        for stage_name, st in stages:
            trace = []
            res, pack, mods = run_scene(st["tree"], st.get("rotated"), modules, outline, trace)
            scenes.append({
                "id": name if stage_name == "main" else f"{name}_{stage_name}",
                "example": name, "stage": stage_name,
                "title": ex["title"], "idea": ex["idea"],
                "tree": st["tree"], "tree_nested": parse_tree(st["tree"]),
                "walk": preorder(parse_tree(st["tree"])),
                "rotated": st.get("rotated", []), "modules": mods, "outline": outline,
                "pack": {i: pack[i] for i in sorted(pack)}, "steps": trace,
                "bbox": res["bbox"], "area": res["area"], "wasted": res["wasted"], "legal": res["legal"],
                "outside": res["outside"],
                "outline_deadspace": outline["w"] * outline["h"] - block_area(mods),
            })
    relations = []
    for name in EXAMPLE_FILES:
        ex = load_example(name)
        if "then" in ex:
            relations.append({"from": f"{name}_start", "to": f"{name}_after", "op": ex["then"]["op"], "args": ex["then"]["args"]})
        if "derived_from" in ex:
            d = ex["derived_from"]
            relations.append({"from": d["example"], "to": name, "op": d["op"], "args": d["args"]})
    return {"colors": COLORS, "outline": outline, "modules": modules, "scenes": scenes, "relations": relations,
            "stats": stats(modules, outline), "ops": {n: ops_table(n, modules, outline) for n in ("golden", "swap")},
            "chain_legal_rotations": legal_rotations(load_example("rotate")["tree"], modules, outline)}


def show_scene(title, sc):
    print(f"\n{title}   tree {sc['tree']}" + (f"   turned: {','.join(sc['rotated'])}" if sc["rotated"] else ""))
    for st in sc["steps"]:
        who = ",".join(st["supported_by"])
        print(f"   {st['k']}. {st['id']} ({st['side']}"
              + (f" of {st['parent']}" if st["parent"] else "") + f") at ({st['x']},{st['y']}) {st['w']}x{st['h']}"
              f"  held up by {who}  hole {st['hole_under']}  skyline {st['contour']}  box {st['bbox'][0]}x{st['bbox'][1]}")
    print(f"   bounding box {sc['bbox'][0]}x{sc['bbox'][1]} = {sc['area']}, wasted {sc['wasted']}, legal {sc['legal']}"
          + (f", sticks out: {','.join(sc['outside'])}" if sc["outside"] else ""))


# ---------------- main ----------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--impl", help="your .py file with the B*-tree functions")
    ap.add_argument("--show", action="store_true", help="print every pack, step by step")
    ap.add_argument("--vs-node", action="store_true", help="compare with packBstar of the browser lab's JS")
    ap.add_argument("--json", action="store_true", help="print trees, packs, bounding boxes, skylines as JSON")
    ap.add_argument("--dump", action="store_true", help="print the computed golden tables (for authors)")
    ap.add_argument("--write-examples", action="store_true", help="rewrite the `expect` blocks of examples/*.json (authors)")
    args = ap.parse_args()

    modules, outline = load_modules()

    if args.vs_node:
        return vs_node(modules, outline)
    if args.json:
        print(json.dumps(build_json(modules, outline), indent=1))
        return 0
    if args.dump:
        return dump(modules, outline)
    if args.write_examples:
        return write_examples(modules, outline)

    fns = {"pack": pack_bstar, "bbox": bounding_box, "legal": is_legal, "swap": swap, "rotate": rotate, "move": move_leaf}
    name = "reference"
    if args.impl:
        spec = importlib.util.spec_from_file_location("learner_bstar", args.impl)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        fns = {
            "pack": getattr(mod, "pack_bstar", None), "bbox": getattr(mod, "bounding_box", None),
            "legal": getattr(mod, "is_legal", None), "swap": getattr(mod, "swap", None),
            "rotate": getattr(mod, "rotate", None), "move": getattr(mod, "move_leaf", None),
        }
        name = args.impl
    print(f"checking {name}")

    results = []

    def check(label, key, run, ok_fn, expect):
        fn = fns[key]
        if fn is None:
            results.append(None)
            print(f"SKIP  {label}   (function not defined yet)")
            return
        try:
            got = run(fn)
            ok = ok_fn(got)
        except Exception as exc:  # a crash in the learner's code is a FAIL, not a stack trace
            got, ok = f"{type(exc).__name__}: {exc}", False
        results.append(ok)
        print(f"{'PASS' if ok else 'FAIL'}  {label}" + ("" if ok else f"\n        got:      {got}\n        expected: {expect}"))
        if args.show and ok:
            print(f"        {got}")

    def ref(label, ok, detail=""):
        results.append(ok)
        print(f"{'PASS' if ok else 'FAIL'}  {label}" + ("" if ok else f"\n        {detail}"))

    def tri(x):  # compact form of a pack: id -> (x, y, w, h)
        return {i: (r["x"], r["y"], r["w"], r["h"]) for i, r in x.items()}

    def want_pack(ex_name, stage=None):
        ex = load_example(ex_name)
        st = ex[stage] if stage else ex
        _, p, _ = run_scene(st["tree"], st.get("rotated"), modules, outline)
        return tri(p)

    def scene_args(ex_name, stage=None):
        ex = load_example(ex_name)
        st = ex[stage] if stage else ex
        return parse_tree(st["tree"]), with_rotated(modules, st.get("rotated")), st

    def exp_pos(st):
        return {i: tuple(v) for i, v in st["expect"]["pos"].items()}

    def pos_only(p):
        return {i: (r["x"], r["y"]) for i, r in p.items()}

    # --- pack: golden ---
    g_tree, g_mods, g = scene_args("golden")
    check(f"golden {fmt_tree(g_tree)}: A (0,0) B (3,0) C (5,0) D (0,2) E (7,0)", "pack",
          lambda f: pos_only(f(copy.deepcopy(g_tree), copy.deepcopy(g_mods))), lambda x: x == exp_pos(g), exp_pos(g))
    check("golden: the module list in reverse order gives the same pack", "pack",
          lambda f: tri(f(copy.deepcopy(g_tree), list(reversed(g_mods)))), lambda x: x == want_pack("golden"), want_pack("golden"))
    check("golden: the pack keeps each block's w and h", "pack",
          lambda f: tri(f(copy.deepcopy(g_tree), copy.deepcopy(g_mods))), lambda x: x == want_pack("golden"), want_pack("golden"))
    check("golden: pack_bstar does not change the tree or the module list you pass", "pack",
          lambda f: (lambda t, m: (f(t, m), t == g_tree and m == g_mods)[1])(copy.deepcopy(g_tree), copy.deepcopy(g_mods)),
          lambda x: x is True, True)
    check(f"golden: bounding box {g['expect']['bbox'][0]}x{g['expect']['bbox'][1]} = {g['expect']['area']}", "bbox",
          lambda f: tuple(f(pack_bstar(g_tree, g_mods))), lambda x: x == tuple(g["expect"]["bbox"]), g["expect"]["bbox"])
    check(f"golden: legal in the {outline['w']}x{outline['h']} outline", "legal",
          lambda f: f(pack_bstar(g_tree, g_mods), dict(outline)), lambda x: x is True, True)

    # --- pack: the skyline ---
    l_tree, l_mods, lift = scene_args("lift")
    check(f"lift {fmt_tree(l_tree)}: D lands at (0,3), not (0,2), because B is 3 high", "pack",
          lambda f: pos_only(f(copy.deepcopy(l_tree), copy.deepcopy(l_mods))), lambda x: x == exp_pos(lift), exp_pos(lift))
    check(f"lift: bounding box {lift['expect']['bbox'][0]}x{lift['expect']['bbox'][1]} = {lift['expect']['area']}, wasted {lift['expect']['wasted']}", "bbox",
          lambda f: tuple(f(pack_bstar(l_tree, l_mods))), lambda x: x == tuple(lift["expect"]["bbox"]), lift["expect"]["bbox"])
    f_tree, f_mods, fl = scene_args("floor")
    check(f"floor {fmt_tree(f_tree)} with A turned: E is a left child but falls to y = 0", "pack",
          lambda f: pos_only(f(copy.deepcopy(f_tree), copy.deepcopy(f_mods))), lambda x: x == exp_pos(fl), exp_pos(fl))

    # --- pack: the walk order ---
    o_tree, o_mods, od = scene_args("order")
    check(f"order {fmt_tree(o_tree)}: left subtree before right child gives a 7x5 box", "pack",
          lambda f: pos_only(f(copy.deepcopy(o_tree), copy.deepcopy(o_mods))), lambda x: x == exp_pos(od), exp_pos(od))
    check("order: bounding box 7x5 (right child first would give 7x8)", "bbox",
          lambda f: tuple(f(pack_bstar(o_tree, o_mods))), lambda x: x == tuple(od["expect"]["bbox"]), od["expect"]["bbox"])

    # --- the best trees ---
    b_tree, b_mods, best = scene_args("best")
    check(f"best {fmt_tree(b_tree)}: B is lifted onto D, bounding box 6x4 = 24", "pack",
          lambda f: pos_only(f(copy.deepcopy(b_tree), copy.deepcopy(b_mods))), lambda x: x == exp_pos(best), exp_pos(best))

    # --- the operations ---
    s_ex = load_example("swap")
    s_tree, s_mods, s0 = scene_args("swap")
    a, b = s_ex["then"]["args"]
    check(f"swap: start {fmt_tree(s_tree)} packs to a 10x4 box (area 40, wasted 17)", "pack",
          lambda f: pos_only(f(copy.deepcopy(s_tree), copy.deepcopy(s_mods))), lambda x: x == exp_pos(s0), exp_pos(s0))
    check(f"swap({a}, {b}) turns the start into {s_ex['then']['tree']}, the golden tree", "swap",
          lambda f: fmt_tree(f(copy.deepcopy(s_tree), a, b)), lambda x: x == s_ex["then"]["tree"], s_ex["then"]["tree"])
    check("swap: the shape stays, only the names move (swap B and C of the golden)", "swap",
          lambda f: fmt_tree(f(copy.deepcopy(g_tree), "B", "C")), lambda x: x == "A(C(B(E,-),-),D)", "A(C(B(E,-),-),D)")
    check("swap: it returns a new tree and leaves the old one alone", "swap",
          lambda f: (lambda t: (f(t, "A", "C"), t == g_tree)[1])(copy.deepcopy(g_tree)), lambda x: x is True, True)
    check("swap: swapping the same two names twice gives the original tree", "swap",
          lambda f: fmt_tree(f(f(copy.deepcopy(g_tree), "A", "E"), "A", "E")), lambda x: x == fmt_tree(g_tree), fmt_tree(g_tree))
    r_ex = load_example("rotate")
    r_tree, r_mods, r0 = scene_args("rotate")
    check(f"rotate: chain {fmt_tree(r_tree)} is 12 wide: E at (10,0), outside the outline", "pack",
          lambda f: pos_only(f(copy.deepcopy(r_tree), copy.deepcopy(r_mods))), lambda x: x == exp_pos(r0), exp_pos(r0))
    check("rotate: the chain is NOT legal", "legal",
          lambda f: f(pack_bstar(r_tree, r_mods), dict(outline)), lambda x: x is False, False)
    rd = r_ex["then"]["args"][0]
    check(f"rotate(modules, {rd}) exchanges {rd}'s w and h (3x1 becomes 1x3)", "rotate",
          lambda f: [(m["id"], m["w"], m["h"]) for m in f(copy.deepcopy(r_mods), rd)],
          lambda x: x == [(m["id"], m["h"], m["w"]) if m["id"] == rd else (m["id"], m["w"], m["h"]) for m in r_mods], "D turned")
    check("rotate: it returns a new list and leaves the old one alone", "rotate",
          lambda f: (lambda m: (f(m, rd), m == r_mods)[1])(copy.deepcopy(r_mods)), lambda x: x is True, True)
    check("rotate: turning the same block twice gives the original sizes", "rotate",
          lambda f: f(f(copy.deepcopy(r_mods), rd), rd) == r_mods, lambda x: x is True, True)
    _, rr_mods, r1 = scene_args("rotate", "then")
    check(f"rotate: after turning {rd} the chain fits: {r_ex['then']['expect']['bbox'][0]}x{r_ex['then']['expect']['bbox'][1]}, legal", "legal",
          lambda f: f(pack_bstar(r_tree, rr_mods), dict(outline)), lambda x: x is True, True)
    m_ex = load_example("move")
    m_tree, m_mods, m0 = scene_args("move")
    ml, mp, ms = m_ex["then"]["args"]
    check(f"move_leaf({ml}, {mp}, {ms}) turns {m_ex['tree']} into {m_ex['then']['tree']}", "move",
          lambda f: fmt_tree(f(copy.deepcopy(m_tree), ml, mp, ms)), lambda x: x == m_ex["then"]["tree"], m_ex["then"]["tree"])
    check("move_leaf: every module is still in the tree exactly once", "move",
          lambda f: tree_problems(f(copy.deepcopy(m_tree), ml, mp, ms), [m["id"] for m in modules]), lambda x: x == [], [])
    check("move_leaf: it returns a new tree and leaves the old one alone", "move",
          lambda f: (lambda t: (f(t, ml, mp, ms), t == m_tree)[1])(copy.deepcopy(m_tree)), lambda x: x is True, True)

    def refuses(f, *a):
        try:
            f(*a)
        except Exception:
            return True
        return False

    check("move_leaf: refuses to move a node that has children (B of the golden)", "move",
          lambda f: refuses(f, copy.deepcopy(g_tree), "B", "E", "right"), lambda x: x is True, "an error")
    check("move_leaf: refuses a slot that is taken (D under A.left, A.left is B)", "move",
          lambda f: refuses(f, copy.deepcopy(g_tree), "D", "A", "left"), lambda x: x is True, "an error")

    # --- the strongest check: all 5040 trees ---
    ids = [m["id"] for m in modules]

    def sweep(f):
        bad, first = 0, None
        for t in all_trees(ids):
            want = tri(pack_bstar(t, modules))
            got = tri(f(copy.deepcopy(t), copy.deepcopy(modules)))
            if got != want:
                bad += 1
                first = first or fmt_tree(t)
        return (bad, first)

    check("all 5040 labelled trees on A to E: your pack equals the reference pack", "pack",
          sweep, lambda x: x[0] == 0, "0 differences")

    if not args.impl:
        # --- reference only: checks that need helpers outside the learner API ---
        ref_checks(ref, modules, outline, args.show)

    ok = [r for r in results if r is True]
    bad = [r for r in results if r is False]
    skip = [r for r in results if r is None]
    print(f"\n{len(ok)} PASS, {len(bad)} FAIL, {len(skip)} SKIP")
    if args.show and not args.impl:
        for ex_name in EXAMPLE_FILES:
            ex = load_example(ex_name)
            for stage_name, st in [("", ex)] + ([("then ", ex["then"])] if "then" in ex else []):
                trace = []
                res, _, _ = run_scene(st["tree"], st.get("rotated"), modules, outline, trace)
                sc = {"tree": st["tree"], "rotated": st.get("rotated", []), "steps": trace, "bbox": res["bbox"],
                      "area": res["area"], "wasted": res["wasted"], "legal": res["legal"], "outside": res["outside"]}
                show_scene(f"[{ex_name}] {stage_name}".rstrip(), sc)
    return 1 if bad else 0


def ref_checks(ref, modules, outline, show):
    """Checks that only the reference runs: the example files, the 5040-tree statistics, the other packers."""
    ids = [m["id"] for m in modules]
    # the example files agree with the reference
    for name in EXAMPLE_FILES:
        ex = load_example(name)
        bad = []
        for stage_name, st in [("", ex)] + ([("then", ex["then"])] if "then" in ex else []):
            if expect_of(st["tree"], st.get("rotated"), modules, outline) != st["expect"]:
                bad.append(stage_name or "start")
            if tree_problems(parse_tree(st["tree"]), ids):
                bad.append(f"{stage_name} tree invalid")
        if "then" in ex:
            t, m = apply_op(parse_tree(ex["tree"]), with_rotated(modules, ex.get("rotated")), ex["then"]["op"], ex["then"]["args"])
            if fmt_tree(t) != ex["then"]["tree"] or [(x["id"], x["w"], x["h"]) for x in m] != \
               [(x["id"], x["w"], x["h"]) for x in with_rotated(modules, ex["then"].get("rotated"))]:
                bad.append("operation does not give the 'then' scene")
        if "derived_from" in ex:
            d = ex["derived_from"]
            t, _ = apply_op(parse_tree(load_example(d["example"])["tree"]), modules, d["op"], d["args"])
            if fmt_tree(t) != ex["tree"]:
                bad.append("derived_from does not give this tree")
        ref(f"examples/{name}.json: expected packs, boxes and operations agree with the reference", not bad, f"problems: {bad}")

    # reference vs the course packer in common/, and the written rule's counters
    res = vs_common(modules, outline)
    if res is None:
        print("SKIP  common/pack.py not found")
    else:
        ref("reference equals pack_bstar of common/pack.py on all 5040 trees", res == 0, f"{res} trees differ")

    # numbers the labels and the lesson quote
    o = parse_tree(load_example("order")["tree"])
    ref("order: with the right child first the box would be 7x8 (not 7x5)",
        bounding_box(pack_bstar(o, modules, _right_first=True)) == (7, 8), str(bounding_box(pack_bstar(o, modules, _right_first=True))))
    chain = parse_tree(load_example("rotate")["tree"])
    ref("chain: the five widths add up to 12 (3+2+2+3+2), E starts at x = 10",
        sum(m["w"] for m in modules) == 12 and pack_bstar(chain, modules)["E"]["x"] == 10, "widths or E.x differ")
    ref("chain: turning D makes the widths add up to 10 (3+2+2+1+2)",
        sum(m["w"] for m in rotate(modules, "D")) == 10, "sum differs")
    ref("the five block areas add up to 23 (prime), so no rectangle of area 23 holds the 3-high block B",
        block_area(modules) == 23 and all(23 % k for k in range(2, 23)) and max(m["h"] for m in modules) == 3, "23 is not prime or B is not 3 high")
    ref("outline deadspace 80 - 23 = 57 never changes with the tree; the golden box wastes only 4",
        outline["w"] * outline["h"] - block_area(modules) == 57 and load_example("golden")["expect"]["wasted"] == 4, "numbers differ")

    # the written x and y rules hold on every tree
    bad = 0
    for t in all_trees(ids):
        p = pack_bstar(t, modules)
        for i in ids:
            nd = _node(t, i)
            lc, rc = nd.get("left"), nd.get("right")
            if lc and p[lc["id"]]["x"] != p[i]["x"] + p[i]["w"]:
                bad += 1
            if rc and (p[rc["id"]]["x"] != p[i]["x"] or p[rc["id"]]["y"] < p[i]["y"] + p[i]["h"]):
                bad += 1
            if p[i]["y"] < 0:
                bad += 1
    ref("all 5040 trees: left child x = parent.x + parent.w; right child x = parent.x and y >= parent.y + parent.h",
        bad == 0, f"{bad} violations")

    st = stats(modules, outline)
    ops = {n: ops_table(n, modules, outline) for n in ("golden", "swap")}
    rots = legal_rotations(load_example("rotate")["tree"], modules, outline)
    if show:
        print("   stats:", json.dumps(st))
        print("   ops:", json.dumps(ops))
        print("   legal rotations of the chain:", rots)
    for key, want in GOLDEN.get("stats", {}).items():
        ref(f"all 5040 trees: {key} = {want if not isinstance(want, list) else len(want)}", st[key] == want, f"got {st[key]}")
    for name, want in GOLDEN.get("ops", {}).items():
        ref(f"one operation on {name}.json: swaps best {want['swaps']['best']}, turns best {want['rotations']['best']}, "
            f"moves best {want['moves']['best']} (start {want['start']})", ops[name] == want, f"got {ops[name]}")
    if "chain_legal_rotations" in GOLDEN:
        want = GOLDEN["chain_legal_rotations"]
        ref(f"chain: {len(want)} of 32 sets of turned blocks are legal; the only single turn is {[r[0] for r in want if len(r) == 1]}",
            rots == want, f"got {rots}")
    ref("no tree overlaps: a B*-tree is overlap-free by construction", st["overlapping"] == 0, f"{st['overlapping']} trees overlap")
    ref("every illegal tree is illegal only because it sticks out (too wide + too tall)",
        st["legal"] + st["too_wide"] + st["too_tall"] == st["trees"], str(st))
    ref("the best trees listed in best.json are exactly the trees that reach the smallest area",
        sorted(load_example("best")["all_best"]) == st["best_trees"], f"got {st['best_trees']}")


def dump(modules, outline):
    st = stats(modules, outline)
    print("stats =", json.dumps(st, indent=1))
    print("ops =", json.dumps({n: ops_table(n, modules, outline) for n in ("golden", "swap")}, indent=1))
    print("chain_legal_rotations =", json.dumps(legal_rotations(load_example("rotate")["tree"], modules, outline)))
    return 0


def write_examples(modules, outline):
    for name in EXAMPLE_FILES:
        path = HERE / f"{name}.json"
        ex = json.loads(path.read_text(encoding="utf-8"))
        ex["expect"] = expect_of(ex["tree"], ex.get("rotated"), modules, outline)
        if "then" in ex:
            ex["then"]["expect"] = expect_of(ex["then"]["tree"], ex["then"].get("rotated"), modules, outline)
        path.write_text(json.dumps(ex, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("wrote", path.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
