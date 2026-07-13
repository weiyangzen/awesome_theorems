# THM-M-1018 proof recheck at `35d23d01`

Item: `S56-M-1018-PROOF`

Date: `2026-07-14T02:51:41+08:00`

Base revision: `35d23d0193cd7c8fccb1d09f22534c6eba066b02`

Base tree: `4325d20b5ec8db888f28fcedc79cc1b7745c0c68`

## Verdict

`blocked`. This current-base retry found no eligible unconditional proof body for the exact target
`Stage1Instances.THM_M_1018.LevyInversionTarget`. The remaining root cut is
`M1018-T-ANALYTIC`, the fixed-data interval inversion theorem. The first unavailable frozen
package is `M1018-L-DIRICHLET`: neither the repository nor pinned mathlib evaluates the symmetric
improper sine integral with the normalization and endpoint values required by the frozen kernel.

Pinned mathlib does provide `integral_charFun_Icc`, whose explicit product-integrability and
Fubini proof is useful substrate. It proves an unweighted characteristic-function identity, not
the endpoint-kernel interval-mass limit. The pinned scan found no exact Levy inversion declaration,
and the prerequisite immutable anchor audit found no compatible external terminal body to pin.
The existing `root_compose` body remains conditional: it returns the analytic premise it is given
rather than constructing that premise.

Closing the root requires placeholder-free implementations of the endpoint-kernel construction and
Fubini identity, translation and scaling, exhaustive position branches, the Dirichlet sine-integral
limits, passage of pointwise limits through an arbitrary probability measure without false uniform
domination, the atom-free endpoint identity, and their composition into `M1018-T-ANALYTIC`.
Postulating the analytic package, assuming a Dirichlet limit, or substituting characteristic-
function uniqueness or density Fourier inversion would violate the frozen proof-body gate.

No proof body or proof receipt was added. The root vector remains `[H2, M3, R4]`,
`root_closed=false`, and `theorem_complete=false`. Because the assigned positive proof phase is not
genuinely self-tested as complete, `.stage1-worker-selftest.json` is deliberately absent.

## Validation

All local checks reused the automation-provided canonical pinned `.lake` artifacts read-only. No
`lake update`, `lake build`, dependency clone or fetch, or `.lake` mutation was performed. The
untracked `.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all at L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1018` | 0 | rank 494; planned hard-mathlib-anchor-and-wrapper lane; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1018/check_obligation_tree.py` | 0 | 17 obligations and 34 typed edges passed; denominator `c5662da4...d6c2`; root and fixed-data analytic theorem open M3 |
| isolated `lake env lean --trust=0` replay of `Statement.lean` and `ObligationTree.lean` | 0 | exact statement and conditional composition elaborated; `root_compose` reported `[propext, Classical.choice, Quot.sound]` |
| exact pinned mathlib Levy-inversion scan | 1 | expected no-match result; no exact interval-inversion anchor found |
| focused pinned Dirichlet/sine-integral/sinc-limit scan | 0 | matches were unrelated finite integrals, sinc substrate, or noise; no evaluated Dirichlet limit found |
| prohibited-construct scan over owned `*.lean` files | 1 | expected no-match result for `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, and `native_decide` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386...a95`; tree `bdc39a...c2b` |
| SHA-256 over statement, obligation tree, registry, typed graphs, audit, specs, toolchain, and manifest | 0 | exact values are bound in the structured blocker record |
| JSON parse and blocker invariant assertions | 0 | identity, blocked/open flags, unchanged root vector, empty receipts, root cut, and absent completion self-test agreed |
| per-file new-file whitespace checks | 0 aggregate | both files differed from `/dev/null` with no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test deliberately absent because the proof item is incomplete |

The isolated Lean replay compiled `Statement.lean` to a disposable temporary `Statement.olean`,
placed that directory before the pinned `LEAN_PATH`, and elaborated `ObligationTree.lean` with
`--trust=0`. Temporary output was removed. The checked input hashes include `88009a0b...fdd7` for
`Statement.lean`, `2df4f358...055e` for `ObligationTree.lean`, `14938dc0...fb95` for the registry,
and `0ab51094...fba2` for the typed graphs. The pinned toolchain and Lake-manifest hashes are
`651c8acc...b1d2` and `321626c8...2d81`.

## Retry Condition

Resume after a placeholder-free implementation of `M1018-T-ANALYTIC` and its frozen analytic
dependencies, or after discovery of an immutable compatible Lean 4 terminal proof that can be
pinned, exact-type transported, and checked without changing the dependency lock.

This is an owned blocker artifact, not a proof receipt. It does not satisfy
`S56-M-1018-PROOF`, propose checklist state, or support audit, theorem, validation, release, or
master-completion claims.
