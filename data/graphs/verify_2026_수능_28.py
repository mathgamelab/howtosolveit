"""2026 수능 미적분 28번 — 발견 그래프의 모든 수치 주장을 SymPy로 검산한다.

실행: .venv/bin/python -I data/graphs/verify_2026_수능_28.py
"""
import json
import sys

import sympy as sp

x, s, t = sp.symbols("x s t", positive=True)

f = sp.Rational(1, 2) * x**2 - x + sp.log(1 + x)
fp = sp.diff(f, x)

claims = []


def check(claim, ok, detail=""):
    ok = bool(ok)
    claims.append({"claim": claim, "ok": ok})
    print(("PASS " if ok else "FAIL ") + claim + (f"   [{detail}]" if detail else ""))


# --- 1. f 의 개형 (predict 단계 정답) -------------------------------------
fp_simpl = sp.simplify(fp - x**2 / (1 + x))
check("f'(x) = x^2/(1+x)", fp_simpl == 0, str(sp.factor(fp)))
check("f(0) = 0, f'(0) = 0 (원점에서 정류점)", f.subs(x, 0) == 0 and fp.subs(x, 0) == 0)
# x > -1 에서 f' >= 0, 등호는 x=0 뿐  → 극값 없음, 증가
crit = sp.solve(sp.Eq(fp, 0), x)
check("f'(x)=0 의 해는 x=0 뿐 (극값 0개)", crit == [] or crit == [0], str(crit))
check("x>0 에서 f'(x) > 0 (증가)", all(fp.subs(x, v) > 0 for v in [sp.Rational(1, 10), 1, 3, 10]))
check("x→-1+ 에서 f→-∞ (왼쪽 끝 아래)", sp.limit(f, x, -1, "+") == -sp.oo)
check("x→∞ 에서 f→+∞", sp.limit(f, x, sp.oo) == sp.oo)
fpp = sp.diff(fp, x)
check("f''(x) = (x^2+2x)/(1+x)^2 → x>0 에서 아래로 볼록", sp.simplify(fpp - (x**2 + 2 * x) / (1 + x) ** 2) == 0
      and all(fpp.subs(x, v) > 0 for v in [1, 2]))

# --- 2. 수선의 발 H 와 접선의 y절편 T 사이의 거리 t = s f'(s) -----------------
fs = f.subs(x, s)
fps = fp.subs(x, s)
tangent = fps * (x - s) + fs
T_y = tangent.subs(x, 0)                 # 접선의 y절편
H_y = fs                                 # 수선의 발 (0, f(s))
dist = sp.simplify(H_y - T_y)
h = s**3 / (1 + s)
check("H(0,f(s)) 와 T(0, f(s)-s f'(s)) 의 거리 = s·f'(s)", sp.simplify(dist - s * fps) == 0, str(dist))
check("t = h(s) = s^3/(1+s)", sp.simplify(dist - h) == 0)
check("s>0 에서 H 가 T 보다 위 (s f'(s) > 0 → 거리는 양수)", all(dist.subs(s, v) > 0 for v in [sp.Rational(1, 2), 1, 2]))

# --- 3. 발견 1 체크포인트: 접선 기울기 1 ⇔ t = s ⇔ s = (1+√5)/2 ---------------
s_slope1 = [r for r in sp.solve(sp.Eq(fps, 1), s) if r.is_positive]
golden = (1 + sp.sqrt(5)) / 2
check("f'(s)=1 인 양수 s 는 (1+√5)/2 ≈ 1.618 하나", len(s_slope1) == 1 and sp.simplify(s_slope1[0] - golden) == 0,
      f"{s_slope1} ≈ {[float(v) for v in s_slope1]}")
check("그 s 에서 t = s (삼각형 HTP 가 이등변)", sp.simplify(h.subs(s, golden) - golden) == 0)
check("s=2 일 때 기울기 4/3, t = 8/3 = s·기울기", fps.subs(s, 2) == sp.Rational(4, 3) and h.subs(s, 2) == sp.Rational(8, 3))

