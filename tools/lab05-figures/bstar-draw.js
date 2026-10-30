// Draw a B*-tree and its floorplan on a 2D canvas (Lab 05 figures and walkthrough frames).
// One drawing code for both, so the slides and the frames look the same.
//
// A scene is one entry of `bstar_check.py --json` -> scenes[] (tree_nested, steps[], outline, rotated).
// Rules kept everywhere: colour by block id (never by index), left link solid, right link dashed,
// y grows upward from the lower-left corner of the outline.

export const FONT = "system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif";
const INK = "#0f172a";
const MUTED = "#64748b";
const GRID = "#e2e8f0";
const RED = "#dc2626";
const GREEN = "#15803d";
const SKY = "#eab308";

function font(px, bold = false) {
  return `${bold ? "bold " : ""}${Math.round(px)}px ${FONT}`;
}

// text on a white halo, so it stays readable over lines and blocks
function label(ctx, text, x, y, { px = 20, color = INK, align = "center", base = "middle", bold = false, halo = true } = {}) {
  ctx.font = font(px, bold);
  ctx.textAlign = align;
  ctx.textBaseline = base;
  if (halo) {
    ctx.lineWidth = Math.max(3, px * 0.28);
    ctx.strokeStyle = "rgba(255,255,255,0.92)";
    ctx.lineJoin = "round";
    ctx.strokeText(text, x, y);
  }
  ctx.fillStyle = color;
  ctx.fillText(text, x, y);
}

function arrowHead(ctx, x1, y1, x2, y2, size) {
  const a = Math.atan2(y2 - y1, x2 - x1);
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - size * Math.cos(a - 0.45), y2 - size * Math.sin(a - 0.45));
  ctx.lineTo(x2 - size * Math.cos(a + 0.45), y2 - size * Math.sin(a + 0.45));
  ctx.closePath();
  ctx.fill();
}

function hatch(ctx, x, y, w, h, color, gap) {
  ctx.save();
  ctx.beginPath();
  ctx.rect(x, y, w, h);
  ctx.clip();
  ctx.strokeStyle = color;
  ctx.lineWidth = 1.6;
  for (let t = -h; t < w + h; t += gap) {
    ctx.beginPath();
    ctx.moveTo(x + t, y + h);
    ctx.lineTo(x + t + h, y);
    ctx.stroke();
  }
  ctx.restore();
}

// ---------------------------------------------------------------- tree

function treeLayout(nested) {
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
  })(nested, 0, null, null);
  return { pos, links, n: rank, depth };
}

/**
 * opts: colors, placed (ids filled with colour), highlight (ids with a black ring), marks ({id: "?"}),
 * linkLabels ({left: "...", right: "..."}), rootLabel, rotated (ids with a turn badge), px (font size).
 */
export function drawTree(ctx, box, scene, opts) {
  const px = opts.px || 20;
  const colors = opts.colors;
  const placed = new Set(opts.placed || []);
  const hi = new Set(opts.highlight || []);
  const rotated = new Set(opts.rotated || []);
  const { pos, links, n, depth } = treeLayout(scene.tree_nested);
  const r = opts.radius || px * 1.15;
  const dx = Math.min(px * 5.2, (box.w - 2 * r - 8) / Math.max(1, n - 1));
  const dy = Math.min(px * 3.6, (box.h - 2 * r - px * 1.6) / Math.max(1, depth));
  const x0 = box.x + (box.w - dx * (n - 1)) / 2;
  const y0 = box.y + r + px * 1.2;
  const P = (id) => ({ x: x0 + pos[id].r * dx, y: y0 + pos[id].d * dy });

  for (const l of links) {
    const a = P(l.from);
    const b = P(l.to);
    const len = Math.hypot(b.x - a.x, b.y - a.y);
    const ux = (b.x - a.x) / len;
    const uy = (b.y - a.y) / len;
    ctx.save();
    ctx.strokeStyle = "#334155";
    ctx.lineWidth = Math.max(2, px * 0.13);
    if (l.side === "right") ctx.setLineDash([px * 0.5, px * 0.35]);
    ctx.beginPath();
    ctx.moveTo(a.x + ux * r, a.y + uy * r);
    ctx.lineTo(b.x - ux * r, b.y - uy * r);
    ctx.stroke();
    ctx.restore();
    const text = opts.linkLabels && opts.linkLabels[l.side];
    if (text && (!opts.linkLabelFrom || opts.linkLabelFrom === l.from)) {
      const mx = (a.x + b.x) / 2;
      const my = (a.y + b.y) / 2;
      const off = px * 0.9;
      ctx.font = font(px * 0.85, true);
      const tw = ctx.measureText(text).width;
      // keep the label inside the panel (long French labels on the right link)
      const lx = l.side === "left" ? Math.max(box.x + tw, mx - off) : Math.min(box.x + box.w - tw, mx + off);
      label(ctx, text, lx, my - px * 0.3,
        { px: px * 0.85, color: "#334155", align: l.side === "left" ? "right" : "left", bold: true });
    }
  }
  for (const id of Object.keys(pos)) {
    const { x, y } = P(id);
    const col = colors[id];
    const on = placed.has(id);
    if (hi.has(id)) {
      ctx.beginPath();
      ctx.arc(x, y, r + px * 0.32, 0, 2 * Math.PI);
      ctx.fillStyle = "rgba(234,179,8,0.45)";
      ctx.fill();
    }
    ctx.beginPath();
    ctx.arc(x, y, r, 0, 2 * Math.PI);
    ctx.fillStyle = on ? col : "#ffffff";
    ctx.fill();
    ctx.lineWidth = hi.has(id) ? Math.max(3, px * 0.18) : Math.max(2, px * 0.12);
    ctx.strokeStyle = hi.has(id) ? INK : col;
    ctx.stroke();
    label(ctx, id, x, y + 1, { px: px * 1.05, color: on ? "#ffffff" : col, bold: true, halo: false });
    if (rotated.has(id)) label(ctx, "↻", x + r * 0.95, y - r * 0.95, { px: px * 0.95, color: INK, bold: true });
    const mark = opts.marks && opts.marks[id];
    if (mark) label(ctx, mark, x + r + px * 0.35, y, { px: px * 1.2, color: INK, align: "left", bold: true });
  }
  if (opts.rootLabel) {
    const { x, y } = P(scene.tree_nested.id);
    label(ctx, opts.rootLabel, x, y - r - px * 0.6, { px: px * 0.85, color: "#334155", bold: true });
  }
}

