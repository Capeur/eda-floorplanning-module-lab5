/**
 * B*-tree lab model (Lab 05): trees, the three operations, packing, the learner's state and the
 * challenge checks. Pure: no DOM, so tests/test_model_vs_checker.py runs it in Node against
 * courses/learn_floorplanning/module02-03-bstar-tree/examples/bstar_check.py.
 *
 * The rule (same as the checker): walk the tree in preorder (node, whole left subtree, right child);
 * root x = 0, left child x = parent.x + parent.w ("next door"), right child x = parent.x ("upstairs");
 * every block y = the highest skyline under [x, x + w). Packing itself is packBstar of the shared
 * floorplanning-core.js (read only); a turned block is a module list with its w and h exchanged.
 *
 * Messages and failure reasons are codes ({ code, ...args }); the UI turns them into words
 * (bstar-tree-strings.js), so this file holds no learner-facing text.
 */
import { OUTLINE, TINY_MODULES, packBstar } from "../../assets/floorplanning-core.js";

export { OUTLINE };
export const IDS = ["A", "B", "C", "D", "E"];
export const MODULES = TINY_MODULES.map(({ id, w, h }) => ({ id, w, h }));
/** One fixed colour per block id, everywhere (figures, deck, lab). Never pick a colour by index. */
export const COLORS = { A: "#1d4ed8", B: "#0f6b5c", C: "#b45309", D: "#7c3aed", E: "#be123c" };
export const SIDES = ["left", "right"];

/* ---------------- trees: text form ---------------- */

/** `A(B(C(E,-),-),D)` -> { id, left?, right? }. `-` is an empty child; a bare id is a leaf. */
export function parseTree(s) {
  let pos = 0;
  const ident = () => {
    const start = pos;
    while (pos < s.length && /[A-Za-z0-9_]/.test(s[pos])) pos++;
    if (start === pos) throw new Error(`expected a name at position ${pos} of ${s}`);
    return s.slice(start, pos);
  };
  const child = () => {
    if (s[pos] === "-") {
      pos++;
      return null;
    }
    return node();
  };
  const node = () => {
    const out = { id: ident() };
    if (s[pos] === "(") {
      pos++;
      const left = child();
      if (s[pos++] !== ",") throw new Error(`expected ',' in ${s}`);
      const right = child();
      if (s[pos++] !== ")") throw new Error(`expected ')' in ${s}`);
      if (left) out.left = left;
      if (right) out.right = right;
    }
    return out;
  };
  const t = node();
  if (pos !== s.length) throw new Error(`extra text in ${s}`);
  return t;
}

export function fmtTree(t) {
  if (!t) return "-";
  if (!t.left && !t.right) return t.id;
  return `${t.id}(${fmtTree(t.left)},${fmtTree(t.right)})`;
}

/** Walk order: the node, its whole left subtree, then its right child. */
export function preorder(t) {
  return t ? [t.id, ...preorder(t.left), ...preorder(t.right)] : [];
}

const clone = (t) => (t ? JSON.parse(JSON.stringify(t)) : null);

function findNode(t, id) {
  if (!t) return null;
  if (t.id === id) return t;
  return findNode(t.left, id) || findNode(t.right, id);
}

/* ---------------- the three operations (exactly as bstar_check.py) ---------------- */

/** New tree with the names a and b exchanged; the shape stays. */
export function swap(tree, a, b) {
  const t = clone(tree);
  (function walk(n) {
    if (!n) return;
    if (n.id === a) n.id = b;
    else if (n.id === b) n.id = a;
    walk(n.left);
    walk(n.right);
  })(t);
  return t;
}

/** New module list where block id is turned 90 degrees (w and h exchanged). The tree does not change. */
export function rotate(modules, id) {
  return modules.map((m) => (m.id === id ? { ...m, w: m.h, h: m.w } : { ...m }));
}

export function withRotated(modules, rotated) {
  return (rotated || []).reduce((mods, id) => rotate(mods, id), modules);
}

/** A refused operation: err.code says why (the UI words it). */
function refuse(code, args = {}) {
  const e = new Error(code);
  e.code = code;
  e.args = args;
  return e;
}

