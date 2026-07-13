# Scope map

## Preserved repository scope

The repository fixes target `THM-M-0979`, the title `Bernstein inequality`, the attribution Sergei
Bernstein, the year 1924, and the gloss "tail probability of a sum." This identifies a probability
inequality family for sums. It does not identify one truth-valued proposition.

The row occurs in the counting-combinatorics section even though its content is probabilistic. A
second source row, retained independently as `THM-M-0995` in probability fundamentals, uses the
translated Chinese title but has the same attribution, year, gloss, importance, and claimed
formalization status. The two IDs remain distinct authority records unless the master lane performs
an explicit target-set correction. Intake neither merges them nor assigns one target's proposition
or evidence to the other.

## Candidate surfaces, not credited

The inspected modern source and the foreign target expose several materially different surfaces:

1. Independent mean-zero subexponential summands, with a two-regime bound controlled by the
   individual subexponential norms and an unspecified absolute constant.
2. A weighted subexponential corollary with Euclidean and maximum coefficient norms.
3. Independent mean-zero almost-surely bounded summands, with variance of the sum and the bound
   entering a denominator of the form `sigma^2 + K*t/3`; the inspected text displays prefactor `2`.
4. `THM-M-0995`'s repo-local candidate for bounded independent centered real summands, a variance
   budget, and one-sided upper tail with prefactor `1`.
5. Lower-tail, two-sided absolute-tail, moment-condition, martingale/Freedman, vector, matrix, and
   other results also called Bernstein inequalities.

No candidate is the canonical claim for `THM-M-0979` at intake.

## Proposition-changing decisions

An admitted source and accountable duplicate-scope review must freeze all of the following before
the statement phase can select a target:

1. Whether `THM-M-0979` owns an independent mathematical root, aliases the same semantic root as
   `THM-M-0995` without sharing state, or should be removed by a future authoritative target-set
   correction. A worker cannot make that target-set decision.
2. The summand domain and codomain, finite index representation, common probability space, and all
   universe and measurability conventions.
3. Independence versus martingale or other dependence assumptions; centering; integrability or
   moment hypotheses; almost-sure boundedness; and whether bounds are common or summand-specific.
4. The variance quantity: exact sum of variances, an upper budget, conditional variance, second
   moment, or a subexponential proxy.
5. Upper, lower, or two-sided tail; strict or non-strict event inequality; threshold domain; and
   any leading prefactor such as `1` or `2`.
6. The exact exponent, constants, denominator normalization, and whether an absolute constant is
   explicit or existential.
7. Ordered binders and all edge cases, including an empty family, zero threshold, zero summand
   bound, zero variance, a zero denominator under Lean's totalized division, deterministic
   variables, and null or non-probability measures.
8. The approved historical or modern source edition, theorem locator, incorporated definitions,
   proof boundary, translation and genealogy, corrections and errata, and independent review.

## Explicit exclusions

- Hoeffding, Bennett, or Chernoff bounds presented as Bernstein merely because they are nearby
  concentration inequalities or possible proof ingredients.
- The `THM-M-0995` statement, task state, or proof artifacts copied into this target without a
  reviewed cross-target ownership and exact-proposition decision.
- A subexponential, martingale, vector, matrix, polynomial-approximation, or PDE Bernstein theorem
  silently substituted for the unidentified scalar sum-tail root.
- A fixed distribution, fixed number of summands, finite computation, numerical experiment, or
  asymptotic slogan presented as the universal theorem.
- A structure or hypothesis storing the requested tail conclusion, or an MGF/Chernoff anchor
  presented as if it closed the Bernstein-specific bridge.
- The catalog's untrusted `verified` label, a citation, a URL, a `#check`, or the intake candidate
  proposition used as source-fidelity or proof evidence.

## Neighbor and ownership boundaries

`THM-M-0977` owns the neighboring Chernoff bound, `THM-M-0978` the Hoeffding inequality, and
`THM-M-0980` the Bennett inequality. `THM-M-0995` is the duplicate-looking probability-category
Bernstein row. Each has independently owned scope, tasks, and evidence. They may become explicit
dependencies or share a deduplicated semantic obligation only after review; proximity and matching
metadata grant no status.

## Formal boundary

Pinned mathlib provides MGFs and CGFs, Chernoff bounds, sub-Gaussian sum bounds, mutual
independence, variances, and variance-of-independent-sum infrastructure. These are credible
ingredients, not a terminal Bernstein theorem. The probe's prefactor-parameterized bounded-tail
shape records expressibility only. Exact minimal imports, the canonical expression, checked
transports, mutation tests, exhaustive candidate provenance, and proof-body trust remain downstream.
