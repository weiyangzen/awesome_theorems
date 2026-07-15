# THM-M-1105 proof recheck at `714fb3bb` (slot50)

Item: `S56-M-1105-PROOF`

Intent: `prove`

Recorded: `2026-07-15T13:40:14+08:00`

Base revision: `714fb3bb6a070c2f659ece069f1a7219f9c045a0`

Base tree: `2c99a78c5fa247aebc885f31e6818fc029f17a60`

## Verdict

`blocked`. No placeholder-free proof body or dependency-legal immutable import proves the exact
canonical proposition `Stage1.THM_M_1105.WignerSemicircleLaw`. This run adds no Lean proof body,
closes no obligation, and leaves the root at `[H2, M3, R4]`. It does not satisfy the assigned proof
item or claim audit completion, theorem completion, validation, release, receipt acceptance, or
master acceptance.

All 20 machine-required obligations still have `terminal_proof_body_id: null`. The only checked
local theorem, `Stage1.THM_M_1105.ObligationTree.root_of_sample_weak_convergence`, consumes
`terminal : forall-almost-everywhere omega, SampleWeakConvergence A hA_hermitian omega`. That
premise is the missing analytic conclusion, so the declaration is conditional composition rather
than a body for `M1105-T-WEAK`, `M1105-T-COMPOSE`, or `M1105-ROOT`.

There is also a prerequisite-state inconsistency that this proof-scoped worker may not silently
repair: the scheduler projection renders `S56-M-1105-OBLIGATION_TREE` provisionally complete, but
the owned `task-dag.json` has `accepted_states: []` and records that prerequisite as `open`.
Dependency legality therefore fails before proof acceptance even if a body were available.

## Failed Gate And Root Cut

The first workflow gate is the unreconciled prerequisite state. Independently, the first missing
machine package remains `M1105-L-NONPAIR`: no eligible body proves asymptotic suppression of all
surviving non-pairing and diagonal-containing walk patterns for the frozen bounded triangular
array. The graph-derived root cut is `M1105-L-NONPAIR`, `M1105-L-PAIRING`,
`M1105-L-CONCENTRATION`, `M1105-L-TIGHTNESS`, and `M1105-L-BC-APPROX`.

Closing the target also requires normalized trace expansion, parity and closed-walk
classification, independence cancellation, Catalan enumeration, expected and almost-sure moment
convergence, semicircle moments, polynomial extension, and final weak convergence. Supplying any
package as an assumption, bodyless declaration, axiom, `sorry`, or differently scoped theorem
would be a prohibited shortcut.

Pinned mathlib has supporting spectrum, trace, probability, integration, tightness,
approximation, and convergence APIs, but no Wigner/random-matrix semicircle theorem. Repository
sources contain no exact body. The frozen candidate audit remains decisive:
`semicircle-catalan@95d99de4` supplies finite combinatorics only, `HighDimProb@8d4eec8b` supplies
infrastructure only, and `FredRaj3/SemicircleLaw@724f9ad6` contains placeholders and proves neither
this ensemble nor its almost-sure weak terminal. None earns proof credit.

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
| `python3 scripts/stage1_target.py show THM-M-1105` | 0 | Rank 545; planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1105/check_obligation_tree.py` | 0 | 22 obligations and 108 typed edges passed; denominator `409c3f4a...26f0e`; root explicitly open at M3. |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-1105/Statement.lean` | 1 | Lake stopped before target elaboration because `.lake/packages/flt-regular` could not resolve `HEAD`. |
| Same root-Lake command for `ObligationTree.lean` | 1 | Same shared-artifact blocker; no target diagnostic was reached. |
| Direct pinned Lean plus existing package build paths, `--trust=0 -t0`, on `Statement.lean` | 0 | Exact canonical proposition elaborated; only five expected unused-hypothesis warnings. |
| Same direct pinned-Lean check of `ObligationTree.lean` | 0 | Conditional composition elaborated with its explicit terminal premise; only five expected warnings. |
| Temporary trust-zero `#print axioms` probe | 0 | Exactly `propext`, `Classical.choice`, and `Quot.sound`; the analytic terminal remains an explicit unproved premise. |
| Token-aware prohibited-construct scan over owned `*.lean` files | 1 | Expected no-match exit; no placeholder, bodyless axiom-like declaration, unsafe/oracle path, or equivalent construct. |
| Required terminal-body count | 0 | `required=20`, `with_terminal_body=0`, `open=20`. |
| Pinned-mathlib topical source scan | 0 | Only Thales' unrelated geometric semicircle comment; no random-matrix terminal. |
| Repository-local exact-interface scan outside this dossier | 1 | Expected no-match exit; no reusable exact proof body. |
| Proof-input diff from integrated recheck base `cc8afe07` to this base | 0 | No change to statement, composition, registry, graphs, inventory, toolchain, or Lake manifest. |

Proof-relevant hashes remain `b7e0e83c...fdf75b` (`Statement.lean`),
`922a4b40...84c0` (`ObligationTree.lean`), `f5561115...45cb` (registry),
`d3ce5de6...e42987` (typed graphs), and `eacb015c...b0d612` (anchor inventory).
Pinned identities are Lean 4.29.0 commit `98dc76e3...16740` and mathlib
`8a178386...ea95` / tree `bdc39a31...1c2b`. Exact commands and hashes are in the paired JSON
artifact.

## Workflow And Retry Boundary

Before this run the owned path already contained 18 structured unresolved proof blocker/recheck
records, while the scheduler projection still says `attempts: 0` and `children: []`. Section 10.2
requires an item split after five unresolved execution ticks. The worker may not edit the
authoritative DAG, repair prerequisite acceptance, or invent unassigned children.

The integration lane must first reconcile `S56-M-1105-OBLIGATION_TREE` state and split
`S56-M-1105-PROOF` into dependency-legal child assignments. Resume proof credit only with
placeholder-free implementations of the frozen proof packages, or with an immutable exact-scope
Lean 4 terminal theorem that can be pinned, exact-type transported, and provenance/trust checked
without changing the target.

This is an owned current-base blocker handoff, not a proof receipt. Because the assigned proof
phase is not genuinely self-tested as complete, `.stage1-worker-selftest.json` is deliberately
absent.
