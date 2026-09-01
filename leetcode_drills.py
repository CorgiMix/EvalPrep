"""
LEETCODE DRILLS  --  all ten, ordered by pattern, not by number
================================================================

HOW TO USE
    1. Run it:   .venv\\Scripts\\python.exe leetcode_drills.py
    2. Solve them IN ORDER. They are grouped so each one reuses the
       idea from the one before -- P3 and P4 are the same loop, P1 and
       P2 are the same two pointers. Solving by number wastes that.
    3. Replace each `pass`, re-run, repeat until 10/10.

BEFORE YOU WRITE ANY CODE, SAY THESE FOUR THINGS OUT LOUD
    1. What pattern is this?
    2. What is the INVARIANT -- what is true on every iteration?
    3. What is the time and space complexity?
    4. What are the edge cases?

    If you cannot say the invariant, you do not understand the problem
    yet, and the code you are about to write is recalled rather than
    derived. That distinction is exactly what the live session tests.

AFTER IT PASSES
    Dry run it out loud on the example, naming every variable at every
    step. That is a graded duty of the logic role, and it is the part
    everyone skips.

    Stuck?  python leetcode_drills.py --hint 3
    Order?  python leetcode_drills.py --plan

Tests live at the bottom -- do not edit them.
"""

import sys


# ====================================================================
#  PATTERN A -- TWO POINTERS CONVERGING FROM THE ENDS
#  One at each end, walking inward. Always `while i < j`, never <=.
# ====================================================================

# P1  |  LeetCode 344 -- Reverse String
#     |  Reverse the list of characters IN PLACE. Return nothing.
#     |  Required: O(1) extra space.
#     |  (s = s[::-1] does NOT work here. Know why before you start.)
def reverseString(s):
    pass


# P2  |  LeetCode 125 -- Valid Palindrome
#     |  Ignoring case and every non-alphanumeric character, is s a
#     |  palindrome? Return True/False.
#     |  Required: O(1) extra space -- do not build a cleaned copy.
#     |  Watch: a string of pure punctuation must not crash you.
def isPalindrome(s):
    pass


# ====================================================================
#  PATTERN B -- READ / WRITE POINTER (both move forward)
#  `i` reads everything; `k` marks where the next keeper is written.
#  k never overtakes i, which is why in-place is safe.
#  P3 and P4 are the SAME LOOP with one line different. Find it.
# ====================================================================

# P3  |  LeetCode 27 -- Remove Element
#     |  Remove every occurrence of val IN PLACE. Return the count k of
#     |  remaining elements. Anything past index k is ignored.
def removeElement(nums, val):
    pass


# P4  |  LeetCode 283 -- Move Zeroes
#     |  Move all zeroes to the end IN PLACE, keeping the relative
#     |  order of the non-zero elements. Return nothing.
def moveZeroes(nums):
    pass


# ====================================================================
#  PATTERN C -- HASH MAP / SET
#  Trade O(n) memory for O(1) membership, collapsing a nested loop
#  into a single pass.
# ====================================================================

# P5  |  LeetCode 1 -- Two Sum
#     |  Return the indices of the two numbers adding to target.
#     |  Exactly one solution; you may not reuse the same element.
#     |  Required: O(n). The order of your check and your insert
#     |  decides whether [3,2,4] target 6 returns the wrong answer.
def twoSum(nums, target):
    pass


# P6  |  LeetCode 217 -- Contains Duplicate
#     |  True if any value appears at least twice.
#     |  Write the EARLY-EXIT version, not the one-line set trick --
#     |  then be ready to say why you preferred it.
def containsDuplicate(nums):
    pass


# ====================================================================
#  PATTERN D -- ONE PASS, RUNNING STATE
#  Carry a little state through a single sweep. O(1) memory.
# ====================================================================

# P7  |  LeetCode 121 -- Best Time to Buy and Sell Stock
#     |  One buy, one later sell. Max profit, or 0 if none possible.
#     |  Required: O(n) time, O(1) space, single pass.
def maxProfit(prices):
    pass


# P8  |  LeetCode 268 -- Missing Number
#     |  nums holds n distinct values from the range 0..n. Find the
#     |  absent one. Required: O(1) space.
#     |  Use the Gauss sum. Careful: // not /, or you return a float.
def missingNumber(nums):
    pass


