"""
======================================================================
  PART 1 -- Python Fundamentals            (10 points of the coursework)
  functions, loops, if statements, variables, strings, print
======================================================================

    python notebook/part1.py --teach          all four questions
    python notebook/part1.py --teach 1.2      just that one
    python notebook/part1.py --trace          watch the numbers
    python notebook/part1.py --quiz           examiner questions
    python notebook/part1.py --answers        ... with answers
    python notebook/part1.py                  mark your variants

Part 1 is only 10 points, but it is where the assessor warms up, and
it contains the single best sentence available to you in the whole
sitting -- see Q1.3.
======================================================================
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _data as D


STATEMENTS = {
    "1.1": """Q1.1 -- Unit Converter (2 points)

  Birth weight in this dataset is measured in OUNCES. Write a function
  oz_to_grams(oz) that converts ounces to grams.
      1 ounce = 28.3495 grams
  The function should RETURN the result rounded to 2 decimal places.

      oz_to_grams(120)  ->  3401.94
      oz_to_grams(0)    ->  0.0""",

    "1.2": """Q1.2 -- Weight Category Classifier (2 points)

  Write classify_weight(bwt_oz) returning a category string based on
  WHO standards. Use your oz_to_grams from Q1.1 inside it.

      "Low"     < 2500 g
      "Normal"  2500 - 3999 g
      "High"    >= 4000 g

      classify_weight(80)   # 2267.96 g  ->  'Low'
      classify_weight(120)  # 3401.94 g  ->  'Normal'
      classify_weight(145)  # 4110.68 g  ->  'High'""",

    "1.3": """Q1.3 -- Counting Categories with a Loop (3 points)

  Given the list of birth weights below, use a FOR LOOP and your
  classify_weight function to count how many babies fall into each
  category. Print the counts.

      weights = [75, 88, 120, 130, 150, 60, 110, 142]

  The brief prints this expected output:
      Low: 2      Normal: 4      High: 2""",

    "1.4": """Q1.4 -- Summary Statistics, No Libraries (3 points)

  Write summary_stats(data) taking a list of numbers and returning a
  dictionary with min, max, mean and count. Built-in Python only --
  no numpy, no pandas.

      summary_stats([75, 88, 120, 130, 150, 60, 110, 142])
      -> {'count': 8, 'min': 60, 'max': 150, 'mean': 109.375}""",
}


