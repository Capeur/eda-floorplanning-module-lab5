/**
 * Every word the B*-tree lab shows (Lab 05), in one place. Stage 5 (French site) replaces these
 * English snippets one by one, so keep each string literal on one line and unique in this file.
 * Block names (A-E), challenge ids, codes and numbers stay as they are.
 * Vocabulary: next door = left child, upstairs = right child, skyline, bounding box, wasted squares, turn.
 */
export const T = {
  // ---------------- page chrome ----------------
  panelLeft: "Tree and floorplan",
  panelRight: "Edit the tree",
  starterButton: "Reset workspace",
  idlePrompt: "Pick a challenge and click <strong>Start</strong>. Edit the tree, press <strong>Pack</strong>, then <strong>Check</strong>. The reveal is for study: it never counts.",
  starterHtml: `<p><strong>Your workspace:</strong> the tree on the left is a recipe for the floorplan next to it.
    Choose where each block hangs (its parent, and next door or upstairs), swap two names, turn a block, move a leaf,
    then press <strong>Pack</strong> to drop the blocks onto the skyline. Challenges check the tree <em>you</em> built
    and packed: a change after Pack needs a new Pack, and the study reveal never counts.</p>`,

  // ---------------- tree view ----------------
  treeCaption: "The tree",
  treeLegendLeft: "solid line = next door (left child)",
  treeLegendRight: "dashed line = upstairs (right child)",
  treeLegendWalk: "small number = walk order",
  treeEmpty: "Empty tree: choose a root in the table on the right.",
  loose: "not in the tree:",
  rootTag: "root",
  problems: {
    "no-root": () => "No root yet: one block must be the root.",
    "two-roots": (p) => `Two roots (${p.ids.join(", ")}): only one block can be the root.`,
    "slot-twice": (p) => `${p.ids.join(" and ")} both hang ${p.side === "left" ? "next door to" : "upstairs on"} ${p.parent}: one slot holds one block.`,
    "parent-out": (p) => `${p.id} hangs on ${p.parent}, but ${p.parent} is not in the tree.`,
    "cut-off": (p) => `${p.id} is not connected to the root.`,
  },

  // ---------------- floor view ----------------
  floorCaption: "The floorplan (outline 10 × 8)",
  floorLegendSky: "yellow line = skyline",
  floorLegendBox: "dashed box = bounding box",
  floorNotPacked: "Press Pack to drop the blocks.",
  floorStale: "The tree changed: press Pack again.",
  floorBad: "Fix the tree first (see the red lines).",
  bboxLabel: (bw, bh, area) => `${bw} × ${bh} = ${area}`,
  turnedMark: "↻",

  // ---------------- editor ----------------
  editorHelp: "For each block, choose its parent and its side. Then press Pack.",
  colBlock: "Block",
  colSize: "Size",
  colParent: "Parent",
  colSide: "Side",
  optNone: "— not in tree",
  optRoot: "root",
  optLeft: "next door (left)",
  optRight: "upstairs (right)",
  sizeOf: (w, h, turned) => `${w}×${h}${turned ? " ↻" : ""}`,
  ariaParent: (id) => `Parent of ${id}`,
  ariaSide: (id) => `Side of ${id}`,
  swapLabel: "Swap",
  swapWith: "with",
  swapBtn: "Swap names",
  turnLabel: "Turn",
  turnBtn: "Turn block",
  moveLabel: "Move leaf",
  moveTo: "to",
  moveBtn: "Move leaf",
  guessLabel: "Guess D.y before you pack:",
  guessBtn: "Save guess",
  guessAria: "Your guess for D.y",
  guessNone: "no guess saved",
  guessShown: (g) => `saved guess D.y = ${g.value}${g.blind ? " (made before packing this tree)" : " (made after this tree was packed: does not count)"}`,

  // ---------------- buttons above the workspace ----------------
  loadLabel: "Load a tree:",
  presets: {
    golden: "Golden",
    lift: "A and C swapped",
    order: "Walk-order tree",
    chain: "Long row",
    swap: "Bad tree (40)",
  },
  packBtn: "Pack",
  clearBtn: "Clear tree",
  revealBtn: "Reveal an answer (study)",

  // ---------------- numbers panel ----------------
  lines: {
    tree: (t) => `tree: ${t}`,
    walk: (w) => `walk order: ${w}`,
    turned: (r) => `turned: ${r.length ? r.join(", ") : "none"}`,
    positions: (p) => `positions: ${p}`,
    bbox: (bw, bh, area) => `bounding box: ${bw} × ${bh} = ${area}`,
    wasted: (w, blocks) => `wasted squares: ${w} (blocks cover ${blocks})`,
    legalYes: "legal: yes (inside the 10 × 8 outline)",
    legalNo: (ids) => `legal: no (${ids.join(", ")} sticks out of the outline)`,
    deadspace: (d) => `outline deadspace: 80 − 23 = ${d} (the same for every tree)`,
    notPacked: "pack: not packed yet",
    stale: "pack: out of date (the tree changed after Pack)",
    base: (b) => `made from: ${b}`,
    ops: (n, list) => `changes since then: ${n ? list : "none"}`,
    guess: (g) => `guess: ${g}`,
  },
  bases: {
    empty: "an empty tree (Clear)",
    golden: "the golden tree",
    lift: "the tree with A and C swapped",
    order: "the walk-order tree",
    chain: "the long row",
    swap: "the bad tree (40)",
    reveal: "the revealed answer (study: never counts)",
  },
  ops: {
    edit: (o) => `edit ${o.id}`,
    swap: (o) => `swap ${o.a},${o.b}`,
    turn: (o) => `turn ${o.id}`,
    move: (o) => `move ${o.leaf} to ${o.parent} ${o.side === "left" ? "next door" : "upstairs"}`,
    pack: () => "pack",
  },
  checkHead: "Check:",

  // ---------------- messages after an action ----------------
  msg: {
    edited: (m) => `${m.id} moved in the tree. Press Pack to see the new floorplan.`,
    "fix-tree": () => "Fix the tree first: every block in the tree needs a place, one block per slot.",
    "empty-tree": () => "The tree is empty: choose a root first.",
    "swap-same": () => "Pick two different blocks to swap.",
    "not-in-tree": (m) => `${m.id} is not in the tree.`,
    swapped: (m) => `Swapped the names ${m.a} and ${m.b}: the shape of the tree stayed the same.`,
    turned: (m) => `Turned ${m.id}: it is now ${m.w} wide and ${m.h} tall.`,
    "turned-back": (m) => `Turned ${m.id} back: ${m.w} wide and ${m.h} tall again.`,
    moved: (m) => `Moved leaf ${m.leaf} ${m.side === "left" ? "next door to" : "upstairs on"} ${m.parent}.`,
    "move-same": (m) => `${m.leaf} already hangs there: nothing changed.`,
    "move-root": (m) => `${m.leaf} is the root: only a leaf can move.`,
    "move-self": (m) => `${m.leaf} cannot hang on itself.`,
    "move-not-leaf": (m) => `${m.leaf} has children: only a leaf (a block with no children) can move.`,
    "move-missing": (m) => `${m.id} is not in the tree.`,
    "move-taken": (m) => `${m.parent} already has a block ${m.side === "left" ? "next door" : "upstairs"}.`,
    "bad-side": () => "Choose next door or upstairs.",
    packed: (m) => `Packed: bounding box ${m.bw} × ${m.bh} = ${m.area}, ${m.legal ? "legal" : "not legal"}.`,
    cleared: () => "Tree cleared: every block is out of the tree. Choose a root to start.",
    preset: (m) => `Loaded ${T.bases[m.name]}. Press Pack to see it.`,
    revealed: () => "An answer is revealed (study): it never counts. Clear the tree, load a tree or press Start to go on.",
    "guess-bad": () => "Type a whole number for D.y, for example 2.",
    "guess-saved": (m) => `Guess saved: D.y = ${m.value}. Now press Pack.`,
    "guess-late": (m) => `Guess saved (D.y = ${m.value}), but this tree was already packed: it does not count. Press Start to try again.`,
  },

  // ---------------- why a Check did not pass ----------------
  why: {
    pass: () => "PASS.",
    unknown: () => "Unknown challenge.",
    revealed: () => "This tree came from the study reveal: it never counts. Press Start (or Clear) and build it yourself.",
    "other-start": (w) => `Start from the tree this challenge loads${w.start === "empty" ? " (an empty tree)" : ""}: a tree loaded with another button does not count. Press Start again.`,
    "empty-tree": () => "The tree is empty.",
    "fix-tree": () => "The tree has a problem (see the red lines under it).",
    "not-packed": () => "Press Pack first: the check reads the packed floorplan.",
    stale: () => "The tree changed after Pack: press Pack again.",
    "not-all": (w) => `Put all five blocks in the tree (${w.ids.join(", ")} missing).`,
    "not-legal": (w) => `Not legal: ${w.ids.join(", ")} sticks out of the 10 × 8 outline.`,
    "no-turns": () => "No turned block for this one: turn it back.",
    "not-golden": () => "Not the golden tree yet: A is the root, B, C and E go next door one after the other, D goes upstairs on A.",
    "d-y": (w) => `D lands at y = ${w.y}, not 3.`,
    "tree-changed": () => "Keep the tree this challenge loads (press Start to get it back).",
    "no-guess": () => "Type your guess for D.y and press Save guess before you pack.",
    "guess-other": () => "Your guess was made for another tree: save a new guess, then pack.",
    "guess-late": () => "Your guess was saved after this tree was packed: it does not count. Press Start and guess first.",
    "guess-wrong": () => "Your guess is not where D lands. Look again at the blocks placed before D, then press Start and guess before you pack.",
    turns: (w) => `Turn exactly one block (now ${w.n}).`,
    "no-change": () => "The tree is unchanged.",
    "not-one-swap": () => "This tree is not one swap away from the bad tree. Press Start and use one swap.",
    "not-one-move": () => "This tree is not one leaf move away from the bad tree. Press Start and move one leaf.",
    area: (w) => `Bounding box ${w.bw} × ${w.bh} = ${w.area}: the target is ${w.target} or less.`,
    "not-below": (w) => `Bounding box ${w.bw} × ${w.bh} = ${w.area}: beat 27 (less than 27).`,
  },

  // ---------------- challenges ----------------
  challenges: {
    "build-golden": {
      title: "Build the golden tree",
      prompt: "Start gives an empty tree. Build the golden tree yourself with the Parent and Side menus: A is the root, B is next door to A, C next door to B, E next door to C, and D upstairs on A. Then Pack and Check.",
      hint: "Set A's parent to root first. Then B: parent A, next door. C: parent B, next door. E: parent C, next door. D: parent A, upstairs.",
    },
    "d-at-3": {
      title: "Lift D to y = 3",
      prompt: "Start loads the golden tree, where D lands at y = 2. Change the tree so that D lands at y = 3, with all five blocks inside the outline.",
      hint: "D is upstairs on the root, three squares wide. Which block is three tall? Put it under D's footprint (try swapping two names).",
    },
    "predict-dy": {
      title: "Predict D.y before packing",
      prompt: "Start loads the walk-order tree. Before you press Pack, type where D will land (its y) and press Save guess. Then Pack and Check.",
      // two hints in one (the shared chrome shows one hint text): a question first, then the fact that answers it
      hint: "1. Which blocks are placed before D? Count them in walk order. 2. E is placed before D, and part of E is under D.",
    },
    "chain-turn": {
      title: "Make the long row fit with one turn",
      prompt: "Start loads the long row: every block next door, 12 wide in a 10 wide outline. Keep the tree, turn exactly one block so the row fits, then Pack and Check.",
      hint: "The row is 3 + 2 + 2 + 3 + 2 = 12 wide. Which block becomes narrower when it is turned? It must save two squares.",
    },
    "fix-swap": {
      title: "Fix the bad tree. One swap is enough.",
      prompt: "Start loads a bad tree: bounding box 10 × 4 = 40. One swap of two names is enough to get a box of 27. Then Pack and Check.",
      hint: "E sits upstairs on A and makes the box 4 tall, while D sits at the end of the row. Which two names would trade places?",
    },
    "move-leaf": {
      title: "One leaf move is enough: 40 → 28.",
      prompt: "Start loads the same bad tree (40). One leaf move is enough: move a leaf (a block with no children) to a free slot so the bounding box drops to 28. Then Pack and Check.",
      hint: "D is a leaf at the end of the row and makes the box 10 wide. Hang it upstairs on a block in the middle of the row.",
    },
    "reach-27": {
      title: "From the long row to 27",
      prompt: "Start loads the long row (12 wide, not legal). Rebuild the tree any way you like until the floorplan is legal with a bounding box of 27 or less.",
      hint: "The golden tree gives 9 × 3 = 27: put one block upstairs instead of at the end of the row.",
    },
    "beat-27": {
      title: "Beat 27",
      prompt: "Start loads the golden tree (27). Find any tree with a bounding box smaller than 27, all five blocks inside the outline. Turning blocks is allowed.",
      hint: "Try a box 6 wide and 4 tall, or 5 wide and 5 tall. Put a low block (D) next door to A and stack other blocks upstairs.",
    },
    "reach-24": {
      title: "Reach 24 without turning",
      prompt: "Stretch: reach the smallest possible box, 24 squares, with no turned block. Only eight of the 5,040 trees do it.",
      hint: "Aim for 6 × 4. A at the root, D next door (D is only 1 tall). Then C upstairs on A, E next door to C, and B somewhere that the skyline lifts onto D.",
    },
  },
};