# P9  |  Same problem, XOR instead. This is the likely follow-up.
#     |  Works because a ^ a == 0 and a ^ 0 == a.
def missingNumberXor(nums):
    pass


# ====================================================================
#  PATTERN E -- POINTERS ON A LINKED LIST, AND A SLIDING WINDOW
# ====================================================================

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# P10 |  LeetCode 21 -- Merge Two Sorted Lists
#     |  Splice two sorted lists into one sorted list, REUSING the
#     |  existing nodes. Return the head.
#     |  Use a dummy head -- and know what it saves you from.
def mergeTwoLists(list1, list2):
    pass


# P11 |  LeetCode 28 -- First Occurrence in a String
#     |  Return the first index where needle starts in haystack, else
#     |  -1. Do not use .find() or .index().
#     |  The whole problem is the upper bound of your range. Empty
#     |  needle must return 0; a needle longer than the haystack, -1.
def strStr(haystack, needle):
    pass


# ====================================================================
#  TESTS -- do not edit below this line
# ====================================================================

HINTS = {
    1: "i, j = 0, len(s)-1. Swap, then i += 1 and j -= 1. Python swaps "
       "with s[i], s[j] = s[j], s[i] -- no temp variable needed, because "
       "the right side is built as a tuple first.",
    2: "Outer `while i < j`. Inside it, two inner whiles that skip "
       "non-alphanumeric characters -- and BOTH need `i < j` in their "
       "own condition or ',,,' walks off the end. Compare .lower().",
    3: "k = 0. Loop i over every index. If nums[i] != val, write it to "
       "nums[k] and increment k. Return k.",
    4: "Identical to P3 with val=0, except you SWAP instead of "
       "overwriting -- nums[k], nums[i] = nums[i], nums[k]. Swapping "
       "sends the zero to the back instead of discarding it.",
    5: "Dict of value -> index. For each element compute the "
       "complement, CHECK it is in the dict, and only THEN insert the "
       "current value. Insert first and element 0 pairs with itself.",
    6: "A set, and return True the moment you see a repeat. Say out "
       "loud why a set beats a list here: membership is O(1), not O(n).",
    7: "Track the cheapest price seen so far. At each price, the best "
       "profit if you sold today is price - cheapest. Keep the max. "
       "Update cheapest FIRST.",
    8: "The numbers 0..n sum to n*(n+1)//2. Subtract the actual sum. "
       "Use // so you return an int, not a float.",
    9: "Start with out = len(nums), then XOR in every index AND every "
       "value. Everything present in both cancels to 0.",
    10: "dummy = ListNode(); tail = dummy. While BOTH lists are "
        "non-empty, attach the smaller node and advance that list. "
        "After the loop, tail.next = list1 or list2 attaches the whole "
        "remainder in one line. Return dummy.next, not dummy.",
    11: "for i in range(len(haystack) - len(needle) + 1). That bound "
        "gives you the empty-needle and too-long-needle cases for "
        "free. Compare haystack[i:i+m] == needle.",
}

PLAN = """
  Solve in this order -- each group reuses the previous idea:

    A  converging pointers   P1 Reverse String      -> P2 Valid Palindrome
    B  read/write pointer    P3 Remove Element      -> P4 Move Zeroes
    C  hash map / set        P5 Two Sum             -> P6 Contains Duplicate
    D  running state         P7 Buy and Sell Stock  -> P8/P9 Missing Number
    E  the remaining two     P10 Merge Lists        -> P11 strStr

  P3 and P4 are the same loop with one line changed. If you solve P4
  without noticing that, go back and look again -- saying it out loud
  in the session is worth more than solving either one alone.
"""


def _is_stub(fn):
    """True while the function body is still just `pass`."""
    import inspect
    try:
        src = inspect.getsource(fn)
    except Exception:
        return False
    lines = [ln.strip() for ln in src.splitlines()]
    lines = [ln for ln in lines if ln and not ln.startswith("#")]
    return [ln for ln in lines if not ln.startswith("def ")] == ["pass"]


