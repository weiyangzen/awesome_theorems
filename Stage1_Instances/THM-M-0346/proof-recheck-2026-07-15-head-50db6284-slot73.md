# THM-M-0346 proof recheck at current base

Item: `S56-M-0346-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T16:59:18+08:00`

Base revision: `50db6284742415b7da294d323c820bf4b224711d`

Base tree: `bb477aa021efaf69c84ee3a98f486f4ba407bae2`

## Verdict

`blocked`. The assigned proof phase remains `[ ]`; no completion self-test is issued.

The exact target is `Stage1.THM_M_0346.CarlesonTarget`: every complex `L^2` function on the
period-one additive circle has its inclusive symmetric Fourier partial sums converge to its
canonical `Lp` representative almost everywhere. The existing `Proof.lean` remains genuine,
placeholder-free partial progress. A trust-zero replay checks its representative certificate,
period and exponent facts, dossier-local cutoff equality, upstream-shaped specialization adapter,
and conditional almost-everywhere composition.

This does not prove `RawCarlesonHunt`. In particular,
`carlesonTarget_of_rawCarlesonHunt : RawCarlesonHunt -> CarlesonTarget` is conditional, and the
actual external `partialFourierSum'` is not imported. Treating that premise as proved, or replacing
the target with mathlib's `L2`-topology convergence theorem, would not close the frozen theorem.

The first failed gate is `M0346-L-CARLESON-HUNT`. The pinned package closure has no Carleson
package, `carleson_hunt`, `partialFourierSum'`, or compiled Carleson-Hunt artifact. Pinned mathlib's
`hasSum_fourier_series_L2` proves convergence in `Lp`, not pointwise or almost-everywhere
convergence. Its pointwise theorem instead assumes a continuous function with summable Fourier
coefficients.

The audited external history still supplies no compatible proof body. The only Lean `v4.29.0`
revision, `306ae5b29300771aece1aa39f0a939183cc59486`, pins mathlib
`f1a99cc3d4b62bff01325ac228882baadea934af` and defines `carleson_hunt := sorry`. The
source-complete body at `d422163115553c400bb93b6b3b0d50313b7a9f25` (identical relevant source
at the already audited `80e151dff5ddce2426079ec6392616496a4ec927`) requires Lean
`v4.30.0-rc2` and mathlib `1a4917a18b30ea1333c195e597067fe044ac9176`, while this repository is
pinned to Lean `v4.29.0` and mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The newer mathlib Git object exists locally, but no
checked-out source/build or matching cache exists; compiling it would construct an alternate
dependency closure, which is not allowed worker validation.

A source-level import traversal from the source-complete `CarlesonHunt.lean` reaches 117 Carleson
modules and five active `sorry` terms, including three in
`RealInterpolation/LorentzInterpolation.lean` and one each in `NoAtoms.lean` and
`Rearrangement.lean`. This scan does not establish whether `carleson_hunt`'s declaration body
depends on those constants; only an imported `#print axioms carleson_hunt` and terminal-body audit
could do that. It does establish that vendoring the import closure would not meet the
placeholder-free gate without further proof work.

