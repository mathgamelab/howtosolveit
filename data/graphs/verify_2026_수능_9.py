"""2026 수능 공통 9번 — 발견 그래프의 수치 주장을 SymPy로 검산.

실행:  .venv/bin/python -I data/graphs/verify_2026_수능_9.py
각 주장(claim)마다 PASS/FAIL 을 출력하고, 마지막에 JSON "verification" 필드에
그대로 넣을 수 있는 claims 배열을 출력한다.
"""
import json
import sympy as sp

x, a = sp.symbols("x a", real=True)
f = x**3 + 3 * a * x**2 - 9 * a**2 * x + 4
fp = sp.diff(f, x)
fpp = sp.diff(fp, x)

claims = []


def check(claim, ok):
    ok = bool(ok)
    claims.append({"claim": claim, "ok": ok})
    print(("PASS" if ok else "FAIL"), "-", claim)


# 1. 도함수 인수분해
check("f'(x) = 3(x+3a)(x-a)", sp.expand(fp - 3 * (x + 3 * a) * (x - a)) == 0)

# 2. 임계점과 극대/극소 판정 (a>0)
crit = sp.solve(sp.Eq(fp, 0), x)
check("임계점은 x=-3a, x=a 두 개", set(map(sp.simplify, crit)) == {-3 * a, a})
check("x=-3a 에서 극대 (f''<0, a>0)", sp.simplify(fpp.subs(x, -3 * a)) == -12 * a
      and sp.ask(sp.Q.negative(-12 * a), sp.Q.positive(a)))
check("x=a 에서 극소 (f''>0, a>0)", sp.simplify(fpp.subs(x, a)) == 12 * a
      and sp.ask(sp.Q.positive(12 * a), sp.Q.positive(a)))
check("a>0 이면 항상 극값이 2개 (판별식 4a^2+12a^2>0)",
      sp.simplify(sp.discriminant(fp, x) - 144 * a**2) == 0)

# 3. 극값 공식
fmax = sp.expand(f.subs(x, -3 * a))
fmin = sp.expand(f.subs(x, a))
check("극댓값 f(-3a) = 27a^3 + 4", sp.expand(fmax - (27 * a**3 + 4)) == 0)
check("극솟값 f(a) = 4 - 5a^3", sp.expand(fmin - (4 - 5 * a**3)) == 0)

# 4. 곡선은 a와 무관하게 (0,4)를 지난다; 극소점은 항상 y=4 아래, 극대점은 항상 위
check("모든 a에 대해 f(0)=4", sp.simplify(f.subs(x, 0)) == 4)
check("a>0 이면 극솟값 < 4 < 극댓값",
      sp.ask(sp.Q.negative(fmin - 4), sp.Q.positive(a))
      and sp.ask(sp.Q.positive(fmax - 4), sp.Q.positive(a)))
check("극솟값은 5가 될 수 없다 (4-5a^3=5 의 양수해 없음)",
      all(not (s.is_real and s > 0) for s in sp.solve(sp.Eq(fmin, 5), a)))

# 5. 접하는 조건: f(x)=5 와 f'(x)=0 의 공통해 (a>0)
sols = sp.solve([sp.Eq(f, 5), sp.Eq(fp, 0)], [x, a], dict=True)
pos = [s for s in sols if s[a].is_real and s[a] > 0]
check("y=5 가 접하는 양수 a 는 유일하게 a=1/3, 접점 x=-1",
      len(pos) == 1 and pos[0][a] == sp.Rational(1, 3) and pos[0][x] == -1)
check("극댓값=5 에서 a=1/3", sp.solve(sp.Eq(fmax, 5), a) and
      [s for s in sp.solve(sp.Eq(fmax, 5), a) if s.is_real] == [sp.Rational(1, 3)])

a0 = sp.Rational(1, 3)
f0 = f.subs(a, a0)
check("a=1/3 일 때 f(x)-5 = (x+1)^2 (x-1)  (이중근 = 접점)",
      sp.expand(f0 - 5 - (x + 1) ** 2 * (x - 1)) == 0)
check("a=1/3 일 때 변곡점 x=-a=-1/3 에서 f'(-1/3) = -4/3 ≠ 0 (수평접선 아님)",
      sp.simplify(fp.subs({a: a0, x: -a0})) == sp.Rational(-4, 3))
check("접점 (-1, 5) 는 극대점", f0.subs(x, -1) == 5 and -3 * a0 == -1)
check("a=1/3 일 때 극솟값 f(1/3) = 103/27 ≈ 3.815",
      f0.subs(x, a0) == sp.Rational(103, 27))

# 6. 교점 개수가 a 에 따라 1 → 2 → 3 으로 바뀐다
def n_real_roots(aval):
    return len(sp.Poly(f.subs(a, aval) - 5, x).real_roots())

check("a=0.3 : y=5 와 교점 1개", n_real_roots(sp.Rational(3, 10)) == 1)
check("a=1/3 : y=5 와 서로 다른 교점 2개", len(set(sp.Poly(f0 - 5, x).real_roots())) == 2)
check("a=0.4 : y=5 와 교점 3개", n_real_roots(sp.Rational(2, 5)) == 3)

# 7. 최종 답
check("f(2) = 14  → ④", f0.subs(x, 2) == 14)

# 8. 장면(scene) 수치: 슬라이더 범위 [0.1, 0.6] 에서 극점이 view 안에 들어오는가
#    s1 view = [-3, 11, 3, 1]  (xmin, ymax, xmax, ymin)
ok_view = True
for aval in [sp.Rational(1, 10), sp.Rational(1, 2), sp.Rational(3, 5)]:
    xm, ym = -3 * aval, fmax.subs(a, aval)
    xn, yn = aval, fmin.subs(a, aval)
    ok_view &= (-3 <= xm <= 3) and (1 <= ym <= 11) and (-3 <= xn <= 3) and (1 <= yn <= 11)
check("슬라이더 a∈[0.1,0.6] 에서 극대점·극소점이 view [-3,11,3,1] 안에 있다", ok_view)
check("초기값 a=0.5 : 극대점 (-1.5, 7.375), 극소점 (0.5, 3.375)",
      fmax.subs(a, sp.Rational(1, 2)) == sp.Rational(59, 8)
      and fmin.subs(a, sp.Rational(1, 2)) == sp.Rational(27, 8))
# 체크포인트 허용오차: 슬라이더 step 0.01 에서 a=0.33 의 극댓값과 5의 차이
gap = abs(fmax.subs(a, sp.Rational(33, 100)) - 5)
check("step 0.01 슬라이더의 a=0.33 에서 |극댓값-5| ≈ 0.030 < tolerance 0.08", gap < sp.Rational(8, 100))

print()
print("ALL PASS" if all(c["ok"] for c in claims) else "SOME FAILED")
print(json.dumps({"tool": "sympy", "claims": claims}, ensure_ascii=False, indent=2))
