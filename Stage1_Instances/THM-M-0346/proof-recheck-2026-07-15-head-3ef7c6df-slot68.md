# THM-M-0346 proof recheck at current base

Item: `S56-M-0346-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T15:14:40+08:00`

Base revision: `3ef7c6dff0c66bc8c02e842f4cea6b9936349094`

Base tree: `58db6c40c0fa9186c4a56a022a6a37d1c2be551b`

## Verdict

`blocked`. The assigned proof phase remains `[ ]`; no completion self-test is issued.

The exact target is `Stage1.THM_M_0346.CarlesonTarget`: every complex `L^2` function on the
period-one additive circle has symmetric Fourier partial sums converging to its canonical `Lp`
representative almost everywhere. The existing `Proof.lean` contains genuine, sorry-free bodies
for the representative certificate, period and exponent facts, the dossier-local cutoff equality,
an upstream-shaped specialization adapter, and conditional composition. A trust-zero replay checks
all six bodies. It does not prove `RawCarlesonHunt`; consequently
`carlesonTarget_of_rawCarlesonHunt : RawCarlesonHunt -> CarlesonTarget` is not root closure.

The first failed gate remains `M0346-L-CARLESON-HUNT`. Neither the pinned packages nor the owned
sources contain the actual `carleson_hunt` declaration or its `partialFourierSum'` API. Mathlib's
`L^2`-topology convergence and summable-coefficient pointwise theorems have different conclusions
or stronger hypotheses and cannot replace the frozen target.

## Additional local-object audit

A pre-existing partial Git object cache at `/tmp/carleson-inspect` was inspected read-only; it was
not fetched, checked out, copied, imported, or treated as a dependency. It strengthens, rather than
removes, the blocker:

- `fpvandoorn/carleson` commit `d422163115553c400bb93b6b3b0d50313b7a9f25` contains a source body
  for `carleson_hunt`, but targets Lean `v4.30.0-rc2` and mathlib
  `1a4917a18b30ea1333c195e597067fe044ac9176`, not the repository's Lean `v4.29.0` and mathlib
  `8a178386ffc0f5fef0b77738bb5449d50efeea95` pins.
- A raw textual scan of that commit reports `sorry` at
  `Carleson/Classical/CarlesonOnTheRealLine.lean:27`, but the token is inside a block-commented,
  unused theorem and is not an elaborated placeholder. It does not itself invalidate the candidate;
  source inspection still cannot establish the exact terminal-body, axiom, or TCB closure required
  for proof credit.
- The upstream tag `v4.29.0` has a literal
  `carleson_hunt ... := sorry` and pins mathlib
  `f1a99cc3d4b62bff01325ac228882baadea934af`, so it is both placeholder-invalid and not aligned to
  this repository's exact mathlib revision.
- The previously audited commit `80e151dff5ddce2426079ec6392616496a4ec927` uses the same
  incompatible Lean `v4.30.0-rc2` / mathlib `1a4917...` environment as `d422163`.

The cached Git objects are neither a pinned Lake package nor elaborated kernel evidence. The task
forbids dependency fetches and `.lake` mutation, and this proof worker may not migrate repository-
wide pins. Vendoring an unbuilt multi-module source tree from an incidental `/tmp` cache would not
satisfy the immutable dependency, exact-toolchain, transitive trust, or reproducibility gates.

## Narrow evidence

All validation commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused read-only. Temporary
Lean objects were written below `/tmp` and removed. No `lake update`, `lake build`, dependency
clone/fetch, network request, checkout of the external cache, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1,546 unique ordered targets and ranks passed. |
| `python3 scripts/stage1_target.py show THM-M-0346` | 0 | Rank 839; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0346/check_obligation_tree.py` | 0 | Eleven obligations and 24 typed edges passed; denominator `1ff60884fc043439ab5a7b812bc9f2e8133e9d1eb8d130330d43f2709439c8c5`; root open at M3. |
| `cd Formalizations/Lean && lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0346/Statement.lean` | 0 | The exact target elaborated under the pinned project environment. |
| Isolated pinned-artifact `lake env lean --trust=0 -t0` replay of copied `Statement.lean` and `Proof.lean` below a temporary directory | 0 | The target and all six local adapter declarations elaborated; every declaration was sorry-free and reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| Prohibited-mechanism scan over `Statement.lean`, `Proof.lean`, and `ObligationTree.lean` | 1 | Expected no-match exit; no `sorry`, `admit`, axiom-like declaration, unsafe mechanism, or `native_decide` occurred. |
| Existing-package scan for a directory named `carleson` | 1 | Expected no-match exit; no pinned Carleson package exists. |
| Pinned-source scan for `theorem carleson_hunt` or `def partialFourierSum'` | 1 | Expected no-match exit; the external theorem and API are absent. |
| `git diff --name-status e89fe5cc..HEAD -- <scoped proof, registry, graph, pin, target-manifest, and skill inputs>` | 0 | Empty output; only prior blocker evidence for this target was integrated after the preceding recheck. |
| Read-only `git show` / `git grep` inspection of `/tmp/carleson-inspect` at `d422163`, `80e151d`, and tag `v4.29.0` | 0 | Confirmed the exact upstream declarations, incompatible pins, current source body, and the v4.29 placeholder body described above. |
| `cd Formalizations/Lean && timeout 30 lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3`; the pinned environment is available. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest deliberately absent because the proof phase is incomplete. |
| JSON parse, blocked/open/no-selftest invariant check, and `git diff --check` | 0 | The structured blocker parsed, stayed explicitly open with no completion self-test, and had no whitespace errors. |

The source SHA-256 values remain
`a2af9f8bfdb524a60b3fc3d2e3eaaa064d8e70063d90e25a5134c79ae0bc4a4d` for
`Statement.lean` and `690e35222ca644aaf708ba0ab2ffc5d886b60209d46511edea6bfc1a60fbb81d`
for `Proof.lean`. The isolated temporary object hashes are recorded in the accompanying structured
artifact.

## Boundary and retry condition

Lifecycle stays `planned`; the frozen obligation-tree authority keeps the root at
`[H3, M3, R4]`. The remaining root cut is `M0346-C-REPRESENTATIVE`,
`M0346-N-NORMALIZATION`, `M0346-N-CUTOFF`, `M0346-L-CARLESON-HUNT`, and
`M0346-T-AE-REP`. `audit_complete=false` and `theorem_complete=false`. This blocker record changes
no scheduler item, accepts no receipt, and supports no proof-completion or master-acceptance claim.

Resume after an immutable, license-reviewed, placeholder-free Carleson package compatible with the
repository pins is installed by the integration lane, or after a deliberate repository-wide pin
migration. Then import the real theorem, check the exact upstream partial-sum transport, audit its
transitive terminal bodies and axioms, and compose the exact root. Until then,
`.stage1-worker-selftest.json` must remain absent.