/**
 * New tree: cut `leaf` (no children, not the root) and hang it on parent's free `side` slot.
 * The slot is free after the cut. Throws (err.code) for the root, parent == leaf, a non-leaf,
 * a missing name or a taken slot, in the checker's order.
 */
export function moveLeaf(tree, leaf, parent, side) {
  if (!SIDES.includes(side)) throw refuse("bad-side");
  const t = clone(tree);
  if (t.id === leaf) throw refuse("move-root", { leaf });
  if (leaf === parent) throw refuse("move-self", { leaf });
  let cut = false;
  (function remove(n) {
    for (const s of SIDES) {
      const c = n[s];
      if (c && c.id === leaf) {
        if (c.left || c.right) throw refuse("move-not-leaf", { leaf });
        delete n[s];
        cut = true;
        return;
      }
      if (c) remove(c);
    }
  })(t);
  if (!cut) throw refuse("move-missing", { id: leaf });
  const attach = (n) => {
    if (n.id === parent) {
      if (n[side]) throw refuse("move-taken", { parent, side });
      n[side] = { id: leaf };
      return true;
    }
    return SIDES.some((s) => n[s] && attach(n[s]));
  };
  if (!attach(t)) throw refuse("move-missing", { id: parent });
  return t;
}

/** Every single leaf move [leaf, parent, side] that changes the tree, in the checker's order. */
export function leafMoves(tree) {
  const out = [];
  const ids = preorder(tree);
  const leaves = ids.filter((i) => {
    const n = findNode(tree, i);
    return !n.left && !n.right;
  });
  for (const leaf of [...leaves].sort()) {
    if (leaf === tree.id) continue;
    for (const parent of [...ids].sort()) {
      for (const side of SIDES) {
        let t;
        try {
          t = moveLeaf(tree, leaf, parent, side);
        } catch {
          continue;
        }
        if (fmtTree(t) !== fmtTree(tree)) out.push([leaf, parent, side]);
      }
    }
  }
  return out;
}

/** Every labelled binary tree using each id once (5 ids: 5040), in the checker's order. */
export function* allTrees(ids) {
  ids = [...ids].sort();
  if (!ids.length) {
    yield null;
    return;
  }
  for (const r of ids) {
    const rest = ids.filter((i) => i !== r);
    for (let k = 0; k <= rest.length; k++) {
      for (const leftIds of combinations(rest, k)) {
        const rightIds = rest.filter((i) => !leftIds.includes(i));
        for (const lt of allTrees(leftIds)) {
          for (const rt of allTrees(rightIds)) {
            const n = { id: r };
            if (lt) n.left = lt;
            if (rt) n.right = rt;
            yield n;
          }
        }
      }
    }
  }
}

function* combinations(arr, k, start = 0, pre = []) {
  if (pre.length === k) {
    yield pre;
    return;
  }
  for (let i = start; i < arr.length; i++) yield* combinations(arr, k, i + 1, [...pre, arr[i]]);
}

/* ---------------- packing and score ---------------- */

/** packBstar of the shared core, with the turned blocks' w and h exchanged first. */
export function packTree(tree, rotated = []) {
  if (!tree) return {};
  return packBstar(tree, withRotated(MODULES, rotated));
}

export function boundingBox(pack) {
  const rs = Object.values(pack);
  if (!rs.length) return [0, 0];
  return [Math.max(...rs.map((r) => r.x + r.w)), Math.max(...rs.map((r) => r.y + r.h))];
}

/** { legal, outside: ids sticking out, overlaps: [a, b] pairs }. Touching edges is not an overlap. */
export function legality(pack, outline = OUTLINE) {
  const ids = Object.keys(pack).sort();
  const outside = ids.filter((i) => {
    const r = pack[i];
    return r.x < 0 || r.y < 0 || r.x + r.w > outline.w || r.y + r.h > outline.h;
  });
  const overlaps = [];
  for (let i = 0; i < ids.length; i++) {
    for (let j = i + 1; j < ids.length; j++) {
      const p = pack[ids[i]];
      const q = pack[ids[j]];
      if (!(p.x + p.w <= q.x || q.x + q.w <= p.x || p.y + p.h <= q.y || q.y + q.h <= p.y)) overlaps.push([ids[i], ids[j]]);
    }
  }
  return { legal: !outside.length && !overlaps.length, outside, overlaps };
}

