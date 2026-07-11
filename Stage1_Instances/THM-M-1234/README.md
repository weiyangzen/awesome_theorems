# THM-M-1234 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Yudovich theorem target. It inherits no
proof credit from the Stage0 label or the generated legacy queue.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Global-in-time existence for the two-dimensional incompressible Euler equations in the Yudovich bounded-vorticity regime | Domain regularity, boundary condition, forcing, initial-data spaces, and solution notion must be fixed by the statement phase |
| Source boundary | V. I. Yudovich's 1963 non-stationary ideal-fluid result | The generated description says only "global existence"; uniqueness is not silently added to the root |
| PDE model | Velocity/pressure Euler system, incompressibility, initial data, and an impermeable boundary condition on a planar domain | No particular mathlib representation is credited yet |
| Vorticity layer | Scalar curl, bounded initial vorticity, transport, and velocity reconstruction | Candidate architecture only; no formal bridge is claimed |
| Analytic layer | Energy control, elliptic/Biot-Savart estimates, compactness or approximation, and time-global continuation | Proof obligations belong to later phases |
| Foundations | Lean 4 kernel plus a pinned mathlib environment and an accepted classical/choice/quotient policy | Exact toolchain, imports, axioms, and TCB remain open |

The scope deliberately preserves the manifest's global-existence claim while recording the data
needed to make it a theorem rather than a slogan. The canonical human claim and open formal fields
are structured in `intake.json`; source correspondence and ambiguity are recorded in
`source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate is
the exact-statement gate: no precise domain, boundary/data hypotheses, solution predicate,
elaborated Lean expression, or environment fingerprint has been accepted. The theorem is not
complete.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
Each edge is blocking. This intake supplies scope only and gives no closure credit to a downstream
node.

## Validation

The commands and exact intake-level results are recorded in `validation.md`. They establish target
membership, standard consistency, JSON syntax, and local artifact hygiene only; no Lean theorem or
kernel proof is introduced.
