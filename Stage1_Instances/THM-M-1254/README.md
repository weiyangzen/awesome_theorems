# THM-M-1254 rev-5.6 intake

This directory is the `planned` intake for the repository record named "fundamental solution".
The discovery text says only "fundamental solution of a differential operator". That phrase fixes a
definition-shaped relation, not an existence theorem: for an operator `L`, a fundamental solution is
a generalized function `E` satisfying `L E = delta_0`. It does not identify the operator class,
domain, scalar field, generalized-function space, or whether the intended claim is a definition,
existence, uniqueness, or an explicit formula.

The neighboring `THM-M-1255` is specifically the Malgrange-Ehrenpreis existence theorem for
nonzero constant-coefficient operators. It is excluded here; silently adopting that statement would
duplicate and substitute another target.

## Intake Status

- Lifecycle: `planned`
- Provisional root vector: `[H4, M4, R3]`
- First failed theorem gate: exact human statement identification
- Machine evidence: none; no Lean expression or declaration is credited
- Theorem completion: false

The scope inventory is in `scope-map.md`, and every source-to-statement gap is recorded in
`source-statement-crosswalk.md`. The exact command results in `validation.md` establish only target
membership, valid dossier structure, and the fail-closed status boundary.

## Open Task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
The statement phase must obtain a source-owner decision or primary-source pinpoint that determines
the claim and all mathematical parameters. Only then may it encode and elaborate a Lean target.

