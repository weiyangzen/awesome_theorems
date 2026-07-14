# THM-M-0580 proof-phase recheck at base 111bbeb1

Item: `S56-M-0580-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `111bbeb1a210ae4e8525a4342012921ab60e466f`

Base tree: `8f705aa79622bf1e9be0665ae1254313df21b4f6`

## Verdict

`blocked`. No eligible terminal Lean 4 body exists in the repository or pinned dependency closure
for the exact proposition `Stage1Instances.THM_M_0580.PerelmanPoincareTarget`. No proof body or
receipt was added. The item remains `[ ]`, the root vector remains `[H2, M4, R4]`, and the audit,
root, and theorem remain incomplete.

The immediate frozen root cut set remains:

- `M0580-N-SMOOTH`, the proposed topological smoothing package;
- `M0580-T-SMOOTH-POINCARE`, the proposed smooth three-dimensional Poincare package.

`root_of_smoothing_and_smooth_poincare` assumes both packages and only composes them. The diagnostic
`smoothThreeDimensionalPoincare_of_perelmanPoincareTarget` runs from the root back to the second
package, so using it to manufacture a premise for the root would be circular.

Pinned mathlib supplies the matching generalized, topological, and smooth signatures only through
`proof_wanted`. The pinned Batteries implementation elaborates such signatures inside
`withoutModifyingEnv`; it deliberately discards all three constants. The trust-zero probe confirms
that they are unknown after import. Current scoped searches found no alternate retained body, and
the immutable external audit contains only a three-dimensional statement plus an unrelated
dimension-zero proof.

## First Failed Gate

The structured prerequisite is not dependency-legal. `task-dag.json` still marks `STATEMENT`,
`ANCHOR_AUDIT`, and `OBLIGATION_TREE` open, even though the generated checklist shows provisional
worker artifacts. A proof worker cannot accept or reconcile prerequisite state.

The frozen proof architecture also needs a new append-only revision before node-level implementation:

- `TopologicalThreeManifoldSmoothable` receives an already selected `ChartedSpace` and asks for
  `Nonempty (IsManifold ... M)` for that atlas. This is not existence of a replacement compatible
  smooth atlas; wrapping a proposition in `Nonempty` selects no atlas.
- `SmoothThreeDimensionalPoincare` concludes the same homeomorphism as the root under an extra
  `IsManifold` instance. The root therefore implies this package directly. It does not encode the
  distinct diffeomorphism-valued smooth result described by the graph prose and legacy boundary.
- `C-METRIC` through `L-PI1-ELIMINATION` have `planned ...` prose strings, not exact Lean formal
  targets, and no owned Lean sources. Their recipes only rerun the structural registry validator;
  they cover no declarations.

Silently replacing these contracts would violate the frozen-registry rule and this proof worker's
phase authority. Even after correction, the Ricci-flow, surgery, extinction, decomposition, and
fundamental-group packages remain unformalized in the pinned closure.

## Validation

All commands ran in this worker clone. Lean outputs were confined to a disposable `/tmp` directory
and removed. The automation-provided untracked `.lake` symlink was reused read-only. No `lake
update`, `lake build`, dependency clone/fetch, or dependency mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; planned; L0/rework-required; theorem incomplete |
| isolated trust-zero `lake env lean` chain below | 0 | statement, conditional composition, and blocker probe elaborated; both local theorem axiom reports were `[propext, Classical.choice, Quot.sound]`; all three `proof_wanted` names were absent |
| `python3 Stage1_Instances/THM-M-0580/check_statement.py` | 0 | expression hash `938ef54298273a011a66395812b53e6bf8071b0925b84cd94ae5fb4f9a6eb664`; all four structural mutations killed; pinned toolchain and mathlib revision matched |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root remains open at M4 |
| scoped exact-root/cut-set and Poincare searches with `rg` | 0 | no repo-local terminal body; pinned packages expose only three relevant `proof_wanted` markers |
| inverted prohibited-construct `rg --pcre2` scan of the four owned Lean modules | 0 | no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `external` token |
| `cd Formalizations/Lean && timeout 60 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `python3 -m json.tool Stage1_Instances/THM-M-0580/proof-recheck-2026-07-15-head-111bbeb1.json` | 0 | companion blocker record parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-0580` | 0 | no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | required self-test manifest is absent because proof completion failed |

The narrow Lean check was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0580
tmp=$(mktemp -d /tmp/thm-m-0580-slot28-head111bbeb1.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_bin=$(cd "$lean_root" && lake env which lean)
base_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$base_path" \
  timeout 300 "$lean_bin" --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" \
  timeout 300 "$lean_bin" --trust=0 -t0 -o "$tmp/ObligationTree.olean" ObligationTree.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" \
  timeout 300 "$lean_bin" --trust=0 -t0 ProofBlockerProbe.lean
```

This produced `Statement.olean` SHA-256
`8c69718898cfefd3f33ccce0ac95ca8f4e9a82bc28fda79b6b91ae01b7cffba6` and
`ObligationTree.olean` SHA-256
`6f2ad414a2fe0d0dd9544cc489751163408ac7b85a9823e3935ff1663af7dcb8`.

## Retry Condition

First reconcile and accept the prerequisite task state. Then publish an append-only obligation-tree
revision with a replacement-atlas smoothing contract, faithful smooth-package semantics, exact Lean
targets for every child, checked composition, and declaration-covering recipes. Implement those
corrected packages without placeholders. Alternatively, integrate an immutable, licensed,
compatible exact-root Lean 4 proof with a complete dependency lock and exact-type/provenance checks.

Assuming either missing package, treating `proof_wanted` as an axiom, or presenting conditional
composition as root closure would violate the exact-target and proof-body gates. This is an owned
blocker artifact, not a proof receipt; it does not satisfy `S56-M-0580-PROOF` or support theorem
completion. Because the phase is not genuinely complete, `.stage1-worker-selftest.json` remains
absent.
