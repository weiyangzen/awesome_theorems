# THM-M-0173 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Atiyah-Singer index theorem. The manifest's
historical `已验证` label is untrusted metadata and supplies no proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Equality of the analytic and topological indices for an elliptic differential operator between complex vector bundles on a compact smooth manifold | Closed-manifold convention and operator realization must be pinned before elaboration |
| Analytic side | section spaces, ellipticity, Fredholm realization, kernel/cokernel, integer-valued analytic index | No functional-analytic construction is credited |
| Symbol side | principal symbol, invertibility off the zero section, compactly supported K-theory symbol class | The Lean K-theory object model is unresolved |
| Topological side | Thom/Gysin construction and pushforward to a point | No topological-index construction is credited |
| Comparison | proof that both integer indices agree | Full theorem remains open on the machine side |
| Variants | cohomological formula and Dirac specializations | Candidates only; a specialization cannot replace the root |
| Foundations | Lean 4 kernel, pinned mathlib, and an accepted classical/choice/quotient policy | Fingerprints and transitive TCB remain open |

The proof architecture is not frozen by this phase. Its minimum later scope must preserve the
analytic-index construction, symbol/K-theory construction, topological pushforward, and the actual
comparison bridge rather than replacing the theorem with a characteristic-class identity or a
single special operator.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. `M4` is used because no exact
Lean declaration or fully selected object model exists yet. The first failed theorem gate is the
exact statement gate. The theorem is not complete.

## Validation

The commands and exact outcomes are recorded in `validation.md`. They validate target membership,
repository-standard consistency, JSON syntax, and dossier structure only; no Lean kernel result is
claimed.
