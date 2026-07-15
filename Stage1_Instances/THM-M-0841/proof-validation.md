# THM-M-0841 proof-phase validation

Item: `S56-M-0841-PROOF`. Base revision
`aef94f39853f9222e48f83b2358a6822aafd3c50` (tree
`8c42e198fdbcc36b0f5cc0f865e0961715a35c17`).

## Implemented proof

`Proof.lean` supplies a local placeholder-free inhabitant of the exact frozen
`SparseFromDense` interface. It proves the finite complement identity

```text
#(Gᶜ).edgeFinset = n.choose 2 - #G.edgeFinset
```

and normalizes the real cast of `n.choose 2`. Given the frozen dense family, it applies that
family with tolerance `epsilon / 2` and chooses a threshold above `1 / epsilon`. The linear
`n / 2` difference between `n.choose 2` and `n^2 / 2` is then absorbed by the half-epsilon
slack. The original epsilon/r/n/graph/k binders, iterated-log lower bound, and complement
containment are unchanged.

This supplies exact direct-body evidence for `M0841-S-COMPLEMENT-TRANSPORT`. The two helper
theorems are not separately frozen obligations. Canonical closure is deliberately withheld:
the frozen graph makes this transport a nonleaf with open `logical_decomposition` children
`M0841-N-DENSE-FORM` and `M0841-N-THRESHOLD-PACKAGE`, and no exact child-to-parent certificate
currently consumes them. The dense-family and root declarations likewise retain `DenseBase` and
`DenseStep` as explicit premises and receive conditional-composition evidence only.

## Commands and results

Validation ran on 2026-07-15 (`Asia/Shanghai`) using the automation-provided canonical pinned
`.lake` symlink read-only. No `lake update`, `lake build`, dependency clone/fetch, checkout, or
`.lake` mutation ran.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0841` | 0 | Rank 1398, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete. |
| `python3 -B Stage1_Instances/THM-M-0841/check_proof.py` | 0 | Isolated `Statement -> ObligationTree -> Proof` elaboration with `--trust=0`; the exact transport body, two helpers, and two conditional composers are sorry-free and each reports only `propext`, `Classical.choice`, and `Quot.sound`; hashes, pin, graph-closure boundary, receipt, blocker, worker packet, and open root pass. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e3...6740`; Lake 5.0.0-src+98dc76e. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Revision `8a178386...ea95`; tree `bdc39a31...c2b`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | Empty output; pinned mathlib worktree clean. |
| `rg -n '\b(sorry\|admit\|sorryAx\|axiom\|constant\|unsafe\|implemented_by\|native_decide\|extern\|opaque\|run_tac)\b' Stage1_Instances/THM-M-0841/Proof.lean` | 1 | Expected no-match exit; no prohibited proof escape occurs outside comments. The proof checker repeats a comment-stripped scan. |
| `python3 -m json.tool` on the receipt, blocker, and worker packet | 0 | All structured artifacts parse. |
| `python3 -m py_compile` was not used | n/a | The checker is syntax-checked with Python `ast.parse` without writing bytecode. |
| `git diff --check -- Stage1_Instances/THM-M-0841 .stage1-worker-selftest.json` | 0 | No tracked whitespace diagnostics; per-file no-index checks cover untracked artifacts. |

## Status boundary

The frozen-graph root cut remains `M0841-S-COMPLEMENT-TRANSPORT`, `M0841-B-R-TWO`, and
`M0841-B-R-GE-THREE`. The direct body discharges the transport as a Lean premise, so the optimistic
formal-premise cut is the latter two branches; it does not override the frozen graph's closure
contract. Their descendants still require the intersection engine, high-degree base,
admissible-tolerance split, repeated block deletion, asymptotic estimates, and limiting
contradiction. The pinned closure contains no exact growing-part Erdos-Stone terminal theorem.

This is provisional exact-body evidence. Because no canonical graph obligation closes, both the
proposed and authoritative accepted root vectors remain `H1/M3/R4` with no accepted proof
obligations.
Validation, release, H0, R0, full transitive trust/provenance closure, hermetic replay,
independent verification, and deterministic release evidence remain open. Neither audit
completion nor theorem completion is claimed.
