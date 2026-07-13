# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:7141-7146` records:

- title: `Hoeffding inequality`;
- attribution: Wassily Hoeffding;
- year: 1963;
- gloss: `concentration of sums of bounded random variables`;
- importance: high; and
- untrusted formalization status: `verified`.

All six uncited lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, formula,
ordered binders, hypotheses, definitions, proof boundary, correction history, reviewer, or formal
artifact. `Docs/Stage0_Blueprint.md:26659-26684` repeats the gloss while explicitly leaving the
formal system, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine state, and artifact links open. These records establish target-family identity only.

## Duplicate catalog record

`Docs/researches/math_theorems.md:7266-7271` separately records `THM-M-0994` as
`Hoeffding inequality` in Chinese transliteration, with the same author, year, literal gloss,
importance, and untrusted status. Both records arrived in the same catalog commit. The target
manifest assigns `THM-M-0994` to probability foundations and the legacy slot `S1-M-274`, while
this target remains in enumerative combinatorics without a legacy slot. Category and scheduling do
not provide a mathematical allocation rule.

The current `THM-M-0994` dossier and `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_274.lean`
contain exact-topic statements and wrappers. They are discovery inputs owned by another target,
not source authority or transferable accepted state. The integration lane must decide whether the
two records are retained as distinct encodings, reconciled, or deduplicated before this target's
canonical statement is accepted.

## Inspected primary-source lead

Wassily Hoeffding, *Probability Inequalities for Sums of Bounded Random Variables*, *Journal of
the American Statistical Association* 58(301) (1963), pages 13-30, DOI
`10.1080/01621459.1963.10500830`.

A 25-page scan hosted by the North Carolina State University repository was inspected at
`https://repository.lib.ncsu.edu/server/api/core/bitstreams/d0e6ed15-3e1c-432f-8419-e55ffb6f3171/content`.
The observed file was 891,780 bytes with SHA-256
`e4c1f30fef09d420bc4b791a53f95cb461f47b363d0d9debaf13e15fbaaef203`.
It is a 1962 University of North Carolina Institute of Statistics mimeograph corresponding to the
1963 journal article; the scan title page says May 1962 and Mimeo Series No. 326. The catalog gives
the publication year 1963. Host repository, issuing institution, edition identity, and any
journal/mimeograph differences must therefore be distinguished and reviewed rather than silently
equated.

The introduction, printed page 1, defines independent random variables `X_1, ..., X_n`, their sum
`S`, average `Xbar = S/n`, and `mu = E Xbar = E S / n`. It says the paper studies
`P(Xbar - mu >= t) = P(S - E S >= n*t)` for `t > 0` when each range is bounded or bounded above.

Theorem 2, printed page 6, scan PDF page 7, equation (2.10), states: if `X_1, ..., X_n` are
independent and `a_i <= X_i <= b_i`, then for `t > 0`,

```text
P(Xbar - mu >= t)
  <= exp(-2 * n^2 * t^2 / sum_{i=1}^n (b_i - a_i)^2).
```

Section 3 proves Theorem 2 on printed pages 12-13. It applies the exponential Markov bound and
independence, then a convexity/Taylor estimate for each centered bounded summand, obtaining
equation (3.17) and optimizing at `h = 4*n*t / sum_i (b_i-a_i)^2`. This identifies a complete
human proof route and supports provisional `H1`.

It is not `H0`: the catalog does not cite or pinpoint Theorem 2, the paper contains several
bounded-sum inequalities and dependent-sum extensions, the mimeograph/journal relationship and
corrections or errata have not been independently audited, no independent reviewer is recorded,
and the source's pointwise, average, positive-threshold formulation has not been approved and
transported to one exact modern measure-theoretic statement for this duplicate ID.

## Clause crosswalk

| Clause | Source | Prospective Lean surface | Status |
|---|---|---|---|
| bounded variables | pointwise `a_i <= X_i <= b_i` | real measurable functions with pointwise or AE `Set.Icc` membership | pointwise/AE transport open |
| sum concentration | average tail equals centered-sum tail | finite sum of `X_i - integral X_i` | index and normalization open |
| independence | explicit in Theorem 2 | `ProbabilityTheory.iIndepFun X mu` | exact encoding open |
| upper tail | `P(Xbar - mu >= t)` | `mu.real {omega | epsilon <= sum_i (...)}` | candidate only |
| threshold | `t > 0` | real `t` or `epsilon` | boundary transport open |
| exponent | `-2*n^2*t^2 / sum (b_i-a_i)^2` | centered form with `epsilon = n*t` | algebraic transport open |
| 1963 attribution | JASA article and 1962 mimeograph | no Lean content | edition review open |
| `verified` | no evidence accompanies label | no declaration | no H or M credit |

## Pinned Lean candidates, not credited

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Probability.Moments.SubGaussian` contains:

- `ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun`, a finite-family upper-tail
  bound for independent sub-Gaussian real variables;
- `ProbabilityTheory.HasSubgaussianMGF.measure_sum_range_ge_le_of_iIndepFun`, an initial-segment,
  common-parameter form;
- `ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc_of_integral_eq_zero`, Hoeffding's lemma for an
  almost-surely bounded centered variable; and
- `ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc`, the centered corollary for an almost-surely
  bounded variable.

`IntakeProbe.lean` authenticates all four declarations in the pinned environment and prints axiom
reports for the general finite-sum bound and the centered bounded-variable lemma. The declarations
make `M3` appropriate at intake, but they do not select this target's proposition. Their source
match, terminal bodies, exact assumptions, denominator-zero semantics, trust and dependency
closure, and relationship to the other Hoeffding target require the downstream statement and
anchor audits.

## Required closure

Before H0 or the Lean statement gate, accountable reviewers must select and preserve one exact
source edition and theorem, reconcile the 1962 mimeograph and 1963 publication, audit corrections
and errata, map every definition, binder, premise, conclusion, proof step, and boundary case, and
approve an allocation for `THM-M-0978` versus `THM-M-0994`. A formal reviewer must then encode that
same proposition with minimal pinned imports, serialize the expression and environment
fingerprints, compile every credited transport, and execute the four required mutation classes.
