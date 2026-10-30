#!/usr/bin/env python3
"""Browser test of the BUILT site's lab (B*-tree, Lab 05), in English and French.

It is the course's own platform/tools/bstar-tree/tests/test_lab_playwright.py (same learner actions, same cases:
every challenge passes when solved with the menus and buttons, and never on load, after Clear, from Pack alone, from
the reveal, from a preset, from a wrong answer or after an edit made after Pack; one fixed colour per block id)
run against docs/ and docs/fr/. The actions use element ids, so they are identical in both languages; the LANGS table
holds only what the page says in each language (the PASS word, the "Check:" line, the progress word, the text that
must NOT be left over from the other language).

    python3 -m http.server 8090 --directory docs          # from this repo's root, in another shell
    python3 tools/test_lab_site.py [--base http://127.0.0.1:8090] [--lang en|fr|both] [--teacher ../eda-learning-lab5-fp] [--headed]

Also per language: html lang, no console error, failed request, HTTP error or request outside the site; the French
lab shows no English snippet of the lab (page, messages, Check lines). Needs: pip install playwright pillow &&
python3 -m playwright install chromium
"""
from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser()
ap.add_argument("--base", default="http://127.0.0.1:8090")
ap.add_argument("--lang", choices=["en", "fr", "both"], default="both")
ap.add_argument("--teacher", default=HERE.parent / "eda-learning-lab5-fp", type=Path)
ap.add_argument("--headed", action="store_true")
args = ap.parse_args()
BASE = args.base.rstrip("/")
sys.path.insert(0, str(args.teacher / "courses/learn_floorplanning/module02-03-bstar-tree/examples"))
import bstar_check as C  # noqa: E402

COLORS = C.COLORS  # A blue, B teal, C amber, D violet, E rose

# what the page says in each language
LANGS = {
    "en": {"prefix": "", "html_lang": "en", "check_head": "Check:", "progress": "9 / 9", "pack": "Pack",
           "status_pass": "PASS", "leftover": []},
    "fr": {"prefix": "fr/", "html_lang": "fr", "check_head": "Vérification :", "progress": "9 / 9", "pack": "Placer",
           "status_pass": "RÉUSSI",
           "leftover": ["Skip to content", "Edit the tree", "Tree and floorplan", "Reveal an answer", "Reset workspace",
                        "Next challenge", "Show hint", "Pick one", "Press Pack", "Check:", "next door", "upstairs",
                        "skyline", "bounding box", "wasted squares", "walk order", "Not legal", "Packed:",
                        "Swapped the names", "Interactive tool"]},
}


# ---------------- learner actions (element ids only) ----------------
def start(pg, cid):
    pg.select_option("#lab-chal-sel", cid)
    pg.click("#lab-chal-start")


def check(pg):
    pg.click("#lab-chal-check")
    return "pass" in (pg.get_attribute("#lab-status", "class") or "").split()


def parent(pg, i, v):
    pg.select_option(f"#bt-parent-{i}", v)


def side(pg, i, v):
    pg.select_option(f"#bt-side-{i}", v)


def swap(pg, a, b):
    pg.select_option("#bt-swap-a", a)
    pg.select_option("#bt-swap-b", b)
    pg.click("#bt-do-swap")


def turn(pg, i):
    pg.select_option("#bt-turn", i)
    pg.click("#bt-do-turn")


def move(pg, leaf, to, sd):
    pg.select_option("#bt-move-leaf", leaf)
    pg.select_option("#bt-move-parent", to)
    pg.select_option("#bt-move-side", sd)
    pg.click("#bt-do-move")


def guess(pg, v):
    pg.fill("#bt-guess", str(v))
    pg.click("#bt-save-guess")


def pack(pg):
    pg.click("#bt-pack")


def clear(pg):
    pg.click("#bt-clear")


def reveal(pg):
    pg.click("#bt-reveal")


def preset(name):
    return lambda pg: pg.click(f"#bt-preset-{name}")


