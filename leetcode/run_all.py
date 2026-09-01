"""
======================================================================
  ALL TEN PROBLEMS -- index, progress board and study order
======================================================================

    python leetcode/run_all.py            progress across all ten
    python leetcode/run_all.py --plan     the order to study them in

Each problem lives in its own file. Inside every file:

    --teach     the full derivation: brute force, the insight, the
                invariant, the complexity, the edge cases
    --trace     an instrumented dry run printing every variable at
                every step (this is a GRADED duty of the logic role)
    --quiz      the questions an examiner asks, without answers
    --answers   the same questions with model answers
    (no flag)   run the reference solutions and mark your variants

Four variants sit at the bottom of every file. They are the "now
change it" adaptations. Forty in total. They matter more than the ten
originals, because the live session grades whether you can ADAPT the
code, not whether you can recite it.
======================================================================
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

FILES = [
    ("lc344_reverse_string.py", "344 Reverse String"),
    ("lc125_valid_palindrome.py", "125 Valid Palindrome"),
    ("lc027_remove_element.py", "27  Remove Element"),
    ("lc283_move_zeroes.py", "283 Move Zeroes"),
    ("lc001_two_sum.py", "1   Two Sum"),
    ("lc217_contains_duplicate.py", "217 Contains Duplicate"),
    ("lc121_best_time_to_buy_and_sell_stock.py", "121 Best Time to Buy/Sell"),
    ("lc268_missing_number.py", "268 Missing Number"),
    ("lc021_merge_two_sorted_lists.py", "21  Merge Two Sorted Lists"),
    ("lc028_first_occurrence.py", "28  First Occurrence in a String"),
]

PLAN = """
STUDY THEM IN THIS ORDER, NOT BY NUMBER
=======================================

Grouped so each problem reuses the idea from the one before. Solving
by LeetCode number throws that away.

  A. TWO POINTERS CONVERGING FROM THE ENDS
       344  Reverse String          the pattern in its purest form
       125  Valid Palindrome        the same loop plus guarded skips

  B. READ / WRITE POINTER, BOTH MOVING FORWARD
       27   Remove Element          overwrite, tail is garbage
       283  Move Zeroes             THE SAME LOOP, one line changed:
                                    swap instead of overwrite

  C. HASH MAP / SET
       1    Two Sum                 check before insert
       217  Contains Duplicate      check before insert, again

  D. ONE PASS CARRYING RUNNING STATE
       121  Best Time to Buy/Sell   cheapest-so-far, best-so-far
       268  Missing Number          the sum you expected, minus the
                                    sum you got

  E. EVERYTHING ELSE
       21   Merge Two Sorted Lists  linked-list pointers, dummy head
       28   First Occurrence        windows, and the +1 that everyone
                                    gets wrong


THE FOUR THINGS TO SAY BEFORE WRITING ANY CODE
==============================================

  1. What PATTERN is this, and what have I solved that is like it?
  2. What is the INVARIANT -- what is true on every single iteration?
  3. What is the TIME and SPACE complexity, and what is the trade?
  4. What are the EDGE CASES, and which does my loop handle for free?

If you cannot state the invariant, you do not understand the problem
yet, and whatever you are about to write is recalled rather than
derived. That distinction is exactly what the live session tests.


THE TWO ROLES
=============

The brief says one of you dictates the logic, explains the algorithm
out loud and dry runs it; the other writes Python and handles edge
cases. Your grade is individual and is about how well you execute YOUR
role -- so know which one you are doing.

  LOGIC / NAVIGATOR
    - name the pattern and the invariant before any code exists
    - state the brute force and its cost, then the improvement
    - dry run on the given example, naming every variable at every
      step (use --trace until you can do it from memory)
    - call out edge cases for your partner to handle

  CODE / DRIVER
    - translate, do not re-derive; if the logic is wrong, say so
    - narrate as you type: "loop while i is less than j"
    - name the edge cases you are covering as you cover them
    - when it works, say the complexity back

Silence is the failure mode for BOTH roles. Communicating your thought
process out loud is graded explicitly.
"""


def main():
    if "--plan" in sys.argv:
        print(PLAN)
        return

    print()
    print("=" * 72)
    print("  ALL TEN -- PROGRESS")
    print("=" * 72)

    grand_done = grand_fail = grand_todo = 0
    for fname, label in FILES:
        path = os.path.join(HERE, fname)
        out = subprocess.run([sys.executable, path],
                             capture_output=True, text=True)
        text = out.stdout + out.stderr
        done = fail = todo = 0
        broken = False
        for line in text.splitlines():
            s = line.strip()
            if " solved   " in s and " not attempted" in s:
                parts = s.split()
                done, fail, todo = int(parts[0]), int(parts[2]), int(parts[4])
        if out.returncode != 0:
            broken = True
        bar = "#" * done + "." * (fail + todo)
        status = "ERROR" if broken else "%d/4" % done
        print("  %-34s [%-4s] %-5s %s"
              % (label, bar, status, "<- broken" if broken else ""))
        grand_done += done
        grand_fail += fail
        grand_todo += todo

    print("-" * 72)
    print("  %d of 40 variants solved   %d failing   %d not attempted"
          % (grand_done, grand_fail, grand_todo))
    print("-" * 72)
    print()
    print("  next:  python leetcode/run_all.py --plan")
    print("         python leetcode/lc344_reverse_string.py --teach")
    print()


if __name__ == "__main__":
    main()
