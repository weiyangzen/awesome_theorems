# THM-M-1105 proof recheck at `f9c6966c` (slot39)

Item: `S56-M-1105-PROOF`

Intent: `prove`

Recorded: `2026-07-16T00:35:51+08:00`

Base revision: `f9c6966c4a9f779a85442d309d9a4e6d4bbfe36b`

Base tree: `153efbfdf2465303d2ee3999dfbd92ee883d6220`

## Verdict

`blocked`. No dependency-legal, placeholder-free local proof body or immutable pinned theorem
proves the exact proposition `Stage1.THM_M_1105.WignerSemicircleLaw`. This run adds no Lean proof
body, closes no obligation, and leaves the root at `[H2, M3, R4]`. It does not satisfy the proof
item or claim audit completion, theorem completion, validation, release, receipt acceptance, or
master acceptance.

Dependency legality fails first. `S56-M-1105-OBLIGATION_TREE` is only provisional `[_]` in the
authoritative scheduler projection, while the owned `task-dag.json` has `accepted_states: []` and
records that prerequisite as `open`. Both states are unfinished under rev-5.6. A proof worker
cannot accept the prerequisite or edit authoritative scheduler state.

Independently, the frozen architecture is not ready for proof execution. Nineteen of the twenty
machine-required obligations have only `planned:v1` fingerprints rather than exact Lean
signatures, and all twenty have `terminal_proof_body_id: null`. The only checked theorem,
`Stage1.THM_M_1105.ObligationTree.root_of_sample_weak_convergence`, consumes
`terminal : forall-almost-everywhere omega, SampleWeakConvergence A hA_hermitian omega`. That
premise is the missing analytic weak-convergence result, so the declaration is conditional
composition rather than a body for `M1105-T-WEAK`, `M1105-T-COMPOSE`, or `M1105-ROOT`.

## Proof Search And Root Cut

Pinned mathlib contains supporting spectrum, trace, probability, integration, approximation, and
convergence interfaces but no Wigner/random-matrix semicircle theorem. No exact-interface proof
exists elsewhere in the repository. The frozen external candidates remain nonclosing:
`semicircle-catalan@95d99de4` covers finite Catalan combinatorics only,
`HighDimProb@8d4eec8b` supplies infrastructure only, and
`FredRaj3/SemicircleLaw@724f9ad6` is placeholder-bearing, lacks an almost-sure weak-convergence
terminal, and has a mismatched ensemble and convergence mode. None is in the pinned closure.

The graph-derived root cut is `M1105-L-NONPAIR`, `M1105-L-PAIRING`,
`M1105-L-CONCENTRATION`, `M1105-L-TIGHTNESS`, and `M1105-L-BC-APPROX`. The complete route also
requires normalized trace expansion, parity and closed-walk classification, independence
cancellation, Catalan enumeration, expected and almost-sure moment convergence, semicircle
moments, polynomial extension, and weak-convergence composition. An assumption, bodyless
declaration, axiom, `sorry`, or differently scoped theorem for any package would be a prohibited
shortcut.

## Current-Base Validation

No `lake update`, `lake build`, dependency clone/fetch, checkout repair, or `.lake` mutation was
performed. The automation-provided `.lake` symlink points to the canonical pinned artifacts, so
the Lean checks below are warm nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1105` | 0 | Rank 545; planned lifecycle; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1105/check_obligation_tree.py` | 0 | 22 obligations and 108 typed edges passed; denominator `409c3f4a...26f0e`; root explicitly open at M3. |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout --foreground --kill-after=10s 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-1105/Statement.lean` | 0 | The exact canonical proposition elaborated and printed its type; five unused-hypothesis linter warnings only. |
| Same command for `ObligationTree.lean` | 0 | Conditional composition elaborated and printed its explicit terminal premise; five unused-hypothesis linter warnings only. |
| Trust-zero stdin replay plus `#print axioms Stage1.THM_M_1105.ObligationTree.root_of_sample_weak_convergence` | 0 | Exactly `propext`, `Classical.choice`, and `Quot.sound`; the analytic terminal remains an explicit premise. |
| Parser-oriented prohibited-construct scan over owned `*.lean` | 1 | Expected no-match exit; no placeholder, bodyless axiom-like declaration, unsafe/oracle path, or equivalent construct. |
| Exact required-terminal-body count from `obligation-registry.json` | 0 | `obligations=22 machine_required=20 with_terminal_body=0 open=20 planned_required=19`. |
| Pinned-mathlib topical source scan | 0 | Only Thales' unrelated geometric use of "semicircle". |
| Repository-local exact-interface scan outside this dossier | 1 | Expected no-match exit; no reusable exact proof body. |
| Proof-input diff from `270e3fb3` to this base | 0 | No change to the statement, composition, registry, graphs, inventory, task DAG, toolchain, or Lake manifest. |

Proof-relevant SHA-256 values remain `b7e0e83c...fdf75b` (`Statement.lean`),
`922a4b40...84c0` (`ObligationTree.lean`), `f5561115...45cb` (registry),
`d3ce5de6...e42987` (typed graphs), `eacb015c...b0d612` (anchor inventory), and
`5640b1df...33ae` (task DAG). The pinned environment is Lean 4.29.0 commit
`98dc76e3...16740` and mathlib `8a178386...ea95` / tree `bdc39a31...1c2b`.

## Retry Boundary

There were already 47 structured unresolved proof blocker/recheck records in this owned path
before this run, while the assigned scheduler record still reports `attempts: 0` and `children: []`.
Rev-5.6 requires splitting after five unresolved execution ticks. The integration lane must first
reconcile and accept the obligation-tree prerequisite, materialize exact Lean signatures for the
substantive nodes, and split this parent into dependency-legal child assignments for the frozen
proof packages. The alternative retry event is an immutable exact-scope Lean 4 terminal theorem
that can be pinned, exact-type transported, and provenance/trust checked without changing the root.

This is a target-owned blocker handoff, not a proof receipt. Because the assigned proof phase is
not genuinely self-tested as complete, `.stage1-worker-selftest.json` is deliberately absent.
