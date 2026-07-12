# Scope map

## Included theorem family

- A smooth, closed, oriented four-manifold `X`, together with the source-required connectedness,
  homology-orientation, and positivity assumptions.
- A spin-c or equivalent characteristic structure and its associated spinor bundles and
  determinant line bundle.
- The Seiberg-Witten monopole equations for a connection and positive spinor, modulo gauge.
- A compact, oriented moduli space after the generic metric/perturbation and reducible-solution
  conditions required by the selected result.
- A signed count or cohomological pairing defining an integer-valued invariant, and the precise
  independence/diffeomorphism-invariance conclusion proved by the selected primary theorem.

## Decisions required at statement freeze

The statement phase must select and inspect one exact theorem. It must freeze: smoothness,
compactness, boundary, connectedness, and orientation assumptions on `X`; the spin-c encoding; the
configuration and gauge groups and Sobolev completions; metric and perturbation regularity; the
equations and sign conventions; expected dimension; compactness, transversality, and orientation
premises; the definition for positive or zero-dimensional moduli spaces; the codomain and finite
support of the invariant; the `b2+ > 1` metric-independence range versus the `b2+ = 1` chamber
dependence; homology orientation; reducibles; and the exact quantifier order.

These choices change the proposition. In particular, "Seiberg-Witten theory" cannot be silently
normalized to one numerical invariant without a source decision.

## Explicit exclusions

- The Seiberg-Witten equations or moduli-space definitions alone, with no construction and
  invariance conclusion.
- Witten's physical low-energy duality conjectures, the Donaldson/Seiberg-Witten relation, Taubes's
  `SW = Gr`, or a special computation for one manifold as a substitute for the selected root.
- A vanishing, adjunction, simple-type, or exotic-smooth-structure consequence alone.
- An abstract structure containing compactness, transversality, or the desired invariant as a
  field; those are proof obligations, not admissible hypotheses introduced for convenience.
- The separately scheduled records `THM-M-0185` and `THM-M-0608` as aliases that confer proof
  credit, and the repository metadata value `已验证` as source or kernel evidence.

No canonical Lean expression is frozen at intake. A later target must expose the four-manifold,
spin-c, connection, spinor, gauge action, monopole equations, moduli space, orientation/counting,
and invariance interfaces concretely, or report a precise missing-API blocker.
