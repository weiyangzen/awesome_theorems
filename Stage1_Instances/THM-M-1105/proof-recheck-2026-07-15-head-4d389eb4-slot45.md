# THM-M-1105 proof recheck at `4d389eb4` (slot45)

Item: `S56-M-1105-PROOF`

Intent: `prove`

Recorded: `2026-07-15T17:00:46+08:00`

Base revision: `4d389eb47e043f6f44925a418baee0d034f764ba`

Base tree: `64faabd76665273032b8cb1554b90655b5c94256`

## Verdict

`blocked`. No placeholder-free local body or dependency-legal immutable import proves the exact
canonical proposition `Stage1.THM_M_1105.WignerSemicircleLaw`. This run adds no Lean proof body,
closes no obligation, and leaves the root at `[H2, M3, R4]`. It does not satisfy the assigned proof
item or claim audit completion, theorem completion, validation, release, receipt acceptance, or
master acceptance.

The first workflow failure is dependency legality. The scheduler projection renders
`S56-M-1105-OBLIGATION_TREE` provisional `[_]`, while rev-5.6 section 10.1 says both `[ ]` and `[_]`
are unfinished; the owned task authority also has `accepted_states: []` and records the prerequisite
as `open`. Independently, all 20 machine-required obligations have
`terminal_proof_body_id: null`. The sole checked local theorem,
`Stage1.THM_M_1105.ObligationTree.root_of_sample_weak_convergence`, consumes
`terminal : forall-almost-everywhere omega, SampleWeakConvergence A hA_hermitian omega`. That
premise is the missing analytic conclusion, so the declaration is conditional composition rather
than a proof body for `M1105-T-WEAK`, `M1105-T-COMPOSE`, or `M1105-ROOT`.

There is no contradiction or vacuity route. Bounded symmetric Rademacher off-diagonal matrices with
zero diagonal have the frozen hypothesis shape, so the target requires substantive random-matrix
combinatorics and analysis.

## Failed Gates And Root Cut

After dependency reconciliation, kernel closure first fails at `M1105-L-NONPAIR`: no eligible body
proves asymptotic suppression of all surviving non-pairing and diagonal-containing walk patterns.
The graph-derived root cut is `M1105-L-NONPAIR`, `M1105-L-PAIRING`,
`M1105-L-CONCENTRATION`, `M1105-L-TIGHTNESS`, and `M1105-L-BC-APPROX`.

The complete route additionally needs normalized trace expansion, parity and closed-walk
classification, independence cancellation, Catalan enumeration, expected and almost-sure moment
convergence, semicircle moments, polynomial extension, and weak convergence. Supplying any missing
package as an assumption, bodyless declaration, axiom, `sorry`, or differently scoped theorem is a
prohibited shortcut.

Pinned mathlib has supporting spectrum, probability, integration, approximation, and convergence
APIs but no Wigner/random-matrix semicircle theorem. Repository-local exact-interface search found
no second body. The immutable candidate audit remains decisive:
`semicircle-catalan@95d99de4` supplies only finite pairing/Catalan combinatorics,
`HighDimProb@8d4eec8b` supplies infrastructure only, and
`FredRaj3/SemicircleLaw@724f9ad6` contains placeholders in its essential moment and variance
declarations and has no exact almost-sure weak terminal. None earns proof credit or can be pinned as
the required body.

## Current-Base Validation

No `lake update`, `lake build`, dependency clone/fetch, checkout repair, or `.lake` mutation was
performed. The automation-provided `.lake` symlink points to shared canonical pinned artifacts, so
these are warm nonrelease checks. The target modules elaborated through `lake env lean` at trust
level zero; this validates the exact open interfaces but closes no proof obligation.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1105` | 0 | Rank 545; lifecycle planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1105/check_obligation_tree.py` | 0 | 22 obligations and 108 typed edges passed; denominator `409c3f4a...26f0e`; root explicitly open at M3. |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-1105/Statement.lean` | 0 | Exact canonical proposition elaborated; no error output. |
| Same command for `ObligationTree.lean` | 0 | Conditional composition elaborated with its explicit terminal premise; no error output. |
| Stdin trust-zero `#print axioms` probe | 0 | Exactly `propext`, `Classical.choice`, and `Quot.sound`; the analytic terminal remains an explicit premise. |
| Token-aware prohibited-construct scan over owned `*.lean` files | 1 | Expected no-match exit; no placeholder, bodyless axiom-like declaration, unsafe/oracle path, or equivalent construct. |
| Required terminal-body count | 0 | `obligations=22 machine_required=20 with_terminal_body=0 open=20`. |
| Pinned-mathlib topical source scan | 0 | Only Thales' unrelated geometric semicircle comment; no random-matrix terminal. |
| Repository-local exact-interface scan outside this dossier | 1 | Expected no-match exit; no reusable exact proof body. |
| Proof-input diff from `50db6284` to this base | 0 | No change to the statement, composition, registry, graphs, inventory, toolchain, or Lake manifest. |

Proof-relevant SHA-256 values remain `b7e0e83c...fdf75b` (`Statement.lean`),
`922a4b40...84c0` (`ObligationTree.lean`), `f5561115...45cb` (registry),
`d3ce5de6...e42987` (typed graphs), and `eacb015c...b0d612` (anchor inventory).
Pinned identities are Lean 4.29.0 commit `98dc76e3...16740`, mathlib
`8a178386...ea95` / tree `bdc39a31...1c2b`, and `flt-regular`
`56161b6e...1a27` / tree `32c9eace...c893`. Exact hashes and the complete command ledger are in
the paired JSON artifact.

## Workflow And Retry Boundary

Before this run the owned path already contained 28 structured unresolved proof blocker/recheck
records, far beyond the five-tick split threshold, while the scheduler still says `attempts: 0` and
`children: []`. Rev-5.6 section 10.2 requires the integration lane to stop redispatching this
oversized parent, reconcile prerequisite acceptance, and split it into dependency-legal child
assignments. This worker may not edit the authoritative DAG, generated checklist, or an earlier
phase's state.

Resume only after those child assignments exist for placeholder-free implementations of the frozen
trace-moment, walk-classification, non-pairing, pairing, concentration, almost-sure moment,
semicircle-moment, tightness, polynomial-approximation, bounded-continuous approximation, and weak-
convergence packages, or after an immutable exact-scope Lean 4 terminal theorem becomes available
for pinning, exact-type transport, and provenance/trust validation without changing the target.

This is an owned current-base blocker handoff, not a proof receipt. Because the assigned proof phase
is not genuinely self-tested as complete, `.stage1-worker-selftest.json` is deliberately absent.