def build(text):
    """Set every block's Parent and Side menus, in walk order, to make the tree `text`."""
    def act(pg):
        def walk(n, par, sd):
            if not n:
                return
            parent(pg, n["id"], par)
            if par != "root":
                side(pg, n["id"], sd)
            walk(n.get("left"), n["id"], "left")
            walk(n.get("right"), n["id"], "right")
        walk(C.parse_tree(text), "root", None)
    return act


def seq(*acts):
    def act(pg):
        for a in acts:
            a(pg)
    return act


def edit_back(pg):
    """Turn B and turn it back: same tree as before, but the Pack no longer counts."""
    turn(pg, "B")
    turn(pg, "B")


# ---------------- the cases ----------------
SOLVE = {
    "build-golden": seq(build("A(B(C(E,-),-),D)"), pack),
    "d-at-3": seq(lambda pg: swap(pg, "A", "C"), pack),
    "predict-dy": seq(lambda pg: guess(pg, 4), pack),
    "chain-turn": seq(lambda pg: turn(pg, "D"), pack),
    "fix-swap": seq(lambda pg: swap(pg, "D", "E"), pack),
    "move-leaf": seq(lambda pg: move(pg, "D", "B", "right"), pack),
    # long row -> golden with two menu edits: D upstairs on A, then E next door to C
    "reach-27": seq(lambda pg: (parent(pg, "D", "A"), side(pg, "D", "right"), parent(pg, "E", "C"), side(pg, "E", "left")), pack),
    "beat-27": seq(clear, build("A(-,D(B,C(E,-)))"), pack),  # 5 x 5 = 25
    # golden -> A(D,C(E(B,-),-)) without Clear: D next door to A (two blocks share the slot for a moment), C upstairs, B on E
    "reach-24": seq(lambda pg: (side(pg, "D", "left"), parent(pg, "C", "A"), side(pg, "C", "right"),
                                parent(pg, "B", "E"), side(pg, "B", "left")), pack),
}
WRONG = {
    "build-golden": seq(build("A(B(C(-,E),-),D)"), pack),      # E upstairs on C
    "d-at-3": seq(lambda pg: swap(pg, "B", "C"), pack),
    "predict-dy": seq(lambda pg: guess(pg, 3), pack),           # the parent's top, not the skyline
    "chain-turn": seq(lambda pg: turn(pg, "C"), pack),          # a square: turning changes nothing
    "fix-swap": seq(lambda pg: swap(pg, "A", "D"), pack),       # the wrong swap: 30
    "move-leaf": seq(lambda pg: move(pg, "E", "D", "right"), pack),
    "reach-27": seq(lambda pg: turn(pg, "D"), pack),            # legal, but 30
    "beat-27": seq(lambda pg: swap(pg, "C", "E"), pack),        # still 27
    "reach-24": seq(clear, build("A(B,C(E,D))"), lambda pg: turn(pg, "A"), pack),  # 24, but with a turn
}
PRESET_TRAP = {  # the preset closest to an answer
    "build-golden": "golden", "d-at-3": "lift", "predict-dy": "order", "chain-turn": "chain", "fix-swap": "golden",
    "move-leaf": "swap", "reach-27": "golden", "beat-27": "golden", "reach-24": "golden",
}


def negatives(cid):
    return {
        "load (Start, Check)": lambda pg: None,
        "Clear": clear,
        "Clear + Pack": seq(clear, pack),
        "Pack only": pack,
        "Reveal": reveal,
        "Reveal + Pack": seq(reveal, pack),
        "wrong answer": WRONG[cid],
        "edit after Pack": seq(SOLVE[cid], edit_back),
        f"preset {PRESET_TRAP[cid]} + Pack": seq(preset(PRESET_TRAP[cid]), pack),
    }


def pixel_rgb(pg, shot, selector, where):
    """Colour of the screenshot inside the element: where = 'lower-left' (blocks) or 'node' (tree circles)."""
    box = pg.evaluate(
        "(s) => { const r = document.querySelector(s).getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; }",
        selector)
    x, y, w, h = box
    px, py = (x + 7, y + h - 7) if where == "lower-left" else (x + w * 0.78, y + h * 0.72)
    return shot.getpixel((round(px), round(py)))[:3]


