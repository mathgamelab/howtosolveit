"""쇼츠 시안 #3 — 2025학년도 10월 고1 전국연합학력평가 30번 (발견 해설)

흐름 (폴리아): 구하는 것(미지수 셋 → 식 셋) → g 만들기 → h = 위에 있는 것 → t를 내리며 발견
            → 범위 양 끝 = 식 두 개 → 이제야 계산
p, q 는 모르는 값이므로 장면은 예시 값 p=2, q=-4 로 구조를 보여 준다.
렌더:
  cd shorts && PATH=/Library/TeX/texbin:$PATH ../.venv/bin/manim -r 1080,1920 --fps 30 s03_2025_10_g1_30.py Short03
"""
import numpy as np
from manim import *

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.background_color = "#101418"

KO = "AppleSDGothicNeo"
BLUE_C_ = "#5aa2ff"
ORANGE_ = "#ffa94d"
GREEN_ = "#51cf66"
RED_ = "#ff6b6b"
MUTED = "#9aa4ae"

P, Q = 2.0, -4.0   # 예시 값
Y_LO, Y_HI = -6, 8


def ko(s, size=40, color=WHITE, weight=NORMAL):
    return Text(s, font=KO, font_size=size, color=color, weight=weight)


def f(x):
    return 0.5 * (x - P) ** 2 + Q


def g(x, m):
    return -0.5 * (x - P - m) ** 2 - Q


def h(x, m):
    return max(f(x), g(x, m))


def ab(m):
    d = np.sqrt(-2 * Q - m * m / 4)
    return P + m / 2 - d, P + m / 2 + d


def roots_h(t, m):
    a, b = ab(m)
    rs = []
    if t >= Q:
        s = np.sqrt(2 * (t - Q))
        rs += [r for r in (P - s, P + s) if r <= a + 1e-9 or r >= b - 1e-9]
    if t <= -Q:
        s = np.sqrt(2 * (-Q - t))
        rs += [r for r in (P + m - s, P + m + s) if a < r < b]
    out = []
    for r in sorted(rs):
        if not out or abs(r - out[-1]) > 1e-6:
            out.append(r)
    return out


