# THM-M-1105 proof-phase recheck at base `7bc16474`

Item: `S56-M-1105-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `7bc16474ba6a97ad369a618990b1ffbec170db3c`

Base tree: `d911a4fe236f270edbd1521a474442e0de79c6b3`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact target
`Stage1.THM_M_1105.WignerSemicircleLaw`. All 20 machine-required obligations still have
`terminal_proof_body_id: null`, the closed-obligation set is empty, and the root remains open at
`[H2, M3, R4]`. No theorem was weakened or substituted, and no graph, composition certificate,
debt vector, or scheduler state was changed.

The only checked local theorem,
`Stage1.THM_M_1105.ObligationTree.root_of_sample_weak_convergence`, is conditional composition. Its
`terminal` binder assumes almost-everywhere `SampleWeakConvergence`, the missing analytic
conclusion. It therefore closes neither `M1105-T-WEAK`, `M1105-T-COMPOSE`, nor the root. A
trust-zero axiom probe reports only `propext`, `Classical.choice`, and `Quot.sound`, but an accepted
foundation profile cannot turn an explicit unproved premise into a proof body.

The graph-derived minimal root cut remains `M1105-L-NONPAIR`, `M1105-L-PAIRING`,
`M1105-L-CONCENTRATION`, `M1105-L-TIGHTNESS`, and `M1105-L-BC-APPROX`. The complete route also
requires trace expansion, parity and walk classification, independence cancellation, Catalan
enumeration, expected and almost-sure moment convergence, semicircle moments, polynomial extension,
and final weak convergence. Supplying any missing package as an axiom, assumed terminal, or
bodyless declaration would be a prohibited placeholder.

A focused truth audit found no shortcut by contradiction and no missing hypothesis that makes the
target false. Cross-dimension independence is unnecessary for first Borel-Cantelli after summable
per-dimension concentration. The single deterministic entry bound can be intersected over the
countable matrix-coordinate family to obtain one common full-measure set. Uniformly bounded
diagonal entries are lower order after square-root scaling, and pathwise weak convergence yields
all bounded continuous tests simultaneously. These observations preserve plausibility; they are
not Lean proof bodies and do not clear the still-open primary-source fidelity audit.

## Candidate Recheck

Pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` still contains only supporting
Hermitian-spectrum, trace, independence, integration, and weak-convergence APIs. A source-wide
topical scan found no Wigner or random-matrix semicircle theorem.

Read-only GitHub metadata searches on the recheck date returned only the two previously audited
semicircle repositories. `FredRaj3/SemicircleLaw` remains at
`724f9ad681a2da6ffe6be02fc3e11a38c4b1b701`; the immutable audit found 25 `sorry` tokens, no
terminal weak or almost-sure empirical spectral convergence theorem, and a different ensemble and
convergence mode. `Wondermonger-daydreaming/semicircle-catalan` remains at
`95d99de4490a50af6d909f27e670a82691d6c4e8` and supplies only finite Catalan/genus-zero
combinatorics.

`dududuguo/HighDimProb` advanced from the audited revision `8d4eec8b` to
`5c548a41f803135eb39d4e9161f8ac7a4dd5f3c5`. The three intervening commits add or reorganize
matrix-concentration and centered-rank-one APIs; its current tree still exposes no Wigner,
semicircle, empirical-spectral, or eigenvalue-distribution theorem. A scan of its 299 Lean files
found no prohibited proof token. This remains useful infrastructure, not an exact proof candidate.
Candidate archives were inspected only under `/tmp`; no external project was installed, built,
cloned into the project, fetched into `.lake`, or granted proof credit.

## Validation

All Lean checks reused the automation-provided canonical pinned artifacts read-only. Temporary
axiom-probe outputs were created under `/tmp` and removed. No `lake update`, `lake build`, dependency
clone/fetch, or `.lake` mutation was performed. The pre-existing untracked
`Formalizations/Lean/.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1,546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1105` | 0 | rank 545; planned; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1105/check_obligation_tree.py` | 0 | 22 obligations and 108 typed edges passed; denominator `409c3f4a...26f0e`; root open at M3 |
| `(cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-1105/Statement.lean)` | 0 | exact canonical proposition elaborated; only expected unused-hypothesis linter warnings |
| corresponding trust-zero check of `ObligationTree.lean` | 0 | conditional terminal-to-root composition elaborated; only expected unused-hypothesis linter warnings |
| isolated copy of `ObligationTree.lean` with `#print axioms` | 0 | composition reports `[propext, Classical.choice, Quot.sound]`; temporary files removed |
| prohibited-construct scan over owned `*.lean` files | 1 | expected no-match exit; no `sorry`, axiom, unsafe/oracle, opaque, external, or implemented body found |
| pinned-mathlib Wigner/semicircle source scan | 0 | only Thales' unrelated geometric semicircle comment; no random-matrix theorem |
| read-only GitHub repository and immutable-revision metadata checks | 0 | no new exact candidate; bounded search limitations recorded in the JSON handoff |

Proof-relevant SHA-256 values remain `b7e0e83c...fdf75b` for `Statement.lean`,
`922a4b40...84c0` for `ObligationTree.lean`, `f5561115...45cb` for the registry,
`d3ce5de6...2987` for the typed graphs, and `eacb015c...0d612` for the anchor inventory. The pinned
Lake manifest and toolchain hashes are `321626c8...2d81` and `651c8acc...b1d2`.

## Retry Condition

Resume after placeholder-free implementations of the frozen trace-moment, walk-classification,
non-pairing, pairing, concentration, almost-sure moment, semicircle-moment, tightness, approximation,
and weak-convergence packages. An alternative is an immutable exact-scope Lean 4 theorem that can
be dependency-legally pinned, exact-type transported, and provenance/trust validated without
changing the frozen target.

This current-base record is an owned nonrelease blocker handoff, not a proof receipt. It does not
satisfy `S56-M-1105-PROOF`, propose scheduler state promotion, or support audit completion, theorem
completion, validation, release, or master acceptance. Because the proof phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` is deliberately absent.
