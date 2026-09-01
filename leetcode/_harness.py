"""
Shared harness for the ten LeetCode teaching files.

Nothing problem-specific lives here -- just printing, stub detection and
the test runner, so each lcNNN_*.py file stays about its own problem.
"""

import inspect

W = 72


def rule(ch="="):
    print(ch * W)


def head(title):
    print()
    rule()
    print("  " + title)
    rule()


def sub(title):
    print()
    print("  " + title)
    print("  " + "-" * (W - 4))


def is_stub(fn):
    """True while a function body is still just `pass` (plus comments)."""
    try:
        src = inspect.getsource(fn)
    except Exception:
        return False
    body = []
    for ln in src.splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#") or ln.startswith("def "):
            continue
        body.append(ln)
    return body == ["pass"]


def inplace(fn, seq, *extra):
    """Run an in-place function on a copy and hand back the mutated copy."""
    c = list(seq)
    fn(c, *extra)
    return c


def inplace_k(fn, seq, *extra):
    """For order-CHANGING compaction: (k, first k elements as a multiset)."""
    c = list(seq)
    k = fn(c, *extra)
    if not isinstance(k, int):
        return (k, None)
    return (k, sorted(c[:k]))


def inplace_k_ordered(fn, seq, *extra):
    """For order-PRESERVING compaction: (k, first k elements in order)."""
    c = list(seq)
    k = fn(c, *extra)
    if not isinstance(k, int):
        return (k, None)
    return (k, c[:k])


def check(label, fn, cases):
    """cases: list of (name, call(fn) -> actual, expected).

    Returns "TODO", "PASS" or "FAIL".
    """
    if is_stub(fn):
        print("  [ ] %-34s not attempted" % label)
        return "TODO"
    bad = []
    for name, call, expected in cases:
        try:
            got = call(fn)
            ok = got == expected
        except Exception as exc:
            got = "%s: %s" % (type(exc).__name__, exc)
            ok = False
        if not ok:
            bad.append((name, got, expected))
    if bad:
        print("  [X] %-34s %d/%d" % (label, len(cases) - len(bad), len(cases)))
        for name, got, expected in bad[:4]:
            print("        %s -> %r" % (name, got))
            print("        %s    expected %r" % (" " * len(name), expected))
        return "FAIL"
    print("  [OK] %-33s %d/%d" % (label, len(cases), len(cases)))
    return "PASS"


def report(results):
    done = sum(1 for r in results if r == "PASS")
    fail = sum(1 for r in results if r == "FAIL")
    todo = sum(1 for r in results if r == "TODO")
    print()
    rule("-")
    print("  %d solved   %d failing   %d not attempted" % (done, fail, todo))
    rule("-")


def quiz(pairs, show):
    """pairs: list of (question, answer). show=False hides the answers."""
    for i, (q, a) in enumerate(pairs, 1):
        print()
        print("  Q%d. %s" % (i, q))
        if show:
            for line in a.strip().splitlines():
                print("      " + line.strip())
        else:
            print("      ...")


def argmode(argv):
    """Return one of: run, teach, quiz, answers, trace."""
    for flag in ("teach", "quiz", "answers", "trace"):
        if "--" + flag in argv:
            return flag
    return "run"
