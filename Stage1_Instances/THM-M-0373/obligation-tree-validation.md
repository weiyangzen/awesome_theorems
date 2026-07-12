# Obligation-tree validation record

Item: `S56-M-0373-OBLIGATION_TREE`  
Base revision: `3f994388953e417edafd54b069ab45d648619698`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The registry contains 20 unique semantic records and 59 typed edges. Its
canonical denominator is
`d9e327aa6b5172feb581b020248ede731797b2ef6a1f40d837a8ace1e1ed67e9`.
Exact statement and anchor-audit file hashes bind the freeze. Proof edges are
acyclic, every required machine node is root-reachable, semantic budgets are
between 1 and 100, and proof, refinement, provenance, evidence, trust,
documentation, and workflow graphs remain separate.

The Lean harness checks only conditional final-child composition. Lean reports
`propext`, `Classical.choice`, and `Quot.sound` for that harness. It does not
prove the corona theorem. All `closed_obligations` remain empty; the root is
`M4`, and the analytic/dbar construction cut remains open.

## Commands and results

All commands ran in this worker clone. Lean used the existing pinned Lake
environment. No update, build, clone, fetch, or other `.lake` mutation command
was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0373/build_obligation_artifacts.py` | 0 | wrote 20 obligations and 59 edges; printed the denominator above |
| `python3 Stage1_Instances/THM-M-0373/check_obligation_tree.py` | 0 | hashes, denominator, graphs, reachability, acyclicity, budgets, open boundary, and placeholder scan passed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0373/ObligationTree.lean` | 0 | conditional root interface elaborated; axioms printed as `propext`, `Classical.choice`, `Quot.sound` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0373/Statement.lean` | 0 | exact frozen statement and transport re-elaborated |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets valid |
| `python3 scripts/stage1_target.py show THM-M-0373` | 0 | rank 865, planned, L0/rework required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0373 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The first later gate is proof-phase exact signatures and node-specific proof,
provenance, trust, and composition evidence. Master acceptance is separate.
