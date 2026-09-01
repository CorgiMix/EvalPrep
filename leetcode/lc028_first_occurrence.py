"""
======================================================================
  LeetCode 28 -- Find the Index of the First Occurrence in a String
  Notebook concepts: String Manipulation, Slicing
======================================================================

THE PROBLEM (as stated on LeetCode)

    Given two strings needle and haystack, return the index of the
    first occurrence of needle in haystack, or -1 if needle is not
    part of haystack.

    Example 1:
        Input:  haystack = "sadbutsad", needle = "sad"
        Output: 0
        ("sad" occurs at index 0 and again at index 6; return the first)

    Example 2:
        Input:  haystack = "leetcode", needle = "leeto"
        Output: -1

    Constraints:
        1 <= haystack.length, needle.length <= 10^4
        haystack and needle consist of only lowercase English
        characters.

HOW TO USE THIS FILE
    python leetcode/lc028_first_occurrence.py --teach / --trace
                                              --quiz  / --answers
======================================================================
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _harness import head, sub, check, report, quiz, argmode


# ======================================================================
#  THE LESSON
# ======================================================================

LESSON = """
STEP 1 -- THE BUILT-IN, AND WHY YOU STILL SAY IT

      return haystack.find(needle)

  That is the entire problem, and haystack.find already returns -1 when
  absent, which is exactly the required contract. Say it in one breath,
  then say: "but the exercise is to implement it, so here is the
  algorithm."

  Never pretend not to know the built-in. Naming it and then setting it
  aside is what a competent engineer does.

STEP 2 -- THE ALGORITHM: TRY EVERY STARTING POSITION

  For each index i in the haystack, ask whether the m characters
  starting at i equal the needle. First match wins.

      n, m = len(haystack), len(needle)
      for i in range(n - m + 1):
          if haystack[i:i + m] == needle:
              return i
      return -1

STEP 3 -- THE + 1 IS THE ENTIRE DIFFICULTY

  Why `range(n - m + 1)` and not `range(n - m)` or `range(n)`?

  The last position where an m-character window still FITS is index
  n - m. range() is exclusive of its endpoint, so to include n - m you
  must write n - m + 1.

  Check it concretely: haystack "abc" (n=3), needle "c" (m=1). The
  match is at index 2, which is n - m = 2. range(3 - 1) = range(2)
  gives 0 and 1, and you miss it. range(3 - 1 + 1) = range(3) gives
  0, 1, 2 and you find it.

  Derive that on the spot with a two-character example rather than
  trying to remember it. Off-by-one errors are the single most common
  live-coding failure, and showing your check is worth more than
  getting it right silently.

  Bonus: if m > n then n - m + 1 is zero or negative, range() is empty,
  and you correctly return -1 with no special case.

STEP 4 -- WHY SLICING IS ACCEPTABLE HERE

  haystack[i:i+m] allocates a new string of length m on every
  iteration. Strictly, that makes the space O(m) rather than O(1).

  The notebook's stated concepts for this problem are literally
  "String Manipulation, Slicing", so slicing is the intended solution.
  But knowing the cost -- and being able to write the character-by-
  character version that avoids the allocation -- is what separates
  understanding from copying.

STEP 5 -- COMPLEXITY, STATED HONESTLY

  There are up to n - m + 1 starting positions, and each comparison
  costs up to m character checks. So O((n - m + 1) * m), which people
  quote as O(n * m).

  The worst case is real, not theoretical: haystack "aaaaaaaaab",
  needle "aaab". Every window matches on its first three characters and
  fails on the fourth, so you pay nearly the full m at every position.

  Best case is O(n) when the first character rarely matches.

STEP 6 -- NAME KMP, DO NOT WRITE KMP

  There is an O(n + m) algorithm: Knuth-Morris-Pratt. It precomputes,
  for each prefix of the needle, the length of the longest proper
  prefix that is also a suffix, so that after a mismatch it can skip
  ahead instead of restarting.

  In a 30-minute pair-programming session, the right move is: name it,
  state its complexity, explain in one sentence what the prefix table
  buys you, and then say you would write the O(n*m) version unless the
  input size demanded otherwise. That is a senior answer. Attempting
  KMP from memory under time pressure is not.

STEP 7 -- EDGE CASES

  needle longer than haystack -> range is empty, return -1.
  needle == haystack          -> matches at 0.
  empty needle                -> the loop matches immediately at i = 0,
                                 returning 0. That is the convention
                                 Python's str.find uses too. The
                                 constraints forbid it, but knowing what
                                 your code does on it is the point.
  repeated occurrences        -> the loop returns the first, because it
                                 scans left to right and returns on the
                                 first hit.
