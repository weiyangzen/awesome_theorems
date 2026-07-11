# THM-M-1202 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the Lax entropy condition. The Stage0 phrase
"entropy condition for shocks" is not precise enough to select a theorem without fixing the system,
shock family, side convention, eigenvalue ordering, and whether the claim is a definition, a
necessary admissibility condition, or part of a larger existence/uniqueness theorem. This intake
therefore freezes the narrow classical Lax-shock interpretation and records those choices as open
statement work rather than silently inventing a stronger theorem.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| PDE model | One-dimensional system `u_t + f(u)_x = 0` near two constant traces | Weak-solution spaces and global Cauchy theory are excluded |
| Jump | Left/right states, speed, and the Rankine-Hugoniot relation | No existence of a discontinuous weak solution is claimed |
| Hyperbolicity | Real, distinct, ordered characteristic speeds at both traces | A Lean representation of eigenvalue branches is not selected |
| Entropy condition | Compressivity of a designated `k`-shock | Oleinik, Kruzkov, entropy-pair, viscosity, and scalar formulations are separate targets |
| Equivalent views | Core kth-family inequalities, adjacent-family inequalities, incoming-characteristic count | Equivalences are candidates and receive no credit before checked transports |
| Boundary cases | Explicit first/last characteristic families | No fictitious `lambda_0` or `lambda_(n+1)` is introduced |
| Foundations | Lean 4 kernel with a versioned mathlib analysis/linear-algebra surface | Toolchain, imports, axioms, and TCB are open |

The canonical human wording, provisional binders, hypotheses, exclusions, and formal-target gap are
structured in `intake.json`. `source_statement_crosswalk.md` separates the repository metadata from
the primary-source candidate and makes the convention-sensitive work visible.

## Open task DAG

`S56-M-1202-INTAKE` freezes scope. The dependent nodes remain, in order:
`STATEMENT`, `ANCHOR_AUDIT`, `OBLIGATION_TREE`, `PROOF`, `VALIDATION`, and `RELEASE`. The next node
must transcribe a page-level primary statement, choose ordered finite-index/eigenvalue APIs, handle
`k = 1` and `k = n`, and elaborate one exact Lean expression before inspecting proof closure.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. `H2` records that a plausible
primary source has been identified but no page-level premise/errata review is accepted. `M4`
records that no Lean target or candidate declaration has yet been selected. The first failed theorem
gate is the exact statement gate. This theorem is not complete.

## Validation

The commands and results in `validation.md` establish manifest membership, repository-standard
consistency, JSON syntax, local artifact integrity, and absence of prohibited proof constructs only.
No Lean source is introduced, so no kernel result is claimed.
