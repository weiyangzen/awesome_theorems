# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-0255`, the label "quasiconformal mapping theory," attribution
to Lars Ahlfors, the year 1935, and the gloss "existence and uniqueness of quasiconformal maps."
Importance "high" and status `已验证` are catalog metadata, not source or kernel evidence. Intake
preserves only the quasiconformal existence-and-uniqueness family.

## Proposition-changing decisions

An approved source correction must select one truth-valued root and freeze:

- whether the objects are maps of planar domains, the extended complex plane, Riemann surfaces,
  normed real spaces, or another sourced category;
- orientation, homeomorphism, absolute-continuity, Sobolev, ACL, differentiability, and almost-
  everywhere conventions;
- whether quasiconformality is analytic, metric, geometric, modulus-based, or expressed through a
  Beltrami coefficient, plus a checked equivalence if more than one definition is credited;
- the coefficient or distortion data, its measurability and essential-norm bound, and all null-set
  and representative conventions;
- the exact equation or mapping problem, local or global domain, boundary behavior, and whether
  existence is asserted for a map, a normalized solution, or an equivalence class;
- the normalization that makes uniqueness meaningful, such as fixed points or boundary values, or
  the exact conformal postcomposition freedom when no normalization is imposed;
- any parameter dependence, regularity, inverse, composition, orientation, or surface-uniformization
  clause; and
- all universes, ordered binders, quantifier dependencies, hypotheses, and conclusion clauses.

These choices produce inequivalent propositions. They form a resolution ledger, not a canonical
statement.

## Candidate families not credited

- A measurable Riemann mapping theorem solving a Beltrami equation for a measurable coefficient
  with essential norm strictly below one, with a source-selected normalization.
- Existence and uniqueness of an extremal quasiconformal representative in a homotopy or isotopy
  class between marked Riemann surfaces.
- Existence of a quasiconformal extension or map subject to boundary data.
- An equivalence theorem among analytic, metric, geometric, and modulus definitions.
- A compactness, normal-family, deformation, or parameter-dependence theorem.

No family in this list is selected, asserted, or credited at intake.

## Degenerate and boundary cases

Source review must explicitly resolve a coefficient with norm equal to one; coefficients identified
only almost everywhere; empty, disconnected, non-simply-connected, or whole-plane domains; maps at
infinity on the sphere; orientation reversal; constant or noninjective maps; exceptional points or
sets; zero distortion and the conformal special case; identity and conformal automorphisms;
normalizations that fail to remove automorphisms; boundary regularity; and uniqueness as literal
function equality versus equality almost everywhere or modulo conformal postcomposition.

## Neighboring target boundaries

`THM-M-0256` separately names Teichmuller theory and Riemann-surface moduli. `THM-M-0257`
separately names the Ahlfors-Bers theorem and a complex-structure conclusion. `THM-M-0258`
separately names a Teichmuller-space boundary result. This target may eventually depend on checked
results from those dossiers, but it cannot absorb their roots or inherit their source or proof
credit.

## Explicit exclusions

A generic homeomorphism, conformal map, differentiable map, or existence-and-uniqueness interface
is not a quasiconformal theorem without a checked source-faithful bridge. A structure that stores
the desired map or uniqueness property as a field and then projects it is not a proof. The
Laplace-Beltrami operator is an unrelated namesake. Numerical deformation, a sampled distortion
bound, a plotted grid, and the catalog word `已验证` supply no theorem evidence.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides generic homeomorphisms and
conformal-calculus predicates, but a bounded exact-topic search found no quasiconformal, Beltrami-
coefficient, measurable-Riemann-mapping, or Ahlfors-Bers target declaration. This is intake
discovery only, not an exhaustive anchor audit or a global absence claim.
