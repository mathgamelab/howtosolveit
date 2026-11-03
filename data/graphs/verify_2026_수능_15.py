"""2026 수능 공통 15번 — 발견 그래프의 모든 수치 주장을 SymPy로 검산.

실행: .venv/bin/python -I data/graphs/verify_2026_수능_15.py
"""
import json
import sys

import sympy as sp

x, t = sp.symbols("x t", real=True)
a = sp.symbols("a", positive=True)

# 문제의 함수
f_left = -x**2            # x < 0
f_right = x**2 - x        # x >= 0
g_left = a * x + a        # x < -1
g_mid = sp.Integer(0)     # -1 <= x < 1
g_right = a * x - a       # x >= 1


def f_num(xv):
    return -xv**2 if xv < 0 else xv**2 - xv


def g_num(xv, av):
    if xv < -1:
        return av * xv + av
    if xv < 1:
        return 0
    return av * xv - av


def d_num(xv, av):
    """h'(x) = g(x) - f(x)"""
    return sp.nsimplify(g_num(xv, av) - f_num(xv))


def count_extrema(av, lo=-20, hi=20, step=sp.Rational(1, 100)):
    """h' = g - f 의 부호가 바뀌는 점의 개수 (격자 + 영점 근방 정밀 확인)."""
    # 후보 영점: 각 조각의 근
    cands = set()
    for expr, dom in [
        (g_left.subs(a, av) - f_left, lambda v: v < -1),
        (g_mid - f_left, lambda v: -1 <= v < 0),
        (g_mid - f_right, lambda v: 0 <= v < 1),
        (g_right.subs(a, av) - f_right, lambda v: v >= 1),
    ]:
        for r in sp.solve(sp.Eq(expr, 0), x):
            if r.is_real and dom(r):
                cands.add(sp.nsimplify(r))
    cands |= {sp.Integer(-1), sp.Integer(0), sp.Integer(1)}  # 조각 경계
    eps = sp.Rational(1, 1000)
    n = 0
    for c in sorted(cands):
        sl = sp.sign(d_num(c - eps, av))
        sr = sp.sign(d_num(c + eps, av))
        if sl * sr < 0:
            n += 1
    return n


claims = []


def check(claim, ok, detail=""):
    claims.append({"claim": claim, "ok": bool(ok)})
    print(("PASS" if ok else "FAIL"), "|", claim, ("| " + detail if detail else ""))


# 1. 전사 및 기본 성질
check("f는 x=0에서 연속 (f(0)=0)", sp.limit(f_left, x, 0, "-") == 0 and f_right.subs(x, 0) == 0)
check("f'(0-)=0, f'(0+)=-1 (원점에서 꺾임)", sp.diff(f_left, x).subs(x, 0) == 0 and sp.diff(f_right, x).subs(x, 0) == -1)
check("f는 [0,1]에서 x=1/2일 때 최솟값 -1/4", sp.solve(sp.diff(f_right, x), x) == [sp.Rational(1, 2)] and f_right.subs(x, sp.Rational(1, 2)) == -sp.Rational(1, 4))
check("f의 영점은 0, 1", set(sp.solve(f_right, x)) == {0, 1} and sp.solve(f_left, x) == [0])
check("g는 모든 a에 대해 x=-1, x=1에서 연속 (힌지 (-1,0),(1,0))",
      sp.simplify(g_left.subs(x, -1)) == 0 and sp.simplify(g_right.subs(x, 1)) == 0)

# 2. h' = g - f  (미적분의 기본정리)
h_expr_right = sp.integrate((g_right - f_right).subs(x, t), (t, 1, x))
check("h'(x)=g(x)-f(x) (x>1 조각에서 미분으로 확인)", sp.simplify(sp.diff(h_expr_right, x) - (g_right - f_right)) == 0)

# 3. 각 구간에서 g - f
d_left = sp.expand(g_left - f_left)      # x^2 + a x + a
check("x<-1: g-f = x^2+ax+a", sp.expand(d_left - (x**2 + a * x + a)) == 0)
disc = sp.discriminant(d_left, x)
check("x^2+ax+a 의 판별식 = a^2-4a, a=4에서 0", sp.expand(disc - (a**2 - 4 * a)) == 0 and disc.subs(a, 4) == 0)
check("a<4이면 왼쪽에서 g>f (교점 없음) — a=2 샘플", all(d_left.subs({a: 2, x: v}) > 0 for v in [-10, -3, -1.5, -1.01]))
dbl = sp.solve(d_left.subs(a, 4), x)
check("a=4일 때 접점 x=-2 (중근)", dbl == [-2])
check("접점 좌표 (-2,-4)", f_left.subs(x, -2) == -4 and g_left.subs({a: 4, x: -2}) == -4)
check("접점에서 기울기 일치: f'(-2)=4=a", sp.diff(f_left, x).subs(x, -2) == 4)
roots5 = sp.solve(d_left.subs(a, 5), x)
check("a=5이면 왼쪽 교점 2개가 모두 x<-1", len(roots5) == 2 and all(r < -1 for r in roots5))

