# Obligation-tree validation record

Item: `S56-M-0987-OBLIGATION_TREE`  
Base revision: `c6077f63d112c9e6b348b0e7e2370bc1b6024593`

## Result

Registry version 1 freezes 20 canonical obligations and 36 typed edges across separate proof, refinement, provenance, evidence, trust, documentation, and workflow graphs. The denominator SHA-256 is `8345bb31e9d2f5c8eb87d11211645ceb206a87ac10633d1deccfb1a01bd82cfe`. The proof graph expands the pinned theorem through its zero/nonzero variance split and characteristic-function route, while keeping source and release overlays out of machine closure.

`ObligationTree.lean` checks the final conditional composition from an explicit exact bridge premise to a local transcription of the frozen canonical root. Lean reports only `propext`, `Classical.choice`, and `Quot.sound`. The bridge premise is deliberately not inhabited here: `M0987-X-PINNED` remains the root cut set for the proof phase, so the root remains `M3` and theorem completion is false.

## Commands and results

Commands ran on 2026-07-12 in this worker clone. Existing pinned `.lake` artifacts were used read-only. No update, build, clone, or fetch ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0987/build_obligation_artifacts.py` | 0 | Deterministically wrote 20 obligations and 36 typed edges; emitted the frozen denominator hash |
| `python3 Stage1_Instances/THM-M-0987/check_obligation_tree.py` | 0 | Checked source hashes, required node schema, denominators, graph names and adjacency, reciprocal proof edges, acyclicity/reachability, structured recipes, hygiene, and the open-root boundary |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0987/ObligationTree.lean` | 0 | Conditional exact-root composition elaborated; axiom report contained `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0987` | 0 | Rank 267, planned, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0987 .stage1-worker-selftest.json` | 0 | No whitespace errors |

## Setup attempt retained as evidence

An initial direct elaboration exited 1 because `import Statement` was outside Lake's module roots. A second attempt to emit `Statement.olean` beside the external source also exited 1 due to Lean's root-containment rule. The final scoped check instead imports the same minimal mathlib feature module and repeats the already frozen canonical type in the conditional harness. The structural validator binds this registry to the SHA-256 of `Statement.lean`, preventing that harness from silently substituting the target. These setup failures do not indicate a source elaboration failure and are not hidden.

This phase freezes architecture only. It does not apply the pinned theorem to the canonical root, accept transitive proof-body provenance or trust, establish H0/R0, complete the audit, or complete the theorem. Master acceptance remains required.
