"""
======================================================================
  PART 2 -- Data Loading & Preprocessing with Pandas   (20 points)
======================================================================

    python notebook/part2.py --teach          all six questions
    python notebook/part2.py --teach 2.6      just that one
    python notebook/part2.py --trace 2.3      watch the numbers
    python notebook/part2.py --quiz / --answers
    python notebook/part2.py                  mark your live edits

Q2.6 alone is 6 points and asks for written hypotheses -- it is the
biggest single item in Part 2. Q2.3 contains the best interpretive
observation in the whole of Part 2. Both are flagged below.
======================================================================
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
import _data as D


STATEMENTS = {
    "2.1": """Q2.1 -- Load and Inspect the Dataset (2 points)

  Load the CSV into a DataFrame `df`. The starter code is GIVEN and
  already drops rownames, id, date, plurality, outcome, sex, time and
  number, and renames wt -> bwt, ht -> height, wt.1 -> weight.

  You add code to display:  the first 5 rows; the shape; the column
  names and data types.

  Expected shape: (1236, 16)""",

    "2.2": """Q2.2 -- Missing Values (2 points)

  1. Count missing values per column and print the result.
  2. dht and dwt (father's height/weight) are missing in ~40% of rows.
     Dropping those rows would gut the dataset, so DROP THESE TWO
     COLUMNS ENTIRELY.
  3. Drop all remaining rows containing any missing value; save back
     to df.
  4. Print the new shape.

  Expected shape afterwards: (993, 14)""",

    "2.3": """Q2.3 -- Exploratory Statistics (4 points)

  1. Print descriptive statistics for all numeric columns.
  2. Print the percentage of mothers who smoke. `smoke` is categorical
     (never / now / until current pregnancy / once did, not now) --
     treat any value other than "never" as a smoker.
  3. Print average bwt split by smoking status, all four categories.

  Expected (example):
     Smokers: 55.5%
     never 122.55 | now 113.40 | once did, not now 123.20
     until current pregnancy 122.64""",

    "2.4": """Q2.4 -- Feature Engineering (2 points)

  1. Add `bwt_grams`, converting bwt to grams with your Q1.1 function.
  2. Add `weight_category` by applying your Q1.2 function to bwt.
  3. Print the value counts of weight_category.

  Expected: Normal 839 | High 101 | Low 53""",

    "2.5": """Q2.5 -- Filter and Sort (4 points)

  1. Build `high_risk`: rows where the mother is a SMOKER AND bwt is
     below 100 oz.
  2. Sort by bwt ascending and print the first 5 rows.
  3. Print how many high-risk births were found.

  Expected: High-risk births found: 98""",

    "2.6": """Q2.6 -- Correlation matrix (6 points)

  Select the numeric feature columns and compute the correlation
  matrix.
  1. Display the full matrix.
  2. Identify the pair with the HIGHEST absolute correlation and the
     pair with the LOWEST (closest to 0).
  3. Write a short paragraph for each pair proposing a biological or
     social hypothesis, backed by clinical, physiological or
     demographic literature.""",
}


LESSONS = {
    "2.1": """
THE STARTER CODE IS GIVEN, WHICH MEANS YOU WILL BE ASKED ABOUT IT

  You did not write the drops, so the assessor will check you can
  justify them. Three groups:

    CONSTANT      plurality (always single fetus), outcome (always live
                  birth), sex (every baby here is male). A column with
                  one value has zero variance and cannot predict
                  anything. More importantly it tells you the SAMPLE
                  WAS PRE-FILTERED -- see dataset.py.
    REDUNDANT     rownames (R's index), id (a row label).
    SUBSUMED      time and number just break `smoke` down further;
                  keeping them alongside smoke would encode the same
                  information three times.
    NOT DROPPED   date. It is dropped here as unused, not as useless --
                  a season-of-birth effect is real in the literature.

  The rename matters more than it looks: the raw file has the BABY's
  weight and the MOTHER's weight, which R's duplicate-name handling
  turned into `wt` and `wt.1`. They become `bwt` (the target) and
  `weight` (a feature). Mixing them up leaks the target.

WHAT `.dtypes` IS ACTUALLY TELLING YOU

  gestation, age, height, weight, dage are float64 even though every
  value is a whole number. bwt and parity are int64.

  The reason is NaN. NaN is a floating-point value, so a column with
  any missing entry cannot stay int64 -- pandas promotes it to
  float64. bwt and parity have zero missing values, so they stay int.

  So the dtype listing is secretly a missing-value report, and saying
  that out loud in Q2.1 sets up Q2.2 beautifully.

  (On very recent pandas the text columns show as `str` rather than
  `object`. Same thing; the dtype was renamed.)

df.info() GIVES YOU SHAPE, DTYPES AND NON-NULL COUNTS AT ONCE

  Print head(), shape and dtypes because the question asks for them --
  then mention info() collapses all three plus memory usage.

THE STATEFULNESS HAZARD -- THIS WILL BITE YOU LIVE

  Q2.2 drops columns from df. If you then re-run the Q2.2 cell, the
  columns are already gone and you get

      KeyError: ['dht', 'dwt'] not found in axis

  Nothing is wrong with your code. The cell is simply not idempotent.
  In the live session, if anything looks broken, use Restart Kernel
  and Run All rather than re-running one cell. Knowing this in advance
  turns a panic into a shrug.
""",

    "2.2": """
THE NUMBERS, AND THE ARGUMENT THEY MAKE FOR YOU

      dht missing 492 of 1236 = 39.8%
      dwt missing 499 of 1236 = 40.4%

  Two options:
      drop the two COLUMNS  ->  993 rows survive  (lose 19.7%)
      drop the NaN ROWS     ->  593 rows survive  (lose 52.0%)

  So keeping the father's height and weight costs you 400 rows. That
  is the trade, quantified. Do not say "about 40% are missing so we
  drop them" -- say "keeping them would cost 400 of 993 rows, and two
  columns are not worth 40% of the sample."

  Being able to produce the 593 on demand is the difference between
  reciting the instruction and having understood it.

COMPLETE-CASE ANALYSIS, AND ITS ONE ASSUMPTION

  dropna() on rows is called listwise deletion or complete-case
  analysis. It is unbiased ONLY if the data are Missing Completely At
  Random -- missingness unrelated to anything, including the values
  themselves.

  Is that plausible here? `inc` is missing 124 times. Income is
  exactly the kind of field people decline to report, and refusal
  probably correlates with actual income. If poorer mothers are more
  likely to be missing, dropping them makes the surviving sample
  richer than the population, and every downstream estimate inherits
  that bias.

  So the honest answer is: the assignment tells me to drop, and I do,
  but the assumption is MCAR and I doubt it holds for `inc`.

  The vocabulary, if pushed:
      MCAR  missing for reasons unrelated to anything -> dropping is safe
      MAR   missing depends on OBSERVED variables -> imputation can fix it
      MNAR  missing depends on the UNOBSERVED value itself -> hardest case

WHAT YOU WOULD DO INSTEAD

  - median imputation for numerics, mode for categoricals -- cheap,
    but it shrinks variance and weakens correlations
  - add a MISSING indicator column, so the model can learn from the
    fact of absence
  - treat "missing" as its own category for the categorical columns
  - iterative / model-based imputation, which is the principled option

  If asked "why not just impute dht?", the answer is that with 40%
  missing you would be inventing more of the column than you observed.

ORDER OF OPERATIONS MATTERS

  Drop the COLUMNS first, then drop the ROWS. Reversed, you would drop
  every row missing a father's measurement before you ever removed the
  columns, and you would land on 593. Same two instructions, wrong
  order, 400 rows gone.
""",

    "2.3": """
THE BEST INTERPRETIVE OBSERVATION IN PART 2 IS HIDING IN THIS TABLE

      never                      122.55
      now                        113.40
      once did, not now          123.20
      until current pregnancy    122.64

  Look at it properly. Three of the four categories sit within one
  ounce of each other around 122-123. Only `now` is different, and it
  is different by about NINE OUNCES.

  So the effect is not "smoking lowers birth weight". It is "smoking
  DURING THIS PREGNANCY lowers birth weight". Women who quit -- even
  those who quit only at the start of this pregnancy -- have babies
  indistinguishable from never-smokers. "Once did, not now" is
  actually the HIGHEST of the four.

  That is a causal-looking, dose-and-timing story, and it is the kind
  of interpretation the live assessment is explicitly grading.

WHICH MAKES THE QUESTION'S OWN DEFINITION QUESTIONABLE

  The brief says treat anything other than "never" as a smoker. That
  gives 55.5%. But it lumps the 87 women who quit long ago and the 76
  who quit at conception in with the 388 who currently smoke -- and we
  have just seen those groups behave like never-smokers.

  So the binary variable DILUTES the effect. If you must have a
  binary, `smoke == "now"` is the meaningful one (39.1% of the
  sample). Say this. It shows you read the numbers rather than
  executing the instruction.

  Do the calculation the way the brief asks -- 55.5% -- and then add
  the caveat. Never silently substitute your own definition.

HOW TO COMPUTE A PERCENTAGE OF A CONDITION

      (df["smoke"] != "never").mean() * 100

  A boolean Series has True as 1 and False as 0, so its MEAN is the
  proportion. This is much better than sum()/len() and being able to
  explain why -- booleans are ints under the hood -- is a small,
  cheap win.

describe() -- KNOW WHAT IT LEAVES OUT

  df.describe() covers only numeric columns by default. The seven
  categorical columns are silently absent. describe(include="all")
  adds them, with count / unique / top / freq instead of quartiles.

  If asked "is that all your columns?", the answer is no, and knowing
  it without checking is the tell.
""",

    "2.4": """
TWO WAYS TO BUILD bwt_grams, AND THEY ARE NOT EQUIVALENT

      df["bwt_grams"] = df["bwt"].apply(oz_to_grams)     # calls Python 993x
      df["bwt_grams"] = (df["bwt"] * 28.3495).round(2)   # vectorised

  The brief says to use your Q1.1 function, so use apply. But know
  that apply is a Python-level loop -- roughly 10 to 100 times slower
  than the vectorised form at scale. At 993 rows it is irrelevant; at
  10 million it is the whole runtime.

  weight_category genuinely needs apply, because classify_weight
  contains branching. The vectorised equivalent would be pd.cut:

      pd.cut(grams, bins=[0, 2500, 4000, np.inf],
             labels=["Low", "Normal", "High"], right=False)

  right=False makes each interval [lo, hi) -- closed on the left, open
  on the right -- which is exactly the WHO convention: 2500 belongs to
  Normal, not Low. Getting `right` wrong flips both boundaries.

  Offering pd.cut as the vectorised alternative, with the right=False
  detail, is a strong Q2.4 answer.

THE COUNTS, AND WHAT THEY MEAN CLINICALLY

      Normal 839    High 101    Low 53

  53 of 993 is 5.3% low birth weight. Real-world rates run 6-8%, so
  this cohort is slightly better than typical -- consistent with an
  insured population that had antenatal care.

THE TARGET LEAKAGE YOU ARE BEING SET UP FOR

  Both new columns are DERIVED FROM bwt, which is the target.

      bwt_grams        is bwt times a constant -- a perfect predictor
      weight_category  is bwt discretised -- nearly perfect

  Leaving either in X would give an R-squared near 1.0 and a model
  that has learned nothing. Q3.1 tells you to drop them, and the
  reason is target leakage.

  Say the phrase "target leakage" in Q2.4, before Q3.1 asks. Getting
  there first is worth more than answering when prompted.
""",

    "2.5": """
BOOLEAN MASKS: & AND |, NEVER and AND or

      mask = (df["smoke"] != "never") & (df["bwt"] < 100)
      high_risk = df[mask]

  Two rules, and both are asked about:

  1. Use & and |, not `and` / `or`. Python's `and` calls bool() on
     its operands, and bool() of a multi-element Series is ambiguous,
     so you get
         ValueError: The truth value of a Series is ambiguous
     & is the element-wise operator.

  2. PARENTHESES ARE MANDATORY. In Python, & binds TIGHTER than !=
     and <. Without the brackets,
         df["smoke"] != "never" & df["bwt"] < 100
     parses as "never" & df["bwt"] first, and blows up. This is the
     single most common pandas error in a live session.

WHICH DEFINITION OF SMOKER?

  Q2.3 told you: anything other than "never". Stay consistent with it
  here -- and note, again, that Q2.3's own table says the effect lives
  in `now`. With `now` only, the count drops from 98 to 85.

  Consistency is what is graded. Flag the alternative, do not silently
  switch.

SORTING

      high_risk.sort_values("bwt").head()

  sort_values returns a NEW frame; it does not sort in place unless
  you pass inplace=True. `ascending=True` is the default, so passing
  it is optional -- but the question says ascending, so write it and
  be explicit.

  nsmallest(5, "bwt") does the same job in one call and is O(n) rather
  than O(n log n). Worth mentioning.

SettingWithCopyWarning -- KNOW THIS BY NAME

  df[mask] can return a VIEW. If you later assign into it,

      high_risk["flag"] = 1

  pandas may warn that you are modifying a copy, and the write may or
  may not land on the original. The fix is to be explicit:

      high_risk = df[mask].copy()

  You are not assigning here, so you will not trigger it -- but
  naming the warning and saying .copy() prevents it is a strong signal
  that you have actually used pandas rather than read about it.
""",

    "2.6": """
THE ANSWERS, COMPUTED (do not guess these)

  Over the six numeric FEATURES:

      HIGHEST |r| :  age  vs  dage   =  0.8275
      LOWEST  |r| :  dage vs  height =  0.0089

  If you include bwt in the matrix, the ordering above is unchanged,
  and the strongest link to the TARGET is:

      gestation vs bwt = 0.4265

  Nothing else clears 0.20 against bwt (height 0.20, weight 0.16,
  dage 0.06, age 0.05, parity 0.03).

  The full ranking of the feature-feature pairs, for context:
      age/dage 0.83, age/parity 0.51, parity/dage 0.47,
      height/weight 0.44, weight/dage 0.19, weight/parity 0.16 ...

HOW TO FIND THE EXTREMES WITHOUT TRIPPING OVER THE DIAGONAL

  The diagonal is all 1.0 and every pair appears twice. So:

      c = df[cols].corr()
      m = c.where(~np.eye(len(c), dtype=bool)).abs().stack()
      m = m[[i < j for i, j in m.index]]      # keep one of each pair
      m.idxmax(), m.idxmin()

  If you forget to mask the diagonal, idxmax returns a variable paired
  with itself at r = 1.0. That is the classic wrong answer, and the
  assessor is watching for it.

PART 3 OF THE QUESTION IS WRITTEN, AND IT IS WORTH THE MOST
-----------------------------------------------------------

  HYPOTHESIS FOR age vs dage, r = 0.83

    This is ASSORTATIVE MATING -- people partner with people close to
    themselves on age, education and background. It is one of the most
    consistently replicated findings in demography; age homogamy is
    documented across essentially every society studied, with a modal
    spousal age gap of two to three years and the husband typically
    slightly older. Here mean maternal age is 27.3 and mean paternal
    age is 30.2, a gap of 2.9 years, which sits exactly where the
    demographic literature would put it.

    Crucially this is SOCIAL, not biological. There is no physiological
    mechanism by which a mother's age constrains a father's. The
    correlation arises from partner selection, which means it is a
    property of who forms couples, not of pregnancy.

    The modelling consequence matters more than the fact: two features
    correlated at 0.83 are largely redundant. In a linear model this
    is MULTICOLLINEARITY -- the coefficients on age and dage become
    unstable and can flip sign, because the model cannot tell which of
    the two is doing the work. It does not hurt PREDICTION, but it
    destroys INTERPRETATION of those two coefficients.

  HYPOTHESIS FOR dage vs height, r = 0.009

    Essentially zero, and it should be. Adult stature is set by
    genetics and childhood nutrition, with heritability estimates
    around 0.8 in well-nourished populations; it is fixed by the end
    of puberty, when the epiphyseal growth plates fuse. A partner's
    age is determined by the year he was born and by mate selection.
    There is no causal pathway in either direction and no plausible
    common cause.

    Note the ASYMMETRY that makes this interesting: mother's age and
    father's age correlate at 0.83 through mate selection, but
    mother's HEIGHT and father's age do not correlate at all. So
    assortative mating operates strongly on age and, in this sample,
    not detectably between one partner's height and the other's age.

    A near-zero correlation is a real finding, not an absence of one:
    it says the two variables carry INDEPENDENT information, which is
    exactly what you want from features in a model.

  AND IF THEY ASK ABOUT gestation vs bwt, r = 0.43

    Mechanistic and directional. Fetal weight gain in the third
    trimester runs at roughly 200 grams per week, so a baby delivered
    at 38 weeks has had two fewer weeks of accretion than one at 40.
    Preterm birth is the dominant cause of low birth weight worldwide.
    That r = 0.43 -- rather than 0.9 -- reflects that gestational age
    sets the TIME available while maternal nutrition, placental
    function, smoking and genetics set the RATE.

TWO CAVEATS TO HAVE READY

  1. Pearson measures LINEAR association only. A perfect U-shaped
     relationship has r near 0. If asked whether r = 0.009 proves
     independence: no, it proves no linear relationship. Spearman
     would catch a monotone non-linear one.

  2. Correlation is not causation, and here you can prove you mean it:
     age/dage at 0.83 has no causal link in either direction. It is
     the cleanest possible example, and it is in your own data.
""",
}


EXAMINER = [
    ("2.1", "Why were sex, plurality and outcome dropped?",
     """They are constant -- every baby is male, every birth a single
        fetus, every outcome live. Zero variance means zero predictive
        content. More importantly it reveals the sample was
        pre-filtered, so the model cannot generalise to girls, twins or
        stillbirths."""),

    ("2.1", "Why is gestation float64 when every value is a whole "
            "number?",
     """Because it has 13 missing values and NaN is a float, so pandas
        promotes the column. bwt and parity have no missing values and
        stay int64 -- so the dtype listing is really a missing-value
        report."""),

    ("2.1", "You re-run the Q2.2 cell and get KeyError on dht and dwt. "
            "What happened?",
     """Nothing is wrong with the code -- the cell is not idempotent.
        The columns were dropped on the first run and are already gone.
        Restart the kernel and run all rather than re-running one
        cell."""),

    ("2.2", "Why drop dht and dwt as columns instead of dropping their "
            "rows?",
     """Because dropping the rows leaves 593 rows instead of 993 -- 52%
        of the data gone to keep two columns. Dropping the columns
        costs 19.7%. Two features are not worth 400 rows."""),

    ("2.2", "What assumption does dropna make, and does it hold here?",
     """Complete-case analysis is unbiased only under Missing Completely
        At Random. I doubt it holds for `inc`, which is missing 124
        times -- income non-response usually correlates with actual
        income, so the surviving sample may be systematically
        richer."""),

    ("2.2", "What would you do instead of dropping?",
     """Median or mode imputation, or better, add a missing-indicator
        column so the model can use the fact of absence. For dht I
        would not impute at all -- with 40% missing you would be
        inventing more of the column than you observed."""),

    ("2.2", "Does the order of the two drops matter?",
     """Yes. Columns first, then rows. Reversed, you drop every row
        missing a father's measurement before removing the columns and
        land on 593 instead of 993."""),

    ("2.3", "You report 55.5% smokers. Is that the right number to "
            "report?",
     """It is the number the brief asks for. But it lumps 87 long-ago
        quitters and 76 who quit at conception in with 388 current
        smokers, and the four-category table shows the first two groups
        behave like never-smokers. `smoke == "now"`, at 39.1%, is the
        meaningful binary."""),

    ("2.3", "Interpret the birth weight by smoking status table.",
     """Three of the four categories sit within one ounce of each other
        near 122-123. Only `now` differs, at 113.40, about nine ounces
        lower. So the effect is specific to smoking DURING the
        pregnancy -- women who quit, even at conception, look like
        never-smokers. 'Once did, not now' is actually the highest of
        the four."""),

    ("2.3", "Why does (series != 'never').mean() give a percentage?",
     """Booleans are integers in Python -- True is 1, False is 0 -- so
        the mean of a boolean Series is the proportion of True.
        Multiply by 100."""),

    ("2.3", "Does describe() cover all your columns?",
     """No. By default it covers numeric columns only, so the seven
        categorical columns are silently absent.
        describe(include='all') adds them with count, unique, top and
        freq."""),

    ("2.4", "Why use apply rather than a vectorised multiply?",
     """The brief says to reuse the Q1.1 function. apply is a Python-level
        loop and is roughly 10 to 100 times slower, which is irrelevant
        at 993 rows. The vectorised form is (df.bwt * 28.3495).round(2),
        and for the categories, pd.cut with right=False."""),

    ("2.4", "Why right=False in pd.cut?",
     """It makes each bin closed on the left and open on the right, so
        2500 falls in Normal rather than Low. That matches the WHO
        table. right=True would flip both boundaries."""),

    ("2.4", "Is there a problem with these two new columns?",
     """Yes -- both are derived from the target. bwt_grams is bwt times a
        constant and weight_category is bwt discretised. Leaving either
        in X is target leakage and would give a near-perfect R-squared
        from a model that learned nothing. Q3.1 drops them for exactly
        that reason."""),

    ("2.5", "Why & instead of and?",
     """`and` calls bool() on its operands and bool() of a multi-element
        Series is ambiguous, raising ValueError. & is the element-wise
        operator."""),

    ("2.5", "Why the parentheses?",
     """Because & binds tighter than the comparison operators. Without
        brackets, df.smoke != 'never' & df.bwt < 100 evaluates
        'never' & df.bwt first and fails. It is the most common live
        pandas error."""),

    ("2.5", "What is SettingWithCopyWarning?",
     """df[mask] can return a view rather than a copy. Assigning into it
        may not propagate to the original, so pandas warns. Writing
        df[mask].copy() makes the intent explicit and removes the
        ambiguity."""),

    ("2.6", "Which pair is most correlated, and why?",
     """Mother's age and father's age, r = 0.83. Assortative mating --
        people partner with people close to their own age. Mean
        maternal age 27.3, mean paternal 30.2, a 2.9-year gap, exactly
        where the demographic literature puts it. It is social, not
        biological."""),

    ("2.6", "Which pair is least correlated, and is that meaningful?",
     """Father's age and mother's height, r = 0.009. Adult stature is set
        by genetics and childhood nutrition and fixed when the growth
        plates fuse at the end of puberty; a partner's age is set by
        birth year and mate selection. No pathway either way. A
        near-zero correlation is a real finding -- it says the features
        carry independent information."""),

    ("2.6", "Does r = 0.009 prove the two are independent?",
     """No. Pearson measures LINEAR association only. A perfect U-shape
        would also give r near zero. Spearman would catch a monotone
        non-linear relationship."""),

    ("2.6", "What does the 0.83 mean for your Part 3 model?",
     """Multicollinearity. age and dage are largely redundant, so their
        coefficients become unstable and can flip sign -- the model
        cannot attribute the shared effect. It does not hurt prediction,
        but it destroys the interpretation of those two
        coefficients."""),

    ("2.6", "A common mistake here returns r = 1.0. What is it?",
     """Forgetting to mask the diagonal. Every variable correlates
        perfectly with itself, so idxmax on the raw matrix returns a
        variable paired with itself."""),
]


# ======================================================================
#  REFERENCE SOLUTIONS
# ======================================================================

def q21_inspect(df):
    return {"shape": df.shape, "n_float": int((df.dtypes == "float64").sum())}


def q22_missing(df):
    return df.isna().sum()


def q23_smoker_pct(df):
    return (df["smoke"] != "never").mean() * 100


def q23_bwt_by_smoke(df):
    return df.groupby("smoke")["bwt"].mean().round(2)


def q24_categories(df):
    return df["bwt"].apply(D.classify_weight).value_counts()


def q25_high_risk(df):
    mask = (df["smoke"] != "never") & (df["bwt"] < 100)
    return df[mask].sort_values("bwt", ascending=True)


def q26_extremes(df, cols=None):
    cols = cols or D.NUMERIC
    c = df[cols].corr()
    m = c.where(~np.eye(len(c), dtype=bool)).abs().stack()
    m = m[[i < j for i, j in m.index]]
    hi, lo = m.idxmax(), m.idxmin()
    return ((hi[0], hi[1], round(float(m.max()), 4)),
            (lo[0], lo[1], round(float(m.min()), 4)))


# ======================================================================
#  TRACES
# ======================================================================

def trace_missing():
    raw = D.load_raw()
    print()
    print("  %-12s %-9s %-9s %s" % ("column", "missing", "pct", "note"))
    print("  " + "-" * 58)
    miss = raw.isna().sum().sort_values(ascending=False)
    for c, n in miss.items():
        pct = 100 * n / len(raw)
        note = ""
        if pct > 30:
            note = "<- drop the COLUMN"
        elif n and c == "inc":
            note = "<- probably not MCAR"
        print("  %-12s %-9d %-9.1f %s" % (c, n, pct, note))
    print()
    print("  drop dht/dwt as columns, then dropna rows : %d rows"
          % len(D.load_clean()))
    print("  dropna rows without dropping the columns  : %d rows"
          % len(raw.dropna()))
    print("  the two father columns cost you            : %d rows"
          % (len(D.load_clean()) - len(raw.dropna())))


def trace_smoke():
    df = D.load_clean()
    print()
    vc = df["smoke"].value_counts()
    means = df.groupby("smoke")["bwt"].mean()
    never = means["never"]
    print("  %-26s %-7s %-9s %s" % ("smoke", "n", "mean bwt", "vs never"))
    print("  " + "-" * 58)
    for k in ["never", "now", "once did, not now", "until current pregnancy"]:
        print("  %-26s %-7d %-9.2f %+.2f" % (k, vc[k], means[k], means[k] - never))
    print()
    print("  brief's binary  (!= never) : %.1f%% of the sample"
          % ((df["smoke"] != "never").mean() * 100))
    print("  meaningful binary (== now) : %.1f%% of the sample"
          % ((df["smoke"] == "now").mean() * 100))
    print()
    print("  Only `now` moves. Quitters look like never-smokers.")


def trace_corr():
    df = D.load_clean()
    c = df[D.NUMERIC + ["bwt"]].corr()
    print()
    print(c.round(3).to_string())
    print()
    (a, b, rh), (x, y, rl) = q26_extremes(df)
    print("  highest |r| among FEATURES : %s vs %s = %.4f" % (a, b, rh))
    print("  lowest  |r| among FEATURES : %s vs %s = %.4f" % (x, y, rl))
    print()
    tb = c["bwt"].drop("bwt").abs().sort_values(ascending=False)
    print("  correlation with the TARGET:")
    for k in tb.index:
        print("    %-10s %+.4f" % (k, c.loc[k, "bwt"]))


TRACES = {"2.1": trace_missing, "2.2": trace_missing, "2.3": trace_smoke,
          "2.4": trace_smoke, "2.5": trace_smoke, "2.6": trace_corr}


# ======================================================================
#  YOUR TURN -- LIVE EDITS
# ======================================================================

# V1 | "Show me every column missing more than X of its values."
#    | Return a SORTED list of column names whose missing FRACTION is
#    | strictly greater than `frac`.
#    |   (raw, 0.40) -> ['dwt']
#    |   (raw, 0.30) -> ['dht', 'dwt']
#    |   (raw, 0.05) -> ['dht', 'dwt', 'inc']
#    | Hint: isna() gives a boolean frame; the MEAN of a boolean is a
#    | proportion. One line, no loop.
def missing_above(df, frac):
    pass


# V2 | "Now define a smoker differently."
#    | Return the percentage of rows whose `smoke` value is in the
#    | given collection.
#    |   (clean, {"now","until current pregnancy","once did, not now"})
#    |       -> 55.4884...        (the brief's definition)
#    |   (clean, {"now"}) -> 39.0735...
#    | This is the single most likely Q2.3 live edit.
def smoker_pct(df, smoker_values):
    pass


# V3 | "Split the target by a different column."
#    | Return mean bwt grouped by `col`, rounded to 2dp, sorted by the
#    | group name.
#    |   (clean, "smoke") -> never 122.55, now 113.40,
#    |                       once did not now 123.20, until... 122.64
#    |   (clean, "race")  -> asian 109.49, black 113.12, mex 123.55,
#    |                       mixed 115.11, white 120.90
def bwt_by(df, col):
    pass


# V4 | "Change the risk threshold."
#    | Rows where smoke is in `smoker_values` AND bwt < max_bwt,
#    | sorted by bwt ascending. Return the DataFrame.
#    |   defaults -> 98 rows, lowest bwt 58
#    |   max_bwt=90 -> 39 rows
#    |   smoker_values={"now"} -> 85 rows
#    | Watch the parentheses.
def high_risk(df, max_bwt=100, smoker_values=None):
    pass


# V5 | "Which two features are most and least correlated?"
#    | Return ((a, b, r), (c, d, r)) for the highest and lowest ABSOLUTE
#    | correlation, excluding the diagonal and counting each pair once.
#    | Names within a pair in alphabetical order; r rounded to 4dp.
#    |   (clean, NUMERIC) -> (('age','dage',0.8275), ('dage','height',0.0089))
#    | Getting r = 1.0 means you forgot the diagonal.
def corr_extremes(df, cols):
    pass


# V6 | "Add the engineered columns."
#    | Return a NEW DataFrame (do not mutate the input) with bwt_grams
#    | and weight_category added.
#    |   len(out.columns) == len(df.columns) + 2
#    |   out["weight_category"].value_counts() -> Normal 839, High 101, Low 53
#    |   the input df must be unchanged afterwards
def add_features(df):
    pass


# ======================================================================
#  TESTS -- do not edit
# ======================================================================

_RAW = D.load_raw()
_CLEAN = D.load_clean()

_V1 = [
    ("frac 0.40", lambda f: f(_RAW, 0.40), ["dwt"]),
    ("frac 0.30", lambda f: f(_RAW, 0.30), ["dht", "dwt"]),
    ("frac 0.05", lambda f: f(_RAW, 0.05), ["dht", "dwt", "inc"]),
    ("frac 0.99", lambda f: f(_RAW, 0.99), []),
    ("clean has none", lambda f: f(_CLEAN, 0.0), []),
]

_BRIEF = {"now", "until current pregnancy", "once did, not now"}
_V2 = [
    ("brief definition", lambda f: f(_CLEAN, _BRIEF), 55.48841892245721),
    ("now only", lambda f: f(_CLEAN, {"now"}), 39.07351459214501),
    ("never only", lambda f: f(_CLEAN, {"never"}), 44.51158107754279),
    ("nothing", lambda f: f(_CLEAN, set()), 0.0),
]

_V3 = [
    ("by smoke", lambda f: f(_CLEAN, "smoke"),
     pd.Series([122.55, 113.40, 123.20, 122.64],
               index=pd.Index(["never", "now", "once did, not now",
                               "until current pregnancy"], name="smoke"))),
    ("by race", lambda f: f(_CLEAN, "race"),
     pd.Series([109.49, 113.12, 123.55, 115.11, 120.90],
               index=pd.Index(["asian", "black", "mex", "mixed", "white"],
                              name="race"))),
]

_V4 = [
    ("defaults count", lambda f: len(f(_CLEAN)), 98),
    ("defaults lowest bwt", lambda f: int(f(_CLEAN)["bwt"].iloc[0]), 58),
    ("max_bwt 90", lambda f: len(f(_CLEAN, 90)), 39),
    ("now only", lambda f: len(f(_CLEAN, 100, {"now"})), 85),
    ("sorted ascending",
     lambda f: list(f(_CLEAN)["bwt"]) == sorted(f(_CLEAN)["bwt"]), True),
]

_V5 = [
    ("features only", lambda f: f(_CLEAN, D.NUMERIC),
     (("age", "dage", 0.8275), ("dage", "height", 0.0089))),
    ("with the target", lambda f: f(_CLEAN, D.NUMERIC + ["bwt"]),
     (("age", "dage", 0.8275), ("dage", "height", 0.0089))),
    ("two columns only", lambda f: f(_CLEAN, ["age", "dage"]),
     (("age", "dage", 0.8275), ("age", "dage", 0.8275))),
]

_V6 = [
    ("adds two columns",
     lambda f: len(f(_CLEAN).columns) - len(_CLEAN.columns), 2),
    ("category counts",
     lambda f: dict(f(_CLEAN)["weight_category"].value_counts()),
     {"Normal": 839, "High": 101, "Low": 53}),
    ("grams are right",
     lambda f: round(float(f(_CLEAN)["bwt_grams"].iloc[0]), 2),
     round(float(_CLEAN["bwt"].iloc[0]) * 28.3495, 2)),
    ("input not mutated",
     lambda f: (f(_CLEAN), "bwt_grams" in _CLEAN.columns)[1], False),
]


def main():
    argv = sys.argv
    mode = D.argmode(argv)
    qid = D.which(argv)
    ids = [qid] if qid in STATEMENTS else sorted(STATEMENTS)

    if mode == "teach":
        for q in ids:
            D.head("PART 2 :: Q%s" % q)
            print(STATEMENTS[q])
            print(LESSONS[q])
        return
    if mode == "trace":
        seen = set()
        for q in ids:
            fn = TRACES[q]
            if fn in seen:
                continue
            seen.add(fn)
            D.head("PART 2 :: TRACE (Q%s)" % q)
            fn()
        return
    if mode in ("quiz", "answers"):
        D.head("PART 2 :: EXAMINER")
        pairs = [(("Q%s  " % q) + question, a)
                 for q, question, a in EXAMINER if q in ids]
        D.quiz(pairs, show=(mode == "answers"))
        return

    D.head("PART 2 -- Pandas")
    D.sub("reference solutions")
    D.check("shapes", lambda: None if False else (_RAW.shape, _CLEAN.shape),
            [("raw and clean", lambda f: f(), ((1236, 16), (993, 14)))])
    D.check("q23_smoker_pct", q23_smoker_pct,
            [("55.49", lambda f: f(_CLEAN), 55.48841892245721)])
    D.check("q25_high_risk", q25_high_risk,
            [("98 rows", lambda f: len(f(_CLEAN)), 98)])
    D.check("q26_extremes", q26_extremes,
            [("extremes", lambda f: f(_CLEAN),
              (("age", "dage", 0.8275), ("dage", "height", 0.0089)))])

    D.sub("your live edits")
    D.report([
        D.check("V1 missing_above", missing_above, _V1),
        D.check("V2 smoker_pct", smoker_pct, _V2),
        D.check("V3 bwt_by", bwt_by, _V3),
        D.check("V4 high_risk", high_risk, _V4),
        D.check("V5 corr_extremes", corr_extremes, _V5),
        D.check("V6 add_features", add_features, _V6),
    ])


if __name__ == "__main__":
    main()
