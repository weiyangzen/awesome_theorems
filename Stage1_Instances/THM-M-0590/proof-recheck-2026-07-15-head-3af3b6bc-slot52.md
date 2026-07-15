# THM-M-0590 proof phase blocked at `3af3b6bc`

Item: `S56-M-0590-PROOF`

Recorded: `2026-07-15T16:55:10+08:00`

Base revision: `3af3b6bc58d308bda7dc1cb164a9a258512b8c53`

Base tree: `65dce2e2ba00c806bf25b436c98caf996c1c56d2`

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
general Fredholm-index, essential-spectrum, Busby-extension, or
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

## Workflow Boundary

The prerequisite `S56-M-0590-OBLIGATION_TREE` remains provisional `[_]`, not
master-accepted `[x]`. This assignment can therefore produce only provisional
current-base blocker evidence; master closure remains dependency ordered.

Twenty-three integrated unresolved proof-recheck JSON records existed before
this run, while the authoritative proof item still records `attempts=0` and
`children=[]`. Rev-5.6 section 10.2 requires a split after five unresolved
execution ticks rather than another root-sized retry. This worker cannot edit
the authoritative DAG or generated checklist. The master must reconcile that
cursor and create dependency-legal child tasks.

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
| Initial `git status`, base/tree, patch hash, and `.lake` link checks | 0 | Tracked patch empty; only the automation-provided `.lake` link untracked; base/tree match this record. |
| `python3 Stage1_Instances/THM-M-0590/check_obligation_tree.py` | 0 | 17 obligations and 37 typed edges passed; denominator `2d5b17d...9a9e8`; root and both directional packages remain open M4. |
| Isolated `lake env lean --trust=0 -t0` replay of `Statement.lean` and `ObligationTree.lean` | 0 | Exact target and conditional composition elaborated; target stdout SHA-256 `0d233828...f14b`, composer stdout SHA-256 `05a0a820...03a`, and composer axioms `[propext, Classical.choice, Quot.sound]`. |
| Owned Lean prohibited-construct scan | 1 (expected) | No `sorry`, `admit`, `sorryAx`, axiom/bodyless declaration, unsafe/oracle, implementation override, or native-decision shortcut was found. |
| Repo-local exact-name Lean search outside this dossier | 1 (expected) | No unconditional root or directional-package body was found. |
| Pinned-mathlib target/API search | 1 (expected) | No BDF target or missing Calkin, general Fredholm-index, essential-spectrum, Busby, or Atkinson API was found. |
| Frozen-registry terminal-body assertion | 0 | Fifteen obligations are machine-required: 14 have no terminal body, and `M0590-T-ASSEMBLE` alone records the conditional composer. |
| Mathlib revision/tree/status check | 0 | Revision `8a178386...e95`, tree `bdc39a31...e2b`, clean dependency worktree. |
| Lean/Lake identity and executable hash | 0 | Lean 4.29.0 commit `98dc76e...740`, Lake `5.0.0-src+98dc76e`, executable SHA-256 `3e0d0d3d...28bbf`. |
| Prior recheck count plus DAG state inspection | 0 | Twenty-three prior integrated JSON records; authoritative proof item remains `[ ]`, `attempts=0`, `children=[]`; split threshold exceeded. |
| Current-base JSON parse, invariants, and whitespace checks | 0 | Item/base, hashes, denominator, workflow states, open cut set, empty bodies/receipts, split trigger, changed paths, self-test absence, and whitespace agreed. |

The exact narrow Lean replay was:

```bash
TMP=$(mktemp -d /tmp/thm-m-0590-proof-3af3b6bc-slot52.XXXXXX)
LEAN=$(cd Formalizations/Lean && lake env which lean)
LP=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
(cd Stage1_Instances/THM-M-0590 &&
  LEAN_NUM_THREADS=1 LEAN_PATH="$LP" timeout 600 "$LEAN" --trust=0 -t0 \
    -o "$TMP/Statement.olean" Statement.lean)
(cd Stage1_Instances/THM-M-0590 &&
  LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LP" timeout 600 "$LEAN" --trust=0 -t0 \
    -o "$TMP/ObligationTree.olean" ObligationTree.lean)
rm -rf "$TMP"
```

Exact hashes, structured results, the open cut set, and the required scheduler
split are recorded in the paired JSON artifact. This is durable current-base
blocker evidence, not a proof receipt.
