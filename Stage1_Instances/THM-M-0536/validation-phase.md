# THM-M-0536 validation-phase evidence

Item: `S56-M-0536-VALIDATION`. Base revision:
`bdfc69baefbe6cfce9a205be72f3d46cb31458e8`.

This validation independently checks the proof-phase claim rather than adding proof content. The
validator binds the frozen target, proof, obligation artifacts, proof receipt, Lean toolchain, Lake
manifest, pinned mathlib revision, and the exact upstream homotopy-invariance source. It scans the
Lean proof for placeholders and unsafe trust declarations, checks exact target-body identity, then
copies `Proof.lean` alone into a fresh temporary directory and asks the kernel to elaborate it.

## Commands and results

All commands ran in this worker clone on 2026-07-12. No network access, `lake update`, `lake build`,
dependency clone/fetch, or mutation of `.lake` occurred.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard structure and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | Manifest has 1546 unique ranked targets. |
| `python3 scripts/stage1_target.py show THM-M-0536` | 0 | Rank 593; planned; theorem completion false. |
| `python3 Stage1_Instances/THM-M-0536/check_validation.py` | 0 | Exact root replay, trust profile, pins, hashes, and provenance passed. |
| `python3 Stage1_Instances/THM-M-0536/check_proof.py` | 0 | Proof target, receipt binding, and prohibited-token checks passed. |
| `python3 Stage1_Instances/THM-M-0536/check_obligation_tree.py` | 0 | Frozen 15-obligation registry and typed graphs passed. |
| `git diff --check -- Stage1_Instances/THM-M-0536 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The fresh-source replay reported exactly `[propext, Classical.choice, Quot.sound]` for
`induced_left_identity`, `induced_right_identity`, and `homotopyInvariance`. The local proof root is
therefore kernel-closed under that trust profile, subject to master acceptance.

## Status boundary

This is provisional worker validation, not release evidence. It reuses the canonical pinned warm
`.lake` dependency cache, so the cold empty-cache hermetic gate remains open. It also runs in the
same checkout and is not the distinct signed independent runner required for release. Human-source,
readability, complete TCB/SBOM, audit, release, and master-acceptance gates remain open;
`theorem_complete` remains false.
