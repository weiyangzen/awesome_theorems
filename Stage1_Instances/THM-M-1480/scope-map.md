# THM-M-1480 scope map

## Catalog scope preserved

- Target identity: `THM-M-1480`, named `拟Monte Carlo方法`.
- Catalog attribution and date: Harald Niederreiter, 1978.
- Literal gloss: `低差异序列的积分` (integration using low-discrepancy sequences).
- Recognizable topic boundary: deterministic numerical integration whose sample sites are chosen
  for a distribution-quality property rather than independent random sampling.

This identifies a quasi-Monte Carlo theorem family, not one mathematical proposition.

## Decisions required before statement freeze

An accountable source correction must select one immutable proposition and freeze:

1. Whether the sampling object is a finite ordered point set, multiset, or the first `N` points of
   an infinite sequence, including whether duplicates matter.
2. Dimension, scalar field, and domain: normally a unit cube such as `[0,1)^s` or `[0,1]^s`, but
   endpoints, product representation, measure normalization, and any transformation to another
   domain must be explicit.
3. The distribution predicate: star discrepancy, extreme discrepancy, `L^p` discrepancy, isotropic
   discrepancy, a digital-net parameter, uniform distribution, or another source-defined notion.
4. The integrand class and regularity quantity: Hardy-Krause variation with an exact anchoring
   convention, one-dimensional Jordan variation, Sobolev or reproducing-kernel norm, Lipschitz or
   bounded-variation condition, periodicity, weights, measurability, and integrability.
5. The quadrature estimator: normalization by `N`, indexing convention, exact finite sum, equal or
   unequal weights, treatment of repeated/boundary points, and the intended integral.
6. The conclusion: a finite-`N` error bound, convergence, asymptotic rate, tractability statement,
   existence or construction of point sets, or a randomized mean-square/probability result.
7. Every constant, norm, absolute-value convention, strict or non-strict inequality, logarithm and
   discrepancy normalization, dimension dependence, and whether a rate is uniform over a class.
8. Quantifier order, zero dimension, `N = 0`, empty samples, constant or nonintegrable functions,
   zero variation, endpoints of half-open boxes, exact versus floating-point arithmetic, and any
   computation or certificate boundary.

These choices change truth conditions and proof obligations. They are a resolution checklist, not
a candidate statement.

## Candidate families not credited

- The Koksma-Hlawka inequality bounding equal-weight quadrature error by Hardy-Krause variation
  times star discrepancy.
- Convergence of sample averages for a uniformly distributed sequence and an appropriate
  Riemann-integrable or continuous integrand class.
- A discrepancy bound for a named low-discrepancy construction combined with an integration rate.
- Weighted, randomized, scrambled, lattice-rule, digital-net, or infinite-dimensional variants.

No candidate is selected, combined, or credited at intake. In particular, the 1978 Niederreiter
survey title does not by itself identify which definition or theorem the catalog author intended.

## Neighbor ownership and exclusions

- `THM-M-1479` owns the broader random-sampling Monte Carlo method topic. It contributes no source,
  statement, probability estimate, or proof credit to this deterministic target.
- The catalog's nearby MCMC and Metropolis-Hastings entries own stochastic Markov-chain methods and
  cannot substitute for a quasi-Monte Carlo integration theorem.
- A generic integral, finite sum, average, uniform probability distribution, Riemann-sum
  convergence theorem, bounded-variation definition, or discrepancy structure that assumes the
  desired inequality is substrate only.
- Numerical experiments, convergence tables, sampled discrepancy values, floating-point outputs,
  or the catalog label `已验证` provide no human-source or kernel evidence.

## Pinned Lean boundary

Pinned mathlib contains Bochner integral averages, integration against sums of Dirac masses,
uniform probability distributions, and box-integral Riemann-sum convergence machinery.
`IntakeProbe.lean` authenticates representative declarations. Bounded repository and pinned-mathlib
searches found no quasi-Monte Carlo, low-discrepancy, star-discrepancy, Koksma-Hlawka, or
equidistributed-sequence target declaration. This is bounded intake discovery, not an exhaustive
external anchor audit or a proof of global absence.

No canonical Lean target, checked transport, expression fingerprint, discovery-protocol hash,
obligation registry, or proof state is frozen in this phase.
