"""
======================================================================
  LeetCode 217 -- Contains Duplicate
  Notebook concepts: Sets, Hash Tables
======================================================================

THE PROBLEM (as stated on LeetCode)

    Given an integer array nums, return true if any value appears at
    least twice in the array, and return false if every element is
    distinct.

    Example 1:
        Input:  nums = [1,2,3,1]
        Output: true

    Example 2:
        Input:  nums = [1,2,3,4]
        Output: false

    Example 3:
        Input:  nums = [1,1,1,3,3,4,3,2,4,2]
        Output: true

    Constraints:
        1 <= nums.length <= 10^5
        -10^9 <= nums[i] <= 10^9

HOW TO USE THIS FILE
    python leetcode/lc217_contains_duplicate.py --teach / --trace
                                                --quiz  / --answers
    python leetcode/lc217_contains_duplicate.py          run variants
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
STEP 1 -- THE ONE-LINER, AND WHY IT IS NOT THE ANSWER THEY WANT

      return len(set(nums)) != len(nums)

  This is correct, idiomatic, and what you would actually ship. Say it
  immediately -- refusing to mention it looks like you do not know it.

  Then say why you are about to write something else: it always builds
  the ENTIRE set before deciding, even when the duplicate is at index
  1. On [1,1,x,x,...,x] with 100,000 elements it allocates 100,000
  entries to answer a question that was settled after two.

STEP 2 -- THE EARLY-EXIT VERSION

      seen = set()
      for n in nums:
          if n in seen:
              return True
          seen.add(n)
      return False

  Same worst case. Much better best case. And critically, lower PEAK
  MEMORY when a duplicate appears early, which is the argument that
  actually distinguishes the two.

STEP 3 -- CHECK BEFORE ADD, AGAIN

  Exactly the same discipline as Two Sum. If you add first and then
  check, every element finds itself and you return True immediately for
  any non-empty input.

  Notice you have now seen check-before-insert twice. That is not a
  coincidence -- it is the defining habit of this whole pattern. When
  you are asked "what links Two Sum and Contains Duplicate", THAT is
  the answer, not "they both use hashing".

STEP 4 -- THE INVARIANT

      `seen` contains exactly the values at strictly earlier indices.

  So `n in seen` means precisely "this value occurred before", which is
  the definition of a duplicate.

STEP 5 -- COMPLEXITY, AND THE HONEST CAVEAT

  Time  O(n) average.  Space O(n) worst case.

  Both the set and the one-liner are O(n)/O(n). The difference lives
  entirely in the constant and in when you can stop.

  Worth knowing: hashing an int in Python is trivial (hash(n) == n for
  small ints), so collisions are not a practical worry here.

STEP 6 -- THE NO-EXTRA-SPACE ALTERNATIVE

  If someone forbids the O(n) memory:

      nums.sort()
      for i in range(1, len(nums)):
          if nums[i] == nums[i - 1]:
              return True
      return False

  O(n log n) time, O(1) extra space -- but it MUTATES the caller's
  array, which you must flag out loud. Duplicates become adjacent once
  sorted, which is the whole idea.

  This is the trade to have ready: hash set buys time with memory, sort
  buys memory with time and a side effect.

STEP 7 -- EDGE CASES

  [ ]      -> False (nothing can repeat). Constraints forbid it, but
              your loop handles it without special-casing.
  [1]      -> False.
  [1,1]    -> True after two iterations.
  huge n   -> the early-exit version is the one you want.
"""


# ======================================================================
#  THE SOLUTION
# ======================================================================

def solve(nums):
    """True if any value occurs at least twice. Early-exit version."""
    seen = set()
    for n in nums:
        # Check BEFORE add, so `seen` holds only strictly earlier values.
        if n in seen:
            return True
        seen.add(n)
    return False


def solve_oneline(nums):
    """The idiomatic version. Always builds the whole set."""
    return len(set(nums)) != len(nums)


def solve_sorting(nums):
    """O(1) extra space, O(n log n) time -- but it mutates the input."""
    nums = sorted(nums)          # sorted() copies; nums.sort() would mutate
    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1]:
            return True
    return False


