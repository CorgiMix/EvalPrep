"""
======================================================================
  PART 3 -- Model Building & Evaluation            (40 of 60 points)
======================================================================

    python notebook/part3.py --teach          all five questions
    python notebook/part3.py --teach 3.5      the 20-point one
    python notebook/part3.py --trace 3.4      watch the numbers
    python notebook/part3.py --quiz / --answers
    python notebook/part3.py                  mark your live edits

Q3.5 alone is 20 points -- a third of the coursework. Read its lesson
twice. It contains the one result in this whole assignment that will
surprise your assessor, and the one question most likely to sink you.
======================================================================
"""

import sys
import os
import warnings

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import _data as D


STATEMENTS = {
    "3.1": """Q3.1 -- Prepare Features and Target (2 points)

  Numeric features:      gestation, parity, age, height, weight, dage
  Categorical (one-hot): race, ed, drace, ded, marital, inc, smoke

  X = numeric as-is + pd.get_dummies(..., drop_first=True)
  y = bwt

  Drop bwt_grams and weight_category -- they are derived from the
  target.

  Expected:  X (993, 40)    y (993,)""",

    "3.2": """Q3.2 -- Train / Test Split (6 points)

  80% train, 20% test, with a random seed. Print all four sizes.

  Expected:  X_train (794, 40)   X_test (199, 40)

  "Present another way to split the data that takes into account the
   dataset characteristics. Is the new method better for model
   training? Explain."   <--
   this second half is where the marks are""",

    "3.3": """Q3.3 -- Train a Linear Regression Model (5 points)

  Fit LinearRegression on the training set. Print the ~40 coefficients
  alongside their feature names, and print the intercept.

  Expected intercept: -94.18
  Largest coefficients: drace_mex 14.92, drace_white 12.30,
  marital_never married -12.00, ded_Trade school HS unclear -10.73""",

    "3.4": """Q3.4 -- Evaluate the Model (7 points)

  Evaluate on the TEST set with MAE, RMSE and R-squared, each printed
  to 4 decimal places.

  Expected:  MAE 12.2751   RMSE 15.5115   R2 0.2511""",

    "3.5": """Q3.5 -- Compare with a Stronger Model (20 points)

  Train a stronger model of your choice on the same split. Choose one
  whose architecture you can EXPLAIN -- you will be asked.

  Evaluate with the same three metrics and print a comparison table
  against the Linear Regression baseline.

  "Why might your chosen model outperform Linear Regression on this
   specific dataset?" """,
}


