# THM-M-1105 proof recheck at `c74f595e` (slot52)

Item: `S56-M-1105-PROOF`

Intent: `prove`

Recorded: `2026-07-15T12:11:51+08:00`

Base revision: `c74f595e99fe574f4619307c859ec20986bb2297`

Base tree: `b27451453ff7d1e87d296c6634bd270799c666d9`

## Verdict

`blocked`. No placeholder-free proof body exists in the owned sources, reachable repository
history, or pinned mathlib closure for the exact canonical proposition
`Stage1.THM_M_1105.WignerSemicircleLaw`. This run adds no Lean proof body, closes no obligation,
and leaves the root at `[H2, M3, R4]`. It does not satisfy the proof item or claim audit
completion, theorem completion, validation, release, receipt acceptance, or master acceptance.

The frozen registry still has 22 obligations, of which 20 are machine-required. Every required
`terminal_proof_body_id` is null. The only checked theorem,
`Stage1.THM_M_1105.ObligationTree.root_of_sample_weak_convergence`, consumes
`terminal : forall-almost-everywhere omega, SampleWeakConvergence A hA_hermitian omega`. That
premise is the missing analytic conclusion, so the declaration is conditional composition rather
than a proof of `M1105-T-WEAK`, `M1105-T-COMPOSE`, or the root.

No contradiction or vacuity shortcut was found. Independent symmetric Rademacher upper-triangular
off-diagonal entries with zero diagonal give the standard consistency witness shape, and the outer
almost-everywhere quantifier expresses ordinary pathwise weak convergence. Cross-dimension
independence is not needed for a summable-deviation plus first-Borel-Cantelli route.

## Failed Gate And Root Cut

The first failed machine gate remains `M1105-L-NONPAIR`: there is no eligible body proving
asymptotic suppression of all surviving non-pairing and diagonal-containing walk patterns for the
frozen bounded triangular array. The graph-derived root cut is `M1105-L-NONPAIR`,
`M1105-L-PAIRING`, `M1105-L-CONCENTRATION`, `M1105-L-TIGHTNESS`, and
`M1105-L-BC-APPROX`.

Closing the target also requires normalized trace expansion, parity and closed-walk
classification, independence cancellation, Catalan enumeration, expected and almost-sure moment
convergence, semicircle moments, polynomial extension, and final weak convergence. Supplying any
package as an assumption, bodyless declaration, axiom, `sorry`, or differently scoped theorem
would be a prohibited shortcut.

Pinned mathlib provides spectrum, trace, independent-integral, Borel-Cantelli, tightness,
Weierstrass-approximation, and weak-convergence interfaces, but no Wigner/random-matrix semicircle
theorem. The immutable candidates remain ineligible: `semicircle-catalan@95d99de4` is finite
combinatorics only, `HighDimProb@5c548a41` is infrastructure only, and
`FredRaj3/SemicircleLaw@724f9ad6` has 25 `sorry` occurrences and a different ensemble and
convergence mode.

## Current-Base Validation

No `lake update`, `lake build`, dependency clone/fetch, checkout repair, or `.lake` mutation was
performed. The automation-provided `.lake` symlink points to shared canonical artifacts, so these
checks are warm nonrelease evidence.

The prescribed `lake env lean` checks stopped before usable target elaboration because the shared
`flt-regular` checkout has no resolvable `HEAD`. Its pinned commit object exists, but worker policy
forbids repairing or mutating `.lake`. The same pinned Lean 4.29.0 binary was therefore invoked
directly with `LEAN_PATH` assembled only from existing package build directories and excluding the
target-irrelevant broken checkout. Both target modules elaborated at trust level zero.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1105` | 0 | Rank 545; planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1105/check_obligation_tree.py` | 0 | 22 obligations and 108 typed edges passed; denominator `409c3f4a...26f0e`; root explicitly open at M3. |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-1105/Statement.lean` | 1 | Lake stopped before target elaboration because `.lake/packages/flt-regular` could not resolve `HEAD`. |
| Same root-Lake command for `ObligationTree.lean` | 1 | The shared dependency defect prevented usable target elaboration. |
| Pinned `lean` 4.29.0 plus existing-package `LEAN_PATH`, `--trust=0 -t0`, on `Statement.lean` | 0 | Exact proposition elaborated; only five expected unused-hypothesis warnings. |
| Same direct pinned-Lean check of `ObligationTree.lean` | 0 | Conditional composition elaborated with its explicit terminal premise; only five expected unused-hypothesis warnings. |
| Token-aware prohibited-construct scan over owned `*.lean` files | 1 | Expected no-match exit; no placeholder, bodyless axiom-like declaration, unsafe/oracle path, or equivalent construct. |
| Required terminal-body count | 0 | `required=20 closed=0 open=20`. |
| Pinned-mathlib topical source scan | 0 | Only Thales' unrelated geometric semicircle comment; no random-matrix terminal. |
| Repository-local exact-interface scan outside this dossier | 1 | Expected no-match exit; no reusable exact proof body. |
| Proof-relevant diff from `443b8bbc` | 0 | Statement, composition, registry, graphs, inventory, manifest, and toolchain are unchanged. |
| JSON parse and blocker-invariant check | 0 | Identity, base/tree, source hashes, 20 open required bodies, fail-closed state, and self-test absence agree. |
| `git diff --check -- Stage1_Instances/THM-M-1105 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

Lean is version `4.29.0` at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`;
Lake is `5.0.0-src+98dc76e`; mathlib is `8a178386...ea95`, tree
`bdc39a31...1c2b`. Exact hashes and the complete command ledger are in the paired JSON artifact.

## Workflow And Retry Boundary

The owned path contained 13 unresolved proof-run records before this run while the authoritative
scheduler projection still reports `attempts: 0` and `children: []`. Rev-5.6 section 10.2 requires
an oversized item to be split after five unresolved ticks. This worker may neither edit the
scheduler DAG nor invent unassigned children, so the integration lane must reconcile and split the
proof work before dispatching it again.

Resume only with dependency-legal child assignments for placeholder-free implementations of the
frozen proof packages, or with an immutable exact-scope Lean 4 terminal theorem that can be pinned,
exact-type transported, and provenance/trust checked without changing the target.

This is an owned current-base blocker handoff, not a proof receipt. Because the assigned phase is
not genuinely self-tested as complete, `.stage1-worker-selftest.json` is deliberately absent.
