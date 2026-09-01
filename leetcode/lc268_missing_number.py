"""
======================================================================
  LeetCode 268 -- Missing Number
  Notebook concepts: Arrays, Math
======================================================================

THE PROBLEM (as stated on LeetCode)

    Given an array nums containing n distinct numbers in the range
    [0, n], return the only number in the range that is missing from
    the array.

    Example 1:
        Input:  nums = [3,0,1]
        Output: 2
        (n = 3, so the range is [0,3]; 2 is the one absent)

    Example 2:
        Input:  nums = [0,1]
        Output: 2
        (n = 2, so the range is [0,2]; 2 is the one absent)

    Example 3:
        Input:  nums = [9,6,4,2,3,5,7,0,1]
        Output: 8

    Constraints:
        n == nums.length
        1 <= n <= 10^4
        0 <= nums[i] <= n
        All the numbers of nums are unique.

    Follow up: could you implement a solution using only O(1) extra
    space complexity and O(n) runtime complexity?

HOW TO USE THIS FILE
    python leetcode/lc268_missing_number.py --teach / --trace
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
STEP 1 -- READ THE RANGE CAREFULLY. IT IS THE WHOLE PROBLEM.

  n numbers, drawn from a range containing n + 1 values: 0, 1, ..., n.

  So there are n+1 slots and n occupants. Exactly one slot is empty.
  If you misread the range as [0, n-1] you will get a correct-looking
  solution that fails on [0,1] -- where the answer is 2, the value
  equal to the length.

  Check yourself with example 2 before writing anything. That example
  exists precisely to catch this.

STEP 2 -- THE BASELINE

      s = set(nums)
      for i in range(len(nums) + 1):
          if i not in s:
              return i

  O(n) time, O(n) space. Correct. State it, then the follow-up asks for
  O(1) space and you have somewhere to go.

STEP 3 -- THE MATH INSIGHT

  You know exactly what the complete set sums to. Gauss:

      0 + 1 + 2 + ... + n  =  n(n + 1) / 2

  The array is that complete set minus one element. So:

      missing = n(n + 1) / 2  -  sum(nums)

  One pass, two integers, done.

      n = len(nums)
      return n * (n + 1) // 2 - sum(nums)

STEP 4 -- THE // THAT PEOPLE GET WRONG

  Use INTEGER division, //, not /.

  In Python 3, / always produces a float. n*(n+1)/2 gives 6.0, not 6,
  and your function returns 6.0 where the test expects 6. Depending on
  the comparison that may or may not fail -- 6.0 == 6 is True in
  Python, but the returned TYPE is wrong, and on large n floats lose
  precision entirely.

  n*(n+1) is always even (consecutive integers, one of them even), so
  // is exact with no rounding concern. Say that: it is not that you
  are truncating, it is that the division is exact.

STEP 5 -- THE XOR ALTERNATIVE, AND THE HONEST CAVEAT

      out = n
      for i, x in enumerate(nums):
          out ^= i ^ x
      return out

  Why it works: XOR is its own inverse (a ^ a == 0) and is commutative
  and associative. XOR-ing together every index 0..n-1, the value n,
  and every array element pairs up every present number with its own
  index. Everything cancels except the one value that has an index but
  no matching element.

  The usual reason to prefer XOR is overflow: in C++ or Java, n(n+1)/2
  can exceed a 32-bit int for large n, while XOR never grows.

  In PYTHON that argument does not apply -- integers are arbitrary
  precision and cannot overflow. So say it exactly like that: "XOR is
  the standard answer to the overflow objection, but Python's ints do
  not overflow, so here it is a stylistic choice rather than a fix."

  Knowing WHY a famous trick is unnecessary in your language is a much
  stronger signal than reciting the trick.

STEP 6 -- COMPLEXITY

  Gauss:   O(n) time (the sum), O(1) space.
  XOR:     O(n) time, O(1) space.
  Set:     O(n) time, O(n) space.
  Sorting: O(n log n) time, O(1) extra -- and it mutates the input.

STEP 7 -- EDGE CASES

  [0]     -> n = 1, total = 1, sum = 0, missing = 1.
  [1]     -> n = 1, total = 1, sum = 1, missing = 0.
  [0,1]   -> n = 2, total = 3, sum = 1, missing = 2. THE key case.
  missing at the front, middle or end all fall out of the same
  arithmetic -- there is no positional special case at all, which is
  the appeal of the approach.
"""


# ======================================================================
#  THE SOLUTION
# ======================================================================

def solve(nums):
    """The one absent value from 0..n. Gauss sum, O(n) time, O(1) space."""
    n = len(nums)
    # // not /  --  n*(n+1) is always even, so the division is exact,
    # and / would hand back a float.
    return n * (n + 1) // 2 - sum(nums)


