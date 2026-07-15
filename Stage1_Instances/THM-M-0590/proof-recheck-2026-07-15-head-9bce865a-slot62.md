# THM-M-0590 proof phase blocked at `9bce865a` (`slot62`)

Item: `S56-M-0590-PROOF`

Recorded: `2026-07-15T13:48:35+08:00`

Base revision: `9bce865a14bcc270344ea909d6936c6ea22aa1c2`

Base tree: `523a9471aac257c4cf54acceee07172fab22f5b4`

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
no Calkin-algebra, general Fredholm-index, essential-spectrum,
Busby-extension, or BDF-classification implementation. A scoped repo-local
Lean search likewise found no unconditional body outside this dossier. The
prior immutable anchor audit retained no exact compatible external Lean 4
candidate. This run used no network and makes no global nonexistence claim.

No premise, axiom, placeholder, weaker target, changed convention, moving
dependency, or unrelated-target change was introduced. The proof item remains
`[ ]`; the root remains `[H1, M4, R3]`. No proof, validation, release,
theorem-completion, receipt, or master-acceptance claim is made. Because the
proof phase is incomplete, `.stage1-worker-selftest.json` is deliberately
absent.

## Split Required

Fourteen integrated unresolved proof-recheck packets existed before this run,
so this is the fifteenth root-sized recheck. The authoritative DAG still
records `attempts=0` and `children=[]`. Rev-5.6 section 10.2 requires a split
after five unresolved execution ticks rather than another root-sized
assignment. This worker cannot edit scheduler authority or the generated
checklist, so the master must reconcile the cursor and create dependency-legal
child tasks before another proof retry.

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
checks. A citation, auxiliary lemma, or conditional composer does not satisfy
this condition.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was performed. Temporary Lean objects were created under `/tmp` and
removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0590` | 0 | Rank 630; lifecycle `planned`; hard-statement-first lane; legacy artifacts unaccepted; theorem incomplete. |
| Start-state identity check | 0 | Only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present; base `9bce865a...1c2`, tree `523a9471...b5b4`, and the tracked patch was empty. |
| `python3 Stage1_Instances/THM-M-0590/check_obligation_tree.py` | 0 | 17 obligations and 37 typed edges passed; denominator `2d5b17d...9a9e8`; root and both directional packages remain open M4. |
| `cd Formalizations/Lean && timeout 60 lake env lean --version` | 1 | The repository entry point reported that shared `flt-regular` could not resolve `HEAD`; no repair or mutation was attempted. |
| Pinned-mathlib `lake env` Lean replay of `Statement.lean` and `ObligationTree.lean` with `--trust=0 -t0` | 0 | Exact target and conditional composition elaborated; target stdout SHA-256 `0d233828...f14b`, target olean SHA-256 `943e690c...e38`, composer stdout SHA-256 `05a0a820...03a`, both stderr streams empty, and composer axioms `[propext, Classical.choice, Quot.sound]`. |
| Owned Lean prohibited-construct scan | 1 (expected) | No `sorry`, `admit`, `sorryAx`, axiom/bodyless declaration, unsafe/oracle, implementation override, or native-decision shortcut was found. |
| Repo-local exact-name Lean search outside this dossier | 1 (expected) | No unconditional root or directional-package proof body was found. |
| Pinned-mathlib target/API search | 1 (expected) | No BDF target or missing Calkin, Fredholm-index, essential-spectrum, or Busby API was found. |
| Frozen-registry terminal-body assertion | 0 | Fifteen obligations are machine-required: 14 have no terminal body, and `M0590-T-ASSEMBLE` alone records the conditional composer. |
| Mathlib revision/tree/status check | 0 | Revision `8a178386...e95`, tree `bdc39a31...c2b`, clean dependency worktree. |
| Toolchain check from pinned mathlib checkout | 0 | Lean 4.29.0 commit `98dc76e3...740`; Lake `5.0.0-src+98dc76e`. |
| Prior recheck count plus DAG attempts/children inspection | 0 | Fourteen integrated unresolved rechecks; authoritative `attempts=0`, `children=[]`, state `[ ]`; split threshold exceeded. |
| JSON, invariant, hash, self-test-absence, and `git diff --no-index --check` diagnostic checks | 0 | The paired blocker JSON parsed; base identity, source hashes, open state, cut set, fifteenth-recheck split trigger, changed paths, and deliberate self-test absence agreed; no whitespace diagnostics were emitted. |

The successful narrow replay obtained `lean` through `lake env` in the pinned
mathlib checkout and used an explicit `LEAN_PATH` containing eight existing
canonical package `build/lib/lean` directories, excluding the broken
`flt-regular` checkout. It used `LEAN_NUM_THREADS=1`, `timeout 600`,
`--trust=0`, and `-t0`. It first wrote `Statement.olean` under a new `/tmp`
directory, added that directory to `LEAN_PATH`, checked
`ObligationTree.lean`, and removed the temporary directory. Exact hashes and
results are recorded in the paired JSON artifact.

This current-base blocker record is not a proof receipt. It does not satisfy
`S56-M-0590-PROOF`, change scheduler state, or claim M0, audit completion,
theorem completion, validation, release, or master acceptance.