LESSONS = {
    "3.1": """
WHY 40 COLUMNS, EXACTLY

      6 numeric
    + race 4 + ed 6 + drace 3 + ded 6 + marital 3 + inc 9 + smoke 3
    = 6 + 34 = 40

  Each categorical contributes (number of categories - 1) columns,
  because drop_first=True removes one. Without drop_first you get 47.
  Being able to derive 40 rather than just observe it is the whole of
  this 2-point question.

WHAT drop_first=True ACTUALLY PREVENTS

  If you keep every category, the dummies for one variable always sum
  to exactly 1 for every row. That column of 1s is precisely the
  intercept, so the design matrix becomes rank-deficient and there is
  no unique solution -- infinitely many coefficient sets fit equally
  well. This is the DUMMY VARIABLE TRAP, or perfect multicollinearity.

  sklearn will not crash: it uses a least-squares solver that returns
  the minimum-norm solution. So you get numbers, and they are
  meaningless individually. That is worse than an error.

  Dropping one category per variable makes the rest identifiable
  against it.

WHICH CATEGORY GETS DROPPED -- AND THE ANSWER IS UNCOMFORTABLE

  get_dummies sorts the categories and drops the FIRST
  ALPHABETICALLY. Not the most common. Not a chosen baseline.
  Alphabetical.

      race     -> 'asian'                               (35 rows)
      drace    -> 'asian'                               (32 rows)
      ed, ded  -> '8th -12th grade - did not graduate'  (136 / 142)
      marital  -> 'divorced'                            (2 ROWS)
      inc      -> '0-2500'                              (28 rows)
      smoke    -> 'never'                               (442 rows)

  So smoke_now = -7.64 means "7.64 ounces lighter than a NEVER-smoker,
  holding everything else fixed". You cannot interpret a single
  coefficient without naming its baseline, and this is the sentence
  that proves you can.

  And look at `marital`. The baseline is 'divorced', which has TWO
  observations. Every marital coefficient in your model is measured
  against two people. marital_never married = -12.00 is estimated from
  three people against a baseline of two. It is noise in a large font,
  and volunteering that is worth more than the coefficient.

INCOME IS ORDINAL AND YOU JUST DESTROYED THE ORDER

  0-2500 < 2500-5000 < 5000-7500 ... is an ORDERED scale. One-hot
  encoding throws that away and hands the model nine unordered flags.
  The model cannot know 20000-22500 is bigger than 0-2500.

  The alternative is ordinal encoding -- map each bracket to its
  midpoint and keep it as ONE numeric column. That costs 8 columns and
  imposes linearity in income, which may or may not be right.

  Also: the dummies sort ALPHABETICALLY, so inc_10000-12500 comes
  before inc_2500-5000. "10000" sorts before "2500" as text.

  And the brackets are not even a clean partition -- the data contains
  both '15000+' and '15000-17500'. That is a defect in the source.

TARGET LEAKAGE -- SAY THE PHRASE

  bwt_grams is bwt * 28.3495, a perfect linear function of the target.
  weight_category is bwt bucketed. Either one in X gives R-squared near
  1.0 from a model that has learned nothing.

  The brief tells you to drop them. Say WHY without being asked.
""",

    "3.2": """
THE MECHANICS, AND THE ONE ARGUMENT THAT MATTERS

      X_train (794, 40)    X_test (199, 40)
      794 = floor(993 * 0.8),  199 = the remainder

  random_state makes the split reproducible. Without it every run
  gives different metrics and you cannot compare anything. Say
  "reproducibility", not "it makes it random".

THE SECOND HALF OF THE QUESTION IS WHERE THE SIX POINTS LIVE
------------------------------------------------------------

  "Present another way to split the data that takes into account the
   dataset characteristics."

  Work through the candidates OUT LOUD and reject them with reasons.
  The rejections are worth as much as the answer.

    STRATIFIED SPLIT   stratify= needs a discrete variable. bwt is
                       continuous, so you would have to bin it first
                       -- e.g. stratify on weight_category, or on
                       quartiles of bwt. Legitimate, and it does help
                       when the target is skewed. Here bwt is roughly
                       symmetric (mean 119.0, median 119.0), so the
                       gain is small.

    GROUPED SPLIT      GroupKFold exists for repeated subjects. DOES
                       NOT APPLY HERE -- I checked: all 1,236 id
                       values are unique, so no mother appears twice.
                       Saying "I checked and it does not apply" is far
                       stronger than not mentioning it.

    TIME-BASED SPLIT   The raw data has a `date` column, so a
                       chronological split is conceivable. But the
                       starter code drops date, and there is no
                       forecasting task here, so it is not warranted.

    K-FOLD CROSS-VALIDATION   <-- this is the answer

  WHY K-FOLD, WITH THE NUMBERS TO PROVE IT

  A single 199-row test set gives you ONE estimate. Here is what
  5-fold cross-validation actually returns on this data:

      fold R-squared:  0.2511  0.2567  0.2847  0.2742  0.1054
      mean 0.2344, standard deviation 0.0656

  Look at that spread. The folds range from 0.11 to 0.28. Your single
  reported test R-squared of 0.2511 is a draw from that distribution
  -- and it happens to sit on the optimistic side of the mean.

  So the honest statement is: 0.2511 is one sample from a distribution
  with a standard deviation of about 0.066. Quoting it to four decimal
  places implies a precision that does not exist.

  IS K-FOLD "BETTER"? -- ANSWER BOTH HALVES

    Better for ESTIMATING performance: yes, decisively. Every row is
    used for validation exactly once, the estimate averages over five
    splits, and you get an uncertainty estimate for free.

    Better for TRAINING the final model: no, it is orthogonal. CV is
    an evaluation protocol, not a training method. You still fit the
    deployed model on all the data at the end.

    Cost: five times the compute. Irrelevant at 993 rows; relevant at
    scale.

  The question literally asks "is the new method better for model
  training?" -- so the precise answer is: it is better for MODEL
  SELECTION and for ESTIMATING generalisation, and it does not change
  training at all. Making that distinction is the point.

  ONE MORE THING THAT WILL IMPRESS

  993 rows with 40 features is a small-n, wide-p setting. That is
  exactly where a single split is least trustworthy, because 199 test
  rows cannot pin down a difference of a few hundredths in R-squared.
  Repeated k-fold (RepeatedKFold, several different seeds) is the
  standard fix.
""",

    "3.3": """
THE INTERCEPT IS -94.18 AND IT IS NOT A BUG

  A negative birth weight looks alarming. It is not.

  The intercept is the predicted bwt when EVERY feature is zero --
  gestation 0 days, height 0 inches, weight 0 lbs, mother's age 0, and
  every dummy at its baseline. That row is physically impossible, so
  the intercept is a pure mathematical anchor obtained by extrapolating
  far outside the data.

  Say: "the intercept is not interpretable here because zero is
  outside the range of every numeric feature. If I centred the
  predictors, the intercept would become the prediction at the mean of
  every feature, which is about 119 ounces and is interpretable."

  That is the answer. Centring is the fix, and naming it is the tell.

THE COEFFICIENT RANKING IS A UNITS ARTEFACT -- THIS IS THE BIG ONE

  What the model prints, largest first:

      drace_mex                      14.92
      drace_white                    12.30
      marital_never married         -12.00
      ded_Trade school HS unclear   -10.73
      drace_black                     8.05
      marital_married                -7.75
      smoke_now                      -7.64
      ...
      gestation                       0.44      <-- looks negligible

  It is not negligible. A dummy can only move from 0 to 1, so its
  coefficient IS its full effect. gestation moves in DAYS, and its
  standard deviation is 15.45 days. Multiply each coefficient by its
  feature's standard deviation and you get the effect of a typical
  one-SD move:

      feature        raw      per SD    rank change
      gestation      0.44      6.85     35th -> 1st
      drace_white   12.30      5.46      2nd -> 2nd
      smoke_now     -7.64     -3.73      7th -> 3rd
      drace_black    8.05      3.27      5th -> 4th
      height         1.21      3.00     ~20th -> 5th
      drace_mex     14.92      2.61      1st -> 6th

  GESTATION IS THE STRONGEST PREDICTOR IN THE MODEL AND IT LOOKS LIKE
  ONE OF THE WEAKEST IN THE PRINTOUT. The largest printed coefficient,
  drace_mex, falls to sixth.

  This is the single best thing you can say in Q3.3. It is also
  consistent with Q2.6, where gestation was the only feature
  correlating above 0.20 with bwt.

  Caveat to add yourself: standardising dummies is slightly odd -- the
  SD of a 0/1 variable is a function of how rare it is, so a very rare
  category gets shrunk. That is arguably the right behaviour, since a
  category with 5 members should not dominate a ranking. Raise it
  before they do.

THE THREE COEFFICIENTS YOU SHOULD REFUSE TO INTERPRET

      marital_never married  -12.00   3 rows, baseline 'divorced' = 2 rows
      ded_Trade school ...   -10.73   5 rows
      marital_married         -7.75   978 rows, but same 2-row baseline

  Large coefficients estimated from almost no data. Point at them
  before the assessor does.

MULTICOLLINEARITY, WITH EVIDENCE FROM YOUR OWN Q2.6

  age and dage correlate at 0.83. race and drace overlap heavily too.
  Consequences:

    - coefficients become unstable; small data changes swing them
    - signs can flip without any change in predictive power
    - individual coefficients stop being interpretable, though the
      MODEL's predictions are fine

  The diagnostic is the Variance Inflation Factor; VIF above 5 or 10
  is the usual flag. The fix is Ridge regression, which adds an L2
  penalty and shrinks correlated coefficients toward each other. On
  this data, Ridge with alpha=10 shrinks the race/drace block by about
  29% while leaving gestation essentially untouched (6.85 -> 6.77) --
  exactly the signature you would predict, since gestation is a
  genuine stable effect and the race block is not.

  Two race coefficients even FLIP SIGN under Ridge. That is direct
  evidence of instability, from your own data.
""",

    "3.4": """
THE THREE NUMBERS

      MAE   12.2751     mean absolute error, in OUNCES
      RMSE  15.5115     root mean squared error, in OUNCES
      R2     0.2511     proportion of variance explained, unitless

  MAE and RMSE are in the units of the target. Saying "the model is
  off by about 12 ounces on average" is the interpretation; quoting
  12.2751 without units is not.

  Context: 12.28 oz is about 348 grams, against a mean birth weight of
  119 oz. So the typical error is around 10% of the value. The
  standard deviation of bwt is 18.20 oz, so predicting the mean every
  time would give an MAE near 14.5 -- your model is better than that,
  but not dramatically.

WHY RMSE IS ALWAYS >= MAE, AND WHAT THE GAP MEANS

  It is a mathematical guarantee, not a property of this data: by
  Jensen's inequality the root-mean-square of a set of non-negative
  numbers is at least their arithmetic mean, with equality only if
  every error is identical.

  Here RMSE / MAE = 15.51 / 12.28 = 1.26. The gap exists because
  squaring punishes large errors disproportionately, so RMSE is
  inflated by a minority of badly-missed births -- almost certainly
  the very preterm ones, where gestation runs down to 181 days.

  If asked which to report: MAE if all errors matter equally, RMSE if
  large errors are disproportionately costly. For birth weight,
  missing a low-birth-weight baby badly IS worse, so RMSE is arguably
  the better headline.

R-SQUARED, SAID PROPERLY

      R2 = 1 - SS_res / SS_tot

  SS_res is the squared error of your model; SS_tot is the squared
  error of always predicting the mean. So R-squared is "how much
  better than the mean, in squared error terms".

      R2 = 0     no better than predicting the mean
      R2 = 1     perfect
      R2 < 0     WORSE than predicting the mean -- possible on a test
                 set, and worth saying you know it

  0.2511 means the model explains about 25% of the variance in birth
  weight and leaves 75% unexplained. For a biological outcome from
  demographic predictors, that is unremarkable and honest. Birth
  weight depends on genetics, nutrition, placental function and chance
  -- none of which are in these 40 columns.

  Resist calling it good or bad. Call it what it is.

TRAIN VERSUS TEST -- COMPUTE THE GAP, IT WILL BE ASKED

      train R2  0.3126
      test  R2  0.2511
      gap       0.0616

  A modest gap. The model is slightly overfit, which is expected with
  40 features and 794 training rows -- and especially with dummies for
  categories that have only a handful of members. It is not severe;
  a gap of 0.5 would be.

AND THE CAVEAT THAT ELEVATES THE ANSWER

  0.2511 comes from ONE test set of 199 rows. Five-fold CV on the same
  data gives fold scores of 0.2511, 0.2567, 0.2847, 0.2742 and 0.1054
  -- mean 0.2344, SD 0.0656.

  So the reported figure sits on the optimistic side of the
  distribution, and four decimal places imply a precision that a
  199-row sample cannot support. Say that.
""",

    "3.5": """
=====================================================================
  THIS IS 20 POINTS. THE HONEST ANSWER IS COUNTERINTUITIVE.
=====================================================================

WHAT ACTUALLY HAPPENS WHEN YOU RUN IT

  Measured on this data, same split, seed 42:

    model                 test R2    5-fold CV R2 (SD)   train R2
    LinearRegression       0.2511      0.2344 (0.066)     0.3126
    Ridge alpha=10         0.2570      0.2376 (0.065)     0.3121
    RandomForest(300)      0.3164      0.2242 (0.075)     0.8935
    RF(min_samples_leaf=5) 0.3274      0.2441 (0.073)     0.6242
    GradientBoosting       0.2795      0.2190 (0.045)     0.5870
    XGB depth3 lr.05 n300  0.2448      0.2162 (0.048)     0.6493
    XGB depth2 lr.03 lam5  0.3257      0.2821 (0.055)     0.4315

  READ THAT TABLE CAREFULLY. THREE THINGS JUMP OUT.

  1. A REASONABLE-LOOKING XGBOOST LOSES TO LINEAR REGRESSION.
     depth 3, lr 0.05, 300 trees -- a perfectly standard
     configuration -- scores 0.2448 on test against linear's 0.2511,
     and 0.2162 on CV against 0.2344. It is WORSE on both. Its train
     R-squared of 0.6493 against a test of 0.2448 tells you exactly
     why: it memorised.

  2. RANDOM FOREST "WINS" ON THE TEST SET AND LOSES ON CV.
     0.3164 test looks like a clear victory over 0.2511. But its CV
     mean is 0.2242 -- BELOW linear regression. Train R-squared 0.8935.
     The test-set win is largely luck of that particular 199-row draw.
     This is Q3.2's argument made concrete in your own results.

  3. ONLY A HEAVILY REGULARISED BOOSTER GENUINELY WINS.
     depth 2, learning rate 0.03, reg_lambda 5: test 0.3257, CV 0.2821,
     train 0.4315. Better on test AND on CV, with the smallest
     train-test gap of any tree model.

  SO THE ANSWER TO "WHY MIGHT IT OUTPERFORM" IS NOT "BECAUSE IT IS
  STRONGER". It is conditional, and the condition is regularisation.

WHY THIS DATASET PUNISHES CAPACITY

  - 993 rows, 40 features, and 34 of those are sparse 0/1 dummies.
    Several categories have fewer than 10 members. A deep tree will
    happily isolate a five-row leaf and call it a pattern.
  - The signal is weak. The best R-squared anyone gets here is around
    0.28, so roughly three quarters of the variance is irreducible
    noise. Extra capacity has nothing left to fit except that noise.
  - The dominant relationship, gestation to birth weight, is close to
    LINEAR. Linear regression models it perfectly well; trees have to
    approximate a straight line with a staircase, which costs them
    accuracy on the one thing that matters most.

  This is the crisp version: gradient boosting buys you non-linearity
  and interactions. On this data there is very little non-linearity to
  buy, and not enough rows to estimate interactions reliably. So you
  pay the variance cost and receive almost no bias reduction.

WHAT YOU SHOULD ACTUALLY SAY

  "I tried gradient boosting. With standard settings it did NOT beat
   linear regression -- 0.2448 against 0.2511 on test, and worse on
   cross-validation, with a train R-squared of 0.65 showing clear
   overfitting. Only after constraining it hard -- depth 2, learning
   rate 0.03, an L2 penalty -- did it win, at 0.2821 CV against 0.2344.
   The reason is that with 993 rows, mostly sparse dummies and a
   largely linear signal, model capacity is a liability rather than an
   asset here."

  That answer is worth more than a table showing a win, because it
  demonstrates you evaluated rather than assumed.

THE ARCHITECTURE, BECAUSE THE BRIEF SAYS YOU WILL BE ASKED
----------------------------------------------------------

  GRADIENT BOOSTING, in the order it actually happens:

  1. Start with a constant prediction -- the mean of y.
  2. Compute the GRADIENT of the loss with respect to the current
     prediction for every row. For squared error that gradient is
     just the residual, which is why people say "fit the next tree to
     the residuals" -- true for this loss, not in general.
  3. Fit a SHALLOW regression tree to those gradients.
  4. Add that tree's output to the running prediction, multiplied by
     the LEARNING RATE (shrinkage), typically 0.01 to 0.1.
  5. Repeat for n_estimators rounds.

  It is ADDITIVE and SEQUENTIAL: each tree corrects what the ensemble
  so far got wrong. Contrast with a random forest, which grows deep
  trees INDEPENDENTLY in parallel and averages them.

  The distinction to state: boosting reduces BIAS by adding
  corrections; bagging reduces VARIANCE by averaging. That is why
  boosting overfits more readily, and why it is the wrong default on
  993 noisy rows.

  WHAT XGBOOST ADDS specifically:
    - a SECOND-ORDER expansion: it uses both the gradient g and the
      hessian h, so the optimal leaf weight is -G / (H + lambda)
      rather than a plain mean. This is Newton boosting.
    - regularisation IN the split criterion: lambda on leaf weights,
      gamma as a minimum gain to make a split at all
    - subsample and colsample_bytree, which inject randomness per tree
    - sparsity-aware split finding and a default direction for
      missing values
    - histogram-based binning of features for speed

  HYPERPARAMETERS, AND WHAT EACH ONE TRADES:
      n_estimators    more rounds -> lower bias, higher overfit risk
      learning_rate   smaller -> needs more rounds, generalises better
      max_depth       controls interaction ORDER; depth 2 allows only
                      pairwise interactions
      subsample /     row and column sampling; decorrelates the trees
      colsample
      reg_lambda      L2 on leaf weights; directly shrinks predictions
      min_child_weight  minimum hessian in a leaf; blocks tiny leaves

  Depth is the one to lead with here, because depth is exactly what
  you had to reduce to make it work.

=====================================================================
  THE QUESTION MOST LIKELY TO SINK YOU
=====================================================================

  "How did you choose those hyperparameters?"

  If you tuned them by watching the TEST R-squared go up -- which is
  what everyone does -- then the test set stopped being a test set the
  moment you looked at it twice. Your 0.3257 is optimistically biased,
  and the amount of bias is unknown.

  DO NOT PRETEND OTHERWISE. Say this:

    "I selected them by trying configurations and comparing scores,
     and I need to be honest that if I judged those comparisons on the
     test set, then the test score is no longer an unbiased estimate
     of generalisation -- I have used it for selection. The correct
     procedure is to tune inside the TRAINING set using
     cross-validation, with GridSearchCV or RandomizedSearchCV, and
     touch the test set exactly once at the end. For a fully unbiased
     estimate you need NESTED cross-validation: an inner loop for
     tuning and an outer loop for evaluation."

  Admitting the flaw and naming the correct procedure scores far
  higher than a confident wrong answer. This is a 20-point question
  and this is its hardest moment.

  ALSO HAVE READY: use a Pipeline. If you scale, the scaler must be
  fitted inside each CV fold, not on the whole dataset beforehand --
  otherwise the fold's test rows influenced the mean and standard
  deviation used to transform them, which is leakage. Pipeline makes
  that automatic. (Trees do not need scaling, so this bites you on
  Ridge, not on XGBoost.)

WHAT ELSE COULD ACTUALLY IMPROVE THINGS HERE

  - Ordinal-encode `inc` as bracket midpoints: one column instead of
    nine, and it restores the ordering the model currently cannot see.
  - Collapse the rare categories. `marital` is 978 married against 15
    everything-else; a binary married/not is more honest than three
    dummies against a 2-row baseline.
  - Collapse `smoke` to now / not-now, since Q2.3 showed the three
    non-current categories are indistinguishable.
  - Ridge or ElasticNet rather than plain OLS, given the
    multicollinearity between age/dage and race/drace.
  - Accept the ceiling. With these predictors, R-squared around 0.28
    may simply be what is available.
""",
}