LESSONS = {
    "1.1": """
WHAT IS ACTUALLY BEING TESTED

  RETURN versus PRINT. The word "return" is bold in the brief for a
  reason: Q1.2 has to call this function and use its value. A version
  that prints returns None, and None cannot be compared to 2500, so
  Q1.2 collapses with a TypeError. If Q1.2 breaks, look here first.

THE ROUNDING, AND THE TWO THINGS PEOPLE GET WRONG

  round(x, 2) is not the schoolbook rounding you were taught.

  (a) BANKER'S ROUNDING. Python rounds halfway cases to the nearest
      EVEN digit, not always up:
          round(0.5) -> 0        round(1.5) -> 2
          round(2.5) -> 2        round(3.5) -> 4
      This is deliberate -- always rounding up biases sums upward.
      IEEE 754 specifies it. It is not a bug.

  (b) BINARY FLOAT REPRESENTATION. round(2.675, 2) gives 2.67, not
      2.68, because 2.675 cannot be represented exactly in binary; the
      stored value is fractionally below 2.675, so it rounds down.

  Neither changes your answer here. Being able to say them if asked
  "are you sure round does what you think?" is what earns the mark.

WHY oz_to_grams(0) IS 0.0 AND NOT 0

  0 * 28.3495 is float multiplication, so the result is the float 0.0.
  round(0.0, 2) is still 0.0. The brief's expected output shows 0.0,
  which is a small signal that they are checking you noticed.

DO NOT HARD-CODE THE CONSTANT INLINE TWICE

  One named constant, used once. If the assessor says "now use
  28.35", you change one character rather than hunting.
""",

    "1.2": """
BUILD ON Q1.1, DO NOT REIMPLEMENT IT

  The brief says explicitly to use oz_to_grams inside this. Recomputing
  the conversion here is the wrong answer even if it produces the right
  number, because it duplicates the constant.

if / elif / elif, NOT THREE SEPARATE ifs

      if g < 2500:    return "Low"
      elif g < 4000:  return "Normal"
      else:           return "High"

  Each elif is only reached when the previous test failed, so
  "elif g < 4000" already means "g >= 2500 and g < 4000". You never
  have to write the lower bound. Say that -- it shows you understand
  control flow rather than pattern-matching a shape.

  With early returns, three separate ifs happen to work too. Be ready
  to say why: because return exits immediately, so the later tests are
  unreachable once one fires. That is a different argument, and
  knowing which one applies to your code is the point.

THE BOUNDARIES ARE ASYMMETRIC -- READ THE TABLE AGAIN

      Low     < 2500          strictly below
      Normal  2500 - 3999     inclusive of 2500
      High    >= 4000         inclusive of 4000

  So exactly 2500.00 g is Normal, and exactly 4000.00 g is High. Using
  <= anywhere in the chain flips a boundary case.

  Also note "3999" in the brief is loose: grams are continuous, so
  3999.5 exists and must be Normal. Coding "< 4000" is right; coding
  "<= 3999" is wrong.

THE ROUNDING TRAP  (this is the one to volunteer)

  The threshold in ounces is 2500 / 28.3495 = 88.18498 oz.

      88.1849 oz  ->  true grams 2499.9978  ->  should be "Low"
                  ->  but round(.., 2) = 2500.00  ->  returns "Normal"

  Following the brief exactly -- round in Q1.1, reuse it in Q1.2 --
  makes classification depend on a rounding artefact in a band about
  0.0001 oz wide. No real row lands there, so the answer is unaffected.
  But saying "my classifier inherits Q1.1's rounding, which can flip a
  hairline case; I would classify on the unrounded grams and round only
  for display" is exactly the kind of remark that separates a 2/2 from
  a 1/2 in the live part.
""",

    "1.3": """
THE BRIEF'S EXPECTED OUTPUT IS WRONG, AND YOU SHOULD SAY SO

      weights = [75, 88, 120, 130, 150, 60, 110, 142]

      75 oz -> 2126.21 g -> Low
      88 oz -> 2494.76 g -> Low      <-- the brief counts this as Normal
     120 oz -> 3401.94 g -> Normal
     130 oz -> 3685.43 g -> Normal
     150 oz -> 4252.43 g -> High
      60 oz -> 1700.97 g -> Low
     110 oz -> 3118.44 g -> Normal
     142 oz -> 4025.63 g -> High

      correct:      Low 3, Normal 3, High 2
      brief says:   Low 2, Normal 4, High 2

  2494.76 is below 2500, so 88 oz is a Low birth weight. The brief is
  off by one.

  DO NOT bend your code to reproduce the brief. Say, calmly:

    "My count gives Low 3, Normal 3, High 2. The difference is 88
     ounces, which is 2494.76 grams -- just under the 2500 gram
     threshold, so my function classifies it as Low. I believe the
     expected output in the brief has that one in Normal."

  That is a graded moment. You are being marked on interpreting data
  and explaining logic, and catching an error in the question is the
  strongest possible evidence of both. Deliver it as an observation,
  not an accusation.

THE COUNTING LOOP ITSELF

  Three ways, in ascending order of how much they show:

      counts = {"Low": 0, "Normal": 0, "High": 0}
      for w in weights:
          counts[classify_weight(w)] += 1

  Pre-seeding the dict guarantees all three keys exist even when a
  category has no members -- which matters, because printing a
  category with a zero count is usually what the reader wants.

      counts[c] = counts.get(c, 0) + 1        # no pre-seeding needed
      collections.Counter(...)                # idiomatic, but Q1.3
                                              # asks for a for loop

  Use the explicit loop, then mention Counter exists. The question
  says "use a for loop", so leading with Counter answers a different
  question.

PRINT, DO NOT RETURN

  Q1.3 says print. Opposite of Q1.1. Read each question's verb.
""",

    "1.4": """
"NO LIBRARIES" MEANS NO import statistics EITHER

  statistics.mean is the standard library, and the spirit of the
  question is that you can compute it. sum(data) / len(data).

THE FOUR KEYS, SPELLED EXACTLY

      {'count': 8, 'min': 60, 'max': 150, 'mean': 109.375}

  If anything checks your output automatically, 'avg' instead of
  'mean' fails. Copy the key names from the brief character for
  character.

  min() and max() are built-ins, not libraries, so they are allowed.
  Writing your own loop to find them is also fine and shows more --
  say which you did and why.

THE EMPTY LIST IS THE ONLY REAL EDGE CASE

  sum([]) is 0, len([]) is 0, so the mean raises ZeroDivisionError.
  min([]) raises ValueError before that.

  There is no single right answer to what an empty list should do --
  return None, return an empty dict, or raise a clear error. What is
  graded is that you NOTICED and made a deliberate choice. Say:

    "An empty list would raise ValueError on min. I would either guard
     it and return None, or let it raise, but I would not let it fail
     silently."

WHAT ELSE THEY MIGHT ASK FOR

  Median is the obvious next request, and it has a real decision in
  it: sort a COPY, not the caller's list, and handle even length by
  averaging the two middle values. Standard deviation is the other,
  and it has the population-versus-sample question in it -- divide by
  n or by n-1. Have both answers ready; see V4 below.
""",
}


