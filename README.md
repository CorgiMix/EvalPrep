# EvalPrep

Study material for a Python programming final task: a pandas/scikit-learn
analysis of the **Child Health and Development Studies** birth-weight data,
plus the ten LeetCode problems that accompany it.

The grading is **20% written code, 80% live viva** — you have to explain your
logic, interpret the data, and adapt the code on request. So every file here
is built around explaining and changing code rather than producing it.

Every number in every lesson is computed from the actual data file. Nothing is
transcribed from the assignment brief — and where the brief and the data
disagree, the files say so.

---

## Layout

```
notebook/          the assignment
  _data.py           loaders + the marking harness
  dataset.py         the data itself: provenance, live numbers, landmines
  part1.py           Q1.1 - Q1.4   Python fundamentals      10 pts
  part2.py           Q2.1 - Q2.6   pandas                   20 pts
  part3.py           Q3.1 - Q3.5   modelling & evaluation   40 pts
  run_all.py         progress board + study triage

leetcode/          the ten problems, grouped by pattern
  _harness.py        test runner
  lc344, lc125       two pointers converging
  lc027, lc283       read/write pointer
  lc001, lc217       hash map / set
  lc121, lc268       one pass, running state
  lc021, lc028       linked lists; substring search
  run_all.py         progress board + study order
```

## Usage

Every file takes the same flags:

```bash
python notebook/part3.py --teach 3.5    # the full lesson for one question
python notebook/part3.py --trace 3.3    # instrumented walkthrough, real numbers
python notebook/part3.py --quiz         # examiner questions
python notebook/part3.py --answers      # ... with model answers
python notebook/part3.py                # mark your own live-edit attempts

python notebook/run_all.py --plan       # what to study, in what order
python leetcode/run_all.py --plan       # pattern order, not numeric order
```

Start here:

```bash
python notebook/dataset.py --traps
python notebook/run_all.py --plan
```

## Exercises

Stubs are left for you to fill in — **40** adaptation variants across the ten
LeetCode problems, **16** live-edit drills across the notebook. Each one is a
plausible "now change it" from an assessor. Running a file marks your attempts
and reports anything still unattempted.

All 56 have been verified against reference solutions, so the expected values
are checked rather than asserted.

## Notes on the data

Child Health and Development Studies — pregnancies in the Kaiser Foundation
Health Plan, Oakland, California, roughly 1960-1967. 1,236 births, reduced to
993 complete cases across 14 columns.

Source: [Rdatasets — mosaicData::Gestation](https://vincentarelbundock.github.io/Rdatasets/doc/mosaicData/Gestation.html)

A few things the analysis turns up that the brief does not mention:

- The sample is pre-filtered — every baby is male, every birth a live singleton
  — so three columns are constant and get dropped. That limits what the model
  can generalise to.
- `bwt` is in **ounces** and `gestation` in **days**. Mean birth weight is
  119 oz = 3,375 g = 7 lb 7 oz.
- Dropping the father's height/weight as *columns* leaves 993 rows; dropping
  those rows instead leaves 593. Two columns cost 400 rows.
- The smoking effect is specific to smoking *during* the pregnancy. Mothers who
  quit — even at conception — are indistinguishable from never-smokers.
- `get_dummies(drop_first=True)` drops the alphabetically first category. For
  `marital` that is `divorced`, which has **two** rows.
- Raw regression coefficients are not comparable across features. Scaled by
  standard deviation, `gestation` moves from 35th to 1st.
- A default-configuration gradient booster does **not** beat linear regression
  on this data. Only a heavily regularised one does.

`gestation_raw.csv` is committed so the numbers reproduce exactly; `_data.py`
falls back to downloading it if absent.

## Requirements

Python 3.11+, `pandas`, `scikit-learn`, `numpy`. `xgboost` is optional and used
only in the Part 3 model comparison.
