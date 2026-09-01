"""
======================================================================
  LeetCode 125 -- Valid Palindrome
  Notebook concepts: String Manipulation, Two Pointers
======================================================================

THE PROBLEM (as stated on LeetCode)

    A phrase is a palindrome if, after converting all uppercase letters
    into lowercase letters and removing all non-alphanumeric characters,
    it reads the same forward and backward. Alphanumeric characters
    include letters and numbers.

    Given a string s, return true if it is a palindrome, or false
    otherwise.

    Example 1:
        Input:  s = "A man, a plan, a canal: Panama"
        Output: true          ("amanaplanacanalpanama")

    Example 2:
        Input:  s = "race a car"
        Output: false         ("raceacar")

    Example 3:
        Input:  s = " "
        Output: true          (the empty string reads the same both ways)

    Constraints:
        1 <= s.length <= 2 * 10^5
        s consists only of printable ASCII characters.

HOW TO USE THIS FILE
    python leetcode/lc125_valid_palindrome.py --teach / --trace
                                              --quiz  / --answers
    python leetcode/lc125_valid_palindrome.py          run your variants
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
STEP 1 -- WHAT CHANGED FROM 344

  Reverse String swapped UNCONDITIONALLY: every position was a legal
  position. Here two things break that.

    (a) You COMPARE instead of swap, so a mismatch means early exit.
    (b) Some positions must not be compared at all. Commas, colons and
        spaces have to be stepped over.

  (b) is the entire problem. Everything else is 344.

STEP 2 -- THE TEMPTING WRONG ANSWER

      clean = "".join(c.lower() for c in s if c.isalnum())
      return clean == clean[::-1]

  This is CORRECT. It is also two O(n) allocations, and the follow-up
  question is always "now do it in O(1) extra space". Offer it as your
  baseline, name its cost, then write the pointer version. Volunteering
  the trade-off before you are asked is worth real marks.

STEP 3 -- THE INVARIANT

      Everything OUTSIDE the window [i, j] has already been checked and
      matched as a palindrome pair.

  Compare that with 344's "already in its final position". Same window,
  same shrinking, different verb.

STEP 4 -- SKIP BEFORE YOU COMPARE, NEVER AFTER

  Consider s = "a,". If you compare first, you test 'a' against ',',
  they differ, and you return False. But stripping punctuation leaves
  "a", which IS a palindrome. Comparing a character that should never
  have entered the conversation has already lost you the answer.

  So the loop body is: advance i past junk, retreat j past junk, THEN
  compare.

STEP 5 -- THE GUARD, AND WHY IT IS NOT DEFENSIVE PADDING

  The naive skip has no bound:

      while not s[i].isalnum():
          i += 1

  Feed it ",,," -- there is no alphanumeric character to stop at, so i
  walks 0, 1, 2, 3 and raises IndexError. The only exit condition is
  "found a letter" and there is no letter.

  Carrying the outer condition into the inner loop fixes it:

      while i < j and not s[i].isalnum():

  Say this out loud: the `i < j` is the TERMINATION PROOF of the inner
  loop, not a crash guard. i can never pass j, so it can never leave
  the string. That sentence separates someone who memorised the guard
  from someone who understands it.

STEP 6 -- THE "0P" TRAP

  Both characters are alphanumeric, so no skipping happens at all.
  '0'.lower() is '0', 'P'.lower() is 'p', they differ, answer False.
  Correct.

  People who hand-roll case folding as `ord(c) | 32` instead of .lower()
  get True here, because ord('0') | 32 == ord('P') | 32 == 112. It is
  the single most common wrong answer on this problem. Know it by name.

STEP 7 -- "YOU HAVE A WHILE INSIDE A WHILE. ISN'T THAT O(n^2)?"

  No, and this is the question that catches people.

  i only ever increases; j only ever decreases. Across the ENTIRE run,
  the inner loops can advance i at most n times in total and retreat j
  at most n times in total. Total work is bounded by 2n, so the whole
  thing is O(n).

  Nesting is not what makes something quadratic. Re-scanning is. These
  pointers never re-scan.

STEP 8 -- COMPLEXITY AND EDGES

  Time  O(n).   Space O(1) -- two integers.

  " "     -> i stops at 0 (i<j fails immediately at n=1), True.
  ",,,"   -> guard halts i at j, compares s[j] to itself, True.
  "0P"    -> False.
  "aa"    -> True after one comparison.
"""


# ======================================================================
#  THE SOLUTION
# ======================================================================