EXAMINER = [
    ("3.1", "Derive the number 40 for me.",
     """Six numeric columns, plus categories minus one for each
        categorical: race 4, ed 6, drace 3, ded 6, marital 3, inc 9,
        smoke 3. That is 34 dummies plus 6 numeric = 40. Without
        drop_first it would be 47."""),

    ("3.1", "What does drop_first=True prevent?",
     """The dummy variable trap. With every category kept, a variable's
        dummies sum to 1 in every row, which duplicates the intercept
        and makes the design matrix rank-deficient. There is then no
        unique solution. sklearn will not error -- it returns the
        minimum-norm solution -- so you get meaningless numbers rather
        than a crash, which is worse."""),

    ("3.1", "Which category does it drop?",
     """The first alphabetically -- not the most common. So race and
        drace drop 'asian', ed and ded drop '8th -12th grade', marital
        drops 'divorced', inc drops '0-2500', and smoke drops
        'never'."""),

    ("3.1", "So what does smoke_now = -7.64 mean?",
     """A current smoker's baby is predicted 7.64 ounces lighter than a
        NEVER-smoker's, holding every other feature fixed. The baseline
        has to be named or the coefficient means nothing."""),

    ("3.1", "Is there a problem with the marital baseline?",
     """Yes, a serious one. 'divorced' has two rows. Every marital
        coefficient is measured against two people, and
        marital_never married = -12.00 is estimated from three. Those
        coefficients are noise, not findings."""),

    ("3.1", "Is one-hot the right encoding for income?",
     """No. Income is ordinal and one-hot discards the ordering, so the
        model cannot know 20000-22500 exceeds 0-2500. Mapping brackets
        to midpoints gives one numeric column instead of nine and
        preserves the order, at the cost of assuming linearity. The
        source data also has overlapping brackets -- both '15000+' and
        '15000-17500' exist."""),

    ("3.1", "Why drop bwt_grams and weight_category?",
     """Target leakage. bwt_grams is the target times a constant and
        weight_category is the target bucketed. Either gives R-squared
        near 1.0 from a model that learned nothing."""),

    ("3.2", "What does random_state do?",
     """Fixes the shuffle so the split is reproducible. Without it every
        run gives different metrics and no comparison between models is
        valid."""),

    ("3.2", "Give me another way to split, appropriate to this data.",
     """K-fold cross-validation. Every row is used for validation
        exactly once and you get an uncertainty estimate. On this data
        5-fold gives 0.2511, 0.2567, 0.2847, 0.2742, 0.1054 -- mean
        0.2344, SD 0.066. The single reported 0.2511 sits on the
        optimistic side of that."""),

    ("3.2", "What about a stratified split?",
     """stratify needs a discrete variable and bwt is continuous, so you
        would bin it first -- on weight_category or on quartiles. It is
        legitimate and helps with a skewed target, but bwt here is
        roughly symmetric with mean and median both 119, so the gain is
        small."""),

    ("3.2", "What about GroupKFold?",
     """It would matter if mothers repeated across rows, but I checked:
        all 1,236 id values are unique, so every row is a distinct
        pregnancy and grouping does not apply."""),

    ("3.2", "Is cross-validation better for model TRAINING?",
     """No -- it is an evaluation protocol, not a training method. It is
        better for estimating generalisation and for model selection.
        The final model is still fitted on all the data. Making that
        distinction is what the question is actually testing."""),

    ("3.3", "Your intercept is negative. Explain.",
     """It is the prediction when every feature is zero -- zero
        gestation, zero height, zero maternal weight. That row is
        impossible, so the intercept is an extrapolation far outside
        the data and is not interpretable. Centring the predictors
        would make it the prediction at the mean of every feature,
        about 119 ounces."""),

    ("3.3", "Which feature has the largest effect on birth weight?",
     """gestation -- but you cannot see it in the raw coefficients.
        Raw, it is 0.44 and ranks about 35th. Multiplied by its
        standard deviation of 15.45 days it is 6.85 ounces per SD,
        which is the largest in the model. The printed ranking is a
        units artefact: dummies only move from 0 to 1."""),

    ("3.3", "Then why is drace_mex 14.92 the biggest printed number?",
     """Because it is a dummy, so 14.92 is its entire effect rather than
        a per-unit rate. Standardised it falls to 2.61 and sixth place.
        It is also estimated on 28 rows against a 32-row baseline, so I
        would not lean on it."""),

    ("3.3", "Any issue with standardising the dummies?",
     """Slightly, yes. The SD of a 0/1 column is a function of how rare
        the category is, so rare categories get shrunk. I would argue
        that is desirable -- a five-member category should not top an
        importance ranking -- but it is a choice worth stating."""),

    ("3.3", "You have age and dage correlated at 0.83. What does that "
            "do?",
     """Multicollinearity. Their individual coefficients become
        unstable and can flip sign, because the model cannot attribute
        the shared variance. Prediction is unaffected; interpretation
        is not. The diagnostic is VIF, and Ridge is the fix -- on this
        data alpha=10 shrinks the race/drace block about 29% while
        gestation barely moves, 6.85 to 6.77."""),

    ("3.4", "What are the units of MAE and RMSE?",
     """Ounces, the units of the target. So the model is off by about 12
        ounces on average -- roughly 348 grams against a mean birth
        weight of 119 ounces, so about 10%."""),

    ("3.4", "Why is RMSE larger than MAE?",
     """It always is -- Jensen's inequality guarantees the
        root-mean-square of non-negative numbers is at least their
        arithmetic mean, with equality only if all errors are equal.
        The ratio here is 1.26, driven by a minority of badly-missed
        births, most likely the very preterm ones."""),

    ("3.4", "Define R-squared.",
     """One minus the residual sum of squares over the total sum of
        squares, where the total is measured against always predicting
        the mean. So it is how much better than the mean you are, in
        squared-error terms. It can be negative on a test set if the
        model is worse than the mean."""),

    ("3.4", "Is 0.2511 good?",
     """It is what it is: about a quarter of the variance explained,
        three quarters not. For a biological outcome predicted from
        demographics that is unremarkable. Birth weight also depends on
        genetics, nutrition, placental function and chance, none of
        which are in these columns."""),

    ("3.4", "What is your training R-squared, and what does the gap "
            "say?",
     """0.3126 against 0.2511, a gap of 0.062. Mild overfitting, which
        is expected with 40 features on 794 rows and several dummies
        for very rare categories. It is not severe."""),

    ("3.5", "Did your stronger model beat linear regression?",
     """Not with standard settings. XGBoost at depth 3, learning rate
        0.05, 300 trees scored 0.2448 on test against linear's 0.2511,
        and 0.2162 on CV against 0.2344 -- worse on both, with a train
        R-squared of 0.6493 showing it memorised. Only after
        constraining it to depth 2, learning rate 0.03 and reg_lambda 5
        did it win, at 0.2821 CV."""),

    ("3.5", "Your random forest got 0.3164 on test. Is that a win?",
     """Not a trustworthy one. Its cross-validated R-squared is 0.2242,
        which is BELOW linear regression, and its train R-squared is
        0.8935. The test-set number is largely luck of that particular
        199-row draw. It is the clearest possible illustration of why a
        single split is not enough."""),

    ("3.5", "Why does this dataset punish a high-capacity model?",
     """993 rows, 40 features, 34 of them sparse dummies with some
        categories under ten members; a weak signal with a ceiling
        around R-squared 0.28; and a dominant relationship, gestation
        to birth weight, that is essentially linear. Boosting buys
        non-linearity and interactions, and there is very little of
        either to buy, so you pay the variance cost for almost no bias
        reduction."""),

    ("3.5", "Explain gradient boosting.",
     """Start from a constant prediction, the mean of y. Compute the
        gradient of the loss with respect to the current prediction for
        each row -- for squared error that is the residual. Fit a
        shallow tree to those gradients, add it to the running
        prediction scaled by the learning rate, and repeat. It is
        additive and sequential: each tree corrects the ensemble's
        current errors."""),

    ("3.5", "How does that differ from a random forest?",
     """A forest grows deep trees independently and averages them,
        reducing VARIANCE. Boosting grows shallow trees sequentially,
        each correcting the last, reducing BIAS. That is why boosting
        overfits more readily and why it is the wrong default on 993
        noisy rows."""),

    ("3.5", "What does XGBoost add over plain gradient boosting?",
     """A second-order expansion -- it uses the hessian as well as the
        gradient, so the optimal leaf weight is -G/(H+lambda), making it
        Newton boosting. Plus regularisation inside the split criterion
        via lambda and gamma, row and column subsampling, sparsity-aware
        splits with a default direction for missing values, and
        histogram binning for speed."""),

    ("3.5", "How did you choose your hyperparameters?",
     """Honestly: by comparing configurations. And if those comparisons
        were judged on the test set, then the test score is no longer
        unbiased -- I used it for selection. The correct procedure is to
        tune inside the training set with cross-validation via
        GridSearchCV, and touch the test set once at the end. For a
        fully unbiased estimate you need nested cross-validation."""),

    ("3.5", "If you scale features before cross-validating, what goes "
            "wrong?",
     """Fitting the scaler on the whole dataset lets each fold's
        validation rows influence the mean and SD used to transform
        them -- that is leakage. Wrapping the scaler and the model in a
        Pipeline makes the scaler refit inside each fold. It matters for
        Ridge, not for trees, which are scale-invariant."""),

    ("3.5", "What would you actually change to improve this model?",
     """Ordinal-encode income as bracket midpoints, which replaces nine
        columns with one and restores the ordering. Collapse marital to
        married/not, since it is 978 against 15. Collapse smoke to
        now/not-now, since Q2.3 showed the other three are
        indistinguishable. Use Ridge given the multicollinearity. And
        accept that the ceiling here is around 0.28."""),
]


