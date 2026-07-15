# THM-M-0580 proof-phase recheck at base b366bdd9 (slot 29)

Item: `S56-M-0580-PROOF`

Recorded: `2026-07-15T19:55:53+08:00`

Base revision: `b366bdd9f72217b5465ccd19133760b911ed0b58`

Base tree: `987b635fe76400c0818b485a6e5fc7a7067311e4`

## Verdict

`blocked`. Proof execution is not dependency-legal. The target-local structured state authority,
`task-dag.json`, has `accepted_states: []` and records `S56-M-0580-OBLIGATION_TREE` as open. The
generated blueprint's `[_]` marker is unfinished worker output rather than master acceptance of the
prerequisite.

There is also no eligible terminal Lean 4 proof body in this checkout or its pinned dependency
closure for the exact proposition `Stage1Instances.THM_M_0580.PerelmanPoincareTarget`. The frozen
immediate root cut set remains:

- `M0580-N-SMOOTH`, compatible smoothing of the topological three-manifold;
- `M0580-T-SMOOTH-POINCARE`, the complete smooth three-dimensional Poincare package.

`root_of_smoothing_and_smooth_poincare` assumes both packages and checks only conditional
composition. `smoothThreeDimensionalPoincare_of_perelmanPoincareTarget` derives the second package
from the exact root, so using it to construct a root premise would be circular.

The prerequisite architecture also needs an append-only correction before node-level proof work can
be credited. `TopologicalThreeManifoldSmoothable` quantifies over an already selected
`ChartedSpace` and asks whether that atlas satisfies `IsManifold`; `Nonempty` around this proposition
does not select a replacement smooth atlas or record compatibility. `SmoothThreeDimensionalPoincare`
is the root homeomorphism under an extra `IsManifold` instance rather than the faithful
diffeomorphism-valued smooth theorem. The metric, Ricci-flow, noncollapse, canonical-neighborhood,
surgery, extinction, decomposition, and fundamental-group children still have planned fingerprints
rather than exact Lean propositions and own no terminal proof bodies.

Pinned mathlib contains the generalized, topological, and smooth Poincare signatures only as
`proof_wanted`. Batteries elaborates these statements inside `withoutModifyingEnv` and discards
them. Trust-zero elaboration confirms that all three matching names are unknown after import. A
scoped repository and pinned-package search found only statement surfaces, conditional wrappers,
blocker probes, and the single mathlib `proof_wanted` source module; it found no exact-root or
root-cut terminal declaration.

No proof body or completion receipt was added. The item remains `[ ]`; the root vector remains
`[H2, M4, R4]`; `audit_complete`, root closure, and theorem completion remain false.

## Validation

All commands ran in this worker clone. The automation-provided canonical `.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, or dependency mutation was run.
Lean outputs were confined to and removed with a disposable `/tmp` directory.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; lifecycle `planned`; baseline L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0580/check_statement.py` | 0 | expression SHA-256 `938ef54298273a011a66395812b53e6bf8071b0925b84cd94ae5fb4f9a6eb664`; all four mutations killed; pinned toolchain and mathlib revision matched |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root open at M4 |
| `python3 Stage1_Instances/THM-M-0580/check_anchor_audit.py` | 0 | exact statement anchors remain bodyless; external dimension-three root is statement-only; root M4 |
| isolated trust-zero `lake env lean` chain below | 0 | statement, conditional composition, and blocker probe elaborated; local theorem axiom reports were `[propext, Classical.choice, Quot.sound]`; all three `proof_wanted` names were unknown |
| inverted forbidden-construct scan over the four owned Lean modules | 0 | no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `external` token matched |
| scoped retained-declaration and pinned-package search | 0 | no exact-root or root-cut terminal body; only definitions, statement transports, conditional composition, diagnostic converse, and one mathlib `proof_wanted` module were found |
| `cd Formalizations/Lean && timeout 60 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| pinned dependency revision/tree/cleanliness probes | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` / tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; Batteries `756e3321fd3b02a85ffda19fef789916223e578c` / tree `02666252fd943c970ee0b7a66ec65a2e5efe7230`; both clean |
| `python3 -m json.tool Stage1_Instances/THM-M-0580/proof-recheck-2026-07-15-head-b366bdd9-slot29.json` | 0 | structured blocker artifact is valid JSON |
| `jq -e <blocked-state invariants> Stage1_Instances/THM-M-0580/proof-recheck-2026-07-15-head-b366bdd9-slot29.json` | 0 | item/target identity, blocked outcome, false completion flags, two changed paths, known failures, and absent self-test claim agreed |
| `git diff --check -- Stage1_Instances/THM-M-0580/proof-recheck-2026-07-15-head-b366bdd9-slot29.{md,json}` | 0 | no whitespace errors |

The narrow Lean check was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0580
tmp=$(mktemp -d /tmp/thm-m-0580-slot29-headb366bdd9.XXXXXX)
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
`8c69718898cfefd3f33ccce0ac95ca8f4e9a82bc28fda79b6b91ae01b7cffba6` for
`Statement.olean` and
`6f2ad414a2fe0d0dd9544cc489751163408ac7b85a9823e3935ff1663af7dcb8` for
`ObligationTree.olean`.

## Retry Condition

First publish and master-accept an append-only obligation-tree correction with compatible
replacement-atlas data, a faithful smooth theorem, exact Lean targets for every proof child,
checked composition, and declaration-covering recipes. Then implement the corrected smoothing and
complete smooth-Poincare packages without placeholders. Alternatively, integrate an immutable,
licensed, compatible exact-root Lean 4 proof with a complete dependency lock and exact-type,
provenance, and trust checks.

This dossier already contained 47 structured proof-blocker rechecks before this attempt. Under the
rev-5.6 five-tick rule, the master should split this oversized proof item into dependency-legal
child tasks rather than reschedule the unchanged root. This proof worker has no authority to edit
the DAG.

Assuming either missing package, treating `proof_wanted` as an axiom, or presenting conditional
composition as root closure would violate the exact-target and proof-body gates. This is an owned
blocker artifact, not a proof receipt. It does not satisfy `S56-M-0580-PROOF`, propose state
promotion, or support theorem completion. Because the assigned phase is not genuinely complete,
`.stage1-worker-selftest.json` remains absent.
