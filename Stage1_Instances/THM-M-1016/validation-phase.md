# S56-M-1016-VALIDATION worker evidence

Validation time: `2026-07-14T02:33:47+08:00` to `2026-07-14T02:36:14+08:00`. Base revision:
`3bb4cb3ae15dff8b48c93242019edec3bf858e48`.

The node-scoped validator copied the exact frozen statement, composition module, proof, and an
exact-type probe into a fresh temporary directory. It then elaborated all four modules with the
existing pinned Lean toolchain inside a network-isolated bubblewrap sandbox whose host root was
read-only. The composition certificate, seven proof declarations, and exact
root probe report exactly `propext`, `Classical.choice`, and `Quot.sound`. Nine elaborator-aware
`assert_no_sorry` probes, source hygiene, frozen
hashes, obligation denominator, proof receipt, clean mathlib pin, and named terminal source/olean
hashes also pass.

`Validation.lean` deliberately imports `Proof.lean`: it checks the proof declaration's exact frozen
type but does not pretend to be a second proof. The immutable typed graph still contains its honest
pre-proof observation. Both facts are recorded fail-closed rather than rewritten by this worker.

## Gate results

| Gate | Result | Evidence or boundary |
|---|---|---|
| Exact kernel replay | pass provisionally | Fresh temporary copies of `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and `Validation.lean` elaborate with network isolated and dependency sources read-only. |
| Exact target and composition | pass provisionally | `statementProof` and `exactRootProbe` inhabit the unchanged `StatementShape`; the frozen conditional composition also kernel-checks. |
| Source hygiene | pass | Nine `assert_no_sorry` probes pass, and comment-stripped sources contain no `sorry`, `admit`, `sorryAx`, local `axiom`, `unsafe`, or `implemented_by`. |
| Axiom observation | pass as observation only | All nine declarations report the same three classical mathlib axioms. The versioned foundation-profile acceptance gate remains open. |
| Local/pinned provenance | pass for named surfaces | Local input hashes, manifest revision/tree, clean mathlib source, and three terminal source/olean pairs agree. Full transitive provenance/TCB closure remains open. |
| Structured-state freshness | fail closed | The frozen pre-proof graph still reports root M3 and `M1016-T-REMAINDER` open; master reconciliation is required. |
| Hermetic release replay | fail closed | Network and write isolation passed, but the recipe reused a shared warm `.lake` symlink; it was not an empty-cache cold build or offline archive restoration. |
| Independent verification | fail closed | The exact-type probe ran in this mutable worker and cache. There is no distinct signed independently provisioned runner or independent minimal verifier. |

## Commands and exact results

```text
$ env -i /usr/bin/python3 Stage1_Instances/THM-M-1016/check_validation.py
exit 0
validation: PASS: exact statement, composition, proof root, and exact-type probe kernel-replayed from fresh temporary sources with network isolated and dependency sources read-only
validation: PASS: all nine checked declarations report exactly propext, Classical.choice, and Quot.sound
validation: PASS: elaborator-aware no-sorry checks, source hygiene, frozen hashes, denominator, proof receipt, dependency pin, terminal provenance, and clean mathlib checks passed
validation: STALE: frozen typed graph predates proof closure and awaits master reconciliation
validation: BLOCKED release-only: the read-only shared warm .lake is not a cold empty-cache replay and the foundation/TCB profile is not release-closed
validation: BLOCKED release-only: exact-type replay in this worker is not a distinct independently provisioned verifier
validation spec sha256: 60654897c290ad7c84e891a9f2cbc6f4a6b3066d0e40755a4f5dce5eee9e31af
validation probe sha256: ddd214e7013a802f5d5f3a498a40bd46d2f8afd8831fd525ba4c9d6998f9b448
validator sha256: 98d362ce2820acdcbd1c98b366fc279b12bab4bb04e365998076fbb165fcc4e1

$ python3 Docs/tools/check_stage1_standard.py
exit 0; 15 assurance groups and 1546 uniform-L0 targets valid

$ python3 scripts/stage1_target.py check
exit 0; 1546 unique targets, ranks 1..1546, all L0/rework-required

$ python3 scripts/stage1_target.py show THM-M-1016
exit 0; rank 295, planned, theorem_complete false

$ python3 Stage1_Instances/THM-M-1016/check_statement.py
exit 0; canonical expression fingerprint matched and all four mutations were distinguished

$ python3 Stage1_Instances/THM-M-1016/check_anchor_audit.py
exit 0; anchor structure, source hashes, classifications, and status boundary passed

$ python3 Stage1_Instances/THM-M-1016/check_obligation_tree.py
exit 0; 14 obligations and 32 typed edges passed; frozen pre-proof root remains open

$ bash Stage1_Instances/THM-M-1016/check_proof.sh
exit 0; seven proof declarations report exactly propext, Classical.choice, and Quot.sound

$ python3 Stage1_Instances/THM-M-1016/check_proof.py
exit 0; exact root and analytic proof bodies passed source/input checks

$ cd Formalizations/Lean && lake env lean --version
exit 0; Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740

$ git diff --check -- Stage1_Instances/THM-M-1016 .stage1-worker-selftest.json
exit 0; no output
```

No `lake update`, `lake build`, dependency clone/fetch, network dependency operation, or `.lake`
mutation was performed.

## Status boundary

This is a self-tested provisional validation-node handoff, pending master acceptance. The first
dependency failure is proof master acceptance; the first local validation failure is foundation
profile acceptance; and the first release failure is the cold hermetic gate. No `E0/E1`, accepted
`M0-L`, `H0`, `R0`, `AUDIT-Z`, `THEOREM-Z`, release, or theorem completion is claimed.
