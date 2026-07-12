# Proof execution validation receipt

Item: `S56-M-0464-PROOF`  
Base revision: `6bf36d02b85429a55c272e015740031c598c25bb`

`Proof.lean` supplies seven kernel-checked proof bodies for the frozen set-theoretic,
algebraic-part, monotonicity, and degenerate counting branches. It does not introduce a theorem of
type `PilaWilkieStatement`, and it does not assume any open package from the obligation tree.

## Validation

Commands were run from this worker clone on 2026-07-12. Lean used the existing canonical pinned
artifacts through the pre-existing `Formalizations/Lean/.lake` symlink. No Lake update, build,
fetch, clone, or dependency mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `{ printf '%s\n' 'import Mathlib'; cat ../../Stage1_Instances/THM-M-0464/Statement.lean ../../Stage1_Instances/THM-M-0464/ObligationTree.lean ../../Stage1_Instances/THM-M-0464/Proof.lean; } \| lake env lean /dev/stdin` from `Formalizations/Lean` | 0 | Exact statement, conditional assembly, and all seven new declarations elaborated. Every new `#print axioms` reported exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present. |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0464` | 0 | rank 310; planned; L0/rework-required; theorem incomplete. |
| `python3 -m json.tool Stage1_Instances/THM-M-0464/proof.json >/dev/null` | 0 | Proof execution record is valid JSON. |
| `rg -n '\b(sorry\|admit\|axiom\|sorryAx)\b' Stage1_Instances/THM-M-0464 --glob '*.lean'` | 1 | No prohibited declaration or placeholder token found. |
| `git diff --check -- Stage1_Instances/THM-M-0464 .stage1-worker-selftest.json` | 0 | No whitespace errors before self-test manifest creation. |

## Boundary

The connected positive-dimensional semialgebraic and empty-set branches are genuinely closed, but
the general Pila-Wilkie theorem remains `M3`. The pinned environment has no exact upstream closure,
and `M0464-N-CELL`, `M0464-C-PARAM`, `M0464-L-DETERMINANT`, the general
`M0464-B-ALGEBRAIC`, `M0464-L-INDUCTION`, `M0464-L-COUNT`, and transport work remain open.
Accordingly this receipt supports proof-phase self-test and master review only, not theorem completion.
