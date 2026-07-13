# THM-M-1244 proof-phase recheck at `92246ea9`

Item: `S56-M-1244-PROOF`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `92246ea92c0c44282c05728798bc7c7e4a5a1464`

Base tree: `bd58be98bf3046078c016d44fb4a677ea231cb23`

## Verdict

`blocked`. The exact assigned proof phase remains open. The existing placeholder-free bodies in
`Proof.lean` recheck the coordinate-to-operator energy branch, but no repository-local or pinned
declaration inhabits
`Stage1Instances.THM_M_1244.CoordinateLogSobolevPackage`. Consequently
`Stage1Instances.THM_M_1244.GaussianLogSobolevTarget` is not kernel-closed, the item remains `[ ]`,
and the root vector remains `[H1, M4, R3]`.

The local bodies prove three genuine pieces:

- `coordinateEnergy_le_operatorEnergy` bounds the sum of coordinate squares by the squared
  operator norm for Lean's product sup norm;
- `coordinateEnergy_integral_le` integrates that pointwise comparison;
- `coordinateToOperatorEnergyPackage` packages the required factor-two inequality.

These support frozen obligations `M1244-C-COORD`, `M1244-L-POINTWISE`, and
`M1244-L-INTEGRAL`. The checked theorem `gaussianLogSobolevTarget_of_packages` then composes an
assumed coordinate LSI and the energy package into the exact root. It does not construct the first
premise, so returning it would be a conditional theorem rather than the requested proof.

## Failed Gate

The first failed gate is `M1244-L-UPSTREAM`. Pinned mathlib has no Gaussian logarithmic Sobolev
terminal theorem. The only audited substantive candidate remains
`GaussianLSI.gaussian_logSobolev_W12_pi` from `lean-stat-learning-theory` commit
`7b82b1323c80f0c21ca449fd12e1c24315ae9782`. That project pins Lean `4.27.0-rc1` and mathlib
`d68c4dc09f5e000d3c968adae8def120a0758729`; it is absent from this repository's pinned Lake
manifest.

The upstream theorem is not a one-file wrapper opportunity. Its recursive local import closure is
24 Apache-2.0 Lean modules, 17,381 lines, and 875,518 bytes. A scratch-only compatibility probe
compiled the first three modules in topological order against this repository's Lean 4.29/mathlib
pin: `MeasureInfrastructure`, `GaussianMeasure`, and `GaussianSobolevDense.Defs`. No source edits
were needed, but this checks neither the remaining 21 modules nor the terminal theorem. Even after
such a port, exact bridges are still required for product-Gaussian measure identity, zero-safe
entropy, `ContDiff` regularity, `MemW12GaussianPi`, zero mass, and boundary behavior.

This worker did not vendor that unpinned source, mutate `.lake`, or claim the scratch feasibility
probe as proof evidence. Closing the root requires a deliberate dependency integration with full
provenance and trust validation, or a new local proof of the same analytic package. Assuming the
package, copying only its terminal declaration, or changing the frozen target is prohibited.

## Validation

All credited checks used the existing canonical pinned `.lake` artifacts read-only. No `lake
update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. Lean outputs were
isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-1244` | 0 | Rank 425; lifecycle `planned`; theorem incomplete. |
| isolated `lake env lean --trust=0 -t0` replay of `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` | 0 | The exact statement, conditional composition, pointwise comparison, integral comparison, and energy package elaborated. The recorded proof axiom profile is `[propext, Classical.choice, Quot.sound]`. |
| `python3 Stage1_Instances/THM-M-1244/check_obligation_tree.py` | 0 | 18 obligations and 36 typed edges passed; denominator `edecb957...c297`; the frozen pre-proof graph remains open M4. |
| scoped prohibited-construct scan over every owned `*.lean` file | 1 | Expected no-match: no `sorry`, `admit`, axiom declaration, `sorryAx`, `unsafe`, `implemented_by`, or `native_decide`. |
| pinned-mathlib search for log-Sobolev names and Gaussian/entropy combinations | 1 | Expected no-match: no eligible terminal theorem in pinned mathlib. |
| scratch topological compilation of three immutable upstream modules | 0 each | Feasibility only: all three compiled without source edits; only deprecated `push_neg` warnings occurred. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | Revision `8a178386...eea95`; tree `bdc39a31...e242b`. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The isolated Lean recipe was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1244
tmp=$(mktemp -d /tmp/thm-m-1244-proof-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/ObligationTree.lean" "$tmp/ObligationTree.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
cd "$tmp"
LEAN_PATH="$lean_path" "$lean" --trust=0 -t0 -o Statement.olean Statement.lean
LEAN_PATH=".:$lean_path" "$lean" --trust=0 -t0 -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$lean_path" "$lean" --trust=0 -t0 Proof.lean
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Retry Condition

Resume only after the immutable upstream closure is deliberately added to the repository's pinned
dependency design and fully ported, provenance-audited, and kernel-checked, or after local
placeholder-free implementations of `M1244-L-UPSTREAM` and its transport children are available.

This is fresh owned blocker evidence, not a proof receipt. It does not satisfy
`S56-M-1244-PROOF`. Because the assigned phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` remains absent.
