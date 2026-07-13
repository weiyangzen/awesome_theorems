# Scope map

## Preserved catalog family

The intake preserves the Azuma-Hoeffding concentration family for real martingale differences. The
catalog's four-word gloss does not select one proposition, so the following are candidate roots,
not statements or proof claims:

1. A finite-horizon one-sided upper-tail bound for a sum of conditionally sub-Gaussian martingale
   differences.
2. The classical bounded-difference corollary, using deterministic almost-sure bounds on each
   martingale increment.
3. A two-sided absolute-tail form derived from upper and lower tails.
4. One of Azuma's original weighted-sum exponential-moment or asymptotic results.

## Statement decisions

Before elaboration, an admitted source and independent review must fix:

- whether the root is a martingale, its increment sequence, or a strongly adapted process;
- finite horizon versus an asymptotic weighted-sum conclusion;
- the probability space, measure normalization, filtration, adaptedness, integrability, and
  conditional-expectation conventions;
- deterministic symmetric bounds `|Y_k| <= c_k`, predictable interval bounds, or conditional
  sub-Gaussian parameters, including the exact conversion and exponent constant;
- weighted versus unweighted sums and the indexing of the initial term;
- one-sided upper tail, lower tail, or two-sided absolute tail, and whether the others are checked
  descendants;
- real-valued variables, finite index encoding, event measurability, and real/extended-real
  probability coercions;
- ordered binders, universes, `n = 0`, threshold zero, zero variance proxy, zero bounds, and all
  almost-sure exceptional-set scopes;
- the precise relationship to Hoeffding's lemma and the reason for the joint attribution.

No degenerate case is excluded at intake.

## Pinned Lean candidate

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Probability.Moments.SubGaussian` provides:

```text
ProbabilityTheory.measure_sum_ge_le_of_hasCondSubgaussianMGF
```

It assumes a standard Borel sample space, a zero-or-probability measure, a natural-number
filtration, a strongly adapted real process `Y`, an ordinary sub-Gaussian MGF bound for `Y 0`, and
conditional sub-Gaussian MGF bounds for `Y (i+1)`. For `epsilon >= 0`, it bounds the upper-tail
probability of `sum_{i<n} Y_i` by
`exp (-epsilon^2 / (2 * sum_{i<n} c_i))`.

The companion theorem `HasSubgaussianMGF.sum_of_hasCondSubgaussianMGF` supplies the sum's MGF
bound. Hoeffding's lemma `hasSubgaussianMGF_of_mem_Icc_of_integral_eq_zero` supplies an ordinary
bounded centered-variable interface, but no source-approved conditional bounded-increment bridge
or checked identity with the catalog root is frozen here. The candidate therefore supports `M3`
feasibility only, not `M0-*` or proof-body credit.

## Explicit exclusions

- The separate `THM-M-1080` Azuma dossier or any of its artifacts used as inherited evidence.
- Independent-variable Hoeffding concentration with no filtration or conditional structure.
- McDiarmid bounded differences, Freedman/Bernstein variance-sensitive bounds, maximal
  inequalities, convergence theorems, or laws of the iterated logarithm used as the root.
- A uniform-bound special case silently substituted for varying deterministic bounds.
- A conditional sub-Gaussian assumption silently presented as identical to an almost-sure
  bounded-increment assumption, or conversely.
- A structure or premise that stores the desired tail inequality, MGF conclusion, or transport as
  input data.
- The theorem name, catalog duplicate, `#check`, source URL, or untrusted verified label used as
  proof or source-fidelity credit.

## Ownership boundary

`THM-M-1080` is a separate manifest target named Azuma's inequality; `THM-M-0978` owns Hoeffding's
inequality for independent bounded variables; `THM-M-0976` owns McDiarmid's inequality. They may
later provide explicit dependency nodes, but no statement or status transfers by topic overlap.