# ======================================================================
#  THE DRY RUN
# ======================================================================

def trace(nums):
    print()
    print("  nums = %r" % nums)
    print()
    print("  %-4s %-6s %-10s %-24s %s"
          % ("i", "n", "in seen?", "seen before this step", "action"))
    print("  " + "-" * 66)
    seen = set()
    for i, n in enumerate(nums):
        hit = n in seen
        before = sorted(seen)
        print("  %-4d %-6d %-10s %-24s %s"
              % (i, n, "yes" if hit else "no", before,
                 "RETURN True" if hit else "seen.add(%d)" % n))
        if hit:
            print()
            print("  result: True   (stopped after %d of %d elements)"
                  % (i + 1, len(nums)))
            return
        seen.add(n)
    print()
    print("  result: False   (scanned all %d elements)" % len(nums))


# ======================================================================
#  WHAT THE EXAMINER ASKS
# ======================================================================

EXAMINER = [
    ("What is the one-line solution?",
     """return len(set(nums)) != len(nums). Correct and idiomatic. Say it
        first so it is clear you know it, then explain why you would
        write the loop instead."""),

    ("So why write the loop?",
     """The one-liner always constructs the entire set before deciding.
        The loop stops at the first repeat, so on input where a
        duplicate appears early it does far less work and holds far less
        memory. Same worst case, much better best case."""),

    ("What is the invariant?",
     """`seen` contains exactly the values at strictly earlier indices,
        so `n in seen` means precisely 'this value has occurred
        before'."""),

    ("What breaks if you add before you check?",
     """Every element finds itself, so you return True for any non-empty
        array. It is the same check-before-insert discipline as Two
        Sum."""),

    ("What links this problem to Two Sum?",
     """Both replace a nested scan with a single pass plus O(1)
        membership lookups, and both depend on checking before
        inserting so the structure only ever holds strictly earlier
        elements. That habit is the pattern, not 'they both hash'."""),

    ("Now do it without the extra memory.",
     """Sort, then scan adjacent pairs -- duplicates become neighbours.
        O(n log n) time, O(1) extra space, but it mutates the caller's
        array unless you copy, and copying gives the memory back."""),

    ("Which would you actually ship?",
     """The one-liner, unless profiling showed this on a hot path with
        early duplicates. Readability wins by default; the loop wins
        when the early exit demonstrably matters."""),

    ("Is dict/set lookup guaranteed O(1)?",
     """Average and amortised, yes. Worst case O(n) under adversarial
        collisions. For Python ints, hash(n) == n for small values, so
        it is a non-issue in practice."""),
]


# ======================================================================
#  YOUR TURN -- VARIANTS
# ======================================================================

# V1 | LeetCode 219. True if there are two EQUAL values whose indices
#    | differ by at most k.
#    | ([1,2,3,1], 3) -> True    ([1,2,3,1], 2) -> False
#    | ([1,0,1,1], 1) -> True    ([1,2,3,1,2,3], 2) -> False
#    | Hint: the set must now hold only a WINDOW of the last k values,
#    | not everything. What do you remove, and when?
def contains_nearby_duplicate(nums, k):
    pass


# V2 | Return the first value that repeats -- meaning the one whose
#    | SECOND occurrence comes earliest -- or None if all distinct.
#    | [2,1,3,5,3,2] -> 3   (3 repeats at index 4, 2 not until index 5)
#    | [1,2,3] -> None
#    | Read that definition twice. "First repeated" does NOT mean the
#    | smallest, and does NOT mean the earliest first-occurrence.
def first_repeated(nums):
    pass


# V3 | Return every value appearing at least twice, sorted ascending,
#    | each listed once.
#    | [4,3,2,7,8,2,3,1] -> [2,3]
#    | [1,2,3] -> []
def all_duplicates(nums):
    pass


# V4 | True if any value appears at least THRESHOLD times.
#    | ([1,1,2], 2) -> True    ([1,1,2], 3) -> False
#    | ([1,1,1,2], 3) -> True
#    | The generalisation. Notice a set can no longer do the job --
#    | be ready to say what structure replaces it and why.
def contains_n_duplicates(nums, threshold):
    pass


