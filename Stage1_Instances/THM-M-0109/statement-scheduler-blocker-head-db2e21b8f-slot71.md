# THM-M-0109 statement scheduler-ownership blocker

Item: `S56-M-0109-STATEMENT`

Theorem: `THM-M-0109`

Claim order: `(v2_execution_rank=268, phase_layer=1, phase_item_id=S56-M-0109-STATEMENT)`

Worker base revision: `db2e21b8fec263c5b65014acb1ee2039566e35a3`

Worker base tree: `815414c57391f2c12871c05a6e3d2944b0f2fef2`

Worker verdict: `blocked`

Authoritative state: `[_]` with `attempts=1` (unchanged)

Phase accepted: `false`

## First failed gate

`G05-AUTHORITY-REPLAY.validator_is_stale_for_the_current_authoritative_item_state`

The mandatory HEAD contract is
`Docs/Stage1_Phase_Acceptance_Contracts.json`, SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`.
For `statement` it declares these scheduler-owned candidates after theorem-ID
substitution:

- `Stage1_Instances/THM-M-0109/check_statement.py`
- `Stage1_Instances/THM-M-0109/check_statement_artifacts.py`

Exactly one is present at this worker base: `check_statement.py`, Git blob
`79d27b98c32c947496331587b77b84f8c0b0d303`, SHA-256
`5bafc4633ba9b6e8caf2223603b5894c193a621cf640cc847922ddfadef30111`.
The worker did not create, refresh, rename, replace, or delete either candidate.

The unique candidate is nevertheless not replayable at the current authority
snapshot. It hard-codes base revision
`778c2db4855d48868391ea236f702e592067e798`, tree
`27abf0ec82dad50561a14d1db471126fb7ac8665`, theorem-DAG SHA-256
`9db2a7cc29bf218211004677abe45ce1742f597405c2d879675dbc66542c4c8b`,
and an exact checklist row requiring statement state `[ ]` with `attempts=0`.
The sole task-state authority now records this item as `[_]` with `attempts=1`,
and the current theorem-DAG SHA-256 is
`91ea782c662e40b9608f8900ad586114c5ef8e8e5d2d2f13316185bd8f205067`.

Running the exact contract argv from the repository root,

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0109/check_statement.py
```

exits 1, writes no stdout, and writes exactly
`sole task-state authority no longer has the exact open statement row` to
stderr. It therefore does not produce the mandatory single JSON object with
schema `stage1-validator-semantic-result/1.0`. Exit status from any other check
cannot replace this scheduler-owned semantic replay. The assignment forbids
this worker from refreshing the validator, so no valid phase receipt or worker
self-test handoff can be produced at this base.

## DAG and reuse audit

The authoritative theorem DAG and supplied dependency context agree on v2 rank
268 and context SHA-256
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
The complete `parent_inspection_order`, direct-hard-parent closure,
transitive-hard-ancestor closure, hard-edge list, reuse-hint list, and shared
group list are all `[]`. The required ordered traversal was therefore completed
exactly once with zero provider visits. No declaration was imported, copied,
transported, reused, or credited, and no provider acceptance was inherited.

The existing target-owned `dependency-reuse-ledger.json` uses schema
`stage1-dependency-reuse-ledger/1.1` and truthfully records the empty closure,
but it binds the old worker revision and old full-graph digest. It is stale for
this claim. Refreshing it alone cannot repair the immutable-validator failure,
and doing so would make a new receipt/self-test impossible without a lawful
validator replay, so this blocker leaves it unchanged.

## Statement boundary

The mathematical blocker also remains unchanged. The repository identifies
the target by the conventional name Chow's lemma but supplies only the gloss
"properties of the coordinate ring of an algebraic variety." The gloss names
no ring property, base, domains, ordered binders, hypotheses, conclusion, or
boundary cases. Repository history leads to the bulk catalog import and
supplies no primary publication, theorem/page locator, exact quotation,
translation review, correction, or errata disposition that reconciles the two.

The standard scheme-theoretic Chow lemma and finite-generation,
polynomial-quotient, or Noetherian coordinate-ring claims are materially
different theorems. Selecting one would broaden or substitute the target. The
legacy module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_033.lean`, SHA-256
`4b4e66cfbc43f85647f9081d81d4b524f77bc49fcebec27d9cb9a511288d4242`,
explicitly treats `AlgebraicGeometry.IsProper` as a properness-only placeholder
for projectivity. Its auxiliary coordinate-ring wrappers and statement shape
are discovery inputs only, not an exact canonical target.

Accordingly the canonical human claim, Lean declaration/expression, minimal
imports, expression and environment fingerprints, checked transports, and all
four required mutation classes remain unavailable. The current declaration-free
`Statement.lean` elaborates at trust level 0, but that only checks its explicit
fail-closed boundary; it supplies no statement or proof credit.

## Commands and results

All commands ran inside this worker clone. The automation-provided `.lake`
symlink was reused read-only; no update, build, clone, fetch, or dependency
mutation ran.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok` with 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, the v2 DAG, the phase contract, and the execution skill present |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | `check_stage1_theorem_dag_v2: ok` with 1546 theorems, 10822 blueprint states, 2 hard edges, 5 reuse hints, 311 shared groups, acyclic |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok` with 1546 unique targets, ranks 1..1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0109` | 0 | rank 33; planned; legacy artifacts unaccepted; theorem incomplete |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0109/check_statement.py` | 1 | empty stdout; exact stderr quoted above; no semantic JSON object |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0109/Statement.lean` | 0 | empty output; declaration-free boundary elaborated, with no exact-target credit |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean --version`; `lake --version` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e` |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'`; `git status --short` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, clean package worktree |

The successful structural and Lean commands prove only the stated structural,
pin, and declaration-free-boundary facts. They do not self-test the assigned
positive statement phase and cannot be interpreted as `phase_accepted`.

## Retry condition and status boundary

The scheduler must refresh the declared statement validator in its authoritative
lane, commit it, and issue a fresh claim whose base contains the identical
validator blob and whose checks accept the current authoritative `[_]`/attempt-1
snapshot without treating it as a new `[ ] -> [_]` transition. A lawful replay
must emit exactly one semantic JSON object and preserve the blocked mathematical
verdict unless an independently reviewed immutable source actually resolves the
claim. The intake predecessor must separately receive master acceptance before
statement master closure.

This file is target-scoped blocker evidence only. It creates no new receipt,
no self-test manifest, no state transition, no canonical statement, no proof
credit, no audit completion, no theorem completion, and no master acceptance.
`.stage1-worker-selftest.json` remains absent as required.
