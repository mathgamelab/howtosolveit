"""2026_6월모평 13번 검산 (SymPy).

실행: /Users/happyyoon/Documents/howtosolveit/.venv/bin/python -I verify_2026_6월모평_13.py
그래프 JSON의 모든 수치 주장을 다시 계산해 PASS/FAIL 을 찍는다.
"""
import json
import sys

import sympy as sp

x, k, t = sp.symbols("x k t", real=True)
R = sp.Rational

f = 3 * x**2 - 7 * x + 2
g = x / 3 - R(2, 3)
h = sp.expand(f - g)                      # 곡선 - 직선
H = sp.integrate(h, (x, 0, t))            # 부호 있는 넓이 누적기 S(t)

claims = []


def claim(text, ok):
    claims.append({"claim": text, "ok": bool(ok)})
    print(("PASS " if ok else "FAIL ") + text)


# --- understand / predict 단계 수치 ---
claim("f(x)=(3x-1)(x-2): f의 영점은 x=1/3, 2", sorted(sp.solve(f, x)) == [R(1, 3), 2])
claim("f의 y절편은 2", f.subs(x, 0) == 2)
claim("f의 꼭짓점 x=7/6, 최솟값 -25/12",
      sp.solve(sp.diff(f, x), x) == [R(7, 6)] and f.subs(x, R(7, 6)) == R(-25, 12))
claim("직선 y=x/3-2/3 은 기울기 1/3, x절편 2 (곡선과 직선이 모두 (2,0)을 지난다)",
      g.subs(x, 2) == 0 and f.subs(x, 2) == 0)

# --- 교점 ---
roots = sorted(sp.solve(h, x))
claim("곡선과 직선의 교점 x좌표는 4/9, 2", roots == [R(4, 9), 2])
claim("h(x)=f(x)-g(x)=3x^2-22x/3+8/3", sp.simplify(h - (3 * x**2 - R(22, 3) * x + R(8, 3))) == 0)
claim("부호: [0,4/9]에서 h>0, [4/9,2]에서 h<0, x>2에서 h>0",
      h.subs(x, R(2, 9)) > 0 and h.subs(x, 1) < 0 and h.subs(x, 3) > 0)

# --- 세 영역의 넓이 ---
A = sp.integrate(h, (x, 0, R(4, 9)))
B = sp.integrate(-h, (x, R(4, 9), 2))
C = sp.integrate(h, (x, 2, k))
claim("A = 400/729", sp.simplify(A - R(400, 729)) == 0)
claim("B = 1372/729", sp.simplify(B - R(1372, 729)) == 0)
claim("S(2) = A - B = -4/3", sp.simplify(H.subs(t, 2) - R(-4, 3)) == 0)
claim("A - B + C = ∫_0^k h(x)dx  (세 넓이의 부호합 = 정적분 하나)",
      sp.simplify((A - B + C) - sp.integrate(h, (x, 0, k))) == 0)

# --- 누적기 S(t)의 모양 (predict 2) ---
S = sp.expand(H)
claim("S(t) = t^3 - 11t^2/3 + 8t/3", sp.simplify(S - (t**3 - R(11, 3) * t**2 + R(8, 3) * t)) == 0)
crit = sorted(sp.solve(sp.diff(S, t), t))
claim("S'(t)=h(t): S는 t=4/9에서 극대(=A), t=2에서 극소(=A-B)",
      crit == [R(4, 9), 2] and S.subs(t, R(4, 9)) == A and S.subs(t, 2) == A - B)
claim("S(0)=0 이고 S(t)는 t=8/3 에서 다시 0 이 된다", S.subs(t, 0) == 0 and S.subs(t, R(8, 3)) == 0)

# --- 답 ---
eq = sp.factor(sp.integrate(h, (x, 0, k)))
claim("∫_0^k h dx = k(k-1)(3k-8)/3", sp.simplify(eq - k * (k - 1) * (3 * k - 8) / 3) == 0)
sols = sorted(sp.solve(sp.integrate(h, (x, 0, k)), k))
claim("∫_0^k h dx = 0 의 해는 k = 0, 1, 8/3", sols == [0, 1, R(8, 3)])
good = [s for s in sols if s > 2]
claim("k>2 인 해는 8/3 뿐", good == [R(8, 3)])
k_ans = R(8, 3)
C_val = C.subs(k, k_ans)
claim("k=8/3 일 때 C = 4/3 = 972/729", C_val == R(4, 3))
claim("k=8/3 일 때 A + C = B", sp.simplify(A + C_val - B) == 0)
choices = {"①": R(29, 12), "②": R(5, 2), "③": R(31, 12), "④": R(8, 3), "⑤": R(11, 4)}
claim("정답은 ④ 8/3", choices["④"] == k_ans)
claim("다른 선택지는 조건을 만족하지 않는다",
      all((A + C.subs(k, v) - B) != 0 for key, v in choices.items() if key != "④"))

# --- 딸깍 누수 점검: 정수 눈금만 보이면 선택지를 구별할 수 없다 ---
claim("S(2.5)<0, S(3)>0: 영점이 눈금 2와 3 사이에만 있어 눈금만으로는 ③④⑤ 구별 불가",
      S.subs(t, R(5, 2)) < 0 and S.subs(t, 3) > 0
      and all(R(5, 2) <= v <= 3 for v in (R(31, 12), R(8, 3), R(11, 4))))

n_fail = sum(1 for c in claims if not c["ok"])
print(f"\n{len(claims) - n_fail}/{len(claims)} PASS")
if "--json" in sys.argv:
    print(json.dumps({"tool": "sympy", "script": "verify_2026_6월모평_13.py",
                      "claims": claims}, ensure_ascii=False, indent=2))
sys.exit(1 if n_fail else 0)