EXAMINER = [
    ("1.1", "Why must oz_to_grams return rather than print?",
     """Because Q1.2 calls it and compares the result to 2500. A printing
        version returns None, and None < 2500 raises TypeError, so Q1.2
        breaks."""),

    ("1.1", "Does round() do what you think it does?",
     """Not quite. Python uses banker's rounding, so halfway cases go to
        the nearest even digit: round(0.5) is 0 and round(1.5) is 2.
        Separately, binary float representation means round(2.675, 2)
        gives 2.67. Neither affects this answer, but both are real."""),

    ("1.1", "Why is oz_to_grams(0) equal to 0.0 rather than 0?",
     """Multiplying an int by a float yields a float, so the result is
        0.0 and round leaves it a float."""),

    ("1.2", "Why elif rather than three separate ifs?",
     """Each elif is only reached when the previous condition failed, so
        elif g < 4000 already implies g >= 2500 and I never write the
        lower bound. With early returns three ifs would also work,
        because return exits immediately -- but the elif version makes
        the mutual exclusivity explicit."""),

    ("1.2", "What does your function return for exactly 2500 grams?",
     """Normal. The table makes Low strictly below 2500, so 2500 is the
        first Normal value. Likewise exactly 4000 is High, not
        Normal."""),

    ("1.2", "Is there any input where your classifier gives the wrong "
            "answer?",
     """Yes, in a hairline band. The threshold is 88.18498 ounces.
        88.1849 oz is 2499.9978 grams, genuinely Low, but Q1.1 rounds
        it to 2500.00 and my classifier says Normal. No real row lands
        there, but I would classify on the unrounded grams and round
        only for display."""),

    ("1.3", "Your counts do not match the expected output. Explain.",
     """My counts are Low 3, Normal 3, High 2. The disagreement is 88
        ounces: 88 times 28.3495 is 2494.76 grams, which is below the
        2500 threshold, so it is Low. The brief appears to have counted
        it as Normal. I am confident in the arithmetic."""),

    ("1.3", "Why pre-seed the dictionary with all three keys?",
     """So that a category with zero members still prints. Without
        pre-seeding you either need dict.get with a default, or you
        silently omit empty categories from the output."""),

    ("1.3", "Could you use collections.Counter?",
     """Yes, and it is what I would write in production. The question
        asks for a for loop, so I wrote the loop -- but Counter over a
        generator of classify_weight calls is the one-liner."""),

    ("1.4", "What happens on an empty list?",
     """min raises ValueError, and the mean would raise ZeroDivisionError
        if it got that far. There is no obviously correct behaviour, so
        the right move is a deliberate one: guard and return None, or
        let it raise. What matters is not failing silently."""),

    ("1.4", "min and max are functions. Does that count as a library?",
     """No -- they are builtins, always available with no import. The
        restriction is on numpy and pandas. I could also write the loop
        by hand, which is trivial."""),

    ("1.4", "Add standard deviation. Which denominator?",
     """Depends on the claim. Divide by n for the population standard
        deviation, when the list IS the whole group. Divide by n-1,
        Bessel's correction, when the list is a sample and you are
        estimating a wider population. numpy defaults to n, pandas
        defaults to n-1, which is a classic source of mismatched
        numbers."""),
]


