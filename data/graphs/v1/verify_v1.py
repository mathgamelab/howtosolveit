"""스키마 v1 발견 그래프 검사기.

사용법: .venv/bin/python -I data/graphs/v1/verify_v1.py data/graphs/v1/<id>.json

1. verified 블록의 수치를 SymPy로 재계산한다 (문항별 검사 함수).
2. JSON 안의 모든 "$verified.*" 참조가 실제 키인지 확인한다.
3. leak_guard 규칙(곡선 공개 순서, 눈금 공개 시점, explore 뒤 notice, 식 노출)을 검사한다.
"""
import json
import re
import sys

import sympy as sp

x, k, a = sp.symbols("x k a", real=True)


def check(name, ok, results):
    results.append((name, bool(ok)))


def math_2025_6_7(v, results):
    f = sp.sympify(v["f"], locals={"x": x})
    crit = sorted(sp.solve(sp.diff(f, x), x))
    check("임계점 = critical_x", [str(c) for c in crit] == v["critical_x"], results)
    lmax, lmin = f.subs(x, crit[0]), f.subs(x, crit[1])
    check("극댓값 = local_max", str(lmax) == v["local_max"], results)
    check("극솟값 = local_min", str(lmin) == v["local_min"], results)
    check("봉우리 접함 k = -극댓값", str(-lmax) == v["k_max_touch"], results)
    check("골짜기 접함 k = -극솟값", str(-lmin) == v["k_min_touch"], results)
    disc_k = sorted(sp.solve(sp.discriminant(f + k, x), k))
    check("판별식=0 인 k = k_values", [str(r) for r in disc_k] == v["k_values"], results)

    def distinct_roots(kv):
        return len(set(sp.Poly(f + kv, x).real_roots()))

    seq = [distinct_roots(kv) for kv in (-40, -5, 0, 27, 40)]
    check("개수 순서 1,2,3,2,1", seq == v["count_sequence"], results)
    total = sum(sp.Integer(s) for s in v["k_values"])
    check("합 = answer_value", str(total) == v["answer_value"], results)
    return {"slider_values_needed": [int(s) for s in v["k_values"]]}


def math_2026_su_9(v, results, g):
    f = sp.sympify(v["f"], locals={"x": x, "a": a})
    fp = sp.factor(sp.diff(f, x))
    crit = sp.solve(sp.diff(f, x), x)
    xl, xr = sp.sympify(v["x_left"], locals={"a": a}), sp.sympify(v["x_right"], locals={"a": a})
    pos = {a: sp.Rational(1, 2)}
    check("f'=0 의 근 = x_left, x_right", set(crit) == {xl, xr} and xl.subs(pos) < xr.subs(pos), results)
    lmax, lmin = sp.expand(f.subs(x, xl)), sp.expand(f.subs(x, xr))
    check("극댓값 = local_max", sp.simplify(lmax - sp.sympify(v["local_max"], locals={"a": a})) == 0, results)
    check("극솟값 = local_min", sp.simplify(lmin - sp.sympify(v["local_min"], locals={"a": a})) == 0, results)
    check("f(0)=4 (a와 무관)", f.subs(x, 0) == 4, results)
    ap = sp.symbols("ap", positive=True)
    check("a>0 이면 극솟값 < 4 < 극댓값", sp.simplify(lmin.subs(a, ap) - 4).is_negative and sp.simplify(lmax.subs(a, ap) - 4).is_positive, results)
    sols = [s_ for s_ in sp.solve(sp.Eq(lmax, 5), a) if s_.is_real and s_ > 0]
    check("극댓값=5 인 양수 a = a_value", [str(s_) for s_ in sols] == [v["a_value"]], results)
    check("극솟값=5 인 양수 a 없음", [s_ for s_ in sp.solve(sp.Eq(lmin, 5), a) if s_.is_real and s_ > 0] == [], results)
    av = sp.Rational(v["a_value"])
    tx, ty = [sp.Integer(t) for t in v["tangent_point"]]
    check("접점 tangent_point (중근)", sp.factor(f.subs(a, av) - 5) == (x + 1) ** 2 * (x - 1) and xl.subs(a, av) == tx, results)
    nroots = lambda av_: len(set(sp.Poly(f.subs(a, av_) - 5, x).real_roots()))
    check("a=1/2 에서 y=5 와 교점 3개 = count_at_half", nroots(sp.Rational(1, 2)) == v["count_at_half"], results)
    check("교점 개수 a=0.3→1, 1/3→2, 0.4→3", [nroots(sp.Rational(3, 10)), nroots(av), nroots(sp.Rational(2, 5))] == [1, 2, 3], results)
    check("f(2) = answer_value", str(f.subs({a: av, x: 2})) == v["answer_value"], results)
    # 슬라이더 격자 위에는 정확히 1/3 이 없으므로, touch_tol 안에서 접함으로 잡히는 격자값이 있어야 한다
    sc = g["scenes"]["s1"]
    sl = next(o for o in sc["objects"] if o["type"] == "slider")
    tol = next(o for o in sc["objects"] if o["type"] == "intersections")["touch_tol"]
    n = round((sl["range"][1] - sl["range"][0]) / sl["step"])
    grid = [sl["range"][0] + i * sl["step"] for i in range(n + 1)]
    hits = [gv for gv in grid if abs(float(lmax.subs(a, gv)) - 5) < tol]
    check(f"격자 위 접함 판정값 존재 ({', '.join(f'{h:.3f}' for h in hits)})", 0 < len(hits) <= 3, results)
    check("골짜기는 격자 어디서도 touch_tol 안에 들지 않음", all(abs(float(lmin.subs(a, gv)) - 5) >= tol for gv in grid), results)
    check("view 안에 극점 자취가 들어감", all(sc["view"]["y"][0] < float(e.subs(a, gv)) < sc["view"]["y"][1] for gv in grid for e in (lmax, lmin)), results)
    return {"slider_values_needed": []}


