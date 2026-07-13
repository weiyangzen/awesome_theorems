# THM-M-0912 proof-phase validation

Item: `S56-M-0912-PROOF`. Base revision:
`5931467f7eefac7a6e57777cc3082e4a2edc03d4` (tree
`45a10c953e5dc79c1eb9ae7d755ee84866717775`).

## Implemented proof route

`Proof.lean` adopts `Nat.choose_eq_choose_pred_add` from manifest-pinned mathlib as the exact
predecessor recurrence. It applies the already checked positive-row and summand-order bridges and
the frozen `root_of_bridges_and_predecessorAnchor` composition to obtain the unchanged
`PascalIdentityTarget`.

The module also exposes the two children inside the pinned theorem body. It installs
`Nat.choose_succ_right` at `ChooseSuccRightAnchor`, implements the positive-column reindexing with
`Nat.exists_eq_add_of_le'`, and consumes both through
`predecessorRecurrence_of_chooseSuccRight_and_reindex`. A second exact root exercises this full
frozen route. Both roots share the same mathlib proof family and are not counted twice.

The terminal bodies remain in `Mathlib/Data/Nat/Choose/Basic.lean` at pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. They are not vendored. This proof phase therefore
proposes `M0-W` only; master acceptance and downstream validation remain required.

## Commands and results

Validation ran in the isolated worker clone on 2026-07-13 (Asia/Shanghai). The existing canonical
pinned `.lake` symlink was reused. No `lake update`, `lake build`, dependency clone/fetch, network
operation, source edit, or `.lake` mutation was performed.

```text
bash Stage1_Instances/THM-M-0912/check_proof.sh
  exit 0
  complete stdout SHA-256 c992e4e246af412dc7a18bf35e90239c8c91607c7905916109f87a42e27f2726
  isolated Statement.olean and ObligationTree.olean elaborated under /tmp and were removed
  Proof.lean elaborated with lake env lean
  Nat.choose_succ_right, Nat.choose_eq_choose_pred_add, and all eight local declarations were
  sorry-free; every axiom report was exactly [propext]
  both declarations of the exact PascalIdentityTarget closed

python3 -B Stage1_Instances/THM-M-0912/check_proof.py
  exit 0
  exact item identity, canonical fingerprint, registry denominator, complete proof-graph
  reachability, source/olean pins, local wrappers, composition, receipt, and handoff passed

python3 -B Stage1_Instances/THM-M-0912/check_obligation_tree.py
  exit 0
  deterministic frozen architecture and its pre-proof open observation still passed

python3 -B Stage1_Instances/THM-M-0912/check_intake.py
  exit 1
  historical checker hardcodes its intake-plus-statement file set and rejects the already-expanded
  dossier; the same incompatibility exists at this worker's base before the new proof files

python3 -B Stage1_Instances/THM-M-0912/check_statement.py
  exit 1
  historical checker expects authoritative statement state [ ], while the current base records [_]

python3 -B Stage1_Instances/THM-M-0912/check_anchor_audit.py
  exit 1
  historical checker requires its original anchor-audit HEAD rather than the current worker base

python3 Docs/tools/check_stage1_standard.py
  exit 0
  15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0
  1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-0912
  exit 0
  rank 1454, planned, L0/rework_required, theorem_complete false

python3 -m json.tool Stage1_Instances/THM-M-0912/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0
  both proof-phase JSON artifacts parsed

PYTHONPYCACHEPREFIX=/tmp/stage1-m0912-proof-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0912/check_proof.py
  exit 0

git diff --check -- Stage1_Instances/THM-M-0912 .stage1-worker-selftest.json
plus direct trailing-whitespace/newline checks over every new proof-phase file
  exit 0; no whitespace errors
```

## Status boundary

This is genuine kernel-checked proof progress but does not claim theorem completion. The accepted
instance remains `[H1, M3, R4]` with no accepted proof receipt until the integration lane acts.
`M0912-S-FOUNDATION`, H0 primary-source mapping, R0 readable review, transitive provenance and
trust, hermetic replay, independent verification, validation, release, `AUDIT-Z`, and `THEOREM-Z`
remain open. The shared warm cache also makes this nonrelease evidence.

The three predecessor-checker failures above are snapshot-maintenance limitations, not Lean proof
failures. This proof lane leaves those immutable predecessor artifacts untouched; the integration
lane must reconcile phase-tolerant aggregate replay before accepting downstream release evidence.
