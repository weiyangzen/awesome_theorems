# THM-M-0070 proof-phase recheck at `4d389eb4` (slot55)

Item: `S56-M-0070-PROOF`

Intent: `prove`

Validated at: `2026-07-15T17:09:32+08:00` (`Asia/Shanghai`)

Base revision: `4d389eb47e043f6f44925a418baee0d034f764ba`

Base tree: `64faabd76665273032b8cb1554b90655b5c94256`

## Verdict

`blocked`. The unchanged frozen target is the full Feit-Thompson odd order theorem:

```text
forall (G : Type u) [Group G] [Finite G],
  Odd (Nat.card G) -> IsSolvable G
```

No placeholder-free Lean term inhabits this proposition in the repository or pinned dependency
closure. The first failed gate is `M0070-X-LEAN-BODY`.
`Stage1Instances.THM_M_0070.ObligationTree.TranslatedOddOrderBody` is definitionally the exact
canonical target. The checked adapter and terminal declarations consume that open proposition;
none constructs it. The 51 smaller architecture packages currently have only structured
JSON/Markdown obligations, not dependency-legal Lean proposition interfaces. Adding another
conditional wrapper would hide rather than resolve the proof debt.

Pinned mathlib supplies solvability interfaces and strict commutative, nilpotent, and Z-group
special cases, but no theorem deriving solvability from finite odd order. A bounded exact-topic
search again found no endpoint. The exact external Lean declaration
`ianklatzco/odd-order-lean@0f4a5dae...:odd_order_solvable` ends in `by sorry` and has incompatible
Lean/mathlib pins, so it is ineligible. The complete
`math-comp/odd-order@6afa795b...:PFsection14.Feit_Thompson` proof is a Coq/Rocq object; no approved
semantics-preserving Lean bridge or repo-local cross-kernel validation closure exists.

No proof body, axiom, placeholder, unsafe declaration, weakened statement, substituted theorem,
or dependency was added. No obligation receives closure credit. The root stays `[H1, M3, R4]`,
and this proof item stays `[ ]`. Because the phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Mandatory Split Handoff

The immediate proof cut is `M0070-X-LEAN-BODY`. The broader frozen root cut also retains
`M0070-X-SOURCE`, `M0070-S-FOUNDATION`, `M0070-X-PROVENANCE`, `M0070-X-TRUST`,
`M0070-X-LICENSE`, `M0070-X-READABLE`, and `M0070-X-WORKFLOW`. The architecture contains 51 open
logical-decomposition nodes, 2,084 exact MathComp source-declaration obligations, and 229 bounded
source-body chunks. That inventory is a translation plan, not Lean proof evidence.

Eight prior proof-recheck pairs already record the same blocker. This is the ninth target-scoped
proof recheck. Section 10.2 of the rev-5.6 standard requires splitting after five unresolved
execution ticks rather than assigning the same oversized item again. The integration lane must
split `S56-M-0070-PROOF` into dependency-legal child nodes, first adding exact Lean interfaces for
the frozen architecture/source packages where required, while retaining `M0070-X-LEAN-BODY` as the
terminal integration gate. This worker cannot edit the authoritative DAG or generated blueprint
and does not invent scheduler children.

Positive proof work can resume only on bounded child nodes with typed Lean interfaces, or when an
immutable compatible placeholder-free Lean body inhabits the unchanged `TranslatedOddOrderBody`.
Any body must pass exact-type, terminal provenance, axiom/TCB, placeholder, dependency, and
child-to-parent composition checks. The prerequisite `S56-M-0070-OBLIGATION_TREE` remains
provisional `[_]`, not master accepted. Its owned-artifact inventory is stale because the sixteen
integrated prior proof-recheck files are not listed in `instance.json`; this proof worker did not
rewrite prerequisite authority.

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
| Bounded exact-topic search over repo-local Lean and pinned package source | 1 | Expected no-match exit: no Feit-Thompson or odd-order-solvability root endpoint exists in the checked source surface; output was empty. |
| Scoped prohibited-device scan over owned Lean files | 1 | Expected no-match exit: no `sorry`, `admit`, bodyless axiom/constant, unsafe/opaque/extern body, external implementation, native oracle, or `proof_wanted` occurs; output was empty. |
| Pin/tree/clean checks for pinned mathlib and `flt-regular`, plus Lean/Lake version checks | 0 | Mathlib is `8a178386...ea95` / tree `bdc39a31...c2b`; `flt-regular` is `56161b6e...1a27` / tree `32c9eace...c893`; both worktrees were tracked-clean; Lean 4.29.0 and Lake 5.0.0 were used. |
| `env LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 420 python3 -B Stage1_Instances/THM-M-0070/check_obligation_tree.py` | 1 | The validator elaborated its Lean checks, then failed the final artifact-inventory equality: sixteen integrated proof-recheck files are absent from `instance.json:owned_artifacts`. This prerequisite drift supplies no proof evidence. |
| `python3 -B Stage1_Instances/THM-M-0070/check_statement.py` | 1 | It completed elaboration and reported the same stale instance inventory. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker-completion packet. |
| Blocker invariant/source-hash check, JSON parse, newline and whitespace checks | 0 | Base/tree, exact target, `[ ]` state, unchanged vector, empty closure lists, false completion flags, source hashes, ninth-recheck split trigger, self-test absence, JSON syntax, newline policy, and whitespace passed. |

The direct Lean replay used pinned Lean commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, executable SHA-256
`3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`, trust level zero, and only
temporary output removed after checking. Exact input hashes, the full cut set, command results,
candidate classifications, known failures, and retry conditions are in the companion JSON.

This is current-base durable blocker evidence. It does not satisfy `S56-M-0070-PROOF`, propose a
state transition, close any obligation or the root, or claim audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance.
