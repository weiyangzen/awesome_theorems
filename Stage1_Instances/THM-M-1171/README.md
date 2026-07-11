# THM-M-1171 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the Calderon-Zygmund estimate. The Stage0
label `已验证` is untrusted discovery metadata and supplies no proof or acceptance credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Whole-space scalar second-derivative estimate on `R^n`: for `1 < p < infinity`, smooth compactly supported `u` satisfies `norm (D^2 u)_(L^p) <= C norm (Delta u)_(L^p)` | The source metadata says only "second derivative L-p estimate"; the exact norm, dimension, scalar field, and quantifier order must be fixed at statement review |
| Analytic setting | Euclidean `R^n`, `n >= 1`, Lebesgue measure, real-valued test functions | Domains, boundary-value variants, weighted estimates, vector-valued systems, and endpoint `p = 1, infinity` are excluded |
| Operator layer | Distributional/Fréchet second derivatives and the Laplacian, initially on `C_c^infinity` | A concrete mathlib encoding and checked equivalences are deferred |
| Extension layer | Possible extension from test functions to `W^{2,p}` or homogeneous Sobolev spaces | Candidate consequence only; not part of the intake root |
| Proof architecture | Fundamental solution, second derivatives as singular integrals, Calderon-Zygmund operator boundedness, componentwise assembly | Architecture only; no obligation or proof closure is credited |
| Foundations | Lean 4 kernel, pinned mathlib, classical analysis policy | Exact toolchain, imports, axioms, TCB, and computation profile remain open |

The canonical human claim and its unresolved choices are structured in `intake.json`. Primary-source
genealogy and the source-to-statement gaps are recorded in `source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed downstream gate
is exact-statement identity: the source record does not uniquely determine one formal proposition,
and no Lean expression or checked transport exists. The intake scope is nevertheless concrete and
fail-closed. The theorem is not complete.

## Validation

The exact intake-only checks and results are recorded in `validation.md`. They establish target
membership, standard consistency, JSON syntax, and dossier-local integrity only. Master acceptance
and all dependent phases remain outstanding.