# ======================================================================
#  REFERENCE SOLUTIONS
# ======================================================================

def q31_build():
    return D.build_xy()


def q33_fit(X_train, y_train):
    return D.fit_linear(X_train, y_train)


def q34_evaluate(model, X_test, y_test):
    m = D.metrics(model, X_test, y_test)
    return {k: round(v, 4) for k, v in m.items()}


def standardised_coefs(model, X_train, n=5):
    s = pd.Series(model.coef_, index=X_train.columns) * X_train.std()
    return s.reindex(s.abs().sort_values(ascending=False).index).head(n).round(4)


# ======================================================================
#  TRACES
# ======================================================================

def trace_encoding():
    df = D.load_clean()
    print()
    print("  %-9s %-6s %-8s %s" % ("column", "cats", "dummies", "baseline (dropped)"))
    print("  " + "-" * 66)
    total = 0
    for c in D.CATEGORICAL:
        cats = sorted(df[c].unique())
        total += len(cats) - 1
        n = int((df[c] == cats[0]).sum())
        flag = "   <-- only %d rows!" % n if n < 40 else ""
        print("  %-9s %-6d %-8d %r%s" % (c, len(cats), len(cats) - 1, cats[0], flag))
    print("  " + "-" * 66)
    print("  %d numeric + %d dummies = %d columns" % (len(D.NUMERIC), total,
                                                      len(D.NUMERIC) + total))


