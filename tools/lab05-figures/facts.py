#!/usr/bin/env python3
"""Save every number the Lab 05 figures and frames use, straight from the module checker.

    python3 facts.py <module dir>        # writes facts.json next to this file

Runs `examples/bstar_check.py --json` (the reference packer) and keeps its output whole, then checks
the numbers the transcript speaks, so a change in the checker stops the figures instead of drawing
a wrong picture. Nothing on a figure is typed by hand: make_figures.py and patch_walkthrough.py
read facts.json.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    mod = Path(sys.argv[1]).resolve()
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    out = subprocess.run([sys.executable, "examples/bstar_check.py", "--json"], cwd=mod, env=env,
                         check=True, capture_output=True, text=True).stdout
    d = json.loads(out)
    sc = {s["id"]: s for s in d["scenes"]}
    pos = lambda s, i: next((st["x"], st["y"]) for st in sc[s]["steps"] if st["id"] == i)  # noqa: E731

    # the numbers the transcript says aloud (slide numbers in brackets)
    g, lift, chain, turn, best = sc["golden"], sc["lift"], sc["rotate_start"], sc["rotate_after"], sc["best"]
    assert d["outline"] == {"w": 10, "h": 8}                                         # [3]
    assert g["tree"] == "A(B(C(E,-),-),D)" and g["walk"] == ["A", "B", "C", "E", "D"]  # [9]
    assert pos("golden", "A") == (0, 0) and pos("golden", "B") == (3, 0)              # [5, 8]
    assert pos("golden", "C") == (5, 0) and pos("golden", "E") == (7, 0)              # [10]
    assert pos("golden", "D") == (0, 2)                                               # [11, 12]
    assert g["bbox"] == [9, 3] and g["area"] == 27 and g["wasted"] == 4 and g["legal"]  # [16, 17]
    assert sum(m["w"] * m["h"] for m in d["modules"]) == 23                           # [17]
    assert lift["tree"] == "C(B(A(E,-),-),D)" and pos("lift", "D") == (0, 3)          # [13, 15]
    d5 = lift["steps"][-1]
    assert d5["id"] == "D" and d5["supported_by"] == ["B"] and d5["hole_under"] == 2  # [15]
    assert lift["bbox"] == [9, 4] and lift["area"] == 36 and lift["wasted"] == 13     # [18]
    assert {"from": "golden", "to": "lift", "op": "swap", "args": ["A", "C"]} in d["relations"]
    assert chain["tree"] == "A(B(C(D(E,-),-),-),-)"                                   # [19]
    assert chain["steps"][3]["x"] + chain["steps"][3]["w"] == 10                      # [20] 3+2+2+3
    assert pos("rotate_start", "E") == (10, 0) and chain["bbox"][0] == 12             # [21]
    assert not chain["legal"] and chain["outside"] == ["E"]                           # [21]
    assert d["stats"]["overlapping"] == 0                                             # [22]
    assert turn["rotated"] == ["D"] and turn["bbox"][0] == 10 and turn["legal"]       # [23]
    assert next(m for m in turn["modules"] if m["id"] == "D") == {"id": "D", "w": 1, "h": 3}
    assert d["chain_legal_rotations"][0] == ["D"]
    assert d["stats"]["legal_below"]["27"] > 0 and d["stats"]["best_area"] == 24      # [24, 25]
    assert best["tree"] == "A(D,C(E(B,-),-))" and best["walk"] == ["A", "D", "C", "E", "B"]  # [25]
    assert pos("best", "B") == (4, 1) and best["steps"][-1]["supported_by"] == ["D"]  # [26]
    assert best["bbox"] == [6, 4] and best["area"] == 24 and best["wasted"] == 1      # [26]
    assert d["stats"]["trees"] == 5040                                                # [29]

    (HERE / "facts.json").write_text(json.dumps(d, indent=1))
    print("wrote", HERE / "facts.json", f"({len(d['scenes'])} scenes, all spoken numbers checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
