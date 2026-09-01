"""
======================================================================
  LeetCode 1 -- Two Sum
  Notebook concepts: Hash Maps, Array Traversal
======================================================================

THE PROBLEM (as stated on LeetCode)

    Given an array of integers nums and an integer target, return
    indices of the two numbers such that they add up to target.

    You may assume that each input would have exactly one solution, and
    you may not use the same element twice.

    You can return the answer in any order.

    Example 1:
        Input:  nums = [2,7,11,15], target = 9
        Output: [0,1]        (2 + 7 == 9)

    Example 2:
        Input:  nums = [3,2,4], target = 6
        Output: [1,2]

    Example 3:
        Input:  nums = [3,3], target = 6
        Output: [0,1]

    Constraints:
        2 <= nums.length <= 10^4
        -10^9 <= nums[i] <= 10^9
        -10^9 <= target <= 10^9
        Only one valid answer exists.

    Follow up: can you come up with an algorithm less than O(n^2)?

HOW TO USE THIS FILE
    python leetcode/lc001_two_sum.py --teach / --trace
                                     --quiz  / --answers
    python leetcode/lc001_two_sum.py          run your variants
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
STEP 1 -- START WITH THE BRUTE FORCE, OUT LOUD

      for i in range(n):
          for j in range(i + 1, n):
              if nums[i] + nums[j] == target:
                  return [i, j]

  O(n^2) time, O(1) space. Correct. SAY IT ANYWAY. Two reasons: it
  proves you understand what is being asked before you optimise, and
  the follow-up literally asks you to beat it -- you cannot beat
  something you never stated.

  Note `range(i + 1, n)`, not `range(n)`. That is what enforces "you
  may not use the same element twice".

STEP 2 -- WHAT THE INNER LOOP IS ACTUALLY DOING

  Rewrite the condition:

      nums[i] + nums[j] == target        becomes
      nums[j] == target - nums[i]

  The inner loop is not doing arithmetic. It is asking a MEMBERSHIP
  question: "have I seen the value target - nums[i]?"

  Membership questions are what hash maps answer in O(1). That single
  rewrite is the entire insight, and it is the thing to say out loud.

STEP 3 -- WHY A MAP AND NOT A SET

  A set would tell you the value exists. You must return INDICES. So
  you store value -> index.

STEP 4 -- THE ORDER OF CHECK AND INSERT DECIDES CORRECTNESS

  This is the trap, and it is the whole reason this problem is worth
  anything.

  WRONG -- insert first, then check:

      seen[n] = i
      if target - n in seen:
          return [seen[target - n], i]

  Run it on nums = [3,2,4], target = 6. At i = 0 you insert {3: 0},
  then look for 6 - 3 = 3, find it at index 0, and return [0, 0]. You
  have used the same element twice. The answer is [1, 2].

  RIGHT -- check first, then insert:

      if target - n in seen:
          return [seen[target - n], i]
      seen[n] = i

  Checking before inserting means `seen` contains only STRICTLY
  EARLIER indices. The current element cannot pair with itself because
  it is not in the map yet.

  Say it in exactly those words: "I check before I insert, so the map
  only ever holds strictly earlier indices."

STEP 5 -- WHY DUPLICATE VALUES ARE NOT A PROBLEM

  nums = [3,3], target = 6. Storing value -> index means the second 3
  would overwrite the first. Does that break it?

  No. At i = 1 you check FIRST: 6 - 3 = 3 is in seen at index 0, so you
  return [0, 1] before the overwrite ever happens. Check-before-insert
  saves you a second time.

  And in general, overwriting is harmless because the problem
  guarantees exactly one solution -- there is never a second pairing
  that needed the older index.

STEP 6 -- COMPLEXITY

  Time  O(n)  -- one pass, O(1) average per lookup and insert.
  Space O(n)  -- the map, in the worst case every element.

  Note "average". Dict operations are O(1) amortised average, O(n)
  worst case under adversarial hash collisions. Nobody will fail you
  for saying O(1), but knowing the caveat is a differentiator.

  You have traded O(n) memory for a factor of n in time. Being able to
  name the trade rather than just perform it is the point.

STEP 7 -- EDGE CASES

  The constraints do a lot of work for you: at least 2 elements, and
  exactly one solution guaranteed. So no empty input, no "not found".
  The `return []` at the end is unreachable defensive code -- SAY that
  it is unreachable and why, rather than leaving it unexplained.

  Negative numbers and a negative target work with no changes: the
  arithmetic target - n does not care about sign.
"""


# ======================================================================
#  THE SOLUTION
# ======================================================================

