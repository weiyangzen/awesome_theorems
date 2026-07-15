# THM-M-1105 proof recheck at `443b8bbc` (slot58)

Item: `S56-M-1105-PROOF`

Intent: `prove`

Recorded: `2026-07-15T11:46:50+08:00`

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

## Verdict

`blocked`. No placeholder-free proof body exists in the owned sources, the scoped repository
history, or the pinned mathlib closure for the exact canonical proposition
`Stage1.THM_M_1105.WignerSemicircleLaw`. This run adds no Lean proof body, closes no obligation,
and leaves the root at `[H2, M3, R4]`. It does not satisfy the proof item or claim audit
completion, theorem completion, validation, release, receipt acceptance, or master acceptance.

The frozen registry still has 22 obligations, of which 20 are machine-required. Every required
`terminal_proof_body_id` is null and the typed closure set is empty. The only checked theorem,
`Stage1.THM_M_1105.ObligationTree.root_of_sample_weak_convergence`, consumes
`terminal : forall-almost-everywhere omega, SampleWeakConvergence A hA_hermitian omega`. That
premise is the missing analytic conclusion, so the declaration is conditional composition rather
than a proof of `M1105-T-WEAK`, `M1105-T-COMPOSE`, or the root.

There is no vacuity shortcut. The hypotheses are consistent (a product-space symmetric
Rademacher construction with zero diagonal is a standard witness shape); independence across
matrix sizes is unnecessary for the summable-deviation/Borel-Cantelli route, and the common
almost-everywhere test-function conclusion is ordinary pathwise weak convergence.

## Failed Gate And Root Cut

The first failed machine gate remains `M1105-L-NONPAIR`: there is no eligible body proving
asymptotic suppression of all surviving non-pairing and diagonal-containing walk patterns for the
frozen bounded triangular array. The graph-derived root cut is `M1105-L-NONPAIR`,
`M1105-L-PAIRING`, `M1105-L-CONCENTRATION`, `M1105-L-TIGHTNESS`, and
`M1105-L-BC-APPROX`.

Closing the exact target also requires normalized trace expansion, parity and closed-walk
classification, independence cancellation, Catalan enumeration, expected and almost-sure moment
convergence, semicircle moments, polynomial extension, and final weak convergence. Supplying any
of those packages as an assumption, bodyless declaration, axiom, `sorry`, or differently scoped
theorem would be a prohibited shortcut.

Pinned mathlib provides supporting spectrum, trace, independence, integration, and convergence
interfaces but no Wigner/random-matrix semicircle theorem. The immutable candidate audit remains
decisive: `semicircle-catalan@95d99de4` is finite combinatorics only,
`HighDimProb@5c548a41` is infrastructure only, and
`FredRaj3/SemicircleLaw@724f9ad6` has 25 `sorry` occurrences and a different ensemble and
convergence mode. None supplies an eligible terminal body.

## Current-Base Validation

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. The
automation-provided `.lake` symlink points to shared canonical artifacts and makes this warm,
nonrelease evidence. During this run the shared `flt-regular` checkout had
`HEAD -> refs/heads/.invalid`, so the prescribed root `lake env lean` commands stopped before
elaboration. The pinned commit object still exists, but worker policy forbids repairing or
mutating `.lake`.

To obtain the smallest real kernel check without changing dependencies, the same pinned Lean
4.29.0 binary was invoked directly with `LEAN_PATH` assembled only from the existing canonical
package build directories, excluding the broken and target-irrelevant `flt-regular` checkout.
Both owned modules elaborated at trust level zero. This fallback is explicitly nonrelease evidence;
it does not replace the later validation or hermetic release gates.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1105` | 0 | Rank 545; planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1105/check_obligation_tree.py` | 0 | 22 obligations and 108 typed edges passed; denominator `409c3f4a...26f0e`; root explicitly open at M3. |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-1105/Statement.lean` | 1 | Lake stopped before elaboration because `.lake/packages/flt-regular` could not resolve `HEAD`. |
| Same root-Lake command for `ObligationTree.lean` | 1 | Same shared-artifact blocker; no target diagnostic was reached. |
| Pinned `lean` 4.29.0 plus an existing-package `LEAN_PATH`, `--trust=0 -t0`, on `Statement.lean` | 0 | The exact canonical proposition elaborated; only five expected unused-hypothesis linter warnings were emitted. |
| Same direct pinned-Lean check of `ObligationTree.lean` | 0 | The conditional terminal-to-root composition elaborated; only five expected unused-hypothesis linter warnings were emitted. |
| Stdin trust-zero `#print axioms` probe using the same pinned environment | 0 | Exactly `propext`, `Classical.choice`, and `Quot.sound`; the explicit terminal premise remains open. |
| Token-aware prohibited-construct scan over owned `*.lean` files | 1 | Expected no-match exit; no placeholder, bodyless axiom-like declaration, unsafe/oracle path, or equivalent construct was found. |
| Pinned-mathlib topical source scan | 0 | The only match was Thales' unrelated geometric semicircle comment. |
| Repository-local exact-interface scan outside this dossier | 1 | Expected no-match exit; no reusable exact proof body was found. |

The source hashes remain `b7e0e83c...fdf75b` (`Statement.lean`),
`922a4b40...84c0` (`ObligationTree.lean`), `f5561115...45cb` (registry),
`d3ce5de6...e42987` (typed graphs), and `eacb015c...b0d612` (anchor inventory).
Proof-relevant inputs are unchanged from the original proof execution at `270e3fb3` and the prior
recheck at `a23d86cd`.

## Workflow And Retry Boundary

The owned path now contains more than five unresolved proof-run records while the authoritative
scheduler projection still reports `attempts: 0` and `children: []`. Section 10.2 requires an
oversized item to be split after five unresolved ticks. This worker may neither edit the scheduler
DAG nor invent unassigned children, so the integration lane must reconcile and split the proof
work before dispatching it again.

Resume only with dependency-legal child assignments for placeholder-free implementations of the
frozen proof packages, or with an immutable exact-scope Lean 4 terminal theorem that can be pinned,
exact-type transported, and provenance/trust checked without changing the target.

This is an owned current-base blocker handoff, not a proof receipt. Because the assigned phase is
not genuinely self-tested as complete, `.stage1-worker-selftest.json` is deliberately absent.