# --- 4. h 의 개형과 단조성 → g = h^{-1} -----------------------------------------
hp = sp.simplify(sp.diff(h, s))
check("h'(s) = (2s^3+3s^2)/(1+s)^2", sp.simplify(hp - (2 * s**3 + 3 * s**2) / (1 + s) ** 2) == 0, str(hp))
check("s>0 에서 h'(s) > 0 (h 증가 → g 는 h 의 역함수)", all(hp.subs(s, v) > 0 for v in [sp.Rational(1, 10), 1, 3]))
hpp = sp.simplify(sp.diff(h, s, 2))
check("s>0 에서 h''(s) > 0 (아래로 볼록)", all(hpp.subs(s, v) > 0 for v in [sp.Rational(1, 10), 1, 3]), str(hpp))
check("h(0) = 0", h.subs(s, 0) == 0)
check("h(1) = 1/2  → g(1/2) = 1", h.subs(s, 1) == sp.Rational(1, 2))
check("h(3) = 27/4 → g(27/4) = 3", h.subs(s, 3) == sp.Rational(27, 4))
# 역함수가 하나로 정해지는지: t=1/2, 27/4 에서 양의 해가 유일한지
for tv, sv in [(sp.Rational(1, 2), 1), (sp.Rational(27, 4), 3), (sp.Rational(8, 3), 2)]:
    sols = [r for r in sp.solve(sp.Eq(h, tv), s) if r.is_real and r > 0]
    check(f"h(s) = {tv} 의 양의 실근은 s = {sv} 하나", len(sols) == 1 and sp.simplify(sols[0] - sv) == 0, str(sols))

# --- 5. 역함수 적분 = 직사각형 차 - 곡선 아래 넓이 -------------------------------
area_under_h = sp.integrate(h, (s, 1, 3))
check("∫_1^3 h(s) ds = 20/3 - ln 2", sp.simplify(area_under_h - (sp.Rational(20, 3) - sp.log(2))) == 0,
      str(sp.simplify(area_under_h)))
check("s^3/(1+s) = s^2 - s + 1 - 1/(1+s) (나눗셈)", sp.simplify(h - (s**2 - s + 1 - 1 / (1 + s))) == 0)
big_rect = 3 * sp.Rational(27, 4)
small_rect = 1 * sp.Rational(1, 2)
check("큰 직사각형 3·27/4 = 81/4", big_rect == sp.Rational(81, 4))
check("작은 직사각형 1·1/2 = 1/2", small_rect == sp.Rational(1, 2))
answer_geom = sp.simplify(big_rect - small_rect - area_under_h)

# 치환적분으로 독립 검산: ∫ g(t) dt = ∫_1^3 s h'(s) ds
answer_subst = sp.simplify(sp.integrate(s * sp.diff(h, s), (s, 1, 3)))
target = sp.Rational(157, 12) + sp.log(2)
check("∫_{1/2}^{27/4} g(t) dt = 81/4 - 1/2 - (20/3 - ln2) = 157/12 + ln 2 (넓이 관계)",
      sp.simplify(answer_geom - target) == 0, str(answer_geom))
check("치환 ∫_1^3 s h'(s) ds 도 157/12 + ln 2 (독립 검산)", sp.simplify(answer_subst - target) == 0, str(answer_subst))

# 수치 적분으로 한 번 더 (역함수를 직접 수치로 뒤집어서)
import mpmath as mp
mp.mp.dps = 30
def g_num(tv):
    return mp.findroot(lambda u: u**3 / (1 + u) - tv, 2)
num = mp.quad(g_num, [0.5, 6.75])
check("수치 적분 ∫ g(t) dt ≈ 13.7765 = 157/12 + ln2", abs(num - float(target)) < 1e-8, f"{num}")

# --- 6. 답지 매칭 -------------------------------------------------------------
options = {
    "①": sp.Rational(161, 12) + sp.log(3),
    "②": sp.Rational(40, 3) + sp.log(3),
    "③": sp.Rational(53, 4) + sp.log(2),
    "④": sp.Rational(79, 6) + sp.log(2),
    "⑤": sp.Rational(157, 12) + sp.log(2),
}
matches = [k for k, v in options.items() if sp.simplify(v - answer_geom) == 0]
check("정답은 ⑤ (다른 보기와 일치하지 않음)", matches == ["⑤"], str(matches))

print()
print(json.dumps({"tool": "sympy", "claims": claims}, ensure_ascii=False, indent=2))
n_fail = sum(1 for c in claims if not c["ok"])
print(f"\n{len(claims) - n_fail}/{len(claims)} PASS")
sys.exit(1 if n_fail else 0)