d_mid_l = sp.expand(g_mid - f_left)      # x^2 on [-1,0)
d_mid_r = sp.expand(g_mid - f_right)     # x - x^2 on [0,1)
check("-1<=x<1 에서 g-f>=0, 영점은 x=0, x=1뿐",
      d_mid_l == x**2 and d_mid_r == x - x**2 and d_mid_r.subs(x, sp.Rational(1, 2)) > 0)
check("x=0에서 g=f이지만 부호 변화 없음 (극값 아님) — a=2",
      sp.sign(d_num(sp.Rational(-1, 100), 2)) == sp.sign(d_num(sp.Rational(1, 100), 2)) == 1)

d_right = sp.factor(g_right - f_right)
check("x>=1: g-f = (x-1)(a-x)", sp.expand(d_right - (x - 1) * (a - x)) == 0)
for av in [sp.Rational(1, 2), 1, 2, 4]:
    # 오른쪽(x>=1, 경계 x=1 포함)에서 부호 변화 1회
    cands = {sp.Integer(1), av} if av > 1 else {sp.Integer(1)}
    eps = sp.Rational(1, 1000)
    n = sum(1 for c in cands if sp.sign(d_num(c - eps, av)) * sp.sign(d_num(c + eps, av)) < 0)
    check(f"x>=1 쪽에서는 항상 가로지름 1회 (a={av})", n == 1)

# 4. 극값 개수 vs a
check("a=2: 극값 1개", count_extrema(2) == 1)
check("a=4: 극값 1개 (접점은 가로지름 아님)", count_extrema(4) == 1)
check("a=4.5: 극값 3개", count_extrema(sp.Rational(9, 2)) == 3)
check("a=5: 극값 3개", count_extrema(5) == 3)
check("a=1/2, a=1: 극값 1개", count_extrema(sp.Rational(1, 2)) == 1 and count_extrema(1) == 1)
check("k = 4", count_extrema(4) == 1 and count_extrema(sp.Rational(401, 100)) == 3)

# 5. a=4 일 때 h(3)
I1 = sp.integrate((g_mid - f_right).subs(x, t), (t, 0, 1))
I2 = sp.integrate((g_right.subs(a, 4) - f_right).subs(x, t), (t, 1, 3))
check("∫_0^1 (g-f) dt = 1/6", I1 == sp.Rational(1, 6))
check("∫_1^3 (g-f) dt = 10/3 (a=4)", I2 == sp.Rational(10, 3))
h3 = I1 + I2
check("h(3) = 7/2", h3 == sp.Rational(7, 2))
check("0<=x<=3 에서 g-f>=0 (h(3)은 순수 넓이)", all(d_num(sp.Rational(i, 10), 4) >= 0 for i in range(0, 31)))
ans = 4 + h3
check("k + h(3) = 15/2 (④)", ans == sp.Rational(15, 2))

# 6. 되돌아보기: a=4 일 때 h의 증감
check("a=4: x<4 에서 h'>=0, x>4 에서 h'<0 (x=4에서 유일한 극대)",
      all(d_num(sp.Rational(v, 10), 4) >= 0 for v in range(-100, 40))
      and all(d_num(sp.Rational(v, 10), 4) < 0 for v in range(41, 120)))
check("a=4: h'(-2)=h'(0)=h'(1)=0 이지만 부호 불변 (평평해질 뿐)",
      all(d_num(v, 4) == 0 for v in [-2, 0, 1]))

# a=4 일 때 h(x) 조각별 식 (s3 장면용)
h_mid_l = sp.integrate((g_mid - f_left).subs(x, t), (t, 0, x))                 # -1<=x<0
h_left = h_mid_l.subs(x, -1) + sp.integrate((g_left.subs(a, 4) - f_left).subs(x, t), (t, -1, x))  # x<-1
h_mid_r = sp.integrate((g_mid - f_right).subs(x, t), (t, 0, x))                # 0<=x<1
h_right = h_mid_r.subs(x, 1) + sp.integrate((g_right.subs(a, 4) - f_right).subs(x, t), (t, 1, x))  # x>=1
check("a=4: h(x) 조각식 — x<-1: x^3/3+2x^2+4x+2", sp.expand(h_left - (x**3 / 3 + 2 * x**2 + 4 * x + 2)) == 0)
check("a=4: h(x) 조각식 — -1<=x<0: x^3/3", sp.expand(h_mid_l - x**3 / 3) == 0)
check("a=4: h(x) 조각식 — 0<=x<1: x^2/2-x^3/3", sp.expand(h_mid_r - (x**2 / 2 - x**3 / 3)) == 0)
check("a=4: h(x) 조각식 — x>=1: -x^3/3+5x^2/2-4x+2", sp.expand(h_right - (-x**3 / 3 + sp.Rational(5, 2) * x**2 - 4 * x + 2)) == 0)
check("조각식으로 h(3)=7/2 재확인", h_right.subs(x, 3) == sp.Rational(7, 2))
check("a=4: h(4) = 14/3 (극댓값)", h_right.subs(x, 4) == sp.Rational(14, 3))

n_fail = sum(1 for c in claims if not c["ok"])
print(f"\n{len(claims)-n_fail}/{len(claims)} PASS")
if "--json" in sys.argv:
    print(json.dumps({"tool": "sympy", "script": "verify_2026_수능_15.py", "claims": claims}, ensure_ascii=False, indent=2))
sys.exit(1 if n_fail else 0)
