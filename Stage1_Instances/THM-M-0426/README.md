# THM-M-0426 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the functional equation of
Hecke-character L-functions. It does not inherit proof credit or accepted state from the legacy
`S1-M-080` Lean file or from the source label `已验证`.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human root | A functional equation for the completed L-function attached to a Hecke character | The generated source record does not specify the character class, completion, conductor, infinity type, dual, or normalization |
| Arithmetic objects | number field, idele-class/Hecke character, conductor and archimedean type | Concrete definitions and ordered binders remain statement-phase work |
| Analytic objects | Euler product/Dirichlet series, continuation, gamma factors, completed L-function | No construction or analytic theorem is credited |
| Equation | reflection about the normalization center, root number, and dual character | `Lambda(s, chi) = epsilon(chi) Lambda(1-s, dual chi)` is only a conventional scope guide until a primary-source formulation is selected |
| Branches | primitive versus imprimitive; finite-order/unitary versus general quasicharacter; ramified local factors | These variants must not be silently identified or broadened |
| Lean surface | future exact target over concrete pinned APIs | Legacy `StatementShape` is an abstract proposition and is discovery input only |
| Foundations | Lean 4 kernel and pinned mathlib, with classical/choice/quotient policy audited | Exact toolchain, dependency closure, TCB, and computation profile remain open |

The source title is too terse to determine one exact theorem without inventing mathematics. The
intake therefore freezes the ambiguity rather than selecting a convenient variant. The statement
phase must choose and cite a primary formulation, map every normalization parameter, and only then
elaborate the canonical target. Likely proof architecture includes local zeta integrals, local
functional equations, restricted-product/global factorization, Poisson summation, analytic
continuation, and identification with the completed Hecke L-function; this is scope, not a frozen
obligation registry.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed theorem gate is
exact source identification, followed by the Lean statement gate. The theorem is not complete.

## Validation

On base revision `1a30b84c1f86a2bbbf08b36f9afd06912b8f6c06`, the commands in `validation.md`
establish manifest membership, standard consistency, JSON syntax, and dossier-local hygiene only.

