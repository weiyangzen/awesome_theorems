# Scope map

## Preserved theorem family

- Target: `THM-M-0980`, named `Bennett不等式` (Bennett's inequality).
- Catalog attribution and date: George Bennett, 1962.
- Literal gloss: `随机变量和的尾概率` ("tail probability of a sum of random variables").
- Historical source-family lead: George Bennett, *Probability Inequalities for the Sum of
  Independent Random Variables*, JASA 57(297), 33-45 (1962), DOI
  `10.1080/01621459.1962.10482149`.
- Conventional topic: exponential concentration bounds for sums of independent random variables
  under boundedness and moment or variance assumptions.

The final bullet disambiguates the named family for planning only. Neither the catalog nor an
admitted source selects one exact proposition.

## Decisions required at statement freeze

An immutable, independently reviewed source must decide all of the following before a canonical
Lean expression may be credited:

1. Whether the index set is `Fin n`, a finite set, or another finite or countable family, and
   whether the variables are identically distributed.
2. The probability space, measurability and integrability assumptions, independence notion, and
   whether the variables are centered or are centered inside the conclusion.
3. Whether boundedness is one-sided (`X_i <= b_i`), two-sided (`|X_i| <= b_i`), or expressed by
   another moment condition, and whether the bound is common or summand-specific.
4. Whether the variance parameter is the exact sum of variances, an upper bound for it, a sum of
   second moments, or another variance proxy.
5. The exact rate function, normalization, constants, exponent sign, and placement of any common
   bound. A familiar formula must not be chosen without a source crosswalk.
6. Whether the conclusion is an upper tail, lower tail, two-sided absolute tail, or maximum-of-
   partial-sums event; whether the comparison is strict or non-strict; and whether probability is
   represented in `ENNReal` or `Real`.
7. Exact ordered binders, universes, typeclass assumptions, foundation and TCB profiles, credited
   alternate encodings, and checked transport directions.

## Degenerate and boundary cases

The selected source and Lean expression must explicitly resolve the empty family, threshold zero,
zero common bound, zero variance proxy, deterministic variables, zero denominators, the value of
the rate function at zero, and any limiting convention needed when a quotient is undefined as an
ordinary real expression. Negative thresholds and negative bounds must either be ruled out by
explicit hypotheses or handled by the exact proposition. Null events, almost-everywhere versus
pointwise bounds, and equality at the tail threshold also require source-mapped decisions.

No degenerate case is silently excluded at intake.

## Explicit exclusions and non-substitutions

- Bernstein's inequality, Hoeffding's inequality, Chernoff's bound, Azuma-Hoeffding, McDiarmid,
  Freedman, and sub-Gaussian or sub-exponential concentration results are related but distinct.
- A Poisson, binomial, Gaussian, scalar one-variable, identically distributed, fixed-dimension, or
  numerical special case cannot replace the selected general claim.
- A statement using the Bernstein relaxation of a Bennett rate is not Bennett's exact rate merely
  because one inequality can be derived from the other.
- A theorem that assumes the required MGF or tail estimate as a premise supplies no proof of that
  estimate from boundedness and variance assumptions.
- An MGF definition, Chernoff wrapper, independence product rule, variance-sum identity, theorem
  name, search hit, numerical experiment, or `#check` is infrastructure or discovery evidence, not
  the root theorem.
- The catalog's `已验证` label, a citation without a pinpoint statement, an axiom, placeholder,
  unsafe injection, unchecked certificate, or oracle supplies no H or M completion credit.

## Neighbor and category boundaries

The manifest places this record in `组合数学 / 计数组合`, while the duplicate catalog wording also
appears immediately before the `概率论与随机过程` section. This category inconsistency is metadata
provenance, not permission to replace the probability inequality with a combinatorial theorem.
Neighboring records separately own Chernoff, Hoeffding, Bernstein, Azuma-Hoeffding, and McDiarmid
inequalities. Their artifacts provide no statement identity or proof credit for this target.

## Formal boundary

Pinned mathlib exposes `ProbabilityTheory.mgf`, `ProbabilityTheory.cgf`, Chernoff upper-tail bounds,
`ProbabilityTheory.iIndepFun.mgf_sum`, and `ProbabilityTheory.IndepFun.variance_sum`. Intake checks a
small representative surface only. The statement phase must first freeze a source-faithful root;
the later anchor audit must then search and classify exact proof bodies, dependencies, axioms,
placeholders, unsafe or oracle boundaries, and transports without substituting a related bound.