def _build(vals):
    head = None
    for x in reversed(vals):
        head = ListNode(x, head)
    return head


def _unroll(h):
    out = []
    while h:
        out.append(h.val)
        h = h.next
    return out


def _cases():
    C = []

    def rev(x):
        s = list(x)
        reverseString(s)
        return "".join(s)
    C.append((1, "Reverse String", reverseString, [
        ("hello", lambda: rev("hello"), "olleh"),
        ("ab (even)", lambda: rev("ab"), "ba"),
        ("a (single)", lambda: rev("a"), "a"),
        ("empty", lambda: rev(""), ""),
    ]))

    C.append((2, "Valid Palindrome", isPalindrome, [
        ("classic", lambda: isPalindrome("A man, a plan, a canal: Panama"), True),
        ("race a car", lambda: isPalindrome("race a car"), False),
        ("single space", lambda: isPalindrome(" "), True),
        ("',,,' all punctuation", lambda: isPalindrome(",,,"), True),
        ("'.,' all punctuation", lambda: isPalindrome(".,"), True),
        ("empty", lambda: isPalindrome(""), True),
        ("0P (case trap)", lambda: isPalindrome("0P"), False),
    ]))

    def rm(v, val):
        n = list(v)
        k = removeElement(n, val)
        return (k, sorted(n[:k]) if k else [])
    C.append((3, "Remove Element", removeElement, [
        ("[3,2,2,3] val 3", lambda: rm([3, 2, 2, 3], 3), (2, [2, 2])),
        ("all removed", lambda: rm([2, 2, 2], 2), (0, [])),
        ("none removed", lambda: rm([1, 2, 3], 9), (3, [1, 2, 3])),
        ("empty", lambda: rm([], 1), (0, [])),
    ]))

    def mz(v):
        n = list(v)
        moveZeroes(n)
        return n
    C.append((4, "Move Zeroes", moveZeroes, [
        ("[0,1,0,3,12]", lambda: mz([0, 1, 0, 3, 12]), [1, 3, 12, 0, 0]),
        ("all zero", lambda: mz([0, 0, 0]), [0, 0, 0]),
        ("no zero", lambda: mz([1, 2, 3]), [1, 2, 3]),
        ("order preserved", lambda: mz([0, 5, 0, 4, 0, 3]), [5, 4, 3, 0, 0, 0]),
        ("empty", lambda: mz([]), []),
    ]))

    C.append((5, "Two Sum", twoSum, [
        ("[2,7,11,15] t9", lambda: twoSum([2, 7, 11, 15], 9), [0, 1]),
        ("duplicates [3,3] t6", lambda: twoSum([3, 3], 6), [0, 1]),
        ("[3,2,4] t6 no self-pair", lambda: twoSum([3, 2, 4], 6), [1, 2]),
        ("negatives [-1,-2,-3] t-5", lambda: twoSum([-1, -2, -3], -5), [1, 2]),
    ]))

    C.append((6, "Contains Duplicate", containsDuplicate, [
        ("[1,2,3,1]", lambda: containsDuplicate([1, 2, 3, 1]), True),
        ("[1,2,3,4]", lambda: containsDuplicate([1, 2, 3, 4]), False),
        ("empty", lambda: containsDuplicate([]), False),
        ("single", lambda: containsDuplicate([1]), False),
    ]))

    C.append((7, "Buy and Sell Stock", maxProfit, [
        ("[7,1,5,3,6,4]", lambda: maxProfit([7, 1, 5, 3, 6, 4]), 5),
        ("falling market", lambda: maxProfit([7, 6, 4, 3, 1]), 0),
        ("single day", lambda: maxProfit([5]), 0),
        ("empty", lambda: maxProfit([]), 0),
        ("rise at the very end", lambda: maxProfit([2, 2, 2, 9]), 7),
    ]))

    C.append((8, "Missing Number (Gauss)", missingNumber, [
        ("[3,0,1]", lambda: missingNumber([3, 0, 1]), 2),
        ("[0] -> 1", lambda: missingNumber([0]), 1),
        ("[1] -> 0", lambda: missingNumber([1]), 0),
        ("[9,6,4,2,3,5,7,0,1]", lambda: missingNumber([9, 6, 4, 2, 3, 5, 7, 0, 1]), 8),
        ("returns int not float",
         lambda: isinstance(missingNumber([3, 0, 1]), int), True),
    ]))

    C.append((9, "Missing Number (XOR)", missingNumberXor, [
        ("[3,0,1]", lambda: missingNumberXor([3, 0, 1]), 2),
        ("[9,6,4,2,3,5,7,0,1]",
         lambda: missingNumberXor([9, 6, 4, 2, 3, 5, 7, 0, 1]), 8),
        ("[0] -> 1", lambda: missingNumberXor([0]), 1),
    ]))

    C.append((10, "Merge Two Sorted Lists", mergeTwoLists, [
        ("[1,2,4]+[1,3,4]",
         lambda: _unroll(mergeTwoLists(_build([1, 2, 4]), _build([1, 3, 4]))),
         [1, 1, 2, 3, 4, 4]),
        ("both empty", lambda: _unroll(mergeTwoLists(None, None)), []),
        ("one empty", lambda: _unroll(mergeTwoLists(None, _build([0]))), [0]),
        ("uneven lengths",
         lambda: _unroll(mergeTwoLists(_build([1]), _build([2, 3, 4, 5]))),
         [1, 2, 3, 4, 5]),
    ]))

    C.append((11, "strStr", strStr, [
        ("sadbutsad / sad", lambda: strStr("sadbutsad", "sad"), 0),
        ("leetcode / leeto", lambda: strStr("leetcode", "leeto"), -1),
        ("EMPTY needle -> 0", lambda: strStr("abc", ""), 0),
        ("needle LONGER -> -1", lambda: strStr("a", "abc"), -1),
        ("match at the end", lambda: strStr("mississippi", "pi"), 9),
        ("overlap trap", lambda: strStr("aaaaab", "aaab"), 2),
    ]))
    return C