def trace_coefs():
    X, y = D.build_xy()
    Xtr, Xte, ytr, yte = D.split(X, y)
    m = D.fit_linear(Xtr, ytr)
    co = pd.Series(m.coef_, index=X.columns)
    sd = Xtr.std()
    std = co * sd
    order_raw = co.abs().sort_values(ascending=False).index
    rank_std = {k: i + 1 for i, k in
                enumerate(std.abs().sort_values(ascending=False).index)}
    rank_raw = {k: i + 1 for i, k in enumerate(order_raw)}
    print()
    print("  intercept: %.4f  (prediction when EVERY feature is 0)" % m.intercept_)
    print()
    print("  %-30s %8s %8s %8s %8s" % ("feature", "raw", "sd", "per SD", "rank"))
    print("  " + "-" * 68)
    for k in list(order_raw)[:8]:
        print("  %-30s %8.2f %8.2f %8.2f %4d->%-4d"
              % (k, co[k], sd[k], std[k], rank_raw[k], rank_std[k]))
    print("  %-30s %8.2f %8.2f %8.2f %4d->%-4d   <-- LOOK"
          % ("gestation", co["gestation"], sd["gestation"], std["gestation"],
             rank_raw["gestation"], rank_std["gestation"]))


def trace_metrics():
    X, y = D.build_xy()
    Xtr, Xte, ytr, yte = D.split(X, y)
    m = D.fit_linear(Xtr, ytr)
    from sklearn.metrics import r2_score
    mt = D.metrics(m, Xte, yte)
    pred = m.predict(Xte)
    err = np.abs(yte - pred)
    print()
    print("  MAE  = mean(|error|)        = %.4f oz  = %.0f g"
          % (mt["MAE"], mt["MAE"] * 28.3495))
    print("  RMSE = sqrt(mean(error^2))  = %.4f oz" % mt["RMSE"])
    print("  ratio RMSE/MAE              = %.3f  (>= 1 always, Jensen)"
          % (mt["RMSE"] / mt["MAE"]))
    print("  R2   = 1 - SSres/SStot      = %.4f" % mt["R2"])
    print()
    print("  baseline: always predict the mean -> MAE %.4f, R2 0.0"
          % np.abs(yte - ytr.mean()).mean())
    print("  train R2 %.4f   test R2 %.4f   gap %.4f"
          % (r2_score(ytr, m.predict(Xtr)), mt["R2"],
             r2_score(ytr, m.predict(Xtr)) - mt["R2"]))
    print()
    print("  worst 5 misses (|error| oz), with gestation:")
    idx = err.sort_values(ascending=False).head(5).index
    for i in idx:
        print("    error %6.1f   actual %3d   pred %6.1f   gestation %.0f d"
              % (err[i], yte[i], pred[list(yte.index).index(i)],
                 X.loc[i, "gestation"]))


