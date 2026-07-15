# THM-M-0419 rev-5.6 dossier

This directory is the rev-5.6 `planned` instance for the Kronecker-Weber theorem. Historical
Stage1 files are discovery inputs only and confer no accepted statement or proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human root | Every finite abelian extension of `Q` is contained in a cyclotomic extension of `Q` | Source wording is frozen; detailed source audit remains open |
| Lean root | Every number field `K` with `IsAbelianGalois Q K` admits a `Q`-algebra embedding into `CyclotomicField n Q` for some nonzero `n` | `Statement.lean` elaborates this exact closed target; master acceptance is pending |
| Object model | finite extension, abelian Galois group, cyclotomic field, algebra embedding | Equivalence between abstract extension presentations and the chosen typeclass presentation is not credited |
| Degenerate cases | conductor/index `n = 0`; trivial extension `K = Q`; alternate indexing conventions | Target excludes `n = 0`; the zero mutation is killed; the trivial extension remains included |
| Mathematical architecture | ramification/conductor reduction, primary/cyclic decomposition, prime-power core, compositum containment | Architecture only; no proof node is closed |
| Foundations | Lean 4 kernel plus pinned mathlib and an accepted classical/choice/quotient policy | Statement environment is fingerprinted; full TCB-policy acceptance remains open |

The exact human claim, domains, assumptions, and provisional formal target are structured in
`intake.json`. The relationship to located human and Lean sources is recorded in
`source_statement_crosswalk.md`.

## Current verdict

Lifecycle remains `planned`; provisional root vector remains `[H1, M3, R3]`. The exact statement has
worker self-test evidence in `statement.json` and `statement-receipt.md`, but only the integration
lane may accept it. The bounded anchor audit is recorded in `anchor-audit.json` and
`anchor-audit-validation.md`, pending master acceptance. Pinned mathlib supplies supporting APIs but
no terminal converse. The external `atlas-lean` candidate is placeholder-bearing and receives zero
proof credit. Registry v1 now freezes 25 obligations and seven typed graph families in
`obligation-registry.json` and `typed-graphs.json`. `ObligationTree.lean` checks only the positive-
index transport and conditional cyclic/local/root composition interfaces; all substantive local and
global packages remain open. This obligation-tree node is worker-self-tested pending master
acceptance. The theorem is not complete.

## Validation

The commands in `validation.md` establish target membership, exact statement elaboration, mutation
failures, JSON syntax, and dossier-local integrity. They do not establish proof closure.
