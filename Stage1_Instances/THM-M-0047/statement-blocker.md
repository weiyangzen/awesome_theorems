# THM-M-0047 exact-statement gate: blocked

Item: `S56-M-0047-STATEMENT`

Base revision: `72f928bdf1a47d7c119826db45575bd02a3a63ce` (tree
`171a6bfae88220f5df9b39cdd6c7e1bf17639889`).

## Decision

The statement item remains `[ ]`. Its prerequisite intake has provisional worker state `[_]`, not
master-accepted state `[x]`, and its receipt deliberately leaves the corrected proposition and Lean
target null. More importantly, there is no source-approved exact proposition to elaborate.

The catalog says only that a matrix is a product of a lower-triangular and an upper-triangular
matrix. It does not select the matrix shape or index type, scalar domain, pivot or permutation
convention, hypotheses, normalization, uniqueness, equation orientation, or boundary cases. Its
natural unrestricted unpivoted reading is false: `IntakeProbe.lean` proves that the rational swap
matrix `[[0, 1], [1, 0]]` cannot equal `L * U` with lower-triangular `L` and upper-triangular `U`.

The inspected primary lead does not authorize a silent repair. Turing, *Rounding-off Errors in
Matrix Processes*, Section 3, pages 289-290, proves a unique normalized `A = L D U` factorization
under nonsingular-principal-minor hypotheses. Folding `D` into the upper factor still retains that
material hypothesis. A pivoted `P A = L U`, `A = P L U`, or LUP theorem is another proposition.
The exact meaning of principal minors, domain, transport, corrections, preservation, and independent
review remain open. Selecting any of these variants from mathematical familiarity would broaden or
substitute the target.

Rev-5.6 makes source ambiguity and a missing elaborated-expression fingerprint hard blockers. There
is therefore no honest canonical expression whose imports can be certified minimal, no approved
alternate encoding for a checked transport, and no canonical target against which removed-
hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can run. These mutation
results are undefined, not passed. The vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with these direct imports:

- `Mathlib.LinearAlgebra.Matrix.Block`
- `Mathlib.LinearAlgebra.Matrix.Notation`
- `Mathlib.LinearAlgebra.Matrix.Transvection`

It kernel-checks the rational swap-matrix obstruction and authenticates six adjacent triangular,
determinant, explicit multiplication, and pivot/transvection interfaces. Its output reports only
the standard mathlib proof dependencies `propext`, `Classical.choice`, and `Quot.sound`. The probe
declares no corrected target, source transport, or corrected-root proof body, and its imports cannot
be certified minimal for an absent canonical target.

A bounded search found no exact general finite LU, PLU, LUP, or source-exact LDU declaration in
repo-local Lean or pinned mathlib. `Mathlib.LinearAlgebra.Matrix.SchurComplement` contains two
specialized `2 x 2` block LDU identities under an invertible-corner hypothesis. Those identities are
not the catalog theorem and receive no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`).
The `commands_and_results` array in `statement-blocker.json` preserves the literal shell commands;
the table below keeps long compound checks readable.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check && python3 scripts/stage1_target.py show THM-M-0047` | 0 | all 1546 targets passed; target rank 1087 is planned, rework-required, legacy artifacts unaccepted, and theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0047/IntakeProbe.lean` | 0 | swap-matrix obstruction and six adjacent interfaces elaborated; stdout SHA-256 `85212b1124123df2a24a58ed1631096335d68cdcc74c15bf792f47d31678807c` |
| Lean/Lake version, lock-hash, mathlib revision/tree/status commands | 0 | pinned environment above confirmed; mathlib package source was clean |
| bounded `rg` search for LU/LUP/PLU/LDU declarations | 0 | only two specialized Schur-complement block LDU results matched; no exact target declaration found |
| `python3 -B Stage1_Instances/THM-M-0047/check_intake.py` | 1 | stale intake-only checker expected intake `[ ]`, while integration now records provisional `[_]`; it was not edited or represented as statement evidence |
| JSON syntax and scoped blocker invariant checks | 0 | blocker identity, null target/imports/fingerprints, unchanged vector, four undefined mutations, and false completion flags agree |
| prohibited Lean declaration scan | 0 | inner `rg` returned expected no-match exit 1; no prohibited declaration found |
| scoped tracked and new-file whitespace checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the statement deliverable did not pass |

The intake checker is bound to the intake's original authority state and exact nine-file inventory.
The integration lane has since advanced the intake to `[_]`, and this statement attempt adds two
owned artifacts. Its failure is expected phase evolution, not statement validation, and the intake
checker was not weakened to manufacture agreement.

## Retry Condition And Status Boundary

Accountable reviewers must lawfully preserve and hash an immutable primary or authoritative source,
select and independently approve one binder-complete proposition, and transcribe every incorporated
definition, ordered binder, hypothesis, conclusion, proof boundary, correction, and boundary case.
They must decide LU, LDU, PLU, or LUP; shape and indices; scalar domain; leading-minor or pivot
hypotheses; permutation and equation orientation; normalization and uniqueness; and zero, singular,
rectangular, and low-dimensional cases. A later statement run can then encode precisely that claim,
minimize its pinned imports, serialize its elaborated expression and environment, compile every
credited transport, and execute all four required mutation classes. Master acceptance of the intake
also remains required before an accepted statement transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and `theorem_complete: false`;
no debt-vector change is proposed. No `.stage1-worker-selftest.json`, statement receipt, worker
`[_]`, master acceptance, expression fingerprint, or proof credit is claimed.
