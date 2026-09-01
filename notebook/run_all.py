"""
======================================================================
  THE NOTEBOOK -- index, progress board and triage
======================================================================

    python notebook/run_all.py            progress across all three parts
    python notebook/run_all.py --plan     what to study, in what order

Files:
    dataset.py   the data itself -- provenance, live numbers, the six
                 landmines, examiner questions
    part1.py     Q1.1 - Q1.4    10 points
    part2.py     Q2.1 - Q2.6    20 points
    part3.py     Q3.1 - Q3.5    40 points

Every file takes the same flags:
    --teach [q]   the full lesson (--teach 3.5 for one question)
    --trace [q]   instrumented walkthrough with real numbers
    --quiz [q]    examiner questions, no answers
    --answers [q] the same with model answers
    (no flag)     run the reference solutions, mark your live edits
======================================================================
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

FILES = [
    ("part1.py", "Part 1  fundamentals", 10, 4),
    ("part2.py", "Part 2  pandas", 20, 6),
    ("part3.py", "Part 3  model + eval", 40, 6),
]

PLAN = """
TRIAGE -- THE COURSEWORK IS 20% OF EACH QUESTION, THE LIVE VIVA IS 80%
=====================================================================

So the code is already written. What is being graded tomorrow is
whether you can EXPLAIN it, INTERPRET it, and CHANGE it on request.
Study accordingly: read the lessons, run the traces, answer the quiz
out loud, and do the live-edit variants.

POINTS, AND WHERE TO SPEND YOUR TIME
------------------------------------

    Q3.5   20 pts   <-- a third of the coursework, on its own
    Q3.4    7 pts
    Q2.6    6 pts   <-- and it needs WRITTEN paragraphs
    Q3.2    6 pts   <-- half the marks are in the second half of the question
    Q3.3    5 pts
    Q2.3    4 pts
    Q2.5    4 pts
    Q1.3    3 pts   <-- contains the best single sentence available to you
    Q1.4    3 pts
    Q1.1 Q1.2 Q2.1 Q2.2 Q2.4 Q3.1   2 pts each

IF YOU HAVE ONE EVENING, DO EXACTLY THIS
----------------------------------------

  1.  python notebook/dataset.py --traps          (10 min)
      Six things that are wrong or surprising in this data. Two of
      them are errors in the assignment brief itself.

  2.  python notebook/part3.py --teach 3.5        (25 min)
      Twenty points. Includes the result that a standard XGBoost
      LOSES to linear regression here, and the hyperparameter
      question most likely to sink you.

  3.  python notebook/part3.py --trace 3.3        (10 min)
      Watch gestation go from 35th to 1st when you scale by standard
      deviation. Best single observation in Part 3.

  4.  python notebook/part2.py --teach 2.6        (20 min)
      Six points, and it wants written hypotheses. The paragraphs are
      drafted for you -- read them, then say them in your own words.

  5.  python notebook/part2.py --trace 2.3        (5 min)
      Only `now` moves. Quitters look like never-smokers. Best
      interpretive point in Part 2.

  6.  python notebook/part3.py --teach 3.2        (15 min)
      The second half of the question is where the marks are.

  7.  python notebook/part1.py --teach 1.3        (5 min)
      The brief's expected output is wrong. Know exactly how to say
      so.

  8.  Then answer these OUT LOUD, timed, without notes:
        python notebook/part3.py --quiz
        python notebook/part2.py --quiz
      Check yourself with --answers afterwards.

  9.  Only then, if time remains, do the live-edit variants:
        python notebook/part3.py
        python notebook/part2.py

THE THREE THINGS TO SAY THAT NOBODY ELSE WILL
---------------------------------------------

  1.  "88 ounces is 2494.76 grams, which is below 2500, so it is Low.
       I think the expected output in Q1.3 has it in Normal."

  2.  "gestation looks negligible at 0.44, but multiplied by its
       standard deviation of 15.45 days it is 6.85 ounces per SD --
       the largest effect in the model. The printed ranking is a units
       artefact."

  3.  "My gradient booster did not beat linear regression with
       standard settings. It only won once I constrained it hard,
       because with 993 rows and a largely linear signal, capacity is
       a liability here."

THE TWO QUESTIONS MOST LIKELY TO CATCH YOU
------------------------------------------

  "How did you choose those hyperparameters?"
      If you tuned on the test set, say so, and name the fix:
      GridSearchCV inside the training set, nested CV for an unbiased
      estimate. Admitting it scores higher than bluffing.

  "Your marital coefficient is -12. What does that tell us?"
      Almost nothing. It is estimated from 3 rows against a baseline
      ('divorced') of 2 rows. Say that before they do.

IF THE NOTEBOOK MISBEHAVES DURING THE SESSION
---------------------------------------------

  Re-running the Q2.2 cell raises KeyError: ['dht','dwt'] not found.
  Nothing is broken -- the cell is not idempotent, the columns are
  already gone. Restart the kernel and run all. Knowing this in
  advance turns a panic into a shrug.
"""


def main():
    if "--plan" in sys.argv:
        print(PLAN)
        return

    print()
    print("=" * 72)
    print("  THE NOTEBOOK -- PROGRESS")
    print("=" * 72)

    tot_done = tot_fail = tot_todo = 0
    for fname, label, pts, n in FILES:
        out = subprocess.run([sys.executable, os.path.join(HERE, fname)],
                             capture_output=True, text=True)
        done = fail = todo = 0
        for line in (out.stdout + out.stderr).splitlines():
            s = line.strip()
            if " solved   " in s and " not attempted" in s:
                p = s.split()
                done, fail, todo = int(p[0]), int(p[2]), int(p[4])
        broken = out.returncode != 0
        bar = "#" * done + "." * (fail + todo)
        print("  %-24s %2d pts  [%-6s] %s"
              % (label, pts, bar, "ERROR" if broken else "%d/%d" % (done, n)))
        tot_done += done
        tot_fail += fail
        tot_todo += todo

    print("-" * 72)
    print("  %d of 16 live-edits solved   %d failing   %d not attempted"
          % (tot_done, tot_fail, tot_todo))
    print("-" * 72)
    print()
    print("  next:  python notebook/run_all.py --plan")
    print("         python notebook/dataset.py --traps")
    print()


if __name__ == "__main__":
    main()
