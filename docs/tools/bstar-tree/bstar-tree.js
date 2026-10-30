/**
 * B*-tree — learner-driven lab (Lab 05).
 *
 * The learner edits the tree (parent and side of each block, swap two names, turn a block, move a
 * leaf), presses Pack and sees the blocks drop onto the skyline. Challenges read that learner state
 * on every Check (bstar-tree-lab-model.js): a change after Pack needs a new Pack, a tree loaded with
 * another button does not count, and the study reveal never counts.
 *
 * Drawing is our own SVG (not drawFloorplan): one fixed colour per block id, left link solid,
 * right link dashed, y up from the lower-left corner. Every word shown is in bstar-tree-strings.js.
 */
import { createChallengeLab, el, metricsBlock } from "../../assets/clustering-ui.js";
import * as M from "./bstar-tree-lab-model.js";
import { T } from "./bstar-tree-strings.js";

const root = document.getElementById("lab-root");

let state = M.createState("golden", { pack: true });
let lastMsg = null; // { code, ... } of the last action
let lastCheck = null; // { id, ok, why, ... } of the last Check
let guessText = ""; // text in the guess box (kept across rerenders)
const pick = { swapA: "A", swapB: "C", turn: "D", leaf: "E", to: "B", toSide: "right" };

const INK = "#0f172a";
const RED = "#dc2626";
const SKY = "#eab308";
const SVGNS = "http://www.w3.org/2000/svg";

function svg(tag, attrs = {}, text) {
  const n = document.createElementNS(SVGNS, tag);
  for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
  if (text != null) n.textContent = text;
  return n;
}

const challengeOn = (ctx) => (ctx.state.challengeOn ? ctx.state.challengeId : "");

function apply(ctx, res) {
  state = res.state;
  lastMsg = res.msg;
  lastCheck = null;
  ctx.rerender();
}

/* ---------------- tree view ---------------- */

function drawTree(read, rotated) {
  const W = 340;
  const H = 300;
  const R = 17;
  const out = svg("svg", { viewBox: `0 0 ${W} ${H}`, class: "bt-svg", id: "bt-tree", role: "img", "aria-label": T.treeCaption });
  const turned = new Set(rotated);
  // x = in-order rank (left child to the lower left, right child to the lower right), y = depth
  const pos = {};
  const links = [];
  let rank = 0;
  let depth = 0;
  (function walk(n, d, parent, side) {
    if (!n) return;
    walk(n.left, d + 1, n.id, "left");
    pos[n.id] = { r: rank++, d };
    depth = Math.max(depth, d);
    if (parent) links.push({ from: parent, to: n.id, side });
    walk(n.right, d + 1, n.id, "right");
  })(read.tree, 0, null, null);
  const dx = rank > 1 ? Math.min(66, (W - 2 * R - 24) / (rank - 1)) : 0;
  const dy = depth ? Math.min(58, (H - 96 - 2 * R) / depth) : 0;
  const x0 = (W - dx * (rank - 1)) / 2;
  const y0 = 50;
  const P = (id) => ({ x: x0 + pos[id].r * dx, y: y0 + pos[id].d * dy });

  for (const l of links) {
    const a = P(l.from);
    const b = P(l.to);
    const len = Math.hypot(b.x - a.x, b.y - a.y);
    const ux = (b.x - a.x) / len;
    const uy = (b.y - a.y) / len;
    out.append(svg("line", {
      x1: a.x + ux * R, y1: a.y + uy * R, x2: b.x - ux * R, y2: b.y - uy * R,
      stroke: "#334155", "stroke-width": 2.4, "stroke-dasharray": l.side === "right" ? "7 5" : "none",
      class: `bt-link bt-link-${l.side}`, "data-from": l.from, "data-to": l.to,
    }));
  }
  const walkOrder = M.preorder(read.tree);
  for (const id of Object.keys(pos)) {
    const { x, y } = P(id);
    const g = svg("g", { class: "bt-node", "data-id": id });
    g.append(svg("circle", { cx: x, cy: y, r: R, fill: M.COLORS[id], stroke: INK, "stroke-width": 1.5 }));
    g.append(svg("text", { x, y: y + 1, class: "bt-node-label" }, id));
    const k = walkOrder.indexOf(id);
    if (!read.problems.length && k >= 0) {
      // walk-order badge, upper left of the node (the root tag sits above it)
      g.append(svg("circle", { cx: x - R * 0.95, cy: y - R * 0.95, r: 7.5, fill: "#ffffff", stroke: "#334155", "stroke-width": 1.2 }));
      g.append(svg("text", { x: x - R * 0.95, y: y - R * 0.95 + 0.5, class: "bt-badge" }, String(k + 1)));
    }
    if (turned.has(id)) g.append(svg("text", { x: x + R * 1.05, y: y - R * 0.9, class: "bt-turn" }, T.turnedMark));
    out.append(g);
  }
  if (read.tree) {
    const p = P(read.tree.id);
    out.append(svg("text", { x: p.x + 6, y: p.y - R - 15, class: "bt-root-tag" }, T.rootTag));
  } else {
    out.append(svg("text", { x: W / 2, y: 80, class: "bt-empty" }, T.treeEmpty));
  }
  if (read.loose.length) {
    const y = H - 22;
    out.append(svg("text", { x: 8, y: y + 4, class: "bt-loose-label" }, T.loose));
    read.loose.forEach((id, i) => {
      const x = 150 + i * 40;
      const g = svg("g", { class: "bt-node bt-loose", "data-id": id });
      g.append(svg("circle", { cx: x, cy: y, r: 14, fill: "#ffffff", stroke: M.COLORS[id], "stroke-width": 3 }));
      g.append(svg("text", { x, y: y + 1, class: "bt-node-label", style: `fill:${M.COLORS[id]}` }, id));
      if (turned.has(id)) g.append(svg("text", { x: x + 15, y: y - 12, class: "bt-turn" }, T.turnedMark));
      out.append(g);
    });
  }
  return out;
}

