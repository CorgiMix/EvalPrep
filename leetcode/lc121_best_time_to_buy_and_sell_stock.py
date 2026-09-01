"""
======================================================================
  LeetCode 121 -- Best Time to Buy and Sell Stock
  Notebook concepts: Greedy Algorithm, Two Pointers
======================================================================

THE PROBLEM (as stated on LeetCode)

    You are given an array prices where prices[i] is the price of a
    given stock on the ith day.

    You want to maximise your profit by choosing a single day to buy
    one stock and choosing a different day in the future to sell that
    stock.

    Return the maximum profit you can achieve from this transaction.
    If you cannot achieve any profit, return 0.

    Example 1:
        Input:  prices = [7,1,5,3,6,4]
        Output: 5        (buy on day 1 at 1, sell on day 4 at 6)
        Note:   buying at 1 and selling at 0 is not allowed --
                you must buy before you sell.

    Example 2:
        Input:  prices = [7,6,4,3,1]
        Output: 0        (no profitable transaction exists)

    Constraints:
        1 <= prices.length <= 10^5
        0 <= prices[i] <= 10^4

HOW TO USE THIS FILE
    python leetcode/lc121_best_time_to_buy_and_sell_stock.py --teach
                                              --trace --quiz --answers
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
STEP 1 -- SAY WHAT IS BEING MAXIMISED, PRECISELY

      max over all pairs (i, j) with i < j  of  prices[j] - prices[i]
      ... or 0 if every such difference is negative.

  The `i < j` is the whole problem. Without it you would just answer
  max(prices) - min(prices), and that is wrong the moment the maximum
  occurs before the minimum. [7,1] would give 6 instead of 0.

  State that counterexample out loud. It proves you understood the
  ordering constraint rather than reading past it.

STEP 2 -- BRUTE FORCE, THEN THE REFRAME

      for i ...: for j in range(i+1, n): best = max(best, p[j]-p[i])

  O(n^2). Now reframe. Fix the SELL day j and ask: what is the best
  possible buy? Obviously the cheapest price on any day before j.

      best profit selling on day j  =  prices[j] - min(prices[0..j-1])

  And min(prices[0..j-1]) does not need recomputing each time. You can
  carry it forward in a single variable as you walk.

  That is the move: an inner loop that was recomputing a minimum
  becomes one variable updated in O(1).

STEP 3 -- THE INVARIANT

      cheapest = the smallest price seen so far
      best     = the best profit achievable using any sell day so far

  Two numbers. That is the entire state. This is why it is called
  "running state" -- you never look backwards, you carry forward
  exactly what the future needs.

STEP 4 -- THE ORDERING QUESTION EVERYONE GETS ASKED

  Which comes first inside the loop?

      (a)  cheapest = min(cheapest, p)        then   best = max(best, p - cheapest)
      (b)  best = max(best, p - cheapest)     then   cheapest = min(cheapest, p)

  (b) is the strictly faithful one: it only ever sells at a price whose
  buy-day is genuinely earlier.

  (a) looks like it cheats -- on the day of a new minimum it computes
  p - p = 0, which is buying and selling on the same day. But it is
  still CORRECT, because best starts at 0 and a contribution of 0 can
  never raise it. The illegal transaction has zero value, so it cannot
  win.

  Both are right. Being able to explain WHY (a) is safe, rather than
  just asserting it, is the answer that scores.

STEP 5 -- WHY GREEDY IS VALID HERE

  Greedy usually needs an argument. Here it is this: the decision at
  day j depends only on the minimum before j, and that minimum is
  independent of every choice you have made. There is no future
  decision that could make a higher earlier buy-price preferable. So
  taking the running minimum is always optimal -- no backtracking is
  ever needed.

  Contrast with LeetCode 122 (unlimited transactions), where greedy is
  still valid but for a completely different reason, and with problems
  involving a cooldown, where greedy fails outright and you need DP.

STEP 6 -- WHY float('inf') FOR THE INITIAL cheapest

  It is the identity for min: anything beats it, so the first real
  price becomes the minimum with no special-casing of the first
  iteration.

  You could equally write cheapest = prices[0] and loop from index 1 --
  but then you must handle the empty list yourself. The constraints
  forbid an empty list, but a function that crashes on [] is still a
  worse function.

  best starts at 0, not -inf, because "no profit" is a legal answer,
  and 0 is exactly the value of doing nothing.

STEP 7 -- COMPLEXITY AND EDGES

  Time  O(n), one pass.  Space O(1), two numbers.

  [7,6,4,3,1] -> monotonically falling, every p - cheapest is <= 0,
                 best stays 0. Correct.
  [1,2,3,4,5] -> best updates every day, ends at 4.
  [5]         -> one day, no sell day exists, returns 0.
  []          -> loop never runs, returns 0. (Forbidden by the
                 constraints, but it should not crash.)
  all equal   -> every difference is 0, returns 0.
"""


# ======================================================================
#  THE SOLUTION
# ======================================================================

