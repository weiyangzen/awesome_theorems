# Obligation-tree validation record

Item: `S56-M-1061-OBLIGATION_TREE`  
Base revision: `6e150acf7218670345921eaa8bae426adf83c677`

## Result

Registry version 1 freezes 15 distinct semantic obligations with denominator
SHA-256 `9b84baaedfed9f75ef3fce37e77b91bb48ddabb2dd1316216bf7c84ea5d4e811`.
The bundle contains separate proof, refinement, provenance, evidence, trust,
documentation, and workflow graphs with 49 typed edges. Required proof edges
have reciprocal composition edges, the required-machine graph is root
reachable and acyclic, and every node owns the rev-5.6 node fields and a
validation recipe.

The Lean check reports only `propext`, `Classical.choice`, and `Quot.sound` for
the conditional identity composition. The exact analytic terminal remains M4,
the root remains open at M3, and the theorem is not complete.

## Commands and results

Commands ran inside this worker clone on 2026-07-12. No dependency or `.lake`
artifact was updated, fetched, cloned, or built.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1061/build_obligation_artifacts.py` | 0 | deterministically emitted registry, graph bundle, and validation specs; printed the frozen denominator hash |
| `python3 Stage1_Instances/THM-M-1061/check_obligation_tree.py` | 0 | PASS: 15 obligations, 49 typed edges, root open |
| `{ sed -n '1,$p' ../../Stage1_Instances/THM-M-1061/Statement.lean; sed -n '1,$p' ../../Stage1_Instances/THM-M-1061/ObligationTree.lean; } > /tmp/THM-M-1061-ObligationTree.lean && lake env lean /tmp/THM-M-1061-ObligationTree.lean` from `Formalizations/Lean` | 0 | exact statement plus conditional composition elaborated; axiom report was `propext`, `Classical.choice`, `Quot.sound` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | repository standard and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | ordered 1546-target manifest passed |
| `python3 scripts/stage1_target.py show THM-M-1061` | 0 | rank 504, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1061 .stage1-worker-selftest.json` | 0 | no whitespace errors |

Status boundary: this self-tests the assigned obligation-tree freeze only. It
does not claim proof-phase closure, H0, root M0, validation, release, master
acceptance, or theorem completion.