export function score(pack, outline = OUTLINE) {
  const [bw, bh] = boundingBox(pack);
  const blocks = Object.values(pack).reduce((s, r) => s + r.w * r.h, 0);
  const leg = legality(pack, outline);
  return { bbox: [bw, bh], area: bw * bh, blocks, wasted: bw * bh - blocks, ...leg };
}

/** Final skyline as merged [x1, x2, height] segments over [0, widest x). */
export function skyline(pack) {
  const [bw] = boundingBox(pack);
  const out = [];
  for (let x = 0; x < bw; x++) {
    let top = 0;
    for (const r of Object.values(pack)) if (x >= r.x && x < r.x + r.w) top = Math.max(top, r.y + r.h);
    const last = out[out.length - 1];
    if (last && last[2] === top && last[1] === x) last[1] = x + 1;
    else out.push([x, x + 1, top]);
  }
  return out;
}

/** Outline deadspace W*H - block areas: the same for every tree (57 here). */
export const OUTLINE_DEADSPACE = OUTLINE.w * OUTLINE.h - MODULES.reduce((s, m) => s + m.w * m.h, 0);

/* ---------------- example trees ---------------- */

/** Text forms of the module's example trees (examples/*.json; the Node test checks they match). */
export const TREES = {
  golden: "A(B(C(E,-),-),D)",
  lift: "C(B(A(E,-),-),D)",
  order: "A(B(C(-,E),D),-)",
  chain: "A(B(C(D(E,-),-),-),-)",
  swap: "A(B(C(D,-),-),E)",
  moved: "A(B(C,D),E)",
  best: "A(D,C(E(B,-),-))",
};
/** Trees the learner can load with a button (bases). "empty" is the Clear button. */
export const PRESETS = ["golden", "lift", "order", "chain", "swap"];

/* ---------------- the learner's state ---------------- */
//
// place[id] = { parent: null | "root" | <id>, side: "left" | "right" }   (parent null = not in the tree)
// rotated   = sorted ids of turned blocks
// base      = what the tree was loaded from: "empty" (Clear), a preset name, or "reveal" (study)
// packed    = { sig, pack } of the last Pack; its sig becomes null as soon as the tree or a turn changes
// seen      = signatures packed (or revealed) since the challenge started: a guess on one of them is not blind
// guess     = { value, sig, blind } for "predict D.y"
// ops       = what the learner did since the base was loaded ({ kind, ... }), shown in the panel

function emptyPlace() {
  return Object.fromEntries(IDS.map((i) => [i, { parent: null, side: "left" }]));
}

export function placeFromTree(tree) {
  const place = emptyPlace();
  (function walk(n, parent, side) {
    if (!n) return;
    place[n.id] = { parent, side };
    walk(n.left, n.id, "left");
    walk(n.right, n.id, "right");
  })(tree, "root", "left");
  return place;
}

/**
 * Read the placement as a tree. Returns { tree, problems, loose }:
 * tree is built from the root (for an invalid placement: the part that can be drawn, first name wins a slot),
 * problems = [{ code, ... }], loose = ids not in the drawn tree.
 */
export function readTree(place) {
  const problems = [];
  const inTree = IDS.filter((i) => place[i].parent != null);
  const roots = inTree.filter((i) => place[i].parent === "root");
  if (inTree.length && !roots.length) problems.push({ code: "no-root" });
  if (roots.length > 1) problems.push({ code: "two-roots", ids: roots });
  for (const p of IDS) {
    for (const side of SIDES) {
      const kids = inTree.filter((i) => place[i].parent === p && place[i].side === side);
      if (kids.length > 1) problems.push({ code: "slot-twice", parent: p, side, ids: kids });
    }
  }
  let tree = null;
  const reached = new Set();
  if (roots.length) {
    const build = (id) => {
      reached.add(id);
      const n = { id };
      for (const side of SIDES) {
        const k = inTree.find((i) => place[i].parent === id && place[i].side === side && !reached.has(i));
        if (k) n[side] = build(k);
      }
      return n;
    };
    tree = build(roots[0]);
  }
  for (const i of inTree) {
    if (reached.has(i) || place[i].parent === "root") continue;
    const p = place[i].parent;
    if (place[p].parent == null) problems.push({ code: "parent-out", id: i, parent: p });
    else if (!problems.some((q) => q.code === "slot-twice" && q.ids.includes(i))) problems.push({ code: "cut-off", id: i });
  }
  return { tree, problems, loose: IDS.filter((i) => !reached.has(i)) };
}

