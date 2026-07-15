# THM-M-0346 proof recheck at current base

Item: `S56-M-0346-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T15:34:58+08:00`

Base revision: `431e77db6367a2eda83060b7212cb490d11ca39f`

Base tree: `7ed0ffdf78a9b7a5d8d474b30aca0d8809c1d087`

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

## Upstream History Audit

The pre-existing partial Git object cache at `/tmp/carleson-inspect` was inspected read-only. It was
not fetched, checked out, copied, imported, or treated as a dependency. All 970 cached commits were
checked for the repository's exact mathlib revision and Lean toolchain:

- No cached revision pins mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- Upstream tag `v4.29.0` (annotated tag object `f241d9b48d63ff9528debc3cd493ed5cdc4ac0df`)
  resolves to commit `306ae5b29300771aece1aa39f0a939183cc59486`, the only cached Lean `v4.29.0`
  revision. It pins mathlib
  `f1a99cc3d4b62bff01325ac228882baadea934af`, and `carleson_hunt` is literally `:= sorry`.
- Tag `v4.29.1` (annotated tag object `feecd0e2b7b619ef7b973cff64cfca47fb3e7344`)
  resolves to commit `17be9be73343aefe5a124e0fac9d2aebb08e6759`, which still has the literal
  placeholder and pins mathlib `5e932f97dd25535344f80f9dd8da3aab83df0fe6`.
- The source-complete theorem at commit `d422163115553c400bb93b6b3b0d50313b7a9f25` targets Lean
  `v4.30.0-rc2` and mathlib `1a4917a18b30ea1333c195e597067fe044ac9176`.

Thus no current-pins, placeholder-free upstream revision exists. This closes a compatibility-search
question but does not supply a proof body. Vendoring unbuilt sources from an incidental cache would
not satisfy the immutable dependency, exact-toolchain, transitive trust, or reproducibility gates.

## Narrow Evidence

All validation commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only. Temporary Lean objects were written below
`/tmp` and removed. No `lake update`, `lake build`, dependency clone/fetch, network request,
external checkout, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1,546 unique ordered targets and ranks passed. |
| `python3 scripts/stage1_target.py show THM-M-0346` | 0 | Rank 839; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0346/check_obligation_tree.py` | 0 | Eleven obligations and 24 typed edges passed; denominator `1ff60884fc043439ab5a7b812bc9f2e8133e9d1eb8d130330d43f2709439c8c5`; root open at M3. |
| `cd Formalizations/Lean && timeout 240 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0346/Statement.lean` | 0 | The exact target elaborated under the pinned project environment. |
| Isolated pinned-artifact `lake env lean --trust=0 -t0` replay of copied `Statement.lean` and `Proof.lean` below a temporary directory | 0 | The target and all six local adapter declarations elaborated; every declaration was sorry-free and reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| Prohibited-mechanism scan over `Statement.lean`, `Proof.lean`, and `ObligationTree.lean` | 1 | Expected no-match exit; no `sorry`, `admit`, axiom-like declaration, unsafe mechanism, or `native_decide` occurred. |
| Existing-package scan for a directory named `carleson` | 1 | Expected no-match exit; no pinned Carleson package exists. |
| Pinned-source scan for `theorem carleson_hunt` or `def partialFourierSum'` | 1 | Expected no-match exit; the external theorem and API are absent. |
| `git diff --name-status 3ef7c6df..HEAD --` followed by the canonical statement, proof, tree, registry, graph, anchor, pin, manifest, target-manifest, and execution-skill paths | 0 | Empty output; only prior blocker evidence was integrated after the preceding recheck. |
| `git rev-list --all` plus read-only `git show`, `jq`, and `rg` inspection of all 970 commits in `/tmp/carleson-inspect` | 0 | No exact mathlib-pin match; the sole Lean 4.29.0 revision has `sorry`, while the real body requires incompatible Lean/mathlib pins. |
| `cd Formalizations/Lean && timeout 30 lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3`; the pinned environment is available. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest deliberately absent because the proof phase is incomplete. |

The source SHA-256 values remain
`a2af9f8bfdb524a60b3fc3d2e3eaaa064d8e70063d90e25a5134c79ae0bc4a4d` for
`Statement.lean` and `690e35222ca644aaf708ba0ab2ffc5d886b60209d46511edea6bfc1a60fbb81d`
for `Proof.lean`. The isolated temporary object hashes are
`a349e94179235a765512cd39fca2fd50f09a0fb20009d0ad55155d2677906b82` and
`b7dd98fcb48d359df7bc92c1bea086896383aa08053f76772eb2852df44d2c91`.

## Boundary And Retry Condition

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
