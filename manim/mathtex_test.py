from manim import *

class Pythagoras(Scene):
    def construct(self):
        title = Text("피타고라스 정리", font="AppleSDGothicNeo").to_edge(UP)
        eq = MathTex("a^2", "+", "b^2", "=", "c^2").scale(1.5)
        eq[0].set_color(BLUE)
        eq[2].set_color(GREEN)
        eq[4].set_color(RED)
        frac = MathTex(r"c = \sqrt{a^2 + b^2}").next_to(eq, DOWN, buff=0.8)
        self.play(Write(title))
        self.play(Write(eq))
        self.play(FadeIn(frac, shift=UP))
        self.wait()
