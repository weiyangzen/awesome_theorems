# Scope map

## Preserved theorem family

The repository fixes the following family and no more:

- concentration of a finite sum of bounded random variables;
- attribution to Wassily Hoeffding and the year 1963;
- a probabilistic inequality despite this record's enumerative-combinatorics category; and
- a Lean 4 target to be selected only after the source and duplicate-ID boundaries are approved.

Hoeffding's inspected Theorem 2 is a precise candidate: for independent `X_1, ..., X_n` satisfying
pointwise bounds `a_i <= X_i <= b_i` and `t > 0`, it bounds the upper tail of the sample average
above its expectation. This is a source locator, not the canonical statement frozen by intake.

## Proposition-changing decisions

The source and statement phases must settle all of the following before an exact target is frozen:

1. Whether `THM-M-0978` and the near-verbatim `THM-M-0994` remain two encodings, are deduplicated,
   or receive distinct source propositions. This worker does not change the target set or allocate
   another target's statement.
2. Whether the root is Hoeffding 1963 Theorem 2, the equal-range special case in Theorem 1, a
   lower-tail or two-sided corollary, or another bounded-sum result in the paper.
3. A natural-number initial segment, a nonempty `Fin n`, or an arbitrary finite index type, and
   the exact relationship between those encodings.
4. A probability space, measurable real random variables, mutual independence, and the precise
   measurability and integrability hypotheses used to define every expectation and event.
5. Pointwise bounds as printed in Theorem 2 versus almost-sure bounds used by the pinned Hoeffding
   lemma, including a checked source-to-measure-theoretic transport.
6. The sample-average form `P(Xbar - mu >= t)` with `t > 0` versus the centered-sum form with
   `epsilon = n*t`; any extension to `epsilon >= 0` requires an explicit boundary argument.
7. The exact exponent and its normalization: `-2*n^2*t^2 / sum_i (b_i-a_i)^2` for the average,
   or the checked centered-sum equivalent `-2*epsilon^2 / sum_i (b_i-a_i)^2`.
8. Whether lower and upper endpoints must satisfy `a_i <= b_i` explicitly or whether nonempty
   pointwise or almost-sure interval membership supplies that condition.
9. Whether lower-tail, two-sided absolute-tail, equal-width, identically distributed, weighted,
   sampling-without-replacement, or dependent-variable results are root content or later
   corollaries.
10. Every universe, ordered binder, typeclass, coercion, foundation/TCB profile, and alternate
    encoding with its checked directional relationship.

## Boundary cases

- `n = 0`, which the source's average notation does not admit, versus an empty finite Lean family.
- `n = 1` and deterministic or constant variables.
- `t = 0` and `t < 0`; the source explicitly states `t > 0` and says no nontrivial general upper
  bound exists for nonpositive `t` under its assumptions.
- Zero-width intervals and zero total squared width, including the meaning of real division by
  zero in a candidate Lean expression.
- Reversed or inconsistent endpoints and vacuous almost-sure interval premises.
- Null events, atoms exactly on the threshold, and closed versus strict tail events.
- Pointwise bounds on all outcomes versus bounds outside a null set.

No case is excluded at intake because no canonical proposition has been selected.

## Explicit exclusions

- The Azuma-Hoeffding inequality for martingale differences.
- McDiarmid's bounded-differences inequality for a function of independent inputs.
- Generic Chernoff, Bernstein, Bennett, Janson, Kim-Vu, or Talagrand inequalities.
- A bounded or sub-Gaussian assumption that directly stores the desired tail conclusion.
- An iid-only, equal-width-only, symmetric, two-sided, fixed-dimension, or numerical special case
  used as the unrestricted root.
- Sampling-without-replacement or U-statistic extensions used in place of the independent-summand
  theorem.
- `THM-M-0994`, `S1_M_274.lean`, a pinned declaration, theorem name, URL, or the catalog's
  untrusted verified label used as inherited target identity or proof credit.

## Neighbor boundary

`THM-M-0975` owns Azuma-Hoeffding, `THM-M-0976` McDiarmid, `THM-M-0977` Chernoff,
`THM-M-0979` Bernstein, and `THM-M-0980` Bennett. `THM-M-0994` is a near-verbatim duplicate
Hoeffding record in the probability category. Their artifacts may inform later source and formal
audits but cannot supply accepted state to this target by proximity.
