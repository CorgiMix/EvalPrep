"""
======================================================================
  PRACTICE -- all ten problems, NO SOLUTIONS, NO HINTS
======================================================================

  Statements and constraints only. Nothing in this file tells you how
  to solve anything -- that is the point. Fill in each `pass`, then:

      python leetcode/practice.py           mark everything
      python leetcode/practice.py 5         mark only problem 5
      python leetcode/practice.py --list     see the running order

  Order is by PATTERN, not by LeetCode number, because each problem
  reuses the idea from the one before.

  Before you write any code, say these four things OUT LOUD:
      1. What pattern is this?
      2. What is the INVARIANT -- what is true on every iteration?
      3. Time and space complexity?
      4. What are the edge cases?

  If you want the taught version of a problem, it lives in its own
  file -- but go there only AFTER you have attempted it here.

  Tests are at the bottom. Do not read them before you attempt, and
  do not edit them.
======================================================================
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _harness import (head, sub, check, report, is_stub,
                      inplace, inplace_k_ordered)


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build(values):
    node = None
    for v in reversed(values):
        node = ListNode(v, node)
    return node


def unroll(node, limit=200):
    out = []
    while node is not None and len(out) < limit:
        out.append(node.val)
        node = node.next
    return out


# ====================================================================
#  1  |  LeetCode 344 -- Reverse String
#     |
#     |  Write a function that reverses a string. The input string is
#     |  given as an array of characters s.
#     |
#     |  You must do this by modifying the input array in-place with
#     |  O(1) extra memory. Return nothing.
#     |
#     |    ["h","e","l","l","o"]     -> ["o","l","l","e","h"]
#     |    ["H","a","n","n","a","h"] -> ["h","a","n","n","a","H"]
#     |
#     |  1 <= s.length <= 10^5 ; s[i] is a printable ascii character.
# ====================================================================
def reverseString(s):
    i, j = 0, len(s)-1
    while i<j:
        s[i], s[j] = s[j], s[i]
        i += 1
        j -= 1


# ====================================================================
#  2  |  LeetCode 125 -- Valid Palindrome
#     |
#     |  A phrase is a palindrome if, after converting all uppercase
#     |  letters into lowercase and removing all non-alphanumeric
#     |  characters, it reads the same forward and backward.
#     |  Return True or False.
#     |
#     |    "A man, a plan, a canal: Panama" -> True
#     |    "race a car"                     -> False
#     |    " "                              -> True
#     |
#     |  1 <= s.length <= 2*10^5, printable ASCII.
#     |  Required: O(1) extra space -- do not build a cleaned copy.
# ====================================================================
def isPalindrome(s):
    pass


# ====================================================================
#  3  |  LeetCode 27 -- Remove Element
#     |
#     |  Given an integer array nums and an integer val, remove all
#     |  occurrences of val in nums IN-PLACE. Return the number k of
#     |  elements that are not equal to val.
#     |
#     |  The first k elements of nums must hold the survivors. Anything
#     |  past index k is ignored, as is the size of nums.
#     |
#     |    ([3,2,2,3], 3)           -> 2, nums starts [2,2]
#     |    ([0,1,2,2,3,0,4,2], 2)   -> 5, nums starts [0,1,3,0,4]
#     |
#     |  0 <= nums.length <= 100 ; 0 <= nums[i] <= 50 ; 0 <= val <= 100
#     |  (Keep the survivors in their original order.)
# ====================================================================
def removeElement(nums, val):
    pass


# ====================================================================
#  4  |  LeetCode 283 -- Move Zeroes
#     |
#     |  Move all 0's to the end of nums while maintaining the relative
#     |  order of the non-zero elements. In-place, no copy of the array.
#     |  Return nothing.
#     |
#     |    [0,1,0,3,12] -> [1,3,12,0,0]
#     |    [0]          -> [0]
#     |
#     |  1 <= nums.length <= 10^4 ; -2^31 <= nums[i] <= 2^31 - 1
# ====================================================================
def moveZeroes(nums):
    pass


# ====================================================================
#  5  |  LeetCode 1 -- Two Sum
#     |
#     |  Given an array of integers nums and an integer target, return
#     |  the INDICES of the two numbers that add up to target.
#     |
#     |  Exactly one solution exists. You may not use the same element
#     |  twice. Return the answer in any order.
#     |
#     |    ([2,7,11,15], 9) -> [0,1]
#     |    ([3,2,4], 6)     -> [1,2]
#     |    ([3,3], 6)       -> [0,1]
#     |
#     |  2 <= nums.length <= 10^4 ; -10^9 <= nums[i], target <= 10^9
#     |  Follow up: can you do better than O(n^2)?
# ====================================================================
def twoSum(nums, target):
    pass


# ====================================================================
#  6  |  LeetCode 217 -- Contains Duplicate
#     |
#     |  Return True if any value appears at least twice in nums, and
#     |  False if every element is distinct.
#     |
#     |    [1,2,3,1] -> True
#     |    [1,2,3,4] -> False
#     |
#     |  1 <= nums.length <= 10^5 ; -10^9 <= nums[i] <= 10^9
# ====================================================================
def containsDuplicate(nums):
    pass


# ====================================================================
#  7  |  LeetCode 121 -- Best Time to Buy and Sell Stock
#     |
#     |  prices[i] is the price of a stock on day i. Choose ONE day to
#     |  buy and a DIFFERENT, LATER day to sell. Return the maximum
#     |  profit, or 0 if no profit is possible.
#     |
#     |    [7,1,5,3,6,4] -> 5   (buy at 1 on day 1, sell at 6 on day 4)
#     |    [7,6,4,3,1]   -> 0
#     |
#     |  1 <= prices.length <= 10^5 ; 0 <= prices[i] <= 10^4
#     |  Required: O(n) time, O(1) space, single pass.
# ====================================================================
def maxProfit(prices):
    pass


# ====================================================================
#  8  |  LeetCode 268 -- Missing Number
#     |
#     |  nums contains n DISTINCT numbers drawn from the range [0, n].
#     |  Return the one number in that range that is missing.
#     |
#     |    [3,0,1]             -> 2
#     |    [0,1]               -> 2
#     |    [9,6,4,2,3,5,7,0,1] -> 8
#     |
#     |  n == nums.length ; 1 <= n <= 10^4 ; 0 <= nums[i] <= n
#     |  Follow up: O(1) extra space and O(n) time.
#     |  (Read the range twice. It is [0, n], not [0, n-1].)
# ====================================================================
def missingNumber(nums):
    pass


# ====================================================================
#  9  |  LeetCode 21 -- Merge Two Sorted Lists
#     |
#     |  Given the heads of two sorted linked lists, merge them into one
#     |  sorted list by SPLICING TOGETHER THE EXISTING NODES. Return the
#     |  head of the merged list.
#     |
#     |    [1,2,4] + [1,3,4] -> [1,1,2,3,4,4]
#     |    []      + []      -> []
#     |    []      + [0]     -> [0]
#     |
#     |  0 to 50 nodes each ; -100 <= Node.val <= 100 ; both sorted.
#     |  A ListNode class is defined at the top of this file.
# ====================================================================
def mergeTwoLists(list1, list2):
    pass


# ====================================================================
# 10  |  LeetCode 28 -- First Occurrence in a String
#     |
#     |  Return the index of the first occurrence of needle in
#     |  haystack, or -1 if needle is not part of haystack.
#     |
#     |    ("sadbutsad", "sad") -> 0    (not 6 -- the FIRST one)
#     |    ("leetcode", "leeto") -> -1
#     |
#     |  1 <= haystack.length, needle.length <= 10^4
#     |  Lowercase English letters only.
#     |  (Do not use str.find or the `in` operator -- implement it.)
# ====================================================================
def strStr(haystack, needle):
    pass


# ====================================================================
#  TESTS -- do not read before attempting, do not edit
# ====================================================================

_K = inplace_k_ordered

PROBLEMS = [
    ("1  LC 344  reverseString", lambda: reverseString, [
        ("hello", lambda f: "".join(inplace(f, list("hello"))), "olleh"),
        ("Hannah", lambda f: "".join(inplace(f, list("Hannah"))), "hannaH"),
        ("single", lambda f: "".join(inplace(f, list("x"))), "x"),
        ("empty", lambda f: "".join(inplace(f, [])), ""),
        ("two", lambda f: "".join(inplace(f, list("ab"))), "ba"),
        ("returns None", lambda f: f(list("ab")), None),
    ]),
    ("2  LC 125  isPalindrome", lambda: isPalindrome, [
        ("Panama", lambda f: f("A man, a plan, a canal: Panama"), True),
        ("race a car", lambda f: f("race a car"), False),
        ("one space", lambda f: f(" "), True),
        ("all punctuation", lambda f: f(",,,"), True),
        ("0P", lambda f: f("0P"), False),
        ("a,", lambda f: f("a,"), True),
        ("ab", lambda f: f("ab"), False),
        ("a,, a", lambda f: f("a,, a"), True),
    ]),
    ("3  LC 27   removeElement", lambda: removeElement, [
        ("[3,2,2,3] val 3", lambda f: _K(f, [3, 2, 2, 3], 3), (2, [2, 2])),
        ("[0,1,2,2,3,0,4,2] val 2",
         lambda f: _K(f, [0, 1, 2, 2, 3, 0, 4, 2], 2), (5, [0, 1, 3, 0, 4])),
        ("empty", lambda f: _K(f, [], 1), (0, [])),
        ("all match", lambda f: _K(f, [7, 7, 7], 7), (0, [])),
        ("none match", lambda f: _K(f, [1, 2, 3], 9), (3, [1, 2, 3])),
    ]),
    ("4  LC 283  moveZeroes", lambda: moveZeroes, [
        ("[0,1,0,3,12]", lambda f: inplace(f, [0, 1, 0, 3, 12]), [1, 3, 12, 0, 0]),
        ("[0]", lambda f: inplace(f, [0]), [0]),
        ("no zeroes", lambda f: inplace(f, [1, 2, 3]), [1, 2, 3]),
        ("all zeroes", lambda f: inplace(f, [0, 0, 0]), [0, 0, 0]),
        ("leading run", lambda f: inplace(f, [0, 0, 1]), [1, 0, 0]),
        ("order kept", lambda f: inplace(f, [0, -1, 0, -2, 5]), [-1, -2, 5, 0, 0]),
        ("returns None", lambda f: f([0, 1]), None),
    ]),
    ("5  LC 1    twoSum", lambda: twoSum, [
        ("[2,7,11,15] t9", lambda f: f([2, 7, 11, 15], 9), [0, 1]),
        ("[3,2,4] t6", lambda f: f([3, 2, 4], 6), [1, 2]),
        ("[3,3] t6", lambda f: f([3, 3], 6), [0, 1]),
        ("negatives", lambda f: f([-3, 4, 3, 90], 0), [0, 2]),
        ("negative target", lambda f: f([5, -2, -4], -6), [1, 2]),
        ("last pair", lambda f: f([1, 5, 2, 8], 10), [2, 3]),
    ]),
    ("6  LC 217  containsDuplicate", lambda: containsDuplicate, [
        ("[1,2,3,1]", lambda f: f([1, 2, 3, 1]), True),
        ("[1,2,3,4]", lambda f: f([1, 2, 3, 4]), False),
        ("long mixed", lambda f: f([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]), True),
        ("single", lambda f: f([7]), False),
        ("adjacent pair", lambda f: f([5, 5]), True),
        ("negatives", lambda f: f([-1, -2, -1]), True),
    ]),
    ("7  LC 121  maxProfit", lambda: maxProfit, [
        ("[7,1,5,3,6,4]", lambda f: f([7, 1, 5, 3, 6, 4]), 5),
        ("[7,6,4,3,1]", lambda f: f([7, 6, 4, 3, 1]), 0),
        ("rising", lambda f: f([1, 2, 3, 4, 5]), 4),
        ("single", lambda f: f([5]), 0),
        ("all equal", lambda f: f([3, 3, 3]), 0),
        ("min after max", lambda f: f([7, 1]), 0),
        ("late peak", lambda f: f([9, 8, 1, 2, 100]), 99),
    ]),
    ("8  LC 268  missingNumber", lambda: missingNumber, [
        ("[3,0,1]", lambda f: f([3, 0, 1]), 2),
        ("[0,1]", lambda f: f([0, 1]), 2),
        ("[9,6,4,2,3,5,7,0,1]", lambda f: f([9, 6, 4, 2, 3, 5, 7, 0, 1]), 8),
        ("[0]", lambda f: f([0]), 1),
        ("[1]", lambda f: f([1]), 0),
        ("missing 0", lambda f: f([1, 2, 3]), 0),
        ("missing last", lambda f: f([0, 1, 2]), 3),
        ("returns an int", lambda f: isinstance(f([0, 1]), int), True),
    ]),
    ("9  LC 21   mergeTwoLists", lambda: mergeTwoLists, [
        ("[1,2,4]+[1,3,4]",
         lambda f: unroll(f(build([1, 2, 4]), build([1, 3, 4]))), [1, 1, 2, 3, 4, 4]),
        ("[]+[]", lambda f: unroll(f(build([]), build([]))), []),
        ("[]+[0]", lambda f: unroll(f(build([]), build([0]))), [0]),
        ("[0]+[]", lambda f: unroll(f(build([0]), build([]))), [0]),
        ("disjoint", lambda f: unroll(f(build([8, 9]), build([1, 2]))), [1, 2, 8, 9]),
        ("all ties", lambda f: unroll(f(build([1, 1]), build([1, 1]))), [1, 1, 1, 1]),
        ("uneven", lambda f: unroll(f(build([1]), build([2, 3, 4, 5]))), [1, 2, 3, 4, 5]),
    ]),
    ("10 LC 28   strStr", lambda: strStr, [
        ("sadbutsad/sad", lambda f: f("sadbutsad", "sad"), 0),
        ("leetcode/leeto", lambda f: f("leetcode", "leeto"), -1),
        ("needle longer", lambda f: f("ab", "abcdef"), -1),
        ("identical", lambda f: f("abc", "abc"), 0),
        ("at the end", lambda f: f("abc", "c"), 2),
        ("worst case", lambda f: f("aaaaaaaaab", "aaab"), 6),
        ("mississippi/issip", lambda f: f("mississippi", "issip"), 4),
    ]),
]

ORDER = """
  A  two pointers converging      1 (344)   2 (125)
  B  read / write pointer         3 (27)    4 (283)
  C  hash map / set               5 (1)     6 (217)
  D  one pass, running state      7 (121)   8 (268)
  E  pointers and windows         9 (21)   10 (28)

  Each pair shares a pattern. Solve 3 before 4 and the second one
  takes a minute -- they are the same loop with one line different.
"""


def main():
    if "--list" in sys.argv:
        head("PRACTICE :: RUNNING ORDER")
        print(ORDER)
        return

    only = None
    for a in sys.argv[1:]:
        if a.isdigit():
            only = int(a)

    head("PRACTICE :: ALL TEN" if only is None else "PRACTICE :: PROBLEM %d" % only)
    results = []
    for i, (label, getter, cases) in enumerate(PROBLEMS, 1):
        if only is not None and i != only:
            continue
        results.append(check(label, getter(), cases))
    if not results:
        print("  no such problem -- pick 1 to 10")
        return
    report(results)
    if only is None:
        print()
        print("  one problem at a time:  python leetcode/practice.py 3")
        print("  the running order:      python leetcode/practice.py --list")
        print()


if __name__ == "__main__":
    main()