/** Signature of the current tree + turns, or null when the placement is not a valid tree. */
export function sigOf(state) {
  const { tree, problems } = readTree(state.place);
  if (problems.length || !tree) return null;
  return `${fmtTree(tree)}|${state.rotated.join(",")}`;
}

export function currentTree(state) {
  const r = readTree(state.place);
  return r.problems.length ? null : r.tree;
}

/** The pack on screen: only when Pack was pressed after the last change. */
export function currentPack(state) {
  const sig = sigOf(state);
  return state.packed && sig && state.packed.sig === sig ? state.packed.pack : null;
}

export function createState(base = "golden", { pack = false } = {}) {
  let s = {
    place: base === "empty" ? emptyPlace() : placeFromTree(parseTree(TREES[base])),
    rotated: [],
    base,
    packed: null,
    seen: [],
    guess: null,
    ops: [],
  };
  if (pack) s = doPack(s).state;
  return s;
}

const msg = (code, args = {}) => ({ code, ...args });

/**
 * Every change of the tree or of a turn: the last Pack no longer counts, even if a second change
 * gives the same tree back (its sig is wiped, so only a new Pack makes it current again).
 */
function changed(s, op, patch) {
  return { ...s, ...patch, packed: s.packed ? { ...s.packed, sig: null } : null, ops: [...s.ops, op] };
}

/** Set where block id hangs: "" (not in the tree), "root" or a parent id. Keeps the side if that slot is free. */
export function setParent(s, id, parent) {
  parent = parent || null;
  if (parent === id) return { state: s, msg: msg("move-self", { leaf: id }) };
  const old = s.place[id];
  if (old.parent === parent) return { state: s, msg: null };
  let side = old.side;
  if (parent && parent !== "root") {
    const taken = (sd) => IDS.some((i) => i !== id && s.place[i].parent === parent && s.place[i].side === sd);
    if (taken(side) && !taken(side === "left" ? "right" : "left")) side = side === "left" ? "right" : "left";
  }
  const place = { ...s.place, [id]: { parent, side } };
  return { state: changed(s, { kind: "edit", id }, { place }), msg: msg("edited", { id }) };
}

export function setSide(s, id, side) {
  if (!SIDES.includes(side) || s.place[id].side === side) return { state: s, msg: null };
  const place = { ...s.place, [id]: { ...s.place[id], side } };
  return { state: changed(s, { kind: "edit", id }, { place }), msg: msg("edited", { id }) };
}

function needTree(s) {
  const r = readTree(s.place);
  if (r.problems.length) return { err: msg("fix-tree") };
  if (!r.tree) return { err: msg("empty-tree") };
  return { tree: r.tree };
}

export function doSwap(s, a, b) {
  if (a === b) return { state: s, msg: msg("swap-same") };
  const { tree, err } = needTree(s);
  if (err) return { state: s, msg: err };
  const ids = preorder(tree);
  const out = [a, b].find((i) => !ids.includes(i));
  if (out) return { state: s, msg: msg("not-in-tree", { id: out }) };
  const place = placeFromTree(swap(tree, a, b));
  return { state: changed(s, { kind: "swap", a, b }, { place }), msg: msg("swapped", { a, b }) };
}

