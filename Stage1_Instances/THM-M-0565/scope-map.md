# Scope map

## Literal subject boundary

- Real vector bundles (or an equivalent classifying-space formulation).
- Cohomology with coefficients in `F_2`.
- Graded characteristic classes conventionally denoted `w_i`, including a total class `w` when
  the selected theorem uses it.
- Naturality, direct-sum behavior, normalization, existence, uniqueness, and obstruction results
  are candidate theorem components only; none is selected by the inventory phrase itself.

The repository wording is a topic label, not yet a frozen mathematical claim. In particular, a
class definition, a construction theorem, the axiomatic characterization of the whole family, and
an application to tangent bundles have different quantifiers and conclusions.

## Decisions required before statement freeze

The statement phase must select and inspect one exact primary theorem. It must then fix the bundle
category and base-space hypotheses; finite rank versus stable bundles; reduced versus unreduced
cohomology; the `F_2` model; degree and rank conventions; whether `w_0 = 1` and `w_i = 0` above the
rank are conclusions or definitions; the normalization object; pullback naturality; the precise
Whitney-sum formula; and all empty, rank-zero, disconnected-base, and non-paracompact boundary
cases. The ordered binders, universes, foundation profile, and minimal Lean imports follow only
after these choices.

## Explicit exclusions

- Chern or Pontryagin classes, Wu classes, Euler classes, or a generic characteristic-class API.
- Stiefel-Whitney numbers and their cobordism classification as substitutes for the class family.
- The tangent-bundle orientability criterion `w_1 = 0`, the spin criterion involving `w_2`, or a
  non-immersion obstruction unless a selected source makes that exact result canonical.
- A record that assumes classes, naturality, or the sum formula as fields and then projects them.
- The inventory label `已验证` as mathematical-source or kernel evidence.

No canonical Lean declaration is selected at intake. Failure to identify one exact source theorem
must keep the statement phase blocked rather than produce a convenient theorem about mod-2
cohomology.
