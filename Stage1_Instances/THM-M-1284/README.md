# THM-M-1284 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for Ye's theorem on the Yamabe flow. The upstream
metadata phrase "convergence of Yamabe flow" is not an exact theorem statement and receives no
proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human source | Rugang Ye, *Global existence and convergence of Yamabe flow*, JDG 39 (1994), 35-50 | Primary paper identified; theorem text, hypotheses, and errata still require page-level verification |
| Geometric domain | closed Riemannian manifolds and the normalized Yamabe flow considered by Ye | Dimension, regularity, sign, and geometric hypotheses are deliberately not guessed |
| Evolution | existence of the metric-valued flow | Exact PDE normalization and time interval remain open |
| Asymptotics | convergence to a constant-scalar-curvature metric under Ye's stated assumptions | Topology/rate and all exceptional cases remain open |
| Lean boundary | a future definition of the flow plus existence and convergence propositions | No repo-local Lean declaration has been selected or credited |
| Foundations | Lean 4 kernel with pinned mathlib and an audited analysis/geometry stack | Environment, TCB, classical choice, and computation profiles remain open |

The exact root cannot truthfully be frozen from the repository's one-line description. The dependent
statement phase must transcribe the primary theorem before choosing ordered binders or a Lean
expression. This intake therefore records `M4`, not an invented formalization.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed gate is exact
source-statement identification. No theorem, source fidelity, machine closure, or completion is
claimed. The open task DAG is the six dependent nodes already defined by the authoritative
rev-5.6 blueprint: statement, anchor audit, obligation tree, proof, validation, and release.