# ======================================================================
#  TESTS -- do not edit
# ======================================================================

_SOLVE_CASES = [
    ("[1,2,3,1]", lambda f: f([1, 2, 3, 1]), True),
    ("[1,2,3,4]", lambda f: f([1, 2, 3, 4]), False),
    ("long mixed", lambda f: f([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]), True),
    ("single", lambda f: f([7]), False),
    ("empty", lambda f: f([]), False),
    ("negatives", lambda f: f([-1, -2, -1]), True),
    ("adjacent pair", lambda f: f([5, 5]), True),
]

_NEARBY_CASES = [
    ("[1,2,3,1] k=3", lambda f: f([1, 2, 3, 1], 3), True),
    ("[1,2,3,1] k=2", lambda f: f([1, 2, 3, 1], 2), False),
    ("[1,0,1,1] k=1", lambda f: f([1, 0, 1, 1], 1), True),
    ("[1,2,3,1,2,3] k=2", lambda f: f([1, 2, 3, 1, 2, 3], 2), False),
    ("k=0", lambda f: f([1, 1], 0), False),
    ("empty", lambda f: f([], 3), False),
    ("all distinct", lambda f: f([1, 2, 3], 10), False),
]

_FIRST_REPEATED_CASES = [
    ("[2,1,3,5,3,2]", lambda f: f([2, 1, 3, 5, 3, 2]), 3),
    ("[1,2,3]", lambda f: f([1, 2, 3]), None),
    ("[1,1,2,2]", lambda f: f([1, 1, 2, 2]), 1),
    ("[2,2]", lambda f: f([2, 2]), 2),
    ("empty", lambda f: f([]), None),
    ("[5,1,5,1]", lambda f: f([5, 1, 5, 1]), 5),
]

_ALL_DUP_CASES = [
    ("[4,3,2,7,8,2,3,1]", lambda f: f([4, 3, 2, 7, 8, 2, 3, 1]), [2, 3]),
    ("[1,2,3]", lambda f: f([1, 2, 3]), []),
    ("[1,1,1]", lambda f: f([1, 1, 1]), [1]),
    ("negatives", lambda f: f([-1, -1, 0, 0, 5]), [-1, 0]),
    ("empty", lambda f: f([]), []),
]

_THRESHOLD_CASES = [
    ("[1,1,2] t=2", lambda f: f([1, 1, 2], 2), True),
    ("[1,1,2] t=3", lambda f: f([1, 1, 2], 3), False),
    ("[1,1,1,2] t=3", lambda f: f([1, 1, 1, 2], 3), True),
    ("[1,2,3] t=1", lambda f: f([1, 2, 3], 1), True),
    ("empty t=1", lambda f: f([], 1), False),
    ("[5,5,5,5] t=4", lambda f: f([5, 5, 5, 5], 4), True),
]


def main():
    mode = argmode(sys.argv)

    if mode == "teach":
        head("LC 217 -- Contains Duplicate :: THE LESSON")
        print(LESSON)
        return
    if mode == "trace":
        head("LC 217 -- Contains Duplicate :: DRY RUN")
        trace([1, 2, 3, 1])
        trace([1, 1, 9, 9, 9, 9, 9])
        trace([1, 2, 3, 4])
        return
    if mode in ("quiz", "answers"):
        head("LC 217 -- Contains Duplicate :: EXAMINER")
        quiz(EXAMINER, show=(mode == "answers"))
        return

    head("LC 217 -- Contains Duplicate")

    sub("reference solutions")
    check("solve", solve, _SOLVE_CASES)
    check("solve_oneline", solve_oneline, _SOLVE_CASES)
    check("solve_sorting", solve_sorting, _SOLVE_CASES)

    sub("your variants")
    results = [
        check("V1 contains_nearby_duplicate", contains_nearby_duplicate, _NEARBY_CASES),
        check("V2 first_repeated", first_repeated, _FIRST_REPEATED_CASES),
        check("V3 all_duplicates", all_duplicates, _ALL_DUP_CASES),
        check("V4 contains_n_duplicates", contains_n_duplicates, _THRESHOLD_CASES),
    ]
    report(results)


if __name__ == "__main__":
    main()
