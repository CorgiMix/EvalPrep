"""
======================================================================
  THE DATA ITSELF
  Child Health and Development Studies (CHDS) / mosaicData::Gestation
======================================================================

Everything here is computed live from the actual file, not copied from
the assignment brief. Where the brief and the data disagree, this file
says so.

    python notebook/dataset.py --teach     provenance and what it is
    python notebook/dataset.py --facts     live numbers, computed now
    python notebook/dataset.py --traps     the six landmines
    python notebook/dataset.py --quiz      examiner questions
    python notebook/dataset.py --answers   ... with answers
======================================================================
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _data as D


PROVENANCE = """
WHAT THIS DATA ACTUALLY IS

  The Child Health and Development Studies. Pregnancies among women in
  the Kaiser Foundation Health Plan in Oakland, California, enrolled
  roughly 1960-1967. 1,236 births.

  This matters because every claim you make about the data is really a
  claim about THAT population. If asked "would your model generalise?",
  the answer is no, and here is the list of reasons:

    - one geography, one insurance scheme, one decade
    - 1960s obstetric practice, 1960s smoking norms (55% of these
      mothers are smokers, which is nothing like a modern cohort)
    - the columns dropped as CONSTANT tell you the sample was already
      filtered: every baby is MALE, every birth is a SINGLE fetus, and
      every outcome is a LIVE BIRTH

  That last point is the good one. `sex`, `plurality` and `outcome`
  were not dropped because they were useless -- they were dropped
  because they were constant, and they were constant because the
  sample was constructed that way. So your model cannot say anything
  about girls, about twins, or about stillbirths. Volunteering that is
  a strong move.

  Units are non-obvious and get asked:
    bwt        OUNCES (not grams, not pounds) -- this is why Q1.1 exists
    gestation  DAYS (not weeks) -- 280 days is the 40-week textbook term
    height     INCHES        weight  POUNDS (pre-pregnancy)
    age, dage  YEARS

  A useful sanity anchor: mean bwt is 119 oz, which is about 3,374 g,
  or 7 lb 7 oz. That is a completely normal mean birth weight, which
  tells you the data is sane.


THE THREE SHAPES, AND WHERE THEY COME FROM

  24 columns   the raw CSV as downloaded
  16 columns   after Q2.1's GIVEN starter code drops 8 and renames 3
  14 columns   after Q2.2 drops dht and dwt
  993 rows     after Q2.2 drops rows with any remaining NaN

  Dropped by the starter code, with reasons:
    rownames    a redundant index written by R
    id          a row identifier, no predictive content
    date        the date of birth, not modelled here
    plurality   CONSTANT: always a single fetus
    outcome     CONSTANT: always a live birth
    sex         CONSTANT: every baby in this sample is male
    time        breaks `smoke` down further -- redundant with smoke
    number      breaks `smoke` down further -- redundant with smoke

  Renamed: wt -> bwt, ht -> height, wt.1 -> weight.
  The rename exists because the raw file has BOTH the baby's weight
  and the mother's weight, and R's read of the duplicate name produced
  `wt` and `wt.1`. Knowing which is which is the point: `bwt` is the
  target, `weight` is a feature.
"""


TRAPS = """
THE SIX LANDMINES
=================

1. THE BRIEF'S Q1.3 EXPECTED OUTPUT IS WRONG.

     The brief says   Low: 2, Normal: 4, High: 2
     The truth is     Low: 3, Normal: 3, High: 2

   88 oz  ->  88 * 28.3495  =  2494.76 g  ->  below 2500  ->  "Low".
   The brief counted 88 as Normal. Your code, written correctly, will
   disagree with the printed expected output.

   Do NOT quietly change your code to match. Say: "my function returns
   Low for 88 ounces because 2494.76 is under the 2500 threshold; I
   believe the expected output in the brief is off by one here." That
   is the single highest-value sentence available to you in Part 1.


2. ROUNDING CAN FLIP A CATEGORY.

     88.1849 oz  ->  true value 2499.9978 g   (Low)
                 ->  round(.., 2) gives 2500.00 g  ->  "Normal"

   Q1.1 says round to 2dp, and Q1.2 says use Q1.1 inside it. Following
   both instructions literally makes classification depend on a
   rounding artefact in a razor-thin band. The exact thresholds are
   2500/28.3495 = 88.18498 oz and 4000/28.3495 = 141.09596 oz.

   The fix is to classify on the UNROUNDED grams and round only for
   display. Whether or not you change the code, naming this is what
   demonstrates you understand your own function.


3. `marital` COEFFICIENTS ARE NOISE, AND THE BASELINE IS WORSE.

     married            978
     legally separated   10
     never married        3
     divorced             2   <-- and get_dummies drops this one

   drop_first=True drops the ALPHABETICALLY FIRST category. For
   marital that is "divorced", which has TWO observations. So every
   marital coefficient in your model -- including the eye-catching
   marital_never married = -12.00 -- is measured against a baseline of
   two people, using three people.

   That coefficient is not a finding. It is noise with a large font.