/** Turn block id 90 degrees (a second turn turns it back). Works on any block. */
export function doTurn(s, id) {
  const on = s.rotated.includes(id);
  const rotated = on ? s.rotated.filter((i) => i !== id) : [...s.rotated, id].sort();
  const m = withRotated(MODULES, rotated).find((x) => x.id === id);
  return { state: changed(s, { kind: "turn", id }, { rotated }), msg: msg(on ? "turned-back" : "turned", { id, w: m.w, h: m.h }) };
}

export function doMove(s, leaf, parent, side) {
  const { tree, err } = needTree(s);
  if (err) return { state: s, msg: err };
  let t;
  try {
    t = moveLeaf(tree, leaf, parent, side);
  } catch (e) {
    return { state: s, msg: msg(e.code || "fix-tree", e.args || {}) };
  }
  if (fmtTree(t) === fmtTree(tree)) return { state: s, msg: msg("move-same", { leaf, parent, side }) };
  return { state: changed(s, { kind: "move", leaf, parent, side }, { place: placeFromTree(t) }), msg: msg("moved", { leaf, parent, side }) };
}

export function doPack(s) {
  const { tree, err } = needTree(s);
  if (err) return { state: s, msg: err };
  const sig = sigOf(s);
  const pack = packTree(tree, s.rotated);
  const seen = s.seen.includes(sig) ? s.seen : [...s.seen, sig];
  const sc = score(pack);
  return {
    state: { ...s, packed: { sig, pack }, seen, ops: [...s.ops, { kind: "pack" }] },
    msg: msg("packed", { bw: sc.bbox[0], bh: sc.bbox[1], area: sc.area, legal: sc.legal }),
  };
}

export function doClear(s) {
  return {
    state: { ...s, place: emptyPlace(), rotated: [], base: "empty", packed: null, guess: null, ops: [] },
    msg: msg("cleared"),
  };
}

export function doPreset(s, name) {
  return {
    state: { ...s, place: placeFromTree(parseTree(TREES[name])), rotated: [], base: name, packed: null, guess: null, ops: [] },
    msg: msg("preset", { name }),
  };
}

/** Study only: show an answer, packed. base "reveal" makes every challenge fail until Clear, a preset or Start. */
export function doReveal(s, challengeId) {
  const ans = ANSWERS[challengeId] || ANSWERS[""];
  const r = { ...s, place: placeFromTree(parseTree(TREES[ans.tree])), rotated: [...ans.rotated], base: "reveal", guess: null, ops: [] };
  const { state } = doPack(r);
  return { state: { ...state, ops: [] }, msg: msg("revealed") };
}

/** Save a typed guess for D.y. Blind = this tree had not been packed (or revealed) since the challenge started. */
export function saveGuess(s, text) {
  const t = String(text ?? "").trim();
  if (!/^-?\d+$/.test(t)) return { state: s, msg: msg("guess-bad") };
  const sig = sigOf(s);
  if (!sig) return { state: s, msg: msg("fix-tree") };
  if (!preorder(currentTree(s)).includes("D")) return { state: s, msg: msg("not-in-tree", { id: "D" }) };
  const blind = !s.seen.includes(sig);
  return { state: { ...s, guess: { value: Number(t), sig, blind } }, msg: msg(blind ? "guess-saved" : "guess-late", { value: Number(t) }) };
}

/* ---------------- challenges ---------------- */

/**
 * start: the tree Start loads (the base the work must come from). allowEmpty: building from an
 * empty tree (Clear) also counts. Titles, prompts and hints are in bstar-tree-strings.js.
 */
export const CHALLENGES = [
  { id: "build-golden", level: "Intro", start: "empty" },
  { id: "d-at-3", level: "Intro", start: "golden", allowEmpty: true },
  { id: "predict-dy", level: "Practice", start: "order" },
  { id: "chain-turn", level: "Practice", start: "chain" },
  { id: "fix-swap", level: "Practice", start: "swap" },
  { id: "move-leaf", level: "Practice", start: "swap" },
  { id: "reach-27", level: "Practice", start: "chain", allowEmpty: true },
  { id: "beat-27", level: "Stretch", start: "golden", allowEmpty: true },
  { id: "reach-24", level: "Stretch", start: "golden", allowEmpty: true },
];

