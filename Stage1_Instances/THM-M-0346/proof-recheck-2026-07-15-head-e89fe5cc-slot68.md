# THM-M-0346 proof recheck at current base

Item: `S56-M-0346-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T14:44:44+08:00`

Base revision: `e89fe5cc9f4b8de45e791d470b1e02e39ca0e734`

Base tree: `dc43d49d892d5f7eb05124c95f52f837b97734ba`

## Verdict

`blocked`. The assigned proof phase remains `[ ]`; no completion self-test is issued.

The current `Proof.lean` is genuine partial proof work. A trust-zero replay checks the canonical
`Lp` representative's `MemLp` certificate, the period-one and exponent-two side conditions, an
adapter from an upstream-shaped theorem, exact equality of its dossier-local inclusive cutoff with
`symmetricPartialSum`, and conditional composition into the exact
`Stage1.THM_M_0346.CarlesonTarget`. All six declarations are sorry-free and depend only on
`propext`, `Classical.choice`, and `Quot.sound`.

This does not prove the analytic premise `RawCarlesonHunt`. The actual external
`partialFourierSum'` is not imported, so no equality against that external definition has been
checked. In particular, `carlesonTarget_of_rawCarlesonHunt : RawCarlesonHunt -> CarlesonTarget`
is a conditional adapter, not a proof of its premise or of the root.

The first failed gate is `M0346-L-CARLESON-HUNT`. The existing pinned packages contain neither a
Carleson package nor declarations named `carleson_hunt` or `partialFourierSum'`. The audited
candidate remains `fpvandoorn/carleson` at commit
`80e151dff5ddce2426079ec6392616496a4ec927`, module
`Carleson.Classical.CarlesonHunt`, declaration `carleson_hunt`. It targets Lean
`v4.30.0-rc2` and mathlib `1a4917a18b30ea1333c195e597067fe044ac9176`, whereas this
repository is pinned to Lean `v4.29.0` and mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. It is absent from the allowed dependency closure
and supplies no local kernel proof or transitive trust evidence.

The frozen open root cut remains `M0346-C-REPRESENTATIVE`, `M0346-N-NORMALIZATION`,
`M0346-N-CUTOFF`, `M0346-L-CARLESON-HUNT`, and `M0346-T-AE-REP`. Assuming the analytic
premise, treating the conditional adapter as root evidence, or substituting mathlib's
`L2`-topology convergence theorem would violate the exact target.

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
| Isolated pinned-artifact `lake env lean --trust=0 -t0` replay of `Statement.lean` and `Proof.lean` | 0 | The exact target and all six local adapter declarations elaborated; each was sorry-free and used only `propext`, `Classical.choice`, and `Quot.sound`. |
| Prohibited-mechanism scan over the three owned Lean sources | 1 | Expected no-match exit; no `sorry`, `admit`, axiom-like body, `unsafe`, or `native_decide` mechanism occurred. |
| Existing-package scan for a directory named `carleson` | 1 | Expected no-match exit; no pinned Carleson package exists. |
| Source scan for `theorem carleson_hunt` or `def partialFourierSum'` | 1 | Expected no-match exit; the external theorem and API are absent. |
| Scoped diff of proof inputs and pins from prior recheck base `7505614b` through current `HEAD` | 0 | Empty output; no statement, proof, registry, graph, anchor, toolchain, dependency manifest, target manifest, or execution-skill input changed. |
| `cd Formalizations/Lean && timeout 30 lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3`; the pinned project environment is available. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest deliberately absent because the proof phase is incomplete. |
| JSON parse, blocked/open/no-selftest invariant check, and `git diff --check` | 0 | The structured blocker parsed, stayed explicitly open with no completion self-test, and had no whitespace errors. |

Source SHA-256 values were `a2af9f8bfdb524a60b3fc3d2e3eaaa064d8e70063d90e25a5134c79ae0bc4a4d`
for `Statement.lean` and `690e35222ca644aaf708ba0ab2ffc5d886b60209d46511edea6bfc1a60fbb81d`
for `Proof.lean`. Temporary object SHA-256 values were
`a349e94179235a765512cd39fca2fd50f09a0fb20009d0ad55155d2677906b82` and
`b7dd98fcb48d359df7bc92c1bea086896383aa08053f76772eb2852df44d2c91`.

## Boundary and retry condition

Lifecycle stays `planned`; the frozen obligation-tree authority keeps the root at
`[H3, M3, R4]`. The intake-era `instance.json` still records the pre-freeze `[H3, M4, R4]` and
is stale; this proof worker does not rewrite that predecessor-owned intake authority.
`audit_complete=false` and `theorem_complete=false`. This is current-base warm-cache blocker
evidence only. It changes no scheduler item, accepts no receipt, and supports no validation,
release, audit-completion, theorem-completion, or master-acceptance claim.

Resume after an immutable, license-reviewed Carleson package compatible with the repository pins
is provided, or after a deliberate repository-wide pin migration. Then import the actual
`carleson_hunt`, check the exact external partial-sum transport, audit its transitive terminal
bodies and axioms, and compose the exact root. Because that proof body is unavailable under this
worker's no-fetch and no-`.lake`-mutation constraints, `.stage1-worker-selftest.json` remains
absent.
