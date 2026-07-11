# Source-statement crosswalk

## Repository sources inspected

`Docs/researches/math_theorems.md` supplies only the Chinese phrase "曲线上小高度的点", the
attribution, and the year 1992. `Docs/Stage0_Blueprint.md` repeats that phrase and explicitly leaves
the precise definitions and hypotheses open. Its "已验证" label is metadata, not source or kernel
evidence.

## Primary-source discovery candidates

- Shouwu Zhang, *Positive line bundles on arithmetic varieties*, Journal of the American
  Mathematical Society 8 (1995), 187-221. This is a likely source family for height inequalities
  and successive minima, but the intake has not verified that it is the intended named theorem.
- Shouwu Zhang, *Small points and adelic metrics*, Journal of Algebraic Geometry 4 (1995),
  281-300. This is a likely small-points source family, but it must not be conflated with the
  separately queued equidistribution result.

These are discovery anchors only. Exact editions, theorem numbers/pages, wording, assumptions,
errata, and bibliographic fit to the repository's 1992 date remain unverified, so neither is H0.

## Crosswalk

| Repository component | Required source resolution | Required Lean surface | Status |
|---|---|---|---|
| "curve" | type of curve and base field | concrete curve/scheme model | open |
| "height" | divisor/line bundle, metric, normalization | pinned height definition | open |
| "small" | bound, essential minimum, or limiting condition | exact inequality/quantifier | open |
| "points" | rational/algebraic/geometric points | exact point type and field extension | open |
| theorem conclusion | existence/finiteness/density/inequality | exact proposition | open |

The statement phase must select a primary theorem and produce a row-by-row assumption crosswalk.
If no source uniquely matches the metadata, it must retain M4 and report the identification blocker
rather than broaden or substitute the claim.