# ======================================================================
#  REFERENCE SOLUTIONS
# ======================================================================

OUNCE_IN_GRAMS = 28.3495


def oz_to_grams(oz):
    """Q1.1. Ounces to grams, rounded to 2dp. RETURNS, does not print."""
    return round(oz * OUNCE_IN_GRAMS, 2)


def classify_weight(bwt_oz):
    """Q1.2. WHO category from a weight in ounces."""
    grams = oz_to_grams(bwt_oz)
    if grams < 2500:
        return "Low"
    elif grams < 4000:          # already implies grams >= 2500
        return "Normal"
    else:
        return "High"


WEIGHTS = [75, 88, 120, 130, 150, 60, 110, 142]


def count_categories(weights=None):
    """Q1.3. Pre-seeded so a zero-count category still appears."""
    weights = WEIGHTS if weights is None else weights
    counts = {"Low": 0, "Normal": 0, "High": 0}
    for w in weights:
        counts[classify_weight(w)] += 1
    return counts


def summary_stats(data):
    """Q1.4. Builtins only."""
    return {
        "count": len(data),
        "min": min(data),
        "max": max(data),
        "mean": sum(data) / len(data),
    }


# ======================================================================
#  TRACES
# ======================================================================

def trace_conversion():
    print()
    print("  %-8s %-14s %-12s %-10s %s"
          % ("oz", "exact grams", "rounded", "category", "note"))
    print("  " + "-" * 66)
    rows = [75, 88, 88.1849, 120, 130, 141.0, 141.2, 150, 60, 110, 142]
    for oz in rows:
        exact = oz * OUNCE_IN_GRAMS
        r = oz_to_grams(oz)
        note = ""
        if exact < 2500 <= r:
            note = "ROUNDING FLIPS IT Low -> Normal"
        elif oz in (88,):
            note = "the brief calls this Normal; it is Low"
        print("  %-8s %-14.4f %-12.2f %-10s %s"
              % (oz, exact, r, classify_weight(oz), note))
    print()
    print("  thresholds in ounces:  2500 g = %.5f oz    4000 g = %.5f oz"
          % (2500 / OUNCE_IN_GRAMS, 4000 / OUNCE_IN_GRAMS))


def trace_counting():
    print()
    print("  weights = %r" % WEIGHTS)
    print()
    print("  %-6s %-12s %-10s %s" % ("oz", "grams", "category", "counts after"))
    print("  " + "-" * 60)
    counts = {"Low": 0, "Normal": 0, "High": 0}
    for w in WEIGHTS:
        c = classify_weight(w)
        counts[c] += 1
        print("  %-6d %-12.2f %-10s %s" % (w, oz_to_grams(w), c, counts))
    print()
    print("  correct : Low %d, Normal %d, High %d"
          % (counts["Low"], counts["Normal"], counts["High"]))
    print("  brief   : Low 2, Normal 4, High 2      <-- disagrees on 88 oz")


