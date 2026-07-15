# THM-M-1105 proof recheck at `46320e01` (slot41)

Item: `S56-M-1105-PROOF`

Intent: `prove`

Recorded: `2026-07-15T14:03:52+08:00`

Base revision: `46320e01d1897482417e7b0d03a15a5b77ae5275`

Base tree: `2260ad94d18a6662ffc00f47b8955ae3a2a18184`

## Verdict

`blocked`. No placeholder-free body or dependency-legal immutable import proves the exact
canonical proposition `Stage1.THM_M_1105.WignerSemicircleLaw`. This run adds no Lean proof body,
closes no obligation, and leaves the root at `[H2, M3, R4]`. It does not satisfy the assigned proof
item or claim audit completion, theorem completion, validation, release, receipt acceptance, or
master acceptance.

The local dependency gate is not accepted: `task-dag.json` has `accepted_states: []` and records
`S56-M-1105-OBLIGATION_TREE` as `open`, although the scheduler projection renders that prerequisite
provisional. Independently, all 20 machine-required obligations still have
`terminal_proof_body_id: null`. The only checked local theorem,
`Stage1.THM_M_1105.ObligationTree.root_of_sample_weak_convergence`, consumes
`terminal : forall-almost-everywhere omega, SampleWeakConvergence A hA_hermitian omega`. That
premise is the missing analytic conclusion, so the declaration is conditional composition rather
than a body for `M1105-T-WEAK`, `M1105-T-COMPOSE`, or `M1105-ROOT`.

There is no contradiction or vacuity shortcut. Bounded independent symmetric Rademacher
off-diagonal entries with zero diagonal have the standard shape of a model satisfying the frozen
hypotheses. The target requires substantive random-matrix combinatorics and analysis.

## Failed Gates And Root Cut

The first workflow gate is dependency legality: the owned state authority has not accepted the
obligation-tree prerequisite. Even after that is reconciled, kernel proof closure first fails at
`M1105-L-NONPAIR`: no eligible body proves asymptotic suppression of all surviving non-pairing and
diagonal-containing walk patterns for the frozen bounded triangular array. The graph-derived root
cut is `M1105-L-NONPAIR`, `M1105-L-PAIRING`, `M1105-L-CONCENTRATION`,
`M1105-L-TIGHTNESS`, and `M1105-L-BC-APPROX`.

The complete route also requires normalized trace expansion, parity and closed-walk
classification, independence cancellation, Catalan enumeration, expected and almost-sure moment
convergence, semicircle moments, polynomial extension, and final weak convergence. Supplying any
package as an assumption, bodyless declaration, axiom, `sorry`, or differently scoped theorem
would be a prohibited shortcut.

Pinned mathlib has supporting spectrum, trace, probability, integration, tightness, approximation,
and convergence APIs, but no Wigner/random-matrix semicircle theorem. Repository sources contain
no exact body. The frozen candidate audit remains decisive: `semicircle-catalan@95d99de4` supplies
finite combinatorics only, `HighDimProb@8d4eec8b` supplies infrastructure only, and
`FredRaj3/SemicircleLaw@724f9ad6` contains placeholders and proves neither this ensemble nor its
almost-sure weak terminal. None earns proof credit.

## Current-Base Validation

No `lake update`, `lake build`, dependency clone/fetch, checkout repair, or `.lake` mutation was
performed. The automation-provided `.lake` symlink points to shared canonical artifacts, so these
checks are warm nonrelease evidence. The prescribed `lake env lean` commands stopped before target
elaboration because the shared, target-irrelevant `flt-regular` checkout cannot resolve `HEAD`;
worker policy forbids repairing it.

The same pinned Lean 4.29.0 binary was therefore invoked read-only with `LEAN_PATH` assembled from
the existing canonical package build directories other than `flt-regular`. Both owned modules
elaborated at trust level zero. This fallback validates the exact open interfaces but closes no
obligation.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1105` | 0 | Rank 545; lifecycle planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1105/check_obligation_tree.py` | 0 | 22 obligations and 108 typed edges passed; denominator `409c3f4a...26f0e`; root explicitly open at M3. |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-1105/Statement.lean` | 1 | Lake stopped before elaboration because `.lake/packages/flt-regular` could not resolve `HEAD`. |
| Same root-Lake command for `ObligationTree.lean` | 1 | The shared dependency defect prevented usable target elaboration. |
| Pinned `lean` 4.29.0 plus existing-package `LEAN_PATH`, `--trust=0 -t0`, on `Statement.lean` | 0 | Exact proposition elaborated; only five expected unused-hypothesis warnings. |
| Same direct pinned-Lean check of `ObligationTree.lean` | 0 | Conditional composition elaborated with its explicit terminal premise; only five expected warnings. |
| Stdin trust-zero `#print axioms` probe | 0 | Exactly `propext`, `Classical.choice`, and `Quot.sound`; the analytic terminal remains an explicit unproved premise. |
| Token-aware prohibited-construct scan over owned `*.lean` files | 1 | Expected no-match exit; no placeholder, bodyless axiom-like declaration, unsafe/oracle path, or equivalent construct. |
| Required terminal-body count | 0 | `machine_required=20 with_terminal_body=0 open=20`. |
| Pinned-mathlib topical source scan | 0 | Only Thales' unrelated geometric semicircle comment; no random-matrix terminal. |
| Repository-local exact-interface scan outside this dossier | 1 | Expected no-match exit; no reusable exact proof body. |
| Proof-input diff from `714fb3bb` to this base | 0 | No change to statement, composition, registry, graphs, inventory, toolchain, or Lake manifest. |
| JSON parse and blocker-invariant check | 0 | Identity, base/tree, 20 open required bodies, fail-closed state, changed paths, and self-test declaration agree. |
| `git diff --check -- Stage1_Instances/THM-M-1105 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

Proof-relevant hashes remain `b7e0e83c...fdf75b` (`Statement.lean`),
`922a4b40...84c0` (`ObligationTree.lean`), `f5561115...45cb` (registry),
`d3ce5de6...e42987` (typed graphs), and `eacb015c...b0d612` (anchor inventory).
Pinned identities are Lean 4.29.0 commit `98dc76e3...16740` and mathlib
`8a178386...ea95` / tree `bdc39a31...1c2b`. Exact hashes and the complete command ledger are in
the paired JSON artifact.

## Workflow And Retry Boundary

Before this run the owned path already contained 19 structured unresolved proof blocker/recheck
records, while the scheduler projection still says `attempts: 0` and `children: []`. Section 10.2
requires an item split after five unresolved execution ticks. The worker may not edit the
authoritative DAG, the generated checklist, or an earlier phase's state, so the integration lane
must reconcile the prerequisite and split this oversized proof item before dispatching it again.

Resume only after the obligation-tree prerequisite is accepted and dependency-legal child
assignments exist for placeholder-free implementations of the frozen proof packages, or after an
immutable exact-scope Lean 4 terminal theorem becomes available for pinning, exact-type transport,
and provenance/trust validation without changing the target.

This is an owned current-base blocker handoff, not a proof receipt. Because the assigned proof phase
is not genuinely self-tested as complete, `.stage1-worker-selftest.json` is deliberately absent.
