# THM-M-1105 proof recheck at `7787e214` (slot34)

Item: `S56-M-1105-PROOF`

Intent: `prove`

Recorded: `2026-07-15T21:40:27+08:00`

Base revision: `7787e214a8b29a1e90effb45a51c79bf485e1d78`

Base tree: `3bd6ee7fd3409565bd5ddfb06d6c007b063b7984`

## Verdict

`blocked`. No dependency-legal, placeholder-free proof body or immutable pinned exact theorem is
available for `Stage1.THM_M_1105.WignerSemicircleLaw`. This run adds no Lean body, closes no
obligation, and leaves the root at `[H2, M3, R4]`. It does not satisfy the assigned proof node or
claim audit completion, theorem completion, validation, release, receipt acceptance, or master
acceptance.

Dependency legality and interface readiness fail first. The generated blueprint marks
`S56-M-1105-OBLIGATION_TREE` only provisional `[_]`, while the owned `task-dag.json` has
`accepted_states: []` and still records that prerequisite as `open`. In addition, 19 of the 20
machine-required nodes have only `planned:v1` fingerprints and prose signatures. A proof worker
cannot fill exact bodies for interfaces that the prerequisite phase has not materialized and the
master has not accepted.

Kernel closure independently fails. The frozen registry has 22 obligations, 20 machine-required,
and all 20 have `terminal_proof_body_id: null`. The sole checked theorem,
`root_of_sample_weak_convergence`, consumes an explicit almost-everywhere
`SampleWeakConvergence` premise. That premise is the missing analytic conclusion, so the theorem
closes neither `M1105-T-WEAK`, `M1105-T-COMPOSE`, nor `M1105-ROOT`.

## Scope And Root Cut

The target is not vacuous and no contradictory hypotheses or legitimate short proof were found.
Standard bounded symmetric Wigner examples satisfy its assumptions. A real proof must implement the
frozen moment route: trace expansion, closed-walk classification, independence cancellation,
non-pairing suppression, Catalan leading terms, expected and almost-sure moments, semicircle
moments, tightness, polynomial extension, bounded-continuous approximation, and terminal weak
convergence. Assuming the sample convergence premise or proving only finite Catalan combinatorics
would change the theorem.

The graph-derived immediate cut remains `M1105-L-NONPAIR`, `M1105-L-PAIRING`,
`M1105-L-CONCENTRATION`, `M1105-L-TIGHTNESS`, and `M1105-L-BC-APPROX`. Pinned mathlib contains
supporting matrix, probability, integration, and approximation APIs, but no Wigner semicircle
terminal. The repository has no exact reusable declaration outside this dossier. The immutable
external candidates remain partial, outside the pinned closure, placeholder-bearing,
statement-mismatched, or a combination of those blockers.

## Current-Base Checks

No `lake update`, `lake build`, clone, fetch, dependency repair, or `.lake` mutation was performed.
The automation-provided `.lake` symlink was reused read-only, so these checks are warm nonrelease
evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1105` | 0 | Rank 545; lifecycle planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1105/check_obligation_tree.py` | 0 | 22 obligations and 108 typed edges passed; denominator `409c3f4a...26f0e`; root open at M3. |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout --foreground --kill-after=10s 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-1105/Statement.lean` | 0 | Exact proposition elaborated and printed its type; five unused-hypothesis warnings only. |
| The same command for `ObligationTree.lean` | 0 | Conditional composition elaborated and exposed its terminal premise; five unused-hypothesis warnings only. |
| Trust-zero stdin replay with `#print axioms Stage1.THM_M_1105.ObligationTree.root_of_sample_weak_convergence` | 0 | Exactly `propext`, `Classical.choice`, and `Quot.sound`; analytic convergence remains an explicit premise. |
| Parser-oriented prohibited-construct scan over owned `*.lean` | 1 | Expected no-match exit; no placeholder, bodyless axiom-like declaration, unsafe/oracle path, or equivalent construct. |
| Exact `jq` registry count query | 0 | `obligations=22 machine_required=20 with_terminal_body=0 open=20 planned_required=19`. |
| Pinned-mathlib topical source scan | 0 | Only Thales' unrelated geometric semicircle comment. |
| Repository-local exact-interface scan outside this dossier | 1 | Expected no-match exit; no reusable exact body. |
| Proof-input diff from `118d66d` to this base | 0 | No statement, composition, registry, graph, inventory, task-DAG, toolchain, or Lake-manifest change. |
| `python3 -m json.tool`, structured invariant checks, and `git diff --check` | 0 | The blocker packet is valid, current-base-bound, fail-closed, and free of whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test deliberately absent. |

Exact hashes and full commands are recorded in the paired JSON. Pinned identities are Lean 4.29.0
commit `98dc76e3...16740`, mathlib `8a178386...ea95` / tree `bdc39a31...1c2b`, and `flt-regular`
`56161b6e...1a27` / tree `32c9eace...c893`.

## Retry Boundary

There were 44 structured unresolved proof blocker/recheck records in this owned path before this
run, but the scheduler item still reports `attempts: 0` and `children: []`. Rev-5.6 section 10.2
requires a split after five unresolved execution ticks. The integration lane must accept and
reconcile the prerequisite, materialize exact node signatures, and create dependency-legal child
assignments for the substantive proof packages. The only alternative is a new immutable exact-scope
Lean 4 theorem that can be pinned and validated without changing the root.

This is an owned blocker handoff, not a proof receipt. Because the assigned proof phase is not
genuinely self-tested as complete, `.stage1-worker-selftest.json` is deliberately absent.