def trace_summary():
    data = WEIGHTS
    s = sorted(data)
    print()
    print("  data   = %r" % data)
    print("  sorted = %r" % s)
    print()
    print("  count = len(data)                = %d" % len(data))
    print("  min   = min(data)                = %d" % min(data))
    print("  max   = max(data)                = %d" % max(data))
    print("  sum   = %d" % sum(data))
    print("  mean  = %d / %d = %s" % (sum(data), len(data), sum(data) / len(data)))
    mid = len(s) // 2
    print("  median (even n) = (s[%d] + s[%d]) / 2 = (%d + %d) / 2 = %s"
          % (mid - 1, mid, s[mid - 1], s[mid], (s[mid - 1] + s[mid]) / 2))


TRACES = {"1.1": trace_conversion, "1.2": trace_conversion,
          "1.3": trace_counting, "1.4": trace_summary}


# ======================================================================
#  YOUR TURN -- LIVE EDITS
#
#  Each is a plausible "now change it" from the assessor. Replace
#  `pass` and re-run this file.
# ======================================================================

# V1 | Make the converter general: `dp` controls the decimal places,
#    | and reverse=True means the INPUT is grams and you return ounces.
#    |   (120)                 -> 3401.94
#    |   (120, dp=0)           -> 3402.0
#    |   (3401.94, reverse=True) -> 120.0
#    | Keep one named constant. This is the most likely Q1.1 live edit.
def oz_to_grams_flex(oz, dp=2, reverse=False):
    pass


# V2 | Fix the rounding trap AND add a fourth category.
#    | Classify on the UNROUNDED grams, and add "Very Low" below 1500.
#    |   52      -> 'Very Low'   (1474.17 g)
#    |   88      -> 'Low'
#    |   88.1849 -> 'Low'        (the rounded version wrongly says Normal)
#    |   120     -> 'Normal'     145 -> 'High'
def classify_weight_exact(bwt_oz):
    pass


# V3 | Count into a dict for ANY list and ANY classifier function.
#    | Return the dict rather than printing, and include a key for
#    | every category the classifier can produce -- which you now have
#    | to be told, so `categories` is a parameter.
#    |   ([75,88,120], classify_weight, ["Low","Normal","High"])
#    |     -> {'Low': 2, 'Normal': 1, 'High': 0}
#    | Note the zero. That is the whole reason for pre-seeding.
def count_into(values, classifier, categories):
    pass


# V4 | Extend the stats: add 'median' and 'std'. Use the POPULATION
#    | standard deviation (divide by n). Return None for an empty list
#    | rather than raising.
#    |   [75,88,120,130,150,60,110,142]
#    |     -> count 8, min 60, max 150, mean 109.375,
#    |        median 115.0, std 30.269...
#    |   [] -> None
#    | Do not sort the caller's list in place -- sort a copy.
def summary_stats_plus(data):
    pass


# ======================================================================
#  TESTS -- do not edit
# ======================================================================

_V1 = [
    ("120", lambda f: f(120), 3401.94),
    ("0", lambda f: f(0), 0.0),
    ("dp=0", lambda f: f(120, dp=0), 3402.0),
    ("dp=4", lambda f: f(1, dp=4), 28.3495),
    ("reverse", lambda f: f(3401.94, reverse=True), 120.0),
    ("reverse dp=1", lambda f: f(2494.76, reverse=True, dp=1), 88.0),
]

