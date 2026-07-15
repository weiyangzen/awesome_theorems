# THM-M-0346 proof recheck at current base

Item: `S56-M-0346-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T19:36:19+08:00`

Base revision: `88a5a5c6fe6bac0d813a74ca20fa553eaf2a6d68`

Base tree: `a0a75048a918a3bf566c3dbcf6b4352c3b2ee8e4`

## Verdict

`blocked`. The assigned proof phase remains `[ ]`; no completion self-test is issued.

The exact target is `Stage1.THM_M_0346.CarlesonTarget`: every complex `L^2` class on the
period-one additive circle has its inclusive symmetric Fourier partial sums converge to its
canonical `Lp` representative almost everywhere. The six existing declarations in `Proof.lean`
are genuine, placeholder-free adapter bodies. An isolated trust-zero replay checks the
representative's `MemLp` certificate, the period and exponent facts, specialization of an
upstream-shaped Carleson-Hunt theorem, equality of the dossier-local cutoff with
`symmetricPartialSum`, and conditional composition into the exact target. They are sorry-free and
report only `propext`, `Classical.choice`, and `Quot.sound`.

These bodies do not prove `RawCarlesonHunt`.
`carlesonTarget_of_rawCarlesonHunt : RawCarlesonHunt -> CarlesonTarget` is a checked conditional
composition, not a proof of its premise or of the root. The local `upstreamPartialFourierSum`
models the audited external API but does not import or validate the external
`partialFourierSum'` definition.

The first failed gate is `M0346-L-CARLESON-HUNT`. The pinned dependency closure has no Carleson
package and no source or compiled declarations for `carleson_hunt` or `partialFourierSum'`.
Pinned mathlib's `hasSum_fourier_series_L2` proves convergence in the `Lp` Hilbert space, not
pointwise or almost-everywhere convergence. Its pointwise theorem requires a continuous function
with summable Fourier coefficients and therefore cannot establish the arbitrary-`L^2` target.

The pre-existing read-only upstream cache does not supply a compatible body. Revision
`306ae5b29300771aece1aa39f0a939183cc59486` uses Lean `v4.29.0`, but pins mathlib
`f1a99cc3d4b62bff01325ac228882baadea934af` and defines `carleson_hunt := sorry`. The audited
source-complete revision `d422163115553c400bb93b6b3b0d50313b7a9f25` requires Lean
`v4.30.0-rc2` and mathlib `1a4917a18b30ea1333c195e597067fe044ac9176`; it is not installed or
compiled in this repository's pinned closure. Its 117-module import closure also contains five
active `sorry` terms, and the candidate's transitive axiom dependency has not been kernel-audited.
No cached upstream revision uses this repository's mathlib pin
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Fetching or mutating dependencies is forbidden for
this worker, so the missing analytic proof body cannot truthfully be integrated here.