"""


# ======================================================================
#  THE SOLUTION
# ======================================================================

def solve(haystack, needle):
    """Index of the first occurrence of needle in haystack, else -1."""
    n, m = len(haystack), len(needle)
    # n - m is the last index where an m-wide window still fits;
    # range() excludes its endpoint, hence the + 1.
    # If m > n this range is empty and we correctly fall through to -1.
    for i in range(n - m + 1):
        if haystack[i:i + m] == needle:
            return i
    return -1


def solve_no_slicing(haystack, needle):
    """Same algorithm without allocating a slice per iteration. O(1) space."""
    n, m = len(haystack), len(needle)
    for i in range(n - m + 1):
        j = 0
        while j < m and haystack[i + j] == needle[j]:
            j += 1
        if j == m:                 # ran the whole needle without a mismatch
            return i
    return -1


# ======================================================================
#  THE DRY RUN
# ======================================================================

def trace(haystack, needle):
    n, m = len(haystack), len(needle)
    print()
    print("  haystack = %r  (n = %d)" % (haystack, n))
    print("  needle   = %r  (m = %d)" % (needle, m))
    print("  windows to try: range(n - m + 1) = range(%d) -> %s"
          % (n - m + 1, list(range(max(0, n - m + 1)))))
    print()
    print("  %-5s %-14s %-10s %s" % ("i", "haystack[i:i+m]", "== needle?", "action"))
    print("  " + "-" * 52)
    for i in range(n - m + 1):
        window = haystack[i:i + m]
        hit = window == needle
        print("  %-5d %-14r %-10s %s"
              % (i, window, "yes" if hit else "no",
                 "RETURN %d" % i if hit else "advance"))
        if hit:
            print()
            print("  result: %d" % i)
            return
    print()
    print("  result: -1  (no window matched)")


# ======================================================================
#  WHAT THE EXAMINER ASKS
# ======================================================================

EXAMINER = [
    ("What is the built-in that does this?",
     """haystack.find(needle), which already returns -1 when absent.
        Name it, then implement the algorithm because that is the
        exercise. Pretending not to know it is worse than using it."""),

    ("Why does your loop run to n - m + 1?",
     """n - m is the last index at which an m-character window still
        fits inside the haystack, and range excludes its endpoint, so
        you need + 1 to include it. On haystack 'abc' and needle 'c'
        the match is at index 2 == n - m, and range(n - m) would miss
        it."""),

    ("What happens if needle is longer than haystack?",
     """n - m + 1 is zero or negative, range is empty, the loop body
        never runs and you return -1. No special case needed."""),

    ("What is the time complexity?",
     """O((n - m + 1) * m), usually quoted as O(n*m). Up to n - m + 1
        starting positions, each costing up to m character
        comparisons."""),

    ("Give me an input that actually hits the worst case.",
     """haystack = 'aaaaaaaaab', needle = 'aaab'. Every window matches
        on its leading a's and fails only at the last character, so you
        pay nearly the full m at every starting position."""),

    ("Your slicing version -- is it really O(1) space?",
     """No. haystack[i:i+m] allocates a fresh string of length m each
        iteration, so it is O(m) space. The character-by-character
        version compares in place and is genuinely O(1)."""),

    ("Is there a faster algorithm?",
     """Yes, Knuth-Morris-Pratt, O(n + m). It precomputes for each
        prefix of the needle the longest proper prefix that is also a
        suffix, which lets it resume after a mismatch instead of
        restarting the window. I would name it and implement the O(n*m)
        version unless the input size demanded otherwise."""),

    ("What does your code return for an empty needle?",
     """0 -- the first window is the empty string and matches
        immediately. That is the same convention as Python's str.find.
        The constraints forbid it, but the behaviour is defined."""),

    ("If there are several occurrences, which do you return?",
     """The first, because the scan runs left to right and returns on
        the first match. 'sadbutsad' with 'sad' returns 0, not 6."""),
]


# ======================================================================
#  YOUR TURN -- VARIANTS
# ======================================================================

# V1 | Write the version with NO slicing -- compare character by
#    | character. Then say what its space complexity is and why that
#    | differs from the slicing version.
#    | ("sadbutsad", "sad") -> 0        ("leetcode", "leeto") -> -1
#    | Hint: an inner counter j, and after the inner loop you must
#    | distinguish "ran out of needle" from "hit a mismatch". How?
def str_str_no_slicing(haystack, needle):
    pass


# V2 | Return the index of the LAST occurrence instead of the first,
#    | or -1. Do not use rfind.
#    | ("sadbutsad", "sad") -> 6        ("aaa", "a") -> 2
#    | There are two ways: scan forward and remember, or scan the
#    | window positions backwards and return immediately. Say which
#    | you chose and why.
def last_occurrence(haystack, needle):
    pass


# V3 | Count occurrences, ALLOWING OVERLAP.
#    | ("aaa", "aa") -> 2   (indices 0 and 1 -- they overlap)
#    | ("sadbutsad", "sad") -> 2        ("abc", "z") -> 0
#    | Note that "aaa".count("aa") returns 1, because str.count does
#    | NOT count overlaps. Knowing that the built-in answers a
#    | different question is the trap here.
def count_occurrences(haystack, needle):
    pass


# V4 | LeetCode 796. Return True if goal is a rotation of s -- that is,
#    | if some number of left-shifts of s produces goal.
#    | ("abcde", "cdeab") -> True       ("abcde", "abced") -> False
#    | Hint: every rotation of s appears as a substring of s + s.
#    | Convince yourself WHY on paper, and do not forget the length
#    | check -- without it "ab" and "a" would pass.
def is_rotation(s, goal):
    pass


# ======================================================================
#  TESTS -- do not edit
# ======================================================================

_SOLVE_CASES = [
    ("sadbutsad / sad", lambda f: f("sadbutsad", "sad"), 0),
    ("leetcode / leeto", lambda f: f("leetcode", "leeto"), -1),
    ("needle longer", lambda f: f("ab", "abcdef"), -1),
    ("identical", lambda f: f("abc", "abc"), 0),
    ("at the end", lambda f: f("abc", "c"), 2),
    ("worst case", lambda f: f("aaaaaaaaab", "aaab"), 6),
    ("single char miss", lambda f: f("abc", "z"), -1),
    ("mississippi / issip", lambda f: f("mississippi", "issip"), 4),
]

_LAST_CASES = [
    ("sadbutsad / sad", lambda f: f("sadbutsad", "sad"), 6),
    ("aaa / a", lambda f: f("aaa", "a"), 2),
    ("leetcode / leeto", lambda f: f("leetcode", "leeto"), -1),
    ("identical", lambda f: f("abc", "abc"), 0),
    ("aaa / aa", lambda f: f("aaa", "aa"), 1),
    ("needle longer", lambda f: f("ab", "abcdef"), -1),
]

_COUNT_CASES = [
    ("aaa / aa (overlap)", lambda f: f("aaa", "aa"), 2),
    ("sadbutsad / sad", lambda f: f("sadbutsad", "sad"), 2),
    ("abc / z", lambda f: f("abc", "z"), 0),
    ("aaaa / a", lambda f: f("aaaa", "a"), 4),
    ("aaaa / aa", lambda f: f("aaaa", "aa"), 3),
    ("needle longer", lambda f: f("ab", "abc"), 0),
]

_ROTATION_CASES = [
    ("abcde / cdeab", lambda f: f("abcde", "cdeab"), True),
    ("abcde / abced", lambda f: f("abcde", "abced"), False),
    ("identical", lambda f: f("abc", "abc"), True),
    ("length mismatch", lambda f: f("ab", "a"), False),
    ("both empty", lambda f: f("", ""), True),
    ("aa / aa", lambda f: f("aa", "aa"), True),
    ("abab / baba", lambda f: f("abab", "baba"), True),
    ("length mismatch other way", lambda f: f("a", "ab"), False),
]


def main():
    mode = argmode(sys.argv)

    if mode == "teach":
        head("LC 28 -- First Occurrence in a String :: THE LESSON")
        print(LESSON)
        return
    if mode == "trace":
        head("LC 28 -- First Occurrence in a String :: DRY RUN")
        trace("sadbutsad", "sad")
        trace("leetcode", "leeto")
        trace("aaaaaaaaab", "aaab")
        return
    if mode in ("quiz", "answers"):
        head("LC 28 -- First Occurrence in a String :: EXAMINER")
        quiz(EXAMINER, show=(mode == "answers"))
        return

    head("LC 28 -- Find the Index of the First Occurrence in a String")

    sub("reference solutions")
    check("solve", solve, _SOLVE_CASES)
    check("solve_no_slicing", solve_no_slicing, _SOLVE_CASES)

    sub("your variants")
    results = [
        check("V1 str_str_no_slicing", str_str_no_slicing, _SOLVE_CASES),
        check("V2 last_occurrence", last_occurrence, _LAST_CASES),
        check("V3 count_occurrences", count_occurrences, _COUNT_CASES),
        check("V4 is_rotation", is_rotation, _ROTATION_CASES),
    ]
    report(results)


if __name__ == "__main__":
    main()
