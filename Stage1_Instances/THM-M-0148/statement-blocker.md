# THM-M-0148 Exact-Statement Gate: Blocked

Item: `S56-M-0148-STATEMENT`

Base revision: `af9c55e3e17639cd0c13bfd85bfb4bf30554785a` (tree
`4e842676a2087338f5582d16e365c51c87763af0`). Attempted on 2026-07-15
(`Asia/Shanghai`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0148-INTAKE` is only
provisional worker state `[_]`, not master-accepted state `[x]`, and the owned
intake dossier contains no accepted receipt. More importantly, the
exact-source-statement gate itself fails.

The complete repository source record supplies the title "Mori minimal model
program", Mori attribution, the year 1988, and only the slogan "birational
classification of higher-dimensional algebraic varieties". It does not select
one truth-valued theorem. It fixes neither ground field nor characteristic;
absolute versus relative setting; dimension; variety versus log pair; boundary
data and singularity class; normality, projectivity, properness, or
Q-factoriality; the permitted MMP steps and termination scope; nor an exact
minimal-model or Mori-fibre-space conclusion.

The possible cone, contraction, flip-existence, dimension-scoped termination,
minimal-model-existence, and Mori-fibre-space-output branches are materially
different propositions. Selecting one here, combining several, or filling the
missing notions with arbitrary `Prop` parameters would invent, narrow, broaden,
or substitute proposition-changing mathematics. The source's `partially
complete` label is untrusted metadata and cannot select a branch.

Sections 5 and 5.1 of the rev-5.6 standard make statement ambiguity and a
missing elaborated-expression fingerprint hard blockers. Consequently there is
no honest canonical Lean expression whose imports can be certified minimal.
The expression and environment fingerprints, checked alternate transports,
and removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations are undefined, not passed. No `Statement.lean`, canonical
declaration, proof body, axiom, placeholder, statement receipt, or worker
self-test was added.

## Lean Boundary Checked

The legacy module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_028.lean` was re-elaborated
only as discovery input. Its `MMPStatementData` stores projectivity, normality,
terminal singularities, Q-factoriality, canonical-divisor existence, and both
output notions as unconstrained `Prop` fields. Its alternate `StatementShape`
likewise takes the MMP-specific assumptions and outputs as predicate
parameters. The module itself records that a named, dimension/characteristic/
singularity-scoped theorem branch must replace those fields and that no branch
is repo-locally closed. Successful elaboration therefore verifies only the
scheme/rational-map substrate and blocker metadata, not the target statement.

The environment was Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
canonical `.lake` symlink was used read-only. No `lake update`, `lake build`,
dependency clone/fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this worker clone unless another working directory is shown.
They validate the blocker and the discovery boundary, not an exact MMP target.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0148` | 0 | rank 28; planned; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit tree contained only the automation-provided untracked `.lake` symlink; base revision and tree are above |
| source, Stage0, intake, scope, and legacy-module inspection | 0 | source contains only the programme slogan; intake leaves the formal target null; legacy module explicitly parameterizes the missing mathematics |
| `lake env lean --version`; `lake --version` from `Formalizations/Lean` | 0 | pinned Lean and Lake versions recorded above |
| `git rev-parse HEAD 'HEAD^{tree}'`; `git status --short` from pinned mathlib | 0 | pinned revision/tree recorded above; package worktree clean |
| `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_028.lean` from `Formalizations/Lean` | 0 | discovery module elaborated; printed only substrate, abstract statement shapes, open branch ledgers, and no MMP proof claim |
| bounded `rg` search for MMP/Mori/minimal-model/extremal-ray names over pinned mathlib and repo-local Lean | 0 | no source-selected mathlib theorem was located; results were legacy discovery artifacts and unrelated names, not an anchor-audit claim |
| prohibited-construct scan over the owned target and legacy module | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0148/statement-blocker.json` | 0 | structured blocker parsed as valid JSON |
| Python blocker-invariant and recorded-input-fingerprint check | 0 | identity, open state, null target/imports, unchanged `H5/M4/R3`, four undefined mutations, absent self-test, and recorded hashes agreed |
| `git diff --no-index --check /dev/null` for each blocker artifact | 0 wrapper result | new-file checks returned only the expected difference status and no whitespace diagnostics |
| final rerun of the standard validator, target validator, and target display | 0 | all structural checks still passed; target remains rank 28, planned, L0/rework-required, and theorem incomplete |
| `test ! -e .stage1-worker-selftest.json` | 0 | worker self-test intentionally absent because the exact-statement deliverable failed |

## Retry Condition And Status Boundary

The integration lane must first accept dependency-legal intake evidence. An
accountable source/scope reviewer must then approve one named theorem branch and
pin an immutable primary source with edition, theorem/section/page, assumptions,
corrections, and exact conclusion. That decision must freeze the field and
characteristic, absolute or relative base, dimension, variety/pair and boundary
data, singularities, positivity/projectivity/properness conditions, all ordered
binders, the precise output, termination boundary, and degenerate cases.

A fresh statement worker can then encode exactly that reviewed claim, minimize
its pinned imports, serialize and hash the elaborated expression and
environment, compile every credited transport, and execute all four mutation
classes.

This is the assigned phase's truthful blocker, not completion of the statement
or any downstream node. Lifecycle remains `planned`; the vector remains
`H5 / M4 / R3`; `audit_complete: false`; `theorem_complete: false`; and no
debt-vector change, accepted receipt, worker `[_]`, or master acceptance is
claimed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json` is emitted.
