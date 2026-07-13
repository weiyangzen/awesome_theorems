# THM-M-0239 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label `雅可比反演定理`
(Jacobi inversion theorem). The repository attributes the item to Carl Jacobi in 1834 and gives
only the gloss `阿贝尔积分的反演` ("inversion of Abelian integrals"). Its `已验证` label is
untrusted metadata under rev-5.6 and supplies no human-source or Lean proof credit.

The gloss identifies the classical Jacobi inversion family, but it does not select one exact
proposition. A fixed Encyclopedia of Mathematics revision describes simultaneous inversion of
first-kind Abelian integrals on a compact genus-`g` Riemann surface, modulo their period lattice,
including normal and exceptional theta-function cases. A modern paper's abstract describes the
widely used existence form: the degree-`g` Abel-Jacobi map from the symmetric product `X^(g)` to
the Jacobian `J(X)` is surjective. These are source leads, not an accepted equivalence or H0
crosswalk. The catalog does not say whether the root is surjectivity, a divisor-class existence
statement, the integral-congruence system, or an explicit theta-function inversion formula.

Pinned mathlib has useful neighboring interfaces: type-level symmetric powers, complex manifolds,
a one-dimensional two-variable Jacobi theta function, commutativity of suitable group schemes,
the Picard group of a ring, and Jacobian-coordinate points on a Weierstrass curve. None supplies a
general compact-curve Jacobian, Abel-Jacobi map, period quotient, genus-`g` Riemann theta function,
or Jacobi inversion theorem. `IntakeProbe.lean` authenticates only those adjacent interfaces.

The provisional vector is `[H1, M4, R4]`: credible modern statement and exposition leads exist,
but the exact source statement, definitions, assumptions, historical attribution, proof boundary,
errata, and independent review are open; no usable exact formal artifact is credited; and no
source-faithful proof reconstruction exists. `instance.json` is the structured scope authority and
`task-dag.json` keeps all six downstream phases open. No canonical mathematical or Lean
proposition, H0, M0, R0, accepted proof state, audit completion, theorem completion, or master
acceptance is claimed.
