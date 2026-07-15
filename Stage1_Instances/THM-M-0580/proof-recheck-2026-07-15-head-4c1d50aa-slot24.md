# THM-M-0580 Proof Recheck: Current-Base Blocker Handoff

## Scope and Verdict

This is proof-phase evidence for `S56-M-0580-PROOF` at base
`4c1d50aa6552eb6ec56338a663a5dff79a4ae2e3` (tree
`e38ee217e0bb768c5c915905d1d0b04fc89e25f2`). The exact target is
`Stage1Instances.THM_M_0580.PerelmanPoincareTarget`, expression SHA-256
`938ef54298273a011a66395812b53e6bf8071b0925b84cd94ae5fb4f9a6eb664`.

The attempt is `blocked`. The target-local task authority still has `accepted_states=[]` and
records `S56-M-0580-OBLIGATION_TREE` as open, so the proof item is not dependency-legal for master
acceptance. The generated checklist's `[_]` prerequisite marker is provisional worker state and
does not override the structured authority.

Independently, the immediate root cut set remains `M0580-N-SMOOTH` and
`M0580-T-SMOOTH-POINCARE`. Neither obligation has an eligible terminal body. The checked theorem
`root_of_smoothing_and_smooth_poincare` assumes both open packages; it is conditional composition,
not a proof of either premise or of the root. The diagnostic theorem
`smoothThreeDimensionalPoincare_of_perelmanPoincareTarget` derives the second package from the exact
root, so using it to construct a root premise would be circular.

The prerequisite proof architecture also remains unsuitable for faithful child execution:

- `TopologicalThreeManifoldSmoothable` checks `IsManifold` for an already selected `ChartedSpace`;
  it does not carry a replacement smooth atlas and a compatibility bridge.
- `SmoothThreeDimensionalPoincare` concludes the root homeomorphism after adding an `IsManifold`
  instance; it is not the diffeomorphism-valued smooth theorem described by the source anchor.
- The Ricci-flow, surgery, extinction, decomposition, and fundamental-group children retain
  planned fingerprints rather than exact Lean propositions and have no terminal proof bodies.

Pinned mathlib contains the three relevant signatures only as `proof_wanted` commands. Batteries
elaborates these inside `withoutModifyingEnv` and discards the helper declaration, explicitly
preventing use as axioms. The trust-zero probe confirms all three names are unknown after import.
Scoped searches across all pinned package Lean sources and repository-local Lean sources found no
alternate exact-root or cut-set proof body.

No proof body or completion receipt was added. The item remains `[ ]`, lifecycle remains `planned`,
the root vector remains `[H2, M4, R4]`, and `audit_complete`, root closure, and theorem completion
remain false. The only target-path change from base `d44ed2b1` to this base was integration of the
immediately preceding blocker packet; the statement, registry, task state, proof modules, pins, and
their hashes did not change.

## Validation

All commands ran in this worker clone. The automation-provided canonical `.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, or dependency mutation was run.
Lean outputs were confined to a disposable `/tmp` directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; lifecycle `planned`; L0/rework-required; theorem incomplete |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-0580/check_statement.py` | 0 | expression SHA-256 matched; all four structural mutations were killed; pinned toolchain and mathlib revision matched |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root open at M4 |
| isolated trust-zero `lake env lean` chain below | 0 | statement, conditional composition, and blocker probe elaborated; local theorem axioms were `[propext, Classical.choice, Quot.sound]`; all three `proof_wanted` names were unknown |
| target-local prerequisite-state assertion | 0 | `accepted_states=[]`; `S56-M-0580-OBLIGATION_TREE=open` |
| pinned and repository-local retained-declaration searches | 0 | the sole pinned source match was mathlib's Poincare module; the only local definition matches were the three owned modules; no exact-root or cut-set body exists |
| inverted prohibited-construct scan over the four owned Lean modules | 0 | no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `external` token matched |
| `cd Formalizations/Lean && timeout 60 lake env lean --version` plus dependency revision/tree/status probes | 0 | Lean 4.29.0 commit `98dc76e3`; mathlib `8a178386` / tree `bdc39a31`, clean; Batteries `756e3321` / tree `02666252`, clean |
| substantive-input comparison against `d44ed2b1` | 0 | all target statement, proof, registry, graph, validation, and task-state inputs were unchanged; only the prior blocker packet was integrated |
| `python3 -m json.tool ...slot24.json`, blocker-invariant `jq -e`, and `git diff --check` | 0 | blocker JSON parsed; item/base/open/noncompletion/change-path invariants agreed; both owned artifacts had no whitespace errors |
| scoped worktree and `test ! -e .stage1-worker-selftest.json` | 0 | only this owned blocker pair was added apart from the pre-existing canonical `.lake` symlink; the self-test manifest is absent because proof is incomplete |

The narrow Lean validation used only the pinned toolchain and existing compiled artifacts:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0580
tmp=$(mktemp -d /tmp/thm-m-0580-slot24-head4c1d50aa.XXXXXX)
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

Temporary olean SHA-256 values were
`8c69718898cfefd3f33ccce0ac95ca8f4e9a82bc28fda79b6b91ae01b7cffba6` for
`Statement.olean` and
`6f2ad414a2fe0d0dd9544cc489751163408ac7b85a9823e3935ff1663af7dcb8` for
`ObligationTree.olean`.

## Retry Condition

First reconcile and master-accept the prerequisite state. Then publish an append-only
obligation-tree revision with compatible replacement-atlas smoothing data, faithful smooth-
Poincare semantics, exact Lean targets for every proof child, checked composition, and declaration-
covering validation recipes. Implement those corrected packages without placeholders.
Alternatively, integrate an immutable, licensed, compatible exact-root Lean 4 proof with a complete
dependency lock and exact-type, provenance, and trust checks.

There were 46 earlier structured `proof-recheck` packets before this attempt, far beyond the five-
tick threshold. Section 10.2 therefore requires the master to split this oversized proof item into
smaller dependency-legal child tasks instead of rescheduling the unchanged root item. A proof worker
cannot edit the authoritative DAG.

This is an owned blocker handoff, not a proof receipt. It does not satisfy `S56-M-0580-PROOF`,
propose state promotion, or support theorem completion. Because the assigned proof phase is not
genuinely complete, `.stage1-worker-selftest.json` remains absent.