def math_2025_10_g1_30(v, results, g):
    p, q, m, t, X = sp.symbols("p q m t X", real=True)
    f = lambda z: sp.Rational(1, 2) * (z - p) ** 2 + q
    gg = lambda z: -f(z - m)
    sol = {p: sp.Integer(v["p"]), q: sp.Integer(v["q"]), m: sp.Integer(v["m"])}
    ab = sorted(sp.solve(sp.Eq(f(x), gg(x)).subs(sol), x))
    check("α, β = alpha, beta", [str(r) for r in ab] == [v["alpha"], v["beta"]], results)
    al, be = ab
    check("f(m)+g(m) = -4", sp.simplify((f(m) + gg(m)).subs(sol)) == -4, results)
    check("g(p) = h(β) = 아래 끝", gg(p).subs(sol) == f(be).subs(sol) == sp.Integer(v["band"][0]), results)
    check("g 꼭짓점 높이 -q = 5 = 위 끝", (-q).subs(sol) == sp.Integer(v["band"][1]), results)
    check("β = p + 2m", be == (p + 2 * m).subs(sol), results)

    # h(x)=t 의 서로 다른 실근을 직접 세어, 합이 4p+2m 인 t 의 범위가 정확히 (3, 5) 인지 확인
    fs, gs = f(x).subs(sol), gg(x).subs(sol)

    def roots_h(tv):
        rs = set()
        for r in sp.solve(sp.Eq(fs, tv), x):
            if r.is_real and (r <= al or r >= be):
                rs.add(sp.nsimplify(r))
        for r in sp.solve(sp.Eq(gs, tv), x):
            if r.is_real and al < r < be:
                rs.add(sp.nsimplify(r))
        return rs

    target = (4 * p + 2 * m).subs(sol)
    ok_ts = []
    for i in range(-24, 41):
        tv = sp.Rational(i, 4)
        rs = roots_h(tv)
        if len(rs) >= 2 and sp.simplify(sum(rs) - target) == 0:
            ok_ts.append(tv)
    check("합=4p+2m 인 t (1/4 간격) 가 정확히 3<t<5", ok_ts and min(ok_ts) == sp.Rational(13, 4) and max(ok_ts) == sp.Rational(19, 4)
          and all(len(roots_h(tv)) == 4 for tv in ok_ts), results)
    check("t=3, t=5 경계에서는 조건 불만족", all(sp.simplify(sum(roots_h(tv)) - target) != 0 or len(roots_h(tv)) < 2 for tv in (3, 5)), results)

    # 연립의 유일성: -q=5, β=p+2m 이 f=g 의 근, f(m)+g(m)=-4, p>0, m>0
    eqs = [sp.Eq(q, -5), sp.Eq(f(p + 2 * m), gg(p + 2 * m)), sp.Eq(f(m) + gg(m), -4)]
    sols = [s_ for s_ in sp.solve(eqs, [p, q, m], dict=True) if s_[p] > 0 and s_[m] > 0]
    check("연립의 해가 유일", len(sols) == 1 and sols[0] == sol, results)
    check("m(p-q) = answer_value", str((m * (p - q)).subs(sol)) == v["answer_value"], results)

    # 예시 장면 (p=2, q=-4): β 가 점선 g(p) 에 올라가는 m = 4/sqrt(5), 슬라이더 격자에서 tol 안에 잡히는지
    ex = {p: 2, q: -4}
    mm = sp.symbols("mm", positive=True)
    beta_ex = sp.solve(sp.Eq(f(x).subs(ex), gg(x).subs(ex).subs(m, mm)), x)
    beta_ex = max(beta_ex, key=lambda r: float(r.subs(mm, 2)))
    mirror = [s_ for s_ in sp.solve(sp.Eq(beta_ex, 2 + 2 * mm), mm)]
    check("예시에서 β=p+2m 되는 m = 4/sqrt(5)", [sp.simplify(s_) for s_ in mirror] == [sp.sympify(v["example"]["m_mirror"])], results)
    sc = g["scenes"]["s1"]
    sl = next(o for o in sc["objects"] if o["id"] == "m")
    e_beta = next(s_ for s_ in g["path"] if s_["id"] == "e_beta")["checkpoint"]
    expr = sp.sympify(e_beta["expr"].replace("Math.sqrt", "sqrt").replace("^", "**"), locals={"m": mm})
    gap = sp.simplify(expr - (gg(2).subs(ex).subs(m, mm) - gg(beta_ex).subs(ex).subs(m, mm)))
    check("e_beta 식 = g(p) - g(β) (예시)", gap == 0, results)
    n = round((sl["range"][1] - sl["range"][0]) / sl["step"])
    hits = [sl["range"][0] + i * sl["step"] for i in range(n + 1) if abs(float(expr.subs(mm, sl["range"][0] + i * sl["step"]))) < e_beta["tol"]]
    check(f"m 격자에서 β 맞춤 판정값 ({', '.join(f'{h_:.2f}' for h_ in hits)})", 1 <= len(hits) <= 4, results)
    check("m 범위 전체에서 f=g 가 두 실근 (8-m²/4>0)", sl["range"][1] ** 2 / 4 < 8, results)
    return {"slider_values_needed": []}


