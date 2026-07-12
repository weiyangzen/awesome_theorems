# Statement validation receipt

Item: `S56-M-0320-STATEMENT`  
Base revision: `609cbc7bf1cbe295038cefb806fb3d4ce8ffa529`

The target and four mutations elaborated against the existing pinned Lean environment. No `.lake`
update, build, clone, or fetch was performed.

| Command | Exact result |
|---|---|
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0320/Statement.lean)` | exit 0; canonical declaration printed; no warnings or errors |
| import trial with only `Mathlib.Topology.Semicontinuity.Hemicontinuity` | exit 1; `EuclideanSpace` and `Convex` unknown |
| import trial with the two imports in `Statement.lean` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0320/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0320/task-dag.json` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-0320 .stage1-worker-selftest.json` | exit 0; no output |

Source acceptance, anchor audit, obligation tree, proof, validation, and release remain open. This
supports statement worker self-test only, not master acceptance or theorem completion.