/** What Reveal shows (study): one answer per challenge; "" = no challenge running. */
export const ANSWERS = {
  "": { tree: "golden", rotated: [] },
  "build-golden": { tree: "golden", rotated: [] },
  "d-at-3": { tree: "lift", rotated: [] },
  "predict-dy": { tree: "order", rotated: [] },
  "chain-turn": { tree: "chain", rotated: ["D"] },
  "fix-swap": { tree: "golden", rotated: [] },
  "move-leaf": { tree: "moved", rotated: [] },
  "reach-27": { tree: "golden", rotated: [] },
  "beat-27": { tree: "best", rotated: [] },
  "reach-24": { tree: "best", rotated: [] },
};

const SWAP_START = parseTree(TREES.swap);
const ONE_SWAP = new Set(
  IDS.flatMap((a, i) => IDS.slice(i + 1).map((b) => fmtTree(swap(SWAP_START, a, b))))
);
const ONE_MOVE = new Set(leafMoves(SWAP_START).map(([l, p, sd]) => fmtTree(moveLeaf(SWAP_START, l, p, sd))));

const no = (why, args = {}) => ({ ok: false, why, ...args });
const YES = { ok: true, why: "pass" };

/** Recomputed from the learner's tree on every Check. Returns { ok, why, ...args }. */
export function checkChallenge(id, s) {
  const ch = CHALLENGES.find((c) => c.id === id);
  if (!ch) return no("unknown");
  if (s.base === "reveal") return no("revealed");
  if (s.base !== ch.start && !(ch.allowEmpty && s.base === "empty")) return no("other-start", { start: ch.start });
  const r = readTree(s.place);
  if (!r.tree && !r.problems.length) return no("empty-tree");
  if (r.problems.length) return no("fix-tree");
  const pack = currentPack(s);
  if (!pack) return no(s.packed ? "stale" : "not-packed");
  const text = fmtTree(r.tree);
  const sc = score(pack);
  const all = r.loose.length === 0;
  const legalAll = () => (!all ? no("not-all", { ids: r.loose }) : !sc.legal ? no("not-legal", { ids: sc.outside }) : null);
  const area = (target) => no("area", { area: sc.area, bw: sc.bbox[0], bh: sc.bbox[1], target });

  switch (id) {
    case "build-golden":
      if (!all) return no("not-all", { ids: r.loose });
      if (s.rotated.length) return no("no-turns");
      return text === TREES.golden ? YES : no("not-golden");
    case "d-at-3":
      return legalAll() || (pack.D.y === 3 ? YES : no("d-y", { y: pack.D.y }));
    case "predict-dy":
      if (text !== TREES.order || s.rotated.length) return no("tree-changed");
      if (!s.guess) return no("no-guess");
      if (s.guess.sig !== sigOf(s)) return no("guess-other");
      if (!s.guess.blind) return no("guess-late");
      return s.guess.value === pack.D.y ? YES : no("guess-wrong"); // the reason never gives D.y away
    case "chain-turn":
      if (text !== TREES.chain) return no("tree-changed");
      if (s.rotated.length !== 1) return no("turns", { n: s.rotated.length });
      return sc.legal ? YES : no("not-legal", { ids: sc.outside });
    case "fix-swap":
      if (s.rotated.length) return no("no-turns");
      if (text === TREES.swap) return no("no-change");
      if (!ONE_SWAP.has(text)) return no("not-one-swap");
      return legalAll() || (sc.area <= 27 ? YES : area(27));
    case "move-leaf":
      if (s.rotated.length) return no("no-turns");
      if (text === TREES.swap) return no("no-change");
      if (!ONE_MOVE.has(text)) return no("not-one-move");
      return legalAll() || (sc.area <= 28 ? YES : area(28));
    case "reach-27":
      return legalAll() || (sc.area <= 27 ? YES : area(27));
    case "beat-27":
      return legalAll() || (sc.area < 27 ? YES : no("not-below", { area: sc.area, bw: sc.bbox[0], bh: sc.bbox[1] }));
    case "reach-24":
      if (s.rotated.length) return no("no-turns");
      return legalAll() || (sc.area <= 24 ? YES : area(24));
    default:
      return no("unknown");
  }
}
