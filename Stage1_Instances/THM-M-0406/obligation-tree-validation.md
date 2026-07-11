# THM-M-0406 obligation-tree validation

Base revision: `680081e6eeda70901a966224430acff134050176`.

This receipt validates only the frozen denominator, typed graphs, and exact
engine/root interface. It supplies no proof of the engine. No dependency was
fetched, updated, built, or modified.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present. |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0406` | 0 | Rank 19, lifecycle `planned`, baseline L0, legacy artifacts unaccepted, `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-0406/build_obligation_artifacts.py` | 0 | Reproducibly wrote 14 obligations and 26 typed edges; denominator `46deb9e278a5e0383923334b032877af6743372ba6cafa2fd0d03a569d1d90a7`. |
| `python3 Stage1_Instances/THM-M-0406/check_obligation_tree.py` | 0 | Required fields, counts, denominator, reciprocal adjacency, acyclicity, reachability, budgets, open debts, and forbidden-token checks passed; root remains `M4`. |
| `lake env lean -R ../../Stage1_Instances/THM-M-0406 -o /tmp/Statement.olean ../../Stage1_Instances/THM-M-0406/Statement.lean` from `Formalizations/Lean` | 0 | The canonical proposition elaborated and only the temporary import artifact was written. |
| `LEAN_PATH=/tmp lake env lean ../../Stage1_Instances/THM-M-0406/ObligationTree.lean` from `Formalizations/Lean` | 0 | Checked the exact conclusion, engine, and both transport directions; `#print axioms` reported the pinned mathlib foundation axioms `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 -m json.tool Stage1_Instances/THM-M-0406/obligation-registry.json >/dev/null` | 0 | Valid JSON. |
| `python3 -m json.tool Stage1_Instances/THM-M-0406/typed-graphs.json >/dev/null` | 0 | Valid JSON. |
| `! rg -n '[[:blank:]]+$' Stage1_Instances/THM-M-0406/{ObligationTree.lean,build_obligation_artifacts.py,check_obligation_tree.py,obligation-registry.json,obligation-tree.md,obligation-tree-validation.md,typed-graphs.json} .stage1-worker-selftest.json` | 0 | No trailing whitespace in the changed artifacts. |

The source file lies outside the Lake package root, so narrow replay creates
`/tmp/Statement.olean` with Lean's `-R` option and exposes only `/tmp` through
`LEAN_PATH`. The existing pinned `.lake` tree was not changed.

The checked adapter has one explicit open premise, `SurfaceDegeneracyEngine`.
The auxiliary-section construction, height argument, quantitative Subspace
Theorem, exceptional-locus descent, proof bodies, H0 review, provenance, trust,
independent validation, and release gates all remain open. This handoff
proposes only `[_]` for this obligation-tree item, pending master acceptance.
