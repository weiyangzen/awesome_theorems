# THM-M-0121 anchor-audit scheduler blocker

Item: `S56-M-0121-ANCHOR_AUDIT`

Worker base: `e19e77ec08fca6a8a9c45a003c9904020dae8382`

Claim order: `(v2_execution_rank=274, phase_layer=2, phase_item_id=S56-M-0121-ANCHOR_AUDIT)`

Verdict: `blocked`; no phase state is proposed.

## First failed gate

`G05-AUTHORITY-REPLAY.validator_requires_exactly_one_unchanged_HEAD_candidate_present_at_worker_base`

The mandatory HEAD contract declares these scheduler-owned candidates:

- `Stage1_Instances/THM-M-0121/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0121/check_anchor.py`

Neither exists at the immutable worker base or in this worker tree. The required count is exactly
one. Worker policy forbids creating, refreshing, renaming, replacing, or deleting either path, so
there is no legal validator argv and no `stage1-validator-semantic-result/1.0` output. Per the
explicit zero-candidate rule, this run emits no anchor inventory, discovery-evidence packet, phase
receipt, `AnchorAudit.lean`, or `.stage1-worker-selftest.json`.

The predecessor is independently not ready for master closure:
`S56-M-0121-STATEMENT` is `[_]`, not `[x]`, and its receipt truthfully reports that the catalog does
not select an exact proposition.

## DAG and reuse boundary

The theorem-DAG SHA-256 is
`53622c848d6a0d8327bba8cd22bf45463f0dd8acb7ea0af2884713983e76c91f`; the target context digest is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
The complete parent inspection order, direct/transitive parent closure, hard-edge list, hint list,
and shared-group list are all empty. The supplied empty sequence was traversed exactly once before
any possible proof work. No proof work occurred and no provider body, receipt, checkbox state,
acceptance, or proof credit was consumed.

The tracked schema-1.1 reuse ledger is an older statement-phase binding. Refreshing it alone cannot
repair scheduler authority, would stale the predecessor receipt's exact input hash, and cannot
support an anchor receipt. A fresh executable anchor claim must refresh the ledger and all consumer
bindings together.

## Current-base observations

These read-only observations are guidance, not the contract's completed seven-lane inventory:

- The source label remains ambiguous among nef-threshold rationality, rational curves or
  uniruledness, rational connectedness, and birational rationality. The unqualified assertion that
  every Fano variety is rational is false.
- The repo-local legacy module is content-bound at SHA-256
  `327fabea1a35f1dd6bf0c7db33a86518cbf50a046fa3f52cec963f2eef8351f3`. It parameterizes both the
  Fano input and conclusion and contains no exact terminal Mori proof, so it is M3 interface and
  discovery material only.
- Pinned mathlib is at revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. Its rational-map source is adjacent representation
  support, not a root theorem. A bounded local exact-topic scan found only the legacy interface and
  a declaration-free `docs/1000.yaml` title; neither is an exact candidate.
- No immutable external project, other-prover snapshot, or admitted primary-source passage was
  supplied. With network denied, those lanes are unexecuted rather than falsely classified as
  exhaustive negative results.

The honest boundary remains H3/M4/R4. No M0/M1, H0, R0, `AUDIT-Z`, `THEOREM-Z`, or theorem
completion follows.

## Commands and results

All commands ran without fetching, updating, or otherwise mutating `.lake`.

| Command | Exit | Result boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 targets, the v2 DAG, phase contract, and skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorems, 10822 phase states, 2 hard edges, 5 hints, 311 groups, acyclic. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phases, twelve common gates, and twenty-three source references passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0121` | 0 | Rank 40, planned, legacy artifacts unaccepted, theorem incomplete. |
| base-tree and worker-tree checks for both declared anchor validators | 0 | Expected blocker assertion passed: eligible candidate count is zero. |
| from `Formalizations/Lean`: `env LEAN_NUM_THREADS=1 LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0121/Statement.lean` | 0 | Adjacent rational-map interfaces elaborated; there is no canonical target or proof body. |
| from `Formalizations/Lean`: `env LEAN_NUM_THREADS=1 LC_ALL=C TZ=UTC lake env lean --trust=0 AwesomeTheorems/Stage1/S1_M_040.lean` | 0 | The legacy parameterized interface elaborated; no exact-root credit follows. |
| post-edit `python3 Docs/tools/check_stage1_standard.py` | 1 | Expected projection drift: deterministic generation inventories the new owned blocker while this worker may not rewrite the checked-in theorem DAG. |
| post-edit `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | Expected projection drift after adding owned evidence; master integration must regenerate the read-only projection. |
| `git diff --check -- Stage1_Instances/THM-M-0121 .stage1-worker-selftest.json` | 0 | Target-scoped files have no whitespace errors. |

The Lean invocations emitted non-fatal sandbox stream-fd diagnostics. Their zero exits validate only
the scoped elaboration observations and cannot substitute for the missing semantic validator.

## Retry condition

The scheduler must commit exactly one declared anchor validator and issue a fresh base containing
its unchanged blob. The statement predecessor must separately reach `[x]` with one exact,
source-faithful proposition. A fresh worker can then refresh the ledger, execute and content-bind
all seven ordered lanes, emit exactly one node receipt, and replay the immutable validator before
writing a self-test handoff.

This target-scoped blocker grants no phase transition, phase receipt, proof credit, audit
completion, theorem completion, or master acceptance.
