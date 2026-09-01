"""
LIVE-EDIT DRILLS  --  Gestation notebook, adapting code on the fly
====================================================================

HOW TO USE
    1. Run it:            .venv\\Scripts\\python.exe drills.py
    2. Every drill says NOT ATTEMPTED. That is correct on the first run.
    3. Open this file, find a drill, replace the `pass` with your code.
    4. Re-run. Repeat until everything is PASS.

RULES THAT MAKE THIS WORTH DOING
    - Do not open the guide while drilling. Look things up only AFTER
      you have failed an attempt. Retrieval is what builds the reflex;
      reading feels like learning but is not.
    - Say what you are writing out loud as you type it. That is the
      thing actually being graded on the day.
    - Time yourself. Anything over 3 minutes for one drill means you
      do not know it yet.

    Stuck? Run:  python drills.py --hint 7      (hint for drill 7)

Everything above the DRILLS banner is given to you -- do not edit it.
"""

import os
import sys

import numpy as np
import pandas as pd

# --------------------------------------------------------------------
# GIVEN SETUP -- do not edit
# --------------------------------------------------------------------

URL = ("https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/"
       "master/csv/mosaicData/Gestation.csv")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "gestation_raw.csv")

CATEGORICAL = ["race", "ed", "drace", "ded", "marital", "inc", "smoke"]
NUMERIC = ["gestation", "parity", "age", "height", "weight", "dage"]


def load_raw():
    """The 1236x16 frame, still containing NaN and the dht/dwt columns."""
    if os.path.exists(CACHE):
        raw = pd.read_csv(CACHE)
    else:
        raw = pd.read_csv(URL)
        raw.to_csv(CACHE, index=False)
    df = raw.drop(columns=["rownames", "id", "date", "plurality",
                           "outcome", "sex", "time", "number"])
    return df.rename(columns={"wt": "bwt", "ht": "height", "wt.1": "weight"})


def load_clean():
    """The 993x14 analysis frame, as at the end of Q2.2."""
    return load_raw().drop(columns=["dht", "dwt"]).dropna()


def oz_to_grams(oz):
    return round(oz * 28.3495, 2)


def classify_weight(bwt_oz):
    g = oz_to_grams(bwt_oz)
    return "Low" if g < 2500 else ("Normal" if g < 4000 else "High")


def build_xy(df):
    """X (993x40) and y, exactly as in Q3.1."""
    X = pd.get_dummies(df.drop(columns=["bwt"]),
                       columns=CATEGORICAL, drop_first=True)
    return X, df["bwt"]


# ====================================================================
#  D R I L L S   --   your code goes below. Replace each `pass`.
# ====================================================================

# --- PART 1 ---------------------------------------------------------

# DRILL 1  |  THEY SAY: "Make it take a number of decimal places, and
#          |  make it able to convert the other way too. Don't break
#          |  any of my existing calls."
def d01_oz_to_grams(oz, dp=2, reverse=False):
    pass


# DRILL 2  |  THEY SAY: "Add a Very Low category for anything under
#          |  1500 grams."
#          |  Return one of: "Very Low" / "Low" / "Normal" / "High"
def d02_classify(bwt_oz):
    pass


# DRILL 3  |  THEY SAY: "Add the median to your summary stats."
#          |  Return dict with keys: count, min, max, mean, median
#          |  No statistics/numpy -- built-ins only.
def d03_summary(data):
    pass


# --- PART 2 ---------------------------------------------------------

# DRILL 4  |  THEY SAY: "Instead of hard-coding dht and dwt, drop any
#          |  column that's more than 30% missing."
#          |  `df` is the RAW 1236-row frame. Return a sorted list of
#          |  the column NAMES you would drop.
def d04_high_missing(df, frac=0.30):
    pass


# DRILL 5  |  THEY SAY: "Give me the mean, the count and the standard
#          |  deviation of birth weight for each smoking group."
#          |  Return a DataFrame indexed by smoke, columns exactly
#          |  ["mean", "count", "std"].
def d05_smoke_table(df):
    pass


# DRILL 6  |  THEY SAY: "You told me 55.5% smoke. I want the percentage
#          |  who are smoking DURING the pregnancy."
#          |  Return a float, e.g. 39.2
def d06_current_smoker_pct(df):
    pass


