# THM-M-1105 proof blocker at base `a9230a2f`

Item: `S56-M-1105-PROOF`

Recorded: `2026-07-15T08:07:48+08:00`

Base revision: `a9230a2f2eeabee7e39c0a3deb08e27174d17575`

Base tree: `ab8a17b9aa773ce0b8305338f2ca0c66974c1bb6`

## Verdict

`blocked`. No eligible placeholder-free proof body or pinned theorem closes the exact canonical
target `Stage1.THM_M_1105.WignerSemicircleLaw`. The frozen registry has 20 machine-required
obligations; every `terminal_proof_body_id` remains null, the closed-obligation set is empty, and
the exact root remains open at `[H2, M3, R4]`. No theorem was weakened or substituted, no axiom or
placeholder was introduced, and no graph, debt vector, composition certificate, or scheduler state
was changed.

The target has no contradiction shortcut. Bounded symmetric Rademacher off-diagonal entries with
zero diagonal give a consistent model of its hypotheses. The checked local theorem
`Stage1.THM_M_1105.ObligationTree.root_of_sample_weak_convergence` is conditional composition only:
its `terminal` binder assumes almost-everywhere `SampleWeakConvergence`, the missing analytic
conclusion. It therefore closes neither `M1105-T-WEAK`, `M1105-T-COMPOSE`, nor the root.

## First Failed Gate

The first failed machine gate is `M1105-L-NONPAIR`: no placeholder-free repo-local,
pinned-mathlib, or immutable exact-scope body proves asymptotic suppression of all surviving
non-pairing and diagonal-containing walk patterns for the frozen bounded triangular array.

The graph-derived root cut remains `M1105-L-NONPAIR`, `M1105-L-PAIRING`,
`M1105-L-CONCENTRATION`, `M1105-L-TIGHTNESS`, and `M1105-L-BC-APPROX`. The complete missing route
also requires normalized trace expansion, parity and walk classification, independence
cancellation, Catalan enumeration, expected and almost-sure moment convergence, semicircle
moments, polynomial extension, and final weak convergence. Supplying any package as an assumed
terminal, bodyless declaration, axiom, or `sorry` would be a prohibited placeholder.

## Candidate Boundary

Pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` provides supporting spectrum, trace,
independent-integral, Borel-Cantelli, tightness, polynomial-approximation, and weak-convergence APIs,
but no Wigner or random-matrix semicircle theorem. Its source-wide topical scan still finds only
the unrelated geometric use of "semicircle" in Thales' theorem.

The immutable candidate audits remain decisive. `semicircle-catalan@95d99de4` supplies only finite
Catalan/genus-zero combinatorics. `HighDimProb@5c548a41` supplies concentration infrastructure but
no empirical spectral limit. `FredRaj3/SemicircleLaw@724f9ad6` has 25 `sorry` occurrences in the
missing random-matrix packages, no weak or almost-sure terminal theorem, a different ensemble and
convergence mode, and incompatible dependency pins. None is in the pinned local closure or earns
proof credit. This recheck used no network and made no `.lake` change.

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
| `(cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-1105/Statement.lean)` | 0 | exact canonical proposition elaborated; only five expected unused-binder linter warnings |
| `(cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-1105/ObligationTree.lean)` | 0 | conditional composition elaborated; only five expected unused-binder linter warnings; its source retains the explicit terminal premise |
| `rg -n --pcre2 '\b(?:sorry\|admit\|sorryAx\|native_decide\|implemented_by\|run_tac)\b\|^[[:space:]]*(?:axiom\|unsafe\|extern\|external\|opaque\|constant)\b' Stage1_Instances/THM-M-1105 --glob '*.lean'; test $? -eq 1` | 0 | the scan returned the expected no-match exit 1 and the assertion passed; no prohibited construct occurs |
| `rg -n -i 'wigner\|semicircle\|semi.?circle\|empirical[ _-]?spectral\|random[ _-]?matri' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | only Thales' unrelated geometric semicircle comment; no random-matrix theorem |
| `jq -r '[.obligations[] \| select(.machine_eligibility == "required")] as $r \| "required=\($r\|length) closed=\([$r[]\|select(.terminal_proof_body_id != null)]\|length) open=\([$r[]\|select(.terminal_proof_body_id == null)]\|length)"' Stage1_Instances/THM-M-1105/obligation-registry.json` | 0 | `required=20 closed=0 open=20` |
| `git diff --exit-code 557b928b377b386864527c9fb4831d45857837aa HEAD -- Stage1_Instances/THM-M-1105/Statement.lean Stage1_Instances/THM-M-1105/ObligationTree.lean Stage1_Instances/THM-M-1105/obligation-registry.json Stage1_Instances/THM-M-1105/typed-graphs.json Stage1_Instances/THM-M-1105/anchor-inventory.json Formalizations/Lean/lake-manifest.json Formalizations/Lean/lean-toolchain` | 0 | no output; proof-relevant target and environment inputs are unchanged |
| toolchain and mathlib identity checks | 0 | Lean 4.29.0, Lake 5.0.0, mathlib `8a178386...ea95` / tree `bdc39a31...1c2b` |
| `python3 -m json.tool Stage1_Instances/THM-M-1105/proof-blocker-2026-07-15-head-a9230a2f.json` | 0 | structured blocker record is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1105 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

Proof-relevant SHA-256 values remain `b7e0e83c...fdf75b` for `Statement.lean`,
`922a4b40...84c0` for `ObligationTree.lean`, `f5561115...45cb` for the registry,
`d3ce5de6...2987` for the typed graphs, and `eacb015c...0d612` for the anchor inventory. The pinned
Lake manifest and toolchain hashes remain `321626c8...2d81` and `651c8acc...b1d2`.

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
