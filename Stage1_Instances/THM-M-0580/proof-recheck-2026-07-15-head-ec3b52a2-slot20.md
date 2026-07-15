# THM-M-0580 proof-phase recheck at base ec3b52a2

Item: `S56-M-0580-PROOF`

Recorded: `2026-07-15T14:37:15+08:00`

Base revision: `ec3b52a20f5e28de012c23dce1af403343b9a1cb`

Base tree: `b08b83715d8f74868d1f31bbe82a7951b26edad1`

## Verdict

`blocked`. The proof node is not dependency-legal: its prerequisite
`S56-M-0580-OBLIGATION_TREE` is only worker-self-tested `[_]`, not master-accepted `[x]`.
Independently, no eligible terminal Lean 4 proof body exists in the repository or pinned dependency
closure for the exact declaration
`Stage1Instances.THM_M_0580.PerelmanPoincareTarget`.

The immediate frozen root cut set remains:

- `M0580-N-SMOOTH`, the proposed topological smoothing package;
- `M0580-T-SMOOTH-POINCARE`, the proposed smooth three-dimensional Poincare package.

`root_of_smoothing_and_smooth_poincare` assumes both packages and only composes them. The diagnostic
`smoothThreeDimensionalPoincare_of_perelmanPoincareTarget` runs from the root back to the second
package, so using it to construct a root premise would be circular.

The frozen smoothing proposition is also not a faithful replacement-atlas contract. It receives an
already selected `ChartedSpace Euclidean3 M` instance and asks for `Nonempty (IsManifold ... M)` for
that atlas. Wrapping this proposition in `Nonempty` selects no replacement atlas or compatibility
bridge. Correcting it requires an append-only prerequisite registry revision, not a silent proof-
phase substitution.

Pinned mathlib supplies the matching generalized, topological, and smooth signatures only through
`proof_wanted`. The pinned Batteries implementation elaborates each signature inside
`withoutModifyingEnv` and then discards it. The trust-zero probe confirms all three names are
unknown after import. Scoped retained-declaration searches found no alternate exact-root or cut-set
body. The substantive metric, Ricci-flow, surgery, extinction, decomposition, and fundamental-group
children still have planned fingerprints rather than exact Lean propositions and proof bodies.

No proof body or completion receipt was added. The item remains `[ ]`, the root remains
`[H2, M4, R4]`, and audit completion, root closure, and theorem completion remain false.

## Validation

All commands ran in this worker clone. The automation-provided canonical `.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, or dependency mutation was run.
Lean output was confined to a disposable `/tmp` directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; planned; L0/rework-required; theorem incomplete |
| isolated trust-zero `lake env lean` chain below | 0 | exact statement, conditional composition, and blocker probe elaborated; local theorem axiom reports were `[propext, Classical.choice, Quot.sound]`; all three `proof_wanted` names were absent |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root open at M4 |
| scoped retained-declaration search | 0 | inverted no-match check passed; no exact-root or cut-set body and no retained declaration for the three `proof_wanted` names |
| inverted prohibited-construct scan | 0 | no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `external` token in the four owned Lean modules |
| toolchain and pin probes | 0 | Lean 4.29.0 commit `98dc76e3...`; mathlib `8a178386...` / tree `bdc39a31...`; Batteries `756e3321...` / tree `02666252...`; both dependency worktrees clean |

The narrow Lean validation command was:

```bash
set -euo pipefail
repo=$PWD
lean_root="$repo/Formalizations/Lean"
target="$repo/Stage1_Instances/THM-M-0580"
tmp=$(mktemp -d /tmp/thm-m-0580-ec3b52a2-slot20.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
paths=("$lean_root/.lake/build/lib/lean")
for p in "$lean_root"/.lake/packages/*/.lake/build/lib/lean; do paths+=("$p"); done
lean_path=$(IFS=:; printf '%s' "${paths[*]}")
cd "$target"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 -o "$tmp/ObligationTree.olean" ObligationTree.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 ProofBlockerProbe.lean
sha256sum "$tmp/Statement.olean" "$tmp/ObligationTree.olean"
```

The temporary olean SHA-256 values were
`8c69718898cfefd3f33ccce0ac95ca8f4e9a82bc28fda79b6b91ae01b7cffba6` and
`6f2ad414a2fe0d0dd9544cc489751163408ac7b85a9823e3935ff1663af7dcb8`.

## Retry Condition

First publish and master-accept an append-only obligation-tree revision with a compatible
replacement-atlas smoothing contract, exact Lean targets for every proof child, checked
composition, and declaration-covering recipes. Then implement the corrected smoothing package and
the complete smooth-Poincare package without placeholders. Alternatively, integrate an immutable,
licensed, compatible exact-root Lean 4 proof with a complete dependency lock and exact-type,
provenance, and trust checks.

Assuming either missing package, treating `proof_wanted` as an axiom, or presenting conditional
composition as root closure would violate the exact-target and proof-body gates. This is an owned
blocker artifact, not a proof receipt. It does not satisfy `S56-M-0580-PROOF`, propose state
promotion, or support theorem completion. Because the assigned phase is not genuinely complete,
`.stage1-worker-selftest.json` remains absent.