/* ---------------- floorplan view ---------------- */

function drawFloor(pack, rotated, note) {
  const O = M.OUTLINE;
  const U = 28;
  const [bw, bh] = pack ? M.boundingBox(pack) : [0, 0];
  const extW = Math.max(O.w + 0.6, bw + 0.6);
  const extH = Math.max(O.h + 0.6, bh + 0.6);
  const ml = 26;
  const mb = 24;
  const mt = 30;
  const mr = 8;
  const W = ml + extW * U + mr;
  const H = mt + extH * U + mb;
  const sx = (x) => ml + x * U;
  const sy = (y) => mt + (extH - y) * U;
  const out = svg("svg", { viewBox: `0 0 ${W} ${H}`, class: "bt-svg", id: "bt-floor", role: "img", "aria-label": T.floorCaption });

  out.append(svg("rect", { x: sx(0), y: sy(O.h), width: O.w * U, height: O.h * U, fill: "#f8fafc" }));
  for (let x = 1; x < O.w; x++) out.append(svg("line", { x1: sx(x), y1: sy(0), x2: sx(x), y2: sy(O.h), stroke: "#e2e8f0" }));
  for (let y = 1; y < O.h; y++) out.append(svg("line", { x1: sx(0), y1: sy(y), x2: sx(O.w), y2: sy(y), stroke: "#e2e8f0" }));
  out.append(svg("rect", { x: sx(0), y: sy(O.h), width: O.w * U, height: O.h * U, fill: "none", stroke: INK, "stroke-width": 2.2, class: "bt-outline" }));
  for (let x = 0; x <= Math.ceil(extW - 0.6); x++) out.append(svg("text", { x: sx(x), y: sy(0) + 15, class: "bt-tick" }, String(x)));
  for (let y = 0; y <= Math.ceil(extH - 0.6); y++) out.append(svg("text", { x: sx(0) - 9, y: sy(y) + 3.5, class: "bt-tick" }, String(y)));

  if (!pack) {
    out.append(svg("text", { x: sx(O.w / 2), y: sy(O.h / 2), class: "bt-floor-note" }, note));
    return out;
  }
  const turned = new Set(rotated);
  const leg = M.legality(pack);
  for (const id of Object.keys(pack).sort()) {
    const r = pack[id];
    const g = svg("g", { class: "bt-block", "data-id": id });
    const bad = leg.outside.includes(id);
    g.append(svg("rect", {
      x: sx(r.x), y: sy(r.y + r.h), width: r.w * U, height: r.h * U, fill: M.COLORS[id],
      stroke: bad ? RED : INK, "stroke-width": bad ? 3.5 : 1.4, class: "bt-block-rect",
    }));
    for (let i = 1; i < r.w; i++) g.append(svg("line", { x1: sx(r.x + i), y1: sy(r.y), x2: sx(r.x + i), y2: sy(r.y + r.h), stroke: "rgba(255,255,255,0.3)" }));
    for (let j = 1; j < r.h; j++) g.append(svg("line", { x1: sx(r.x), y1: sy(r.y + j), x2: sx(r.x + r.w), y2: sy(r.y + j), stroke: "rgba(255,255,255,0.3)" }));
    g.append(svg("text", { x: sx(r.x + r.w / 2), y: sy(r.y + r.h / 2) + 1, class: "bt-block-label" }, id));
    if (turned.has(id)) g.append(svg("text", { x: sx(r.x + r.w) - 7, y: sy(r.y + r.h) + 11, class: "bt-block-turn" }, T.turnedMark));
    g.append(svg("title", {}, `${id} (${r.x},${r.y}) ${r.w}×${r.h}`));
    out.append(g);
  }
  // skyline: the top edge of what is placed, for every x
  const pts = [];
  const right = Math.max(O.w, bw);
  for (const [a, b, h] of M.skyline(pack)) pts.push([a, h], [b, h]);
  if (bw < right) pts.push([bw, 0], [right, 0]);
  const d = pts.map(([x, y]) => `${sx(x)},${sy(y)}`).join(" ");
  out.append(svg("polyline", { points: d, fill: "none", stroke: INK, "stroke-width": 6, "stroke-linejoin": "round", "stroke-linecap": "round", class: "bt-sky-under" }));
  out.append(svg("polyline", { points: d, fill: "none", stroke: SKY, "stroke-width": 3.6, "stroke-linejoin": "round", "stroke-linecap": "round", class: "bt-sky" }));
  // bounding box
  const e = 0.08;
  out.append(svg("rect", {
    x: sx(-e), y: sy(bh + e), width: (bw + 2 * e) * U, height: (bh + 2 * e) * U,
    fill: "none", stroke: INK, "stroke-width": 2.4, "stroke-dasharray": "10 6", class: "bt-bbox",
  }));
  out.append(svg("text", { x: sx(bw), y: sy(bh + e) - 8, class: "bt-bbox-label" }, T.bboxLabel(bw, bh, bw * bh)));
  return out;
}

