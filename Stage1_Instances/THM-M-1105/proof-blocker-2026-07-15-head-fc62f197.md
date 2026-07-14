# THM-M-1105 proof blocker at base `fc62f197`

Item: `S56-M-1105-PROOF`

Recorded: `2026-07-15T06:27:34+08:00`

Base revision: `fc62f197cafb456a785e618910f899d65a2d242a`

Base tree: `0d94e5d2e32c93ebf96e3d3d6f78d317232b8bfa`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact canonical target
`Stage1.THM_M_1105.WignerSemicircleLaw`. All 20 machine-required obligations still have
`terminal_proof_body_id: null`, the closed-obligation set is empty, and the exact root remains open
at `[H2, M3, R4]`. No theorem was weakened or substituted, no axiom or placeholder was introduced,
and no graph, debt vector, composition certificate, or scheduler state was changed.

The only checked local theorem,
`Stage1.THM_M_1105.ObligationTree.root_of_sample_weak_convergence`, is conditional composition. Its
`terminal` binder assumes almost-everywhere `SampleWeakConvergence`, the missing analytic
conclusion. The declaration therefore closes neither `M1105-T-WEAK`, `M1105-T-COMPOSE`, nor the
root. A trust-zero stdin audit reports only `propext`, `Classical.choice`, and `Quot.sound`; this
accepted foundation profile does not turn the explicit terminal premise into a proof body.

## First Failed Gate

The first failed machine gate is `M1105-L-NONPAIR`: no placeholder-free repo-local, pinned-mathlib,
or immutable exact-scope body proves asymptotic suppression of all surviving non-pairing and
diagonal-containing walk patterns for the frozen bounded triangular array. Every machine-required
terminal proof-body field is still null.

The graph-derived root cut remains `M1105-L-NONPAIR`, `M1105-L-PAIRING`,
`M1105-L-CONCENTRATION`, `M1105-L-TIGHTNESS`, and `M1105-L-BC-APPROX`. The complete route also
requires normalized trace expansion, parity and walk classification, independence cancellation,
Catalan enumeration, expected and almost-sure moment convergence, semicircle moments, polynomial
extension, and final weak convergence. Adding any package as an assumed terminal, bodyless
declaration, axiom, or `sorry` would be a prohibited placeholder.

## Candidate Boundary

Pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` still supplies only supporting
Hermitian-spectrum, trace, independence, integration, and weak-convergence APIs. The scoped topical
scan found no Wigner or random-matrix semicircle terminal. Reachable Git history has no hidden or
superseded proof body, and since the preceding current-day audit the only target additions were
blocker records; no proof-relevant Lean source changed.

The preceding immutable current-day audits remain decisive for the known external candidates.
`Wondermonger-daydreaming/semicircle-catalan@95d99de4` covers only finite Catalan/genus-zero
combinatorics. `dududuguo/HighDimProb@5c548a41` supplies concentration infrastructure but no exact
spectral-limit theorem. `FredRaj3/SemicircleLaw@724f9ad6` contains 25 `sorry` tokens, lacks a weak
or almost-sure empirical-spectral terminal, and targets a different ensemble and convergence mode.
No candidate is in the pinned dependency closure or earns proof credit. This recheck used no
network and made no `.lake` change.

## Validation

All Lean checks reused the automation-provided canonical pinned artifacts read-only. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. The
pre-existing untracked `Formalizations/Lean/.lake` symlink makes this warm, nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1,546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1105` | 0 | rank 545; planned; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1105/check_obligation_tree.py` | 0 | 22 obligations and 108 typed edges passed; denominator `409c3f4a...26f0e`; root open at M3 |
| `(cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-1105/Statement.lean)` | 0 | exact canonical proposition elaborated; only expected unused-hypothesis linter warnings |
| corresponding trust-zero check of `ObligationTree.lean` | 0 | conditional terminal-to-root composition elaborated, including its explicit terminal premise; only expected unused-hypothesis linter warnings |
| trust-zero stdin `#print axioms` check of the composition | 0 | `propext`, `Classical.choice`, and `Quot.sound`; no source/build artifact written |
| prohibited-construct scan over owned `*.lean` files | 1 | expected no-match exit; no `sorry`, axiom, unsafe/oracle, opaque, external, or implemented body found |
| pinned-mathlib Wigner/semicircle source scan | 0 | only Thales' unrelated geometric semicircle comment; no random-matrix theorem |
| reachable Git-history/object scan for target proof sources | 0 | only the statement, anchor audit, and conditional obligation-tree module; no prior proof body |
| JSON parse loop over all owned `*.json` files | 0 | every JSON artifact, including this blocker, parsed |
| trailing-whitespace scan over both new blocker artifacts | 1 | expected no-match exit; neither file has trailing whitespace |
| `git diff --check -- Stage1_Instances/THM-M-1105 .stage1-worker-selftest.json` | 0 | no whitespace errors in the owned change |
| toolchain and mathlib identity checks | 0 | Lean 4.29.0, Lake 5.0.0, mathlib `8a178386...ea95` / tree `bdc39a31...1c2b` |

Proof-relevant SHA-256 values remain `b7e0e83c...fdf75b` for `Statement.lean`,
`922a4b40...84c0` for `ObligationTree.lean`, `f5561115...45cb` for the registry,
`d3ce5de6...2987` for the typed graphs, and `eacb015c...0d612` for the anchor inventory. The pinned
Lake manifest and toolchain hashes are `321626c8...2d81` and `651c8acc...b1d2`.

## Retry Condition

Resume after placeholder-free implementations of the frozen trace-moment, walk-classification,
non-pairing, pairing, concentration, almost-sure moment, semicircle-moment, tightness,
polynomial-approximation, bounded-continuous approximation, and weak-convergence packages. The only
alternative is an immutable exact-scope Lean 4 terminal theorem that can be dependency-legally
pinned, exact-type transported, and provenance/trust validated without changing the frozen target.

This current-base record is an owned nonrelease blocker handoff, not a proof receipt. It does not
satisfy `S56-M-1105-PROOF`, propose scheduler state promotion, or support audit completion, theorem
completion, validation, release, or master acceptance. Because the assigned proof phase is not
genuinely self-tested as complete, `.stage1-worker-selftest.json` is deliberately absent.
