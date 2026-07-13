# THM-M-1446 exact-statement gate: blocked

Item: `S56-M-1446-STATEMENT`

Base revision: `be1f1d3c684eb883c819bcc968e0631d7f151bb0` (tree
`cff05d9f99014e6c54839589d4470f02df94a986`).

## Decision

The statement item remains `[ ]`. Its intake prerequisite has provisional worker state `[_]`, not
master-accepted state `[x]`; rev-5.6 section 10.2 permits this dependency-ordered attempt, but that
provisional intake cannot authorize an accepted transition. Independently, the exact-statement
gate fails because the repository has not selected a binder-complete mathematical proposition.

The catalog gives only the topic "LU decomposition" and the gloss "triangular decomposition of a
matrix." It does not choose the matrix shape or ordered index, scalar domain, pivot or permutation
convention, principal-minor hypothesis, diagonal factor, normalization, uniqueness, equation
orientation, reverse clause, or boundary cases. The natural unrestricted unpivoted reading is
false: `IntakeProbe.lean` kernel-checks that the rational swap matrix `[[0, 1], [1, 0]]` cannot be
`L * U` for lower-triangular `L` and upper-triangular `U`.

The inspected primary-source lead does not license a silent repair. Turing, *Rounding-off Errors in
Matrix Processes*, Section 3, journal pages 289-290, proves a qualified unique `A = L D U`
factorization under nonsingular-principal-minor hypotheses and also records a reverse `U D L`
form. Folding `D` into one triangular factor retains the material hypothesis. A pivoted `P A = L U`,
`A = P L U`, or two-sided permutation theorem is another proposition. The exact scalar domain,
principal-minor convention, source-to-catalog identity, LDU-to-LU transport, reverse-clause scope,
corrections, lawful source preservation, duplicate relationship with `THM-M-0047`, and independent
review remain open. Choosing any variant from mathematical familiarity would invent or substitute
the received target.

Sections 5 and 5.1 of rev-5.6 make statement ambiguity and a missing elaborated-expression
fingerprint hard blockers. There is therefore no honest canonical Lean expression whose imports
can be certified minimal, no approved alternate encoding for a checked transport, and no target
against which removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations
can run. Those mutation results are undefined, not passed. The root vector remains
`[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with its three direct imports:

- `Mathlib.LinearAlgebra.Matrix.Block`
- `Mathlib.LinearAlgebra.Matrix.Notation`
- `Mathlib.LinearAlgebra.Matrix.Transvection`

It checks the rational swap-matrix obstruction and six adjacent pinned matrix interfaces. Lean
reports only `propext`, `Classical.choice`, and `Quot.sound` for the obstruction. The probe declares
no corrected target, checked source transport, or corrected-root proof body, so its imports cannot
be claimed as minimal imports for the absent canonical theorem.

A bounded exact-topic search of repository-local Lean and pinned mathlib located only two
specialized block LDU identities in `Mathlib.LinearAlgebra.Matrix.SchurComplement`, each under an
invertible-corner hypothesis. They are not the catalog theorem and receive no statement or proof
credit. This bounded observation is feasibility evidence, not the downstream exhaustive anchor
audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation Record

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`). The structured
`commands_and_results` array in `statement-blocker.json` preserves exact commands and results.

| Command | Exit | Exact result |
|---|---:|---|
| rev-5.6 standard and target preflight | 0 | all 15 assurance groups and 1546 uniform-L0 targets passed; target rank 1123 remains planned and theorem-incomplete |
| base revision, tree, and status inspection | 0 | base identity above confirmed; only the automation-provided `.lake` symlink was initially untracked |
| `lake env lean ../../Stage1_Instances/THM-M-1446/IntakeProbe.lean` | 0 | swap-matrix obstruction and six adjacent interfaces elaborated; stdout SHA-256 `00a1a9138aa5e19f4550b11351becaa187b0b50b346983faf9dcbb08262d1817` |
| Lean/Lake, dependency lock, and pinned mathlib checks | 0 | toolchain, lock hashes, clean mathlib revision, and tree matched the structured blocker record |
| bounded exact-topic Lean search | 0 | only the two specialized Schur-complement block LDU identities matched |
| `python3 -B Stage1_Instances/THM-M-1446/check_intake.py` | 1 | the historical intake checker is fixed to its earlier base revision and correctly failed after integration advanced `HEAD`; it was not weakened or represented as statement evidence |
| blocker JSON and scoped semantic invariants | 0 | identity, null target/imports/fingerprints, unchanged vector, four undefined mutations, and false completion flags agree |
| prohibited-declaration and whitespace checks | 0 | no prohibited Lean declaration or whitespace diagnostic was found |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the statement deliverable did not pass |

The intake checker is historical phase-local evidence: it binds the intake's earlier repository
base and exact nine-file inventory. Integration has since advanced the clone, and this statement
attempt adds two owned blocker files. Its failed replay is recorded rather than hidden, and neither
the intake checker nor an authority file was edited to manufacture agreement.

## Retry Condition And Status Boundary

Accountable reviewers must lawfully preserve and hash an immutable primary or authoritative source,
select and independently approve one binder-complete proposition, and transcribe every incorporated
definition, ordered binder, hypothesis, conclusion, proof boundary, correction, and boundary case.
They must decide LU, LDU, PLU, or LUP; shape and index; scalar domain; leading-minor or pivot
hypotheses; permutation and equation orientation; normalization and uniqueness; reverse-clause
scope; and zero, singular, rectangular, and low-dimensional cases. A later statement run can then
encode exactly that claim, minimize pinned imports, serialize its elaborated expression and
environment, compile every credited transport, and run all four required mutation classes. Master
acceptance of the intake also remains required before an accepted statement transition.

This blocker is the truthful result of the assigned attempt, not completion of the statement node
or any downstream node. Lifecycle remains `planned`; `audit_complete` and `theorem_complete` remain
false; no debt-vector change is proposed. No `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, master acceptance, expression fingerprint, proof credit, or theorem completion is
claimed.