/* ---------------- left panel: both views ---------------- */

function renderViews(ctx) {
  const read = M.readTree(state.place);
  const pack = M.currentPack(state);
  const note = read.problems.length ? T.floorBad : state.packed ? T.floorStale : T.floorNotPacked;
  const problems = el("ul", { className: "bt-problems" }, read.problems.map((p) => el("li", { text: T.problems[p.code](p) })));
  const views = el("div", { className: "bt-views" }, [
    el("figure", { className: "bt-view" }, [
      el("figcaption", { text: T.treeCaption }),
      drawTree(read, state.rotated),
      problems,
      el("p", { className: "bt-legend" }, [
        el("span", { className: "bt-key bt-key-solid" }), T.treeLegendLeft, el("br"),
        el("span", { className: "bt-key bt-key-dashed" }), T.treeLegendRight, el("br"),
        T.treeLegendWalk,
      ]),
    ]),
    el("figure", { className: "bt-view" }, [
      el("figcaption", { text: T.floorCaption }),
      drawFloor(pack, state.rotated, note),
      el("p", { className: "bt-legend" }, [
        el("span", { className: "bt-key bt-key-sky" }), T.floorLegendSky, el("br"),
        el("span", { className: "bt-key bt-key-dashed" }), T.floorLegendBox,
      ]),
    ]),
  ]);
  const body = ctx.canvas.parentElement;
  ctx.canvas.style.display = "none";
  body.querySelector(".bt-views")?.remove();
  body.append(views);
}

