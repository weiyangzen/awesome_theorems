# THM-M-0580 proof-phase recheck at base 3f5b3108 (slot 22)

Item: `S56-M-0580-PROOF`

Recorded: `2026-07-15T14:56:46+08:00`

Base revision: `3f5b310884eb802487a4c901cb0d76752e368da0`

Base tree: `a1bb0a117c463908411f55d51fdb5ed25c457ab0`

## Verdict

`blocked`. The proof node is not dependency-legal: its prerequisite
`S56-M-0580-OBLIGATION_TREE` is only worker-self-tested `[_]`, not master-accepted `[x]`.
The target's structured `task-dag.json` likewise has `accepted_states: []` and still records that
prerequisite as `open`.

Independently, no eligible terminal Lean 4 proof body exists in the repository or pinned dependency
closure for the exact declaration
`Stage1Instances.THM_M_0580.PerelmanPoincareTarget`. The immediate frozen root cut set remains:

- `M0580-N-SMOOTH`, the proposed topological smoothing package;
- `M0580-T-SMOOTH-POINCARE`, the proposed smooth three-dimensional Poincare package.

`root_of_smoothing_and_smooth_poincare` assumes both packages and only composes them. The diagnostic
`smoothThreeDimensionalPoincare_of_perelmanPoincareTarget` runs from the root back to the second
package, so using it to construct a root premise would be circular.

The frozen smoothing proposition is also not a faithful replacement-atlas contract. It receives an
already selected `ChartedSpace Euclidean3 M` instance and asks for `Nonempty (IsManifold ... M)` for
that atlas. Wrapping this proposition in `Nonempty` selects no replacement atlas or compatibility
bridge. Correcting it requires an append-only prerequisite registry revision, not a silent proof-
phase substitution. The Ricci-flow, surgery, extinction, decomposition, and fundamental-group
children still have planned fingerprints rather than exact Lean propositions and proof bodies.

Pinned mathlib supplies the matching generalized, topological, and smooth signatures only through
`proof_wanted`. The pinned Batteries implementation elaborates each signature inside
`withoutModifyingEnv` and discards it, explicitly preventing its use as an axiom. The trust-zero
probe confirms all three names are unknown after import. Scoped retained-declaration searches found
no alternate exact-root or cut-set body. The prerequisite immutable external audit found only a
dimension-three statement and a dimension-zero proof, not a dimension-three terminal body.

No proof body or completion receipt was added. The item remains `[ ]`, the root remains
`[H2, M4, R4]`, and audit completion, root closure, and theorem completion remain false.

## Validation

All commands ran in this worker clone. The automation-provided canonical `.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, or dependency mutation was run.
Lean outputs were confined to a disposable `/tmp` directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; planned; L0/rework-required; theorem incomplete |
| isolated trust-zero `lake env lean` chain below | 0 | exact statement, conditional composition, and blocker probe elaborated; local theorem axiom reports were `[propext, Classical.choice, Quot.sound]`; all three `proof_wanted` names were absent |
| `python3 Stage1_Instances/THM-M-0580/check_statement.py` | 0 | expression SHA-256 `938ef54298273a011a66395812b53e6bf8071b0925b84cd94ae5fb4f9a6eb664`; all four mutations killed; pinned toolchain and mathlib revision matched (final isolated rerun completed in about 207 seconds) |
| `python3 Stage1_Instances/THM-M-0580/check_anchor_audit.py` | 0 | exact statement anchors remain bodyless; audited external root remains statement-only; root remains M4 |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root open at M4 |
| scoped retained-declaration search | 0 | no exact-root or cut-set body; the only three matching pinned entries are `proof_wanted` markers |
| inverted prohibited-construct scan | 0 | no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `external` token in the four owned Lean modules |
| `cd Formalizations/Lean && timeout 60 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| dependency pin and cleanliness probes | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` / tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; Batteries `756e3321fd3b02a85ffda19fef789916223e578c` / tree `02666252fd943c970ee0b7a66ec65a2e5efe7230`; both worktrees clean |

The narrow Lean validation command was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0580
tmp=$(mktemp -d /tmp/thm-m-0580-slot22-head3f5b310.XXXXXX)
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

This owned dossier already contained 33 earlier structured blocker rechecks for this proof item at
the start of this attempt. Under the rev-5.6 five-tick rule, the master should split this oversized
item into dependency-legal child tasks instead of rescheduling the unchanged root. This proof worker
has no authority to edit the execution DAG.

Assuming either missing package, treating `proof_wanted` as an axiom, or presenting conditional
composition as root closure would violate the exact-target and proof-body gates. This is an owned
blocker artifact, not a proof receipt. It does not satisfy `S56-M-0580-PROOF`, propose state
promotion, or support theorem completion. Because the assigned phase is not genuinely complete,
`.stage1-worker-selftest.json` remains absent.
