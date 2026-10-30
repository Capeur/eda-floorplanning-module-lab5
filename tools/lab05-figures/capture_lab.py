#!/usr/bin/env python3
"""Capture assets/lab-starter.png (transcript slide 28) from the Lab 05 browser lab after real learner actions.

    python3 -m http.server 8080 --directory <clone>/platform     # in another shell
    python3 capture_lab.py --module <clone>/courses/learn_floorplanning/module02-03-bstar-tree

French (the translated lab of the built site, served from docs/):
    python3 -m http.server 8090 --directory <site repo>/docs
    python3 capture_lab.py --url http://127.0.0.1:8090/fr/tools/bstar-tree/index.html \\
        --out <site repo>/i18n/fr/module02-03-bstar-tree/assets/lab-starter.png

Actions (element ids only, so the same script works on the French copy): start the challenge
"Lift D to y = 3", swap A and C, Pack, Check (it must PASS). The shot is the "Tree and floorplan"
panel only, at 2x (about 1880x1150): a whole-page shot was too small to read on the 16:9 slide.
"""
import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("--module", type=Path, help="module dir (English: writes <module>/assets/lab-starter.png)")
ap.add_argument("--url", default="http://127.0.0.1:8080/tools/bstar-tree/index.html")
ap.add_argument("--out", type=Path, help="output PNG (default: <module>/assets/lab-starter.png)")
args = ap.parse_args()
if not args.out and not args.module:
    ap.error("give --module or --out")
out = args.out or (args.module / "assets" / "lab-starter.png")

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1280, "height": 1400}, device_scale_factor=2)
    pg.goto(args.url, wait_until="networkidle")
    pg.add_style_tag(content="html{scroll-behavior:auto!important}")
    pg.wait_for_selector("#bt-floor")
    pg.select_option("#lab-chal-sel", "d-at-3")
    pg.click("#lab-chal-start")
    pg.select_option("#bt-swap-a", "A")
    pg.select_option("#bt-swap-b", "C")
    pg.click("#bt-do-swap")
    pg.click("#bt-pack")
    pg.click("#lab-chal-check")
    assert "pass" in pg.get_attribute("#lab-status", "class"), "the challenge did not pass"
    out.parent.mkdir(parents=True, exist_ok=True)
    pg.locator("#lab-root .tool-layout .panel").first.screenshot(path=str(out))
    b.close()
print(f"Wrote {out}")
