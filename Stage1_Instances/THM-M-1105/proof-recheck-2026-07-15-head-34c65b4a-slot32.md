# THM-M-1105 proof recheck at `34c65b4a` (slot32)

Item: `S56-M-1105-PROOF`

Intent: `prove`

Recorded: `2026-07-15T19:55:57+08:00`

Base revision: `34c65b4a5d82231740b5d5346afe3b11fd795d19`

Base tree: `d961c0376362e94e2f72d9f88ceb2ddf55134577`

## Verdict

`blocked`. No dependency-legal, placeholder-free proof body or immutable pinned theorem is
available for the exact proposition `Stage1.THM_M_1105.WignerSemicircleLaw`. This run adds no Lean
proof body, closes no obligation, and leaves the canonical root at `[H2, M3, R4]`. It does not
satisfy the assigned proof node or claim audit completion, theorem completion, validation, release,
receipt acceptance, or master acceptance.

The first failed workflow gate is dependency legality. The generated scheduler projection renders
`S56-M-1105-OBLIGATION_TREE` only provisional `[_]`, while the owned `task-dag.json` is stricter:
`accepted_states` is empty and the prerequisite is `open`. A proof worker cannot accept that phase
or edit either state authority. In addition, the substantive analytic obligations retain
`planned:v1` fingerprints rather than exact Lean signatures, so bodies cannot be filled against
already accepted interfaces.

Kernel closure independently fails. The frozen registry has 22 obligations, 20 machine-required,
and every required `terminal_proof_body_id` is null. The checked local theorem
`Stage1.THM_M_1105.ObligationTree.root_of_sample_weak_convergence` takes the missing almost-everywhere
`SampleWeakConvergence` result as an explicit premise. It is conditional composition, not an
analytic proof, and closes neither `M1105-T-WEAK`, `M1105-T-COMPOSE`, nor `M1105-ROOT`.

## Proof Search And Root Cut

Pinned mathlib provides supporting spectrum, trace, probability, integration, approximation, and
convergence APIs, but no Wigner/random-matrix semicircle terminal. There is no exact reusable
repository-local declaration outside this dossier. The immutable candidate audit remains
nonclosing: `semicircle-catalan@95d99de4` covers finite Catalan combinatorics only;
`HighDimProb@8d4eec8b` supplies infrastructure only; and
`FredRaj3/SemicircleLaw@724f9ad6` is placeholder-bearing and statement-mismatched.

The graph-derived root cut remains `M1105-L-NONPAIR`, `M1105-L-PAIRING`,
`M1105-L-CONCENTRATION`, `M1105-L-TIGHTNESS`, and `M1105-L-BC-APPROX`. The full route also needs
normalized trace expansion, parity and closed-walk classification, independence cancellation,
Catalan enumeration, expected and almost-sure moment convergence, semicircle moments, polynomial
extension, and final weak convergence. An assumed package, bodyless declaration, axiom, `sorry`, or
differently scoped theorem would be a prohibited substitute.

## Current-Base Evidence

All checks reused the automation-provided canonical pinned artifacts read-only. No `lake update`,
`lake build`, dependency clone/fetch, or `.lake` mutation was performed. The untracked `.lake`
symlink makes this warm nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1105` | 0 | Rank 545; lifecycle planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1105/check_obligation_tree.py` | 0 | 22 obligations and 108 typed edges passed; denominator `409c3f4a...26f0e`; root explicitly open at M3. |
| Trust-zero temporary-directory checks of `Statement.lean` and `ObligationTree.lean` using `lake env lean` and the pinned `LEAN_PATH` | 0 | Both exact current sources elaborated without writing owned or `.lake` artifacts; only the five expected unused-hypothesis warnings occurred. |
| Trust-zero temporary copy with appended `#print axioms` | 0 | Exactly `propext`, `Classical.choice`, and `Quot.sound`; the analytic terminal remains an explicit premise. |
| Parser-oriented prohibited-construct scan over owned `*.lean` | 1 | Expected no-match exit; no placeholder, axiom-like bodyless declaration, unsafe/oracle path, or equivalent construct. |
| Required terminal-body count from `obligation-registry.json` | 0 | `obligations=22 machine_required=20 with_terminal_body=0 open=20`. |
| Pinned-mathlib topical source scan | 0 | Only Thales' unrelated geometric semicircle comment. |
| Repository-local exact-interface scan outside this dossier | 1 | Expected no-match exit; no reusable exact proof body. |
| Proof-input diff from `90a1d52c` to this base | 0 | No change to the statement, composition, registry, graphs, inventory, task DAG, toolchain, or Lake manifest. |
| JSON parse and blocker-invariant checks | 0 | Current base/tree, hashes, paths, fail-closed state, 20 open required bodies, and self-test absence agree. |
| `git diff --check -- Stage1_Instances/THM-M-1105 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

Proof-relevant SHA-256 values remain `b7e0e83c...fdf75b` (`Statement.lean`),
`922a4b40...84c0` (`ObligationTree.lean`), `f5561115...45cb` (registry),
`d3ce5de6...e42987` (typed graphs), `eacb015c...b0d612` (anchor inventory), and
`5640b1df...33ae` (task DAG). Pinned identities remain Lean 4.29.0 commit
`98dc76e3...16740`, mathlib `8a178386...ea95` / tree `bdc39a31...1c2b`, and
`flt-regular` `56161b6e...1a27` / tree `32c9eace...c893`. The paired JSON records the exact hashes
and command ledger.

## Retry Boundary

There were already 38 structured unresolved proof blocker/recheck records in this owned path before
the present packet, although the scheduler still reports `attempts: 0` and `children: []`.
Rev-5.6 requires splitting after five unresolved execution ticks. The integration lane must accept
or reconcile the obligation-tree prerequisite, materialize exact node signatures, and replace this
oversized parent redispatch with dependency-legal child assignments for the frozen proof packages.
An alternative retry event is an immutable exact-scope Lean 4 terminal theorem that can be pinned,
exact-type transported, and provenance/trust validated without changing the frozen target.

This is an owned blocker handoff, not a proof receipt. Because the assigned proof phase is not
genuinely self-tested as complete, `.stage1-worker-selftest.json` is deliberately absent.
