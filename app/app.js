// 발견 그래프 v1 렌더러 (프로토타입)
// - path 단계를 순서대로 진행한다: ask / digest / predict / explore / notice / compute / synthesis
// - 장면 객체는 reveal: "after:<step-id>" 조건이 만족될 때만 보인다 (딸깍 방지)
// - 슬라이더 눈금은 readout_reveal 전까지 가린다
(() => {
  const params = new URLSearchParams(location.search);
  const ids = Object.keys(window.GRAPHS || {});
  // 문항 고르기: ?g=<id> 또는 #<id> (파일로 열 때도 동작하도록 해시 우선)
  const want = decodeURIComponent(location.hash.slice(1)) || params.get("g");
  const G = window.GRAPHS[want] || window.GRAPHS[ids[0]];
  const $ = (id) => document.getElementById(id);

  const state = {
    i: 0,                 // 현재 path 단계 번호
    done: new Set(),      // 끝난 단계 id
    vals: {},             // 슬라이더 값 (매개변수 이름 → 값)
    visited: {},          // 슬라이더별로 지나간 값들
    countHits: new Set(), // count-equals 를 만족한 슬라이더 상태
    nearHit: false,       // near 체크포인트를 만족한 적이 있는가
    predictions: {},      // 학생 예측 기록
    notes: {},            // 학생이 쓴 noticing / digest
    attempts: 0,
    timers: [],
  };

  // ---------- 공통 유틸 ----------
  function tex(el) {
    if (window.renderMathInElement) {
      renderMathInElement(el, { delimiters: [{ left: "$$", right: "$$", display: true }, { left: "$", right: "$", display: false }], throwOnError: false });
    }
  }
  function md(s) {
    // 수식 속 부등호(예: $g(p)<t<5$)가 HTML 태그로 읽히지 않도록, 허용한 태그 외의 < 는 &lt; 로
    return String(s).replace(/<(?!\/?(b|div|br)\b)/g, "&lt;")
      .replace(/\*\*(.+?)\*\*/g, "<b>$1</b>").replace(/\n/g, "<br>");
  }
  function verifiedRef(s) {
    const m = /^\$verified\.(\w+)$/.exec(s);
    return m ? G.verified[m[1]] : s;
  }
  function textRef(s) {
    if (s === "$UNDERSTAND.unknown_hint") return G.understand.unknown_hint;
    return s;
  }
  function parseNum(s) {
    s = String(s).trim().replace(/\s/g, "").replace(/−/g, "-");
    const frac = /^(-?\d+(?:\.\d+)?)\/(-?\d+(?:\.\d+)?)$/.exec(s);
    if (frac) return Number(frac[1]) / Number(frac[2]);
    return s === "" ? NaN : Number(s);
  }
  function compileP(expr, names) {
    const js = String(expr).replace(/\^/g, "**");
    // eslint-disable-next-line no-new-func
    return new Function(...names, `return ${js};`);
  }
  function compile(expr, param) {
    const js = String(expr).replace(/\^/g, "**");
    // eslint-disable-next-line no-new-func
    return new Function("x", param, `return ${js};`);
  }
  // 학생이 쓴 식(예: -3a, 27a^3+4, 4-5a³)을 JS 함수로. 실패하면 null
  function compileStudent(s, v) {
    s = String(s).trim().replace(/\s/g, "").replace(/−/g, "-").replace(/×|·/g, "*")
      .replace(/²/g, "^2").replace(/³/g, "^3");
    if (!s || !new RegExp(`^[0-9.+\\-*/^()${v}]+$`).test(s)) return null;
    s = s.replace(new RegExp(`(\\d|\\)|${v})(?=[(${v}])`, "g"), "$1*").replace(/\^/g, "**");
    try { const fn = new Function(v, `return (${s});`); fn(0.7); return fn; } catch (e) { return null; }
  }
  function sameExpr(input, accept, v) {
    const a = compileStudent(input, v), b = compile(accept, v).bind(null, 0);
    if (!a) return false;
    return [0.37, 1.3, 2.1, -0.8].every((t) => Math.abs(a(t) - b(t)) < 1e-9 * (1 + Math.abs(b(t))));
  }
  function isRevealed(rule) {
    if (!rule || rule === "always") return true;
    if (typeof rule === "string" && rule.startsWith("after:")) return state.done.has(rule.slice(6));
    if (rule.all) return rule.all.every(isRevealed);
    if (rule.any) return rule.any.some(isRevealed);
    return false;
  }
  const step = () => G.path[state.i];

  // ---------- 헤더 · 문제 · 지도 ----------
  $("src").textContent = `${G.source.examLabel} ${G.source.section ? G.source.section + " " : ""}${G.source.number}번 (${G.source.score}점)`;
  const pick = $("pick");
  if (pick) {
    pick.innerHTML = ids.map((id) => {
      const s = window.GRAPHS[id].source;
      const short = s.examLabel.replace("학년도", "").replace("대학수학능력시험", "수능").replace(" 전국연합학력평가", " 학평").replace("모의평가", "모평");
      return `<option value="${id}">${short} ${s.number}번 (${s.score}점)</option>`;
    }).join("");
    pick.value = G.id;
    pick.onchange = () => { location.hash = encodeURIComponent(pick.value); location.reload(); };
  }
  $("problem").innerHTML = `<div>${md(G.statement)}</div>` + (G.source.choices
    ? `<div class="choices">${G.source.choices.map((c, i) => "①②③④⑤"[i] + " " + c).join("　")}</div>` : "");
  tex($("problem"));

  function depthOf(id, seen = new Set()) {
    const parent = G.analysis.find((q) => q.needs.includes(id));
    if (!parent || seen.has(parent.id)) return 0;
    seen.add(parent.id);
    return 1 + depthOf(parent.id, seen);
  }
  function renderTree() {
    // 질문은 그 질문에 답하는 단계가 모두 끝났을 때만 '답함'으로 표시한다
    const answered = new Set(G.analysis.map((q) => q.id).filter((qid) => {
      const steps = G.path.filter((s) => s.answers === qid);
      return steps.length && steps.every((s) => state.done.has(s.id));
    }));
    const cur = step() && step().answers;
    $("tree").innerHTML = G.analysis.map((q) => {
      const cls = q.id === cur ? "active" : answered.has(q.id) ? "done" : "";
      return `<li class="${cls}" style="--depth:${depthOf(q.id)}">${md(q.ask)}</li>`;
    }).join("");
    tex($("tree"));
  }

  function renderPolya() {
    const cur = step() ? step().polya : "carry-out";
    const order = ["understand", "plan", "carry-out", "look-back"];
    document.querySelectorAll(".stage").forEach((el) => {
      const s = el.dataset.stage;
      el.classList.toggle("now", s === cur);
      el.classList.toggle("done", order.indexOf(s) < order.indexOf(cur));
    });
  }

  // ---------- 보드 ----------
  const scene = G.scenes.s1;
  const v = scene.view;
  const board = JXG.JSXGraph.initBoard("board", {
    boundingbox: [v.x[0], v.y[1], v.x[1], v.y[0]],
    keepaspectratio: v.aspect !== "free",
    axis: false, showCopyright: false, showNavigation: false,
    pan: { enabled: false }, zoom: { enabled: false },
  });
  // Manim 느낌 (밝은 배경): 격자 없는 축, 굵고 둥근 곡선, Manim 색을 밝은 바탕에 맞게 진하게, KaTeX 글꼴
  const M = { blue: "#2c7fb8", orange: "#e8772e", green: "#3a9a4f", red: "#d0463b", gray: "#a3a3a3", axis: "#3b3b3b" };
  const TONE = { "#2f6fde": M.blue, "#d9822b": M.orange, "#1f8a5b": M.green, "#c2453a": M.red,
    "#9aa0a6": M.gray, "#888": M.gray, "#333": "#3b3b3b", "#6b7078": "#7a7a7a" };
  const tone = (c, fb) => (c ? TONE[c.toLowerCase()] || c : fb);
  const TEXFONT = "font-family: KaTeX_Main, 'Times New Roman', serif;";
  const hasHangul = (t) => /[가-힣]/.test(t);
  // 라벨: 수식이면 KaTeX, 한글이면 일반 글꼴
  const labelAttrs = (t, col, size = 16) => hasHangul(t)
    ? { fontSize: size - 2, strokeColor: col, cssStyle: "font-weight:600;" }
    : { fontSize: size, strokeColor: col, useKatex: true };
  const tickLabel = { fontSize: 13, strokeColor: "#555", cssStyle: TEXFONT, highlight: false };
  const axisStyle = (name, labelOffset, ticks, drawLabels) => ({
    strokeColor: M.axis, strokeWidth: 2, highlight: false, lastArrow: { type: 2, size: 6 },
    name, withLabel: true, label: { position: "rt", offset: labelOffset, ...labelAttrs(name, M.axis, 18) },
    ticks: { ticksDistance: ticks, minorTicks: 0, majorHeight: 9, strokeColor: M.axis, strokeWidth: 1.6,
      drawLabels, drawZero: false, insertTicks: false, label: tickLabel },
  });
  board.create("axis", [[0, 0], [1, 0]], axisStyle(scene.axes.x.name, [-14, 14], scene.axes.x.ticks, true));
  board.create("axis", [[0, 0], [0, 1]], axisStyle(scene.axes.y.name, [10, -8], scene.axes.y.ticks, scene.axes.y.labels !== false));

  // 곡선이 처음 열릴 때 왼쪽에서 오른쪽으로 그려진다 (Manim 의 Create)
  const smooth = (t) => t * t * (3 - 2 * t);
  function drawIn(setEnd, ms = 900) {
    const [x0, , x1] = board.getBoundingBox(), t0 = performance.now();
    // requestAnimationFrame 은 탭이 가려지면 멈추므로 타이머로 돌린다 (가려져도 결국 끝까지 그려진다)
    const tick = () => {
      const t = Math.min(1, (performance.now() - t0) / ms);
      setEnd(t < 1 ? x0 + (x1 - x0) * smooth(t) : Infinity); board.update();
      if (t < 1) setTimeout(tick, 16);
    };
    setEnd(x0); setTimeout(tick, 16);
  }

  const objs = Object.fromEntries(scene.objects.map((o) => [o.id, o]));
  const sliderSpecs = scene.objects.filter((o) => o.type === "slider");
  const PN = sliderSpecs.map((o) => o.id);  // 매개변수 이름들 (k, a, m, t, …)
  sliderSpecs.forEach((o) => { state.vals[o.id] = o.init; state.visited[o.id] = []; });
  const P = PN[0];
  // 식을 매개변수 전체의 함수로: fn(x) — 매개변수 값은 state.vals 에서 읽는다
  function live(expr) {
    const g = compileP(expr, ["x", ...PN]);
    return (xx) => g(xx, ...PN.map((n) => state.vals[n]));
  }
  const rootsSpec = scene.objects.find((o) => o.type === "intersections");
  const fnSpec = objs[rootsSpec.of[0]];
  const color = (name, fb) => getComputedStyle(document.documentElement).getPropertyValue(name).trim() || fb;

  // 함수 그래프들: 주 곡선 + 비교용 곡선 + 고정 직선·안내선
  const fns = {};
  scene.objects.filter((o) => o.type === "function").forEach((o) => {
    const at = live(o.expr);
    const main = o === fnSpec;
    const col = tone(o.color, main ? M.blue : M.gray);
    const guide = o.role === "fixed" || o.role === "guide";
    const ent = { spec: o, at, end: Infinity, shown: false };
    ent.jx = board.create("functiongraph", [at, () => board.getBoundingBox()[0], () => Math.min(ent.end, board.getBoundingBox()[2])], {
      strokeColor: col, strokeWidth: o.width ? o.width + 1 : main ? 5 : guide ? 2.5 : 3.5,
      dash: o.style === "dashed" ? 3 : 0, lineCap: "round", visible: false, highlight: false,
      name: main || o.label_at !== undefined ? "" : (o.label || ""), withLabel: !main && !!o.label && o.label_at === undefined,
      label: { position: "rt", offset: [-56, 12], ...labelAttrs(o.label || "", col) },
    });
    // label_at: 곡선과 겹치지 않는 자리(x=label_at)에 라벨을 따로 붙인다
    if (o.label_at !== undefined) {
      ent.lab = board.create("text", [() => o.label_at + 0.15, () => at(o.label_at) + (o.label_dy || 0), o.label], {
        visible: false, fixed: true, highlight: false, anchorY: "middle", ...labelAttrs(o.label, col),
      });
    }
    fns[o.id] = ent;
  });
  const F = fns[fnSpec.id].at;
  const target = rootsSpec.of[1] === "@x-axis" ? () => 0 : fns[rootsSpec.of[1]].at;

  // 세로선 (대칭축 등)
  const vlines = scene.objects.filter((o) => o.type === "vline").map((o) => {
    const xf = live(o.x);
    const col = tone(o.color, "#7a7a7a");
    const ln = board.create("line", [[() => xf(0), 0], [() => xf(0), 1]], {
      strokeColor: col, strokeWidth: 1.8, dash: 3, visible: false, highlight: false, fixed: true,
      straightFirst: true, straightLast: true,
    });
    const lab = board.create("text", [() => xf(0) + 0.1, () => board.getBoundingBox()[3] + 0.45, o.label || ""], {
      visible: false, fixed: true, highlight: false, ...labelAttrs(o.label || "", col, 15),
    });
    return { spec: o, ln, lab };
  });

  // 곡선 위의 점 (x 는 숫자 또는 매개변수 식 — 식은 렌더 전용, 학생에게는 label 만 보인다)
  const pointObjs = scene.objects.filter((o) => o.type === "point-on-curve").map((o) => {
    const xf = typeof o.x === "number" ? () => o.x : ((g) => () => g(0))(live(o.x));
    const on = fns[o.curve] ? fns[o.curve].at : F;
    const col = tone(o.color, "#3b3b3b");
    const pt = board.create("point", [() => xf(), () => on(xf())], {
      name: o.label || "", withLabel: !!o.label, size: 5, fixed: true, visible: false, highlight: false,
      fillColor: col, strokeColor: "#ffffff", strokeWidth: 1.5,
      label: { offset: [10, 12], ...labelAttrs(o.label || "", col, 16) },
    });
    let trail = null; const seen = new Map();
    if (o.trace) {
      trail = board.create("curve", [[], []], { strokeColor: col, strokeWidth: 3, strokeOpacity: 0.35,
        lineCap: "round", visible: false, highlight: false, fixed: true });
    }
    return { spec: o, pt, trail, record(key) {
      if (!trail) return;
      seen.set(key, [xf(), on(xf())]);
      const arr = [...seen.entries()].sort((p, q) => p[0] - q[0]).map((e) => e[1]);
      trail.dataX = arr.map((p) => p[0]); trail.dataY = arr.map((p) => p[1]);
    } };
  });
  const rootPts = [];
  for (let n = 0; n < 6; n++) {
    rootPts.push(board.create("point", [0, 0], { name: "", size: 5.5, fixed: true, visible: false,
      strokeColor: "#ffffff", strokeWidth: 1.5, fillColor: M.green, highlight: false }));
  }

  // 서로 다른 교점: 부호가 바뀌는 점 + 차이가 0에 '닿는' 극점(중근·접점)을 모아 합친다
  const touchTol = rootsSpec.touch_tol ?? 1e-7;
  const mergeX = rootsSpec.merge_x ?? (rootsSpec.merge_tol || 1e-6) * 1e4;
  function distinctRoots() {
    const D = (xx) => F(xx) - target(xx);
    const lo = -200, hi = 200, N = 8000, h = (hi - lo) / N;
    const roots = [], touches = [];
    const bisect = (g, a, b) => { for (let t = 0; t < 80; t++) { const m = (a + b) / 2; (g(a) * g(m) <= 0) ? (b = m) : (a = m); } return (a + b) / 2; };
    const dD = (xx) => (D(xx + 1e-6) - D(xx - 1e-6)) / 2e-6;
    for (let n = 0; n < N; n++) {
      const a = lo + n * h, b = a + h, fa = D(a), fb = D(b);
      if (fa === 0) roots.push(a);
      else if (fa * fb < 0) roots.push(bisect(D, a, b));
      const da = dD(a), db = dD(b);
      if (da * db < 0) {
        const c = bisect(dD, a, b);
        if (Math.abs(D(c)) < touchTol) touches.push(c);
      }
    }
    // 접점 근처의 (아주 가까운) 교점들은 접점 하나로 본다
    const all = roots.filter((r) => !touches.some((c) => Math.abs(r - c) < mergeX)).concat(touches);
    all.sort((p, q) => p - q);
    const merged = [];
    for (const r of all) if (!merged.length || Math.abs(r - merged[merged.length - 1]) > 1e-4) merged.push(r);
    return merged;
  }
  const sumTarget = rootsSpec.sum_target ? live(rootsSpec.sum_target) : null;

  function refreshBoard() {
    const showCurve = isRevealed(fnSpec.reveal);
    let anyCurve = false;
    Object.values(fns).forEach((ent) => {
      const { spec, jx } = ent;
      const on = isRevealed(spec.reveal);
      if (on && !ent.shown) { ent.shown = true; if (!params.get("to")) drawIn((e) => { ent.end = e; }, spec.role ? 600 : 1000); }
      jx.setAttribute({ visible: on });
      if (ent.lab) ent.lab.setAttribute({ visible: on });
      if (on && spec.role !== "fixed" && spec.role !== "guide") anyCurve = true;
    });
    vlines.forEach(({ spec, ln, lab }) => { const on = isRevealed(spec.reveal); ln.setAttribute({ visible: on }); lab.setAttribute({ visible: on }); });
    pointObjs.forEach((p) => {
      const on = showCurve && isRevealed(p.spec.reveal);
      p.pt.setAttribute({ visible: on });
      if (p.trail) p.trail.setAttribute({ visible: on });
    });
    $("veil").hidden = anyCurve || sketchOn;
    const showRoots = showCurve && isRevealed(rootsSpec.reveal);
    const roots = showRoots ? distinctRoots() : [];
    rootPts.forEach((p, n) => {
      if (n < roots.length) { p.moveTo([roots[n], target(roots[n])]); p.setAttribute({ visible: true }); }
      else p.setAttribute({ visible: false });
    });
    const badge = $("countBadge");
    badge.hidden = !showRoots;
    let sumOk = false;
    if (showRoots) {
      let label = rootsSpec.count_label.replace("{n}", roots.length);
      if (sumTarget) {
        sumOk = roots.length >= 2 && Math.abs(roots.reduce((a, c) => a + c, 0) - sumTarget(0)) < 1e-4;
        label += sumOk ? rootsSpec.sum_ok : rootsSpec.sum_no;
      }
      badge.textContent = label;
      badge.classList.toggle("two", sumTarget ? sumOk : roots.length === (rootsSpec.highlight ?? 2));
    }
    sliderSpecs.forEach((o) => {
      const row = $("row_" + o.id), out = $("out_" + o.id);
      row.hidden = !isRevealed(o.reveal);
      const numeric = o.readout === "numeric" || isRevealed(o.readout_reveal);
      out.textContent = numeric ? `${o.label} = ${state.vals[o.id]}` : "눈금 가림";
      out.classList.toggle("hidden-readout", !numeric);
    });
    board.update();
    return roots.length;
  }

  // ---------- 슬라이더 (여러 개) ----------
  sliderSpecs.forEach((o) => {
    const row = document.createElement("div");
    row.className = "slider-row"; row.id = "row_" + o.id; row.hidden = true;
    row.innerHTML = `<label for="sl_${o.id}">${o.label}</label><input type="range" id="sl_${o.id}">` +
      `<output id="out_${o.id}" class="hidden-readout">눈금 가림</output>`;
    $("sliders").appendChild(row);
    const el = row.querySelector("input");
    el.min = o.range[0]; el.max = o.range[1]; el.step = o.step; el.value = o.init;
    el.addEventListener("input", () => {
      state.vals[o.id] = Number(el.value);
      state.visited[o.id].push(state.vals[o.id]);
      const key = PN.map((n) => state.vals[n]).join(",");
      pointObjs.forEach((p) => { if (isRevealed(p.spec.reveal)) p.record(state.vals[o.id]); });
      const n = refreshBoard();
      const s = step();
      if (s && s.kind === "explore") {
        const c = s.checkpoint;
        if (c.type === "count-equals" && n === c.value) state.countHits.add(key);
        if (c.type === "near" && Math.abs(nearFn(c)()) < c.tol) state.nearHit = true;
        checkExplore();
      }
    });
  });
  const nearCache = new Map();
  function nearFn(c) {
    if (!nearCache.has(c)) { const g = compileP(c.expr, PN); nearCache.set(c, () => g(...PN.map((n) => state.vals[n]))); }
    return nearCache.get(c);
  }

  // ---------- 손 스케치 (개형 예측) ----------
  const sk = $("sketch");
  const ctx = sk.getContext("2d");
  let sketchOn = false, drawing = false, pts = [];
  let sketchCurve = null;
  function sizeCanvas() {
    const r = sk.getBoundingClientRect();
    sk.width = r.width * devicePixelRatio; sk.height = r.height * devicePixelRatio;
    ctx.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0);
    redrawSketch();
  }
  function redrawSketch() {
    const r = sk.getBoundingClientRect();
    ctx.clearRect(0, 0, r.width, r.height);
    if (!pts.length) return;
    ctx.strokeStyle = "#d9822b"; ctx.lineWidth = 3; ctx.lineJoin = ctx.lineCap = "round";
    ctx.beginPath(); pts.forEach((p, n) => (n ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]))); ctx.stroke();
  }
  function setSketch(on) {
    sketchOn = on; sk.classList.toggle("on", on);
    $("boardTip").textContent = on ? "왼쪽에서 오른쪽으로, 한 번에 이어서 그려 보세요. 다시 그리려면 '지우기'." : "";
    refreshBoard();
  }
  const pos = (e) => { const r = sk.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; };
  sk.addEventListener("pointerdown", (e) => { if (!sketchOn) return; drawing = true; pts = [pos(e)]; sk.setPointerCapture(e.pointerId); redrawSketch(); });
  sk.addEventListener("pointermove", (e) => { if (drawing) { pts.push(pos(e)); redrawSketch(); } });
  sk.addEventListener("pointerup", () => { drawing = false; });
  window.addEventListener("resize", sizeCanvas);

  // 스케치에서 개형 특징 추출: 극값(방향 전환) 개수, 양 끝 방향
  function analyzeSketch() {
    if (pts.length < 8) return null;
    const r = sk.getBoundingClientRect();
    const xs = pts.map((p) => p[0]);
    const x0 = Math.min(...xs), x1 = Math.max(...xs);
    if (x1 - x0 < r.width * 0.45) return { tooShort: true };
    const B = 32, bins = Array.from({ length: B }, () => []);
    for (const [px, py] of pts) bins[Math.min(B - 1, Math.floor(((px - x0) / (x1 - x0)) * B))].push(-py);
    let ys = bins.map((b) => (b.length ? b.reduce((a, c) => a + c, 0) / b.length : null));
    for (let n = 0; n < B; n++) if (ys[n] === null) ys[n] = ys[n - 1] ?? ys.find((y) => y !== null);
    ys = ys.map((_, n) => { const w = ys.slice(Math.max(0, n - 1), n + 2); return w.reduce((a, c) => a + c, 0) / w.length; });
    const span = Math.max(...ys) - Math.min(...ys);
    const th = span * 0.06;
    // 방향 전환: 지난 극점에서 th 이상 움직인 뒤 방향이 바뀌면 센다
    let dir = 0, ext = ys[0], turns = 0, firstDir = 0, lastDir = 0;
    for (let n = 1; n < B; n++) {
      const y = ys[n];
      if (dir >= 0 && y < ext - th) { if (dir > 0) turns++; dir = -1; ext = y; if (!firstDir) firstDir = -1; }
      else if (dir <= 0 && y > ext + th) { if (dir < 0) turns++; dir = 1; ext = y; if (!firstDir) firstDir = 1; }
      else if ((dir > 0 && y > ext) || (dir < 0 && y < ext)) ext = y;
      lastDir = dir;
    }
    return { turning_points: turns, ends: [firstDir > 0 ? "down" : "up", lastDir > 0 ? "up" : "down"], x0, x1 };
  }
  function freezeSketch() {
    if (!pts.length) return;
    const usr = pts.map(([px, py]) => new JXG.Coords(JXG.COORDS_BY_SCREEN, [px, py], board).usrCoords.slice(1));
    if (sketchCurve) board.removeObject(sketchCurve);
    sketchCurve = board.create("curve", [usr.map((p) => p[0]), usr.map((p) => p[1])], {
      strokeColor: M.orange, strokeOpacity: 0.7, strokeWidth: 2.5, dash: 2, highlight: false, fixed: true,
    });
    pts = []; redrawSketch();
  }

  // ---------- 단계 진행 ----------
  function clearTimers() { state.timers.forEach(clearTimeout); state.timers = []; }
  function startHintTimers(s, card) {
    (s.hints || []).forEach((h) => {
      const m = /^seconds:(\d+)$/.exec(h.after);
      if (m) state.timers.push(setTimeout(() => addHint(card, h.text), Number(m[1]) * 1000));
    });
  }
  function addHint(card, text) {
    if (!card.isConnected) return;
    const d = document.createElement("div");
    d.className = "hint"; d.innerHTML = "💡 " + md(text);
    card.querySelector(".hints").appendChild(d); tex(d);
  }
  function attemptHints(s, card) {
    (s.hints || []).forEach((h) => {
      const m = /^attempts:(\d+)$/.exec(h.after);
      if (m && Number(m[1]) === state.attempts) addHint(card, h.text);
    });
  }

  function complete(extraHistory) {
    const s = step();
    state.done.add(s.id);
    if (extraHistory) {
      const d = document.createElement("div");
      d.className = "item"; d.innerHTML = md(extraHistory);
      $("history").prepend(d); tex(d);
    }
    clearTimers();
    state.i++; state.attempts = 0;
    render();
  }

  const KIND_LABEL = { ask: "거꾸로 묻기", digest: "조건 뜯어보기", predict: "먼저 예측", explore: "직접 조작",
    notice: "알아차린 것 쓰기", compute: "계산", recall: "미룬 조건 꺼내기", synthesis: "종합법 풀이" };

  function render() {
    renderPolya(); renderTree(); refreshBoard();
    const s = step();
    const card = $("card");
    if (!s) { card.innerHTML = "<p>끝! 🎉</p>"; return; }
    const decisive = s.role === "decisive" ? " decisive" : "";
    card.innerHTML = `<span class="kind ${s.kind}${decisive}">${KIND_LABEL[s.kind]}</span>` +
      `<p class="prompt">${md(s.prompt || "")}</p><div class="body"></div><div class="hints"></div>`;
    const body = card.querySelector(".body");
    setSketch(false);
    (RENDER[s.kind] || (() => {}))(s, body, card);
    tex(card);
    startHintTimers(s, card);
    if (params.get("dev")) window.__state = state;
  }

  const btn = (label, cls, fn) => { const b = document.createElement("button"); b.textContent = label; b.className = cls || ""; b.onclick = fn; return b; };
  const row = (...els) => { const d = document.createElement("div"); d.className = "row"; els.forEach((e) => d.appendChild(e)); return d; };

  // 입력칸: 숫자(기본) · 식(expr) · 고르기(select)
  function makeFields(s, body) {
    const wrap = document.createElement("div"); wrap.className = "fields";
    const inputs = s.input.fields.map((fd) => {
      const l = document.createElement("label"); l.innerHTML = md(fd.label);
      let inp;
      if (fd.type === "select") {
        inp = document.createElement("select");
        inp.innerHTML = `<option value="">고르기…</option>` + fd.options.map((o, n) => `<option value="${n}">${o}</option>`).join("");
      } else {
        inp = document.createElement("input"); inp.type = "text"; inp.inputMode = fd.type === "expr" ? "text" : "decimal";
      }
      l.appendChild(inp); wrap.appendChild(l); return { inp, fd, accept: verifiedRef(fd.accept) };
    });
    body.appendChild(wrap);
    return inputs;
  }
  function fieldOk({ inp, fd, accept }) {
    if (fd.type === "select") return inp.value !== "" && fd.options[Number(inp.value)] === accept;
    if (fd.type === "expr") return sameExpr(inp.value, accept.replace(/\*\*/g, "^"), fd.var);
    return Math.abs(parseNum(inp.value) - parseNum(accept)) < 1e-9;
  }
  function fieldText({ inp, fd }) {
    return fd.type === "select" ? fd.options[Number(inp.value)] : inp.value.trim();
  }
  // select 의 option 안 수식은 KaTeX 가 못 그리므로 $ 를 걷어 읽기 쉬운 글자로
  function plainOptions(card) {
    card.querySelectorAll("option").forEach((o) => {
      o.textContent = o.textContent.replace(/\$/g, "").replace(/\\beta/g, "β").replace(/\\alpha/g, "α").replace(/\\,/g, " ");
    });
  }
  // 바로 앞이 조작 단계이고 그 앞이 예측이면: 조작 전 내 예측 vs 실제
  function predCompare() {
    const prev = G.path[state.i - 1], predStep = G.path[state.i - 2];
    if (!prev || prev.kind !== "explore" || !predStep || predStep.kind !== "predict") return "";
    const pv = state.predictions[predStep.id];
    if (pv === undefined) return "";
    const pk = predStep.predict.kind;
    const truth = pk === "sequence" ? predStep.predict.accept.values.join(" → ")
      : pk === "count" ? `${predStep.predict.accept.value}개` : predStep.predict.correct || "";
    const mine = Array.isArray(pv) ? pv.join(" → ") : typeof pv === "number" ? `${pv}개` : (typeof pv === "string" ? pv : "");
    return truth && mine ? `<div class="compare"><div class="mine"><h4>조작 전 내 예측</h4>${md(mine)}</div><div class="model"><h4>실제</h4>${md(truth)}</div></div>` : "";
  }
  function checkStep(s, body, card) {
    const inputs = makeFields(s, body);
    plainOptions(body);
    const msg = document.createElement("div"); msg.className = "msg";
    const done = (revealed) => {
      inputs.forEach(({ inp }) => { inp.disabled = true; });
      bar.remove();
      const d = document.createElement("div");
      d.innerHTML = predCompare() + `<div class="hint">${revealed ? "정답을 보고 넘어가요.<br>" : ""}${md(textRef(s.model))}</div>`;
      body.appendChild(d); tex(d);
      const mine = inputs.map((it) => `${it.fd.label} ${fieldText(it)}`).join(", ");
      body.appendChild(row(btn("다음", "primary", () => complete(s.history || `<b>${KIND_LABEL[s.kind]}</b> — ${mine}`))));
    };
    const bar = row(btn("확인", "primary", () => {
      state.attempts++;
      if (inputs.every(fieldOk)) { msg.className = "msg good"; msg.textContent = "맞아요!"; done(false); return; }
      msg.className = "msg bad"; msg.textContent = "다시 생각해 보세요.";
      attemptHints(s, card);
      if (state.attempts === 2) bar.appendChild(btn("답 보기", "ghost", () => {
        inputs.forEach((it) => { it.inp.value = it.fd.type === "select" ? String(it.fd.options.indexOf(it.accept)) : it.accept; });
        msg.textContent = ""; done(true);
      }));
    }));
    body.appendChild(bar); body.appendChild(msg);
  }

  const RENDER = {
    recall(s, body, card) { s.input ? checkStep(s, body, card) : RENDER.ask(s, body); },
    ask(s, body, card) {
      if (s.input) return checkStep(s, body, card);
      if (s.reveal_text) {
        const more = btn("생각해 봤어요 → 확인", "primary", () => {
          more.remove();
          const d = document.createElement("div"); d.className = "hint"; d.innerHTML = md(textRef(s.reveal_text));
          body.appendChild(d); tex(d);
          body.appendChild(row(btn("다음", "primary", () => complete(s.history || `<b>구하는 것</b> — ${G.understand.unknown}`))));
        });
        body.appendChild(row(more));
      } else {
        body.appendChild(row(btn("다음", "primary", () => complete())));
      }
    },

    digest(s, body) {
      const cond = G.understand.conditions.find((c) => c.id === s.condition);
      body.innerHTML = `<div class="hint">조건: ${md(cond.text)}</div>`;
      const ta = document.createElement("textarea"); ta.placeholder = "내 말로 바꿔 쓰기…";
      body.appendChild(ta);
      body.appendChild(row(btn("내 생각 제출", "primary", function () {
        if (!ta.value.trim()) { ta.focus(); return; }
        state.notes[s.id] = ta.value.trim();
        this.disabled = true; ta.disabled = true;
        const cmp = document.createElement("div"); cmp.className = "compare";
        cmp.innerHTML = `<div class="mine"><h4>내 요약</h4>${md(ta.value.trim())}</div><div class="model"><h4>이 조건의 결론</h4>${md(cond.digest)}</div>`;
        body.appendChild(cmp); tex(cmp);
        body.appendChild(row(btn("다음", "primary", () => complete(`<b>조건 뜯어보기</b> — ${cond.digest}`))));
      })));
    },

    predict(s, body, card) {
      const p = s.predict;
      if (p.kind === "shape") {
        setSketch(true);
        const msg = document.createElement("div"); msg.className = "msg";
        body.appendChild(row(
          btn("지우기", "ghost", () => { pts = []; redrawSketch(); msg.textContent = ""; }),
          btn("스케치 제출", "primary", () => {
            const a = analyzeSketch();
            if (!a) { msg.className = "msg bad"; msg.textContent = "먼저 캔버스에 곡선을 그려 주세요."; return; }
            if (a.tooShort) { msg.className = "msg bad"; msg.textContent = "조금 더 넓게(왼쪽에서 오른쪽 끝까지) 그려 주세요."; return; }
            state.attempts++;
            const ok = a.turning_points === p.accept.turning_points &&
              a.ends[0] === p.accept.ends[0] && a.ends[1] === p.accept.ends[1];
            state.predictions[s.id] = a;
            const mine = `봉우리·골짜기 ${a.turning_points}개, 왼쪽 끝 ${a.ends[0] === "down" ? "아래" : "위"}, 오른쪽 끝 ${a.ends[1] === "up" ? "위" : "아래"}`;
            if (ok || state.attempts >= p.max_attempts) {
              freezeSketch(); setSketch(false);
              const note = ok ? "개형이 맞았어요! 실제 곡선을 열게요." : "실제 곡선을 열어 볼게요. 내 스케치(점선)와 비교해 보세요.";
              complete(`<b>개형 예측</b> — ${mine} → ${note}`);
            } else {
              msg.className = "msg bad";
              msg.innerHTML = `내 스케치: ${mine}. 다시 생각해 볼까요?<br>💡 ${md(p.on_fail[Math.min(state.attempts - 1, p.on_fail.length - 1)])}`;
              tex(msg); pts = []; redrawSketch();
            }
          })));
        body.appendChild(msg);
      } else if (p.kind === "choice") {
        const opts = document.createElement("div"); opts.className = "opts";
        p.options.forEach((o) => opts.appendChild(btn(o, "", function () {
          state.predictions[s.id] = o;
          if (!s.explain) { complete(`<b>예측</b> — ${o}`); return; }
          opts.querySelectorAll("button").forEach((b) => { b.disabled = true; });
          this.classList.add("picked");
          const d = document.createElement("div"); d.className = "hint";
          d.innerHTML = (o === p.correct ? "맞아요! " : `실제로는 <b>${p.correct}</b>예요. `) + md(s.explain);
          body.appendChild(d); tex(d);
          body.appendChild(row(btn("다음", "primary", () => complete(`<b>예측</b> — ${o}`))));
        })));
        body.appendChild(opts);
      } else if (p.kind === "count") {
        const inp = document.createElement("input"); inp.type = "text"; inp.inputMode = "numeric"; inp.placeholder = "개수";
        body.appendChild(inp);
        body.appendChild(row(btn("예측 제출", "primary", () => {
          const n = parseNum(inp.value);
          if (!Number.isInteger(n) || n < 0) { inp.focus(); return; }
          state.predictions[s.id] = n;
          complete(`<b>개수 예측</b> — ${n}개`);
        })));
      } else if (p.kind === "sequence") {
        const inp = document.createElement("input"); inp.type = "text"; inp.placeholder = "예: 1, 3, 1";
        body.appendChild(inp);
        body.appendChild(row(btn("예측 제출", "primary", () => {
          const vals = inp.value.split(/[,\s→>-]+/).filter(Boolean).map(Number);
          if (!vals.length || vals.some(isNaN)) { inp.focus(); return; }
          state.predictions[s.id] = vals;
          complete(`<b>개수 순서 예측</b> — ${vals.join(" → ")}`);
        })));
      }
    },

    explore(s, body) {
      const st = document.createElement("div"); st.className = "msg"; st.id = "exploreStatus";
      body.appendChild(st);
      PN.forEach((n) => { state.visited[n] = []; }); state.countHits = new Set(); state.nearHit = false;
      updateExploreStatus();
      $("boardTip").textContent = "슬라이더를 드래그하거나, 클릭한 뒤 ← → 키로 한 칸씩 움직일 수 있어요.";
    },

    notice(s, body, card) {
      if (s.input) return checkStep(s, body, card);
      const ta = document.createElement("textarea"); ta.placeholder = "내가 본 것을 한 줄로…";
      body.appendChild(ta);
      body.appendChild(row(btn("내 생각 제출", "primary", function () {
        if (!ta.value.trim()) { ta.focus(); return; }
        state.notes[s.id] = ta.value.trim();
        this.disabled = true; ta.disabled = true;
        const extra = predCompare();
        const cmp = document.createElement("div");
        cmp.innerHTML = extra + `<div class="compare"><div class="mine"><h4>내가 쓴 것</h4>${md(ta.value.trim())}</div><div class="model"><h4>알아차릴 것</h4>${md(s.model)}</div></div>`;
        body.appendChild(cmp); tex(cmp);
        body.appendChild(row(btn("다음", "primary", () => complete(`<b>알아차림</b> — ${s.model}`))));
      })));
    },

    compute(s, body, card) {
      const inputs = makeFields(s, body);
      const msg = document.createElement("div"); msg.className = "msg";
      body.appendChild(row(btn("확인", "primary", () => {
        state.attempts++;
        const ok = inputs.every(fieldOk);
        if (ok) {
          const vals = inputs.map(({ inp }) => inp.value.trim()).join(", ");
          const label = s.input.fields.map((fd) => fd.label).join(", ");
          complete(`<b>계산</b> — ${md(label)}: ${vals}` + (s.on_success ? `<br>${s.on_success}` : ""));
        } else {
          msg.className = "msg bad"; msg.textContent = "다시 확인해 보세요.";
          attemptHints(s, card);
        }
      })));
      body.appendChild(msg);
    },

    synthesis(s, body) {
      body.innerHTML = `<p>발견한 것을 <b>정방향(종합법)</b>으로 정리하면 이렇게 돼요. 교과서·해설지의 풀이는 보통 이 모양이에요 — 발견의 과정은 이 안에 숨어 있죠.</p>` +
        `<ol class="syn">${G.synthesis.map((l) => `<li>${md(l)}</li>`).join("")}</ol>` +
        `<p class="msg good">정답 ${G.source.answer}</p>`;
      if (G.short) {
        // 쇼츠는 발견을 다 거친 뒤에만 연다 (먼저 보면 영상이 발견을 대신해 버린다)
        const src = (window.SHORTS && window.SHORTS[G.short]) || "videos/" + G.short;
        body.insertAdjacentHTML("beforeend", `<div class="short"><h4>🎬 쇼츠로 다시 보기</h4>` +
          `<video controls playsinline preload="metadata" src="${src}"></video></div>`);
      }
      body.appendChild(row(btn("처음부터 다시", "ghost", () => location.reload())));
    },
  };

  // ---------- explore 체크포인트 ----------
  function evalCheck(c) {
    if (c.all) return c.all.every(evalCheck);
    if (c.any) return c.any.some(evalCheck);
    if (c.type === "visited-range") return (state.visited[c.slider] || []).some((x) => x >= c.range[0] - 1e-9 && x <= c.range[1] + 1e-9);
    if (c.type === "near") return state.nearHit;
    if (c.type === "count-equals") return state.countHits.size >= (c.times || 1);
    return false;
  }
  function updateExploreStatus() {
    const s = step(); const st = $("exploreStatus");
    if (!st || !s || s.kind !== "explore" || state.done.has(s.id + ":passed")) return;
    const c = s.checkpoint;
    if (c.type === "count-equals") {
      st.className = "msg";
      st.textContent = state.countHits.size === 0 ? `개수가 ${c.value}가 되는 순간을 찾는 중…`
        : `찾은 순간: ${Math.min(state.countHits.size, c.times)}번 / ${c.times}번`;
    } else if (c.all) {
      const n = c.all.filter(evalCheck).length;
      st.className = "msg"; st.textContent = `구석구석 충분히 움직여 보세요 (${n}/${c.all.length})`;
    } else if (c.type === "near") {
      st.className = "msg"; st.textContent = "딱 맞는 순간을 찾는 중…";
    }
  }
  function checkExplore() {
    const s = step();
    updateExploreStatus();
    if (evalCheck(s.checkpoint) && !state.done.has(s.id + ":passed")) {
      const st = $("exploreStatus");
      st.className = "msg good"; st.textContent = "좋아요! 이제 본 것을 정리해 봅시다.";
      const card = $("card");
      card.querySelector(".body").appendChild(row(btn("다음", "primary", () => { $("boardTip").textContent = ""; complete(); })));
      state.done.add(s.id + ":passed");
    }
  }

  // 개발용: ?dev=1&to=<step-id> 로 해당 단계까지 건너뛰기
  if (params.get("dev") && params.get("to")) {
    const target = G.path.findIndex((s) => s.id === params.get("to"));
    for (let n = 0; n < target; n++) state.done.add(G.path[n].id);
    state.i = Math.max(0, target);
  }

  sizeCanvas();
  render();
})();