_V2 = [
    ("52 very low", lambda f: f(52), "Very Low"),
    ("88 low", lambda f: f(88), "Low"),
    ("88.1849 stays Low", lambda f: f(88.1849), "Low"),
    ("120 normal", lambda f: f(120), "Normal"),
    ("141.0 normal", lambda f: f(141.0), "Normal"),
    ("141.2 high", lambda f: f(141.2), "High"),
    ("145 high", lambda f: f(145), "High"),
    ("0 very low", lambda f: f(0), "Very Low"),
]


def _v3_cases():
    cats = ["Low", "Normal", "High"]
    return [
        ("zero-count category", lambda f: f([75, 88, 120], classify_weight, cats),
         {"Low": 2, "Normal": 1, "High": 0}),
        ("the Q1.3 list", lambda f: f(WEIGHTS, classify_weight, cats),
         {"Low": 3, "Normal": 3, "High": 2}),
        ("empty input", lambda f: f([], classify_weight, cats),
         {"Low": 0, "Normal": 0, "High": 0}),
        ("other classifier", lambda f: f([1, 2, 3, 4], lambda x: "even" if x % 2 == 0
                                         else "odd", ["odd", "even"]),
         {"odd": 2, "even": 2}),
    ]


_V4 = [
    ("the Q1.3 list", lambda f: f(WEIGHTS),
     {"count": 8, "min": 60, "max": 150, "mean": 109.375,
      "median": 115.0, "std": 30.269363637182728}),
    ("odd length", lambda f: f([1, 2, 3]),
     {"count": 3, "min": 1, "max": 3, "mean": 2.0,
      "median": 2.0, "std": 0.816496580927726}),
    ("single", lambda f: f([5]),
     {"count": 1, "min": 5, "max": 5, "mean": 5.0, "median": 5.0, "std": 0.0}),
    ("empty", lambda f: f([]), None),
    ("caller list unsorted after", lambda f: (lambda d: (f(d), d)[1])([3, 1, 2]),
     [3, 1, 2]),
]


def main():
    argv = sys.argv
    mode = D.argmode(argv)
    qid = D.which(argv)
    ids = [qid] if qid in STATEMENTS else sorted(STATEMENTS)

    if mode == "teach":
        for q in ids:
            D.head("PART 1 :: Q%s" % q)
            print(STATEMENTS[q])
            print(LESSONS[q])
        return
    if mode == "trace":
        seen = set()
        for q in ids:
            fn = TRACES[q]
            if fn in seen:
                continue
            seen.add(fn)
            D.head("PART 1 :: TRACE (Q%s)" % q)
            fn()
        return
    if mode in ("quiz", "answers"):
        D.head("PART 1 :: EXAMINER")
        pairs = [(("Q%s  " % q) + question, a)
                 for q, question, a in EXAMINER if q in ids]
        D.quiz(pairs, show=(mode == "answers"))
        return

    D.head("PART 1 -- Python Fundamentals")
    D.sub("reference solutions")
    D.check("oz_to_grams", oz_to_grams,
            [("120", lambda f: f(120), 3401.94), ("0", lambda f: f(0), 0.0)])
    D.check("classify_weight", classify_weight,
            [("80", lambda f: f(80), "Low"), ("120", lambda f: f(120), "Normal"),
             ("145", lambda f: f(145), "High"), ("88", lambda f: f(88), "Low")])
    D.check("count_categories", count_categories,
            [("Q1.3 list", lambda f: f(), {"Low": 3, "Normal": 3, "High": 2})])
    D.check("summary_stats", summary_stats,
            [("Q1.4 list", lambda f: f(WEIGHTS),
              {"count": 8, "min": 60, "max": 150, "mean": 109.375})])

    D.sub("your live edits")
    D.report([
        D.check("V1 oz_to_grams_flex", oz_to_grams_flex, _V1),
        D.check("V2 classify_weight_exact", classify_weight_exact, _V2),
        D.check("V3 count_into", count_into, _v3_cases()),
        D.check("V4 summary_stats_plus", summary_stats_plus, _V4),
    ])


if __name__ == "__main__":
    main()
