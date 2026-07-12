# Obligation-tree validation

Validation date: 2026-07-12 (Asia/Shanghai). Base revision:
`aa55669bb59986e08ea8a0d1d77a1e40343d8142`.

The registry was frozen before observing proof closure against `Statement.lean` and the bounded
anchor audit. It contains 16 stable obligations with denominator SHA-256
`837ddd3dab2eb1adcf59994e8ec4d3bfeeeb8f07f8f562e4df589aa18a6f4d65`. The seven typed graphs
contain 55 reciprocal edges. The checked Lean interface packages graph containment and derivative
components into `IsSolutionWithin`; it accepts those components as premises and supplies no
existence proof.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1333/build_obligation_artifacts.py` | 0 | Wrote 16 obligations; denominator hash as above |
| `python3 Stage1_Instances/THM-M-1333/check_obligation_tree.py` | 0 | `PASS THM-M-1333 obligation tree: 16 obligations, 55 typed edges`; root open at M4 |
| `python3 Stage1_Instances/THM-M-1333/check_obligation_lean.py` | 0 | Pinned `lake env lean` elaborated the interface; axioms `[propext, Classical.choice, Quot.sound]` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard structure accepted: 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | Manifest accepted: 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1333` | 0 | Rank 874, planned, L0/rework required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1333 .stage1-worker-selftest.json` | 0 | No whitespace errors |
| prohibited-token scan over changed proof/registry artifacts | 1 | Expected negative search: no prohibited proof device found |

The initial direct command `cd Formalizations/Lean && lake env lean
../../Stage1_Instances/THM-M-1333/ObligationTree.lean` exited 1 because standalone Lean cannot
resolve the sibling source module without a built local `.olean`. `check_obligation_lean.py`
therefore concatenates the already checked statement and interface into a temporary target-owned
file, invokes the same pinned `lake env lean`, and deletes the temporary file. It does not build,
fetch, or mutate `.lake`.

This is dirty-tree, nonrelease worker evidence pending master acceptance. All substantive proof
obligations remain open; audit completion and theorem completion are false.
