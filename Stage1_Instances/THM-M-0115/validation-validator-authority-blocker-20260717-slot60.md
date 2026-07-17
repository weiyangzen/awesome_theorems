# THM-M-0115 validation validator-authority blocker

## Scope

This is the target-scoped fail-closed result for
`S56-M-0115-VALIDATION` at worker base
`c6ccce54afcb261a3b4c236a3eb538a1e4b829a8` (tree
`13ac09d107589b9b20956e6d2e4c0696058a0b41`). Its exact claim order is
`(v2_execution_rank=260, phase_layer=5,
phase_item_id=S56-M-0115-VALIDATION)`.

The supplied `parent_inspection_order` is empty. That complete direct and
transitive parent closure was traversed exactly once before validation work.
There is no hard edge, reuse hint, or shared group, so no provider phase
state, receipt, declaration body, reusable artifact, checkbox state, proof
credit, or acceptance was consumed or transferred.

## First Failed Gate

`G05-AUTHORITY-REPLAY / validator_candidate_missing` fails before a lawful
validation self-test can exist. The HEAD phase contract declares only these
scheduler-owned candidate paths:

- `Stage1_Instances/THM-M-0115/check_validation.py`
- `Stage1_Instances/THM-M-0115/check_validation.sh`

Neither exists at the immutable worker base or current `HEAD`. Candidate
selection therefore has cardinality zero, no authority-selected argv, and no
possible stdout object with schema
`stage1-validator-semantic-result/1.0`. The worker is forbidden to create,
refresh, rename, replace, or delete either candidate. Structural checks, a
Lean exit code, or an undeclared adapter cannot substitute for the missing
semantic replay.

Accordingly this run deliberately writes no `validation-receipt.json`, no
validation specification, and no `.stage1-worker-selftest.json`.

## Prerequisite Boundary

The positive validation predicate is independently blocked:

- `S56-M-0115-PROOF` is authoritative `[_]`, not master-accepted `[x]`.
- Its exact `stage1-node-receipt/1.0` has `accepted=false`,
  `verdict=blocked`, and `phase_predicate_proven=false`; it closes none of the
  32 frozen positive obligations.
- No validation specification exists at a contract-selected path.
- The frozen graph records `root_closed=false`, machine debt `M3`, and the
  machine cut set `M0115-T-RELATIVE`, `M0115-T-TODD_ACTION`.

An isolated trust-zero replay of unchanged `Statement.lean` and `Proof.lean`
does provide truthful negative evidence. The target-owned declaration

```text
Stage1Instances.THMM0115.Proof.not_grothendieckRiemannRochTarget :
  Not (Stage1Instances.THMM0115.GrothendieckRiemannRochTarget.{0, 0})
```

is sorry-free and reports only `propext`, `Classical.choice`, and
`Quot.sound`. It uses `Spec(Q)` with identity morphisms and `Int` for both
abstract theory carriers; every semantic-label proposition is true while the
unconstrained cap operations reduce the formula to `1 = 0`. This refutes only
the current abstract encoding, not mathematical Grothendieck-Riemann-Roch,
and grants zero positive proof or validation credit.

The existing `dependency-reuse-ledger.json` truthfully records the still-empty
closure under schema `stage1-dependency-reuse-ledger/1.1`, but it is the
historical proof-phase ledger. It binds graph `8be71ef1...` and repository
revision `307c34d3...`; this claim binds graph
`95128825a99c9863fc09b6edc8a4a99ab5fae8e0927e40af88635f8945d2aa3e`
and stable dependency context
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
No validation ledger replacement is emitted because no validation self-test
or accepted hard-edge reuse exists to attach to a consumer receipt.

## Bounded Checks

Before adding this blocker pair, the Stage1 standard, theorem-DAG,
phase-contract, target-manifest, and target-display checks passed. Candidate
enumeration found exactly zero declared validation validators. The isolated
Lean 4.29.0 trust-zero statement and countermodel replay passed; statement
output SHA-256 was `bfff4eb7...`, and proof output SHA-256 was
`30974c6b...`. The owned Lean source scan found no prohibited proof escape or
unsafe declaration token.

The automation-provided pinned `.lake` symlink was reused read-only. No `lake
update`, `lake build`, dependency clone/fetch, network access, or intentional
cache mutation occurred. Exact commands, complete hashes, artifact-role
resolution, and authority bindings are recorded in the companion JSON.

After this pair is added, deterministic theorem-DAG inventory checks are
expected to observe new target-owned evidence while the worker remains
forbidden to regenerate the read-only projection. Scheduler integration owns
that regeneration. Target-scoped JSON parsing, whitespace validation, and
self-test absence are the remaining worker checks.

## Retry Condition

The scheduler/master lane must publish exactly one declared validation
candidate at authoritative `HEAD`, then issue a fresh claim whose immutable
base contains the identical blob. Positive validation also requires a
complete structured validation specification and a master-accepted positive
proof receipt. The refuted statement must first be reopened and replaced with
source-faithful structures and laws that bind every operation in the formula;
statement, anchor audit, obligation tree, and proof must then be reaccepted in
DAG order.

Current validation state remains `[ ]`; `audit_complete=false` and
`theorem_complete=false`. This blocker makes no M0, AUDIT-Z, THEOREM-Z,
release, validation acceptance, worker self-test, or master-acceptance claim.
