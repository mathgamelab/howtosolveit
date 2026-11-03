"""2025학년도 6월 모평 공통 7번 검산 (SymPy).

방정식 x^3 - 3x^2 - 9x + k = 0 의 서로 다른 실근의 개수가 2가 되는 모든 실수 k의 합.
실행: .venv/bin/python -I verify_2025_6월모평_7.py
"""
import json
import sys

import sympy as sp

x, k = sp.symbols("x k", real=True)
g = x**3 - 3 * x**2 - 9 * x          # k 를 분리한 삼차함수
f = g + k                            # 문제의 좌변

claims = []


def check(claim, ok, detail=""):
    ok = bool(ok)
    claims.append({"claim": claim, "ok": ok})
    print(f"[{'PASS' if ok else 'FAIL'}] {claim}" + (f"  ({detail})" if detail else ""))
    return ok


def distinct_real_roots(expr):
    roots = sp.Poly(expr, x).real_roots()
    return sorted(set(roots))


# --- 개형 예측(predict) 관련 ---
dg = sp.diff(g, x)
check("g'(x) = 3(x+1)(x-3)", sp.expand(dg - 3 * (x + 1) * (x - 3)) == 0, str(sp.factor(dg)))
crit = sorted(sp.solve(dg, x))
check("임계점 x = -1, 3", crit == [-1, 3], str(crit))
check("극값 개수 2", len(crit) == 2)
check("양 끝 거동 -∞→-∞, +∞→+∞ (end_behavior '-+')",
      sp.limit(g, x, -sp.oo) == -sp.oo and sp.limit(g, x, sp.oo) == sp.oo)
check("x=0 에서 감소 (g'(0) = -9 < 0)", dg.subs(x, 0) == -9)
check("원점을 지남 g(0)=0", g.subs(x, 0) == 0)
check("g 의 x절편 0, (3±3√5)/2 → k=0 일 때 실근 3개", len(distinct_real_roots(g)) == 3)

# --- 극값 ---
ddg = sp.diff(dg, x)
check("x=-1 은 극대 (g''(-1) < 0)", ddg.subs(x, -1) < 0)
check("x=3 은 극소 (g''(3) > 0)", ddg.subs(x, 3) > 0)
check("극댓값 g(-1) = 5", g.subs(x, -1) == 5, str(g.subs(x, -1)))
check("극솟값 g(3) = -27", g.subs(x, 3) == -27, str(g.subs(x, 3)))

# --- 접하는 순간의 k (중근 조건) ---
# f(x)=0 이 중근을 가질 조건: f 와 f' 의 공통근 ⇔ 판별식 = 0
disc = sp.discriminant(f, x)
k_tangent = sorted(sp.solve(disc, k))
check("판별식=0 인 k 는 -5, 27 두 개뿐", k_tangent == [-5, 27], str(k_tangent))
check("k=-5 ⇔ 극댓값이 x축에 닿음 (5 + k = 0)", sp.solve(5 + k, k) == [-5])
check("k=27 ⇔ 극솟값이 x축에 닿음 (-27 + k = 0)", sp.solve(-27 + k, k) == [27])
check("k=-5: f(x) = (x+1)^2 (x-5)", sp.expand(f.subs(k, -5) - (x + 1)**2 * (x - 5)) == 0)
check("k=27: f(x) = (x-3)^2 (x+3)", sp.expand(f.subs(k, 27) - (x - 3)**2 * (x + 3)) == 0)
check("k=-5 일 때 서로 다른 실근 개수 2 ({-1, 5})",
      distinct_real_roots(f.subs(k, -5)) == [-1, 5])
check("k=27 일 때 서로 다른 실근 개수 2 ({-3, 3})",
      distinct_real_roots(f.subs(k, 27)) == [-3, 3])

# --- 슬라이더 예측: k 를 올릴 때 개수 1→2→3→2→1 ---
samples = [-40, -5, 0, 10, 27, 40]
counts = [len(distinct_real_roots(f.subs(k, kv))) for kv in samples]
check("k = -40, -5, 0, 10, 27, 40 에서 개수 = 1,2,3,2,1 순서 (3→2→1 전이는 접할 때만)",
      counts == [1, 2, 3, 3, 2, 1], f"counts={counts}")
# 접하는 k 이외의 모든 k 에서 개수는 1 또는 3 (= 2 는 오직 두 점에서만)
interior_ok = all(len(distinct_real_roots(f.subs(k, kv))) == 3 for kv in [-4.9, -1, 15, 26.9])
exterior_ok = all(len(distinct_real_roots(f.subs(k, kv))) == 1 for kv in [-5.1, -20, 27.1, 60])
check("-5 < k < 27 이면 3개, k < -5 또는 k > 27 이면 1개", interior_ok and exterior_ok)

# --- 최종 답 ---
total = sum(k_tangent)
check("모든 k 의 합 = 22", total == 22, str(total))
check("정답 ④ (22)", total == 22)

# --- 장면(scene) 수치 ---
check("슬라이더 range [-40, 40], step 1 로 k=-5, 27 이 격자점 위에 있음",
      all((kv + 40) % 1 == 0 and -40 <= kv <= 40 for kv in k_tangent))
check("view [-4, 40, 6, -45] 안에 두 극점 (-1,5), (3,-27) 과 x절편 -3, -1, 3, 5 가 들어감",
      all(-4 <= px <= 6 and -45 <= py <= 40 for px, py in [(-1, 5), (3, -27), (-3, 0), (-1, 0), (3, 0), (5, 0)]))

all_ok = all(c["ok"] for c in claims)
print()
print("ALL PASS" if all_ok else "SOME FAIL")
print(json.dumps({"tool": "sympy", "claims": claims}, ensure_ascii=False, indent=2))
sys.exit(0 if all_ok else 1)
