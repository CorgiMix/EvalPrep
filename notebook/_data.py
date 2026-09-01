"""
Shared data layer for the notebook study files.

Reproduces the assignment's pipeline exactly:
    load_raw()   -> the 1236 x 16 frame Q2.1's starter code hands you
    load_clean() -> the 993 x 14 frame Q2.2 leaves behind
    build_xy()   -> the 993 x 40 X and the 993-long y from Q3.1

Everything else in these files is checked against these, so if the
numbers here are right, the lessons are right.
"""

import os
import inspect

import numpy as np
import pandas as pd

URL = ("https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/"
       "master/csv/mosaicData/Gestation.csv")

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(os.path.dirname(HERE), "gestation_raw.csv")

# The starter code in Q2.1 drops these eight and renames three.
DROP = ["rownames", "id", "date", "plurality", "outcome", "sex", "time", "number"]
RENAME = {"wt": "bwt", "ht": "height", "wt.1": "weight"}

NUMERIC = ["gestation", "parity", "age", "height", "weight", "dage"]
CATEGORICAL = ["race", "ed", "drace", "ded", "marital", "inc", "smoke"]


def load_raw():
    """The 1236 x 16 frame, after Q2.1's given drops and renames."""
    src = CACHE if os.path.exists(CACHE) else URL
    df = pd.read_csv(src)
    if not os.path.exists(CACHE):
        df.to_csv(CACHE, index=False)
    df = df.drop(columns=[c for c in DROP if c in df.columns])
    return df.rename(columns=RENAME)


def load_clean():
    """The 993 x 14 frame: drop dht/dwt as COLUMNS, then any row with a NaN."""
    df = load_raw()
    df = df.drop(columns=["dht", "dwt"])
    return df.dropna().reset_index(drop=True)


def oz_to_grams(oz):
    return round(oz * 28.3495, 2)


def classify_weight(bwt_oz):
    g = oz_to_grams(bwt_oz)
    if g < 2500:
        return "Low"
    elif g < 4000:
        return "Normal"
    return "High"


def build_xy(df=None):
    """Q3.1: numeric columns as-is + one-hot categoricals, drop_first=True."""
    if df is None:
        df = load_clean()
    cols = NUMERIC + CATEGORICAL
    X = pd.get_dummies(df[cols], columns=CATEGORICAL, drop_first=True)
    X = X.astype(float)
    return X, df["bwt"]


def split(X, y, test_size=0.2, random_state=42):
    from sklearn.model_selection import train_test_split
    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def fit_linear(X_train, y_train):
    from sklearn.linear_model import LinearRegression
    return LinearRegression().fit(X_train, y_train)


def metrics(model, X_test, y_test):
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    pred = model.predict(X_test)
    mse = mean_squared_error(y_test, pred)
    return {
        "MAE": mean_absolute_error(y_test, pred),
        "RMSE": float(np.sqrt(mse)),
        "R2": r2_score(y_test, pred),
    }


# ----------------------------------------------------------------------
#  Presentation / marking helpers, shared with the leetcode harness style
# ----------------------------------------------------------------------

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


def _same(got, expected, tol=1e-6):
    if isinstance(expected, pd.DataFrame):
        if not isinstance(got, pd.DataFrame):
            return False
        try:
            pd.testing.assert_frame_equal(
                got, expected, check_dtype=False, check_like=True, rtol=1e-6)
            return True
        except Exception:
            return False
    if isinstance(expected, pd.Series):
        if not isinstance(got, pd.Series):
            return False
        try:
            pd.testing.assert_series_equal(
                got, expected, check_dtype=False, check_names=False, rtol=1e-6)
            return True
        except Exception:
            return False
    if isinstance(expected, float):
        try:
            return abs(float(got) - expected) < max(tol, abs(expected) * 1e-6)
        except Exception:
            return False
    if isinstance(expected, dict):
        if not isinstance(got, dict) or set(got) != set(expected):
            return False
        return all(_same(got[k], expected[k]) for k in expected)
    if isinstance(expected, tuple) and any(isinstance(e, float) for e in expected):
        if not isinstance(got, (tuple, list)) or len(got) != len(expected):
            return False
        return all(_same(g, e) for g, e in zip(got, expected))
    return got == expected


def check(label, fn, cases):
    if is_stub(fn):
        print("  [ ] %-38s not attempted" % label)
        return "TODO"
    bad = []
    for name, call, expected in cases:
        try:
            got = call(fn)
            ok = _same(got, expected)
        except Exception as exc:
            got = "%s: %s" % (type(exc).__name__, exc)
            ok = False
        if not ok:
            bad.append((name, got, expected))
    if bad:
        print("  [X] %-38s %d/%d" % (label, len(cases) - len(bad), len(cases)))
        for name, got, expected in bad[:3]:
            print("        %s" % name)
            print("          got      %s" % _short(got))
            print("          expected %s" % _short(expected))
        return "FAIL"
    print("  [OK] %-37s %d/%d" % (label, len(cases), len(cases)))
    return "PASS"


def _short(v, n=140):
    s = repr(v).replace("\n", " ")
    return s if len(s) <= n else s[:n] + " ..."


def report(results):
    done = sum(1 for r in results if r == "PASS")
    fail = sum(1 for r in results if r == "FAIL")
    todo = sum(1 for r in results if r == "TODO")
    print()
    rule("-")
    print("  %d solved   %d failing   %d not attempted" % (done, fail, todo))
    rule("-")


def quiz(pairs, show):
    for i, (q, a) in enumerate(pairs, 1):
        print()
        print("  Q%d. %s" % (i, q))
        if show:
            for line in a.strip().splitlines():
                print("      " + line.strip())
        else:
            print("      ...")


def argmode(argv):
    for flag in ("teach", "quiz", "answers", "trace"):
        if "--" + flag in argv:
            return flag
    return "run"


def which(argv):
    """Optional question id, e.g. `--teach 2.2` -> '2.2'."""
    for a in argv[1:]:
        if not a.startswith("--") and any(ch.isdigit() for ch in a):
            return a
    return None