def near(rgb, hexc, tol=6):
    ref = tuple(int(hexc[i:i + 2], 16) for i in (1, 3, 5))
    return all(abs(a - b) <= tol for a, b in zip(rgb, ref))


# ---------------- run ----------------
def run(lang: str) -> int:
    L = LANGS[lang]
    url = f"{BASE}/{L['prefix']}tools/bstar-tree/index.html"
    print(f"=== {lang}: {url}")
    rows = []
    with sync_playwright() as p:
        b = p.chromium.launch(headless=not args.headed)
        pg = b.new_page(viewport={"width": 1400, "height": 3000})
        errors = []
        pg.on("console", lambda m: m.type == "error" and errors.append(m.text))
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.on("requestfailed", lambda r: errors.append(f"request failed {r.url}"))
        pg.on("request", lambda r: not r.url.startswith((BASE, "data:", "blob:")) and errors.append(f"external request: {r.url}"))
        pg.on("response", lambda r: r.status >= 400 and errors.append(f"HTTP {r.status}: {r.url}"))
        pg.goto(url, wait_until="networkidle")
        pg.add_style_tag(content="html{scroll-behavior:auto!important}")
        pg.wait_for_selector("#bt-floor")
        rows.append(("page", f"html lang is {L['html_lang']}", pg.get_attribute("html", "lang") == L["html_lang"]))
        rows.append(("page", f"the Pack button says {L['pack']!r}", pg.inner_text("#bt-pack").strip() == L["pack"]))

        cids = pg.eval_on_selector_all("#lab-chal-sel option", "os => os.map(o => o.value)")
        rows.append(("page", "9 challenges in the menu", len(cids) == 9 and set(cids) == set(SOLVE)))
        rows.append(("page", "Check is off until Start (page load)", pg.is_disabled("#lab-chal-check")))

        for cid in cids:
            start(pg, cid)
            SOLVE[cid](pg)
            rows.append((cid, "positive", check(pg)))
            for name, act in negatives(cid).items():
                start(pg, cid)
                act(pg)
                rows.append((cid, f"negative: {name}", not check(pg)))
        # the status word of a pass is in the page language (the cases above read the class, which is the same in both)
        start(pg, "chain-turn")
        SOLVE["chain-turn"](pg)
        passed = check(pg)
        rows.append(("chain-turn", f"status word is {L['status_pass']!r}", passed and pg.inner_text("#lab-status").strip() == L["status_pass"]))
        # a failed Check explains itself, under the language's own "Check:" heading
        start(pg, "chain-turn")
        failed = not check(pg)
        rows.append(("chain-turn", f"failed Check line starts with {L['check_head']!r}", failed and pg.inner_text("#bt-why").strip().startswith(L["check_head"])))
        # predict: a guess typed after the tree was packed does not count
        start(pg, "predict-dy")
        seq(pack, lambda pg: guess(pg, 4), pack)(pg)
        rows.append(("predict-dy", "negative: guess after Pack", not check(pg)))
        # a wrong guess: the Check line explains, but never gives the number (D.y = 4)
        start(pg, "predict-dy")
        WRONG["predict-dy"](pg)
        failed = not check(pg)
        why = pg.inner_text("#bt-why")
        rows.append(("predict-dy", f"wrong-guess Check line has no number ({why.strip()[:60]}...)", failed and not any(c.isdigit() for c in why.replace(L["check_head"], ""))))
        # the cleared counter moved for every positive case
        prog = pg.inner_text(".chal-progress")
        rows.append(("page", f"progress shows 9 cleared ({prog.strip()})", prog.strip().startswith(L["progress"])))

        # ---------------- no text of the other language (messages, tables, legends, Check lines) ----------------
        pg.click("#lab-starter")
        swap(pg, "A", "C")
        move_msgs = []
        for act in (lambda pg: turn(pg, "D"), lambda pg: move(pg, "A", "B", "left"), pack):  # a message of each kind
            act(pg)
            move_msgs.append(pg.inner_text("#lab-root"))
        text = "\n".join(move_msgs) + pg.inner_text("body")
        left = [w for w in L["leftover"] if w in text]
        rows.append(("page", "no leftover text of the other language" if lang == "fr" else "English page keeps its English text",
                     (not left) if lang == "fr" else ("Pack" in text and "next door" in text)))
        if left:
            print("  leftover:", left)

        # ---------------- colours ----------------
        pg.click("#lab-starter")  # golden tree, packed
        pg.wait_for_selector("#bt-floor .bt-block")
        rows.append(("colour", "the shared canvas (index colours) is hidden", not pg.is_visible("#lab-root canvas")))
        shot = Image.open(io.BytesIO(pg.screenshot())).convert("RGB")
        for i in "ABCDE":
            fill = pg.get_attribute(f"#bt-tree g.bt-node[data-id={i}] circle", "fill")
            rgb = pixel_rgb(pg, shot, f"#bt-tree g.bt-node[data-id={i}] circle", "node")
            rows.append(("colour", f"tree node {i} is {COLORS[i]} (attribute and pixel {rgb})", fill == COLORS[i] and near(rgb, COLORS[i])))
        for i in "ABCDE":
            rgb = pixel_rgb(pg, shot, f"#bt-floor g.bt-block[data-id={i}] rect", "lower-left")
            rows.append(("colour", f"floor block {i} is {COLORS[i]} (pixel {rgb})", near(rgb, COLORS[i])))
        # a partial tree: only B and D are packed; index colours would paint B blue and D teal
        clear(pg)
        parent(pg, "B", "root")
        parent(pg, "D", "B")
        side(pg, "D", "right")
        pack(pg)
        shot = Image.open(io.BytesIO(pg.screenshot())).convert("RGB")
        n_blocks = pg.eval_on_selector_all("#bt-floor g.bt-block", "gs => gs.length")
        for i in "BD":
            rgb = pixel_rgb(pg, shot, f"#bt-floor g.bt-block[data-id={i}] rect", "lower-left")
            rows.append(("colour", f"partial pack (B, D only): {i} keeps {COLORS[i]} (pixel {rgb})", n_blocks == 2 and near(rgb, COLORS[i])))
        # after a swap the colours follow the names: C now sits in the corner, so the corner is amber
        preset("golden")(pg)
        swap(pg, "A", "C")
        pack(pg)
        shot = Image.open(io.BytesIO(pg.screenshot())).convert("RGB")
        corner = pg.evaluate("""() => {
            const g = [...document.querySelectorAll('#bt-floor g.bt-block')].find(g => g.querySelector('title').textContent.includes('(0,0)'));
            return g.dataset.id; }""")
        rgb = pixel_rgb(pg, shot, f"#bt-floor g.bt-block[data-id={corner}] rect", "lower-left")
        rows.append(("colour", f"after swap A,C the block at (0,0) is C, amber (pixel {rgb})", corner == "C" and near(rgb, COLORS["C"])))
        # left link solid, right link dashed
        dash = pg.eval_on_selector_all("#bt-tree line.bt-link", "ls => ls.map(l => [l.classList.contains('bt-link-right'), l.getAttribute('stroke-dasharray')])")
        rows.append(("colour", "tree links: left solid, right dashed", bool(dash) and all((d != "none") == r for r, d in dash)))

        rows.append(("page", "no console error, failed request, HTTP error or external request", not errors))
        b.close()

    fails = 0
    pos = sum(1 for _, n, _ in rows if n == "positive")
    neg = sum(1 for _, n, _ in rows if n.startswith("negative"))
    col = sum(1 for c, _, _ in rows if c == "colour")
    for cid, name, good in rows:
        print(f"{'ok  ' if good else 'FAIL'}  {cid:<13} {name}")
        fails += not good
    if errors:
        print("errors:", errors[:5])
    print(f"[{lang}] {len(rows) - fails} ok, {fails} FAIL  ({pos} positive, {neg} negative, {col} colour, "
          f"{len(rows) - pos - neg - col} page)\n")
    return 1 if fails else 0


langs = ["en", "fr"] if args.lang == "both" else [args.lang]
sys.exit(max(run(x) for x in langs))