def solve_xor(nums):
    """XOR version. Same complexity; immune to overflow in languages that overflow."""
    out = len(nums)          # seed with n, the one index that does not exist
    for i, x in enumerate(nums):
        out ^= i ^ x
    return out


def solve_set(nums):
    """The O(n)-space baseline. State it before you optimise."""
    s = set(nums)
    for i in range(len(nums) + 1):
        if i not in s:
            return i
    return -1                # unreachable: exactly one is missing


# ======================================================================
#  THE DRY RUN
# ======================================================================

def trace(nums):
    n = len(nums)
    total = n * (n + 1) // 2
    actual = sum(nums)
    print()
    print("  nums = %r      n = len(nums) = %d" % (nums, n))
    print("  range is [0, %d], so there are %d possible values for %d slots"
          % (n, n + 1, n))
    print()
    print("  complete sum 0+1+...+%d = %d*%d/2 = %d" % (n, n, n + 1, total))
    print("  actual sum of nums       = %d" % actual)
    print("  missing = %d - %d = %d" % (total, actual, total - actual))
    print()
    print("  cross-check with XOR:")
    print("  %-6s %-6s %-6s %s" % ("i", "nums[i]", "i^x", "running out"))
    print("  " + "-" * 44)
    out = n
    print("  %-6s %-6s %-6s %d   (seeded with n)" % ("-", "-", "-", out))
    for i, x in enumerate(nums):
        out ^= i ^ x
        print("  %-6d %-6d %-6d %d" % (i, x, i ^ x, out))
    print()
    print("  result: %d   (both methods agree: %s)"
          % (total - actual, total - actual == out))


# ======================================================================
#  WHAT THE EXAMINER ASKS
# ======================================================================

EXAMINER = [
    ("What exactly is the range of possible values?",
     """0 to n inclusive, where n is the length of the array. That is
        n+1 candidate values for n slots, so exactly one is absent.
        Misreading it as 0..n-1 is the classic error and it fails on
        [0,1], where the answer is 2."""),

    ("Give me the O(n)-space solution first.",
     """Put nums in a set, then scan i from 0 to n and return the first i
        not in the set. O(n) time, O(n) space."""),

    ("Now do it in O(1) space.",
     """Gauss: the complete range sums to n(n+1)/2, and the array is that
        complete range minus one element, so the missing value is
        n(n+1)//2 - sum(nums)."""),

    ("Why // and not /?",
     """/ returns a float in Python 3, so you would return 6.0 rather
        than 6, and floats lose precision on large values. n(n+1) is the
        product of consecutive integers so one of them is even -- the
        division is exact, not truncating."""),

    ("Show me the XOR solution and explain why it works.",
     """Seed with n, then XOR in every index and every element. XOR is
        its own inverse and is commutative, so every value that is
        present cancels against its matching index. The only thing left
        unpaired is the missing value."""),

    ("Why would anyone prefer XOR over the sum?",
     """Overflow. In C++ or Java, n(n+1)/2 can exceed a 32-bit integer,
        while XOR never grows beyond the width of its operands."""),

    ("Does that argument apply in Python?",
     """No. Python integers are arbitrary precision and cannot overflow,
        so here XOR is a stylistic choice rather than a fix. Knowing that
        the famous justification does not apply in this language is the
        actual point."""),

    ("What if the numbers were not distinct?",
     """The Gauss identity collapses immediately -- a duplicate shifts
        the sum by an unknown amount and you can no longer separate
        'missing' from 'repeated' with one equation. You would need two
        equations (sum and sum of squares) or fall back to counting."""),

    ("What if TWO numbers were missing?",
     """One equation cannot determine two unknowns. You would need a
        second independent equation, such as the sum of squares, or
        simply drop to the O(n)-space set approach, or use cyclic
        placement to put each value at its own index and then scan."""),
]


# ======================================================================
#  YOUR TURN -- VARIANTS
# ======================================================================

# V1 | Write the XOR version yourself, from the cancellation argument
#    | rather than from memory. Seed it correctly -- the seed is the
#    | part people get wrong.
#    | [3,0,1] -> 2      [0,1] -> 2      [0] -> 1
def missing_number_xor(nums):
    pass


# V2 | nums is SORTED ascending. Find the missing value in O(log n).
#    | [0,1,3] -> 2      [0,1,2] -> 3      [1,2,3] -> 0
#    | Hint: before the gap, nums[i] == i. After the gap, nums[i] > i.
#    | That is a monotone predicate, which is exactly what binary
#    | search needs. Be very careful about what you return when the
#    | gap is at the very end.
def missing_number_sorted(nums):
    pass


