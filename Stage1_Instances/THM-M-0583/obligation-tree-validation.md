# THM-M-0583 obligation-tree validation

Base revision: `6894f3df8b6434b7b3ef2668d8395476b30b3d48`.

This receipt covers only the frozen obligation registry, seven typed graph
kinds, semantic ledgers, and the exact logical adapter. It gives no proof
credit to the open four-dimensional topology obligations and does not claim
theorem completion. No dependency was fetched, updated, built, or modified.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0583` | 0 | Rank 116, lifecycle `planned`, baseline L0/rework required, legacy artifacts unaccepted, `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-0583/build_obligation_artifacts.py` | 0 | Wrote 16 obligations and 32 typed edges; denominator `910aad119639e1751b6f8c0ad6d04f98a030acdc0e00c951cd46f6efff18cccd`. |
| `python3 Stage1_Instances/THM-M-0583/check_obligation_tree.py` | 0 | Verified unique obligations, the frozen denominator, seven graph kinds, reciprocal adjacency, semantic budgets, required proof reachability, open debts, and forbidden tokens; root remains M2. |
| `lake env lean ../../Stage1_Instances/THM-M-0583/ObligationTree.lean` from `Formalizations/Lean` | 0 | Checked the terminal-core proposition, definitional equivalence, and exact root adapter; `#print axioms` reported `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 -m json.tool Stage1_Instances/THM-M-0583/obligation-registry.json >/dev/null` | 0 | Valid JSON. |
| `python3 -m json.tool Stage1_Instances/THM-M-0583/typed-graphs.json >/dev/null` | 0 | Valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0583 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The registry was serialized before the previously audited M2 status was
attached. All 16 nodes are root-relevant and machine-required; none is closed.
The architecture conservatively exposes the source crosswalk, encoding,
homotopy-data reduction, topological model, disk embedding, surgery,
s-cobordism, homeomorphism construction, terminal body, adapter, composition,
provenance, trust, readable reconstruction, and validation boundaries.

Primary-source review may show that this conservative architecture must
change. Such a finding invalidates registry v1 and requires a new append-only
version; it must not silently alter this denominator. The exact Lean adapter
only proves that a future implementation of the full terminal core has the
canonical type. The terminal core, H0 crosswalk, proof bodies, provenance,
trust closure, R0 reconstruction, hermetic validation, and release all remain
open. This handoff proposes `[_]` only for the assigned obligation-tree item,
pending master acceptance.
