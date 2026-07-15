# THM-M-0070 proof-phase recheck at e90521b4 (slot68)

Item: `S56-M-0070-PROOF`

Intent: `prove`

Base revision: `e90521b4b150b98d81c4dca2462ad36b64d4673e`

Base tree: `f12951f481d2b51f33d6d300dc2874b3c49ed0e0`

Recheck time: `2026-07-15T13:41:55+08:00` (Asia/Shanghai)

## Verdict

`blocked`. The exact frozen proposition is the full Feit-Thompson odd-order theorem:

```text
forall (G : Type u) [Group G] [Finite G],
  Odd (Nat.card G) -> IsSolvable G
```

No placeholder-free Lean term inhabits that proposition in the repository or pinned dependency
closure. The first failed gate is `M0070-X-LEAN-BODY`, whose formal target
`Stage1Instances.THM_M_0070.ObligationTree.TranslatedOddOrderBody` is definitionally the exact
canonical target. The existing adapter and terminal declarations consume that open proposition;
they do not construct it. Adding another conditional wrapper would therefore hide, rather than
solve, the required proof.

Pinned mathlib supplies solvability definitions, closure lemmas, and strict commutative,
nilpotent, and Z-group special cases, but no theorem deriving solvability from finite odd order. A
bounded exact-topic search found no root declaration. The exact external Lean declaration
`ianklatzco/odd-order-lean@0f4a5dae...:odd_order_solvable` ends in `by sorry` and uses incompatible
Lean/mathlib pins, so importing or wrapping it would introduce `sorryAx`. The complete
`math-comp/odd-order@6afa795b...:Feit_Thompson` proof is a Coq/Rocq kernel object. There is no
approved semantics-preserving bridge from that object to the frozen Lean target, no local Coq
replay receipt, and no transitive cross-kernel trust closure.

No proof body, axiom, placeholder, unsafe declaration, weakened statement, substituted theorem,
or dependency was added. No obligation receives closure credit. The root remains
`[H1, M3, R4]`, and the proof item remains `[ ]`. Because the assigned proof phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate

The immediate proof cut is `M0070-X-LEAN-BODY`. The broader frozen root cut also retains source,
foundation, provenance, trust, license, readability, and workflow obligations. The architecture
still contains 51 open logical-decomposition nodes, 2,084 exact source-declaration obligations,
and 229 bounded source-body chunks requiring semantics-preserving Lean translation and checked
composition. Their inventory is proof planning, not proof evidence.

Proof work can resume only after a local placeholder-free Lean translation, or an immutable
compatible Lean proof already in an approved pinned closure, inhabits the unchanged translated-body
type. That body must then pass exact-type, terminal provenance, axiom/TCB, placeholder, dependency,
and child-to-parent composition checks before any proof-phase state change.

## Narrow Validation

All checks ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network operation, or `.lake` mutation occurred. This is warm, dirty, nonrelease
evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0070` | 0 | Rank 1101; lifecycle `planned`; lane `hard_statement_first_partial_verification`; uniform L0/rework-required baseline; legacy artifacts unaccepted; theorem incomplete. |
| Isolated direct pinned-Lean replay of temporary `Statement.lean` and `ObligationTree.lean` copies with `LEAN_NUM_THREADS=1`, `--trust=0`, `-t0`, and existing package olean paths excluding `flt-regular` | 0 | Both modules elaborated. `TranslatedOddOrderBody` printed as the exact target; all four conditional declarations reported only `[propext, Classical.choice, Quot.sound]`. Statement olean SHA-256 `932a7674...e71df`; obligation olean `922a499a...a4cb4`; statement output `395d768d...fade5`; obligation output `a5972c2a...1b1f3`. |
| Bounded repo-local and pinned-mathlib exact-topic search | 1 | Expected no-match exit: no Feit-Thompson or odd-order-solvability root endpoint exists in the checked source surface. |
| Scoped prohibited-device scan over all owned Lean files | 1 | Expected no-match exit: no `sorry`, `admit`, bodyless axiom/constant, unsafe/opaque/extern body, external implementation, native oracle, or `proof_wanted` occurs. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and clean-status check | 0 | Pinned mathlib revision `8a178386...ea95`, tree `bdc39a31...c2b`; the worktree was clean. |
| `timeout --foreground 600 python3 -B Stage1_Instances/THM-M-0070/check_obligation_tree.py` | 124 | The prerequisite validator reached its root `lake env` call but timed out after 600 seconds because the shared `flt-regular` package checkout had no valid `HEAD`. No dependency repair or fetch was attempted; the two relevant Lean modules were replayed directly as recorded above. |
| Blocker JSON invariant/source-hash check, `python3 -m json.tool`, and new-file whitespace checks | 0 | Base, target, `[ ]` state, unchanged vector, empty closure lists, false completion flags, source hashes, absent root self-test manifest, newline policy, and both blocker files passed. |

The direct replay used the pinned Lean executable at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740` with SHA-256
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`. It built temporary copies
against the existing package `lib/lean` paths, excluding the unrelated invalid `flt-regular`
metadata checkout, then removed every temporary artifact. Pinned mathlib remained at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

Exact source hashes, the full command/result ledger, the frozen cut set, candidate classifications,
known failures, and the retry condition are recorded in the adjacent JSON artifact. This is a
proof-phase blocker record, not a proof or acceptance receipt.