## Narrow evidence

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused read-only. Temporary
Lean objects were confined to `/tmp` and removed. No `lake update`, `lake build`, dependency
clone/fetch, network request, external checkout, source import, or `.lake` mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1,546 unique ordered targets and ranks passed. |
| `python3 scripts/stage1_target.py show THM-M-0346` | 0 | Rank 839; lifecycle planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0346/check_obligation_tree.py` | 0 | Eleven obligations and 24 typed edges passed; denominator `1ff60884fc043439ab5a7b812bc9f2e8133e9d1eb8d130330d43f2709439c8c5`; root open at M3. |
| `cd Formalizations/Lean && timeout 240 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0346/Statement.lean` | 0 | The exact canonical target elaborated under the pinned project environment. |
| Isolated replay of copied `Statement.lean` and `Proof.lean` below `/tmp`, using the Lean binary and `LEAN_PATH` obtained through existing `lake env`, with `LEAN_NUM_THREADS=1`, `timeout 600`, `--trust=0`, and `-t0` | 0 | The exact target and all six local adapter declarations elaborated. Every declaration was sorry-free and used only `propext`, `Classical.choice`, and `Quot.sound`. |
| `rg -n --pcre2 '(?m)^\s*(?:axiom\|constant\|opaque)\b\|\b(?:sorry\|admit\|sorryAx\|unsafe\|extern\|implemented_by\|native_decide)\b' Stage1_Instances/THM-M-0346/{Statement,Proof,ObligationTree}.lean` | 1 | Expected no-match exit; no prohibited mechanism occurs in the owned Lean sources. |
| `find -L Formalizations/Lean/.lake/packages -maxdepth 1 -mindepth 1 -type d -printf '%f\n' \| sort \| rg -i '^carleson$'` | 1 | Expected no-match exit; no pinned Carleson package exists. |
| `rg -n --glob '*.lean' 'theorem\s+carleson_hunt\b\|def\s+partialFourierSum.' Formalizations/Lean Stage1_Instances/THM-M-0346` | 1 | Expected no-match exit; the actual upstream theorem and API are absent. |
| Search under pinned `packages` and `build` for `Carleson/Classical/CarlesonHunt.{olean,ilean,ir}` | 0 | Empty output; no compiled Carleson-Hunt artifact exists. |
| `rg -n -C 8 'theorem hasSum_fourier_series_L2\|theorem has_pointwise_sum_fourier_series_of_summable\|theorem hasSum_fourier_series_of_summable' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/Fourier/AddCircle.lean` | 0 | Located only the non-closing `Lp`-topology result and stronger-hypothesis pointwise results. |
| `git diff --name-status d44ed2b11fb201a761afad9b133caa8bc97fd710..HEAD --` over canonical proof, registry, graph, anchor, pin, manifest, target-manifest, and execution-skill inputs | 0 | Empty output; no scoped proof input or pin changed since the preceding recheck base. |
| Canonical JSON projection of every `THM-M-0346` object in `Docs/Stage1_Execution_DAG_rev-5.6.json`, at the preceding and current bases | 0 | Both projections hash to `604bb293d6c47cbc229b9ff7b2869c524bb0653ec4ea8bfd4577c7a209f9c853`; global generated-file changes concern only other targets. |
| Read-only `git show`, `git grep`, `rev-list`, import traversal, and comment-aware placeholder inspection of all 970 revisions in `/tmp/carleson-inspect` | 0 | The sole Lean-4.29-compatible upstream revision has a literal `sorry` body; the source-complete body has incompatible pins and a 117-module import closure containing five active `sorry` terms; no revision matches the repository mathlib pin. |
| `cd Formalizations/Lean && timeout 120 lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3`; the pinned environment is available. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest deliberately absent because the proof phase is incomplete. |
| JSON parse, blocked/open/no-selftest invariant check, and per-artifact whitespace checks | 0 | The structured record parsed, every fail-closed invariant held, and both new owned artifacts had no whitespace errors. |

The source SHA-256 values are `a2af9f8bfdb524a60b3fc3d2e3eaaa064d8e70063d90e25a5134c79ae0bc4a4d`
for `Statement.lean` and `690e35222ca644aaf708ba0ab2ffc5d886b60209d46511edea6bfc1a60fbb81d`
for `Proof.lean`. The temporary object SHA-256 values were
`a349e94179235a765512cd39fca2fd50f09a0fb20009d0ad55155d2677906b82` and
`b7dd98fcb48d359df7bc92c1bea086896383aa08053f76772eb2852df44d2c91`.

## Boundary and retry condition

Lifecycle stays `planned`; the frozen root stays `[H3, M3, R4]`. The remaining root cut is
`M0346-C-REPRESENTATIVE`, `M0346-N-NORMALIZATION`, `M0346-N-CUTOFF`,
`M0346-L-CARLESON-HUNT`, and `M0346-T-AE-REP`. `audit_complete=false` and
`theorem_complete=false`. This record changes no scheduler state, accepts no receipt, and supports
no proof-completion, validation, release, audit-completion, theorem-completion, or master-acceptance
claim.

Resume after the integration lane provides an immutable, license-reviewed, transitively
placeholder-clean Carleson package compatible with the repository pins, or after a deliberate
repository-wide pin migration plus removal or dependency-exclusion proof for every reachable
placeholder. Then import the actual theorem, validate the exact external partial-sum transport,
audit its transitive terminal bodies and axioms, and compose the exact root. Until then,
`.stage1-worker-selftest.json` must remain absent.
