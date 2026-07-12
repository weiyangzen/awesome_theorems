# Anchor-audit validation record

Item: `S56-M-1143-ANCHOR_AUDIT`  
Base revision: `3727de2a4ceed9cd590d437f2e2e51c1a2e7c172`

All local checks used the existing pinned Lake closure. Network probes were read-only searches; no
package update, build, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1143/AnchorAudit.lean` | 0 | candidate type elaborated, plane specialization checked, candidate axioms printed |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib show -s --format='%H %T' HEAD` | 0 | commit and tree match the audit record |
| scoped `rg` over repo-local and pinned package Lean sources | 0 | close plane anchor found; no exact all-dimensional declaration found |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1143` | 0 | rank 348, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1143/anchor-audit.json` | 0 | structured audit parses |
| scoped prohibited-token scan of anchor-audit artifacts | 1 | clean; exit 1 means no forbidden proof placeholder matched |
| `git diff --check -- Stage1_Instances/THM-M-1143 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The Lean output reports the candidate axioms as `propext`, `Classical.choice`, and `Quot.sound`.
Passing this check validates candidate inspection only and does not close the theorem.
