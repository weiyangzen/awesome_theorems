# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-0252`, the label `科罗纳问题` ("corona problem"), attribution
to Lennart Carleson, the year 1962, and the gloss `H^∞的极大理想空间` ("the maximal ideal space
of H-infinity"). Importance "high" and status `已验证` are catalog metadata, not source or kernel
evidence. Intake preserves only this maximal-ideal-space corona subject.

## Proposition-changing decisions

An approved source correction and duplicate-target review must select one truth-valued root and
freeze:

- whether `H^∞` is the Banach algebra of bounded analytic complex functions on the open unit disc
  or a sourced variant on another domain;
- how bounded analytic functions, their norm, multiplication, constants, completeness, and
  equality are represented;
- whether "maximal ideal space" means maximal proper ideals, nonzero continuous characters, the
  Gelfand spectrum, or another space, together with the exact correspondence between encodings;
- the topology on that space and the evaluation map from each point of the domain;
- whether the conclusion is density of evaluation characters, absence of a corona, equality of a
  closure, a point-separation property, or another statement;
- whether the selected root is instead the finite-generator Bezout theorem, including the index
  type, lower-bound convention, boundedness hypotheses, coefficient conclusion, and any
  quantitative constant;
- which direction of the classical equivalence between density and Bezout formulations is part of
  this target and which checked transports are required; and
- all universes, ordered binders, quantifier dependencies, hypotheses, exclusions, and conclusion
  clauses.

These choices produce distinct formal propositions. They form a resolution ledger, not a
canonical statement.

## Candidate formulations not credited

- Evaluation characters from the open unit disc are dense in the character or maximal-ideal space
  of the classical bounded-analytic Banach algebra `H^∞`.
- Every finite family of bounded analytic functions on the disc that is uniformly bounded away
  from a common zero admits bounded analytic Bezout coefficients.
- An explicit quantitative corona theorem bounding the coefficient norms from the number of
  generators, an upper normalization, and a lower corona constant.
- A correspondence or homeomorphism between maximal proper ideals and continuous characters of a
  commutative complex Banach algebra.

No formulation in this list is selected, asserted, or credited at intake.

## Degenerate and boundary cases

Source review must explicitly resolve the empty and singleton generator families; zero or
nonpositive lower bounds; constant, zero, and invertible generators; the open disc versus its
boundary or closure; whether functions are ambient maps or maps on a subtype; pointwise versus
essential boundedness; maximal ideals versus characters; continuity and nonzero/unital
requirements for characters; the weak-star or other topology; evaluation-map injectivity and
continuity; and density expressed by closure equality, neighborhood intersection, or nets.

## Neighboring and duplicate boundaries

`THM-M-0373` separately catalogs `Corona定理`, with the same author and year and the gloss
`H^∞的Corona问题`. Its existing dossier selected the finite-generator Bezout formulation and treats
maximal-ideal-space density as an alternate without a checked witness. That target is a
reconciliation input only. This intake cannot copy its canonical claim, statement-phase evidence,
obligations, receipts, or later work.

`THM-M-0250` separately catalogs Hardy-space theory, `THM-M-0251` inner-outer factorization, and
`THM-M-0253` interpolation sequences. They may eventually supply definitions or proof
dependencies, but their roots and evidence remain independently owned.

## Explicit exclusions

The several-variable corona problem, corona problems on other domains or Banach algebras, operator
corona theorems, polynomial or finite-Blaschke special cases, and a generic maximal-ideal theorem
are not substitutes. A structure that assumes the desired density or Bezout witness, a custom
axiom, an unchecked equivalence, and the catalog word `已验证` provide no proof credit.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib exposes the complex unit disc,
`AnalyticOnNhd`, generic character spaces of topological algebras, maximal ideals, and a map from
maximal ideals to characters for commutative complex Banach algebras. It does not thereby define
the intended `H^∞` Banach algebra, its evaluation map, or the target density/Bezout theorem. The
probe authenticates only these adjacent APIs. Its bounded search is intake discovery, not a
complete formal-anchor audit or a global absence claim.