def trace_cv():
    from sklearn.model_selection import KFold, cross_val_score
    from sklearn.linear_model import LinearRegression
    X, y = D.build_xy()
    kf = KFold(5, shuffle=True, random_state=42)
    cv = cross_val_score(LinearRegression(), X, y, cv=kf, scoring="r2")
    print()
    print("  5-fold cross-validated R2 for LinearRegression:")
    for i, s in enumerate(cv, 1):
        bar = "#" * int(s * 60)
        print("    fold %d  %.4f  %s" % (i, s, bar))
    print()
    print("    mean %.4f   sd %.4f   range %.4f to %.4f"
          % (cv.mean(), cv.std(), cv.min(), cv.max()))
    print()
    print("    the single reported test R2 was 0.2511 -- one draw from")
    print("    this distribution, sitting above the mean of %.4f." % cv.mean())


TRACES = {"3.1": trace_encoding, "3.2": trace_cv, "3.3": trace_coefs,
          "3.4": trace_metrics, "3.5": trace_cv}


# ======================================================================
#  YOUR TURN -- LIVE EDITS
# ======================================================================

# V1 | "What if you had not used drop_first?"
#    | Build X with drop_first controllable and return its shape.
#    |   (clean, True)  -> (993, 40)
#    |   (clean, False) -> (993, 47)
#    | Then be ready to say what breaks in the False case.
def build_x_shape(df, drop_first):
    pass


