# THM-M-1307 rev-5.6 intake

This is the rev-5.6 `planned` instance for the theorem family commonly called Klainerman's
null-condition global-existence theorem. It starts at `L0 / rework_required`; the legacy label
`已验证` supplies no source or proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human root | Small-data global classical existence for nonlinear wave systems satisfying Klainerman's null condition in 3+1 dimensions | Exact equation class, regularity, data norm, support/decay assumptions, and solution space require primary-source transcription |
| Equation model | Minkowski wave operator, nonlinearities in first derivatives, and a quadratic null-form constraint | Quasilinear and semilinear variants may not be silently interchanged |
| Data | Sufficiently small smooth initial data with the source's localization/decay assumptions | “Small” needs a named norm and threshold; zero data is only a boundary case |
| Conclusion | Global-in-time classical solution with source-stated regularity and uniqueness | Scattering and asymptotic completeness are excluded unless source-stated |
| Proof architecture | Vector-field commutators, null-form estimates, weighted energy/decay, bootstrap continuation | Architecture only; no obligation closure is credited |
| Lean model | `Lean 4 + mathlib`; a future explicit PDE model and proposition | No canonical Lean declaration is identified or elaborated |
| Foundations | Lean kernel with a later pinned classical/choice/quotient policy | Toolchain, imports, dependencies, axioms, and TCB remain open |

“Klainerman theorem” is not a unique formal statement. This intake neither broadens the theorem to
every null-condition result nor substitutes a finite-dimensional analogue. The crosswalk identifies
the primary paper matching `零条件与整体存在性`, while leaving source-exact parameters open for the
dependent statement phase.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate is
exact statement identity: no source-exact Lean proposition, expression hash, checked transport, or
mutation result exists. The theorem is not complete.

## Validation

Commands and results are in `validation.md`. They establish membership, standard consistency, JSON
syntax, and dossier hygiene only. No Lean proof or kernel result is claimed.
