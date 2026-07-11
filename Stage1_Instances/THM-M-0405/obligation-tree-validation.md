# THM-M-0405 obligation-tree validation

Base revision: `a32d1624313faffb33c6333bbed8bf8926cf6f70`.

This receipt validates only the frozen obligation denominator, typed graphs,
and exact conjunction interface. It does not prove either BHV branch. No
dependency was fetched, updated, built, or otherwise modified.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present. |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0405` | 0 | Rank 18, lifecycle `planned`, baseline L0, legacy artifacts unaccepted, `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-0405/build_obligation_artifacts.py` | 0 | Reproducibly wrote 15 obligations and 30 typed edges; denominator `cd9daee4b82734d1e98e216a6371bd83f3fcff1a181e79381773133a6b9da793`. |
| `python3 Stage1_Instances/THM-M-0405/check_obligation_tree.py` | 0 | All required fields, denominator, endpoints, reciprocal adjacency, root reachability, budgets, open debts, and forbidden-token checks passed; root remained `M4`. |
| `lake env lean -R ../../Stage1_Instances/THM-M-0405 -o /tmp/Statement.olean ../../Stage1_Instances/THM-M-0405/Statement.lean` from `Formalizations/Lean` | 0 | Printed `Stage1.THM_M_0405.Statement : Prop` and produced only the temporary import artifact. |
| `LEAN_PATH=/tmp lake env lean ../../Stage1_Instances/THM-M-0405/ObligationTree.lean` from `Formalizations/Lean` | 0 | Checked the branch definitions, both root projections, and `statement_of_branches`; `#print axioms` reported the pinned mathlib foundation axioms `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 -m json.tool Stage1_Instances/THM-M-0405/obligation-registry.json >/dev/null` | 0 | Valid JSON. |
| `python3 -m json.tool Stage1_Instances/THM-M-0405/typed-graphs.json >/dev/null` | 0 | Valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0405 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The local source file is outside the Lake package root, so the narrow replay
first writes `/tmp/Statement.olean` with Lean's `-R` option and then exposes
only `/tmp` through `LEAN_PATH`. This neither writes to nor repairs `.lake`.

The checked composition theorem has two explicit open premises. It therefore
does not close `M0405-C-ROOT-COMPOSITION`, either branch, or the root. The
central BHV formalization, source crosswalk review, proof bodies, provenance,
trust closure, audit completion, independent validation, and theorem release
all remain outstanding. This handoff proposes only `[_]` for the assigned
obligation-tree item, pending master acceptance.
