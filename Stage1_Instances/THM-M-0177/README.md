# THM-M-0177 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Grothendieck-Riemann-Roch theorem. It
does not inherit proof credit from the metadata label `已验证` or from the legacy Stage1 queue.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | GRR for a proper morphism `f : X -> Y` of smooth quasi-projective schemes: compatibility of proper pushforward with Chern character after the Todd-class correction | The precise scheme hypotheses, coefficient ring, grading/completion conventions, and Lean encoding belong to the statement phase |
| Algebraic objects | Grothendieck groups of coherent sheaves/vector bundles, Chow groups with rational coefficients, Chern character, Todd class | Candidate object model only; no mathlib availability or equivalence is credited |
| Functorial maps | alternating derived direct-image pushforward `f_!` on K-theory and proper pushforward `f_*` on Chow groups | Construction and functoriality remain open obligations |
| Formula | `ch(f_! E) * td(T_Y) = f_*(ch(E) * td(T_X))` | Human-readable target only; no elaborated Lean expression exists |
| Generality boundary | the classical smooth quasi-projective formulation, not the more general singular-scheme Riemann-Roch transformation | No generalization or differential-geometric substitute may discharge the root |
| Foundations | Lean 4 kernel plus pinned mathlib and an accepted classical/choice/quotient policy | Exact toolchain, imports, dependency closure, and TCB remain open |

The blueprint's differential-geometry profile and curvature/local-coordinate seed are metadata-level
discovery hints, not the canonical mathematics of GRR. This intake preserves the algebraic-geometric
root rather than substituting a Hirzebruch or analytic Riemann-Roch special case.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate is
the exact statement gate: no adequate Lean scheme/K-theory/Chow target, elaborated expression hash,
environment fingerprint, or mutation record has been frozen. The theorem is not complete.

Validation commands and their limited meaning are recorded in `validation.md`.