def solve(s):
    """True if s is a palindrome ignoring case and non-alphanumerics."""
    i, j = 0, len(s) - 1
    while i < j:
        # Skip first. The `i < j` in each inner loop is what makes them
        # terminate on an all-punctuation string.
        while i < j and not s[i].isalnum():
            i += 1
        while i < j and not s[j].isalnum():
            j -= 1
        # .lower() on two characters is O(1) space; lowering the whole
        # string up front would not be.
        if s[i].lower() != s[j].lower():
            return False
        i += 1
        j -= 1
    return True


# ======================================================================
#  THE DRY RUN
# ======================================================================

def trace(s):
    print()
    print("  input: %r   (n = %d)" % (s, len(s)))
    print()
    print("  %-5s %-5s %-6s %-6s %s" % ("i", "j", "s[i]", "s[j]", "what happens"))
    print("  " + "-" * 56)
    i, j = 0, len(s) - 1
    while i < j:
        i0, j0 = i, j
        while i < j and not s[i].isalnum():
            i += 1
        while i < j and not s[j].isalnum():
            j -= 1
        if (i, j) != (i0, j0):
            print("  %-5s %-5s %-6s %-6s %s"
                  % ("%d->%d" % (i0, i), "%d->%d" % (j0, j), "", "", "skipped junk"))
        if s[i].lower() != s[j].lower():
            print("  %-5d %-5d %-6r %-6r %s" % (i, j, s[i], s[j], "MISMATCH -> False"))
            print()
            print("  result: False")
            return
        print("  %-5d %-5d %-6r %-6r %s" % (i, j, s[i], s[j], "match"))
        i += 1
        j -= 1
    print("  %-5d %-5d %-6s %-6s %s" % (i, j, "", "", "i < j is false, stop"))
    print()
    print("  result: True")


# ======================================================================
#  WHAT THE EXAMINER ASKS
# ======================================================================

EXAMINER = [
    ("Give me the one-line solution, then tell me why you did not use it.",
     """clean = "".join(c.lower() for c in s if c.isalnum());
        return clean == clean[::-1].
        It is correct but allocates two strings of length n, so O(n)
        extra space. The two-pointer version is O(1)."""),

    ("Why must the skip happen before the comparison rather than after?",
     """Because comparing a non-alphanumeric character can decide the
        answer wrongly. On "a," a compare-first version tests 'a' against
        ',', returns False, but the cleaned string is "a" -- a
        palindrome."""),

    ("What happens on the input ',,,' if you drop the `i < j` from the "
     "inner skip loops?",
     """IndexError. There is no alphanumeric character to halt on, so i
        increments past the end of the string. The guard is the inner
        loop's termination proof, not merely a crash guard."""),

    ("You have a while inside a while. Is this O(n^2)?",
     """No. i only increases and j only decreases, so summed over the
        whole run the inner loops do at most 2n steps in total. The
        algorithm is O(n). Nesting does not imply quadratic; re-scanning
        does, and there is no re-scanning here."""),

    ("What does your function return for '0P'?",
     """False, correctly. It is the classic trap for anyone folding case
        with `ord(c) | 32` instead of .lower(), because that maps both
        '0' and 'P' to 112."""),

    ("Why lower() at compare time rather than lowering s once up front?",
     """Lowering the whole string allocates an O(n) copy and breaks the
        space constraint. Lowering two characters per iteration is
        O(1)."""),

    ("Is `.isalnum()` exactly what the problem means by alphanumeric?",
     """Close but not identical. Python's str.isalnum() is Unicode-aware,
        so it accepts characters like superscripts and non-Latin digits.
        The constraint here says printable ASCII only, so it is safe.
        Noticing the gap is the point."""),
]


# ======================================================================
#  YOUR TURN -- VARIANTS
# ======================================================================

# V1 | Generalise the skip rule. `keep` is a one-argument function that
#    | returns True for characters that count. Everything else is
#    | skipped. Case-folding still applies.
#    | This is the most realistic "adapt it live" ask on this problem:
#    | the assessor changes the definition of a relevant character and
#    | watches whether your code had that idea factored out.
#    |   keep=str.isalnum  behaves exactly like solve()
#    |   keep=str.isalpha  makes "1a1" a palindrome (only 'a' counts)
def is_palindrome_ignoring(s, keep):
    pass


# V2 | LeetCode 680. Return True if s can be a palindrome after
#    | deleting AT MOST one character. Plain lowercase letters only --
#    | no alphanumeric filtering here.
#    | "aba" -> True    "abca" -> True (drop 'c')    "abc" -> False
#    | Hint: walk in from both ends as usual. The moment you hit a
#    | mismatch you have exactly two candidate repairs. Test both.
def valid_palindrome_one_deletion(s):
    pass


