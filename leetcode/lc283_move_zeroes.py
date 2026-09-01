"""
======================================================================
  LeetCode 283 -- Move Zeroes
  Notebook concepts: Two Pointers, In-place Array Modification
======================================================================

THE PROBLEM (as stated on LeetCode)

    Given an integer array nums, move all 0's to the end of it while
    maintaining the relative order of the non-zero elements.

    Note that you must do this in-place without making a copy of the
    array.

    Example 1:
        Input:  nums = [0,1,0,3,12]
        Output: [1,3,12,0,0]

    Example 2:
        Input:  nums = [0]
        Output: [0]

    Constraints:
        1 <= nums.length <= 10^4
        -2^31 <= nums[i] <= 2^31 - 1

    Follow up: Could you minimise the total number of operations done?

HOW TO USE THIS FILE
    python leetcode/lc283_move_zeroes.py --teach / --trace
                                         --quiz  / --answers
    python leetcode/lc283_move_zeroes.py          run your variants
======================================================================
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _harness import head, sub, check, report, quiz, argmode, inplace


# ======================================================================
#  THE LESSON
# ======================================================================

LESSON = """
STEP 1 -- THIS IS PROBLEM 27 WITH ONE LINE CHANGED

  Solve 27 first. Then this becomes a five-second problem, and being
  able to SAY it is 27 with one line changed is worth more than the
  code itself.

  Same loop, same two pointers moving forward, same invariant shape:

      i  reads every slot
      k  marks where the next non-zero gets written

STEP 2 -- WHAT ACTUALLY DIFFERS

  In 27 the tail was declared garbage, so a keeper was OVERWRITTEN into
  place:

      nums[k] = nums[i]

  Here the zeroes are not garbage. They have to end up at the tail, in
  the right quantity. So instead of overwriting, you SWAP:

      nums[k], nums[i] = nums[i], nums[k]

  That is the whole difference. One line.

STEP 3 -- WHY THE SWAP IS CORRECT (the sentence they want)

  The swap does two jobs at once: it pulls the non-zero forward to k,
  AND it kicks whatever was sitting at k out to position i.

  Why is that safe? Because of the invariant:

      nums[0:k]  holds every non-zero seen so far, in order
      nums[k:i]  is ALL ZEROES

  So whenever k < i, nums[k] is guaranteed to be a zero. The swap is
  therefore always "non-zero forward, zero backward" -- never
  "non-zero backward", which would destroy the ordering.

  Say exactly that: "by the invariant, nums[k] is guaranteed to be a
  zero whenever k < i, so the swap can only ever send a zero rightward."

STEP 4 -- WHEN i == k

  If there are no zeroes yet, k has kept pace with i, and the swap
  becomes nums[i], nums[i] = nums[i], nums[i] -- a self-swap. Harmless,
  no special case needed. Same "edges handled for free" move as 344.

  If you want to answer the follow-up about minimising operations, this
  is where you do it: guard the swap with `if i != k`. It changes
  nothing about correctness, only the write count.

STEP 5 -- THE TWO-PHASE ALTERNATIVE

      k = 0
      for x in nums:
          if x != 0:
              nums[k] = x
              k += 1
      for j in range(k, len(nums)):
          nums[j] = 0

  This is literally problem 27 followed by a zero-fill. Same O(n), same
  O(1) space. It does MORE total writes than the swap version when
  zeroes are rare, and FEWER when zeroes are common. Being able to
  compare the two on write count is the real answer to the follow-up.

STEP 6 -- STABILITY IS THE POINT

  Notice you cannot use 27's swap-from-the-end trick here. That trick
  was licensed by "the order of the elements may be changed". This
  problem demands the opposite -- relative order of the non-zeroes must
  survive. The moment stability is required, swap-from-end is
  disqualified by construction.

  Recognising which constraint kills which algorithm is exactly what
  the live session is testing.

STEP 7 -- COMPLEXITY AND EDGES

  Time  O(n), one pass.  Space O(1).

  [0]           -> no non-zeroes, k stays 0, nothing moves.
  [1,2,3]       -> every iteration is a self-swap, array unchanged.
  [0,0,0]       -> loop never enters the if, array unchanged (correct).
  []            -> loop never runs (the constraints forbid it, but your
                   code should not care).
