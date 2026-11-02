# Storyboard format (one JSON file per part, both languages)

The stage is a 960 × 540 drawing (16:9). Positions of nodes and camera shots use those units; overlay positions
use % of the stage (`x`, `y` = top-left corner). Copy `examples/lab03-part1/storyboard.json` and edit it.

## Times: anchors and references
Every `at`, `from`, `to` is a **time reference**:

| Reference | Meaning |
|---|---|
| `"@name"` | the word of anchor `name` (defined in `anchors`), in the page's language |
| `"@name+0.4"`, `"@name-0.3"` | shifted by seconds |
| `"slide:4"` / `"slide:4:end"` | start of the first / end of the last sentence of transcript slide 4 |
| `"start"`, `"end"` (`"start+0.2"`) | start / end of the part's audio |
| a number | seconds (avoid: breaks when the voice changes) |

```json
"anchors": {
  "sixteen":   { "slide": 1, "en": "sixteen", "fr": "seize" },
  "threeCuts": { "slide": 1, "en": "three#1", "fr": "trois#1" },
  "two":       { "slide": 4, "en": "two plus", "fr": "deux plus" },
  "edge":      { "slide": 3, "en": "edge", "fr": "arête", "edge": "end" }
}
```
- A word matches when it **starts with** the anchor (case and accents ignored; `l'équilibre` matches `équilibre`).
- `"three#1"` = the second "three" of that slide (counting from 0). Several words = consecutive words (`"two plus"`).
- `"edge": "end"` anchors the end of the word instead of its start; `"shift": 0.3` adds seconds.
- Anchors are searched only inside their slide. A missing word is an **error** in the checker, with the slide's
  words listed, so fix the anchor rather than guessing.
- Pick words that are **said when the thing should happen**: the noun or number that the picture shows.

## Graph, poses, splits, cameras
```json
"graph":  { "nodes": ["A","B","C","D","E"], "edges": [["A","B",5], ["A","C",1]], "groups": 2, "cap": 3 },
"poses":  { "base": { "A": [280,230], "B": [553,195] }, "split": { } },
"splits": { "good": "ABC|DE" },
"cameras": { "wires": [416, 262, 540] },
"divider": { "x": 570 }, "chip": { "x": 175, "y": 120, "w": 610, "h": 395 },
"thumbPose": "base", "freePose": "base", "goodCut": 3, "badCut": 9,
"widgets": { "counter": { "x": 81, "y": 68 }, "balance": { "x": 77, "y": 26 } }
```
- `splits` gives optional names (literal split strings work everywhere too). A camera is `[centre x, centre y, width]`;
  its height is width × 9/16. JSON has no comments: keep notes in the part's README.
- `cap` defaults to ceil(nodes / groups). A split is **legal** when every node is placed and each group has 1..cap nodes.
- A split string lists groups separated by `|` (`"ABC|DE"`, `"ABCDE"` = one group, `"none"` = nothing placed).
  Multi-letter names: separate with commas (`"n1,n2|n3"`).
- Colours never depend on group numbers: the group holding the alphabetically first node is blue, then green,
  amber, rose (same rule as the lab and its figures).
- Keep every pose 30 px inside the stage (the builder refuses otherwise). Leave the top 25 % free for headlines
  and the right 20 % for the counter or balance when they show. For a two-side split, put group 0 left of the divider.
- Camera shots are clamped to the stage; width 520–600 is a gentle zoom.

## Timeline: what changes, on which word
```json
"initial": { "pose": "base", "split": "none", "camera": "full", "shape": "node", "wires": false, "dim": 1 },
"timeline": [
  { "at": "@first",   "pose": "split", "split": "ABC|DE" },
  { "at": "slide:2",  "shape": "cell", "wires": true },
  { "at": "@many",    "camera": "wires" },
  { "at": "@several", "dim": 0.12 }
]
```
| Key | Values | Move time |
|---|---|---|
| `pose` | a pose name: nodes glide to it | 1.1 s |
| `split` | split string or name: colours change, the counter counts to the new cut | 1.2 s (count) |
| `camera` | shot name or `"full"` | 1.3 s |
| `shape` | `"cell"` (chip rectangles) or `"node"` (dots) | 0.9 s |
| `wires` | `true`: each edge drawn as w copper wires; `false`: one line | 1.0 s |
| `dim` | graph opacity (0.12 when a card covers it) | 0.6 s |

A new key starts from wherever the previous move had got to, so motion never jumps. But two keys of one track
closer than its move time make a rushed move; the checker warns. Fix: add a pause after the sentence
(`pauses`) or anchor the second key to a later word.

## Show windows (things on for a while)
```json
"show": [
  { "show": "cut", "from": "@cut", "to": "@need" },
  { "show": "heavy", "from": "@heaviest", "to": "slide:4", "edges": ["A-B", "D-E"] },
  { "show": "labels", "from": "@five", "to": "end", "stagger": 0.3 }
]
```
`weights` (edge numbers), `labels` (node letters; if any `labels` window exists, letters show only inside one;
`stagger` pops them one by one), `chip` (chip outline), `divider` (dashed line + tinted halves), `cut` (cut edges
red and dashed), `heavy` / `pulse` / `flash` (edge highlights; `edges` lists them, several windows can overlap),
`counter` (live cutsize), `balance` (bars per group), `cap` (the max line on the bars).