4. `ded_Trade school HS unclear` HAS FIVE OBSERVATIONS.

   Its coefficient is -10.73, fourth largest in the model. Same story:
   a large coefficient estimated from almost no data. When you present
   "the biggest coefficients", the honest framing is that the top of
   that list is dominated by rare categories, not by strong effects.


5. RAW COEFFICIENTS ARE NOT COMPARABLE, AND THE RANKING FLIPS.

   The model prints drace_mex = 14.92 as the largest coefficient and
   gestation = 0.44 as one of the smallest. That is a UNITS artefact:
   a dummy moves 0 to 1, while gestation moves in days.

   Multiply each coefficient by its feature's standard deviation and
   the ranking changes completely:

     feature        raw      per SD    rank
     gestation      0.44      6.85     35th -> 1st
     drace_white   12.30      5.46      2nd -> 2nd
     smoke_now     -7.64     -3.73      7th -> 3rd
     drace_mex     14.92      2.61      1st -> 6th

   Gestation is the strongest predictor in the model and it looks like
   the weakest in the printout. This is the single best thing you can
   say in Q3.3.


6. `inc` IS ORDINAL, ONE-HOT ENCODED, AND ITS BRACKETS OVERLAP.

   Income is ordered -- 0-2500 is less than 2500-5000 -- but
   get_dummies throws that ordering away and produces nine unordered
   flags. The model cannot know 20000-22500 is bigger than 0-2500.

   Worse, the brackets are not a clean partition. The categories
   include BOTH "15000+" (20 rows) AND "15000-17500", "17500-20000"
   and "20000-22500". A row coded 15000+ overlaps three other
   brackets, which is a genuine data quality defect in the source, not
   something you introduced.

   Also note the dummies sort ALPHABETICALLY, so inc_10000-12500 comes
   before inc_2500-5000 in your column list. Ten thousand sorts before
   two thousand five hundred as text. Say that out loud if the column
   order is questioned.
