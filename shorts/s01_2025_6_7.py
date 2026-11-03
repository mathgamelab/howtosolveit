"""쇼츠 시안 #1 — 2025학년도 6월 모의평가 공통 7번 (발견 해설)

흐름 (폴리아): 구하는 것 보기 → 개형 먼저 떠올리기 → k를 움직여 발견 → 계산 → 종합법은 맨 끝
렌더:
  cd shorts && ../.venv/bin/manim -r 1080,1920 --fps 30 s01_2025_6_7.py Short01
  (빠른 미리보기: -ql 대신 -r 540,960 --fps 15)
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
MUTED = "#9aa4ae"


def ko(s, size=40, color=WHITE, weight=NORMAL):
    return Text(s, font=KO, font_size=size, color=color, weight=weight)


def f0(x):
    return x**3 - 3 * x**2 - 9 * x


def visible_x_range(k, y_lo=-45, y_hi=40):
    """곡선이 축 범위(y_lo..y_hi) 안에 있는 x 구간. 삼차함수는 양 끝에서 증가하므로
    왼쪽 끝은 f+k=y_lo 의 가장 작은 실근, 오른쪽 끝은 f+k=y_hi 의 가장 큰 실근."""
    lo = min(z.real for z in np.roots([1, -3, -9, k - y_lo]) if abs(z.imag) < 1e-6)
    hi = max(z.real for z in np.roots([1, -3, -9, k - y_hi]) if abs(z.imag) < 1e-6)
    return [lo, hi]


def distinct_roots(k):
    r = np.roots([1, -3, -9, k])
    real = sorted(z.real for z in r if abs(z.imag) < 1e-6)
    out = []
    for z in real:
        if not out or abs(z - out[-1]) > 1e-3:
            out.append(z)
    return out


class Short01(Scene):
    def construct(self):
        # ---------- 0. 훅 ----------
        tag = ko("2025학년도 6월 모평 · 공통 7번", 30, MUTED).to_edge(UP, buff=0.9)
        hook = VGroup(
            ko("공식부터 쓰지 말고", 54, weight=BOLD),
            ko("그래프를 움직여 보자", 54, ORANGE_, weight=BOLD),
        ).arrange(DOWN, buff=0.3).shift(UP * 3.2)
        prob = VGroup(
            MathTex(r"x^3-3x^2-9x+k=0", font_size=64),
            ko("서로 다른 실근의 개수가 2가 되도록 하는", 32),
            ko("모든 실수 k의 값의 합은?", 32),
        ).arrange(DOWN, buff=0.35).next_to(hook, DOWN, buff=1.0)
        self.play(FadeIn(tag), Write(hook), run_time=1.4)
        self.play(FadeIn(prob, shift=UP * 0.3), run_time=1.0)
        self.wait(1.2)

        # ---------- 1. 이해: 구하는 것 ----------
        step1 = ko("① 구하는 것부터 보기", 36, BLUE_C_, weight=BOLD).to_edge(UP, buff=1.6)
        hl = SurroundingRectangle(prob[2], color=ORANGE_, buff=0.12)
        say1 = ko("'모든 k의 합' → 그런 k는 몇 개뿐이다", 34, ORANGE_).next_to(prob, DOWN, buff=0.8)
        self.play(FadeOut(hook), FadeIn(step1), Create(hl))
        self.play(Write(say1), run_time=1.2)
        self.wait(1.2)
        say1b = ko("실근 = 그래프가 x축과 만나는 점", 34).next_to(say1, DOWN, buff=0.45)
        self.play(FadeIn(say1b, shift=UP * 0.2))
        self.wait(1.2)
        self.play(FadeOut(VGroup(prob, hl, say1, say1b, step1)))

        # ---------- 2. 개형 먼저 ----------
        step2 = ko("② 보기 전에, 개형을 떠올려 봐", 36, BLUE_C_, weight=BOLD).to_edge(UP, buff=1.6)
        expr = MathTex(r"y=x^3-3x^2-9x", font_size=56).next_to(step2, DOWN, buff=0.5)
        axes = Axes(
            x_range=[-5, 7, 1], y_range=[-45, 40, 10], x_length=8.2, y_length=7.6,
            axis_config={"color": GREY_B, "include_ticks": True, "tick_size": 0.05},
            x_axis_config={"numbers_to_include": [-4, -2, 2, 4, 6], "font_size": 26},
            tips=False,
        ).shift(DOWN * 0.9)
        qs = VGroup(
            ko("봉우리·골짜기는 몇 개?", 32),
            ko("양 끝은 어디로 갈까?", 32),
        ).arrange(DOWN, buff=0.25).next_to(axes, DOWN, buff=0.45)
        self.play(FadeIn(step2), Write(expr), Create(axes), run_time=1.4)
        self.play(FadeIn(qs, shift=UP * 0.2))
        # 생각할 시간 (쇼츠에서는 3초 카운트)
        for n in ("3", "2", "1"):
            c = ko(n, 120, ORANGE_, weight=BOLD).move_to(axes.c2p(1, 10))
            self.play(FadeIn(c, scale=1.4), run_time=0.35)
            self.play(FadeOut(c), run_time=0.45)
        k = ValueTracker(0)
        curve = always_redraw(lambda: axes.plot(
            lambda x: f0(x) + k.get_value(), x_range=visible_x_range(k.get_value()),
            color=BLUE_C_, stroke_width=6))
        self.play(Create(curve), run_time=1.6)
        ans2 = ko("극값 2개인 N자 — 봉우리 x=−1, 골짜기 x=3", 30, GREEN_).move_to(qs)
        self.play(ReplacementTransform(qs, ans2))
        self.wait(1.0)

        # ---------- 3. 발견: k를 움직이기 ----------
        step3 = ko("③ k를 움직이면?", 36, BLUE_C_, weight=BOLD).to_edge(UP, buff=1.6)
        expr_k = MathTex(r"y=x^3-3x^2-9x", r"+k", font_size=56).move_to(expr)
        expr_k[1].set_color(ORANGE_)
        self.play(ReplacementTransform(step2, step3), TransformMatchingTex(expr, expr_k), FadeOut(ans2))

        def root_dots():
            rs = distinct_roots(k.get_value())
            return VGroup(*[Dot(axes.c2p(r, 0), radius=0.11, color=GREEN_) for r in rs])

        def badge():
            n = len(distinct_roots(k.get_value()))
            col = GREEN_ if n == 2 else GREY_B
            t = ko(f"x축과 만나는 점: {n}개", 34, BLACK if n == 2 else WHITE, weight=BOLD)
            box = RoundedRectangle(corner_radius=0.3, width=t.width + 0.6, height=t.height + 0.4,
                                   fill_color=col, fill_opacity=1, stroke_width=0)
            return VGroup(box, t).next_to(axes, DOWN, buff=0.45)

        dots = always_redraw(root_dots)
        bdg = always_redraw(badge)
        updown = ko("모양은 그대로, 위아래로 평행이동", 30, MUTED).next_to(axes, DOWN, buff=1.4)
        self.play(FadeIn(dots), FadeIn(bdg))
        self.play(k.animate.set_value(15), run_time=1.0)
        self.play(k.animate.set_value(-15), FadeIn(updown), run_time=1.4)
        self.play(k.animate.set_value(0), run_time=0.8)
        self.wait(0.4)

        q3 = ko("개수가 딱 2개가 되는 순간은?", 34, ORANGE_).move_to(updown)
        self.play(ReplacementTransform(updown, q3))
        # 아래에서 위로 쓸어 올리기: 1 → 2 → 3 → 2 → 1
        self.play(k.animate.set_value(-30), run_time=1.0)
        self.play(k.animate.set_value(-5), run_time=1.6, rate_func=smooth)
        touch1 = Circle(radius=0.45, color=ORANGE_, stroke_width=5).move_to(axes.c2p(-1, 0))
        lab1 = ko("봉우리가 x축에 닿을 때!", 30, ORANGE_).next_to(touch1, UP, buff=0.2)
        self.play(Create(touch1), FadeIn(lab1), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(touch1), FadeOut(lab1), k.animate.set_value(10), run_time=1.0)
        self.play(k.animate.set_value(27), run_time=1.6, rate_func=smooth)
        touch2 = Circle(radius=0.45, color=ORANGE_, stroke_width=5).move_to(axes.c2p(3, 0))
        lab2 = ko("골짜기가 x축에 닿을 때!", 30, ORANGE_).next_to(touch2, DOWN, buff=0.2)
        self.play(Create(touch2), FadeIn(lab2), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(touch2), FadeOut(lab2), k.animate.set_value(38), run_time=0.9)
        self.wait(0.3)

        notice = VGroup(
            ko("발견", 34, GREEN_, weight=BOLD),
            ko("실근 2개 = 극값이 x축에 '접할' 때", 34),
            ko("그런 순간은 딱 두 번", 34),
        ).arrange(DOWN, buff=0.25).next_to(axes, DOWN, buff=1.3)
        self.play(FadeOut(q3), FadeIn(notice, shift=UP * 0.2))
        self.wait(1.8)

        # ---------- 4. 실행: 계산은 이제야 ----------
        step4 = ko("④ 이제야 계산", 36, BLUE_C_, weight=BOLD).to_edge(UP, buff=1.6)
        self.play(FadeOut(VGroup(curve, dots, bdg, axes, notice, expr_k)), ReplacementTransform(step3, step4))
        calc = VGroup(
            MathTex(r"y'=3(x+1)(x-3)", font_size=58),
            VGroup(ko("극댓값", 34), MathTex(r"f(-1)=5", font_size=52),
                   ko("극솟값", 34), MathTex(r"f(3)=-27", font_size=52)).arrange(RIGHT, buff=0.25),
            VGroup(ko("봉우리를 내리려면", 32), MathTex(r"k=-5", font_size=56, color=ORANGE_)).arrange(RIGHT, buff=0.3),
            VGroup(ko("골짜기를 올리려면", 32), MathTex(r"k=27", font_size=56, color=ORANGE_)).arrange(RIGHT, buff=0.3),
            MathTex(r"-5+27=22", font_size=80, color=GREEN_),
        ).arrange(DOWN, buff=0.6).shift(UP * 0.3)
        for m in calc:
            self.play(FadeIn(m, shift=UP * 0.2), run_time=0.7)
            self.wait(0.6)
        ans = ko("정답 ④", 46, GREEN_, weight=BOLD).next_to(calc, DOWN, buff=0.6)
        self.play(Write(ans))
        self.wait(1.0)

        # ---------- 5. 마무리 ----------
        outro = VGroup(
            ko("해설지의 한 줄", 32, MUTED),
            ko("'극값이 0일 때 실근 2개'", 38),
            ko("그 한 줄 뒤에 숨은 발견을 꺼내 보는 것", 34, ORANGE_),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=1.4)
        self.play(FadeIn(outro, shift=UP * 0.2))
        self.wait(2.2)
        self.play(*[FadeOut(m) for m in self.mobjects])
