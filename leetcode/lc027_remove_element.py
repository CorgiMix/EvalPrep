"""
======================================================================
  LeetCode 27 -- Remove Element
  Notebook concepts: Arrays, Basic Iteration
======================================================================

THE PROBLEM (as stated on LeetCode)

    Given an integer array nums and an integer val, remove all
    occurrences of val in nums in-place. The order of the elements may
    be changed. Then return the number of elements in nums which are
    not equal to val.

    Consider the number of elements in nums which are not equal to val
    be k. To get accepted you need to do the following things:

      - Change the array nums such that the first k elements of nums
        contain the elements which are not equal to val.
      - The remaining elements of nums are not important, as well as
        the size of nums.
      - Return k.

    Example 1:
        Input:  nums = [3,2,2,3], val = 3
        Output: 2, nums = [2,2,_,_]

    Example 2:
        Input:  nums = [0,1,2,2,3,0,4,2], val = 2
        Output: 5, nums = [0,1,4,0,3,_,_,_]

    Constraints:
        0 <= nums.length <= 100
        0 <= nums[i] <= 50
        0 <= val <= 100

HOW TO USE THIS FILE
    python leetcode/lc027_remove_element.py --teach / --trace
                                            --quiz  / --answers
    python leetcode/lc027_remove_element.py          run your variants
======================================================================
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _harness import (head, sub, check, report, quiz, argmode,
                      inplace_k, inplace_k_ordered)


# ======================================================================
#  THE LESSON
# ======================================================================

LESSON = """
STEP 1 -- READ THE GRADING RULE, NOT THE TITLE

  Nothing is deleted. The array keeps its length. You return a COUNT,
  and the judge only ever looks at nums[0:k]. Everything past k is
  explicitly declared garbage.

  That permission is what makes an O(1)-space answer possible at all,
  and stating it back is the first thing to say out loud.

STEP 2 -- THE PATTERN: READ POINTER AND WRITE POINTER

  This is a different two-pointer shape from 344 and 125. There the
  pointers came from opposite ends. Here BOTH move forward:

      i  reads every slot, once, left to right
      k  marks where the next KEEPER gets written

STEP 3 -- THE INVARIANT

      nums[0:k] holds every keeper found so far, in original order,
      and k <= i always.

  The second half is the safety proof. k only advances when i does, and
  i advances every single iteration, so k can never overtake i. That is
  precisely why writing into nums[k] can never clobber a cell you have
  not read yet. In-place is safe BECAUSE of that inequality -- say it
  in those words.

STEP 4 -- THE CODE

      k = 0
      for i in range(len(nums)):
          if nums[i] != val:
              nums[k] = nums[i]
              k += 1
      return k

  Four lines. The whole difficulty was giving yourself permission to
  ignore the tail.

STEP 5 -- THE SECOND VALID ALGORITHM (and why the problem hints at it)

  Notice the problem says "the order of the elements MAY BE CHANGED".
  That sentence is not filler -- it licenses a different approach:

      i, n = 0, len(nums)
      while i < n:
          if nums[i] == val:
              nums[i] = nums[n - 1]   # pull the last element over it
              n -= 1                  # and shrink the array
          else:
              i += 1
      return n

  Compare the WRITE counts. The first version writes once per keeper,
  so up to n writes. The second writes once per REMOVAL. If val is rare
  the second does almost no writing; if val is everywhere the first is
  better. Neither is faster in big-O -- both O(n) -- but "which one and
  why" is a genuine engineering answer, and it is the follow-up.

  Careful with the second one: after copying nums[n-1] into position i
  you must NOT increment i, because the element you just pulled in has
  not been examined yet. Incrementing there is the classic bug.

STEP 6 -- COMPLEXITY AND EDGES

  Time  O(n), one pass.   Space O(1), one integer.

  []                    -> loop never runs, k = 0.
  every element == val  -> k = 0, nothing written.
  no element == val     -> k = n, and every write is nums[i] = nums[i],
                           a harmless self-assignment.
