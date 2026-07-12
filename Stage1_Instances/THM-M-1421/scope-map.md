# Scope map

## Preserved theorem family

- A smooth dynamical system on a finite-dimensional compact Riemannian manifold.
- An invariant measure in the class fixed by the accepted source, with its probability,
  normalization, regularity, and relation to Riemannian volume stated explicitly.
- Kolmogorov-Sinai or metric entropy of the measure-preserving transformation, not topological,
  Shannon, binary, cover, partition-cardinality, or differential entropy.
- Lyapunov characteristic exponents of the derivative cocycle, with the time direction, sign,
  multiplicities, exceptional set, and integrability convention fixed.
- The exact source equality between entropy and an integral of the exponent sum.

These bullets delimit the intended family. They do not select or assert a canonical proposition.

## Decisions required at statement freeze

1. The primary theorem and definition chain: the leading candidate is Pesin 1977, Section 5,
   Theorem 5.1, but its standing definitions in Sections 1 and 3, corrections, and translation must
   be mapped before its formula becomes authoritative.
2. The dynamical object: discrete diffeomorphism versus flow, differentiability class (`C^2` in
   the candidate), invertibility, compactness, boundary assumptions, and whether a modern
   `C^{1+alpha}` extension is in or out.
3. The measure: normalized smooth measure compatible/equivalent with Riemannian volume in the
   candidate, versus a general absolutely continuous, SRB, ergodic, or invariant probability
   measure. These are not interchangeable without checked implications.
4. The entropy convention: metric/Kolmogorov-Sinai entropy, its definition through finite
   measurable partitions, logarithm base, value type, finiteness, completion, and normalization.
5. The derivative cocycle and spectrum: tangent-space model, forward or inverse iterates,
   Oseledets hypotheses, ordinary versus extended-real exponents, pointwise multiplicities, and
   whether one common conull set supports all data.
6. The formula orientation. Theorem 5.1 prints minus the sum of negative forward characteristic
   exponents; the introduction describes the sum of positive exponents. Their equivalence requires
   a checked inverse/time-reversal/sign and entropy-invariance bridge, not a prose rewrite.
7. Boundary cases: zero exponent, no negative or positive exponents, the candidate's empty-sum
   convention, nonergodic point-dependent spectra, nonintegrable sums, and infinite entropy.

## Explicit exclusions

- Ruelle's inequality as a substitute for equality, or an equality structure assumed as input.
- An Oseledets theorem that establishes exponents and splitting but not the entropy formula.
- Topological cover entropy from pinned mathlib as if it were measure-theoretic entropy.
- Shannon binary/q-ary entropy or a finite partition entropy without the Kolmogorov-Sinai
  supremum/refinement and source-specific normalization.
- A constant-matrix determinant identity, linear-cocycle norm-growth calculation, or numerical
  finite-time Lyapunov estimate.
- A theorem for uniformly hyperbolic/Anosov maps, one-dimensional interval maps, SRB measures, or
  noninvertible maps silently substituted for the selected smooth-measure diffeomorphism theorem.
- The separately scheduled Lyapunov-exponent, Oseledets, and broad Pesin-theory targets as proof
  credit for this entropy equality.
- The repository label `已验证`, a paper citation, or successful adjacent API checks as H0 or M0.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides measure-preserving maps,
topological cover entropy, manifold derivatives, integration, and finite sums, but the bounded
intake search found no Pesin/Lyapunov/Oseledets or metric-entropy target interface. The Lean probe
records substrate and a crucial mismatch boundary only; it is not the statement or an anchor audit.
