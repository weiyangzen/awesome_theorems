# THM-M-0324 proof blocker at `0261b854` (slot38)

Item: `S56-M-0324-PROOF`

Intent: `prove`

Recorded: `2026-07-15T17:47:08+08:00` (`Asia/Shanghai`)

Base revision: `0261b8540f0ea1bd214785d8675e05c838568a44`

Base tree: `a960a5e67b6ed0ca28cf6237ee01abceb9711953`

## Verdict

`blocked`. No proof body was added or found for the exact root
`Stage1Instances.THM_M_0324.EnfloNoSchauderBasisTarget`. The root remains
`[H1, M3, R4]`, and this proof item remains `[ ]`.

The exact target requires a separable, infinite-dimensional real Banach space
with no `Nat`-indexed `SchauderBasis`. Pinned mathlib supplies the Schauder-basis
object model and projection lemmas, but it supplies neither Enflo's
counterexample space nor a theorem that such a space fails the applicable
approximation property. Repository search found only this dossier and
`S1_M_215`'s open approximation-property vocabulary. No declaration in the
pinned closure inhabits the exact existential target.

The existing `Proof.lean` remains genuine placeholder-free partial work. It
constructs finite-rank Schauder projections converging uniformly on compact
sets and proves that failure of its local compact-approximation predicate
excludes a Schauder basis. It does not prove that failure premise, construct an
Enflo witness, or close a frozen obligation because `M0324-D-APPROX` still has a
planned source-dependent signature.

## Failed Gate

The first failed proof gate is `M0324-C-SPACE`: there is no local or pinned
placeholder-free construction of Enflo's counterexample Banach space. The
downstream Banach, separability, infinite-dimensionality, and exact
approximation-property-failure packages are consequently open. The remaining
root cut is `M0324-C-SPACE`, `M0324-X-SOURCE`, and `M0324-X-FOUNDATION`.

Assuming the missing failure theorem, treating a conditional composer as a
root proof, using a nonseparable shortcut, or proving failure of one chosen
sequence would weaken or substitute the frozen target and is not admissible.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to the
canonical pinned artifacts was reused read-only. No `lake update`, `lake
build`, dependency clone/fetch, network operation, or `.lake` mutation was
performed. Temporary Lean objects and logs were written only under `/tmp` and
removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0324` | 0 | Rank 820; `planned`; hard-statement-first-partial-verification lane; theorem incomplete |
| Disposable ordered direct replay with the Lean executable selected by `lake env`, explicit existing-package `LEAN_PATH`, and `--trust=0 -t0` on `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` | 0 | `Statement_exit=0 ObligationTree_exit=0 Proof_exit=0`; log SHA-256 values `2bfc8d72...a60f0c`, `c8af60b...b1107`, and `7e2bf773...b8c6b`; all four local bodies reported exactly `propext`, `Classical.choice`, and `Quot.sound` |
| The same ordered replay invoking `lake env lean` separately for every module | 1 | `Statement.lean` and `ObligationTree.lean` exited 0, but `Proof.lean` could not see the temporary `ObligationTree.olean`; this runner-boundary failure was superseded by the successful direct invocation above, which kept the selected pinned executable and explicit module path stable |
| `python3 Stage1_Instances/THM-M-0324/check_obligation_tree.py` | 0 | Passed 15 obligations and 55 typed edges; denominator `8bfbe341...f101b`; root remained open at M3 |
| Token-anchored prohibited-device scan over `Stage1_Instances/THM-M-0324/*.lean` | 1 expected | No `sorry`, `admit`, `sorryAx`, `native_decide`, `implemented_by`, `run_tac`, or axiom/constant/opaque/unsafe/extern declaration found |
| Exact-topic `rg` over repository Lean, this dossier, pinned mathlib, and pinned `flt-regular` | 0 | 46 contextual hits, confined to this dossier, Schauder substrate, `S1_M_215`'s open vocabulary, and an unrelated phrase; no terminal Enflo body found |
| `git diff --check -- Stage1_Instances/THM-M-0324`, plus `git diff --no-index --check /dev/null` on both new blocker files | 0 | No whitespace diagnostics; each no-index invocation returned 1 solely because a new file differs from `/dev/null`, as expected |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion self-test was emitted because the assigned proof phase is incomplete |

This is current-base, nonrelease kernel evidence for the existing partial bodies
and blocker evidence for the exact root. It is not proof closure.

## Scheduler Boundary

Twelve prior structured proof rechecks are already tracked. Every one records
`blocked`, `proof_phase_complete=false`, `root_closed=false`, and the same first
failed gate `M0324-C-SPACE`, while the authoritative execution node still has
`attempts=0` and no children. Blueprint section 10.2 requires a split after five
unresolved execution ticks. The integration lane must reconcile which packets
count, then split or redirect this oversized item instead of scheduling another
unchanged whole-root recheck. This worker did not edit authoritative state.

Resume only after placeholder-free bodies exist for Enflo's construction and
the downstream analytic packages, with the exact approximation-property
convention crosswalked. An alternative is immutable compatible integration of
an exact Lean 4 terminal proof with complete dependency, license, trust, and
provenance evidence.

This blocker does not satisfy `S56-M-0324-PROOF`, close a frozen obligation or
the root, change scheduler state, or claim audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance. Because the
proof phase is incomplete, `.stage1-worker-selftest.json` is deliberately
absent.
