"""
======================================================================
  LeetCode 344 -- Reverse String
  Notebook concepts: Two Pointers, In-place Modification
======================================================================

THE PROBLEM (as stated on LeetCode)

    Write a function that reverses a string. The input string is given
    as an array of characters s.

    You must do this by modifying the input array in-place with O(1)
    extra memory.

    Example 1:
        Input:  s = ["h","e","l","l","o"]
        Output: ["o","l","l","e","h"]

    Example 2:
        Input:  s = ["H","a","n","n","a","h"]
        Output: ["h","a","n","n","a","H"]

    Constraints:
        1 <= s.length <= 10^5
        s[i] is a printable ascii character.

HOW TO USE THIS FILE
    python leetcode/lc344_reverse_string.py --teach     the full lesson
    python leetcode/lc344_reverse_string.py --trace     live dry run
    python leetcode/lc344_reverse_string.py --quiz      examiner questions
    python leetcode/lc344_reverse_string.py --answers   ... with answers
    python leetcode/lc344_reverse_string.py             run your variants

    Read --teach, then --trace, then say the dry run OUT LOUD from
    memory, then implement the VARIANTS at the bottom of this file.
    The variants are the point: the live session may ask you to change
    the code, not recite it.
======================================================================
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _harness import (head, sub, check, report, quiz, argmode, inplace)


# ======================================================================
#  THE LESSON
# ======================================================================

LESSON = """
STEP 1 -- READ THE SIGNATURE BEFORE THE SENTENCE

  You are handed a LIST of characters, not a string. That is not
  decoration. Python strings are immutable, so "modify in place" is
  impossible on a str. The moment they hand you a list, they have told
  you the intended solution mutates.

  Say this out loud in the session. It shows you read the constraint
  rather than pattern-matched the title.

STEP 2 -- THE THING THAT LOOKS RIGHT AND IS NOT

      def reverseString(s):
          s = s[::-1]          # WRONG, twice over

  Wrong reason 1 (the fatal one): this rebinds the LOCAL name `s` to a
  brand new list. The caller's list is untouched. The function appears
  to work when you print inside it and does nothing at all outside it.

  Wrong reason 2: s[::-1] allocates a second list of length n, so it is
  O(n) extra memory and the constraint explicitly forbids that.

  The slice-assignment version, s[:] = s[::-1], DOES mutate the caller
  and is a legitimate one-liner -- but it still builds the reversed copy
  first, so it is still O(n) space. And s.reverse() is O(1) space and
  entirely correct, but answering with it skips the algorithm they are
  actually testing. Mention both, then write the pointer version.

STEP 3 -- THE INSIGHT

  Reversing means: 1st swaps with last, 2nd swaps with 2nd-last, and so
  on. Each of those swaps is independent of the others. So you do not
  need a copy -- you need one pointer at each end, walking inward.

STEP 4 -- THE INVARIANT   (memorise this sentence)

      Everything OUTSIDE the window [i, j] is already in its final
      position. Every swap shrinks the window by one from each side.

  When the window is empty or a single element, you are done.

STEP 5 -- WHY `while i < j` AND NOT `while i <= j`

  At i == j both pointers name the SAME element. Swapping an element
  with itself is a no-op -- harmless, but it is a wasted iteration and
  it signals you have not thought about the midpoint. On an odd-length
  list that middle character is already where it belongs.

STEP 6 -- COMPLEXITY

  Time  O(n)   -- exactly floor(n/2) swaps.
  Space O(1)   -- two integers, regardless of input size.

  Careful: O(n/2) is not a thing you say. Constants drop. Say "O(n),
  with n/2 swaps" if you want to show the detail.

