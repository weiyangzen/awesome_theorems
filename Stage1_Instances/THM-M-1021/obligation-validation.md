# THM-M-1021 obligation-tree validation

Item: `S56-M-1021-OBLIGATION_TREE`  
Base revision: `08405432a9f96f6c39ff79724e7f5965d01305ca`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The validator parsed the frozen registry and typed graph bundle, recomputed
the denominator digest, required the complete rev-5.6 node schema, checked
one-to-one registry/node identity, checked all seven graph kinds and reciprocal
edge indexes, rejected duplicate and illegal edge types, and established that
the combined proof/refinement relation is acyclic and root-reaching for all 46
required mathematical obligations. The inventory has 50 obligations and 65
typed edges. Four `M1021-X*` trust/provenance overlays are informational and
cannot contribute mathematical proof credit.

The exact statement re-elaborated using the pinned Lean executable. The
pre-existing untracked `Formalizations/Lean/.lake` artifact was reused and not
modified. No update, build, clone, fetch, or dependency mutation was run.

## Commands and exact outcomes

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1021` | 0 | rank 497, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 Stage1_Instances/THM-M-1021/build_obligation_artifacts.py` | 0 | deterministically built 50 obligations; denominator `032b467a...24688` |
| `python3 Stage1_Instances/THM-M-1021/check_obligation_tree.py` | 0 | `PASS THM-M-1021 obligation tree: 50 obligations, 65 typed edges`; root open M3 |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1021/BochnerStatement.lean)` | 0 | exact `BochnerTarget` proposition re-elaborated; no diagnostics |
| `python3 -m json.tool Stage1_Instances/THM-M-1021/obligation-registry.json >/dev/null` | 0 | frozen registry is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1021/typed-graphs.json >/dev/null` | 0 | typed graph bundle is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1021 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This self-tests only the architecture freeze. Planned signatures and semantic
ledgers are not proofs, the mathlib anchors do not prove the reverse direction,
and no parent has a checked composition certificate. No H0, R0, proof body,
audit completion, or theorem completion is claimed. The root stays
`[H1, M3, R3]`; master acceptance remains required for the assigned item.