def solve(nums, target):
    """Return the indices of the two values summing to target."""
    seen = {}                        # value -> index of that value
    for i, n in enumerate(nums):
        need = target - n
        # CHECK before INSERT: `seen` therefore holds only strictly
        # earlier indices, so an element can never pair with itself.
        if need in seen:
            return [seen[need], i]
        seen[n] = i
    return []                        # unreachable: one solution guaranteed


def solve_brute(nums, target):
    """The O(n^2) baseline. State this before you optimise."""
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


# ======================================================================
#  THE DRY RUN
# ======================================================================

def trace(nums, target):
    print()
    print("  nums = %r, target = %d" % (nums, target))
    print()
    print("  %-4s %-6s %-8s %-10s %-22s %s"
          % ("i", "n", "need", "in seen?", "seen before this step", "action"))
    print("  " + "-" * 72)
    seen = {}
    for i, n in enumerate(nums):
        need = target - n
        hit = need in seen
        action = ("RETURN [%d, %d]" % (seen[need], i)) if hit else "seen[%d] = %d" % (n, i)
        print("  %-4d %-6d %-8d %-10s %-22s %s"
              % (i, n, need, "yes" if hit else "no", seen, action))
        if hit:
            print()
            print("  result: [%d, %d]   (%d + %d == %d)"
                  % (seen[need], i, nums[seen[need]], n, target))
            return
        seen[n] = i
    print()
    print("  result: [] -- unreachable given the problem guarantee")


# ======================================================================
#  WHAT THE EXAMINER ASKS
# ======================================================================

EXAMINER = [
    ("What is the brute force, and what does it cost?",
     """Two nested loops, the inner starting at i+1 so an element cannot
        pair with itself. O(n^2) time, O(1) space."""),

    ("How did you get from O(n^2) to O(n)?",
     """By rewriting the condition. nums[i] + nums[j] == target is the
        same as nums[j] == target - nums[i], which is a membership
        question, and a hash map answers membership in O(1). The inner
        loop was never doing arithmetic, it was doing a lookup."""),

    ("Why a dict rather than a set?",
     """A set proves the value exists; the problem wants indices. So you
        store value -> index."""),

    ("Walk me through [3,2,4] with target 6 if you insert before you "
     "check.",
     """At i=0 you insert {3:0}, then look for 6-3=3 and find it at
        index 0, returning [0,0] -- the same element used twice. Correct
        answer is [1,2]. Checking before inserting keeps the map holding
        only strictly earlier indices, which makes self-pairing
        impossible."""),

    ("Duplicate values overwrite each other in your map. Why is that "
     "safe?",
     """On [3,3] with target 6 the check at i=1 fires before the
        overwrite, returning [0,1]. More generally the problem
        guarantees exactly one solution, so no discarded index was ever
        needed."""),

    ("What is the space complexity, and is the trade worth it?",
     """O(n) for the map. You buy a factor of n in time with n units of
        memory. Worth it here; if memory were the binding constraint and
        the array were sortable, the two-pointer approach on a sorted
        copy is O(n log n) time and O(1) extra space."""),

    ("Is dict lookup really O(1)?",
     """O(1) on average and amortised. The worst case is O(n) under
        pathological hash collisions, so strictly the algorithm is O(n)
        expected, O(n^2) worst case. In practice O(n)."""),

    ("What if the array were already sorted?",
     """Then you would not need the map at all. Two pointers from both
        ends: if the sum is too big move the right pointer in, too small
        move the left pointer out. O(n) time, O(1) space. That is
        LeetCode 167."""),

    ("Your last line is `return []`. When does it execute?",
     """Never, given the guarantee of exactly one solution. It exists so
        the function has a defined value on every path. Saying it is
        unreachable, rather than leaving it silent, is the point."""),
]


# ======================================================================
#  YOUR TURN -- VARIANTS
# ======================================================================

# V1 | LeetCode 167. nums is SORTED ascending. Return the 1-INDEXED
#    | positions of the pair summing to target. O(1) extra space.
#    | ([2,7,11,15], 9) -> [1,2]
#    | Hint: converging two pointers. If the sum is too large, which
#    | pointer must move, and why is that move guaranteed safe?
#    | Watch the 1-indexing -- it is the trap on this one.
def two_sum_sorted(nums, target):
    pass


# V2 | Return ALL unique VALUE pairs that sum to target, each pair as
#    | a tuple (a, b) with a <= b, and the whole list sorted ascending.
#    | No duplicate pairs in the output.
#    | ([1,2,3,4,3], 5) -> [(1,4), (2,3)]
#    | The "exactly one solution" guarantee is gone. Think about what
#    | that breaks in your original approach before you write anything.
def two_sum_all_pairs(nums, target):
    pass


# V3 | Count the number of INDEX pairs (i, j) with i < j and
#    | nums[i] + nums[j] == target.
#    | ([1,1,1], 2) -> 3        ([1,2,3], 5) -> 1        ([1,2], 4) -> 0
#    | Hint: a plain set loses information you now need. What does the
#    | map have to store instead of an index?
def two_sum_count_pairs(nums, target):
    pass