// ---------------------------------------------------------------- floorplan

function heightAt(contour, x) {
  for (const [a, b, h] of contour || []) if (x >= a && x < b) return h;
  return 0;
}

/**
 * opts: colors, k (blocks placed, default all), extentW (units shown across), px,
 * outline (draw the frame, default true), skyline, skylineLabel ({text, x, y} in units),
 * falling (draw step k+1 as a ghost near the top with an arrow to where it lands),
 * hole (hatch the empty squares under the last placed block), bbox ({text} or null), wasted (hatch),
 * annotations: [{type: "text"|"hdim"|"vdim"|"arrow", ...} in units], tray (blocks laid out, not placed).
 */
export function drawFloor(ctx, box, scene, opts) {
  const px = opts.px || 20;
  const colors = opts.colors;
  const O = scene.outline;
  const steps = scene.steps;
  const k = opts.k == null ? steps.length : opts.k;
  const placed = steps.slice(0, k);
  const m = opts.margins || { l: px * 2.4, r: px * 0.6, t: px * 1.6, b: px * 2.4 };
  const extentW = opts.extentW || O.w + 0.6;
  const s = opts.scale || Math.min((box.w - m.l - m.r) / extentW, (box.h - m.t - m.b) / O.h);
  const ox = box.x + m.l;
  const oy = box.y + m.t + ((box.h - m.t - m.b) - O.h * s);
  const sx = (x) => ox + x * s;
  const sy = (y) => oy + (O.h - y) * s;

  if (opts.outline !== false) {
    ctx.fillStyle = "#f8fafc";
    ctx.fillRect(sx(0), sy(O.h), O.w * s, O.h * s);
    ctx.strokeStyle = GRID;
    ctx.lineWidth = 1;
    for (let x = 1; x < O.w; x++) {
      ctx.beginPath(); ctx.moveTo(sx(x), sy(0)); ctx.lineTo(sx(x), sy(O.h)); ctx.stroke();
    }
    for (let y = 1; y < O.h; y++) {
      ctx.beginPath(); ctx.moveTo(sx(0), sy(y)); ctx.lineTo(sx(O.w), sy(y)); ctx.stroke();
    }
    ctx.strokeStyle = INK;
    ctx.lineWidth = Math.max(2, px * 0.13);
    ctx.strokeRect(sx(0), sy(O.h), O.w * s, O.h * s);
  }

  const block = (id, x, y, w, h, { ghost = false, out = false, turned = false } = {}) => {
    const X = sx(x), Y = sy(y + h), W = w * s, H = h * s;
    ctx.save();
    ctx.globalAlpha = ghost ? 0.4 : 0.92;
    ctx.fillStyle = colors[id];
    ctx.fillRect(X, Y, W, H);
    ctx.globalAlpha = 1;
    ctx.strokeStyle = "rgba(255,255,255,0.35)";
    ctx.lineWidth = 1;
    for (let i = 1; i < w; i++) { ctx.beginPath(); ctx.moveTo(X + i * s, Y); ctx.lineTo(X + i * s, Y + H); ctx.stroke(); }
    for (let j = 1; j < h; j++) { ctx.beginPath(); ctx.moveTo(X, Y + j * s); ctx.lineTo(X + W, Y + j * s); ctx.stroke(); }
    ctx.strokeStyle = out ? RED : INK;
    ctx.lineWidth = out ? Math.max(3, px * 0.2) : Math.max(1.5, px * 0.08);
    if (ghost) ctx.setLineDash([px * 0.35, px * 0.25]);
    ctx.strokeRect(X, Y, W, H);
    ctx.restore();
    label(ctx, id, X + W / 2, Y + H / 2 + 1, { px: Math.min(px * 1.3, s * 0.62), color: "#ffffff", bold: true, halo: false });
    if (turned) label(ctx, "↻", X + W - px * 0.55, Y + px * 0.7, { px: px * 0.95, color: "#ffffff", bold: true, halo: false });
  };

  if (opts.tray) {
    // the five blocks laid out on squared paper above the outline, not placed yet
    for (const t of opts.tray) block(t.id, t.x, t.y, t.w, t.h);
  }

  const rotated = new Set(scene.rotated || []);
  for (const st of placed) {
    const out = st.x + st.w > O.w || st.y + st.h > O.h;
    block(st.id, st.x, st.y, st.w, st.h, { out, turned: rotated.has(st.id) });
  }

  if (opts.hole && k > 0) {
    const st = steps[k - 1];
    const before = k > 1 ? steps[k - 2].contour : [];
    for (let xi = st.x; xi < st.x + st.w; xi++) {
      const base = heightAt(before, xi + 0.5);
      if (st.y > base) {
        ctx.fillStyle = "rgba(220,38,38,0.10)";
        ctx.fillRect(sx(xi), sy(st.y), s, (st.y - base) * s);
        hatch(ctx, sx(xi), sy(st.y), s, (st.y - base) * s, RED, px * 0.5);
      }
    }
  }

  if ((opts.wasted || opts.bbox) && placed.length) {
    const W = Math.max(...placed.map((p) => p.x + p.w));
    const H = Math.max(...placed.map((p) => p.y + p.h));
    if (opts.wasted) {
      for (let x = 0; x < W; x++) for (let y = 0; y < H; y++) {
        const used = placed.some((p) => x >= p.x && x < p.x + p.w && y >= p.y && y < p.y + p.h);
        if (!used) {
          ctx.fillStyle = "rgba(100,116,139,0.16)";
          ctx.fillRect(sx(x), sy(y + 1), s, s);
          hatch(ctx, sx(x), sy(y + 1), s, s, MUTED, px * 0.5);
        }
      }
    }
    if (opts.bbox) {
      const e = 0.07;
      ctx.save();
      ctx.strokeStyle = INK;
      ctx.lineWidth = Math.max(2.5, px * 0.16);
      ctx.setLineDash([px * 0.6, px * 0.35]);
      ctx.strokeRect(sx(-e), sy(H + e), (W + 2 * e) * s, (H + 2 * e) * s);
      ctx.restore();
      if (opts.bbox.text) label(ctx, opts.bbox.text, sx(W), sy(H + e) - px * 0.75, { px: px * 1.1, align: "right", bold: true });
    }
  }

  if (opts.skyline) {
    const c = k > 0 ? steps[k - 1].contour : [];
    const right = Math.max(O.w, ...placed.map((p) => p.x + p.w));
    const pts = [];
    let prev = null;
    for (let x = 0; x < right; x++) {
      const h = heightAt(c, x + 0.5);
      if (prev === null) pts.push([0, h]);
      else if (h !== prev) { pts.push([x, prev]); pts.push([x, h]); }
      prev = h;
    }
    pts.push([right, prev]);
    ctx.save();
    ctx.lineJoin = "round";
    ctx.lineCap = "round";
    for (const [w, col] of [[px * 0.42, INK], [px * 0.28, SKY]]) {
      ctx.lineWidth = w;
      ctx.strokeStyle = col;
      ctx.beginPath();
      pts.forEach(([x, y], i) => (i ? ctx.lineTo(sx(x), sy(y)) : ctx.moveTo(sx(x), sy(y))));
      ctx.stroke();
    }
    ctx.restore();
    const L = opts.skylineLabel;
    if (L) label(ctx, L.text, sx(L.x), sy(L.y), { px: px * 1.0, color: "#a16207", bold: true, align: L.align || "center" });
  }

  if (opts.falling && k < steps.length) {
    const st = steps[k];
    const topY = O.h - st.h - 0.4;
    block(st.id, st.x, topY, st.w, st.h, { ghost: true });
    const cx = sx(st.x + st.w / 2);
    ctx.save();
    ctx.strokeStyle = INK;
    ctx.fillStyle = INK;
    ctx.lineWidth = Math.max(2, px * 0.12);
    ctx.setLineDash([px * 0.3, px * 0.25]);
    ctx.beginPath();
    ctx.moveTo(cx, sy(topY) + 2);
    ctx.lineTo(cx, sy(st.y + st.h) - px * 0.5);
    ctx.stroke();
    ctx.setLineDash([]);
    arrowHead(ctx, cx, sy(topY), cx, sy(st.y + st.h) - 2, px * 0.7);
    ctx.restore();
  }

  for (const a of opts.annotations || []) {
    const col = a.color || INK;
    if (a.type === "text") {
      label(ctx, a.text, sx(a.x), sy(a.y), { px: px * (a.size || 1), color: col, align: a.align || "center", bold: a.bold !== false });
    } else if (a.type === "hdim" || a.type === "vdim") {
      const hz = a.type === "hdim";
      const [X1, Y1, X2, Y2] = hz ? [sx(a.x1), sy(a.y), sx(a.x2), sy(a.y)] : [sx(a.x), sy(a.y1), sx(a.x), sy(a.y2)];
      ctx.save();
      ctx.strokeStyle = col;
      ctx.lineWidth = Math.max(1.5, px * 0.09);
      ctx.beginPath(); ctx.moveTo(X1, Y1); ctx.lineTo(X2, Y2); ctx.stroke();
      const t = px * 0.4;
      ctx.beginPath();
      if (hz) { ctx.moveTo(X1, Y1 - t); ctx.lineTo(X1, Y1 + t); ctx.moveTo(X2, Y2 - t); ctx.lineTo(X2, Y2 + t); }
      else { ctx.moveTo(X1 - t, Y1); ctx.lineTo(X1 + t, Y1); ctx.moveTo(X2 - t, Y2); ctx.lineTo(X2 + t, Y2); }
      ctx.stroke();
      ctx.restore();
      if (hz) label(ctx, a.text, (X1 + X2) / 2, Y1 + (a.above ? -px * 0.75 : px * 0.85), { px: px * (a.size || 1), color: col, bold: true });
      else label(ctx, a.text, X1 - px * 0.5, (Y1 + Y2) / 2, { px: px * (a.size || 1), color: col, bold: true, align: "right" });
    } else if (a.type === "arrow") {
      const [X1, Y1, X2, Y2] = [sx(a.x1), sy(a.y1), sx(a.x2), sy(a.y2)];
      ctx.save();
      ctx.strokeStyle = col;
      ctx.fillStyle = col;
      ctx.lineWidth = Math.max(2, px * 0.14);
      if (a.dashed) ctx.setLineDash([px * 0.4, px * 0.3]);
      ctx.beginPath(); ctx.moveTo(X1, Y1); ctx.lineTo(X2, Y2); ctx.stroke();
      ctx.setLineDash([]);
      arrowHead(ctx, X1, Y1, X2, Y2, px * 0.7);
      ctx.restore();
      if (a.text) label(ctx, a.text, sx(a.tx ?? (a.x1 + a.x2) / 2), sy(a.ty ?? (a.y1 + a.y2) / 2),
        { px: px * (a.size || 1), color: col, bold: true, align: a.align || "center" });
    }
  }
  return { s, sx, sy };
}

export const COLORS_FALLBACK = { A: "#1d4ed8", B: "#0f6b5c", C: "#b45309", D: "#7c3aed", E: "#be123c" };
export { RED, GREEN, INK };

/** Walkthrough frame: tree on the left, floorplan on the right, on the viewer's canvas. */
export function drawBstarFrame(canvas, step) {
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  const w = Math.max(200, rect.width);
  const h = Math.max(160, rect.height);
  canvas.width = Math.round(w * dpr);
  canvas.height = Math.round(h * dpr);
  const ctx = canvas.getContext("2d");
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, w, h);
  const f = step.bstar;
  const colors = f.colors || COLORS_FALLBACK;
  const px = f.px || 13;
  const split = w * 0.36;
  drawTree(ctx, { x: 4, y: 4, w: split - 8, h: h - 8 }, f.scene, { ...f.tree, colors, px });
  ctx.strokeStyle = GRID;
  ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(split, 12); ctx.lineTo(split, h - 12); ctx.stroke();
  drawFloor(ctx, { x: split, y: 0, w: w - split, h }, f.scene, { ...f.floor, colors, px });
}
