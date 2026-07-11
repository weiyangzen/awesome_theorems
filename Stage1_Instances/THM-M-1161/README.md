# THM-M-1161 rev-5.6 intake

This is the `planned` rev-5.6 dossier for the classical Fredholm integral equation of the second
kind. The repository source row says only "integral equations of potential theory"; it is not an
exact theorem statement and its historical `已验证` label supplies no proof credit.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Equation | `φ(x) - λ ∫ K(x,y) φ(y) dy = f(x)` on a compact domain | Function spaces, measure, and kernel regularity must be fixed by the statement phase |
| Root claim | Fredholm alternative: unique solvability for every datum, or a nonzero homogeneous solution with the corresponding adjoint compatibility condition | The two alternatives and adjoint pairing must not be weakened to an abstract nearby fact |
| Operator bridge | The kernel induces a compact operator `T`; the equation becomes `(I - λT)φ = f` | Compactness and equality with the integral expression require checked Lean witnesses |
| Boundary cases | `λ = 0`, zero kernel, zero datum, nontrivial homogeneous kernel, real versus complex scalars | None is silently excluded at intake |
| Candidate machine anchor | mathlib compact-operator Fredholm alternative | Adjacent substrate only, not an integral-equation proof or accepted anchor audit |
| Foundations | Lean 4 kernel, pinned mathlib, classical functional analysis | Exact versions, imports, axioms, and TCB remain open |

The exact historical formulation varies with equation convention and regularity assumptions.
`intake.json` therefore freezes the intended mathematical family while marking the formal target
open rather than inventing binders. The dependent statement phase must choose a source-faithful
specialization and demonstrate the integral-operator bridge.

## Intake verdict

Lifecycle is `planned`, with provisional root vector `[H2, M4, R3]`. The first failed theorem gate
is exact-statement elaboration. No theorem, proof body, source acceptance, or completion is claimed.
The open task DAG is the six dependent nodes recorded in the authoritative blueprint: statement,
anchor audit, obligation tree, proof, validation, and release, in that order.

Validation commands and their results are recorded in `validation.md`.