/* ---------------- right panel: editor and numbers ---------------- */

function select(id, aria, options, value, onChange, disabled = false) {
  const s = el("select", { id, "aria-label": aria, className: "bt-select", disabled, onChange: (e) => onChange(e.target.value) });
  for (const [v, text] of options) {
    const o = el("option", { value: v, text });
    if (v === value) o.selected = true;
    s.append(o);
  }
  return s;
}

const btn = (id, text, cls, onClick) => el("button", { id, className: `btn ${cls}`, type: "button", text, onClick });
const idOptions = (ids) => ids.map((i) => [i, i]);
const sideOptions = () => [["left", T.optLeft], ["right", T.optRight]];

function editorTable(ctx) {
  const mods = M.withRotated(M.MODULES, state.rotated);
  const rows = M.IDS.map((id) => {
    const p = state.place[id];
    const m = mods.find((x) => x.id === id);
    const parentOpts = [["", T.optNone], ["root", T.optRoot], ...idOptions(M.IDS.filter((i) => i !== id))];
    return el("tr", {}, [
      el("td", {}, [el("span", { className: "bt-swatch", style: `background:${M.COLORS[id]}` }), id]),
      el("td", { text: T.sizeOf(m.w, m.h, state.rotated.includes(id)) }),
      el("td", {}, [select(`bt-parent-${id}`, T.ariaParent(id), parentOpts, p.parent || "", (v) => apply(ctx, M.setParent(state, id, v)))]),
      el("td", {}, [select(`bt-side-${id}`, T.ariaSide(id), sideOptions(), p.side, (v) => apply(ctx, M.setSide(state, id, v)),
        !p.parent || p.parent === "root")]),
    ]);
  });
  return el("table", { className: "bt-table" }, [
    el("thead", {}, [el("tr", {}, [T.colBlock, T.colSize, T.colParent, T.colSide].map((t) => el("th", { text: t })))]),
    el("tbody", {}, rows),
  ]);
}

function opsRows(ctx) {
  const row = (label, items) => el("div", { className: "tool-actions bt-row" }, [el("span", { className: "bt-label", text: label }), ...items]);
  const keep = (key) => (v) => {
    pick[key] = v;
  };
  const guess = el("input", {
    id: "bt-guess", type: "text", inputmode: "numeric", className: "bt-input", "aria-label": T.guessAria, value: guessText,
    onInput: (e) => {
      guessText = e.target.value;
    },
    onKeydown: (e) => {
      if (e.key === "Enter") apply(ctx, M.saveGuess(state, guessText));
    },
  });
  return [
    row(T.swapLabel, [
      select("bt-swap-a", T.swapLabel, idOptions(M.IDS), pick.swapA, keep("swapA")),
      el("span", { className: "bt-muted", text: T.swapWith }),
      select("bt-swap-b", T.swapWith, idOptions(M.IDS), pick.swapB, keep("swapB")),
      btn("bt-do-swap", T.swapBtn, "btn-secondary", () => apply(ctx, M.doSwap(state, pick.swapA, pick.swapB))),
    ]),
    row(T.turnLabel, [
      select("bt-turn", T.turnLabel, idOptions(M.IDS), pick.turn, keep("turn")),
      btn("bt-do-turn", T.turnBtn, "btn-secondary", () => apply(ctx, M.doTurn(state, pick.turn))),
    ]),
    row(T.moveLabel, [
      select("bt-move-leaf", T.moveLabel, idOptions(M.IDS), pick.leaf, keep("leaf")),
      el("span", { className: "bt-muted", text: T.moveTo }),
      select("bt-move-parent", T.moveTo, idOptions(M.IDS), pick.to, keep("to")),
      select("bt-move-side", T.colSide, sideOptions(), pick.toSide, keep("toSide")),
      btn("bt-do-move", T.moveBtn, "btn-secondary", () => apply(ctx, M.doMove(state, pick.leaf, pick.to, pick.toSide))),
    ]),
    row(T.guessLabel, [guess, btn("bt-save-guess", T.guessBtn, "btn-secondary", () => apply(ctx, M.saveGuess(state, guessText)))]),
  ];
}

