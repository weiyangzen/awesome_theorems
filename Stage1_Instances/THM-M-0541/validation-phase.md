# THM-M-0541 validation-phase evidence

Item: `S56-M-0541-VALIDATION`. Base revision:
`e694abee3f44557daf2f54147d968edf96e64752`.

The validator binds the frozen statement, proof, obligation registry, typed graphs, anchor audit,
toolchain manifest, and pinned mathlib revision. It scans the proof for placeholders and new unsafe
trust declarations, copies only `Proof.lean` into a fresh temporary directory, and asks the Lean
kernel to elaborate the claimed root. This prevents a dossier-local compiled artifact from
supplying the declaration.

## Commands and results

All commands ran in the worker clone on 2026-07-12. No network access, dependency fetch, `lake
update`, `lake build`, or `.lake` mutation occurred.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard structure and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | Manifest has 1546 unique ranked targets. |
| `python3 scripts/stage1_target.py show THM-M-0541` | 0 | Rank 598; planned; theorem completion false. |
| `TZ=UTC LC_ALL=C.UTF-8 python3 Stage1_Instances/THM-M-0541/check_validation.py` | 0 | Fresh-source exact-root replay, trust profile, pins, hashes, and provenance passed. |
| `python3 Stage1_Instances/THM-M-0541/check_proof.py` | 0 | Exact-root markers, proof bodies, and prohibited-construct scans passed. |
| `python3 Stage1_Instances/THM-M-0541/check_obligation_tree.py` | 0 | Frozen 36-obligation registry and seven typed graphs passed. |
| `git diff --check -- Stage1_Instances/THM-M-0541 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The kernel reported exactly `[propext, Classical.choice, Quot.sound]` for
`Stage1Instances.THM_M_0541.statementShape`, with no `sorryAx`.

## Status boundary

This is provisional worker validation, not release evidence. It reuses the canonical pinned warm
`.lake` dependency cache, so the cold empty-cache hermetic gate remains open. Running a new local
validator in this same checkout is also not the distinct signed independent runner required by
rev-5.6. H0/R0 review, complete TCB/SBOM and license closure, audit, release, and master acceptance
remain open; `theorem_complete` remains false. The first failed gate is
`S56-10.6-HERMETIC-COLD-BUILD`.