def main():
    if "--hint" in sys.argv:
        n = int(sys.argv[sys.argv.index("--hint") + 1])
        print("\nHINT P%d: %s\n" % (n, HINTS.get(n, "no hint for that one")))
        return
    if "--plan" in sys.argv:
        print(PLAN)
        return

    groups = {1: "A -- converging pointers", 3: "B -- read/write pointer",
              5: "C -- hash map / set", 7: "D -- running state",
              10: "E -- linked list & sliding window"}

    print("\n" + "=" * 72)
    print("  LEETCODE DRILLS".ljust(58) + "11 solutions")
    print("=" * 72)

    done = todo = broke = 0
    for num, title, fn, cases in _cases():
        if num in groups:
            print("\n  -- PATTERN %s %s" % (groups[num],
                                            "-" * max(0, 50 - len(groups[num]))))
        results = []
        for label, run, want in cases:
            try:
                got = run()
            except Exception as e:
                results.append((label, "ERR", "%s: %s" % (type(e).__name__, e)))
                continue
            results.append((label, "ok" if got == want else "no",
                            "got %r want %r" % (got, want)))

        errs = [r for r in results if r[1] == "ERR"]
        bad = [r for r in results if r[1] == "no"]

        if _is_stub(fn):
            todo += 1
            print("  [ ]   P%-2d %-26s not attempted" % (num, title))
        elif not errs and not bad:
            done += 1
            print("  [ok]  P%-2d %-26s %d/%d cases pass"
                  % (num, title, len(results), len(results)))
        else:
            broke += 1
            first = (errs + bad)[0]
            print("  [X]   P%-2d %-26s %s  <-- %s"
                  % (num, title, first[0], first[2]))
            for label, st, detail in (errs + bad)[1:3]:
                print("        %-32s %s  <-- %s" % ("", label, detail))

    total = 11
    print("\n" + "-" * 72)
    print("  %d/%d solved   |   %d failing, %d not attempted"
          % (done, total, broke, todo))
    if done == total:
        print("  All ten patterns clear. Now redo each one from a blank file,")
        print("  saying the invariant out loud before you type anything.")
    else:
        print("  Order: python leetcode_drills.py --plan")
        print("  Hints: python leetcode_drills.py --hint 1")
    print("-" * 72 + "\n")


if __name__ == "__main__":
    main()
