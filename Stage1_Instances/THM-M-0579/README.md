# THM-M-0579 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Poincare conjecture. It begins at the
uniform `L0 / rework_required` baseline and claims no inherited proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Every closed, connected, simply connected topological 3-manifold is homeomorphic to the 3-sphere | Lean elaboration and expression fingerprint belong to the dependent statement phase |
| Object model | Topological manifolds without boundary, dimension three, connectedness, compactness, and simple connectedness | Exact mathlib structures and typeclass binders remain to be selected and checked |
| Conclusion | Existence of a homeomorphism with the standard topological 3-sphere | Orientation and smooth/PL upgrades are not part of the root claim |
| Geometrization route | Ricci flow with surgery, finite-time extinction for the simply connected case, and topological reconstruction | Architecture only; no machine closure is credited |
| Foundations | Lean 4 kernel plus a versioned classical/choice/quotient policy | Exact profile and dependency fingerprint remain open |
| Exclusions | General geometrization, classification of non-simply-connected 3-manifolds, and differentiable equivalence | These may be dependencies but are not substituted roots |

The source wording, formalization boundary, and unresolved source audit are recorded in
`source_statement_crosswalk.md`. The structured intake fields are authoritative in `intake.json`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate is
the exact statement gate: no canonical Lean declaration, normalized expression hash, environment
fingerprint, checked transports, or mutation results exist yet. The theorem is not complete.

## Validation

The commands in `validation.md` establish target membership, repository-standard consistency, JSON
syntax, and dossier-local hygiene only. No Lean theorem or kernel result is claimed by this intake.
