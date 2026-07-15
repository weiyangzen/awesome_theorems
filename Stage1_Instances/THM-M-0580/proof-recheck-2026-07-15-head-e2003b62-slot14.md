# THM-M-0580 proof-phase recheck at base e2003b62 (slot 14)

Item: `S56-M-0580-PROOF`

Recorded: `2026-07-15T17:19:03+08:00`

Base revision: `e2003b62b5f0ceb98b13c8e76e1753e6cf38dda6`

Base tree: `803084183e6ae6e2d6cf35c89dbdce8820a80e6d`

## Verdict

`blocked`. Provisional proof preparation is permitted, but proof acceptance is not dependency-legal.
The target-local task-state authority remains `planned`, has `accepted_states: []`, and records
`S56-M-0580-OBLIGATION_TREE` as `open`. The blueprint's `[_]` marker for that prerequisite is
provisional worker output, not master acceptance.

Independently, the exact proposition
`Stage1Instances.THM_M_0580.PerelmanPoincareTarget` has no eligible terminal Lean 4 proof body in
this checkout or its pinned dependency closure. Its immediate root cut set remains:

- `M0580-N-SMOOTH`, a compatible topological smoothing package;
- `M0580-T-SMOOTH-POINCARE`, the complete smooth three-dimensional Poincare theorem.

The checked theorem `root_of_smoothing_and_smooth_poincare` assumes both packages and only composes
them. The diagnostic theorem `smoothThreeDimensionalPoincare_of_perelmanPoincareTarget` derives the
second package from the exact root, so using it to construct a root premise would be circular.

The prerequisite architecture also needs append-only repair before proof work can be credited.
`TopologicalThreeManifoldSmoothable` quantifies over an already selected `ChartedSpace` and asks
whether that atlas satisfies `IsManifold`; it supplies neither replacement-atlas data nor a checked
compatibility bridge. `SmoothThreeDimensionalPoincare` concludes the root homeomorphism under an
extra `IsManifold` instance rather than the diffeomorphism-valued smooth theorem. Its metric,
Ricci-flow, noncollapse, canonical-neighborhood, surgery, extinction, decomposition, and
fundamental-group children have planned fingerprints rather than exact Lean propositions and own
no terminal proof bodies.

Pinned mathlib has the generalized, topological-three, and smooth-three signatures only as
`proof_wanted` entries. Batteries elaborates these inside `withoutModifyingEnv` and explicitly
discards them, so they cannot be used as axioms. Trust-zero elaboration confirms that all three
names are unknown after import. Scoped source searches found no retained exact-root or root-cut
theorem in the repository or pinned packages.

No proof body or receipt was added. The item remains `[ ]`, lifecycle remains `planned`, the root
vector remains `[H2, M4, R4]`, and audit completion, root closure, and theorem completion remain
false.

## Validation

All commands ran in this worker clone. The automation-provided canonical `.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, or dependency mutation was run.
Lean output was confined to a disposable `/tmp` directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; lifecycle `planned`; L0/rework-required; theorem incomplete |
| `timeout 300 python3 Stage1_Instances/THM-M-0580/check_statement.py` | 0 | expression SHA-256 `938ef54298273a011a66395812b53e6bf8071b0925b84cd94ae5fb4f9a6eb664`; all four mutations killed; pinned toolchain and mathlib revision matched |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root open at M4 |
| isolated trust-zero `lake env lean` chain below | 0 | statement, conditional composition, and blocker probe elaborated; local theorem axioms were `[propext, Classical.choice, Quot.sound]`; all three `proof_wanted` names were unknown |
| inverted prohibited-construct scan over the four owned Lean modules | 0 | no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `external` token matched |
| retained-declaration search plus pinned Poincare/Batteries source inspection | 0 | no exact-root or cut-set body; the three matching mathlib entries are discarded `proof_wanted` markers |
| `cd Formalizations/Lean && timeout --foreground --kill-after=5s 60s lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| pinned dependency revision/tree and clean-tree probes | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` / tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; Batteries `756e3321fd3b02a85ffda19fef789916223e578c` / tree `02666252fd943c970ee0b7a66ec65a2e5efe7230`; both clean |

The narrow Lean validation used the pinned toolchain and existing compiled artifacts:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0580
tmp=$(mktemp -d /tmp/thm-m-0580-slot14-heade2003b62.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
paths=("$lean_root/.lake/build/lib/lean")
for p in "$lean_root"/.lake/packages/*/.lake/build/lib/lean; do paths+=("$p"); done
lean_path=$(IFS=:; printf '%s' "${paths[*]}")
cd "$target"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 \
  -o "$tmp/Statement.olean" Statement.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 \
  -o "$tmp/ObligationTree.olean" ObligationTree.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout --foreground --kill-after=5s 300s lake env lean --trust=0 -t0 ProofBlockerProbe.lean
sha256sum "$tmp/Statement.olean" "$tmp/ObligationTree.olean"
```

The temporary olean SHA-256 values were
`8c69718898cfefd3f33ccce0ac95ca8f4e9a82bc28fda79b6b91ae01b7cffba6` for
`Statement.olean` and
`6f2ad414a2fe0d0dd9544cc489751163408ac7b85a9823e3935ff1663af7dcb8` for
`ObligationTree.olean`.

## Retry Condition

First publish and master-accept an append-only prerequisite revision with replacement-atlas
smoothing data and compatibility, a faithful diffeomorphism-valued smooth theorem, exact Lean
targets for every proof child, checked composition, and declaration-covering recipes. Then
implement the corrected smoothing and complete smooth-Poincare packages without placeholders.
Alternatively, integrate an immutable, licensed, compatible exact-root Lean 4 proof with complete
dependency lock, exact-type, provenance, and trust checks.

There were 39 prior structured `proof-recheck` packets before this attempt. The rev-5.6 five-tick
rule therefore requires the master to split this oversized root proof item into dependency-legal
child tasks rather than reschedule the unchanged item. This proof worker cannot edit the DAG.

This is an owned blocker packet, not a proof receipt. It does not satisfy `S56-M-0580-PROOF`,
propose a state promotion, or support theorem completion. Because the assigned proof phase is not
genuinely complete, `.stage1-worker-selftest.json` remains absent.
