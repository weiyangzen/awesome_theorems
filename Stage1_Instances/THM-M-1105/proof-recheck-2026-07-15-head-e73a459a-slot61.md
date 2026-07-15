# THM-M-1105 proof recheck at `e73a459a` (slot61)

Item: `S56-M-1105-PROOF`

Intent: `prove`

Recorded: `2026-07-15T18:36:31+08:00`

Base revision: `e73a459aa33f8b656019c9c36e3d5dfc84dffc30`

Base tree: `81105927f8e46d0076dd20433240ecf0fd185cea`

## Verdict

`blocked`. No dependency-legal, placeholder-free local body or immutable pinned theorem proves the
exact proposition `Stage1.THM_M_1105.WignerSemicircleLaw`. This run adds no Lean proof body, closes
no obligation, and leaves the exact root at `[H2, M3, R4]`. It does not satisfy the assigned proof
node or claim audit completion, theorem completion, validation, release, receipt acceptance, or
master acceptance.

The first failed workflow gate is dependency legality. The structured authority in
`task-dag.json` has `accepted_states: []` and still records `S56-M-1105-OBLIGATION_TREE` as `open`,
while the scheduler projection renders that prerequisite only provisional `[_]`. Both states are
unfinished under rev-5.6, and this proof worker may neither accept an earlier phase nor edit the
authoritative scheduler state.

Independently, kernel closure fails. The frozen registry has 22 obligations, 20 machine-required,
and every required `terminal_proof_body_id` is null. The checked local theorem
`Stage1.THM_M_1105.ObligationTree.root_of_sample_weak_convergence` consumes
`terminal : forall-almost-everywhere omega, SampleWeakConvergence A hA_hermitian omega`. That
premise is the missing analytic conclusion, so this declaration is conditional composition and
closes neither `M1105-T-WEAK`, `M1105-T-COMPOSE`, nor `M1105-ROOT`.

## Proof Search And Root Cut

Pinned mathlib contains supporting spectrum, trace, probability, integration, tightness, and
approximation interfaces, but no Wigner/random-matrix semicircle terminal. A current-base
repository-local exact-interface search found no reusable body. The immutable candidates remain
nonclosing: `semicircle-catalan@95d99de4` supplies finite Catalan combinatorics only;
`HighDimProb@8d4eec8b` supplies infrastructure only; and
`FredRaj3/SemicircleLaw@724f9ad6` is placeholder-bearing and has no almost-sure weak
empirical-spectral terminal for this exact target.

The graph-derived root cut remains `M1105-L-NONPAIR`, `M1105-L-PAIRING`,
`M1105-L-CONCENTRATION`, `M1105-L-TIGHTNESS`, and `M1105-L-BC-APPROX`. Completing the route also
requires the registered trace-power expansion, closed-walk classification, independence
cancellation, Catalan enumeration, expected and almost-sure moment packages, semicircle moments,
polynomial extension, and weak-convergence composition. Supplying any package as a premise,
bodyless declaration, axiom, `sorry`, or differently scoped theorem would be a prohibited
shortcut.

## Current-Base Checks

No `lake update`, `lake build`, clone, fetch, dependency repair, or `.lake` mutation was performed.
The automation-provided `.lake` symlink points to shared canonical pinned artifacts, so this is
warm nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1105` | 0 | Rank 545; lifecycle planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1105/check_obligation_tree.py` | 0 | 22 obligations and 108 typed edges passed; denominator `409c3f4a...26f0e`; root explicitly open at M3. |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-1105/Statement.lean` | 0 | Exact proposition elaborated; five unused-hypothesis warnings only. |
| Same command for `ObligationTree.lean` | 0 | Conditional composition elaborated with its explicit terminal premise; five unused-hypothesis warnings only. |
| Trust-zero temporary source replay of the composition plus `#print axioms` | 0 | Exactly `propext`, `Classical.choice`, and `Quot.sound`; the analytic terminal remains an explicit premise. The temporary file was removed. |
| Parser-oriented prohibited-construct scan over owned `*.lean` | 1 | Expected no-match exit; no placeholder, axiom-like bodyless declaration, unsafe/oracle path, or equivalent construct. |
| Required-terminal-body count from `obligation-registry.json` | 0 | `obligations=22 machine_required=20 with_terminal_body=0 open=20`. |
| Pinned-mathlib topical source scan | 0 | Only Thales' unrelated geometric semicircle comment. |
| Repository-local exact-interface scan outside this dossier | 1 | Expected no-match exit; no reusable exact proof body. |
| Proof-input diff from `118d66d` to this base | 0 | No changes to the statement, composition, registry, graphs, inventory, task DAG, toolchain, or Lake manifest. |

Proof-relevant hashes remain `b7e0e83c...fdf75b` (`Statement.lean`),
`922a4b40...84c0` (`ObligationTree.lean`), `f5561115...45cb` (registry),
`d3ce5de6...e42987` (typed graphs), `eacb015c...b0d612` (anchor inventory), and
`5640b1df...33ae` (task DAG). Pinned identities are Lean 4.29.0 commit
`98dc76e3...16740`, mathlib `8a178386...ea95` / tree `bdc39a31...1c2b`, and
`flt-regular` `56161b6e...1a27` / tree `32c9eace...c893`. The paired JSON artifact records the
full hashes and exact command ledger.

## Retry Boundary

There were already 32 structured unresolved proof blocker/recheck records in the owned path before
this run, while the scheduler still reports `attempts: 0` and `children: []`. Rev-5.6 section 10.2
requires a split after five unresolved execution ticks. The integration lane must reconcile the
obligation-tree prerequisite and replace this oversized parent redispatch with dependency-legal
child assignments for the frozen proof packages. An alternative retry event is an immutable exact-
scope Lean 4 terminal theorem that can be pinned, exact-type transported, and provenance/trust
validated without changing the target.

This is an owned blocker handoff, not a proof receipt. Because the proof phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` is deliberately absent.