def solve(prices):
    """Max profit from a single buy-then-later-sell. 0 if none exists."""
    cheapest = float("inf")   # identity for min: the first price beats it
    best = 0                  # doing nothing is always available
    for p in prices:
        # Order note: updating cheapest first can compute p - p == 0 on a
        # new minimum. That is a same-day trade, but it is worth 0 and
        # best is already >= 0, so it can never win. Safe either way.
        cheapest = min(cheapest, p)
        best = max(best, p - cheapest)
    return best


def solve_brute(prices):
    """The O(n^2) baseline. State it, then beat it."""
    best = 0
    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            best = max(best, prices[j] - prices[i])
    return best


# ======================================================================
#  THE DRY RUN
# ======================================================================

def trace(prices):
    print()
    print("  prices = %r" % prices)
    print()
    print("  %-5s %-7s %-11s %-14s %-7s %s"
          % ("day", "price", "cheapest", "p - cheapest", "best", "note"))
    print("  " + "-" * 66)
    cheapest = float("inf")
    best = 0
    for i, p in enumerate(prices):
        new_low = p < cheapest
        cheapest = min(cheapest, p)
        gain = p - cheapest
        improved = gain > best
        best = max(best, gain)
        note = []
        if new_low:
            note.append("new minimum")
        if improved:
            note.append("new best")
        print("  %-5d %-7d %-11s %-14d %-7d %s"
              % (i, p, cheapest, gain, best, ", ".join(note)))
    print()
    print("  result: %d" % best)


# ======================================================================
#  WHAT THE EXAMINER ASKS
# ======================================================================

EXAMINER = [
    ("Why is the answer not simply max(prices) - min(prices)?",
     """Because you must buy before you sell. On [7,1] the maximum
        occurs before the minimum, so that formula gives 6 when the
        correct answer is 0."""),

    ("How did you get rid of the inner loop?",
     """By fixing the sell day instead of the buy day. The best profit
        selling on day j is prices[j] minus the cheapest price before j,
        and that running minimum can be carried in one variable rather
        than recomputed."""),

    ("State your invariant.",
     """`cheapest` is the smallest price seen so far, and `best` is the
        largest profit achievable by selling on any day processed so
        far."""),

    ("You update cheapest before computing the profit. Doesn't that let "
     "you buy and sell on the same day?",
     """It computes p - p == 0 on a new minimum, which is indeed a
        same-day trade -- but it is worth zero, and best is initialised
        to 0, so it can never raise the answer. The illegal transaction
        has no value, so correctness is preserved. Swapping the two
        lines avoids it entirely if you prefer strictness."""),

    ("Why does greedy work here? Greedy usually needs justification.",
     """Because the decision at day j depends only on the minimum before
        j, and that minimum is independent of any choice made. No future
        decision could make a higher earlier buy price preferable, so
        the running minimum is always optimal and no backtracking is
        needed."""),

    ("Why initialise best to 0 rather than negative infinity?",
     """Because 'make no trade' is a legal outcome worth exactly 0, and
        the problem says to return 0 when no profit is possible. Zero is
        the value of the do-nothing option, so it is the right floor."""),

    ("Why float('inf') for cheapest?",
     """It is the identity element for min, so the first real price
        replaces it without special-casing the first iteration."""),

    ("What does your code return for a single-element list?",
     """0. There is no later day to sell on, cheapest becomes that price,
        the profit is 0, and best stays 0."""),

    ("Now allow unlimited transactions.",
     """That is LeetCode 122, and it becomes much easier: sum every
        positive consecutive difference. Every upward step can be
        captured independently, so the answer is
        sum(max(0, p[i] - p[i-1])). Different greedy argument
        entirely."""),

    ("Where does greedy stop working?",
     """As soon as transactions interact -- a cooldown after selling, a
        transaction fee, or a cap of exactly k trades. Then a locally
        best trade can block a globally better pair and you need
        dynamic programming over (day, state)."""),
]


# ======================================================================
#  YOUR TURN -- VARIANTS
# ======================================================================

# V1 | Return (buy_day, sell_day, profit) rather than just the profit.
#    | If no profitable trade exists return (-1, -1, 0).
#    | [7,1,5,3,6,4] -> (1, 4, 5)      [7,6,4,3,1] -> (-1, -1, 0)
#    | Hint: you now need to remember WHERE the cheapest price was, not
#    | just what it was -- and you must only commit the buy day at the
#    | moment you improve `best`, not when you find a new minimum.
#    | That distinction is the entire exercise.
def max_profit_with_days(prices):
    pass


# V2 | LeetCode 122. Unlimited transactions -- you may buy and sell as
#    | many times as you like, but you may hold at most one share, so
#    | you must sell before buying again.
#    | [7,1,5,3,6,4] -> 7       [1,2,3,4,5] -> 4       [7,6,4,3,1] -> 0
#    | This is two lines. Work out the greedy argument BEFORE coding:
#    | why can every upward step be taken independently?
def max_profit_many(prices):
    pass


