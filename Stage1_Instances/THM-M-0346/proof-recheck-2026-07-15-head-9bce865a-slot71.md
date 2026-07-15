# THM-M-0346 proof recheck at current base

Item: `S56-M-0346-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T13:47:09+08:00`

Base revision: `9bce865a14bcc270344ea909d6936c6ea22aa1c2`

Base tree: `523a9471aac257c4cf54acceee07172fab22f5b4`

## Verdict

`blocked`. The assigned proof phase remains `[ ]`; no completion self-test is issued.

The existing `Proof.lean` contains genuine, placeholder-free adapter bodies. A trust-zero replay
checks the canonical `Lp` representative's `MemLp` certificate, the unit-period and `p = 2` side
conditions, specialization of an upstream-shaped theorem, exact equality of the dossier-local
inclusive cutoff with `symmetricPartialSum`, and conditional composition into the exact
`Stage1.THM_M_0346.CarlesonTarget`. All six declarations are sorry-free and report only
`propext`, `Classical.choice`, and `Quot.sound`.

These bodies do not prove `RawCarlesonHunt`. The local `upstreamPartialFourierSum` models the
audited API, but the actual external `partialFourierSum'` is not imported. Consequently,
`carlesonTarget_of_rawCarlesonHunt : RawCarlesonHunt -> CarlesonTarget` is a checked conditional
composition, not a proof of its premise or of the exact root.

The first failed gate is `M0346-L-CARLESON-HUNT`. Neither pinned mathlib nor any existing pinned
package contains `carleson_hunt`, `partialFourierSum'`, or a Carleson package. The audited candidate
is `fpvandoorn/carleson` at commit `80e151dff5ddce2426079ec6392616496a4ec927`, module
`Carleson.Classical.CarlesonHunt`, declaration `carleson_hunt`. It targets Lean
`v4.30.0-rc2` and mathlib `1a4917a18b30ea1333c195e597067fe044ac9176`, whereas this
repository pins Lean `v4.29.0` and mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. It therefore remains an external anchor rather
than a locally imported, kernel-checked proof body. The task forbids fetching or mutating `.lake`,
so that missing artifact cannot be supplied in this worker.

The frozen registry remains authoritative. Its open root cut is
`M0346-C-REPRESENTATIVE`, `M0346-N-NORMALIZATION`, `M0346-N-CUTOFF`,
`M0346-L-CARLESON-HUNT`, and `M0346-T-AE-REP`. The local bodies are partial evidence toward the
adapter obligations, but this recheck neither rewrites the frozen closure observation nor claims a
new obligation closed. Assuming `RawCarlesonHunt`, crediting a conditional wrapper as root closure,
or substituting mathlib's `L2`-topology convergence theorem would change the proof contract.

The target task DAG still has no master-accepted predecessor state. Existing intake, statement,
anchor-audit, and obligation-tree artifacts are provisional worker evidence. This recheck may
prepare proof evidence, but it cannot satisfy the dependency-ordered master acceptance gate.

## Narrow evidence

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused read-only. Temporary
Lean objects were written below `/tmp` and removed. No `lake update`, `lake build`, dependency
clone/fetch, network request, or `.lake` mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1,546 unique targets and ranks 1 through 1,546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0346` | 0 | Rank 839; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0346/check_obligation_tree.py` | 0 | Eleven obligations and 24 typed edges passed; denominator `1ff60884ffc043439ab5a7b812bc9f2e8133e9d1eb8d130330d43f2709439c8c5`; root open at M3. |
| Isolated pinned-artifact Lean `--trust=0 -t0` replay of `Statement.lean` and `Proof.lean` | 0 | The exact target and all six local declarations elaborated; every declaration was sorry-free and used only `propext`, `Classical.choice`, and `Quot.sound`. |
| Prohibited-mechanism scan over the three owned Lean sources | 1 | Expected no-match exit; no `sorry`, `admit`, `axiom`, `unsafe`, or `native_decide` mechanism was found. |
| Existing-package scan for a directory named `carleson` | 1 | Expected no-match exit; no pinned Carleson package exists. |
| Source scan for `theorem carleson_hunt` or `def partialFourierSum'` in repository and pinned Lean sources | 1 | Expected no-match exit; the actual external theorem and API are absent. |
| Scoped diff of proof inputs and pins from prior recheck base `a8915398` through current `HEAD` | 0 | Empty output; no statement, proof, registry, graph, anchor, toolchain, dependency manifest, target manifest, or execution-skill input changed. |
| `timeout 30 bash -lc 'cd Formalizations/Lean && lake env lean --version'` | 124 | Project Lake timed out while shared `flt-regular` had unresolved `HEAD` at `refs/heads/.invalid`; it was not repaired or modified. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test is deliberately absent because the proof phase is incomplete. |
| JSON parse, blocker-invariant check, and `git diff --check` | 0 | The structured blocker parsed, remained explicitly blocked/open with no self-test, and had no whitespace errors. |

The successful replay obtained the pinned Lean binary and base `LEAN_PATH` with `lake env` from the
existing mathlib package, redirected its stale nested package prefixes to the same canonical
existing package directories, set `LEAN_NUM_THREADS=1`, used `--trust=0 -t0`, and removed the
temporary directory. Source SHA-256 values were
`a2af9f8bfdb524a60b3fc3d2e3eaaa064d8e70063d90e25a5134c79ae0bc4a4d` for
`Statement.lean` and `690e35222ca644aaf708ba0ab2ffc5d886b60209d46511edea6bfc1a60fbb81d`
for `Proof.lean`. Temporary object SHA-256 values were
`a349e94179235a765512cd39fca2fd50f09a0fb20009d0ad55155d2677906b82` and
`b7dd98fcb48d359df7bc92c1bea086896383aa08053f76772eb2852df44d2c91`.

## Boundary and retry condition

Lifecycle stays `planned`; the root vector stays `[H3, M3, R4]`;
`audit_complete=false` and `theorem_complete=false`. This is current-base warm-cache blocker
evidence only. It does not satisfy `S56-M-0346-PROOF`, close the root, change scheduler state,
accept a receipt, or claim validation, release, audit completion, theorem completion, or master
acceptance.

Resume after an immutable, license-reviewed Carleson package compatible with the repository pins
is provided, or after a deliberate repository-wide pin migration. Then import the real theorem,
check the exact external partial-sum transport, audit its transitive terminal bodies and axioms,
and compose the exact root. Because the proof phase is not genuinely complete,
`.stage1-worker-selftest.json` is deliberately absent.
