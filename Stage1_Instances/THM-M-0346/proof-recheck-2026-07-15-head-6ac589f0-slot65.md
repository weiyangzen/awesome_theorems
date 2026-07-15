# THM-M-0346 proof recheck at current base

Item: `S56-M-0346-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T15:54:19+08:00`

Base revision: `6ac589f0d8c5a9eeb726a1a05def7f9467ea2e2d`

Base tree: `9e8c2b617c489611e447b350a4b4cf4aeff15f39`

## Verdict

`blocked`. The assigned proof phase remains `[ ]`; no completion self-test is issued.

The exact target is `Stage1.THM_M_0346.CarlesonTarget`: every complex `L^2` function on the
period-one additive circle has symmetric Fourier partial sums converging to its canonical `Lp`
representative almost everywhere. The existing `Proof.lean` contains genuine, placeholder-free
bodies for the representative certificate, period and exponent facts, the dossier-local cutoff
equality, an upstream-shaped specialization adapter, and conditional composition. A trust-zero
replay checks all six bodies. It does not prove `RawCarlesonHunt`; therefore
`carlesonTarget_of_rawCarlesonHunt : RawCarlesonHunt -> CarlesonTarget` is not root closure.

The first failed gate remains `M0346-L-CARLESON-HUNT`. Neither the pinned packages nor the owned
sources contain the real `carleson_hunt` declaration or its `partialFourierSum'` API. Pinned
mathlib's `hasSum_fourier_series_L2` gives convergence in the `Lp` Hilbert space, not pointwise or
almost-everywhere convergence. Its pointwise result requires a continuous function with summable
Fourier coefficients, so it cannot replace the arbitrary-`L^2` target.

## Upstream compatibility boundary

The pre-existing partial Git object cache at `/tmp/carleson-inspect` was inspected read-only. It was
not fetched, checked out, copied, imported, or treated as a dependency. Across all 970 cached
commits, no revision pins this repository's mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The only cached Lean `v4.29.0` revision is
`306ae5b29300771aece1aa39f0a939183cc59486`; it pins mathlib
`f1a99cc3d4b62bff01325ac228882baadea934af` and defines `carleson_hunt := sorry`.
The `v4.29.1` revision is likewise placeholder-backed and uses another mathlib pin. The
source-complete theorem at `d422163115553c400bb93b6b3b0d50313b7a9f25` requires Lean
`v4.30.0-rc2` and mathlib `1a4917a18b30ea1333c195e597067fe044ac9176`.

Thus no current-pin, placeholder-free proof body is available. Vendoring unbuilt source from an
incidental cache would not satisfy the immutable dependency, exact-toolchain, transitive trust, or
reproducibility gates, and this worker is forbidden to fetch or mutate `.lake`.

## Narrow evidence

All validation ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only. Temporary Lean objects were confined to
`/tmp` and removed. No `lake update`, `lake build`, dependency clone/fetch, network request,
external checkout, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1,546 unique ordered targets and ranks passed. |
| `python3 scripts/stage1_target.py show THM-M-0346` | 0 | Rank 839; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0346/check_obligation_tree.py` | 0 | Eleven obligations and 24 typed edges passed; denominator `1ff60884ffc043439ab5a7b812bc9f2e8133e9d1eb8d130330d43f2709439c8c5`; root open at M3. |
| `cd Formalizations/Lean && timeout 240 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0346/Statement.lean` | 0 | The exact canonical target elaborated with the pinned Lean project environment. |
| Isolated `lake env lean --trust=0 -t0` replay of copied `Statement.lean` and `Proof.lean` below `/tmp` | 0 | The target and all six local declarations elaborated; each was sorry-free and reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| Prohibited-mechanism scan over `Statement.lean`, `Proof.lean`, and `ObligationTree.lean` | 1 | Expected no-match exit; no `sorry`, `admit`, axiom-like declaration, unsafe mechanism, or `native_decide` occurred. |
| Existing-package scan for a directory named `carleson` | 1 | Expected no-match exit; no pinned Carleson package exists. |
| Pinned-source scan for `carleson_hunt` or `partialFourierSum'` | 1 | Expected no-match exit; the external theorem and API are absent. |
| Inspection of mathlib `AddCircle.lean` convergence declarations | 0 | The available `L^2` result is topology-valued; the available pointwise result assumes continuous `f` and summable coefficients. |
| Scoped diff from prior recheck base `431e77db` through current `HEAD` | 0 | Empty output; the statement, proof, registry, graphs, anchor, toolchain, dependency manifest, target manifest, and execution skill are unchanged. |
| Read-only history inspection of all 970 commits in `/tmp/carleson-inspect` | 0 | No exact mathlib-pin match; the sole Lean 4.29.0 revision has `sorry`, while the real body uses incompatible pins. |
| `cd Formalizations/Lean && timeout 30 lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3`; the pinned environment is available. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest deliberately absent because the proof phase is incomplete. |

Source SHA-256 values remain
`a2af9f8bfdb524a60b3fc3d2e3eaaa064d8e70063d90e25a5134c79ae0bc4a4d` for
`Statement.lean` and `690e35222ca644aaf708ba0ab2ffc5d886b60209d46511edea6bfc1a60fbb81d`
for `Proof.lean`. The isolated object hashes remain
`a349e94179235a765512cd39fca2fd50f09a0fb20009d0ad55155d2677906b82` and
`b7dd98fcb48d359df7bc92c1bea086896383aa08053f76772eb2852df44d2c91`.

## Boundary and retry condition

Lifecycle stays `planned`; the frozen root stays `[H3, M3, R4]`. The remaining root cut is
`M0346-C-REPRESENTATIVE`, `M0346-N-NORMALIZATION`, `M0346-N-CUTOFF`,
`M0346-L-CARLESON-HUNT`, and `M0346-T-AE-REP`. `audit_complete=false` and
`theorem_complete=false`. This record changes no scheduler state, accepts no receipt, and supports
no proof-completion or master-acceptance claim.

Retry after the integration lane provides an immutable, license-reviewed, placeholder-free
Carleson package compatible with the repository pins, or after a deliberate repository-wide pin
migration. Then import the actual theorem, check the external partial-sum transport, audit its
transitive terminal bodies and axioms, and compose the exact root. Until then,
`.stage1-worker-selftest.json` must remain absent.