"""


EXAMINER = [
    ("Where does this data come from and who is in it?",
     """The Child Health and Development Studies: pregnancies in the
        Kaiser Foundation Health Plan in Oakland, California, around
        1960 to 1967. 1,236 births. One region, one insurer, one
        decade."""),

    ("Three columns were dropped as constant. What does that tell you "
     "about the sample?",
     """That it was pre-filtered. sex is constant because every baby is
        male, plurality because every birth is a single fetus, outcome
        because every birth is live. So the model cannot speak to
        girls, twins, or stillbirths -- a real limit on
        generalisation."""),

    ("What are the units of bwt and gestation?",
     """Ounces and days. Mean bwt is 119 oz, about 3,374 g or 7 lb 7 oz,
        which is a normal mean birth weight. Mean gestation is 279 days
        against the 280-day textbook term."""),

    ("Why is there both a `weight` and a `bwt` column?",
     """The raw file holds the baby's weight and the mother's
        pre-pregnancy weight. R's duplicate-name handling produced wt
        and wt.1, and the starter code renames them to bwt (the target)
        and weight (a feature). Confusing them would leak the
        target."""),

    ("How many rows did you lose in cleaning, and was that acceptable?",
     """243 of 1,236, so 19.7%. Acceptable only if the missingness is
        unrelated to birth weight. It is worth checking rather than
        assuming -- if income were missing more often among poorer
        mothers, dropping those rows biases the sample."""),

    ("Why drop dht and dwt as columns rather than dropping their rows?",
     """Because they are missing in about 40% of rows. Dropping rows
        instead leaves 593 rows instead of 993 -- you would lose 52% of
        the data to keep two columns. Dropping the columns saves 400
        rows."""),

    ("Which pair of numeric features is most correlated?",
     """Mother's age and father's age, r = 0.83. Partners tend to be
        close in age, which is assortative mating, not biology."""),

    ("And the least correlated?",
     """Mother's height and father's age, r = 0.009 -- essentially zero.
        There is no plausible mechanism linking how tall a woman is to
        how old her partner is."""),

    ("Which feature correlates most with the target?",
     """gestation, r = 0.43. Nothing else clears 0.20. Height is 0.20
        and weight is 0.16; parity, age and dage are all under 0.07."""),

    ("Are there repeated mothers in this data?",
     """No. All 1,236 id values are unique, so every row is a distinct
        pregnancy. That is worth checking, because if mothers repeated
        you would need grouped cross-validation to stop the same
        mother appearing in both train and test."""),

    ("Why are so many columns float64 when they hold whole numbers?",
     """NaN is a float, so any integer column with a missing value is
        promoted to float64. gestation, age, height, weight, dage and
        the father's columns are all float64 for that reason, while
        bwt and parity -- which have no missing values -- stay
        int64."""),

    ("55% of these mothers smoke. Is that plausible?",
     """For a 1960s American cohort, yes -- smoking during pregnancy was
        common and not yet strongly discouraged. It is wildly unlike a
        modern cohort, which is one more reason the model does not
        transfer to today."""),
]


def facts():
    df = D.load_clean()
    raw = D.load_raw()
    X, y = D.build_xy(df)

    print()
    print("  SHAPES")
    print("    raw (after the given starter code) : %s" % (raw.shape,))
    print("    clean (after Q2.2)                 : %s" % (df.shape,))
    print("    X, y (after Q3.1)                  : %s  %s" % (X.shape, y.shape))
    print("    rows lost                          : %d of %d = %.1f%%"
          % (len(raw) - len(df), len(raw), 100 * (len(raw) - len(df)) / len(raw)))
    print("    rows if dht/dwt kept as columns    : %d  (you would lose %.0f%%)"
          % (len(raw.dropna()), 100 * (1 - len(raw.dropna()) / len(raw))))

    print()
    print("  NUMERIC SUMMARY (the clean 993)")
    desc = df[D.NUMERIC + ["bwt"]].describe().T[["mean", "std", "min", "max"]]
    print(desc.round(2).to_string().replace("\n", "\n    ").rjust(4))

    print()
    print("  TARGET ANCHORS")
    print("    mean bwt : %.2f oz = %.0f g = %d lb %.0f oz"
          % (y.mean(), y.mean() * 28.3495, int(y.mean() // 16), y.mean() % 16))
    print("    sd bwt   : %.2f oz" % y.std())
    print("    range    : %d to %d oz" % (y.min(), y.max()))

    print()
    print("  CATEGORY COUNTS, AND WHICH ONE get_dummies DROPS")
    for c in D.CATEGORICAL:
        vc = df[c].value_counts()
        base = sorted(df[c].unique())[0]
        print("    %-8s baseline=%-36r n=%d" % (c, base, vc[base]))
        if vc[base] < 40:
            print("             ^ only %d rows in the baseline -- every %s "
                  "coefficient is measured against it" % (vc[base], c))

    print()
    print("  CORRELATION WITH THE TARGET")
    corr = df[D.NUMERIC + ["bwt"]].corr()["bwt"].drop("bwt")
    for k, v in corr.abs().sort_values(ascending=False).items():
        print("    %-10s %.4f" % (k, corr[k]))

    print()
    print("  STRONGEST AND WEAKEST FEATURE PAIRS")
    import numpy as np
    c2 = df[D.NUMERIC].corr()
    m = c2.where(~np.eye(len(c2), dtype=bool)).abs().stack()
    m = m[[i < j for i, j in m.index]]
    hi, lo = m.idxmax(), m.idxmin()
    print("    highest |r| : %s vs %s = %.4f" % (hi[0], hi[1], m.max()))
    print("    lowest  |r| : %s vs %s = %.4f" % (lo[0], lo[1], m.min()))

    print()
    print("  THE MODEL, END TO END")
    Xtr, Xte, ytr, yte = D.split(X, y)
    mdl = D.fit_linear(Xtr, ytr)
    mt = D.metrics(mdl, Xte, yte)
    from sklearn.metrics import r2_score
    print("    intercept  : %.4f" % mdl.intercept_)
    print("    test  MAE %.4f   RMSE %.4f   R2 %.4f"
          % (mt["MAE"], mt["RMSE"], mt["R2"]))
    print("    train R2   : %.4f   (gap = %.4f -> mild overfit)"
          % (r2_score(ytr, mdl.predict(Xtr)),
             r2_score(ytr, mdl.predict(Xtr)) - mt["R2"]))

    import pandas as pd
    co = pd.Series(mdl.coef_, index=X.columns)
    std = co * Xtr.std()
    print()
    print("    top 5 by RAW |coef|          top 5 by SD-SCALED |coef|")
    a = co.reindex(co.abs().sort_values(ascending=False).index).head(5)
    b = std.reindex(std.abs().sort_values(ascending=False).index).head(5)
    for (k1, v1), (k2, v2) in zip(a.items(), b.items()):
        print("      %-28s %6.2f   %-16s %6.2f" % (k1, v1, k2, v2))
    print()
    print("    ^ gestation is 1st on the right and 35th on the left.")
    print("      Same model. The left column is a units artefact.")


def main():
    argv = sys.argv
    if "--facts" in argv:
        D.head("THE DATA :: LIVE NUMBERS")
        facts()
        return
    if "--traps" in argv:
        D.head("THE DATA :: THE SIX LANDMINES")
        print(TRAPS)
        return
    if "--quiz" in argv or "--answers" in argv:
        D.head("THE DATA :: EXAMINER")
        D.quiz(EXAMINER, show="--answers" in argv)
        return
    D.head("THE DATA :: PROVENANCE")
    print(PROVENANCE)
    print()
    print("  next:  python notebook/dataset.py --facts")
    print("         python notebook/dataset.py --traps")
    print("         python notebook/dataset.py --answers")
    print()


if __name__ == "__main__":
    main()