# V3 | LeetCode 9. Is the INTEGER x a palindrome? You may not convert
#    | it to a string.
#    | 121 -> True    -121 -> False    10 -> False    0 -> True
#    | Hint: build the reversed number one digit at a time with
#    | x % 10 and x //= 10, and stop at the halfway point rather than
#    | reversing the whole thing (which could overflow in other
#    | languages -- say that out loud, it is the intended insight).
def is_palindrome_number(x):
    pass


# V4 | Return the (i, j) index pair where the palindrome check first
#    | fails, AFTER skipping junk -- or None if s is a palindrome.
#    | Same alphanumeric/case rules as solve().
#    | "race a car" -> (3, 5)        "A man, a plan..." -> None
#    | This one is pure invariant comprehension: you must know exactly
#    | what your pointers hold at the moment of failure.
def first_mismatch(s):
    pass


# ======================================================================
#  TESTS -- do not edit
# ======================================================================

_SOLVE_CASES = [
    ("A man, a plan, a canal: Panama", lambda f: f("A man, a plan, a canal: Panama"), True),
    ("race a car", lambda f: f("race a car"), False),
    ("single space", lambda f: f(" "), True),
    ("all punctuation", lambda f: f(",,,"), True),
    ("0P", lambda f: f("0P"), False),
    ("a,", lambda f: f("a,"), True),
    ("aa", lambda f: f("aa"), True),
    ("ab", lambda f: f("ab"), False),
    ("a,, a", lambda f: f("a,, a"), True),
]


def _ignoring_cases():
    import builtins
    alnum = str.isalnum
    alpha = str.isalpha
    return [
        ("alnum: Panama", lambda f: f("A man, a plan, a canal: Panama", alnum), True),
        ("alnum: race a car", lambda f: f("race a car", alnum), False),
        ("alnum: ,,,", lambda f: f(",,,", alnum), True),
        ("alpha: 1a1", lambda f: f("1a1", alpha), True),
        ("alpha: 1ab1", lambda f: f("1ab1", alpha), False),
        ("alpha: 12321", lambda f: f("12321", alpha), True),
        ("alnum: 12321", lambda f: f("12321", alnum), True),
    ]


_DELETION_CASES = [
    ("aba", lambda f: f("aba"), True),
    ("abca", lambda f: f("abca"), True),
    ("abc", lambda f: f("abc"), False),
    ("deeee", lambda f: f("deeee"), True),
    ("cbbcc", lambda f: f("cbbcc"), True),
    ("empty", lambda f: f(""), True),
    ("a", lambda f: f("a"), True),
    ("eeccccbebaeeabebccceea", lambda f: f("eeccccbebaeeabebccceea"), False),
]

_NUMBER_CASES = [
    ("121", lambda f: f(121), True),
    ("-121", lambda f: f(-121), False),
    ("10", lambda f: f(10), False),
    ("0", lambda f: f(0), True),
    ("1221", lambda f: f(1221), True),
    ("12321", lambda f: f(12321), True),
    ("100", lambda f: f(100), False),
    ("7", lambda f: f(7), True),
]

_MISMATCH_CASES = [
    ("race a car", lambda f: f("race a car"), (3, 5)),
    ("Panama", lambda f: f("A man, a plan, a canal: Panama"), None),
    ("0P", lambda f: f("0P"), (0, 1)),
    (",,,", lambda f: f(",,,"), None),
    ("ab", lambda f: f("ab"), (0, 1)),
]


def main():
    mode = argmode(sys.argv)

    if mode == "teach":
        head("LC 125 -- Valid Palindrome :: THE LESSON")
        print(LESSON)
        return
    if mode == "trace":
        head("LC 125 -- Valid Palindrome :: DRY RUN")
        trace("a,, a")
        trace("race a car")
        trace(",,,")
        return
    if mode in ("quiz", "answers"):
        head("LC 125 -- Valid Palindrome :: EXAMINER")
        quiz(EXAMINER, show=(mode == "answers"))
        return

    head("LC 125 -- Valid Palindrome")

    sub("reference solution")
    check("solve", solve, _SOLVE_CASES)

    sub("your variants")
    results = [
        check("V1 is_palindrome_ignoring", is_palindrome_ignoring, _ignoring_cases()),
        check("V2 valid_palindrome_one_deletion", valid_palindrome_one_deletion, _DELETION_CASES),
        check("V3 is_palindrome_number", is_palindrome_number, _NUMBER_CASES),
        check("V4 first_mismatch", first_mismatch, _MISMATCH_CASES),
    ]
    report(results)


if __name__ == "__main__":
    main()