class Short03(Scene):
    def construct(self):
        # ---------- 0. 훅 ----------
        tag = ko("2025학년도 10월 고1 학평 · 30번", 30, MUTED).to_edge(UP, buff=0.9)
        hook = VGroup(
            ko("식이 하나뿐인데", 54, weight=BOLD),
            ko("미지수는 셋?", 54, ORANGE_, weight=BOLD),
        ).arrange(DOWN, buff=0.3).shift(UP * 3.4)
        prob = VGroup(
            MathTex(r"f(x)=\tfrac12(x-p)^2+q", font_size=50),
            MathTex(r"g(x)=-f(x-m)", font_size=50),
            MathTex(r"h=\begin{cases} f & (x\le\alpha,\ x\ge\beta)\\ g & (\alpha<x<\beta)\end{cases}", font_size=46),
            ko("h(x)=t 의 근이 2개 이상, 합이 4p+2m인 t의 범위", 28),
            MathTex(r"g(p)<t<5", font_size=52, color=ORANGE_),
            MathTex(r"f(m)+g(m)=-4,\quad m(p-q)=?", font_size=48),
        ).arrange(DOWN, buff=0.32).next_to(hook, DOWN, buff=0.7)
        self.play(FadeIn(tag), Write(hook), run_time=1.4)
        self.play(FadeIn(prob, shift=UP * 0.3), run_time=1.2)
        self.wait(1.6)

        # ---------- 1. 이해: 구하는 것 ----------
        step1 = ko("① 구하는 것부터", 36, BLUE_C_, weight=BOLD).to_edge(UP, buff=1.6)
        say = VGroup(
            ko("m, p, q 셋을 알아야 한다 → 식 3개 필요", 32),
            ko("보이는 등식은 f(m)+g(m)=−4 하나뿐", 32),
            ko("범위의 '양 끝'이 나머지 두 식!", 34, ORANGE_, weight=BOLD),
        ).arrange(DOWN, buff=0.35).next_to(prob, DOWN, buff=0.6)
        hl = SurroundingRectangle(prob[4], color=ORANGE_, buff=0.12)
        self.play(FadeOut(hook), FadeIn(step1))
        for line in say:
            self.play(FadeIn(line, shift=UP * 0.2), run_time=0.7)
            self.wait(0.5)
        self.play(Create(hl))
        self.wait(1.2)
        self.play(FadeOut(VGroup(prob, say, hl, step1)))

        # ---------- 2. g 만들기 ----------
        step2 = ko("② 그림부터 — 일단 p=2, q=−4로", 34, BLUE_C_, weight=BOLD).to_edge(UP, buff=1.6)
        axes = Axes(
            x_range=[-3, 9.5, 1], y_range=[Y_LO, Y_HI, 2], x_length=8.2, y_length=8.6,
            axis_config={"color": GREY_B, "include_ticks": True, "tick_size": 0.05},
            x_axis_config={"numbers_to_include": [-2, 2, 4, 6, 8], "font_size": 24},
            tips=False,
        ).shift(DOWN * 0.6)
        m = ValueTracker(2.0)
        xf = np.sqrt(2 * (Y_HI - Q))
        curve_f = axes.plot(f, x_range=[P - xf, P + xf], color=GREY_B, stroke_width=4)
        lab_f = MathTex("f", font_size=40, color=GREY_B).next_to(axes.c2p(P - 3.6, f(P - 3.6)), LEFT, buff=0.1)
        self.play(FadeIn(step2), Create(axes), run_time=1.0)
        self.play(Create(curve_f), FadeIn(lab_f), run_time=1.0)

        # f 를 오른쪽으로 m 옮긴 뒤 뒤집기
        shifted = axes.plot(lambda x: f(x - 2), x_range=[P + 2 - xf, P + 2 + xf], color=ORANGE_, stroke_width=4)
        say2 = ko("오른쪽으로 m 옮기고…", 32, ORANGE_).next_to(axes, DOWN, buff=0.45)
        self.play(TransformFromCopy(curve_f, shifted), FadeIn(say2), run_time=1.2)
        xg = np.sqrt(2 * (Y_HI + 0.0 - Q))  # 아래로 Y_LO 까지

        def g_plot():
            mv = m.get_value()
            s = np.sqrt(2 * (-Q - Y_LO))
            return axes.plot(lambda x: g(x, mv), x_range=[P + mv - s, min(9.4, P + mv + s)], color=ORANGE_, stroke_width=4)

        curve_g = always_redraw(g_plot)
        say2b = ko("…x축에 대해 뒤집기 → 꼭짓점 (p+m, −q)", 32, ORANGE_).move_to(say2)
        self.play(ReplacementTransform(shifted, curve_g), ReplacementTransform(say2, say2b), run_time=1.3)
        lab_g = MathTex("g", font_size=40, color=ORANGE_).next_to(axes.c2p(4, 4), UP, buff=0.15)
        self.play(FadeIn(lab_g))
        self.wait(1.0)

        # ---------- 3. h = 위에 있는 것 ----------
        step3 = ko("③ h는? 보기 전에 떠올려 봐", 34, BLUE_C_, weight=BOLD).to_edge(UP, buff=1.6)
        self.play(ReplacementTransform(step2, step3), FadeOut(say2b))
        for n in ("3", "2", "1"):
            c = ko(n, 110, ORANGE_, weight=BOLD).move_to(axes.c2p(7.5, -3.5))
            self.play(FadeIn(c, scale=1.4), run_time=0.35)
            self.play(FadeOut(c), run_time=0.45)

        def h_plot():
            mv = m.get_value()
            lo, hi = P - xf, P + xf
            return axes.plot(lambda x: h(x, mv), x_range=[lo, hi, 0.01], color=BLUE_C_, stroke_width=9,
                             use_smoothing=False)

        curve_h = always_redraw(h_plot)
        self.play(Create(curve_h), run_time=1.6)
        say3 = ko("h = f, g 중 '위에 있는 것'만 이은 그래프", 32, BLUE_C_).next_to(axes, DOWN, buff=0.45)
        self.play(FadeIn(say3, shift=UP * 0.2))
        self.wait(1.4)

        # ---------- 4. 발견: t 를 내리기 ----------
        step4 = ko("④ y=t를 위에서 내려 보면?", 34, BLUE_C_, weight=BOLD).to_edge(UP, buff=1.6)
        t = ValueTracker(7.0)
        line_t = always_redraw(lambda: DashedLine(axes.c2p(-3, t.get_value()), axes.c2p(9.5, t.get_value()),
                                                  color=GREEN_, stroke_width=4, dash_length=0.12))

        def dots():
            rs = roots_h(t.get_value(), m.get_value())
            return VGroup(*[Dot(axes.c2p(r, t.get_value()), radius=0.1, color=GREEN_) for r in rs])

        def badge():
            rs = roots_h(t.get_value(), m.get_value())
            ok = len(rs) >= 2 and abs(sum(rs) - (4 * P + 2 * m.get_value())) < 1e-6
            txt = f"근 {len(rs)}개 · " + ("합 = 4p+2m ✓" if ok else "합 ≠ 4p+2m")
            tt = ko(txt, 32, BLACK if ok else WHITE, weight=BOLD)
            box = RoundedRectangle(corner_radius=0.3, width=tt.width + 0.6, height=tt.height + 0.4,
                                   fill_color=GREEN_ if ok else GREY_D, fill_opacity=1, stroke_width=0)
            return VGroup(box, tt).next_to(axes, DOWN, buff=0.45)

        dts = always_redraw(dots)
        bdg = always_redraw(badge)
        self.play(ReplacementTransform(step3, step4), FadeOut(say3), FadeOut(lab_f), FadeOut(lab_g),
                  Create(line_t), FadeIn(dts), FadeIn(bdg))
        self.play(t.animate.set_value(4.5), run_time=1.0)
        self.play(t.animate.set_value(3.3), run_time=1.2)
        self.wait(0.6)

        # 왜 4p+2m? 대칭축 두 개
        ax_p = DashedLine(axes.c2p(P, Y_LO), axes.c2p(P, Y_HI), color=GREY_B, stroke_width=3)
        ax_pm = DashedLine(axes.c2p(P + 2, Y_LO), axes.c2p(P + 2, Y_HI), color=ORANGE_, stroke_width=3)
        lp = MathTex("x=p", font_size=34, color=GREY_B).next_to(ax_p.get_top(), DOWN, buff=0.1).shift(LEFT * 0.45)
        lpm = MathTex("x=p+m", font_size=34, color=ORANGE_).next_to(ax_pm.get_top(), DOWN, buff=0.1).shift(RIGHT * 0.75)
        why = VGroup(
            ko("바깥 두 근은 x=p, 가운데 두 근은 x=p+m 대칭", 28),
            MathTex(r"2p+2(p+m)=4p+2m", font_size=44, color=GREEN_),
        ).arrange(DOWN, buff=0.2).next_to(axes, DOWN, buff=1.35)
        self.play(Create(ax_p), Create(ax_pm), FadeIn(lp), FadeIn(lpm), FadeIn(why, shift=UP * 0.2))
        self.wait(1.8)
        self.play(FadeOut(VGroup(ax_p, ax_pm, lp, lpm, why)))

        # 띠의 위 끝과 아래 끝
        self.play(t.animate.set_value(2.0), run_time=1.6)
        self.play(t.animate.set_value(3.3), run_time=0.8)
        b0 = ab(2.0)[1]
        band = Rectangle(width=axes.c2p(9.5, 0)[0] - axes.c2p(-3, 0)[0],
                         height=axes.c2p(0, 4)[1] - axes.c2p(0, f(b0))[1],
                         fill_color=GREEN_, fill_opacity=0.16, stroke_width=0)
        band.move_to(axes.c2p(3.25, (4 + f(b0)) / 2))
        # 곡선과 겹치지 않도록, 띠 오른쪽 끝(곡선이 화면 밖인 곳)에 짧게 표시하고 설명은 축 아래에
        top = MathTex(r"-q", font_size=40, color=GREEN_).next_to(axes.c2p(9.5, 4), LEFT, buff=0.15).shift(UP * 0.22)
        bot = MathTex(r"h(\beta)", font_size=40, color=GREEN_).next_to(axes.c2p(9.5, f(b0)), LEFT, buff=0.15).shift(DOWN * 0.25)
        bot = VGroup(bot, ko("위 끝 = 봉우리 높이,  아래 끝 = 꺾인 점 β의 높이", 26, GREEN_).next_to(axes, DOWN, buff=0.45))
        self.play(FadeIn(band), FadeIn(top), FadeIn(bot), FadeOut(line_t), FadeOut(dts), FadeOut(bdg))
        self.wait(1.4)
        match = VGroup(
            MathTex(r"h(\beta)", r"<t<", r"-q", font_size=50),
            MathTex(r"g(p)", r"<t<", r"5", font_size=50, color=ORANGE_),
        ).arrange(DOWN, buff=0.25).next_to(axes, DOWN, buff=1.3)
        self.play(FadeIn(match[0]))
        self.play(FadeIn(match[1], shift=UP * 0.2))
        self.wait(1.0)
        eqs = VGroup(MathTex(r"-q=5", font_size=48, color=GREEN_),
                     MathTex(r"g(\beta)=g(p)", font_size=48, color=GREEN_)).arrange(RIGHT, buff=1.0).move_to(match)
        self.play(ReplacementTransform(match, eqs))
        self.wait(1.2)
        self.play(FadeOut(VGroup(band, top, bot)))

        # ---------- 5. g(β)=g(p) 이려면? m 을 움직여 맞추기 ----------
        step5 = ko("⑤ β가 높이 g(p)에 오려면?", 34, BLUE_C_, weight=BOLD).to_edge(UP, buff=1.6)
        gp_line = always_redraw(lambda: DashedLine(axes.c2p(-3, g(P, m.get_value())), axes.c2p(9.5, g(P, m.get_value())),
                                                   color=RED_, stroke_width=3, dash_length=0.1))
        gp_dot = always_redraw(lambda: Dot(axes.c2p(P, g(P, m.get_value())), radius=0.11, color=RED_))
        beta_dot = always_redraw(lambda: Dot(axes.c2p(ab(m.get_value())[1], f(ab(m.get_value())[1])), radius=0.12, color=BLUE_C_))
        beta_lab = always_redraw(lambda: MathTex(r"\beta", font_size=40, color=BLUE_C_).next_to(beta_dot, RIGHT, buff=0.1))
        self.play(ReplacementTransform(step4, step5), FadeIn(gp_line), FadeIn(gp_dot), FadeIn(beta_dot), FadeIn(beta_lab))
        self.play(m.animate.set_value(3.0), run_time=1.0)
        self.play(m.animate.set_value(4 / np.sqrt(5)), run_time=1.6, rate_func=smooth)
        mv = 4 / np.sqrt(5)
        y0 = Y_LO + 0.35
        mk = VGroup(*[Line(axes.c2p(xx, y0 - 0.25), axes.c2p(xx, y0 + 0.25), color=WHITE, stroke_width=4)
                      for xx in (P, P + mv, P + 2 * mv)])
        br1 = BraceBetweenPoints(axes.c2p(P, y0), axes.c2p(P + mv, y0), UP, color=ORANGE_)
        br2 = BraceBetweenPoints(axes.c2p(P + mv, y0), axes.c2p(P + 2 * mv, y0), UP, color=ORANGE_)
        bm = VGroup(MathTex("m", font_size=36, color=ORANGE_).next_to(br1, UP, buff=0.05),
                    MathTex("m", font_size=36, color=ORANGE_).next_to(br2, UP, buff=0.05))
        say5 = VGroup(ko("g는 x=p+m 대칭 → β는 p를 뒤집은 자리", 28),
                      MathTex(r"\beta=p+2m", font_size=56, color=GREEN_)).arrange(DOWN, buff=0.2).next_to(axes, DOWN, buff=1.3)
        self.play(FadeIn(mk), GrowFromCenter(br1), GrowFromCenter(br2), FadeIn(bm), FadeOut(eqs))
        self.play(FadeIn(say5, shift=UP * 0.2))
        self.wait(1.8)

        # ---------- 6. 이제야 계산 ----------
        step6 = ko("⑥ 이제야 계산 (식 세 개)", 36, BLUE_C_, weight=BOLD).to_edge(UP, buff=1.6)
        self.play(FadeOut(VGroup(axes, curve_f, curve_g, curve_h, gp_line, gp_dot, beta_dot, beta_lab,
                                 mk, br1, br2, bm, say5)), ReplacementTransform(step5, step6))
        calc = VGroup(
            MathTex(r"-q=5 \;\Rightarrow\; q=-5", font_size=50),
            MathTex(r"f(p+2m)=g(p+2m)", font_size=46),
            MathTex(r"2m^2-5=-\tfrac12m^2+5 \;\Rightarrow\; m=2", font_size=44),
            MathTex(r"f(m)+g(m)=\tfrac12(m-p)^2-\tfrac12p^2=-4", font_size=40),
            MathTex(r"\Rightarrow\; p=3", font_size=48),
            MathTex(r"m(p-q)=2\times 8=16", font_size=70, color=GREEN_),
        ).arrange(DOWN, buff=0.5).shift(UP * 0.4)
        for mob in calc:
            self.play(FadeIn(mob, shift=UP * 0.2), run_time=0.7)
            self.wait(0.5)
        self.wait(1.0)

        # ---------- 7. 마무리 ----------
        outro = VGroup(
            ko("식은 문제에 '써 있는' 게 아니라", 32, MUTED),
            ko("그림 속 범위의 양 끝에 숨어 있었다", 34, ORANGE_),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=1.4)
        self.play(FadeIn(outro, shift=UP * 0.2))
        self.wait(2.2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