# DRILL 7  |  THEY SAY: "Redo weight_category with pd.cut instead of
#          |  apply -- and it must agree with your function exactly."
#          |  Return a Series of strings aligned to df.index.
#          |  (Careful: the boundary at 2500 is the whole point.)
def d07_cut_categories(df):
    pass


# DRILL 8  |  THEY SAY: "Only current smokers this time, still under
#          |  100 ounces, and just show me the 10 lightest."
#          |  Return a DataFrame of 10 rows sorted lightest first.
def d08_high_risk(df):
    pass


# DRILL 9  |  THEY SAY: "Forget the biggest pair in the matrix -- what
#          |  actually correlates with birth weight?"
#          |  Return a Series of ABSOLUTE correlations with bwt,
#          |  strongest first, excluding bwt itself.
def d09_bwt_corr(df):
    pass


# --- PART 3 ---------------------------------------------------------

# DRILL 10 |  THEY SAY: "Income is ordered and you threw that away.
#          |  Encode it as a single numeric column."
#          |  Return a numeric Series aligned to df.index, no NaN.
def d10_income_ordinal(df):
    pass


# DRILL 11 |  THEY SAY: "Do it 70/30 with seed 0 instead."
#          |  Return (X_train, X_test, y_train, y_test)
def d11_split(X, y):
    pass


# DRILL 12 |  THEY SAY: "Your biggest coefficient isn't your biggest
#          |  effect. Rank them fairly."
#          |  Standardise, refit, return the top 5 by absolute value
#          |  as a Series (keep the signs).
def d12_std_coefs(X_train, y_train):
    pass


# DRILL 13 |  THEY SAY: "Score it on the training set as well."
#          |  Return (train_r2, test_r2) as floats.
def d13_r2_gap(X_train, X_test, y_train, y_test):
    pass


# DRILL 14 |  THEY SAY: "Cross-validate it with MAE instead, 5 folds."
#          |  Return the mean MAE as a POSITIVE float.
#          |  (Remember what sklearn does to error metrics.)
def d14_cv_mae(X, y):
    pass


# DRILL 15 |  THEY SAY: "You said race and drace are collinear. Show me
#          |  Ridge fixes it."
#          |  Fit scaled OLS and scaled Ridge(alpha=10) on the same
#          |  split. Return dict:
#          |    {"ols_r2":, "ridge_r2":, "ols_max_coef":, "ridge_max_coef":}
#          |  where *_max_coef is the largest ABSOLUTE coefficient.
def d15_ridge_vs_ols(X_train, X_test, y_train, y_test):
    pass


# ====================================================================
#  MARKING -- do not edit below this line
# ====================================================================

HINTS = {
    1: "Keep dp=2 and reverse=False as DEFAULTS so old calls still work. "
       "One factor, two branches.",
    2: "Branch order matters. The <1500 test must come FIRST or it can "
       "never be reached.",
    3: "sorted(), then n//2. Even length averages the two middle values.",
    4: "df.isna().mean() gives the FRACTION missing per column. Compare, "
       "then take .index and list() it.",
    5: "groupby(...)[...].agg([...]) takes a list of function names.",
    6: "Same trick as before but == 'now', not != 'never'. Mean of a "
       "boolean is a proportion.",
    7: "pd.cut(..., bins=[...], labels=[...], right=False). Without "
       "right=False, 2500 lands in the WRONG bin. Use float('inf') as "
       "the top edge, and compare against classify_weight to check.",
    8: "Build a mask, then .nsmallest(10, 'bwt') -- which also sorts.",
    9: "df[numeric].corr()['bwt'], then .drop('bwt'), .abs(), "
       ".sort_values(ascending=False).",
    10: "Build a dict of bracket -> midpoint, then .map(). Check "
        ".isna().sum() is 0 -- a missed level silently becomes NaN.",
    11: "test_size=0.3, random_state=0.",
    12: "make_pipeline(StandardScaler(), LinearRegression()). The "
        "coefficients live on pipe[-1].coef_. Sort by .abs() but return "
        "the SIGNED values -- reindex is the trick.",
    13: "Fit once, call r2_score twice -- once on train predictions, "
        "once on test.",
    14: "scoring='neg_mean_absolute_error' returns NEGATIVE numbers. "
        "Flip the sign.",
    15: "Ridge penalises raw coefficient size, so it needs scaling to be "
        "fair. np.abs(...).max() on each coef_ array.",
}


