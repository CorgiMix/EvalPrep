"""
======================================================================
  LeetCode 21 -- Merge Two Sorted Lists
  Notebook concepts: Linked Lists, Pointers
======================================================================

THE PROBLEM (as stated on LeetCode)

    You are given the heads of two sorted linked lists list1 and list2.

    Merge the two lists into one sorted list. The list should be made
    by splicing together the nodes of the first two lists.

    Return the head of the merged linked list.

    Example 1:
        Input:  list1 = [1,2,4], list2 = [1,3,4]
        Output: [1,1,2,3,4,4]

    Example 2:
        Input:  list1 = [], list2 = []
        Output: []

    Example 3:
        Input:  list1 = [], list2 = [0]
        Output: [0]

    Constraints:
        The number of nodes in both lists is in the range [0, 50].
        -100 <= Node.val <= 100
        Both list1 and list2 are sorted in non-decreasing order.

    Note the phrase "by SPLICING TOGETHER THE NODES". You are not
    supposed to allocate new nodes holding copied values -- you rewire
    the existing ones. O(1) extra space.

HOW TO USE THIS FILE
    python leetcode/lc021_merge_two_sorted_lists.py --teach / --trace
                                                    --quiz  / --answers
======================================================================
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _harness import head, sub, check, report, quiz, argmode


# ======================================================================
#  THE DATA STRUCTURE
# ======================================================================

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return "ListNode(%r)" % self.val


def build(values):
    """Python list -> linked list. Returns the head, or None if empty."""
    head_node = None
    for v in reversed(values):
        head_node = ListNode(v, head_node)
    return head_node


def unroll(node, limit=200):
    """Linked list -> Python list. `limit` stops runaway cycles."""
    out = []
    while node is not None and len(out) < limit:
        out.append(node.val)
        node = node.next
    return out


# ======================================================================
#  THE LESSON
# ======================================================================

LESSON = """
STEP 1 -- WHAT A LINKED LIST ACTUALLY IS HERE

  A node holds a value and a reference to the next node. The last node
  points at None. You cannot index it, you cannot ask its length
  without walking it, and you cannot go backwards.

  Everything you do is: hold a pointer, look at what it points to,
  move it. That is the entire toolkit.

STEP 2 -- THE SHAPE OF THE ALGORITHM

  You have two sorted lists. Repeatedly take the smaller of the two
  current heads, append it to your output, and advance that list.
  Stop when either list runs out, then attach whatever remains of the
  other -- it is already sorted, so it needs no further work.

  That last part is the piece people miss. You do NOT keep looping to
  drain the remainder one node at a time. One assignment attaches all
  of it.

STEP 3 -- THE DUMMY NODE, AND WHY IT EARNS ITS KEEP

  Without a dummy you must write, on every single append:

      if head is None:
          head = node
      else:
          tail.next = node

  That branch fires exactly once in the whole run and clutters the
  loop forever. Instead:

      dummy = ListNode()      # a throwaway node, value never read
      tail = dummy

  Now `tail.next = node` is unconditionally correct, including the
  very first time. At the end you return dummy.next -- the real head.

  Say it as: "the dummy removes the is-this-the-first-node special
  case, so the loop body has no branch that fires only once." That is
  the reason, and it generalises to almost every linked-list problem.

STEP 4 -- WHY <= AND NOT <

      if list1.val <= list2.val:

  On a tie this takes from list1 first. With < it takes from list2.
  Both produce a correctly SORTED list, so LeetCode accepts either.

  The difference is STABILITY: <= preserves the relative order of
  equal elements, keeping list1's before list2's. It costs nothing and
  it is the convention every real merge (merge sort, database joins)
  follows. Choosing <= deliberately, and being able to say why, is
  free marks.

STEP 5 -- THE INVARIANT

      dummy.next .. tail  is a correctly sorted list containing every
      node already consumed, and `tail` is its last node.
      Every remaining node in list1 and list2 is >= tail.val.

  The second sentence is what licenses appending without ever looking
  backwards.

STEP 6 -- THE ONE-LINE TAIL

      tail.next = list1 or list2

  Python's `or` returns the first operand if it is truthy, otherwise
  the second. Exactly one of these is None when the loop exits (or
  both are, in which case it evaluates to None, which is also correct).

  If that feels too clever to defend under pressure, write it out:

      tail.next = list1 if list1 is not None else list2

  Both are fine. Use whichever you can explain calmly.

STEP 7 -- COMPLEXITY

  Time  O(n + m) -- every node is visited exactly once.
  Space O(1)     -- one dummy node and two pointers. No new nodes are
                    allocated for the data, which is what "splicing"
                    means. The recursive version is O(n + m) STACK
                    space, so it is not O(1) -- do not claim it is.

STEP 8 -- EDGE CASES

  both empty      -> the while never runs, tail.next = None, return None.
  one empty       -> the while never runs, the other is attached whole.
  disjoint ranges -> e.g. [1,2] and [8,9]: one list drains completely,
                     the other is attached in a single assignment.
  all ties        -> [1,1] and [1,1]: <= keeps list1's pair first.
