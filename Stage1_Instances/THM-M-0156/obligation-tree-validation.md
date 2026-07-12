# Obligation-tree validation record

Item: `S56-M-0156-OBLIGATION_TREE`  
Base revision: `27d1586e034f95cbf63801bb339532733308fd9a`

The registry freezes 16 obligations and seven separate typed graphs. `ObligationTree.lean` checks
the conditional empty-exception composition without importing proof credit from the audited
candidate. Validation uses only the existing pinned Lake artifacts and performs no update, build,
fetch, clone, or dependency mutation.

## Commands and results

| Command | Exit/result |
|---|---|
| `python3 Stage1_Instances/THM-M-0156/build_obligation_artifacts.py` | 0; built 16 obligations and frozen denominator digest |
| `python3 Stage1_Instances/THM-M-0156/check_obligation_tree.py` | 0; 16 obligations and 23 typed edges passed; root open M3 |
| `python3 -m json.tool Stage1_Instances/THM-M-0156/obligation-registry.json` | 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0156/typed-graphs.json` | 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0156/validation-specs.json` | 0; valid JSON |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0156/ObligationTree.lean` | 0; conditional composition elaborated; axiom output recorded |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0156/Statement.lean` | 0; predecessor exact statement re-elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0156/AnchorAudit.lean` | 0; predecessor exact candidate adapter re-elaborated |
| `git diff --check -- Stage1_Instances/THM-M-0156 .stage1-worker-selftest.json` | 0; no whitespace errors |

## Boundary

This phase freezes architecture and checks conditional child-to-parent composition. It does not
accept the pinned theorem as the proof node. The candidate's complete transitive provenance/trust,
proof-phase receipt, human source, readable review, hermetic and independent validation, master
acceptance, audit completion, and theorem completion remain open.

The first `ObligationTree.lean` run failed because the empty set was written as the nonexistent
identifier `Set.empty`; Lean also reported the resulting recovery term through `sorryAx`. The term
was corrected to `(∅ : Set (Euclidean n))`, then the checker and Lean command were rerun. The final
successful output above contains only `propext`, `Classical.choice`, and `Quot.sound`; the failed
output is not proof evidence.
