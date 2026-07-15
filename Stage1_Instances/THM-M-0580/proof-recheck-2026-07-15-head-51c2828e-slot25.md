# THM-M-0580 proof-phase recheck at base 51c2828e (slot 25)

Item: `S56-M-0580-PROOF`

Recorded: `2026-07-15T16:25:20+08:00`

Base revision: `51c2828e82ffb19860830f78b771f80e13ad7dff`

Base tree: `4655b8b40829513de6fb5661344b33fc7cd17cd1`

## Verdict

`blocked`. Proof execution is not dependency-legal: the target-local state authority has
`accepted_states: []` and records `S56-M-0580-OBLIGATION_TREE` as open. The generated blueprint's
`[_]` marker is provisional worker output, not master acceptance of that prerequisite.

Independently, no eligible terminal Lean 4 proof body exists in this checkout or its pinned
dependency closure for the exact proposition
`Stage1Instances.THM_M_0580.PerelmanPoincareTarget`. The frozen immediate root cut set remains:

- `M0580-N-SMOOTH`, compatible smoothing of the fixed topological manifold;
- `M0580-T-SMOOTH-POINCARE`, the full smooth three-dimensional Poincare package.

`root_of_smoothing_and_smooth_poincare` assumes both packages and checks only their conditional
composition. `smoothThreeDimensionalPoincare_of_perelmanPoincareTarget` derives the second package
from the exact root, so using that converse to construct a root premise would be circular.

The prerequisite proof architecture also needs an append-only correction before node-level proof
work can be credited. `TopologicalThreeManifoldSmoothable` quantifies over an already selected
`ChartedSpace` and asks whether that atlas satisfies `IsManifold`; `Nonempty` around this proposition
does not select a replacement smooth atlas or record compatibility. `SmoothThreeDimensionalPoincare`
is the root homeomorphism under an extra `IsManifold` instance rather than a faithful
diffeomorphism-valued smooth theorem. The metric, Ricci-flow, noncollapse, canonical-neighborhood,
surgery, extinction, decomposition, and fundamental-group children still have planned fingerprints
rather than exact Lean propositions and own no terminal proof bodies.

Pinned mathlib contains the generalized, topological, and smooth signatures only as `proof_wanted`.
Batteries elaborates those statements inside `withoutModifyingEnv` and discards them. Trust-zero
elaboration confirms that all three matching names are unknown after import. Scoped repository
searches found only statement surfaces, conditional wrappers, blocker probes, and metadata.

A fresh bounded external search located
`frenzymath/Poincare-Conjecture@2d6abb09774efc7c1a5059f7e78b8679db3be6d2`. The immutable Apache-2.0
source describes itself as an active, incomplete beta formalization. Its Morgan-Tian track pins Lean
`v4.30.0-rc2` and mathlib `5fc0241932dd6d465bc5549308cc39011772293a`, contains 141 Lean files, and
describes its implemented surface as the first two chapters. A focused declaration search found no
exact or root-like Poincare theorem. It is useful future partial infrastructure, not an importable
terminal body, and was inspected read-only in `/tmp`; it was not added as a dependency.

No proof body or completion receipt was added. The item remains `[ ]`; the root vector remains
`[H2, M4, R4]`; `audit_complete`, root closure, and theorem completion remain false.

## Validation

All commands ran in this worker clone. The automation-provided canonical `.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, or dependency mutation was run.
Lean outputs and the external archive inspection were confined to disposable `/tmp` directories.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; lifecycle `planned`; baseline L0/rework-required; theorem incomplete |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-0580/check_statement.py` | 0 | expression SHA-256 `938ef54298273a011a66395812b53e6bf8071b0925b84cd94ae5fb4f9a6eb664`; all four mutations killed; pinned toolchain and mathlib revision matched |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root open at M4 |
| isolated trust-zero `lake env lean` chain below | 0 | statement, conditional composition, and blocker probe elaborated; local theorem axiom reports were `[propext, Classical.choice, Quot.sound]`; all three `proof_wanted` names were unknown |
| inverted forbidden-construct scan over the four owned Lean modules | 0 | no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `external` token matched |
| pinned Poincare-module and Batteries implementation search | 0 | exactly three relevant `proof_wanted` entries; implementation uses `withoutModifyingEnv` and discards them |
| scoped retained-declaration inventory | 0 | no exact-root or root-cut terminal body; only definitions, statement transport, conditional composition, diagnostic converse, and string metadata matched |
| `cd Formalizations/Lean && timeout --foreground --kill-after=5s 60s lake env lean --version` plus pin probes | 0 | Lean 4.29.0 commit `98dc76e3`; mathlib `8a178386` / tree `bdc39a31`; Batteries `756e3321` / tree `02666252` |
| read-only immutable `frenzymath/Poincare-Conjecture` archive probe | 0 | HEAD and immutable revision `2d6abb09`; archive SHA-256 `4497ee68...15de1`; 141 Morgan-Tian Lean files; project explicitly incomplete; no exact or root-like declaration |
| `jq -e` plus blocker invariant checks | 0 | structured artifact parsed; item, blocked outcome, open state, noncompletion fields, and changed paths agreed |
| `git diff --check -- Stage1_Instances/THM-M-0580/proof-recheck-2026-07-15-head-51c2828e-slot25.{json,md}` | 0 | no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest absent because the proof phase is not complete |

The narrow Lean check was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0580
tmp=$(mktemp -d /tmp/thm-m-0580-slot25-head51c2828e.XXXXXX)
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

First master-accept a corrected prerequisite. That requires an append-only obligation-tree revision
with replacement-atlas smoothing data and compatibility, faithful diffeomorphism-valued smooth
semantics, exact Lean targets for every proof child, checked composition, and declaration-covering
recipes. Then implement the corrected smoothing and complete smooth-Poincare packages without
placeholders. Alternatively, integrate an immutable, licensed, compatible exact-root Lean 4 proof
with a complete dependency lock and exact-type, provenance, and trust checks.

This dossier contained 37 earlier structured proof rechecks before this attempt. Under the rev-5.6
five-tick rule, the master should split this oversized proof item into dependency-legal child tasks
rather than reschedule the unchanged root. The fresh external project may be re-audited as partial
infrastructure after it publishes relevant declarations, but its current incomplete state supplies
no proof credit. This proof worker has no authority to edit the DAG or prerequisite artifacts.

Assuming either missing package, treating `proof_wanted` as an axiom, presenting conditional
composition as root closure, or pinning an explicitly incomplete external project as a terminal body
would violate the exact-target and proof-body gates. This is an owned blocker artifact, not a proof
receipt. It does not satisfy `S56-M-0580-PROOF`, propose state promotion, or support theorem
completion. Because the assigned phase is not genuinely complete, `.stage1-worker-selftest.json`
remains absent.