"""


# ======================================================================
#  THE SOLUTION
# ======================================================================

def solve(nums, val):
    """Compact nums in place; return the count of surviving elements."""
    k = 0
    for i in range(len(nums)):
        if nums[i] != val:
            # Safe because k <= i is an invariant: we never write over
            # a cell that has not already been read.
            nums[k] = nums[i]
            k += 1
    return k


def solve_swap_from_end(nums, val):
    """The order-changing variant. Writes once per REMOVAL, not per keeper."""
    i, n = 0, len(nums)
    while i < n:
        if nums[i] == val:
            nums[i] = nums[n - 1]
            n -= 1          # note: i does NOT advance -- the pulled-in
        else:               # element still has to be examined
            i += 1
    return n


# ======================================================================
#  THE DRY RUN
# ======================================================================

def trace(nums, val):
    nums = list(nums)
    print()
    print("  nums = %r, val = %d" % (nums, val))
    print()
    print("  %-4s %-8s %-7s %-14s %-4s %s"
          % ("i", "nums[i]", "keep?", "write", "k", "array"))
    print("  " + "-" * 62)
    k = 0
    for i in range(len(nums)):
        if nums[i] != val:
            action = "nums[%d] = %d" % (k, nums[i])
            nums[k] = nums[i]
            k += 1
            keep = "yes"
        else:
            action = "--"
            keep = "no"
        print("  %-4d %-8d %-7s %-14s %-4d %s"
              % (i, nums[i], keep, action, k, nums))
    print()
    print("  return k = %d   ->  judge reads nums[0:%d] = %r" % (k, k, nums[:k]))
    print("  (nums[%d:] = %r is declared garbage by the problem)" % (k, nums[k:]))


# ======================================================================
#  WHAT THE EXAMINER ASKS
# ======================================================================

EXAMINER = [
    ("Why is it safe to write into nums while you are still reading it?",
     """Because k <= i is an invariant. k only advances when i advances,
        and i advances every iteration, so the write index never
        overtakes the read index. You can only ever overwrite a cell you
        have already consumed."""),

    ("What does the caller see in nums[k:] afterwards?",
     """Leftover stale values. The problem explicitly says they do not
        matter, which is exactly the permission that makes an O(1)-space
        solution possible."""),

    ("The problem says the order may be changed. Why does it bother "
     "telling you that?",
     """It licenses the swap-from-the-end algorithm: on a hit, copy the
        last element over the current one and shrink the logical length.
        That writes once per removal instead of once per keeper, which
        wins when val is rare."""),

    ("In the swap-from-end version, why must you not increment i after "
     "a removal?",
     """The element you just pulled in from the end has never been
        examined. If it also equals val and you skip past it, it
        survives. That is the standard bug in this variant."""),

    ("Is either version asymptotically faster?",
     """No, both are O(n) time and O(1) space. The difference is the
        constant factor on writes, which matters if writes are expensive
        -- memory-mapped data, for instance."""),

    ("What if the array is empty?",
     """range(0) is empty, the loop body never runs, k stays 0 and you
        return 0. No special case needed."""),

    ("Now keep the order AND make it stable. Which version do you use?",
     """The first one. Swap-from-end destroys relative order by
        construction, so it is disqualified the moment stability is
        required. Move Zeroes (283) is exactly that situation."""),
]


# ======================================================================
#  YOUR TURN -- VARIANTS
# ======================================================================

# V1 | Write the swap-from-the-end version yourself, from the idea
#    | rather than from the lesson text above. Same signature, same
#    | return value; order of the survivors is allowed to differ.
#    | Watch the "do not increment i" trap.
def remove_element_swap_end(nums, val):
    pass


# V2 | LeetCode 26. nums is SORTED ascending. Remove the duplicates in
#    | place so each distinct value appears once; return the new k.
#    | [1,1,2] -> 2, nums[0:2] == [1,2]
#    | Hint: identical loop. The only change is the keep-test -- and
#    | because the array is sorted, "is this a new value" is a question
#    | you can answer by looking at ONE previously written element.
def remove_duplicates_sorted(nums):
    pass


# V3 | Generalise: keep every element for which pred(x) is True, drop
#    | the rest, preserving order. Return k.
#    | This is the abstraction the other three are instances of, and
#    | recognising that out loud is worth marks.
#    | ([1,2,3,4,5,6], lambda x: x % 2 == 0) -> 3, nums[0:3] == [2,4,6]
def keep_if(nums, pred):
    pass


# V4 | LeetCode 80. nums is SORTED. Allow each value to appear AT MOST
#    | TWICE. Return k.
#    | [1,1,1,2,2,3] -> 5, nums[0:5] == [1,1,2,2,3]
#    | Hint: the keep-test becomes "k < 2 or nums[k-2] != current".
#    | Work out WHY looking two back is the right question before you
#    | write it -- that reasoning is the whole answer.
def remove_duplicates_at_most_twice(nums):
    pass


# ======================================================================
#  TESTS -- do not edit
# ======================================================================

_K = inplace_k_ordered      # order must be preserved
_M = inplace_k              # order may change; compare as a multiset

# For solve(): order IS preserved, so we pin the exact surviving order.
_SOLVE_CASES = [
    ("[3,2,2,3] val 3", lambda f: _K(f, [3, 2, 2, 3], 3), (2, [2, 2])),
    ("[0,1,2,2,3,0,4,2] val 2",
     lambda f: _K(f, [0, 1, 2, 2, 3, 0, 4, 2], 2), (5, [0, 1, 3, 0, 4])),
    ("empty", lambda f: _K(f, [], 1), (0, [])),
    ("all match", lambda f: _K(f, [7, 7, 7], 7), (0, [])),
    ("none match", lambda f: _K(f, [1, 2, 3], 9), (3, [1, 2, 3])),
]

# For the swap-from-end version: only the multiset of survivors is defined.
_SWAP_CASES = [
    ("[3,2,2,3] val 3", lambda f: _M(f, [3, 2, 2, 3], 3), (2, [2, 2])),
    ("[0,1,2,2,3,0,4,2] val 2",
     lambda f: _M(f, [0, 1, 2, 2, 3, 0, 4, 2], 2), (5, [0, 0, 1, 3, 4])),
    ("empty", lambda f: _M(f, [], 1), (0, [])),
    ("all match", lambda f: _M(f, [7, 7, 7], 7), (0, [])),
    ("none match", lambda f: _M(f, [1, 2, 3], 9), (3, [1, 2, 3])),
    ("val at the very end", lambda f: _M(f, [1, 2, 3, 9], 9), (3, [1, 2, 3])),
    ("two vals adjacent at end", lambda f: _M(f, [1, 9, 9], 9), (1, [1])),
]

_DEDUPE_CASES = [
    ("[1,1,2]", lambda f: _K(f, [1, 1, 2]), (2, [1, 2])),
    ("[0,0,1,1,1,2,2,3,3,4]",
     lambda f: _K(f, [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]), (5, [0, 1, 2, 3, 4])),
    ("empty", lambda f: _K(f, []), (0, [])),
    ("single", lambda f: _K(f, [5]), (1, [5])),
    ("all same", lambda f: _K(f, [2, 2, 2, 2]), (1, [2])),
    ("negatives", lambda f: _K(f, [-3, -3, -1, 0, 0]), (3, [-3, -1, 0])),
]


def _keep_if_cases():
    even = lambda x: x % 2 == 0
    pos = lambda x: x > 0
    return [
        ("evens of 1..6", lambda f: _K(f, [1, 2, 3, 4, 5, 6], even), (3, [2, 4, 6])),
        ("positives", lambda f: _K(f, [-1, 3, -2, 4], pos), (2, [3, 4])),
        ("order preserved", lambda f: _K(f, [4, 1, 2, 3, 6], even), (3, [4, 2, 6])),
        ("none kept", lambda f: _K(f, [1, 3, 5], even), (0, [])),
        ("all kept", lambda f: _K(f, [2, 4], even), (2, [2, 4])),
        ("empty", lambda f: _K(f, [], even), (0, [])),
    ]


_TWICE_CASES = [
    ("[1,1,1,2,2,3]", lambda f: _K(f, [1, 1, 1, 2, 2, 3]), (5, [1, 1, 2, 2, 3])),
    ("[0,0,1,1,1,1,2,3,3]",
     lambda f: _K(f, [0, 0, 1, 1, 1, 1, 2, 3, 3]), (7, [0, 0, 1, 1, 2, 3, 3])),
    ("empty", lambda f: _K(f, []), (0, [])),
    ("single", lambda f: _K(f, [1]), (1, [1])),
    ("[1,1]", lambda f: _K(f, [1, 1]), (2, [1, 1])),
    ("all same x5", lambda f: _K(f, [9, 9, 9, 9, 9]), (2, [9, 9])),
]


def main():
    mode = argmode(sys.argv)

    if mode == "teach":
        head("LC 27 -- Remove Element :: THE LESSON")
        print(LESSON)
        return
    if mode == "trace":
        head("LC 27 -- Remove Element :: DRY RUN")
        trace([3, 2, 2, 3], 3)
        trace([0, 1, 2, 2, 3, 0, 4, 2], 2)
        return
    if mode in ("quiz", "answers"):
        head("LC 27 -- Remove Element :: EXAMINER")
        quiz(EXAMINER, show=(mode == "answers"))
        return

    head("LC 27 -- Remove Element")

    sub("reference solutions")
    check("solve", solve, _SOLVE_CASES)
    check("solve_swap_from_end", solve_swap_from_end, _SWAP_CASES)

    sub("your variants")
    results = [
        check("V1 remove_element_swap_end", remove_element_swap_end, _SWAP_CASES),
        check("V2 remove_duplicates_sorted", remove_duplicates_sorted, _DEDUPE_CASES),
        check("V3 keep_if", keep_if, _keep_if_cases()),
        check("V4 remove_duplicates_at_most_twice",
              remove_duplicates_at_most_twice, _TWICE_CASES),
    ]
    report(results)


if __name__ == "__main__":
    main()