# V2 | "Rank the features fairly."
#    | Fit LinearRegression on (X_train, y_train), multiply each
#    | coefficient by that feature's standard deviation IN X_train,
#    | and return the top n as a Series sorted by absolute value
#    | descending, rounded to 4dp.
#    |   top 5 -> gestation 6.8544, drace_white 5.4607,
#    |            smoke_now -3.7342, drace_black 3.2679, height 2.9996
#    | This is the single most valuable Q3.3 live edit.
def top_std_coefs(X_train, y_train, n=5):
    pass


# V3 | "Give me the three metrics."
#    | Return {"MAE":..., "RMSE":..., "R2":...} for a FITTED model,
#    | each rounded to 4dp. Compute RMSE yourself from MSE -- do not
#    | assume a squared=False argument exists, it was removed in
#    | recent sklearn.
#    |   linear on the standard split -> 12.2751 / 15.5115 / 0.2511
def evaluate(model, X_test, y_test):
    pass


# V4 | "Do it properly with cross-validation."
#    | Return (mean, std) of k-fold R2, rounded to 4dp, using
#    | KFold(n_splits=k, shuffle=True, random_state=seed).
#    |   (LinearRegression(), X, y) -> (0.2344, 0.0656)
#    | Note shuffle=True matters -- without it the folds are
#    | contiguous slices of the file order.
def cv_r2(model, X, y, k=5, seed=42):
    pass


