# THM-M-0450 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Mordell-Weil theorem. Historical Stage1
files are discovery inputs only and confer no proof credit or accepted state.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | For every number field `K` and elliptic curve `E/K`, `E(K)` is a finitely generated abelian group | Exact elaboration and expression fingerprint belong to the statement phase |
| Curve model | A nonsingular Weierstrass curve, with its point at infinity and chord-tangent group law | The existing Jacobian-point model is only a candidate encoding |
| Field scope | Number fields, including `K = Rat` as Mordell's original case | Function fields and arbitrary fields are excluded |
| Conclusion | Finite generation of the full rational-point group, equivalently finite rank plus finite torsion | No effective generators, rank bound, or torsion classification is claimed |
| Proof architecture | Weak Mordell-Weil finite quotient, height construction, descent, and terminal assembly | Architecture only; no branch closure is credited |
| Foundations | Lean 4 kernel plus a versioned mathlib foundation/choice policy | Toolchain, dependency, and TCB fingerprints remain open |

The canonical claim, ordered binders, hypotheses, and provisional Lean target are recorded in
`intake.json`. Source genealogy and the exact source-to-statement boundary are recorded in
`source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact Lean statement gate: there is no rev-5.6 normalized expression hash, environment
fingerprint, checked transport, or mutation record. This intake does not assert theorem completion.

## Validation

The commands and results in `validation.md` establish manifest membership, standard consistency,
JSON syntax, dossier-local reference integrity, and compilation of the historical discovery file.
They do not establish the Mordell-Weil theorem.
