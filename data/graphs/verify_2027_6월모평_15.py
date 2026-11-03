"""2027 6월모평 15번 발견 그래프 검산 스크립트.

실행: .venv/bin/python -I data/graphs/verify_2027_6월모평_15.py
그래프(2027_6월모평_15.json)의 모든 수치 주장을 SymPy로 다시 계산하고 PASS/FAIL 을 찍는다.
"""
import json
import sys

import sympy as sp

x, a, p, q = sp.symbols("x a p q", real=True)

CLAIMS = []


def check(claim: str, ok: bool, detail: str = "") -> None:
    CLAIMS.append({"claim": claim, "ok": bool(ok)})
    print(f"[{'PASS' if ok else 'FAIL'}] {claim}" + (f"  ({detail})" if detail else ""))


def int_abs(expr, lo, hi):
    """구간 [lo,hi]에서 ∫|expr|dx. 실근으로 구간을 쪼개 각 조각의 |∫expr| 합."""
    lo, hi = sp.nsimplify(lo), sp.nsimplify(hi)
    roots = sorted({r for r in sp.Poly(expr, x).real_roots() if lo < r < hi})
    cuts = [lo] + list(roots) + [hi]
    return sum(sp.Abs(sp.integrate(expr, (x, cuts[i], cuts[i + 1]))) for i in range(len(cuts) - 1))


def differs(expr, lo, hi) -> bool:
    """∫|expr| ≠ |∫expr| 인가 (= 구간 안에서 부호가 바뀌는가)"""
    return sp.simplify(int_abs(expr, lo, hi) - sp.Abs(sp.integrate(expr, (x, lo, hi)))) != 0


def lit_p_set(expr, samples):
    """길이 3 창 [p,p+3]에 대해 differs 가 참인 p 표본 집합"""
    return {s for s in samples if differs(expr, s, s + 3)}


# ---------------------------------------------------------------- s1: 보기 함수 g
g = (x - 1) * (x - 5) / 2
samples = [sp.Rational(k, 2) for k in range(-8, 14)]  # -4 .. 6.5 step 0.5
expected = {s for s in samples if (-2 < s < 1) or (2 < s < 5)}
check("s1: g=(x-1)(x-5)/2, 창[p,p+3]에서 ∫|g|≠|∫g| ⟺ p∈(-2,1)∪(2,5)",
      lit_p_set(g, samples) == expected, "표본 p 0.5 간격")
check("s1: g의 영점 1,5 / 꼭짓점 x=3 / (1,5)에서 음",
      sp.solve(g, x) == [1, 5] and sp.solve(sp.diff(g, x), x) == [3] and g.subs(x, 3) < 0)

# ---------------------------------------------------------------- s2: 부호 변화점과 (가)
samples2 = [sp.Rational(k, 2) for k in range(-10, 16)]  # -5 .. 7.5


def p_set_is(expr, lo, hi):
    return lit_p_set(expr, samples2) == {s for s in samples2 if lo < s < hi}


f_shape = x**2 * (x - 3)
check("s2: f=x²(x-3) 이면 (가)의 p 범위가 정확히 0<p<3", p_set_is(f_shape, 0, 3))
check("s2: x(x-3)² 는 p 범위가 (-3,0) → (가) 불만족", p_set_is(x * (x - 3) ** 2, -3, 0))
check("s2: x³ 는 p 범위가 (-3,0) → (가) 불만족", p_set_is(x**3, -3, 0))
check("s2: x(x-1)(x-4) (초기 상태) 는 p 범위가 (-3,1)∪(1,4) (p=1에선 창의 양 끝이 근) → (가) 불만족",
      lit_p_set(x * (x - 1) * (x - 4), samples2) == {s for s in samples2 if (-3 < s < 1) or (1 < s < 4)})
check("s2: x(x-1)(x-3) 는 p 범위 (-3,3) → 부호 변화점이 2개 이상이면 길이>3", p_set_is(x * (x - 1) * (x - 3), -3, 3))

# 일반형 ax³+bx²+cx 에서 부호 변화점이 x=3 하나뿐 ⇒ 0이 중근 ⇒ f = a x²(x-3)
b, c = sp.symbols("b c", real=True)
F = a * x**3 + b * x**2 + c * x
sol = sp.solve([F.subs(x, 3), sp.diff(F, x).subs(x, 0)], [b, c], dict=True)[0]
check("s2: f(0)=0, f(3)=0, x=0 중근(f'(0)=0) ⇒ f(x)=a·x²(x-3)",
      sp.expand(F.subs(sol) - a * x**2 * (x - 3)) == 0, f"b={sol[b]}, c={sol[c]}")

# ---------------------------------------------------------------- s3: (나) 와 a
f_a = a * x**2 * (x - 3)
crit = sp.solve(sp.diff(f_a, x), x)
check("s3: f=a x²(x-3) 의 임계점은 x=0, x=2", set(crit) == {0, 2})
check("s3: f(2) = -4a (a>0이면 [0,3]에서의 최솟값)", sp.simplify(f_a.subs(x, 2) + 4 * a) == 0)
check("s3: a>0 이면 [0,3]에서 f≤0 (최댓값 0)",
      all(f_a.subs({a: 1, x: t}) <= 0 for t in [sp.Rational(k, 4) for k in range(13)]))

qs = [sp.Rational(k, 10) for k in range(-15, 26)]  # -1.5 .. 2.5


def q_set(aval):
    return {s for s in qs if differs(f_a.subs(a, aval) + s, 0, 3)}


check("s3: a=1/4 일 때 (나)의 q 범위가 정확히 0<q<1",
      q_set(sp.Rational(1, 4)) == {s for s in qs if 0 < s < 1})
check("s3: a=1/2 일 때 q 범위는 (0,2) → 끝점 = 4a",
      q_set(sp.Rational(1, 2)) == {s for s in qs if 0 < s < 2})
check("s3: a=-1/4 일 때 q 범위는 (-1,0) → 음수 쪽이므로 a<0 불가",
      q_set(-sp.Rational(1, 4)) == {s for s in qs if -1 < s < 0})
check("s3: 0<q<4a = 0<q<1 ⇒ a=1/4", sp.solve(sp.Eq(4 * a, 1), a) == [sp.Rational(1, 4)])

# ---------------------------------------------------------------- 최종
f_final = f_a.subs(a, sp.Rational(1, 4))
check("최종: f(x) = x²(x-3)/4 = (x³-3x²)/4", sp.expand(f_final - (x**3 - 3 * x**2) / 4) == 0)
check("최종: f 는 (가) 만족 (p 범위 (0,3))", p_set_is(f_final, 0, 3))
check("최종: f 는 (나) 만족 (q 범위 (0,1))", q_set(sp.Rational(1, 4)) == {s for s in qs if 0 < s < 1})
check("최종: 극솟값 f(2) = -1", f_final.subs(x, 2) == -1)
check("최종: f(6) = 27", f_final.subs(x, 6) == 27)
check("최종: 정답 ④ (27)", {"①": 18, "②": 21, "③": 24, "④": 27, "⑤": 30}["④"] == 27)

n_fail = sum(not c["ok"] for c in CLAIMS)
print(f"\n{len(CLAIMS) - n_fail}/{len(CLAIMS)} PASS")
if "--json" in sys.argv:
    print(json.dumps({"tool": "sympy", "script": "verify_2027_6월모평_15.py", "claims": CLAIMS},
                     ensure_ascii=False, indent=2))
sys.exit(1 if n_fail else 0)