# V4 | Return the indices as before, but if NO pair exists return None
#    | instead of assuming a solution. Same O(n).
#    | This is the "the guarantee has been withdrawn" adaptation, and
#    | it is the single most likely live change on this problem.
#    | ([1,2,3], 100) -> None      ([2,7], 9) -> [0,1]
def two_sum_maybe(nums, target):
    pass


# ======================================================================
#  TESTS -- do not edit
# ======================================================================

_SOLVE_CASES = [
    ("[2,7,11,15] t=9", lambda f: f([2, 7, 11, 15], 9), [0, 1]),
    ("[3,2,4] t=6", lambda f: f([3, 2, 4], 6), [1, 2]),
    ("[3,3] t=6", lambda f: f([3, 3], 6), [0, 1]),
    ("negatives", lambda f: f([-3, 4, 3, 90], 0), [0, 2]),
    ("negative target", lambda f: f([5, -2, -4], -6), [1, 2]),
    ("last pair", lambda f: f([1, 5, 2, 8], 10), [2, 3]),
]

_SORTED_CASES = [
    ("[2,7,11,15] t=9", lambda f: f([2, 7, 11, 15], 9), [1, 2]),
    ("[2,3,4] t=6", lambda f: f([2, 3, 4], 6), [1, 3]),
    ("[-1,0] t=-1", lambda f: f([-1, 0], -1), [1, 2]),
    ("[1,2,3,4,4,9,56,90] t=8", lambda f: f([1, 2, 3, 4, 4, 9, 56, 90], 8), [4, 5]),
    ("[0,0,3,4] t=0", lambda f: f([0, 0, 3, 4], 0), [1, 2]),
]

_ALL_PAIRS_CASES = [
    ("[1,2,3,4,3] t=5", lambda f: f([1, 2, 3, 4, 3], 5), [(1, 4), (2, 3)]),
    ("[1,1,1,1] t=2", lambda f: f([1, 1, 1, 1], 2), [(1, 1)]),
    ("no pairs", lambda f: f([1, 2, 3], 100), []),
    ("negatives", lambda f: f([-1, 0, 1, 2, -1], 0), [(-1, 1)]),
    ("zero needs a partner", lambda f: f([-1, 0, 0, 1], 0), [(-1, 1), (0, 0)]),
    ("empty", lambda f: f([], 5), []),
]

_COUNT_CASES = [
    ("[1,1,1] t=2", lambda f: f([1, 1, 1], 2), 3),
    ("[1,2,3] t=5", lambda f: f([1, 2, 3], 5), 1),
    ("[1,2] t=4", lambda f: f([1, 2], 4), 0),
    ("[0,0,0,0] t=0", lambda f: f([0, 0, 0, 0], 0), 6),
    ("[1,5,7,-1,5] t=6", lambda f: f([1, 5, 7, -1, 5], 6), 3),
    ("empty", lambda f: f([], 0), 0),
]

_MAYBE_CASES = [
    ("[2,7] t=9", lambda f: f([2, 7], 9), [0, 1]),
    ("[1,2,3] t=100", lambda f: f([1, 2, 3], 100), None),
    ("empty", lambda f: f([], 0), None),
    ("single", lambda f: f([5], 10), None),
    ("[3,2,4] t=6", lambda f: f([3, 2, 4], 6), [1, 2]),
    ("[3] pairs with itself?", lambda f: f([3], 6), None),
]


def main():
    mode = argmode(sys.argv)

    if mode == "teach":
        head("LC 1 -- Two Sum :: THE LESSON")
        print(LESSON)
        return
    if mode == "trace":
        head("LC 1 -- Two Sum :: DRY RUN")
        trace([2, 7, 11, 15], 9)
        trace([3, 2, 4], 6)
        trace([3, 3], 6)
        return
    if mode in ("quiz", "answers"):
        head("LC 1 -- Two Sum :: EXAMINER")
        quiz(EXAMINER, show=(mode == "answers"))
        return

    head("LC 1 -- Two Sum")

    sub("reference solutions")
    check("solve", solve, _SOLVE_CASES)
    check("solve_brute", solve_brute, _SOLVE_CASES)

    sub("your variants")
    results = [
        check("V1 two_sum_sorted", two_sum_sorted, _SORTED_CASES),
        check("V2 two_sum_all_pairs", two_sum_all_pairs, _ALL_PAIRS_CASES),
        check("V3 two_sum_count_pairs", two_sum_count_pairs, _COUNT_CASES),
        check("V4 two_sum_maybe", two_sum_maybe, _MAYBE_CASES),
    ]
    report(results)


if __name__ == "__main__":
    main()