def _f(x):
    return float(np.asarray(x).ravel()[0]) if np.ndim(x) else float(x)


def _check(name, fn, args, verify):
    try:
        got = fn(*args)
    except Exception as e:
        return "ERROR", "%s: %s" % (type(e).__name__, e)
    if got is None:
        return "TODO", "not attempted"
    try:
        ok, msg = verify(got)
    except Exception as e:
        return "ERROR", "your result broke the checker -- %s: %s" % (
            type(e).__name__, e)
    return ("PASS" if ok else "FAIL"), msg


def main():
    if "--hint" in sys.argv:
        n = int(sys.argv[sys.argv.index("--hint") + 1])
        print("\nHINT %d: %s\n" % (n, HINTS.get(n, "no hint for that drill")))
        return

    raw = load_raw()
    df = load_clean()
    df = df.copy()
    X, y = build_xy(df)

    from sklearn.linear_model import LinearRegression, Ridge
    from sklearn.model_selection import train_test_split, KFold, cross_val_score
    from sklearn.metrics import r2_score, mean_absolute_error
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)

    # ---- independently computed truth -------------------------------
    true_smoke = df.groupby("smoke")["bwt"].agg(["mean", "count", "std"])
    true_now = (df["smoke"] == "now").mean() * 100
    true_apply = df["bwt"].apply(classify_weight)
    num_cols = NUMERIC + ["bwt"]
    true_corr = df[num_cols].corr()["bwt"].drop("bwt").abs() \
                  .sort_values(ascending=False)
    base = LinearRegression().fit(Xtr, ytr)
    true_test_r2 = r2_score(yte, base.predict(Xte))
    true_train_r2 = r2_score(ytr, base.predict(Xtr))

    def v01(g):
        if not (abs(_f(g) - 3401.94) < 1e-6):
            return False, "d01(120) should be 3401.94, got %r" % (g,)
        a = d01_oz_to_grams(120, dp=3)
        b = d01_oz_to_grams(3401.94, reverse=True)
        c = d01_oz_to_grams(0)
        if abs(_f(a) - 3401.94) > 1e-9:
            return False, "dp=3 gave %r" % (a,)
        if abs(_f(b) - 120.0) > 0.01:
            return False, "reverse=True should give ~120.0, got %r" % (b,)
        if abs(_f(c)) > 1e-9:
            return False, "d01(0) should be 0.0, got %r" % (c,)
        return True, "defaults preserved, dp and reverse both work"

    def v02(g):
        cases = [(50, "Very Low"), (60, "Low"), (120, "Normal"), (145, "High")]
        for oz, want in cases:
            got = d02_classify(oz)
            if got != want:
                return False, "%s oz (%.2fg) should be %r, got %r" % (
                    oz, oz * 28.3495, want, got)
        if d02_classify(53) != "Low":
            return False, "53 oz = 1502.5g is Low, not %r -- branch order?" % (
                d02_classify(53),)
        return True, "all four bands correct, boundary at 1500 respected"

    def v03(g):
        need = {"count", "min", "max", "mean", "median"}
        if not need.issubset(set(g)):
            return False, "missing keys: %s" % sorted(need - set(g))
        if abs(g["mean"] - 109.375) > 1e-9 or g["count"] != 8:
            return False, "mean/count wrong: %r" % (g,)
        if abs(g["median"] - 115.0) > 1e-9:
            return False, "median of that list is 115.0, got %r" % (g["median"],)
        odd = d03_summary([3, 1, 2])
        if abs(odd["median"] - 2.0) > 1e-9:
            return False, "odd-length median failed: [3,1,2] -> %r" % (
                odd["median"],)
        return True, "even and odd length both correct"

    def v04(g):
        want = ["dht", "dwt"]
        if sorted(g) != want:
            return False, "expected %r, got %r" % (want, sorted(g))
        strict = d04_high_missing(raw, frac=0.05)
        if "inc" not in strict:
            return False, "frac=0.05 should also catch 'inc' (10%% missing)"
        return True, "threshold rule generalises, not hard-coded"

    def v05(g):
        if list(g.columns) != ["mean", "count", "std"]:
            return False, "columns should be ['mean','count','std'], got %r" % (
                list(g.columns),)
        if len(g) != 4:
            return False, "expected 4 smoking groups, got %d" % len(g)
        if abs(g.loc["now", "mean"] - true_smoke.loc["now", "mean"]) > 0.01:
            return False, "'now' mean is wrong"
        if int(g.loc["never", "count"]) != int(true_smoke.loc["never", "count"]):
            return False, "'never' count is wrong"
        return True, "matches groupby truth (now = %.2f oz)" % g.loc["now", "mean"]

    def v06(g):
        if abs(_f(g) - true_now) > 0.05:
            return False, "expected %.1f%%, got %r -- did you use != 'never'?" % (
                true_now, g)
        return True, "%.1f%% smoke during pregnancy (vs 55.5%% ever)" % _f(g)

    def v07(g):
        s = pd.Series(g).astype(str)
        if len(s) != len(true_apply):
            return False, "length %d, expected %d" % (len(s), len(true_apply))
        diff = (s.values != true_apply.values).sum()
        if diff:
            return False, "%d rows disagree with classify_weight -- check " \
                          "right=False on the 2500 boundary" % diff
        return True, "all 993 rows agree with classify_weight"

    def v08(g):
        if len(g) != 10:
            return False, "expected 10 rows, got %d" % len(g)
        if not (g["smoke"] == "now").all():
            return False, "not all rows are current smokers"
        if not (g["bwt"] < 100).all():
            return False, "some rows are >= 100 oz"
        if not g["bwt"].is_monotonic_increasing:
            return False, "not sorted lightest-first"
        return True, "10 lightest current-smoker births, %d-%d oz" % (
            g["bwt"].iloc[0], g["bwt"].iloc[-1])

    def v09(g):
        s = pd.Series(g)
        if "bwt" in s.index:
            return False, "you left bwt in -- it correlates 1.0 with itself"
        if s.index[0] != "gestation":
            return False, "strongest should be gestation, got %r" % (s.index[0],)
        if abs(_f(s.iloc[0]) - 0.426) > 0.01:
            return False, "gestation should be ~0.426, got %.3f" % _f(s.iloc[0])
        if not s.is_monotonic_decreasing:
            return False, "not sorted strongest-first"
        return True, "gestation .426 > height .197 > weight .164"

    def v10(g):
        s = pd.Series(g)
        if s.isna().any():
            return False, "%d NaN -- a bracket is missing from your dict" % (
                s.isna().sum())
        if not pd.api.types.is_numeric_dtype(s):
            return False, "not numeric, got dtype %s" % s.dtype
        if s.nunique() != 10:
            return False, "expected 10 distinct values, got %d" % s.nunique()
        pairs = df[["inc"]].assign(v=s.values).drop_duplicates()
        lo = pairs.loc[pairs["inc"] == "0-2500", "v"].iloc[0]
        hi = pairs.loc[pairs["inc"] == "20000-22500", "v"].iloc[0]
        if not lo < hi:
            return False, "ordering is broken: 0-2500 mapped above 20000-22500"
        return True, "10 brackets mapped, ordering preserved, no NaN"

    def v11(g):
        a, b, c, d = g
        if len(a) != 695 or len(b) != 298:
            return False, "expected 695/298, got %d/%d" % (len(a), len(b))
        if len(c) != 695 or len(d) != 298:
            return False, "y splits don't match X splits"
        return True, "695 train / 298 test"

    def v12(g):
        s = pd.Series(g)
        if len(s) != 5:
            return False, "expected 5 rows, got %d" % len(s)
        if not s.abs().is_monotonic_decreasing:
            return False, "not sorted by absolute value"
        if (s >= 0).all():
            return False, "you lost the signs -- return signed values"
        if "gestation" not in s.index:
            return False, "gestation should be in the top 5 once standardised"
        return True, "top standardised effect: %s = %+.2f oz/SD" % (
            s.index[0], s.iloc[0])

    def v13(g):
        tr, te = g
        if abs(_f(te) - true_test_r2) > 0.002:
            return False, "test R2 should be %.4f, got %.4f" % (
                true_test_r2, _f(te))
        if abs(_f(tr) - true_train_r2) > 0.002:
            return False, "train R2 should be %.4f, got %.4f" % (
                true_train_r2, _f(tr))
        return True, "train %.4f vs test %.4f -- gap of %.4f is the " \
                     "overfitting cost" % (_f(tr), _f(te), _f(tr) - _f(te))

    def v14(g):
        v = _f(g)
        if v < 0:
            return False, "that's negative -- sklearn negates error metrics, " \
                          "flip the sign"
        if not (10.0 < v < 15.0):
            return False, "expected roughly 12-13 oz, got %.4f" % v
        return True, "mean CV MAE = %.4f oz (%.0f g)" % (v, v * 28.3495)

    def v15(g):
        need = {"ols_r2", "ridge_r2", "ols_max_coef", "ridge_max_coef"}
        if not need.issubset(set(g)):
            return False, "missing keys: %s" % sorted(need - set(g))
        if g["ridge_max_coef"] >= g["ols_max_coef"]:
            return False, "Ridge should SHRINK the largest coefficient " \
                          "(ols %.2f vs ridge %.2f)" % (
                              g["ols_max_coef"], g["ridge_max_coef"])
        return True, "largest coef %.2f -> %.2f, R2 %.4f -> %.4f" % (
            g["ols_max_coef"], g["ridge_max_coef"],
            g["ols_r2"], g["ridge_r2"])

    drills = [
        (1, "oz_to_grams: dp + reverse", d01_oz_to_grams, (120,), v01),
        (2, "classify: add Very Low", d02_classify, (120,), v02),
        (3, "summary_stats + median", d03_summary,
         ([75, 88, 120, 130, 150, 60, 110, 142],), v03),
        (4, "drop columns >30% missing", d04_high_missing, (raw,), v04),
        (5, "groupby mean/count/std", d05_smoke_table, (df,), v05),
        (6, "current smokers, not ever", d06_current_smoker_pct, (df,), v06),
        (7, "pd.cut with right=False", d07_cut_categories, (df,), v07),
        (8, "filter + nsmallest(10)", d08_high_risk, (df,), v08),
        (9, "what correlates with bwt", d09_bwt_corr, (df,), v09),
        (10, "income as ordinal", d10_income_ordinal, (df,), v10),
        (11, "70/30 split, seed 0", d11_split, (X, y), v11),
        (12, "standardised coefficients", d12_std_coefs, (Xtr, ytr), v12),
        (13, "train vs test R2", d13_r2_gap, (Xtr, Xte, ytr, yte), v13),
        (14, "5-fold CV, neg MAE", d14_cv_mae, (X, y), v14),
        (15, "Ridge vs OLS", d15_ridge_vs_ols, (Xtr, Xte, ytr, yte), v15),
    ]

    print("\n" + "=" * 72)
    print("  LIVE-EDIT DRILLS".ljust(56) + "%d drills" % len(drills))
    print("=" * 72)

    tally = {"PASS": 0, "FAIL": 0, "ERROR": 0, "TODO": 0}
    part = {1: "PART 1", 4: "PART 2", 10: "PART 3"}
    for n, title, fn, args, verify in drills:
        if n in part:
            print("\n  -- %s %s" % (part[n], "-" * (62 - len(part[n]))))
        status, msg = _check(title, fn, args, verify)
        tally[status] += 1
        mark = {"PASS": "[ok]  ", "FAIL": "[X]   ",
                "ERROR": "[err] ", "TODO": "[ ]   "}[status]
        print("  %s%2d. %-30s %s" % (mark, n, title, msg))

    done = tally["PASS"]
    print("\n" + "-" * 72)
    print("  %d/%d passing   |   %d failing, %d errors, %d not attempted"
          % (done, len(drills), tally["FAIL"], tally["ERROR"], tally["TODO"]))
    if done == len(drills):
        print("  All clear. Now do them again with the guide closed, out loud.")
    elif tally["TODO"] == len(drills):
        print("  Start with drill 1. Hints: python drills.py --hint 1")
    print("-" * 72 + "\n")


if __name__ == "__main__":
    main()
