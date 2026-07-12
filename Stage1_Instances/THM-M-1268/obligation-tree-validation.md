# Obligation-tree validation

Item: `S56-M-1268-OBLIGATION_TREE`  
Base revision: `6fe9e10bc6bd77776ffbe03647af1d6c084ba5b9`

## Result

Registry version 1 freezes 12 obligations and 37 separately typed proof, refinement,
provenance, evidence, trust, documentation, and workflow edges. The canonical denominator digest
is `e92b609b6826f7f67149484343b7824f3d9d397c7256f1ccc16660464d692161`.

The Lean harness replays the exact frozen statement interfaces because the dossier is outside the
Lake source tree, checks both closed-sublevel equivalences, and kernel-checks conditional
child-to-parent composition for the norm-to-weak direction and the root. The harness assumes the
three explicitly typed open bridges; it neither implements them nor proves the root. Its local
interface is bound to the independently re-elaborated `Statement.lean` by the statement hash in the
registry.

## Commands and results

Commands ran on 2026-07-12. Lean reused the existing pinned `.lake` artifacts; no update, build,
clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1268` | 0 | rank 444, planned, theorem incomplete |
| `python3 Stage1_Instances/THM-M-1268/build_obligation_artifacts.py` | 0 | deterministically generated 12 obligations and 37 edges |
| `python3 Stage1_Instances/THM-M-1268/check_obligation_tree.py` | 0 | denominator, IDs, eligibility sets, graph endpoints/indexes, closure boundary, and cut set passed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1268/Statement.lean` | 0 | exact frozen target and expanded transport re-elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1268/ObligationTree.lean` | 0 | typed interfaces, exact local statement replay, support anchor, and conditional compositions elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-1268/obligation-registry.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1268/typed-graphs.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1268` | 0 | no whitespace errors |

## Open gate

No obligation is marked closed. The remaining root cut is convexity of EReal sublevels, exact weak
closure/image transport, and the continuous weak-to-norm direction. Source pinpointing, terminal
proof-body provenance, transitive trust, readable reconstruction, and release validation also
remain open. Root debt is `M4`; this phase claims only a self-tested architecture pending master
acceptance, not proof, audit completion, or theorem completion.
