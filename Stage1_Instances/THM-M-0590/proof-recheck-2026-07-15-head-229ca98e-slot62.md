# THM-M-0590 proof phase blocked at `229ca98e` (`slot62`)

Item: `S56-M-0590-PROOF`

Recorded: `2026-07-15T14:28:27+08:00`

Base revision: `229ca98e7478d389ccf8de8173c94e0e7c8fe670`

Base tree: `d3cc9562940b923aebbe7e01ce66232079760b3b`

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
compact-operator Fredholm-alternative support. Its Banach operator source still
records a TODO for general Fredholm operators. The bounded source search found
no Calkin-algebra, general Fredholm-index, essential-spectrum, Busby-extension,
or BDF-classification implementation. A scoped repo-local Lean search likewise
found no unconditional body outside this dossier. The prior immutable anchor
audit retained no exact compatible external Lean 4 candidate. This run used no
network and makes no global nonexistence claim.

No premise, axiom, placeholder, weaker target, changed convention, or moving
dependency was added. The proof item remains `[ ]`; the root remains
`[H1, M4, R3]`. No proof, validation, release, theorem-completion, receipt, or
master-acceptance claim is made. Because the proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Split Required

Sixteen integrated unresolved proof-recheck pairs existed before this run, so
this is the seventeenth root-sized recheck. The authoritative DAG still records
`attempts=0` and `children=[]`. Rev-5.6 section 10.2 requires a split after five
unresolved execution ticks rather than another root-sized assignment. This
worker cannot edit scheduler authority or the generated checklist, so the
master must reconcile the cursor and create dependency-legal child tasks before
another proof retry.

The frozen architecture identifies suitable child boundaries:
`M0590-S-BOUNDARY`, `M0590-S-FOUNDATION`, `M0590-N-CALKIN`,
`M0590-N-FREDHOLM`, `M0590-L-FWD-SPECTRUM`, `M0590-L-FWD-INDEX`,
`M0590-B-FORWARD`, `M0590-C-BUSBY`, `M0590-L-EXT-CLASS`,
`M0590-L-INDEX-COMPLETE`, and `M0590-T-BACKWARD`.

## Failed Gate And Retry

The first failed gate is terminal proof-body availability for
`M0590-B-FORWARD` and `M0590-T-BACKWARD`; these obligations are the remaining
root cut set. Closing them still requires Calkin and Atkinson bridges, forward
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
| `git status --short --untracked-files=all` | 0 | At start, only the automation-provided untracked `Formalizations/Lean/.lake` link was present. |
| `python3 Stage1_Instances/THM-M-0590/check_obligation_tree.py` | 0 | 17 obligations and 37 typed edges passed; denominator `2d5b17d...9a9e8`; root and both directional packages remain open M4. |
| Isolated `lake env lean --trust=0 -t0` replay of `Statement.lean` and `ObligationTree.lean` | 0 | Exact target and conditional composition elaborated; target stdout SHA-256 `0d233828...f14b`, composer stdout SHA-256 `05a0a820...03a`, both stderr streams empty, and composer axioms `[propext, Classical.choice, Quot.sound]`. |
| Owned Lean prohibited-construct scan | 1 (expected) | No `sorry`, `admit`, `sorryAx`, axiom/bodyless declaration, unsafe/oracle, implementation override, or native-decision shortcut was found. |
| Repo-local exact-name Lean search outside this dossier | 1 (expected) | No unconditional root or directional-package body was found. |
| Pinned-mathlib target/API search | 1 (expected) | No BDF target or missing Calkin, Fredholm-index, essential-spectrum, or Busby API was found. |
| Frozen-registry terminal-body assertion | 0 | Fifteen obligations are machine-required: 14 have no terminal body, and `M0590-T-ASSEMBLE` alone records the conditional composer. |
| Mathlib revision/tree/status check | 0 | Revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, clean dependency worktree. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release; Lake `5.0.0-src+98dc76e`. |
| Prior recheck count plus DAG attempts/children inspection | 0 | Sixteen integrated unresolved rechecks; authoritative `attempts=0`, `children=[]`; split threshold exceeded. |
| JSON, invariant, hash, self-test-absence, and whitespace diagnostic checks | 0 | The paired blocker artifacts, base identity, source hashes, open state, cut set, seventeenth-recheck split trigger, and deliberate self-test absence agreed; no whitespace diagnostic was emitted. |

The exact narrow Lean replay was:

```bash
TMP=$(mktemp -d /tmp/thm-m-0590-proof-229ca98e-slot62.XXXXXX)
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