MATH = {"2025_6월모평_공통_7": math_2025_6_7, "2026_수능_공통_9": math_2026_su_9, "2025_10월학평_고1_30": math_2025_10_g1_30}


def refs(obj, out):
    if isinstance(obj, dict):
        for val in obj.values():
            refs(val, out)
    elif isinstance(obj, list):
        for val in obj:
            refs(val, out)
    elif isinstance(obj, str):
        out += re.findall(r"\$verified\.([A-Za-z_]+)", obj)
    return out


def leak_checks(g, results, extra):
    steps = [s["id"] for s in g["path"]]
    pos = {sid: i for i, sid in enumerate(steps)}
    kinds = {s["id"]: s["kind"] for s in g["path"]}

    for i, s in enumerate(g["path"]):
        if s["kind"] == "explore":
            nxt = g["path"][i + 1]["kind"] if i + 1 < len(g["path"]) else None
            check(f"{s['id']}: explore 뒤에 notice", nxt == "notice", results)

    for sc_id, sc in g["scenes"].items():
        for o in sc["objects"]:
            rv = o.get("reveal", "always")
            if o["type"] == "function" and o.get("role") not in ("guide", "fixed"):
                ok = isinstance(rv, str) and rv.startswith("after:") and kinds.get(rv[6:]) == "predict"
                check(f"{o['id']}: 곡선은 predict 단계 뒤에 공개", ok, results)
            if o["type"] == "slider":
                if o.get("readout") != "numeric":
                    rr = o.get("readout_reveal", "never")
                    if rr.startswith("after:"):
                        target = rr[6:]
                        # 눈금은 값을 구하는 compute 단계 이후에만 열린다
                        first_compute = min(pos[s["id"]] for s in g["path"] if s["kind"] == "compute")
                        check(f"{o['id']}: 눈금은 compute 이후 공개", pos[target] >= first_compute, results)
                step = o.get("step")
                need = extra.get("slider_values_needed", [])
                lo = o["range"][0]
                on_grid = all(abs(((vv - lo) / step) - round((vv - lo) / step)) < 1e-9 for vv in need)
                check(f"{o['id']}: 특수값이 슬라이더 격자 위", step is not None and on_grid, results)

    student_text = json.dumps([s.get("prompt", "") for s in g["path"]] + [h["text"] for s in g["path"] for h in s.get("hints", [])], ensure_ascii=False)
    for sc in g["scenes"].values():
        for o in sc["objects"]:
            if "expr" in o and o.get("role") not in ("guide", "fixed"):
                check(f"{o['id']}: expr 원문이 학생 문구에 없음", o["expr"] not in student_text, results)
    for key in g.get("leak_guard", {}).get("answer_keys", ["k_max_touch", "k_min_touch", "answer_value"]):
        val = g["verified"][key]
        bad = re.search(rf"(?<![\d.]){re.escape(val)}(?![\d.])", student_text) is not None
        check(f"정답값 {key}={val} 이 프롬프트·힌트에 없음", not bad, results)


def main(path):
    g = json.load(open(path, encoding="utf-8"))
    results = []
    fn = MATH[g["id"]]
    extra = fn(g["verified"], results, g) if fn.__code__.co_argcount == 3 else fn(g["verified"], results)
    for r in sorted(set(refs(g, []))):
        check(f"$verified.{r} 참조 존재", r in g["verified"], results)
    leak_checks(g, results, extra)
    fails = 0
    for name, ok in results:
        print(("PASS " if ok else "FAIL ") + name)
        fails += not ok
    print(f"\n{len(results) - fails}/{len(results)} PASS")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main(sys.argv[1])
