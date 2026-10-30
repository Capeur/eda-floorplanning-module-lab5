#!/usr/bin/env python3
"""French walkthrough frames for Lab 05 (B*-tree), for the site repo (Stage 5).

    python3 capture_fr_frames.py --out <folder> [--base http://127.0.0.1:8081/tools/algorithm-walkthrough]

Needs the scratch viewer patched by patch_walkthrough.py (it holds a "bstar-tree-fr" block with the French
text of the same 5 frames) and served on 8081. Writes 01-root.png ... 05-takeaway.png (same names and size
as the English frames, 940x468) into <folder>. The teacher's capture script is not used here because it
always writes into the module's assets/ and STEPS.md.

The viewer's own chrome is English ("Step 1 / 5 ...", "Explanation"): after each render the two labels are
swapped for the French ones ("Étape", "Explication"), as for Lab 03. Everything else (the frame text, the
tree, the floorplan) is already French in the "bstar-tree-fr" block.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
ap.add_argument("--out", type=Path, required=True)
ap.add_argument("--base", default="http://127.0.0.1:8081/tools/algorithm-walkthrough")
args = ap.parse_args()
args.out.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    for i in range(1, 6):
        page.goto(f"{args.base}/?algo=bstar-tree-fr&step={i}", wait_until="networkidle")
        page.wait_for_selector("#walk-frame[data-ready='1']")
        page.wait_for_timeout(300)
        page.evaluate("""() => {
            const f = document.getElementById('walk-frame');
            const meta = f.querySelector('.step-meta');
            meta.textContent = meta.textContent.replace(/^Step /, 'Étape ');
            f.querySelector('.walk-explain h2').textContent = 'Explication';
        }""")
        sid = page.get_attribute("#walk-frame", "data-step-id")
        path = args.out / f"{i:02d}-{sid}.png"
        page.locator("#walk-frame").screenshot(path=str(path))
        print("wrote", path)
    browser.close()
