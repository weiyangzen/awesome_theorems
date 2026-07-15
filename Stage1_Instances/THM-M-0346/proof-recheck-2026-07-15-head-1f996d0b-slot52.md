# THM-M-0346 proof recheck at current base

Item: `S56-M-0346-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T13:14:22+08:00`

Base revision: `1f996d0ba7939acd26bf231689a91751d276bb8c`

Base tree: `ae0448c57d503bd89b62f8f4b753e689abe77e83`

## Verdict

`blocked`. The assigned proof phase remains `[ ]`; no completion self-test is issued.

The current `Proof.lean` is genuine partial proof work. A trust-zero replay checks the canonical
`Lp` representative's `MemLp` certificate, the period-one and exponent-two side conditions, an
adapter from an upstream-shaped theorem, exact equality of its locally modeled inclusive cutoff
with `symmetricPartialSum`, and composition into the exact
`Stage1.THM_M_0346.CarlesonTarget`. All six declarations are sorry-free and depend only on
`propext`, `Classical.choice`, and `Quot.sound`.

This does not prove the analytic premise `RawCarlesonHunt`. The local
`upstreamPartialFourierSum` models the audited API, but the actual external
`partialFourierSum'` is not imported, so no equality against that external definition has been
checked. In particular,
`carlesonTarget_of_rawCarlesonHunt : RawCarlesonHunt -> CarlesonTarget` is a conditional
composition body, not a proof of its premise or of the root.

The first failed gate is `M0346-L-CARLESON-HUNT`. The existing pinned packages contain neither a
Carleson package nor declarations named `carleson_hunt` or `partialFourierSum'`. The audited
candidate remains `fpvandoorn/carleson` at commit
`80e151dff5ddce2426079ec6392616496a4ec927`, module
`Carleson.Classical.CarlesonHunt`, declaration `carleson_hunt`. It targets Lean
`v4.30.0-rc2` and mathlib `1a4917a18b30ea1333c195e597067fe044ac9176`, whereas this
repository is pinned to Lean `v4.29.0` and mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. It is absent from the allowed dependency closure
and therefore supplies no local kernel proof or transitive trust evidence.

The frozen registry remains authoritative. Its open root cut is
`M0346-C-REPRESENTATIVE`, `M0346-N-NORMALIZATION`, `M0346-N-CUTOFF`,
`M0346-L-CARLESON-HUNT`, and `M0346-T-AE-REP`. The existing bodies are partial evidence toward
the adapter obligations, but this recheck does not rewrite the pre-proof closure observation or
claim any new obligation closed. Assuming `RawCarlesonHunt`, using the conditional composer as
root evidence, or substituting mathlib's `L2`-topology convergence theorem would violate the exact
target.

## Narrow evidence

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused read-only. Temporary
Lean objects were written below `/tmp` and removed. No `lake update`, `lake build`, dependency
clone/fetch, network operation, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1,546 unique ordered targets and ranks passed. |
| `python3 scripts/stage1_target.py show THM-M-0346` | 0 | Rank 839; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0346/check_obligation_tree.py` | 0 | Eleven obligations and 24 typed edges passed; denominator `1ff60884ffc043439ab5a7b812bc9f2e8133e9d1eb8d130330d43f2709439c8c5`; root open at M3. |
| Isolated `lake env lean --trust=0 -t0` replay of `Statement.lean` and `Proof.lean` using the existing pinned package paths | 0 | The exact target and six local declarations elaborated; every declaration was sorry-free and used only `propext`, `Classical.choice`, and `Quot.sound`. |
| Prohibited-mechanism scan over `Statement.lean` and `Proof.lean` | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, bodyless axiom/constant, `opaque`, `unsafe`, `extern`, `implemented_by`, or `native_decide` occurred. |
| Existing-package scan for a directory named `carleson` | 1 | Expected no-match exit; no pinned Carleson package exists. |
| Source scan for `theorem carleson_hunt` or `def partialFourierSum'` | 1 | Expected no-match exit; the external theorem and API are absent. |
| Scoped diff of proof inputs and pins from prior recheck base `33a5b0d6` through current `HEAD` | 0 | Empty output; no statement, proof, registry, graph, anchor, toolchain, manifest, target-manifest, or skill input changed. |
| `cd Formalizations/Lean && timeout 30 lake env lean --version` | 1 | Project Lake stopped before Lean because the shared `flt-regular` checkout has unresolved `HEAD`; it was not repaired or modified. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest deliberately absent because the proof phase is incomplete. |

The isolated replay obtained `lean` and `LEAN_PATH` with `lake env` from the existing pinned
mathlib checkout, redirected its stale nested package prefixes to the same canonical package
directories, set `LEAN_NUM_THREADS=1`, and removed the temporary directory. Source SHA-256 values
were `a2af9f8bfdb524a60b3fc3d2e3eaaa064d8e70063d90e25a5134c79ae0bc4a4d` for
`Statement.lean` and `690e35222ca644aaf708ba0ab2ffc5d886b60209d46511edea6bfc1a60fbb81d`
for `Proof.lean`. Temporary object SHA-256 values were
`a349e94179235a765512cd39fca2fd50f09a0fb20009d0ad55155d2677906b82` and
`b7dd98fcb48d359df7bc92c1bea086896383aa08053f76772eb2852df44d2c91`.

## Boundary and retry condition

Lifecycle stays `planned`; the root vector stays `[H3, M3, R4]`;
`audit_complete=false` and `theorem_complete=false`. This is current-base warm-cache blocker
evidence only. It changes no scheduler item, accepts no receipt, and supports no validation,
release, audit-completion, theorem-completion, or master-acceptance claim.

Resume after an immutable, license-reviewed Carleson package compatible with the repository pins
is provided, or after a deliberate repository-wide pin migration. Then import the actual
`carleson_hunt`, check the exact external partial-sum transport, audit its transitive terminal
bodies and axioms, and compose the exact root. Because that proof body is unavailable under this
worker's no-fetch and no-`.lake`-mutation constraints, `.stage1-worker-selftest.json` remains
absent.
