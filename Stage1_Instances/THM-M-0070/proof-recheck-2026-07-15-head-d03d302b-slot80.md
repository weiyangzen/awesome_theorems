# THM-M-0070 proof-phase recheck at `d03d302b` (slot80)

Item: `S56-M-0070-PROOF`

Intent: `prove`

Validated on: `2026-07-15` (`Asia/Shanghai`)

Base revision: `d03d302bba800ecaf216835c488381f045efbbfe`

Base tree: `8c7b74f4ffba9a954a510096902571e859629811`

## Verdict

`blocked`. The exact frozen proposition is the full Feit-Thompson odd-order theorem:

```text
forall (G : Type u) [Group G] [Finite G],
  Odd (Nat.card G) -> IsSolvable G
```

No placeholder-free Lean term inhabits this proposition in the repository or pinned dependency
closure. The first failed gate is `M0070-X-LEAN-BODY`.
`Stage1Instances.THM_M_0070.ObligationTree.TranslatedOddOrderBody` is definitionally the exact
canonical target. The checked adapter and terminal declarations merely consume that open
proposition; none constructs it. Adding another conditional wrapper would conceal rather than
resolve the required proof.

Pinned mathlib provides solvability definitions, closure lemmas, and strict commutative,
nilpotent, and Z-group special cases, but no theorem deriving solvability from finite odd order.
A bounded source search found no endpoint. The exact external Lean declaration
`ianklatzco/odd-order-lean@0f4a5dae...:odd_order_solvable` ends in `by sorry` and uses incompatible
Lean/mathlib pins, so it is ineligible. The complete
`math-comp/odd-order@6afa795b...:Feit_Thompson` proof is a Coq/Rocq kernel object; no approved
semantics-preserving Lean bridge or repo-local cross-kernel validation closure exists.

No proof body, axiom, placeholder, unsafe declaration, weakened statement, substituted theorem,
or dependency was added. No obligation receives closure credit. The root remains
`[H1, M3, R4]`, and this proof item remains `[ ]`. Because the assigned phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The immediate proof cut is `M0070-X-LEAN-BODY`. The broader frozen root cut also retains
`M0070-X-SOURCE`, `M0070-S-FOUNDATION`, `M0070-X-PROVENANCE`, `M0070-X-TRUST`,
`M0070-X-LICENSE`, `M0070-X-READABLE`, and `M0070-X-WORKFLOW`. The architecture contains 51 open
logical-decomposition nodes, 2,084 exact MathComp source-declaration obligations, and 229 bounded
source-body chunks. That inventory is a translation plan, not Lean proof evidence.

Proof work can resume only when a local placeholder-free Lean translation, or an immutable
compatible Lean proof in an approved pinned dependency closure, inhabits the unchanged
`TranslatedOddOrderBody`. The body must then pass exact-type, terminal provenance, axiom/TCB,
placeholder, dependency, and child-to-parent composition checks before proof-phase credit.

The prerequisite `S56-M-0070-OBLIGATION_TREE` is provisional `[_]`, not master-accepted, so
positive proof acceptance is independently unavailable. The authoritative proof item remains
`[ ]` with zero recorded attempts and no children. This recheck records the current base without
inferring progress from repeated unchanged-root searches.

## Narrow Validation

All checks ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network operation, or `.lake` mutation was performed. This is warm, dirty,
nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0070` | 0 | Rank 1101; lifecycle `planned`; lane `hard_statement_first_partial_verification`; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| Temporary `lake env lean --trust=0 -t0` replay of `Statement.lean`, followed by `ObligationTree.lean` with a temporary `Statement.olean` | 0 | Both modules elaborated under Lean 4.29.0. `TranslatedOddOrderBody` printed as the exact target; all four conditional declarations reported only `propext`, `Classical.choice`, and `Quot.sound`. Statement output SHA-256 `395d768d...fade5`; obligation output `a5972c2a...1b1f3`. |
| Bounded exact-topic search over repo-local Lean and pinned package source | 1 | Expected no-match exit: no Feit-Thompson or odd-order-solvability root endpoint exists in that checked source surface. |
| Scoped prohibited-device scan over owned Lean files | 1 | Expected no-match exit: no `sorry`, `admit`, bodyless axiom/constant, unsafe/opaque/extern body, external implementation, native oracle, or `proof_wanted` occurs. |
| `git -C Formalizations/Lean/.lake/packages/{mathlib,flt-regular} rev-parse HEAD HEAD^{tree}` plus clean-status checks | 0 | Mathlib is pinned at `8a178386...ea95` / tree `bdc39a31...c2b`; flt-regular is pinned at `56161b6e...1a27` / tree `32c9eace...c893`; both worktrees were clean. |
| `env LEAN_NUM_THREADS=1 timeout --foreground 420 python3 -B Stage1_Instances/THM-M-0070/check_obligation_tree.py` | 1 | The validator elaborated its Lean checks, then failed its final artifact-inventory equality: eight integrated prior proof-recheck files exist but are absent from `instance.json:owned_artifacts`. This prerequisite drift supplies no proof evidence; this proof worker did not rewrite the prerequisite manifest. |
| `python3 -B Stage1_Instances/THM-M-0070/check_statement.py` | 1 | It completed elaboration and reported `instance owned-artifact inventory is stale` for the same integrated evidence files. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker-completion packet. |
| Blocker invariant/source-hash check, JSON parse, and whitespace checks | 0 | Base/tree, exact target, `[ ]` state, unchanged vector, empty closure lists, false completion flags, recorded source hashes, self-test absence, JSON syntax, newlines, and whitespace passed. |

The direct Lean replay used pinned Lean commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, executable SHA-256
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`, trust level zero, and only
temporary output removed after checking. Exact input hashes, the full cut set, command results,
candidate classifications, known failures, and retry conditions are recorded in the companion
JSON artifact.

This is current-base durable blocker evidence. It does not satisfy `S56-M-0070-PROOF`, propose a
state transition, close any obligation or the root, or claim audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance.