## Overlays (text on the stage)
Each: `{ "from", "to", "x", "y", "type", ... }`. Text fields are `{ "en": "...", "fr": "..." }`.

| type | fields | use |
|---|---|---|
| `headline` | `text`, `sub`, `size` (cqw, default 4.3) | the idea of the moment, top-left |
| `term` | `text` (the term, capitalised), `sub` (plain definition) | first time a word appears |
| `chip` | `text` | short labels that pile up (method names) |
| `tag` | `text` | one fact next to the picture |
| `tags` | `items: [{ text, at? }]` | 2–3 facts appearing one by one |
| `label` | `text`, `color` 0–3 | coloured caption over a group ("Team 1") |
| `vocab` | `items: [{ k, text, at }]` | a growing glossary |
| `eq` | `text` | an equation built term by term |
| `stamp` | `text` | a verdict ("useless") |
| `bigq` | `text` | a big "?" with a sentence; dim the graph |
| `compare` | `rows: [{ tone: "bad"/"good", label, value, note }]` | two outcomes side by side; dim the graph |
| `thumbs` | `items: [{ split, best?, bestLabel? }]` | small graphs with their cuts (computed) |
| `question` | (uses `question`) | the pause-and-guess card |
| `html` | `html` | escape hatch; avoid |

Inline markup inside any text:
- `{piece@name}` makes `piece` appear when anchor `name` is said (also `{piece@slide:3}`).
- `**accent**` gives blue bold, `!!red!!` gives red, and `##5##` marks a number.

## Question, bench, chapters, claims, pauses
```json
"question": { "at": "slide:6:end+0.5", "text": {...}, "hint": {...},
              "options": [ { "label": {...}, "reply": {...} } ] },
"bench": { "deal": true, "seed": 3 },
"chapters": [ { "at": "start", "title": {...} } ],
"claims": [ { "split": "ACE|BD", "cut": 16, "legal": true }, { "deal": 3, "split": "ACE|BD" } ],
"pausing": { "between": 0.55, "scene": 0.9, "question": 1.3, "tail": 2.0 },
"pauses": [ { "after": "@sixteen", "sec": 1.3 }, { "after": "slide:2:end", "sec": 1.5 } ]
```
- The player **stops at `question.at`** and waits for an answer on the stage, then plays the rest.
- `bench.deal` adds the "deal a random split with seed" box. It uses the course's mulberry32 dealer, only for
  two-group partition labs.
- `claims` are checked against the rules. Put every number the narration or the texts say here.
- `pauses` override the silence after the sentence holding an anchor (see `voice-and-pacing.md`).

Page text: `pageTitle`, `eyebrow`, `title`, `lede`, `note` (all `{en, fr}`).

---

# Floorplan scene (`"scene": "floorplan"`, Lab 05 B*-tree and other floorplanning labs)

Everything above (anchors, time references, camera, dim, show windows, overlays, question, chapters, pauses) works
the same. What changes is the picture: a **B*-tree** on the left and the **floor** it packs on the right.
Worked example: `examples/lab05-floorplan-demo/` (EN + FR, 0 errors, 0 warnings).

## The rule the engine uses (the course's packBstar, written down in Lab 05)
Walk the tree in preorder: the node, then its whole left subtree, then its right child. The root sits at (0, 0).
A **left child goes next door**: x = parent.x + parent.w. A **right child goes upstairs**: x = parent.x.
Each block falls until it touches the **skyline** (the highest top under its width); the skyline rises to its top.
A turned block swaps its w and h. The engine recomputes every tree, so a wrong number fails the check.

