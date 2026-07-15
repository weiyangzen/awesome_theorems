# THM-M-0590 proof phase blocked at `4d24384c` (`slot52`)

Item: `S56-M-0590-PROOF`

Recorded: `2026-07-15T17:17:11+08:00`

Base revision: `4d24384c79b14d08717e28f370cc47f13d09d920`

Base tree: `da46ba071a778b32b928f09ef2bcb6ff062ffe15`

## Verdict

`blocked`. No eligible proof body closes the exact frozen Lean target. The
target is the full Brown-Douglas-Fillmore classification of essentially normal
bounded operators on separable infinite-dimensional complex Hilbert spaces by
essential spectrum and the off-spectrum Fredholm-index function.

`THMM0590.root_of_directional_packages` is placeholder-free and checks under
`--trust=0`, but it consumes `ForwardInvariantPackage` and
`BackwardClassificationPackage`. Those parameters are exactly the two missing
directional BDF proofs. The declaration checks final biconditional composition;
it does not inhabit `brownDouglasFillmoreTarget` unconditionally.

Pinned mathlib supplies compact-operator, adjoint, ordinary-spectrum, and
compact-operator Fredholm-alternative support. It has no Calkin-algebra,
general Fredholm-index, essential-spectrum, Atkinson, Busby-extension, or
BDF-classification implementation. In particular,
`Mathlib/Analysis/Normed/Operator/Banach.lean:379` still records general
Fredholm operators as future work. A scoped repository Lean search found no
unconditional body outside this dossier, and the frozen anchor audit retained
no exact immutable compatible Lean 4 candidate. This run used no network and
makes no global nonexistence claim.

No premise, axiom, placeholder, weaker target, changed convention, or moving
dependency was added. The proof item remains `[ ]`; the root remains
`[H1, M4, R3]`. No proof, validation, release, theorem-completion, receipt, or
master-acceptance claim is made. Because the proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Current-Base Delta

The latest preceding packet was integrated at `3af3b6bc` and validated base
`5134bae3`. Its JSON SHA-256 is
`c62accd0630d94e063214450531795555ae4ca574f914b1003e6ff522359fe0f`.
Between that integration and the current base, 146 repository paths changed,
but the complete `THM-M-0590` tree, Lean pin files, target manifest entry, and
selected prerequisite/proof DAG entries did not. A fresh narrow Lean replay at
the current base confirms the same target and conditional composer.

The prerequisite `S56-M-0590-OBLIGATION_TREE` remains provisional `[_]`, not
master-accepted `[x]`. This assignment can therefore produce only provisional
proof-phase evidence; master closure remains dependency ordered.

## Split Required

At base HEAD, 23 integrated proof-recheck JSON records are blocked and
proof-incomplete. The authoritative proof item nevertheless still records
`attempts=0` and `children=[]`. Rev-5.6 section 10.2 requires an item to be split
after five unresolved execution ticks rather than repeatedly assigning the
same oversized root. This worker cannot edit scheduler authority or the
generated checklist. The master must reconcile the cursor and create
dependency-legal children before another proof retry.

Suitable frozen child boundaries are `M0590-S-BOUNDARY`,
`M0590-S-FOUNDATION`, `M0590-N-CALKIN`, `M0590-N-FREDHOLM`,
`M0590-L-FWD-SPECTRUM`, `M0590-L-FWD-INDEX`, `M0590-B-FORWARD`,
`M0590-C-BUSBY`, `M0590-L-EXT-CLASS`, `M0590-L-INDEX-COMPLETE`, and
`M0590-T-BACKWARD`.

## Failed Gate And Retry

The first failed proof gate is terminal proof-body availability for
`M0590-B-FORWARD` and `M0590-T-BACKWARD`; these obligations are the remaining
root cut set. Closing them requires Calkin and Atkinson bridges, forward
invariance of essential spectrum and Fredholm index, Busby extensions, BDF
extension classification, and completeness of the index invariant.

Do not schedule the same root-sized proof item unchanged. Resume a split child
only when its exact placeholder-free Lean body can be implemented, or when a
licensed immutable compatible Lean 4 dependency supplies it and passes
exact-type, provenance, axiom, placeholder, composition, and pinned-replay
checks. A citation or conditional composer does not satisfy this condition.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` link to canonical pinned artifacts was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was performed. Temporary Lean objects were created under `/tmp` and
removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0590` | 0 | Rank 630; lifecycle `planned`; hard-statement-first lane; legacy artifacts unaccepted; theorem incomplete. |
| Initial `git` identity, tree, patch, and status checks | 0 | Base/tree/target tree match this record; tracked patch was empty and only the automation-provided `.lake` link was untracked. |
| `python3 Stage1_Instances/THM-M-0590/check_obligation_tree.py` | 0 | 17 obligations and 37 typed edges passed; denominator `2d5b17d...9a9e8`; root and both directional packages remain open M4. |
| Isolated `lake env lean --trust=0 -t0` replay of `Statement.lean` and `ObligationTree.lean` | 0 | Exact target and conditional composition elaborated; target stdout SHA-256 `0d233828...f14b`, target olean SHA-256 `b4a2a284...a1d9`, composer stdout SHA-256 `05a0a820...03a`, composer olean SHA-256 `d6ed3336...87c`, both stderr streams empty, and composer axioms `[propext, Classical.choice, Quot.sound]`. |
| Owned Lean prohibited-construct scan | 1 (expected) | No `sorry`, `admit`, `sorryAx`, axiom/bodyless declaration, unsafe/oracle, implementation override, or native-decision shortcut was found. |
| Repo-local exact-name Lean search outside this dossier | 1 (expected) | No unconditional root or directional-package body was found. |
| Pinned-mathlib target/API search | 1 (expected) | No BDF target or missing Calkin, Atkinson, general Fredholm-index, essential-spectrum, or Busby API was found. |
| Frozen-registry terminal-body assertion | 0 | Fifteen obligations are machine-required: 14 have no terminal body, and `M0590-T-ASSEMBLE` alone records the conditional composer. |
| Mathlib revision/tree/status check | 0 | Revision `8a178386...eea95`, tree `bdc39a31...f1e5c2b`, clean dependency worktree. |
| Lean/Lake identity and executable hash | 0 | Lean 4.29.0 commit `98dc76e3...fab16740`; Lake `5.0.0-src+98dc76e`; Lean executable SHA-256 `3e0d0d3d...28bbf`. |
| Current-base target/pin/manifest/DAG delta checks | 0 | Target tree, pins, target manifest, and selected DAG entries are unchanged from the latest integrated target evidence. |
| Integrated recheck audit | 0 | All 23 base-HEAD recheck JSON records are blocked and proof-incomplete; authoritative `attempts=0`, `children=[]`; split threshold exceeded. |
| JSON, invariant, self-test-absence, and whitespace checks | 0 | Item/base/tree, hashes, open state, cut set, split requirement, changed paths, deliberate self-test absence, and empty whitespace diagnostics agreed. |

The narrow Lean replay obtained `lean` and `LEAN_PATH` through `lake env`, used
`LEAN_NUM_THREADS=1`, `timeout 600`, `--trust=0`, and `-t0`, wrote both objects
under a new temporary directory, and removed that directory after checking.

Exact hashes and structured results are in the paired JSON artifact. This is
durable current-base blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0590-PROOF`, change scheduler state, or claim M0, audit completion,
theorem completion, validation, release, receipt acceptance, or master
acceptance.
