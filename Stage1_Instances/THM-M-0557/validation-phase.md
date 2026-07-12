# THM-M-0557 validation-phase evidence

Item: `S56-M-0557-VALIDATION`. Base revision:
`f1411d9611fd9a140123ade3316fdecb3a0b3f25`.

This phase rechecks the integrated proof without adding mathematical content. The validator binds
the frozen statement, obligation artifacts, proof source, proof receipt, Lean toolchain, Lake
manifest, clean mathlib revision, and exact upstream homotopy-group source. It independently checks
the root expression, scans for placeholders and unsafe declarations, and copies `Proof.lean` alone
to a fresh temporary directory before kernel elaboration. This prevents a dossier-local stale
`.olean` from satisfying the replay.

## Commands and results

All commands ran in this worker clone on 2026-07-12. No network access, `lake update`, `lake build`,
dependency clone/fetch, or `.lake` mutation occurred.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | Manifest has 1546 unique targets with ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0557` | 0 | Rank 605; planned; theorem completion false. |
| `python3 Stage1_Instances/THM-M-0557/check_validation.py` | 0 | Fresh-source root replay, trust profile, exact target, hashes, pins, and terminal-source provenance passed. |
| `python3 Stage1_Instances/THM-M-0557/check_proof.py` | 0 | Exact frozen expression and both proof branches passed. |
| `python3 Stage1_Instances/THM-M-0557/check_obligation_tree.py` | 0 | Frozen 9-obligation registry and 49 typed edges passed. |
| `git diff --check -- Stage1_Instances/THM-M-0557 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The replay reported exactly `[propext, Classical.choice, Quot.sound]` for
`groupStructureBranch`, `commutativeStructureBranch`, and `homotopyGroupStructureTarget`. It also
verified the clean mathlib pin `8a178386ffc0f5fef0b77738bb5449d50efeea95` and the source route through
`HomotopyGroup.group`, `auxGroup_indep`, `transAt_distrib`, `EckmannHilton.commGroup`, and
`HomotopyGroup.commGroup`.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | Pass | A fresh temporary copy of the exact proof source elaborated against pinned Lean 4.29.0 and mathlib. |
| Exact target and composition | Pass | Independent expression comparison and the three checked declarations close the frozen conjunction. |
| Placeholder and unsafe scan | Pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration appears. |
| Trust observation | Provisional pass | All three declarations report only `propext`, `Classical.choice`, and `Quot.sound`. Authoritative foundation acceptance remains master work. |
| Local provenance | Pass | Dossier hashes, proof receipt, manifest and revision pins, clean dependency tree, upstream source hash, and terminal route agree. |
| Hermetic release replay | Fail closed | The run reused the canonical writable warm dependency cache; there was no empty-cache offline restoration, cold build, or full TCB/SBOM archive. |
| Independent verification | Fail closed | This is the same worker clone and validator, without a second identity, separately provisioned runner, signed attestation, or independently implemented verifier. |

This is self-tested provisional worker evidence. It supports local root proof-body closure but grants
no release, `AUDIT-Z`, `THEOREM-Z`, independent-verification, or master-acceptance credit.
`theorem_complete=false`.