## Narrow evidence

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused read-only. Temporary
Lean objects were written under `/tmp` and removed. No `lake update`, `lake build`, dependency
clone/fetch, network request, source import, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1,546 unique ordered targets and ranks passed. |
| `python3 scripts/stage1_target.py show THM-M-0346` | 0 | Rank 839; lifecycle planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0346/check_obligation_tree.py` | 0 | Eleven obligations and 24 typed edges passed; denominator `1ff60884ffc043439ab5a7b812bc9f2e8133e9d1eb8d130330d43f2709439c8c5`; root open at M3. |
| `cd Formalizations/Lean && timeout 240 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0346/Statement.lean` | 0 | The exact target elaborated under the pinned project environment. |
| Isolated replay of copied `Statement.lean` and `Proof.lean` with the Lean binary and package paths obtained through existing `lake env`, using `--trust=0 -t0` | 0 | The exact target and all six local declarations elaborated; each was sorry-free and reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| `rg -n --pcre2 '(?m)^\s*(?:axiom\|constant\|opaque)\b\|\b(?:sorry\|admit\|sorryAx\|unsafe\|extern\|implemented_by\|native_decide)\b' Stage1_Instances/THM-M-0346/{Statement,Proof,ObligationTree}.lean` | 1 | Expected no-match exit; no prohibited mechanism occurs in the owned Lean sources. |
| `find -L Formalizations/Lean/.lake/packages -maxdepth 1 -mindepth 1 -type d -printf '%f\\n' \| sort \| rg -i '^carleson$'` | 1 | Expected no-match exit; no pinned Carleson package exists. |
| `rg -n --glob '*.lean' 'theorem\s+carleson_hunt\b\|def\s+partialFourierSum.' Formalizations/Lean Stage1_Instances/THM-M-0346` | 1 | Expected no-match exit; the actual upstream theorem and API are absent. |
| Scoped search for `Carleson/Classical/CarlesonHunt.{olean,ilean,ir}` under the repository, `/tmp`, and the mathlib cache | 1 | Expected no-match exit; no compiled external theorem artifact is available. |
| Read-only `git show`, import traversal, and comment-aware placeholder scan of `/tmp/carleson-inspect` at `306ae5b` and `d422163` | 0 | Confirmed the placeholder Lean-4.29 body, incompatible source-complete pins, 117-module import closure, and five active imported `sorry` terms. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Pinned mathlib is `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `git diff --name-status 9db995936e3354d71e109c055e31b9e9588569c5..HEAD --` over canonical proof, registry, graph, anchor, pin, manifest, and execution-skill inputs | 0 | Only the prior `9db99593` blocker pair was added under this target; proof sources and pins did not change. |
| `cd Formalizations/Lean && timeout 120 lake env lean --version` | 0 | Lean `4.29.0`, commit `98dc76e3`; the pinned project frontend is available. An immediately preceding 30-second probe timed out without output, so the longer bounded retry is the recorded environment result. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest is deliberately absent because the proof phase is incomplete. |
| JSON parse, blocker-invariant check, and `git diff --check` | 0 | The structured blocker parsed, retained blocked/open/no-selftest invariants, and the owned diff had no whitespace errors. |

Source SHA-256 values are `a2af9f8bfdb524a60b3fc3d2e3eaaa064d8e70063d90e25a5134c79ae0bc4a4d`
for `Statement.lean` and `690e35222ca644aaf708ba0ab2ffc5d886b60209d46511edea6bfc1a60fbb81d`
for `Proof.lean`. The isolated object SHA-256 values were
`a349e94179235a765512cd39fca2fd50f09a0fb20009d0ad55155d2677906b82` and
`b7dd98fcb48d359df7bc92c1bea086896383aa08053f76772eb2852df44d2c91`.

## Boundary and retry condition

Lifecycle stays `planned`; the frozen root stays `[H3, M3, R4]`. The remaining root cut is
`M0346-C-REPRESENTATIVE`, `M0346-N-NORMALIZATION`, `M0346-N-CUTOFF`,
`M0346-L-CARLESON-HUNT`, and `M0346-T-AE-REP`. `audit_complete=false` and
`theorem_complete=false`. This record changes no scheduler state, accepts no receipt, and supports
no proof completion, validation, release, audit completion, theorem completion, or master
acceptance claim.

Resume after the integration lane provides an immutable, license-reviewed, placeholder-free
Carleson package compatible with the repository pins, or after a deliberate repository-wide pin
migration. Then import the actual theorem, check its axioms and terminal bodies, prove the exact
external partial-sum transport, and compose the root. Until then,
`.stage1-worker-selftest.json` must remain absent.
