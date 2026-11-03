from manim import *

class Hello(Scene):
    def construct(self):
        title = Text("피타고라스 정리", font="AppleSDGothicNeo")
        tri = Polygon([-2, -1, 0], [2, -1, 0], [2, 2, 0], color=BLUE)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))
        self.play(Create(tri))
        self.wait()