"""


# ======================================================================
#  THE SOLUTION
# ======================================================================

def solve(nums):
    """Move every zero to the end, preserving non-zero order. In place."""
    k = 0                       # next slot for a non-zero
    for i in range(len(nums)):
        if nums[i] != 0:
            # By the invariant nums[k:i] is all zeroes, so when k < i
            # this sends a zero rightward and a non-zero leftward.
            nums[k], nums[i] = nums[i], nums[k]
            k += 1


def solve_two_phase(nums):
    """Problem 27 followed by a zero-fill. Same complexity, different writes."""
    k = 0
    for i in range(len(nums)):
        if nums[i] != 0:
            nums[k] = nums[i]
            k += 1
    for j in range(k, len(nums)):
        nums[j] = 0


# ======================================================================
#  THE DRY RUN
# ======================================================================

def trace(nums):
    nums = list(nums)
    print()
    print("  nums = %r" % nums)
    print()
    print("  %-4s %-8s %-16s %-4s %-18s %s"
          % ("i", "nums[i]", "action", "k", "array", "nums[k:i] all zero?"))
    print("  " + "-" * 72)
    k = 0
    for i in range(len(nums)):
        if nums[i] != 0:
            action = ("self-swap" if i == k else "swap %d <-> %d" % (k, i))
            nums[k], nums[i] = nums[i], nums[k]
            k += 1
        else:
            action = "skip (zero)"
        window = nums[k:i]
        ok = "yes" if all(x == 0 for x in window) else "NO"
        print("  %-4d %-8s %-16s %-4d %-18s %s"
              % (i, nums[i] if nums[i] != 0 else 0, action, k, nums,
                 "%s %r" % (ok, window)))
    print()
    print("  result: %r" % nums)


# ======================================================================
#  WHAT THE EXAMINER ASKS
# ======================================================================

EXAMINER = [
    ("How does this relate to Remove Element?",
     """It is the same read/write pointer loop with exactly one line
        changed. 27 overwrites (nums[k] = nums[i]) because its tail is
        declared garbage; 283 swaps because the zeroes must survive and
        land at the end."""),

    ("Why is the swap guaranteed not to break the ordering?",
     """Because the invariant says nums[k:i] is all zeroes. So whenever
        k < i, nums[k] is a zero, and the swap can only ever move a zero
        rightward and a non-zero leftward."""),

    ("What happens when i equals k?",
     """The swap is a self-swap and does nothing. It arises when no zero
        has been seen yet. Harmless -- no special case needed, though
        guarding it with `if i != k` answers the follow-up about
        minimising operations."""),

    ("Could you use the swap-from-the-end trick from problem 27?",
     """No. That trick is licensed by 27's statement that order may
        change. Here relative order of the non-zeroes must be preserved,
        so pulling elements in from the end is disqualified."""),

    ("Which does fewer writes, the swap version or the two-phase "
     "version?",
     """Depends on the data. The swap version writes twice per non-zero;
        the two-phase version writes once per non-zero plus once per
        zero. So swapping wins when zeroes are common and two-phase wins
        when zeroes are rare."""),

    ("Is your solution stable?",
     """Yes for the non-zeroes -- their relative order is preserved,
        which the problem requires. The zeroes are indistinguishable
        from each other so stability among them is meaningless."""),

    ("What if the array is all zeroes?",
     """The if-body never executes, k stays 0, and the array is already
        correct. No special case."""),
]


# ======================================================================
#  YOUR TURN -- VARIANTS
# ======================================================================

# V1 | Write the two-phase version (compact, then fill) from the idea,
#    | without looking at solve_two_phase. Then be ready to say which
#    | of the two does fewer writes on [0,0,0,0,1] and on [1,2,3,4,0].
def move_zeroes_two_phase(nums):
    pass


# V2 | Move all zeroes to the FRONT instead, keeping the relative order
#    | of the non-zeroes.
#    | [0,1,0,3,12] -> [0,0,1,3,12]
#    | Hint: mirror the whole thing. Walk backwards, and let k start at
#    | the last index. Get the direction of every single pointer right
#    | before you run it.
def move_zeroes_to_front(nums):
    pass


# V3 | Stable partition by a predicate: every element satisfying
#    | pred(x) moves to the front, in order; everything else follows,
#    | ALSO in order. Both halves stable.
#    | ([1,2,3,4,5,6], lambda x: x % 2 == 0) -> [2,4,6,1,3,5]
#    | Careful: the swap trick does NOT keep the second group stable.
#    | Work out why, then decide what you actually need. Saying "the
#    | swap version is unstable for the losers" out loud is the win
#    | here, even before you write the code.
def stable_partition(nums, pred):
    pass


# V4 | Move zeroes to the end, but return the number of SWAPS your
#    | implementation performed (counting a self-swap as zero swaps --
#    | i.e. only count when i != k). Mutate nums as normal.
#    | [0,1,0,3,12] -> array [1,3,12,0,0], returns 3
#    | [1,2,3]      -> array [1,2,3],      returns 0
#    | This checks you can instrument your own loop, which is what a
#    | dry run actually is.
def move_zeroes_counting(nums):
    pass


# ======================================================================
#  TESTS -- do not edit
# ======================================================================

_MOVE_CASES = [
    ("[0,1,0,3,12]", lambda f: inplace(f, [0, 1, 0, 3, 12]), [1, 3, 12, 0, 0]),
    ("[0]", lambda f: inplace(f, [0]), [0]),
    ("no zeroes", lambda f: inplace(f, [1, 2, 3]), [1, 2, 3]),
    ("all zeroes", lambda f: inplace(f, [0, 0, 0]), [0, 0, 0]),
    ("leading run", lambda f: inplace(f, [0, 0, 1]), [1, 0, 0]),
    ("trailing run", lambda f: inplace(f, [1, 0, 0]), [1, 0, 0]),
    ("negatives kept in order", lambda f: inplace(f, [0, -1, 0, -2, 5]), [-1, -2, 5, 0, 0]),
    ("empty", lambda f: inplace(f, []), []),
]

_FRONT_CASES = [
    ("[0,1,0,3,12]", lambda f: inplace(f, [0, 1, 0, 3, 12]), [0, 0, 1, 3, 12]),
    ("[0]", lambda f: inplace(f, [0]), [0]),
    ("no zeroes", lambda f: inplace(f, [1, 2, 3]), [1, 2, 3]),
    ("all zeroes", lambda f: inplace(f, [0, 0, 0]), [0, 0, 0]),
    ("trailing zero", lambda f: inplace(f, [1, 2, 0]), [0, 1, 2]),
    ("empty", lambda f: inplace(f, []), []),
]


def _partition_cases():
    even = lambda x: x % 2 == 0
    pos = lambda x: x > 0
    return [
        ("evens first", lambda f: inplace(f, [1, 2, 3, 4, 5, 6], even), [2, 4, 6, 1, 3, 5]),
        ("both stable", lambda f: inplace(f, [5, 2, 7, 4, 1, 6], even), [2, 4, 6, 5, 7, 1]),
        ("positives", lambda f: inplace(f, [-1, 3, -2, 4], pos), [3, 4, -1, -2]),
        ("none match", lambda f: inplace(f, [1, 3, 5], even), [1, 3, 5]),
        ("all match", lambda f: inplace(f, [2, 4], even), [2, 4]),
        ("empty", lambda f: inplace(f, [], even), []),
    ]


def _counting(f, seq):
    c = list(seq)
    n = f(c)
    return (c, n)


_COUNT_CASES = [
    ("[0,1,0,3,12]", lambda f: _counting(f, [0, 1, 0, 3, 12]), ([1, 3, 12, 0, 0], 3)),
    ("[1,2,3]", lambda f: _counting(f, [1, 2, 3]), ([1, 2, 3], 0)),
    ("[0,0,0]", lambda f: _counting(f, [0, 0, 0]), ([0, 0, 0], 0)),
    ("[0,1]", lambda f: _counting(f, [0, 1]), ([1, 0], 1)),
    ("[1,0,2]", lambda f: _counting(f, [1, 0, 2]), ([1, 2, 0], 1)),
]


def main():
    mode = argmode(sys.argv)

    if mode == "teach":
        head("LC 283 -- Move Zeroes :: THE LESSON")
        print(LESSON)
        return
    if mode == "trace":
        head("LC 283 -- Move Zeroes :: DRY RUN")
        trace([0, 1, 0, 3, 12])
        trace([1, 0, 0, 2])
        return
    if mode in ("quiz", "answers"):
        head("LC 283 -- Move Zeroes :: EXAMINER")
        quiz(EXAMINER, show=(mode == "answers"))
        return

    head("LC 283 -- Move Zeroes")

    sub("reference solutions")
    check("solve", solve, _MOVE_CASES)
    check("solve_two_phase", solve_two_phase, _MOVE_CASES)

    sub("your variants")
    results = [
        check("V1 move_zeroes_two_phase", move_zeroes_two_phase, _MOVE_CASES),
        check("V2 move_zeroes_to_front", move_zeroes_to_front, _FRONT_CASES),
        check("V3 stable_partition", stable_partition, _partition_cases()),
        check("V4 move_zeroes_counting", move_zeroes_counting, _COUNT_CASES),
    ]
    report(results)


if __name__ == "__main__":
    main()