STEP 7 -- EDGE CASES, AND WHY YOU WRITE NO CODE FOR THEM

  []        -> j = -1, so i < j is 0 < -1, false. Loop never runs.
  ["a"]     -> i = j = 0, false. Loop never runs.
  ["a","b"] -> one swap, then i=1, j=0, stops.

  All three are handled by the loop condition alone. Saying "my
  termination condition already covers the empty and single-element
  cases, so I need no special-casing" is a strong, checkable claim.
"""


# ======================================================================
#  THE SOLUTION
# ======================================================================

def solve(s):
    """Reverse the list of characters s in place. Returns None."""
    i, j = 0, len(s) - 1
    while i < j:
        # Tuple assignment evaluates the whole right side first, so this
        # is a true simultaneous swap -- no temporary variable needed.
        s[i], s[j] = s[j], s[i]
        i += 1
        j -= 1


# ======================================================================
#  THE DRY RUN  (this is a graded duty of the logic role)
# ======================================================================

def trace(chars=None):
    s = list(chars or "hello")
    print()
    print("  input: %r   (n = %d)" % (s, len(s)))
    print()
    print("  %-4s %-4s %-10s %s" % ("i", "j", "swap", "list after"))
    print("  " + "-" * 46)
    i, j = 0, len(s) - 1
    while i < j:
        a, b = s[i], s[j]
        s[i], s[j] = s[j], s[i]
        print("  %-4d %-4d %-10s %s" % (i, j, "%s <-> %s" % (a, b), "".join(s)))
        i += 1
        j -= 1
    print("  %-4d %-4d %-10s %s" % (i, j, "--", "i < j is false, stop"))
    print()
    print("  result: %r" % s)


# ======================================================================
#  WHAT THE EXAMINER ASKS
# ======================================================================

EXAMINER = [
    ("Why did they give you a list of characters instead of a string?",
     """Python strings are immutable, so an in-place reversal of a str is
        impossible. Handing over a list is how the problem makes the
        in-place requirement expressible at all."""),

    ("What is wrong with `s = s[::-1]` inside the function?",
     """It rebinds the local name to a new list; the caller's list never
        changes. It is also O(n) extra space. `s[:] = s[::-1]` fixes the
        mutation bug but not the space bug."""),

    ("Is `s.reverse()` acceptable?",
     """It is correct and O(1) space. But it delegates the algorithm to
        the standard library, and the algorithm is what is being tested.
        Say it exists, then write the two-pointer version."""),

    ("Why `i < j` rather than `i <= j`?",
     """At i == j the pointers name one element and the swap is a no-op.
        On odd-length input the middle character is already correct."""),

    ("How many swaps for n = 7?",
     """3. floor(7/2). Indices (0,6), (1,5), (2,4); index 3 is untouched."""),

    ("Prove it terminates.",
     """i strictly increases and j strictly decreases every iteration, so
        the quantity (j - i) drops by exactly 2 each pass. It is bounded
        below, so the condition i < j must eventually fail."""),

    ("Could you do this recursively, and should you?",
     """Yes -- swap the ends, recurse on the inner slice indices. But
        Python has no tail-call elimination and a default recursion limit
        near 1000, so with n up to 10^5 it would blow the stack. The
        iterative version is the right call, and knowing WHY is the
        answer they want."""),
]


# ======================================================================
#  YOUR TURN -- VARIANTS
#
#  Each of these is a plausible "now change it" from the assessor.
#  Replace `pass` and re-run this file. Do not look at solve() while
#  you write them -- the whole point is deriving, not copying.
# ======================================================================

# V1 | Reverse only the vowels, leaving every other character in place.
#    | This is LeetCode 345. Same two pointers, but each side must
#    | SKIP forward until it lands on a vowel before swapping.
#    | Think: where have you seen a guarded inner skip before?
#    | "hello" -> "holle"      "leetcode" -> "leotcede"
def reverse_vowels(s):
    pass


# V2 | Reverse only the first k characters, leave the rest alone.
#    | If k is larger than the list, reverse everything.
#    | (list("abcdef"), 3) -> ["c","b","a","d","e","f"]
def reverse_first_k(s, k):
    pass


# V3 | Reverse the list in place WITHOUT a second pointer variable --
#    | you may use only `i` and len(s). Prove to yourself it is the
#    | same algorithm wearing a disguise.
#    | Hint: the mirror of index i is len(s) - 1 - i.
def reverse_one_pointer(s):
    pass


# V4 | Rotate the list left by k positions, in place, O(1) space.
#    | The classic trick: reverse the whole thing, then reverse the
#    | two pieces. Work out on paper WHICH pieces before you code.
#    | (list("abcdef"), 2) -> ["c","d","e","f","a","b"]
def rotate_left(s, k):
    pass


# ======================================================================
#  TESTS -- do not edit
# ======================================================================

def _vowel_cases():
    return [
        ("hello", lambda f: "".join(inplace(f, list("hello"))), "holle"),
        ("leetcode", lambda f: "".join(inplace(f, list("leetcode"))), "leotcede"),
        ("aA", lambda f: "".join(inplace(f, list("aA"))), "Aa"),
        ("bcdfg", lambda f: "".join(inplace(f, list("bcdfg"))), "bcdfg"),
        ("empty", lambda f: "".join(inplace(f, [])), ""),
        (".,!", lambda f: "".join(inplace(f, list(".,!"))), ".,!"),
    ]


def _first_k_cases():
    return [
        ("abcdef k=3", lambda f: "".join(inplace(f, list("abcdef"), 3)), "cbadef"),
        ("abcdef k=0", lambda f: "".join(inplace(f, list("abcdef"), 0)), "abcdef"),
        ("abcdef k=99", lambda f: "".join(inplace(f, list("abcdef"), 99)), "fedcba"),
        ("ab k=1", lambda f: "".join(inplace(f, list("ab"), 1)), "ab"),
    ]


def _one_pointer_cases():
    return [
        ("hello", lambda f: "".join(inplace(f, list("hello"))), "olleh"),
        ("Hannah", lambda f: "".join(inplace(f, list("Hannah"))), "hannaH"),
        ("single", lambda f: "".join(inplace(f, list("x"))), "x"),
        ("empty", lambda f: "".join(inplace(f, [])), ""),
    ]


def _rotate_cases():
    return [
        ("abcdef k=2", lambda f: "".join(inplace(f, list("abcdef"), 2)), "cdefab"),
        ("abcdef k=0", lambda f: "".join(inplace(f, list("abcdef"), 0)), "abcdef"),
        ("abcdef k=6", lambda f: "".join(inplace(f, list("abcdef"), 6)), "abcdef"),
        ("abcdef k=8", lambda f: "".join(inplace(f, list("abcdef"), 8)), "cdefab"),
        ("a k=3", lambda f: "".join(inplace(f, list("a"), 3)), "a"),
    ]


def main():
    mode = argmode(sys.argv)

    if mode == "teach":
        head("LC 344 -- Reverse String :: THE LESSON")
        print(LESSON)
        return
    if mode == "trace":
        head("LC 344 -- Reverse String :: DRY RUN")
        trace("hello")
        trace("Hannah")
        return
    if mode in ("quiz", "answers"):
        head("LC 344 -- Reverse String :: EXAMINER")
        quiz(EXAMINER, show=(mode == "answers"))
        return

    head("LC 344 -- Reverse String")

    sub("reference solution (proof the lesson is not lying to you)")
    check("solve", solve, _one_pointer_cases())

    sub("your variants")
    results = [
        check("V1 reverse_vowels", reverse_vowels, _vowel_cases()),
        check("V2 reverse_first_k", reverse_first_k, _first_k_cases()),
        check("V3 reverse_one_pointer", reverse_one_pointer, _one_pointer_cases()),
        check("V4 rotate_left", rotate_left, _rotate_cases()),
    ]
    report(results)


if __name__ == "__main__":
    main()
