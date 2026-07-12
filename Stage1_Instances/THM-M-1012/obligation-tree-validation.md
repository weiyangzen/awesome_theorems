# Obligation-tree validation

Item: `S56-M-1012-OBLIGATION_TREE`  
Base revision: `a379e5a45829099a04e92cce109f4ac3568d02c0`  
Date: `2026-07-12`

All checks used the worker clone and the existing pinned Lake environment. No dependency was
fetched, updated, cloned, or built.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1012/build_obligation_artifacts.py` | 0 | deterministically built 14 obligations; denominator SHA-256 `b62eb6e1869e2c7db9f45ad1ea1e5b467280a9a2fd75a339916b7c5a5815edfb` |
| `python3 Stage1_Instances/THM-M-1012/check_obligation_tree.py` | 0 | required schemas, denominators, typed reciprocity, reachability, cycle checks, recipes, and open closure boundary passed; 61 typed edges |
| `lake env lean ../../Stage1_Instances/THM-M-1012/ObligationTree.lean` | 0 | exact reverse and root composition interfaces elaborated; both report only `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1012` | 0 | rank 291, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1012` | 0 | no whitespace errors |

## Known failures and boundary

The first Lean attempt failed with unknown identifier `iff_intro`; replacing it with the correct
Lean 4 constructor `Iff.intro` made the exact same composition check pass. That failed attempt is
not evidence and is recorded here for reproducibility.

The graph freeze is self-tested, but master acceptance remains external to this worker. The proof
phase must validate or implement the required formal children; exact primary-source mapping,
readable reconstruction, hermetic replay, freshness, independent verification, and release receipts
remain open. Consequently `root_closed=false` and `theorem_complete=false`.
