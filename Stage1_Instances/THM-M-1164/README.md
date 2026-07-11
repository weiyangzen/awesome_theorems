# THM-M-1164 rev-5.6 intake

This directory is the planned dossier for symmetry of a Green function associated with a
self-adjoint operator. The source phrase alone does not specify an operator realization, boundary
conditions, invertibility, whether the kernel is a function or distribution, or whether equality is
pointwise or almost everywhere. This intake therefore freezes the standard resolvent/inverse form
and records every extra condition needed for the kernel corollary.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | A densely defined self-adjoint operator with `0` in its resolvent set | Lean representation and exact API are open |
| Operator conclusion | The bounded Green operator `G = A⁻¹` is self-adjoint | No kernel theorem is needed for this conclusion |
| Kernel conclusion | `K(x,y) = conj(K(y,x))` almost everywhere for a fixed, unique integral-kernel representation | Pointwise equality needs additional regularity |
| Real specialization | Conjugate symmetry reduces to ordinary symmetry | Real-valuedness must be explicit |
| PDE interpretation | A self-adjoint operator realization includes its domain/boundary conditions | No particular domain, PDE, or boundary condition is silently selected |
| Exclusions | zero modes, generalized inverses, non-self-adjoint operators, distribution-only kernels | These require separate theorem statements |
| Foundations | Lean 4 kernel and pinned mathlib | Toolchain, imports, axioms, and TCB remain open |

The structured claim is in `intake.json`. The repository wording, mathematical clarification, and
source work still required are separated in `source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed theorem gate is
the exact Lean statement gate: there is no selected module or declaration, normalized expression,
environment fingerprint, checked transport, or mutation evidence. The theorem is not complete.

## Validation

On base revision `8e78e1b4206fc224e91466efb397811c09205b0e`, the commands and results in
`validation.md` check target membership, repository-standard consistency, JSON syntax, dossier
references, and whitespace only. They provide intake evidence, not kernel proof evidence.