function numberLines() {
  const read = M.readTree(state.place);
  const pack = M.currentPack(state);
  const lines = [];
  if (!read.problems.length && read.tree) {
    lines.push(T.lines.tree(M.fmtTree(read.tree)), T.lines.walk(M.preorder(read.tree).join(", ")));
  }
  lines.push(T.lines.turned(state.rotated));
  if (pack) {
    const sc = M.score(pack);
    const order = M.preorder(read.tree);
    lines.push(
      T.lines.positions(order.map((i) => `${i}(${pack[i].x},${pack[i].y})`).join(" ")),
      T.lines.bbox(sc.bbox[0], sc.bbox[1], sc.area),
      T.lines.wasted(sc.wasted, sc.blocks),
      sc.legal ? T.lines.legalYes : T.lines.legalNo(sc.outside),
    );
  } else lines.push(state.packed ? T.lines.stale : T.lines.notPacked);
  lines.push(T.lines.deadspace(M.OUTLINE_DEADSPACE), "", T.lines.base(T.bases[state.base]));
  const ops = state.ops.map((o) => T.ops[o.kind](o));
  lines.push(T.lines.ops(ops.length, ops.join(", ")));
  lines.push(T.lines.guess(state.guess ? T.guessShown(state.guess) : T.guessNone));
  return lines;
}

function renderWorkspace(ctx) {
  const heads = root.querySelectorAll(".tool-layout .panel-head h2");
  if (heads[0]) heads[0].textContent = T.panelLeft;
  if (heads[1]) heads[1].textContent = T.panelRight;
  renderViews(ctx);

  const edit = el("div", { className: "bt-edit" });
  edit.append(el("p", { className: "bt-muted", text: T.editorHelp }), editorTable(ctx), ...opsRows(ctx));
  const numbers = el("div", { className: "bt-numbers" });
  if (lastCheck && lastCheck.id === ctx.state.challengeId && ctx.state.challengeOn) {
    numbers.append(el("p", { className: `bt-why ${lastCheck.ok ? "ok" : "no"}`, id: "bt-why" }, [
      el("strong", { text: `${T.checkHead} ` }), T.why[lastCheck.why](lastCheck),
    ]));
  }
  if (lastMsg) numbers.append(el("p", { className: "bt-msg", id: "bt-msg", text: T.msg[lastMsg.code](lastMsg) }));
  numbers.append(metricsBlock(numberLines()));
  ctx.metrics.innerHTML = "";
  ctx.metrics.append(el("div", { className: "bt-panel" }, [edit, numbers]));
}

/* ---------------- buttons above the workspace ---------------- */

function extraActions(ctx) {
  return [
    el("span", { className: "bt-label", text: T.loadLabel }),
    ...M.PRESETS.map((name) => btn(`bt-preset-${name}`, T.presets[name], "btn-ghost", () => apply(ctx, M.doPreset(state, name)))),
    btn("bt-clear", T.clearBtn, "btn-ghost", () => apply(ctx, M.doClear(state))),
    btn("bt-pack", T.packBtn, "btn-primary", () => apply(ctx, M.doPack(state))),
    btn("bt-reveal", T.revealBtn, "btn-ghost", () => apply(ctx, M.doReveal(state, challengeOn(ctx)))),
  ];
}

/* ---------------- challenges (all read the learner's tree) ---------------- */

const challenges = M.CHALLENGES.map((c) => ({
  id: c.id,
  level: c.level,
  ...T.challenges[c.id],
  setup: () => {
    state = M.createState(c.start);
    lastMsg = null;
    lastCheck = null;
    guessText = "";
  },
  check: () => {
    const r = M.checkChallenge(c.id, state);
    lastCheck = { id: c.id, ...r };
    return r.ok;
  },
}));

createChallengeLab(root, {
  starterButtonLabel: T.starterButton,
  idlePromptHtml: T.idlePrompt,
  starterHtml: T.starterHtml,
  challenges,
  loadStarter() {
    state = M.createState("golden", { pack: true });
    lastMsg = null;
    lastCheck = null;
    guessText = "";
  },
  extraActions,
  renderWorkspace,
});
