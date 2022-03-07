from manim import Circle, Square, Dot, Text, Arrow, Scene, NumberPlane
from manim import Axes, MathTex, Line, Tex
from manim import Create, Rotate, ReplacementTransform, FadeIn, Transform
from manim import FadeOut, MoveAlongPath
from manim import np
from manim import PINK, BLUE, GREEN, RED, PI, LEFT, RIGHT, ORIGIN, DOWN, UP
from manim import WHITE, GOLD


class CreateCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen


class SquareAndCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency

        square = Square()  # create a square
        square.set_fill(BLUE, opacity=0.5)  # set the color and transparency

        square.next_to(circle, UP, buff=0.5)  # set the position
        self.play(Create(circle), Create(square))  # show the shapes on screen


class AnimatedSquareToCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        square = Square()  # create a square

        self.play(Create(square))  # show the square on screen
        self.next_section()
        self.play(square.animate.rotate(PI / 4))  # rotate the square
        self.play(
                  ReplacementTransform(square, circle)
        )  # transform the square into a circle
        self.next_section()
        self.play(
            circle.animate.set_fill(PINK, opacity=0.5)
        )  # color the circle on screen


class DifferentRotations(Scene):
    def construct(self):
        left_square = Square(color=BLUE, fill_opacity=0.7).shift(2 * LEFT)
        right_square = Square(color=GREEN, fill_opacity=0.7).shift(2 * RIGHT)
        self.play(
            left_square.animate.rotate(PI), Rotate(right_square, angle=PI),
            run_time=2
        )
        self.wait()


class VectorArrow(Scene):
    def construct(self):
        dot = Dot(ORIGIN)
        arrow = Arrow(ORIGIN, [2, 2, 0], buff=0)
        numberplane = NumberPlane()
        origin_text = Text('(0, 0)').next_to(dot, DOWN)
        tip_text = Text('(2, 2)').next_to(arrow.get_end(), RIGHT)
        self.add(numberplane, dot, arrow, origin_text, tip_text)


class TwoLines(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            x_length=10,
            axis_config={"color": WHITE},
            tips=False,
        )
        title = Text("This is some algebra1")
        title.shift(2 * UP)

        self.play(FadeIn(title))
        self.wait()

        def func_1(x):
            return 2 * x + 1

        def func_2(x):
            return .5 * x - 1

        line_1 = axes.plot(func_1, color=BLUE)
        line_2 = axes.plot(func_2, color=GOLD)

        self.play(FadeIn(axes))
        self.wait()
        self.play(Transform(line_1, line_2))
        self.wait()

        title_2 = Text("There you have it!").shift(2 * UP)

        self.play(Transform(title, title_2))


class ExampleLaTeX(Scene):
    def construct(self):
        tex = MathTex(r'\xrightarrow{Hello}\text{ \LaTeX}').scale(3)
        self.add(tex)


class Example_1(Scene):
    def construct(self):
        axes = Axes(
                x_range=[-10, 10, 1],
                y_range=[-10, 10, 1],
                x_length=10,
                x_axis_config={
                    "numbers_to_include": np.arange(-10, 10.01, 2),
                    "numbers_with_elongated_ticks": np.arange(-10, 10.01, 2),
                },
                y_axis_config={
                    "numbers_to_include": np.arange(-8, 8.01, 2),
                    "numbers_with_elongated_ticks": np.arange(-8, 8.01, 4),
                },
                tips=False
            )

        title = Text("Parallel Rates")
        title.shift(2 * UP)
        self.play(FadeIn(title), FadeIn(axes))
        self.wait()

        def func_1(x):
            return 2 * x + 1

        def func_2(x):
            return .5 * x - 1

        line_1 = axes.plot(func_1, color=BLUE)
        line_2 = axes.plot(func_2, color=RED)

        l1text = MathTex("2x+1", color=BLUE).shift((UP + LEFT)*2)
        l2text = MathTex(".5x-1", color=RED).shift((DOWN + RIGHT)*2)

        self.play(Create(line_1), Create(line_2), FadeOut(title),
                  Create(l1text), Create(l2text))
        self.wait()

        def func_2_mod(x):
            return 2 * x - 1
        line_2_mod = axes.plot(func_2_mod, color=RED)
        l2text_mod = MathTex("2x-1", color=RED).shift((DOWN + RIGHT)*2)

        act = Transform(line_2, line_2_mod)
        act2 = Transform(l2text, l2text_mod)
        self.play(act, act2)
        self.wait()


class Example_2(Scene):
    def construct(self):
        axes = Axes(
                x_range=[-10, 10, 1],
                y_range=[-5, 5, 1],
                x_length=10,
                x_axis_config={
                    "numbers_to_include": np.arange(-10, 10.01, 2),
                },
                y_axis_config={
                    "numbers_to_include": np.arange(-10, 10.01, 2),
                },
                tips=False
            ).add_coordinates()

        title = Tex("Rasins and Walnuts")
        title.shift(2 * UP)
        self.play(FadeIn(title), FadeIn(axes))

        def func_1(x):
            return (-.5 * x) + (15/8)

        line_1 = axes.plot(func_1, color=BLUE)
        l1text = MathTex("4x+8y=15", color=BLUE).shift((UP + RIGHT)*2)

        self.play(Create(line_1), Create(l1text), FadeOut(title))
        self.wait()
        p1_text = MathTex("raisins = 0", color=RED).shift((DOWN + LEFT)*2.5)
        p1_text_2 = MathTex(f"walnuts = {func_1(0)}",
                            color=GOLD).shift((DOWN + RIGHT)*2.5)
        p1_path = Line(axes.c2p(0, 0), axes.c2p(0, func_1(0)))
        p1 = Dot(axes.coords_to_point(0, 0), radius=0.1, color=RED)

        self.play(Create(p1), Create(p1_text))
        self.play(MoveAlongPath(p1, p1_path), Create(p1_text_2))
        self.wait()

        p2_text = MathTex("rasins = 0.25", color=RED).shift((DOWN + LEFT)*2.5)
        p2_text_2 = MathTex(f"walnuts = {func_1(0.25)}",
                            color=GOLD).shift((DOWN + RIGHT)*2.5)
        p2_path = Line(axes.c2p(0.25, 0), axes.c2p(0.25, func_1(0.25)))
        p2 = Dot(axes.c2p(0.25, 0), radius=0.1, color=RED)

        self.remove(p1)
        self.play(Create(p2), Transform(p1_text, p2_text))
        self.play(MoveAlongPath(p2, p2_path), Transform(p1_text_2, p2_text_2))
        self.wait()


def main():
    test_1 = Example_2()
    test_1.construct()


if __name__ == "__main__":
    main()