"""


# ======================================================================
#  THE SOLUTION
# ======================================================================

def solve(list1, list2):
    """Splice two sorted linked lists into one. Returns the new head."""
    dummy = ListNode()        # throwaway; kills the is-this-first branch
    tail = dummy
    while list1 and list2:
        # <= not < : keeps equal elements in list1-before-list2 order.
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next
    # Exactly one (or neither) still has nodes; it is already sorted,
    # so one assignment attaches all of it.
    tail.next = list1 or list2
    return dummy.next


def solve_recursive(list1, list2):
    """Same algorithm, recursive. O(n+m) STACK space -- not O(1)."""
    if list1 is None:
        return list2
    if list2 is None:
        return list1
    if list1.val <= list2.val:
        list1.next = solve_recursive(list1.next, list2)
        return list1
    list2.next = solve_recursive(list1, list2.next)
    return list2


# ======================================================================
#  THE DRY RUN
# ======================================================================

def trace(a, b):
    list1, list2 = build(a), build(b)
    print()
    print("  list1 = %r    list2 = %r" % (a, b))
    print()
    print("  %-10s %-10s %-10s %s"
          % ("list1.val", "list2.val", "take", "merged so far"))
    print("  " + "-" * 56)
    dummy = ListNode()
    tail = dummy
    while list1 and list2:
        if list1.val <= list2.val:
            took = "list1 (%d)" % list1.val
            tail.next = list1
            list1 = list1.next
        else:
            took = "list2 (%d)" % list2.val
            tail.next = list2
            list2 = list2.next
        tail = tail.next
        # Snip so the partial print does not run into unmerged nodes.
        saved = tail.next
        tail.next = None
        print("  %-10s %-10s %-10s %r"
              % (list1.val if list1 else "-",
                 list2.val if list2 else "-",
                 took, unroll(dummy.next)))
        tail.next = saved
    rest = list1 or list2
    tail.next = rest
    print()
    print("  loop ends: one list is empty. Attach the remainder %r "
          "in one assignment." % unroll(rest))
    print("  result: %r" % unroll(dummy.next))


# ======================================================================
#  WHAT THE EXAMINER ASKS
# ======================================================================

EXAMINER = [
    ("Why the dummy node?",
     """It removes the is-this-the-first-node special case. Without it
        every append needs an if-else that fires exactly once in the
        whole run. With it, tail.next = node is unconditionally correct
        and you return dummy.next at the end."""),

    ("Why <= rather than <?",
     """Both give a correctly sorted result. <= is stable: it preserves
        the relative order of equal elements, taking from list1 first on
        a tie. That matches the convention of every real merge and costs
        nothing."""),

    ("What is `tail.next = list1 or list2` doing?",
     """Python's `or` yields the first truthy operand. When the loop
        exits at most one list is non-empty, so this attaches whichever
        remains -- or None if both are exhausted. The remainder is
        already sorted, so no further work is needed."""),

    ("Why do you not loop to drain the remaining list?",
     """Because it is already sorted and already linked. Walking it node
        by node would do O(k) pointer writes to achieve what one
        assignment achieves."""),

    ("State the invariant.",
     """The chain from dummy.next to tail is a correctly sorted list of
        every node consumed so far, and every node still in list1 or
        list2 is greater than or equal to tail.val. That second part is
        why appending never needs to look backwards."""),

    ("What is the space complexity?",
     """O(1). One dummy node and two pointers, independent of input
        size. No new nodes are allocated for the data -- the problem
        says to splice the existing nodes, and that is what this
        does."""),

    ("And the recursive version?",
     """Same O(n+m) time, but O(n+m) stack space -- one frame per node.
        Do not claim it is O(1). With Python's default recursion limit
        near 1000 it would also fail on long lists, though this
        problem caps at 50 nodes."""),

    ("What happens if both inputs are empty?",
     """The while loop never runs, tail is still dummy, tail.next
        becomes None, and you return dummy.next which is None. Correct,
        with no special case."""),

    ("Do you modify the input lists?",
     """Yes -- their nodes are rewired into the result. The original
        heads no longer describe their old lists. That is what splicing
        means, and it is worth flagging out loud since it surprises
        callers."""),

    ("How would you extend this to k lists?",
     """Either fold pairwise -- merge the first two, merge the result
        with the third, and so on, which is O(kn) -- or merge in pairs
        tournament-style for O(n log k), or use a min-heap of the k
        current heads, also O(n log k)."""),
]


# ======================================================================
#  YOUR TURN -- VARIANTS
# ======================================================================

# V1 | Write the recursive version yourself. Get the two base cases
#    | right first, then the one recursive step. Then say out loud
#    | what its space complexity is and why it is NOT O(1).
def merge_recursive(list1, list2):
    pass


# V2 | The same algorithm on plain Python lists (no linked nodes).
#    | Return a NEW sorted list; do not use sorted() or list.sort().
#    | ([1,2,4], [1,3,4]) -> [1,1,2,3,4,4]
#    | Proving to yourself that the pattern is about the ALGORITHM and
#    | not about the data structure is the entire point of this one.
#    | This is also the merge step of merge sort -- say so.
def merge_arrays(a, b):
    pass


# V3 | Merge k sorted linked lists. `heads` is a Python list of heads,
#    | any of which may be None. Return the merged head.
#    | Folding pairwise is fine and is the answer to give under time
#    | pressure -- but state its complexity honestly and name the
#    | better approach.
def merge_k_lists(heads):
    pass


# V4 | LeetCode 206. Reverse a linked list in place and return the new
#    | head. This is the other canonical pointer drill, and it pairs
#    | with merging: one rewires between two lists, this rewires
#    | within one.
#    | [1,2,3] -> [3,2,1]      [] -> []
#    | Hint: you need THREE pointers -- previous, current, and a saved
#    | next. Work out on paper why saving next first is mandatory
#    | before you write a line.
def reverse_list(head_node):
    pass


# ======================================================================
#  TESTS -- do not edit
# ======================================================================

def _merge(f, a, b):
    return unroll(f(build(a), build(b)))


def _merge_k(f, lists):
    return unroll(f([build(x) for x in lists]))


def _rev(f, a):
    return unroll(f(build(a)))


_MERGE_CASES = [
    ("[1,2,4] + [1,3,4]", lambda f: _merge(f, [1, 2, 4], [1, 3, 4]), [1, 1, 2, 3, 4, 4]),
    ("[] + []", lambda f: _merge(f, [], []), []),
    ("[] + [0]", lambda f: _merge(f, [], [0]), [0]),
    ("[0] + []", lambda f: _merge(f, [0], []), [0]),
    ("disjoint [1,2]+[8,9]", lambda f: _merge(f, [1, 2], [8, 9]), [1, 2, 8, 9]),
    ("disjoint [8,9]+[1,2]", lambda f: _merge(f, [8, 9], [1, 2]), [1, 2, 8, 9]),
    ("all ties", lambda f: _merge(f, [1, 1], [1, 1]), [1, 1, 1, 1]),
    ("negatives", lambda f: _merge(f, [-3, 1], [-5, 0]), [-5, -3, 0, 1]),
    ("uneven lengths", lambda f: _merge(f, [1], [2, 3, 4, 5]), [1, 2, 3, 4, 5]),
]

_ARRAY_CASES = [
    ("[1,2,4] + [1,3,4]", lambda f: f([1, 2, 4], [1, 3, 4]), [1, 1, 2, 3, 4, 4]),
    ("[] + []", lambda f: f([], []), []),
    ("[] + [0]", lambda f: f([], [0]), [0]),
    ("disjoint", lambda f: f([8, 9], [1, 2]), [1, 2, 8, 9]),
    ("uneven", lambda f: f([1], [2, 3, 4, 5]), [1, 2, 3, 4, 5]),
    ("negatives", lambda f: f([-3, 1], [-5, 0]), [-5, -3, 0, 1]),
]

_K_CASES = [
    ("3 lists", lambda f: _merge_k(f, [[1, 4, 5], [1, 3, 4], [2, 6]]),
     [1, 1, 2, 3, 4, 4, 5, 6]),
    ("no lists", lambda f: _merge_k(f, []), []),
    ("one empty list", lambda f: _merge_k(f, [[]]), []),
    ("all empty", lambda f: _merge_k(f, [[], [], []]), []),
    ("single list", lambda f: _merge_k(f, [[1, 2, 3]]), [1, 2, 3]),
    ("some empty", lambda f: _merge_k(f, [[], [2], [], [1, 3]]), [1, 2, 3]),
]

_REV_CASES = [
    ("[1,2,3]", lambda f: _rev(f, [1, 2, 3]), [3, 2, 1]),
    ("[]", lambda f: _rev(f, []), []),
    ("[1]", lambda f: _rev(f, [1]), [1]),
    ("[1,2]", lambda f: _rev(f, [1, 2]), [2, 1]),
    ("[1,2,3,4,5]", lambda f: _rev(f, [1, 2, 3, 4, 5]), [5, 4, 3, 2, 1]),
]


def main():
    mode = argmode(sys.argv)

    if mode == "teach":
        head("LC 21 -- Merge Two Sorted Lists :: THE LESSON")
        print(LESSON)
        return
    if mode == "trace":
        head("LC 21 -- Merge Two Sorted Lists :: DRY RUN")
        trace([1, 2, 4], [1, 3, 4])
        trace([1, 2], [8, 9])
        return
    if mode in ("quiz", "answers"):
        head("LC 21 -- Merge Two Sorted Lists :: EXAMINER")
        quiz(EXAMINER, show=(mode == "answers"))
        return

    head("LC 21 -- Merge Two Sorted Lists")

    sub("reference solutions")
    check("solve", solve, _MERGE_CASES)
    check("solve_recursive", solve_recursive, _MERGE_CASES)

    sub("your variants")
    results = [
        check("V1 merge_recursive", merge_recursive, _MERGE_CASES),
        check("V2 merge_arrays", merge_arrays, _ARRAY_CASES),
        check("V3 merge_k_lists", merge_k_lists, _K_CASES),
        check("V4 reverse_list", reverse_list, _REV_CASES),
    ]
    report(results)


if __name__ == "__main__":
    main()
