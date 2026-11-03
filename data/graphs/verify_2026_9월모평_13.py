"""SymPy 검산: 2026 9월모평 공통 13번.

실행: .venv/bin/python -I data/graphs/verify_2026_9월모평_13.py
그래프(2026_9월모평_13.json)에 적힌 모든 수치 주장을 다시 계산하고 PASS/FAIL 을 출력한다.
"""
import json
import sys
from pathlib import Path

import sympy as sp

x, k, a = sp.symbols("x k a", real=True)

f = x**2 + 6 * x + 12
D = f**2 - k * (x + 2) * f              # 분모
g = sp.expand(f - k * (x + 2))          # 분모의 두 번째 인수 (직선과 포물선의 차)
expr = x**2 / D

claims = []


def claim(text, ok):
    claims.append({"claim": text, "ok": bool(ok)})
    print(("PASS " if ok else "FAIL ") + text)


# 1. f는 항상 양수 (꼭짓점 (-3, 3), 실근 없음)
vx = sp.solve(sp.diff(f, x), x)[0]
claim("f(x)=(x+3)^2+3, 꼭짓점 (-3, 3)", vx == -3 and f.subs(x, -3) == 3
      and sp.expand((x + 3)**2 + 3 - f) == 0)
claim("f(x)=0 의 실근 없음 (판별식 -12)", sp.discriminant(f, x) == -12
      and sp.solve(f, x) == [])
fmin = sp.minimum(f, x, sp.Reals)
claim("f(x)>0 (모든 실수 x): 최솟값 3", fmin == 3 and fmin > 0
      and sp.expand(f - 3 - (x + 3)**2) == 0)

# 2. 분모 인수분해
claim("분모 = f(x)·{f(x) - k(x+2)}", sp.expand(D - f * (f - k * (x + 2))) == 0)
claim("g(x)=f(x)-k(x+2) = x^2+(6-k)x+(12-2k)",
      sp.expand(g - (x**2 + (6 - k) * x + (12 - 2 * k))) == 0)

# 3. 직선 y=k(x+2) 는 항상 (-2, 0) 을 지난다
claim("직선 y=k(x+2) 는 k와 무관하게 (-2, 0) 을 지난다",
      sp.simplify((k * (x + 2)).subs(x, -2)) == 0)

# 4. 접하는 k: 판별식 (k-6)(k+2) = 0
disc = sp.factor(sp.discriminant(g, x))
claim("g의 판별식 = (k-6)(k+2)", sp.expand(disc - (k - 6) * (k + 2)) == 0)
tangent_ks = sorted(sp.solve(disc, k))
claim("접하는 k = -2, 6", tangent_ks == [-2, 6])

# 5. 접점
tp6 = sp.solve(g.subs(k, 6), x)
tpm2 = sp.solve(g.subs(k, -2), x)
claim("k=6 일 때 접점 x=0, (0, 12)", tp6 == [0] and f.subs(x, 0) == 12
      and sp.roots(sp.Poly(g.subs(k, 6), x)) == {0: 2})
claim("k=-2 일 때 접점 x=-4, (-4, 4)", tpm2 == [-4] and f.subs(x, -4) == 4
      and sp.roots(sp.Poly(g.subs(k, -2), x)) == {-4: 2})
claim("k=6 접선: f'(0)=6, 접선 y=6(x+2)", sp.diff(f, x).subs(x, 0) == 6
      and sp.expand(f.subs(x, 0) + 6 * x - 6 * (x + 2)) == 0)
claim("k=-2 접선: f'(-4)=-2, 접선 y=-2(x+2)", sp.diff(f, x).subs(x, -4) == -2
      and sp.expand(f.subs(x, -4) - 2 * (x + 4) + 2 * (x + 2)) == 0)

# 6. 교점 개수 표
def n_real_roots(kv):
    return len([r for r in sp.roots(sp.Poly(g.subs(k, kv), x)) if r.is_real])

table_ok = (n_real_roots(-3) == 2 and n_real_roots(-2) == 1
            and all(n_real_roots(kv) == 0 for kv in [-1, 0, 1, 2, 3, 4, 5])
            and n_real_roots(6) == 1 and n_real_roots(7) == 2)
claim("교점 개수: k<-2→2, k=-2→1, -2<k<6→0, k=6→1, k>6→2", table_ok)

# 7. 직선이 x=0 에서 포물선과 만나려면 k=6 뿐 (그때 이중근)
claim("g(0)=0 ⇔ k=6 (x=0 에서 만나면 반드시 k=6, 이중근)",
      sp.solve(g.subs(x, 0), k) == [6])

# 8. k=6 이면 식이 1/f(x) 로 약분되어 모든 a 에서 극한 존재
claim("k=6: x^2/분모 = 1/f(x)", sp.simplify(expr.subs(k, 6) - 1 / f) == 0)
claim("k=6: x→0 극한 = 1/12", sp.limit(expr.subs(k, 6), x, 0) == sp.Rational(1, 12))

# 9. k=-2 이면 a=-4 에서 극한이 존재하지 않음 (분자 16≠0, 분모 이중근)
lim_m2 = sp.limit(expr.subs(k, -2), x, -4)
claim("k=-2: a=-4 에서 극한 발산 (분자 16, 분모 (x+4)^2 f)",
      lim_m2 in (sp.oo, -sp.oo, sp.zoo) and (x**2).subs(x, -4) == 16)

# 10. 범위 안의 정수 예시: k=0 이면 분모가 0 이 되는 실수 없음
claim("k=0: 분모의 실근 없음 → 모든 a 에서 극한 존재",
      sp.solve(D.subs(k, 0), x) == [])
# 범위 밖 예시: k=7 이면 분모가 0 이 되는 a 가 있고 분자≠0 → 극한 없음
r7 = sp.solve(g.subs(k, 7), x)
claim("k=7: 분모의 실근 2개이고 그곳에서 분자≠0 → 극한 없음",
      len(r7) == 2 and all(r != 0 for r in r7))

# 11. 최종 답
in_open = [kv for kv in range(-10, 11) if -2 < kv < 6]
claim("-2<k<6 인 정수 7개 (-1,0,1,2,3,4,5)", in_open == [-1, 0, 1, 2, 3, 4, 5])
total = len(in_open) + 1
claim("정수 k 의 개수 = 8 (④)", total == 8)

# 결과 저장(JSON 의 verification 필드와 대조용)
out = {"tool": "sympy", "claims": claims}
print(json.dumps(out, ensure_ascii=False, indent=1))

gpath = Path(__file__).with_name("2026_9월모평_13.json")
if gpath.exists():
    graph = json.loads(gpath.read_text(encoding="utf-8"))
    same = graph.get("verification") == out
    print("verification 필드 일치:", same)
    if not same:
        graph["verification"] = out
        gpath.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")
        print("-> JSON verification 필드를 갱신했습니다.")

n_fail = sum(1 for c in claims if not c["ok"])
print(f"총 {len(claims)}개 주장, 실패 {n_fail}개")
sys.exit(1 if n_fail else 0)
