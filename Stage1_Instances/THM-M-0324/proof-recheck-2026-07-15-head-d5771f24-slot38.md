# THM-M-0324 proof-phase recheck at `d5771f24`

Item: `S56-M-0324-PROOF`

Intent: `prove`

Recorded: `2026-07-15T18:24:15+08:00` (`Asia/Shanghai`)

Base revision: `d5771f240b8fe26277d018c90fec963af76ed7f2`

Base tree: `f274a52fcf9e5edcd6b8f8dd43726122a041af50`

## Verdict

`blocked`. No proof body was added or found for the exact root
`Stage1Instances.THM_M_0324.EnfloNoSchauderBasisTarget`. The root remains
`[H1, M3, R4]`, and this proof item remains `[ ]`.

The target requires an actual separable, infinite-dimensional real Banach
space with no `Nat`-indexed `SchauderBasis`. The current pinned closure contains
the Schauder object model and its projection lemmas, but neither Enflo's
counterexample space nor a theorem that such a space fails the applicable
approximation property. Independent read-only Lean and repository searches
confirmed that no available declaration inhabits the exact existential target.

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
approximation-property-failure packages remain open. The remaining root cut is
`M0324-C-SPACE`, `M0324-X-SOURCE`, and `M0324-X-FOUNDATION`.

Pinned mathlib `8a178386...` supplies `SchauderBasis.range_proj_eq_span`,
`SchauderBasis.tendsto_proj`, and `SchauderBasis.exists_norm_proj_le` in
`Mathlib.Analysis.Normed.Module.Bases`. Its rank-one-decomposition API
constructs a basis from suitable projections, which is the opposite direction
from the missing counterexample. The adjacent repository module `S1_M_215`
supplies only open approximation vocabulary and a finite-dimensional positive
case. Pinned `flt-regular` supplies nothing on this target.

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
| `cd Formalizations/Lean && ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| Disposable ordered replay through the pinned Lake environment with `--trust=0 -t0` on `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` | 0 | `Statement_exit=0 ObligationTree_exit=0 Proof_exit=0`; log SHA-256 values `2bfc8d72...a60f0c`, `c8af60b...b1107`, and `7e2bf773...b8c6b`; all four local bodies reported exactly `propext`, `Classical.choice`, and `Quot.sound` |
| Initial disposable replay with `LEAN_PATH` set outside `lake env lean` | 1 | Statement and obligation modules passed, but Lake replaced the outer path and `Proof.lean` could not resolve the temporary obligation module; the successful `lake env env` replay above supersedes this runner-boundary failure |
| `python3 Stage1_Instances/THM-M-0324/check_obligation_tree.py` | 0 | Passed 15 obligations and 55 typed edges; denominator `8bfbe341...f101b`; root remained open at M3 |
| Token-anchored prohibited-device scan over `Stage1_Instances/THM-M-0324/*.lean` | 1 expected | No `sorry`, `admit`, `sorryAx`, `native_decide`, `implemented_by`, `run_tac`, or axiom/constant/opaque/unsafe/extern declaration found |
| Exact-topic `rg` over repository Lean and pinned mathlib/`flt-regular` | 0 | Relevant hits were confined to this dossier, Schauder substrate, and `S1_M_215`'s open vocabulary; no terminal Enflo body found |
| `python3 -m json.tool Stage1_Instances/THM-M-0324/proof-recheck-2026-07-15-head-d5771f24-slot38.json` | 0 | Structured blocker parsed |
| `git diff --check -- Stage1_Instances/THM-M-0324`, plus `git diff --no-index --check /dev/null` on both new files | 0 | No whitespace diagnostics; the no-index commands returned 1 only because each new file differs from `/dev/null`, as expected |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion self-test was emitted because the assigned proof phase is incomplete |

This is current-base nonrelease kernel evidence for the existing partial bodies
and blocker evidence for the exact root. It is not proof closure.

## Scheduler Boundary

Fourteen structured proof packets predate this run: the initial partial
implementation packet plus thirteen later whole-item rechecks/blockers. The
initial packet left the phase open, and every later packet records the same
`M0324-C-SPACE` failure, `proof_phase_complete=false`, and
`root_closed=false`. The authoritative execution node nevertheless still has
`attempts=0` and no children. Blueprint section 10.2 requires a split after five
unresolved execution ticks. The integration lane must reconcile which packets
count, then split or redirect this oversized item instead of scheduling another
unchanged whole-root recheck. This worker did not edit authoritative state.

The prerequisite is also only provisional (`[_]`) in the authoritative
projection and open in the stale target-local task DAG. `instance.json` still
contains intake-era registry and owned-artifact fields. These are preexisting
master-reconciliation debts, not proof bodies, and this worker did not silently
rewrite them.

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