# V3 | Maximum DRAWDOWN: the largest drop from an earlier price to a
#    | later one, i.e. max over i < j of prices[i] - prices[j].
#    | Return 0 if prices never fall.
#    | [7,1,5,3,6,4] -> 6   (7 down to 1)      [1,2,3] -> 0
#    | This is the mirror image of the original. Say precisely which
#    | two things swap -- it is not just min and max.
def max_drawdown(prices):
    pass


# V4 | Single transaction, but with a fixed FEE charged on each
#    | completed trade. Return the max profit after the fee, or 0.
#    | ([7,1,5,3,6,4], 1) -> 4       ([1,3,2,8], 2) -> 5
#    | ([1,2], 5) -> 0
#    | Careful: the fee can make an otherwise-positive trade not worth
#    | doing. Where exactly does it belong in your loop?
def max_profit_with_fee(prices, fee):
    pass


# ======================================================================
#  TESTS -- do not edit
# ======================================================================

_SOLVE_CASES = [
    ("[7,1,5,3,6,4]", lambda f: f([7, 1, 5, 3, 6, 4]), 5),
    ("[7,6,4,3,1]", lambda f: f([7, 6, 4, 3, 1]), 0),
    ("rising", lambda f: f([1, 2, 3, 4, 5]), 4),
    ("single", lambda f: f([5]), 0),
    ("empty", lambda f: f([]), 0),
    ("all equal", lambda f: f([3, 3, 3]), 0),
    ("min after max", lambda f: f([7, 1]), 0),
    ("late dip late peak", lambda f: f([9, 8, 1, 2, 100]), 99),
]

_DAYS_CASES = [
    ("[7,1,5,3,6,4]", lambda f: f([7, 1, 5, 3, 6, 4]), (1, 4, 5)),
    ("[7,6,4,3,1]", lambda f: f([7, 6, 4, 3, 1]), (-1, -1, 0)),
    ("rising", lambda f: f([1, 2, 3, 4, 5]), (0, 4, 4)),
    ("single", lambda f: f([5]), (-1, -1, 0)),
    ("empty", lambda f: f([]), (-1, -1, 0)),
    ("all equal", lambda f: f([3, 3, 3]), (-1, -1, 0)),
    ("late dip late peak", lambda f: f([9, 8, 1, 2, 100]), (2, 4, 99)),
]

_MANY_CASES = [
    ("[7,1,5,3,6,4]", lambda f: f([7, 1, 5, 3, 6, 4]), 7),
    ("[1,2,3,4,5]", lambda f: f([1, 2, 3, 4, 5]), 4),
    ("[7,6,4,3,1]", lambda f: f([7, 6, 4, 3, 1]), 0),
    ("single", lambda f: f([5]), 0),
    ("empty", lambda f: f([]), 0),
    ("zigzag", lambda f: f([1, 5, 1, 5, 1, 5]), 12),
]

_DRAWDOWN_CASES = [
    ("[7,1,5,3,6,4]", lambda f: f([7, 1, 5, 3, 6, 4]), 6),
    ("[1,2,3]", lambda f: f([1, 2, 3]), 0),
    ("[5,4,3,2,1]", lambda f: f([5, 4, 3, 2, 1]), 4),
    ("single", lambda f: f([5]), 0),
    ("empty", lambda f: f([]), 0),
    ("peak then trough", lambda f: f([1, 100, 2, 50]), 98),
]

_FEE_CASES = [
    ("[7,1,5,3,6,4] fee 1", lambda f: f([7, 1, 5, 3, 6, 4], 1), 4),
    ("[1,3,2,8] fee 2", lambda f: f([1, 3, 2, 8], 2), 5),
    ("[1,2] fee 5", lambda f: f([1, 2], 5), 0),
    ("[7,6,4] fee 0", lambda f: f([7, 6, 4], 0), 0),
    ("[1,10] fee 0", lambda f: f([1, 10], 0), 9),
    ("empty", lambda f: f([], 1), 0),
]


def main():
    mode = argmode(sys.argv)

    if mode == "teach":
        head("LC 121 -- Best Time to Buy and Sell Stock :: THE LESSON")
        print(LESSON)
        return
    if mode == "trace":
        head("LC 121 -- Best Time to Buy and Sell Stock :: DRY RUN")
        trace([7, 1, 5, 3, 6, 4])
        trace([7, 6, 4, 3, 1])
        return
    if mode in ("quiz", "answers"):
        head("LC 121 -- Best Time to Buy and Sell Stock :: EXAMINER")
        quiz(EXAMINER, show=(mode == "answers"))
        return

    head("LC 121 -- Best Time to Buy and Sell Stock")

    sub("reference solutions")
    check("solve", solve, _SOLVE_CASES)
    check("solve_brute", solve_brute, _SOLVE_CASES)

    sub("your variants")
    results = [
        check("V1 max_profit_with_days", max_profit_with_days, _DAYS_CASES),
        check("V2 max_profit_many", max_profit_many, _MANY_CASES),
        check("V3 max_drawdown", max_drawdown, _DRAWDOWN_CASES),
        check("V4 max_profit_with_fee", max_profit_with_fee, _FEE_CASES),
    ]
    report(results)


if __name__ == "__main__":
    main()
