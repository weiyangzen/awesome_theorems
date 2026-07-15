# THM-M-1105 proof recheck at `aef94f39` (slot33)

Item: `S56-M-1105-PROOF`

Intent: `prove`

Recorded: `2026-07-15T20:23:00+08:00`

Base revision: `aef94f39853f9222e48f83b2358a6822aafd3c50`

Base tree: `8c42e198fdbcc36b0f5cc0f865e0961715a35c17`

## Verdict

`blocked`. No dependency-legal, placeholder-free proof body or eligible pinned theorem is
available for the exact proposition `Stage1.THM_M_1105.WignerSemicircleLaw`. This run adds no Lean
proof body, closes no obligation, and leaves the root at `[H2, M3, R4]`. It does not satisfy the
assigned proof node or claim audit completion, theorem completion, validation, release, receipt
acceptance, or master acceptance.

The first failed workflow gate is dependency legality and exact-interface readiness. The
authoritative execution DAG renders `S56-M-1105-OBLIGATION_TREE` only provisional `[_]`; both
`[ ]` and `[_]` are unfinished. The owned `task-dag.json` is stricter: `accepted_states` is empty
and the prerequisite remains `open`. Nineteen of the twenty required machine obligations also
retain `planned:v1` fingerprints rather than accepted exact Lean signatures. A proof worker cannot
accept the earlier phase, edit either state authority, or invent the missing signatures.

Kernel closure independently fails. The frozen registry has 22 obligations, 20 machine-required,
and every required `terminal_proof_body_id` is null. The checked theorem
`Stage1.THM_M_1105.ObligationTree.root_of_sample_weak_convergence` consumes the missing
almost-everywhere `SampleWeakConvergence` result as an explicit `terminal` premise. It is a
conditional transport, not a proof, and closes neither `M1105-T-WEAK`, `M1105-T-COMPOSE`, nor
`M1105-ROOT`.

## Proof Search And Root Cut

Pinned mathlib provides Hermitian spectrum and trace, finite-product independence integration,
Borel-Cantelli, tightness, weak-convergence, Catalan, and integration infrastructure, but no
Wigner/random-matrix semicircle terminal. No exact reusable declaration was found elsewhere in
the repository. The immutable candidates remain nonclosing: `semicircle-catalan@95d99de4`
supplies finite Catalan/genus-zero combinatorics only; `HighDimProb@8d4eec8b` supplies
infrastructure only; and `FredRaj3/SemicircleLaw@724f9ad6` is placeholder-bearing,
statement-mismatched, outside the pinned closure, and lacks the exact terminal.

The graph-derived root cut remains `M1105-L-NONPAIR`, `M1105-L-PAIRING`,
`M1105-L-CONCENTRATION`, `M1105-L-TIGHTNESS`, and `M1105-L-BC-APPROX`. The full route also needs
normalized trace expansion, parity and closed-walk classification, independence cancellation,
Catalan enumeration, expected and almost-sure moment convergence, semicircle moments, polynomial
extension, and final weak convergence. Supplying any package as an assumption, axiom, bodyless
declaration, `sorry`, or differently scoped theorem would be a prohibited substitute.

## Current-Base Evidence

All checks reused the automation-provided canonical pinned artifacts read-only. No `lake update`,
`lake build`, dependency clone/fetch, checkout repair, or `.lake` mutation was performed. The
untracked `.lake` symlink makes this warm nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1105` | 0 | Rank 545; lifecycle planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1105/check_obligation_tree.py` | 0 | 22 obligations and 108 typed edges passed; denominator `409c3f4a...26f0e`; root explicitly open at M3. |
| Trust-zero `lake env lean` on `Statement.lean` | 0 | Exact proposition elaborated; only five expected unused-hypothesis warnings. |
| Trust-zero `lake env lean` on `ObligationTree.lean` | 0 | Conditional composition elaborated with its explicit terminal premise; only five expected warnings. |
| Trust-zero `lake env lean` on `AnchorAudit.lean` | 0 | Four supporting declarations elaborated and printed their types. |
| Trust-zero stdin `#print axioms` probe | 0 | Exactly `propext`, `Classical.choice`, and `Quot.sound`; the analytic terminal remains an explicit premise. |
| Parser-oriented prohibited-construct scan over owned `*.lean` | 1 | Expected no-match exit; no placeholder, bodyless axiom-like declaration, unsafe/oracle path, or equivalent construct. |
| Required terminal-body count | 0 | `obligations=22 machine_required=20 with_terminal_body=0 open=20 planned_required=19`. |
| Pinned-mathlib topical source scan | 0 | Only Thales' unrelated geometric semicircle comment; no random-matrix terminal. |
| Repository-local exact-interface scan outside this dossier | 1 | Expected no-match exit; no reusable exact proof body. |
| Proof-input diff from `90a1d52c` through this base | 0 | No change to statement, composition, registry, graphs, inventory, task DAG, toolchain, or Lake manifest. |

Proof-relevant SHA-256 values remain `b7e0e83c...fdf75b` (`Statement.lean`),
`922a4b40...84c0` (`ObligationTree.lean`), `f5561115...45cb` (registry),
`d3ce5de6...e42987` (typed graphs), `eacb015c...b0d612` (anchor inventory), and
`5640b1df...33ae` (task DAG). Pinned identities are Lean 4.29.0 commit
`98dc76e3...16740`, mathlib `8a178386...ea95` / tree `bdc39a31...1c2b`, and
`flt-regular` `56161b6e...1a27` / tree `32c9eace...c893`. The paired JSON records the exact hashes
and command ledger.

## Retry Boundary

There were already 40 structured unresolved proof blocker/recheck records in this owned path,
while the scheduler still reports `attempts: 0` and `children: []` for the proof item. Rev-5.6
section 10.2 mandates splitting after five unresolved ticks. The integration lane must reconcile
and accept the prerequisite, materialize exact node signatures, and replace this oversized parent
redispatch with dependency-legal child assignments for the frozen proof packages. An alternative
retry event is an immutable exact-scope Lean 4 terminal theorem that can be pinned, exact-type
transported, and provenance/trust validated without changing the frozen root.

This is an owned current-base blocker handoff, not a proof receipt. Because the assigned proof
phase is not genuinely self-tested as complete, `.stage1-worker-selftest.json` is deliberately
absent.
