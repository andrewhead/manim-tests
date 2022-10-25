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


class TransformEquation(Scene):
  # This animation takes around 5 seconds to generate.
  # It is also confusing because there are multiple constructs for performing
  # the animation: first the "TransformMatchingTex" and then the "TransformMatchingShapes".
  # When is it relevant to use each one? When are the curly braces necessary? And
  # what if I want the "=" sign to fade out, instead of moving? It is kind of confusing.
  # The double brackets are needed for "TransformMatchingTex" to know which expressions
  # in the consecutive formulas correspond to each other.
  # "TransformMatchingShapes" is not as smart, and while it requires less effort to
  # express it, my guess is that it has more unanticipated side effects.
  def construct(self):
    eq1 = MathTex("42 {{ a^2 }} + {{ b^2 }} = {{ c^2 }}")
    eq2 = MathTex("42 {{ a^2 }} = {{ c^2 }} - {{ b^2 }}")
    eq3 = MathTex(r"a^2 = \frac{c^2 - b^2}{42}")
    self.add(eq1)
    self.wait()
    self.play(TransformMatchingTex(eq1, eq2))
    self.wait()
    self.play(TransformMatchingShapes(eq2, eq3))
    self.wait()


class AttentionFormula(Scene):
  # The amount of time I spent getting this to work so far: 60 minutes.
  # One challenge was the regeneration of videos, where the video did not reload
  # when I regenerated it; I had to close it then reopen it.
  # Here is an example of where an animation does not have what I think is the
  # desired behavior: https://docs.manim.community/en/stable/reference/manim.animation.transform_matching_parts.TransformMatchingTex.html
  # The issue here is that the squares should move with the expressions.
  # The more complex the animation gets, the longer the feedback loop becomes. This
  # makes it feel more useful to provide ways of getting instant feedback on
  # individual stages of an animation.
  def construct(self):
    # How do I express combination, for instance, two formulas joining into one?
    # One small piece of friction is the need to specify 'r' for 'raw', instead of
    # writing LaTeX as usual.
    # One need for design is the ability to place multiple sub-formulas on the slide.
    # Another piece of friction is that the formula gets to be so big! It gets to
    # be a challenge to fit it all in one textbox.
    # It is annoying that you need to specifically 'un-create' labels to remote them.
    # I would like to rapidly change some choices like how labels appear or disappear
    # across the whole animation.
    h_t = MathTex(r"\boldsymbol{h}_t")
    self.play(Write(h_t))

    h_t_label = Tex("embeddings at time step $t$")
    h_t_label.next_to(h_t, DOWN, buff=0.5)
    self.add(h_t_label)
    self.wait()
    # self.play(Uncreate(h_t_label))
    self.remove(h_t_label)
    # self.wait()

    # Even adding another symbol to the right of the first one is an obstacle.
    # During my first try, it added the new symbol superimposed over the first.
    # Additional friction is that the symbols are not aligned in their baseline
    # but rather at the tops. And I want to scoot over the h_t when hbar_s
    # is added, but I don't know how. To get them to align at their baseline,
    # I might need to follow a solution like this:
    # https://www.reddit.com/r/manim/comments/k0avc3/aligning_textmobjects_with_descenders/
    hbar_s = MathTex(r"\bar{\boldsymbol{h} }_s").shift(0.5 * RIGHT)
    # This was my first version of code to get hbar_s to appear next to h_t
    # I then attempted several other solutions, ultimately trying the 'shift'
    # option to end up with something that was centered.
    # hbar_s.next_to(h_t, RIGHT, buff=0.5)
    # self.play(Write(hbar_s))
    self.play(h_t.animate.shift(0.5 * LEFT))
    self.play(Write(hbar_s))

    # I really like that the labels can include LaTeX
    hbar_s_label = Tex("embeddings at time step $s$")
    hbar_s_label.next_to(hbar_s, DOWN, buff=0.5)
    self.add(hbar_s_label)
    self.wait()
    self.remove(hbar_s_label)

    # It would be nice to use macros for some of these symbols that are used
    # repeatedly to support rapidly making cross-cutting changes and to reduce
    # the change of typographical errors.
    # This part of it took probably around 20 minutes to figure out and to
    # implement. I had to add double braces around the arguments. I miscorrectly
    # wrote that TeX for one of the formulas, which I only discovered by playing
    # forward the animation. And even still, the animation was not correct---it
    # did not interpolate correctly which terms were supposed to go where. I think
    # one reason for the issue is that the double braces are not getting parsed
    # correctly, when I have double braces in the formula from routine application
    # of multiple macros to a letter.
    # In fact, the double braces caused a couple of errors, not just the fact that
    # my macros were being processed incorrectly (assigning the hat to the wrong part
    # of the formula), but I also, to fix this, I needed to enter a space between
    # the double braces associated with the macro, and that needs to be consistent
    # across all definitions of the symbol (i.e., when I introduce it in the first
    # formula, I need the same brittle spacing). A third issue is that I put my brackets
    # outside of a parentheses, which was an action slip, and it took me a long time to
    # figure out that that was a problem.
    score = MathTex(r"\mathrm{score}({{\boldsymbol{h}_t}}, {{\bar{\boldsymbol{h} }_s}})")
    self.play(TransformMatchingTex(Group(h_t, hbar_s), score))

    score_label = Tex("``match'' between embeddings")
    score_label.next_to(score, DOWN, buff=0.5)
    self.add(score_label)
    self.wait()
    self.remove(score_label)

    # This would be a tricky one to animate through direct manipulation,
    # *especially* if a single expression has multiple destinations, like
    # trying to send the score to *both* the numerator and the denominator.
    # This part has taken me probably around 20 minutes so far.
    # I seem to have hit an impasse with the double braces around
    # the formula: if I take them out below, the formula renders, and if I
    # put them in, the formula does not render. But I am almost positive I need
    # those brackets for one of the formulas to find its place in the next formula.
    softmax = MathTex(
      r"\frac{" +
      r"\exp ( {{ \mathrm{score}(\boldsymbol{h}_t, \bar{\boldsymbol{h} }_s) }} )" +
      r"}{" +
      r"\sum_{s'=1}^S \exp ( \mathrm{score}(\boldsymbol{h}_t, \bar{\boldsymbol{h} }_s') )" +
      r"}")
    self.play(TransformMatchingTex(score, softmax))


class CreateCircle(Scene):
  def construct(self):
    circle = Circle()
    circle.set_fill(PINK, opacity=0.5)
    self.play(Create(circle))