# V5 | "How overfit is it?"
#    | Fit the model, return (train_r2, test_r2, gap) each rounded to
#    | 4dp, where gap = train - test computed BEFORE rounding.
#    |   linear -> (0.3126, 0.2511, 0.0616)
def fit_gap(model, X_train, X_test, y_train, y_test):
    pass


# V6 | "Ordinal-encode income instead."
#    | Replace the nine inc dummies with ONE numeric column holding
#    | the midpoint of each bracket. Return the new X's shape.
#    | Use these midpoints (note '15000+' is open-ended -- pick 25000
#    | and be ready to defend the choice):
#    |   0-2500 1250, 2500-5000 3750, 5000-7500 6250,
#    |   7500-10000 8750, 10000-12500 11250, 12500-15000 13750,
#    |   15000-17500 16250, 17500-20000 18750, 20000-22500 21250,
#    |   15000+ 25000
#    |   -> (993, 32)     because 9 dummies become 1 column
def build_x_ordinal_income(df):
    pass


# ======================================================================
#  TESTS -- do not edit
# ======================================================================

_CLEAN = D.load_clean()
_X, _Y = D.build_xy(_CLEAN)
_XTR, _XTE, _YTR, _YTE = D.split(_X, _Y)
_LIN = D.fit_linear(_XTR, _YTR)


def _fresh_linear():
    from sklearn.linear_model import LinearRegression
    return LinearRegression()


_V1 = [
    ("drop_first=True", lambda f: f(_CLEAN, True), (993, 40)),
    ("drop_first=False", lambda f: f(_CLEAN, False), (993, 47)),
]

_V2 = [
    ("top 5", lambda f: list(f(_XTR, _YTR, 5).index),
     ["gestation", "drace_white", "smoke_now", "drace_black", "height"]),
    ("top 5 values", lambda f: [round(float(v), 4) for v in f(_XTR, _YTR, 5)],
     [6.8544, 5.4607, -3.7342, 3.2679, 2.9996]),
    ("top 1", lambda f: list(f(_XTR, _YTR, 1).index), ["gestation"]),
    ("length honoured", lambda f: len(f(_XTR, _YTR, 12)), 12),
]

_V3 = [
    ("linear on the split", lambda f: f(_LIN, _XTE, _YTE),
     {"MAE": 12.2751, "RMSE": 15.5115, "R2": 0.2511}),
    ("on the train set", lambda f: f(_LIN, _XTR, _YTR)["R2"], 0.3126),
]

_V4 = [
    ("linear 5-fold", lambda f: f(_fresh_linear(), _X, _Y), (0.2344, 0.0656)),
    ("k=3", lambda f: len(f(_fresh_linear(), _X, _Y, 3)), 2),
]

_V5 = [
    ("linear", lambda f: f(_fresh_linear(), _XTR, _XTE, _YTR, _YTE),
     (0.3126, 0.2511, 0.0616)),
]

_V6 = [
    ("shape", lambda f: f(_CLEAN), (993, 32)),
]


def main():
    argv = sys.argv
    mode = D.argmode(argv)
    qid = D.which(argv)
    ids = [qid] if qid in STATEMENTS else sorted(STATEMENTS)

    if mode == "teach":
        for q in ids:
            D.head("PART 3 :: Q%s" % q)
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
            D.head("PART 3 :: TRACE (Q%s)" % q)
            fn()
        return
    if mode in ("quiz", "answers"):
        D.head("PART 3 :: EXAMINER")
        pairs = [(("Q%s  " % q) + question, a)
                 for q, question, a in EXAMINER if q in ids]
        D.quiz(pairs, show=(mode == "answers"))
        return

    D.head("PART 3 -- Model Building & Evaluation")
    D.sub("reference solutions")
    D.check("q31 shapes", q31_build,
            [("X and y", lambda f: (f()[0].shape, f()[1].shape),
              ((993, 40), (993,)))])
    D.check("q32 split sizes", lambda: (_XTR.shape, _XTE.shape),
            [("794/199", lambda f: f(), ((794, 40), (199, 40)))])
    D.check("q33 intercept", lambda: round(float(_LIN.intercept_), 2),
            [("-94.18", lambda f: f(), -94.18)])
    D.check("q34 metrics", q34_evaluate,
            [("MAE/RMSE/R2", lambda f: f(_LIN, _XTE, _YTE),
              {"MAE": 12.2751, "RMSE": 15.5115, "R2": 0.2511})])

    D.sub("your live edits")
    D.report([
        D.check("V1 build_x_shape", build_x_shape, _V1),
        D.check("V2 top_std_coefs", top_std_coefs, _V2),
        D.check("V3 evaluate", evaluate, _V3),
        D.check("V4 cv_r2", cv_r2, _V4),
        D.check("V5 fit_gap", fit_gap, _V5),
        D.check("V6 build_x_ordinal_income", build_x_ordinal_income, _V6),
    ])


if __name__ == "__main__":
    main()
