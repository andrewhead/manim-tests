from manim import *


# Some features of manim
# - align the environment by default
# - All commands from AMS math packages are available
# - Rendering to SVG with automatic interpolation between SVGs
# - Stylization parameters like 'color'
# - It is possible to load arbitrary packages with '\usepackage'
# - Declare substrings to which colorization applies (though
#   the TeX needs to be split into substrings to begin with, which
#   can be done with 'substrings_to_isolate', or they need to 
#   be referred to by an indexing scheme I don't understand).
# - There is *awesome* status messaging
# - Animations take seconds to produce
# - Supports custom fonts for formulas


# About the implementation of manim:
# see here: https://docs.manim.community/en/stable/guides/deep_dive.html


# Next tasks to attempt:
# Build up a formula in parts.


class MathTeXDemo(Scene):
  def construct(self):
    rtarrow0 = MathTex(r"\xrightarrow{x^6y^8}", font_size=96)
    rtarrow1 = Tex(r"$\xrightarrow{x^6y^8}$", font_size=96)
    self.add(VGroup(rtarrow0, rtarrow1).arrange(DOWN))


class LaTeXSubstrings(Scene):
  def construct(self):
    tex = Tex('Hello', r'$\bigstar$', r'\LaTeX', font_size=144)
    tex.set_color_by_tex('igsta', RED)
    self.add(tex)


class CorrectLaTeXSubstringColoring(Scene):
  def construct(self):
    equation = MathTex(
        r"e^x = x^0 + x^1 + \cdots{}",
        substrings_to_isolate="x"
        )
    equation.set_color_by_tex("x", YELLOW)
    self.add(equation)


class LaTeXAlignEnvironment(Scene):
  def construct(self):
    tex = MathTex(r'f(x) &= 3 + 2 + 1\\ &=5 + 1 \\ &=6', font_size=96)
    self.add(tex)


class MovingFrameBox(Scene):
  # Easy use of this library requires a priori understanding of how you want
  # to split up the formula, leading to greater friction to iteration.
  # In reality, this was not that difficult to write (following along with
  # the tutorial). Though it could be a great inspiration to this project
  # to do a usability analysis around animating formulas with manim.
  def construct(self):
    text = MathTex(
        "\\frac{d}{dx}f(x)g(x)=","f(x)\\frac{d}{dx}g(x)","+",
        "g(x)\\frac{d}{dx}f(x)"
        )
    self.play(Write(text))
    framebox1 = SurroundingRectangle(text[1], buff = .1)
    framebox2 = SurroundingRectangle(text[3], buff = .1)
    self.play(Create(framebox1))
    self.wait()
    self.play(ReplacementTransform(framebox1, framebox2))
    self.wait()


class 


class CreateCircle(Scene):
  def construct(self):
    circle = Circle()
    circle.set_fill(PINK, opacity=0.5)
    self.play(Create(circle))

