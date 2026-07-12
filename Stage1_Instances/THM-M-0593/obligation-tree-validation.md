# Obligation-tree validation receipt

Item: `S56-M-0593-OBLIGATION_TREE`  
Theorem: `THM-M-0593`  
Base revision: `b6840b8306a1983491c1963271bd791635c42c3f`  
Date: `2026-07-12` (Asia/Shanghai)

Registry version 1 contains 22 unique obligations and freezes denominator SHA-256
`ff56394a72695c35f72ed72fc1c961a3297943517a2e8b8056047678fb1157e2` against
`Statement.lean` SHA-256 `dd2a4da4f6cb0b0723a656e627378047834867641d63c6e5a8a0255108aed3bb`
and `anchor-audit.md` SHA-256
`4169509b09d08680e68933766c43b726e21b748e7cd0eaa07192f4a637950577`.

All Lean commands used the existing pinned `.lake` tree. The temporary `/tmp/thm-m-0593-lean`
directory held only the locally compiled `Statement.olean`; no dependency update, build, clone,
fetch, or `.lake` mutation was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0593` | exit 0; rank 633, planned, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0593/build_obligation_artifacts.py` | exit 0; deterministically built 22 obligations; denominator digest above |
| `python3 Stage1_Instances/THM-M-0593/check_obligation_tree.py` | exit 0; 22 obligations and 43 typed edges; reciprocal proof edges, reachability, acyclicity, schemas, denominators, recipes, and fail-closed boundary passed |
| `python3 -m json.tool` on the registry, typed graphs, and validation specs | each exit 0 |
| `cd Formalizations/Lean && lake env lean -R ../../Stage1_Instances/THM-M-0593 -o /tmp/thm-m-0593-lean/Statement.olean ../../Stage1_Instances/THM-M-0593/Statement.lean` | exit 0; exact `SardTarget : Prop` compiled outside `.lake` |
| `cd Formalizations/Lean && LEAN_PATH=/tmp/thm-m-0593-lean lake env lean ../../Stage1_Instances/THM-M-0593/ObligationTree.lean` | exit 0; conditional root composition elaborated; axioms `[propext, Classical.choice, Quot.sound]` |
| `git diff --check -- Stage1_Instances/THM-M-0593 .stage1-worker-selftest.json` | exit 0; no output |

This phase is self-tested and proposes only the frozen architecture for master acceptance. The
root remains open at `M4`. The remaining cut is `M0593-L-DIMENSION-IMAGE`,
`M0593-L-RANK-REDUCTION`, and `M0593-L-TAYLOR`; no proof body is claimed for them. Human source
pinpointing below theorem level, readable reconstruction, transitive trust/provenance acceptance,
proof closure, independent validation, audit completion, and theorem completion remain open.
