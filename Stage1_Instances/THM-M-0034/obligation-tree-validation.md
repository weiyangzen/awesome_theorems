# THM-M-0034 obligation-tree validation

Item: `S56-M-0034-OBLIGATION_TREE`

Base revision: `2bfb272c83b2089e9b285d48dce2c30616ff6c36`

Base tree: `f44853226ddecdf2a2b462fd6c85e770bbffbaa3`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

The frozen registry contains 41 unique semantic obligations and has denominator SHA-256
`0f1fd6b2f8450f934acd51372109d93d3b86bfc9ecaac8fe0f58bc566d7fb090`. The graph bundle contains
57 directed edges across proof, refinement, provenance, evidence, trust, documentation, and
workflow graphs. All proof requirements have reciprocal composition edges. External-body
decomposition is deliberately expository because no local composition certificate or kernel replay
exists for that source. It does not affect machine closure or receive proof credit.

The local Lean check re-elaborated the exact statement and checked the all-natural-number field
candidate transport, the stronger PID-candidate specialization, and conditional root composition.
The three declarations report `[propext, Classical.choice, Quot.sound]`. The candidate theorem is
an explicit premise; no external source is imported and no root proof is claimed.

## Commands and exact outcomes

All commands ran from the repository root unless a different working directory is shown.

| Command | Exit | Exact outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0034` | 0 | rank 1078, planned, `L0/rework_required`, theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-0034/build_obligation_artifacts.py` | 0 | deterministically wrote 41 obligations, 57 typed edges, and denominator `0f1fd6b2...b090` |
| `python3 -B Stage1_Instances/THM-M-0034/check_obligation_tree.py` | 0 | registry, denominator, node schemas, seven graphs, reciprocity, acyclicity, reachability, validation recipes, candidate pins, receipt, public ledger, exact open boundary, and hygiene passed |
| `lake env lean --root=../.. ../../Stage1_Instances/THM-M-0034/Statement.lean -o /tmp/stage1-thm-m-0034-obligation-lean/Statement.olean`; then `LEAN_PATH=/tmp/stage1-thm-m-0034-obligation-lean:<pinned lake env LEAN_PATH> lake env lean --root=../.. ../../Stage1_Instances/THM-M-0034/ObligationTree.lean` from `Formalizations/Lean` | 0 each | exact statement and five conditional composition declarations elaborated; axiom output `[propext, Classical.choice, Quot.sound]`; obligation output SHA-256 `e866cce9...c353` |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0034-obligation-pycache python3 -m py_compile Stage1_Instances/THM-M-0034/build_obligation_artifacts.py Stage1_Instances/THM-M-0034/check_obligation_tree.py` | 0 | generator and validator compiled outside the repository tree |
| `python3 -m json.tool` over the obligation JSON files and `.stage1-worker-selftest.json` | 0 | all structured artifacts parsed |
| scoped prohibited-token scan of `ObligationTree.lean` | 1 | expected no match: no proof escape, bodyless axiom, unsafe/opaque declaration, oracle, or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0034 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

The pre-existing automation-provided `Formalizations/Lean/.lake` link was used read-only. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was run.

## Status boundary

This self-test covers only the obligation-tree phase. The selected candidate remains an `E3/M3`
external source anchor outside the dependency closure. Its license, immutable local integration,
kernel and axiom replay, exact wrapper, complete transitive declaration provenance, trust closure,
and every external-body composition certificate remain open. Human-source H0, independently
reviewed R0, proof acceptance, hermetic replay, independent verification, validation, release,
`AUDIT-Z`, theorem completion, and master acceptance are not claimed.