# V3 | Generalise: return EVERY value in the inclusive range [lo, hi]
#    | that does not appear in nums, sorted ascending.
#    | ([3,0,1], 0, 3) -> [2]
#    | ([1,4], 0, 5)   -> [0, 2, 3, 5]
#    | ([], 0, 2)      -> [0, 1, 2]
#    | The guarantees are gone -- no distinctness, no single answer.
#    | Say what that costs you before you write it.
def find_all_missing(nums, lo, hi):
    pass


# V4 | CYCLIC PLACEMENT. Solve the original problem by repeatedly
#    | swapping each value to the index equal to itself, then scanning
#    | for the first index whose value does not match. O(n) time,
#    | O(1) extra space, and no arithmetic identity at all.
#    | [3,0,1] -> 2      [0,1] -> 2      [1] -> 0
#    | Hint: values equal to n have no home index -- leave them where
#    | they are. And after a swap, do NOT advance: the value you just
#    | received has not been placed yet. (You have met that trap
#    | before, in Remove Element.)
#    | Mutating nums is fine here.
def missing_number_cyclic(nums):
    pass


# ======================================================================
#  TESTS -- do not edit
# ======================================================================

_SOLVE_CASES = [
    ("[3,0,1]", lambda f: f([3, 0, 1]), 2),
    ("[0,1]", lambda f: f([0, 1]), 2),
    ("[9,6,4,2,3,5,7,0,1]", lambda f: f([9, 6, 4, 2, 3, 5, 7, 0, 1]), 8),
    ("[0]", lambda f: f([0]), 1),
    ("[1]", lambda f: f([1]), 0),
    ("missing 0", lambda f: f([1, 2, 3]), 0),
    ("missing last", lambda f: f([0, 1, 2]), 3),
    ("missing middle", lambda f: f([0, 1, 3, 4]), 2),
]

_SORTED_CASES = [
    ("[0,1,3]", lambda f: f([0, 1, 3]), 2),
    ("[0,1,2]", lambda f: f([0, 1, 2]), 3),
    ("[1,2,3]", lambda f: f([1, 2, 3]), 0),
    ("[0]", lambda f: f([0]), 1),
    ("[1]", lambda f: f([1]), 0),
    ("[0,1,2,3,5]", lambda f: f([0, 1, 2, 3, 5]), 4),
    ("[0,2,3,4,5]", lambda f: f([0, 2, 3, 4, 5]), 1),
]

_ALL_MISSING_CASES = [
    ("[3,0,1] 0..3", lambda f: f([3, 0, 1], 0, 3), [2]),
    ("[1,4] 0..5", lambda f: f([1, 4], 0, 5), [0, 2, 3, 5]),
    ("[] 0..2", lambda f: f([], 0, 2), [0, 1, 2]),
    ("none missing", lambda f: f([0, 1, 2], 0, 2), []),
    ("duplicates in nums", lambda f: f([1, 1, 1], 0, 3), [0, 2, 3]),
    ("values outside range", lambda f: f([99, 1], 0, 2), [0, 2]),
    ("negative range", lambda f: f([-1, 1], -2, 1), [-2, 0]),
]

_CYCLIC_CASES = [
    ("[3,0,1]", lambda f: f([3, 0, 1]), 2),
    ("[0,1]", lambda f: f([0, 1]), 2),
    ("[9,6,4,2,3,5,7,0,1]", lambda f: f([9, 6, 4, 2, 3, 5, 7, 0, 1]), 8),
    ("[0]", lambda f: f([0]), 1),
    ("[1]", lambda f: f([1]), 0),
    ("missing 0", lambda f: f([1, 2, 3]), 0),
    ("missing last", lambda f: f([0, 1, 2]), 3),
]


def main():
    mode = argmode(sys.argv)

    if mode == "teach":
        head("LC 268 -- Missing Number :: THE LESSON")
        print(LESSON)
        return
    if mode == "trace":
        head("LC 268 -- Missing Number :: DRY RUN")
        trace([3, 0, 1])
        trace([0, 1])
        return
    if mode in ("quiz", "answers"):
        head("LC 268 -- Missing Number :: EXAMINER")
        quiz(EXAMINER, show=(mode == "answers"))
        return

    head("LC 268 -- Missing Number")

    sub("reference solutions")
    check("solve (Gauss)", solve, _SOLVE_CASES)
    check("solve_xor", solve_xor, _SOLVE_CASES)
    check("solve_set", solve_set, _SOLVE_CASES)

    sub("your variants")
    results = [
        check("V1 missing_number_xor", missing_number_xor, _SOLVE_CASES),
        check("V2 missing_number_sorted", missing_number_sorted, _SORTED_CASES),
        check("V3 find_all_missing", find_all_missing, _ALL_MISSING_CASES),
        check("V4 missing_number_cyclic", missing_number_cyclic, _CYCLIC_CASES),
    ]
    report(results)


if __name__ == "__main__":
    main()