## Data: build with the lab checker's JSON
```bash
python3 build_lesson.py ... --data <module>/examples/bstar-check.json    # bstar_check.py --json > that file
```
It gives the outline, the blocks, the colours (one per block id, the course's paper palette) and **every scene of
the checker as a named tree** (`golden`, `lift`, `swap_start`, `rotate_after`, `best`, ...). The engine re-packs
each one and reports an error if it disagrees with the checker (check_lesson prints "11 tree(s) ... all equal").
Without `--data`, give `floorplan.modules`, `floorplan.outline` and `floorplan.trees` yourself.

```json
"scene": "floorplan",
"floorplan": {
  "start": "golden",
  "trees": { "mine": "A(B(C,-),D)", "chainTurned": { "tree": "rotate_start", "rotated": ["D"] } },
  "labels": { "nextDoor": { "en": "next door", "fr": "à côté" }, "upstairs": { "en": "upstairs", "fr": "à l'étage" } },
  "claims": [ { "tree": "lift", "pos": { "D": [0, 3] }, "bbox": [9, 4], "area": 36, "wasted": 13, "legal": true } ],
  "treeBox": [20, 150, 370, 360], "gridBox": [430, 150, 506, 356], "extent": [12, 8]
}
```
- Tree strings: `name(left,right)`, `-` = empty slot, a leaf is just its name (`"A(B(C(E,-),-),D)"`).
  A named tree can also be `{ "tree": <string or name>, "rotated": ["D"] }`.
- `claims`: `tree` (+ `rotated`), and any of `walk` ("ABCED"), `pos` ({id: [x, y]}), `xD`/`yD`/`wD`/`hD`,
  `bbox` ([w, h]), `area`, `wasted` (bounding-box squares not covered), `legal` (fits the outline).
  Put **every number the narration or a text says** here.
- `treeBox`, `gridBox`: where the two drawings sit (stage units). The defaults leave the top band (y < 150) for the
  headline, the counter and the legal badge. `extent`: make the floor wide enough for a tree the learner may build.
  By default it fits the outline and every tree of the timeline.

## Timeline keys
```json
"initial": { "tree": "golden", "placed": 0, "panel": "tree" },
"timeline": [
  { "at": "@corner", "panel": "both", "placed": 1 },
  { "at": "@follow", "placed": 4 },
  { "at": "@swap",  "tree": "lift" },
  { "at": "@turn",  "tree": "rotate_after" }
]
```
| Key | Values | What you see | Move time |
|---|---|---|---|
| `tree` | a named tree or a tree string | names travel in the tree, blocks glide to their new places, a turned block rotates 90° | 1.2 s |
| `placed` | 0..n, `"all"`, `"none"`, or a block name (= up to and including it) | blocks counted in **walk order**: each flies out of its tree node, then falls onto the skyline; a jump of several drops them 0.55 s apart; a lower number removes blocks at once | 1.0 s per block |
| `panel` | `"both"`, `"tree"`, `"grid"`, `"none"` | fades the other drawing to 22 % (talk about one side) | 0.6 s |
| `camera`, `dim` | as above | zoom: frame the floor, e.g. `[702, 330, 556]` | 1.3 s / 0.6 s |

Tree nodes are **hollow** until their block is picked up, then filled with the block's colour. To make a block
fall again onto the skyline (Lab 05 part 3), lower `placed` at a scene change, then raise it on the word.

## Show windows (floorplan)
| show | extra fields | what |
|---|---|---|
| `skyline` | | the amber skyline of the blocks that have landed |
| `bbox` | | dashed bounding box with "w × h = area" (the label waits until the blocks stop moving) |
| `wasted` | | hatches the bounding box: the holes show the wasted squares |
| `walk` | `stagger` | walk-order badges ①..⑤ on the tree nodes, one after the other |
| `links` | `ids` (children) | "next door" / "upstairs" labels on the tree links (texts from `floorplan.labels`) |
| `coords` | `ids` | (x, y) at each block's lower-left corner |
| `dims` | | "3×2" inside each block |
| `highlight` | `ids` | a dark ring on the node and a dark outline on the block (several windows can overlap) |
| `counter` | `metric`, `label`, `good`, `bad` | one counter, top right. `metric`: `area` (default), `width`, `height`, `wasted`, `placed`, `x:D`, `y:D`. Green when ≤ `good`, red when ≥ `bad`. It counts in whole numbers while blocks move |
| `legal` | | badge "fits the 10 × 8 outline" / "sticks out" (the zone outside the outline is hatched red by itself whenever a block sticks out) |

Widget positions: `"widgets": { "counter": { "x": 80, "y": 3 }, "legal": { "x": 46, "y": 21.5 } }` (% of the stage).

## Overlays
All overlay types work. `thumbs` items are trees: `{ "tree": "golden" }`, `{ "tree": "best", "best": "@best",
"bestLabel": {...} }`; the caption is "w × h = area" unless `label` is given. Put thumbs or a question card over the
tree panel and set `"panel": "grid"` (or the reverse).

## Try it yourself (bench)
`"bench": { "ops": ["swap", "turn", "move"] }` (default: all three). Clicking a block (on the floor or in the tree)
pauses the lesson and starts "Your tree" from the tree on screen, with every block placed:
- **Swap two**: click two blocks, their names trade places in the tree (shapes travel with the names).
- **Turn one**: click a block, it turns 90°.
- **Move a leaf**: click a block with no child, then the block it should hang from (its left slot if free, else
  its right slot).
The readout gives the tree, the bounding box, the wasted squares and whether it fits; "Start again" goes back
to the lesson's tree. These are the Lab 05 moves (`bstar_check.py`: swap, rotate, move_leaf).

## Checks
`check_lesson.py` works unchanged. Tree nodes and the centre of each block count as "nodes": text must not cover
them. It also prints how many checker trees the engine re-packed (all must be equal).

## Before the voice exists: draft timing
`scripts/draft_timing.py` makes a silent audio and estimated word times from the transcript, with the same
pauses, so a storyboard can be written and checked right after the script (Stage 3), long before the voices.
