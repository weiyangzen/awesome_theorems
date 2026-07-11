# THM-M-0419 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Kronecker-Weber theorem. Historical
Stage1 files are discovery inputs only and confer no accepted statement or proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human root | Every finite abelian extension of `Q` is contained in a cyclotomic extension of `Q` | Source wording is frozen; detailed source audit remains open |
| Lean root candidate | A number field `K` with `IsAbelianGalois Q K` admits a `Q`-algebra embedding into `CyclotomicField n Q` for some nonzero `n` | Existing `StatementShape` is unaccepted legacy discovery; elaboration belongs to the statement phase |
| Object model | finite extension, abelian Galois group, cyclotomic field, algebra embedding | Equivalence between abstract extension presentations and the chosen typeclass presentation is not credited |
| Degenerate cases | conductor/index `n = 0`; trivial extension `K = Q`; alternate indexing conventions | Candidate excludes `n = 0`; boundary probes remain to be checked |
| Mathematical architecture | ramification/conductor reduction, primary/cyclic decomposition, prime-power core, compositum containment | Architecture only; no proof node is closed |
| Foundations | Lean 4 kernel plus pinned mathlib and an accepted classical/choice/quotient policy | Exact toolchain, imports, TCB, and environment fingerprint remain open |

The exact human claim, domains, assumptions, and provisional formal target are structured in
`intake.json`. The relationship to located human and Lean sources is recorded in
`source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact-statement gate: no normalized expression hash, environment fingerprint, checked
transport, or mutation result has been accepted. The theorem is not complete.

## Validation

The commands in `validation.md` establish target membership, repository-standard consistency,
JSON syntax, and dossier-local integrity only. They do not establish kernel closure.
