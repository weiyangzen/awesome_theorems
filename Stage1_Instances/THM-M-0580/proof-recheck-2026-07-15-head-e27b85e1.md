# THM-M-0580 proof-phase recheck at base e27b85e1

Item: `S56-M-0580-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `e27b85e1503047c5e4bd8d5410b6fba5c4dda896`

Base tree: `29c625431b9c241bce6286123205defcbd1e7f7e`

## Verdict

`blocked`. No eligible terminal Lean 4 proof body exists in the repository or pinned dependency
closure for the exact proposition
`Stage1Instances.THM_M_0580.PerelmanPoincareTarget`. This attempt adds only a diagnostic,
non-closing proof body and leaves the root vector at `[H2, M4, R4]`. The proof item remains `[ ]`;
the audit, root, and theorem remain incomplete.

The frozen immediate root cut set remains:

- `M0580-N-SMOOTH`, the proposed topological smoothing package;
- `M0580-T-SMOOTH-POINCARE`, the proposed smooth three-dimensional Poincare package.

The checked theorem `root_of_smoothing_and_smooth_poincare` assumes both packages and only composes
them into the exact root. It constructs neither package. The new trust-zero checked diagnostic
`smoothThreeDimensionalPoincare_of_perelmanPoincareTarget` proves the converse direction from the
exact root to the frozen smooth package. Consequently that package is not an independent smooth
result in its current homeomorphism-valued form; using the root to inhabit it would be circular.

Pinned mathlib contains the generalized, topological, and smooth Poincare signatures only as
`proof_wanted` source markers. Batteries elaborates those markers under `withoutModifyingEnv`, and
the probe confirms that importing the module leaves all three names absent. Repository and pinned
dependency searches found no alternate exact root or cut-set body. The immutable external candidate
from the prerequisite audit has a dimension-three statement and a dimension-zero proof, not a
dimension-three terminal proof.

There is also an earlier fail-closed defect in `M0580-N-SMOOTH`. Its contract receives an already
selected arbitrary `ChartedSpace Euclidean3 M` and asks for `Nonempty (IsManifold ... infinity M)`.
`IsManifold` applies to that selected atlas; `Nonempty` around the proposition does not select a
replacement atlas. This is stronger than a Moise-style smoothability result. The prerequisite
obligation-tree authority must replace it append-only with a contract carrying a smooth atlas,
smoothness proof, and compatibility bridge. This proof worker did not alter the frozen registry.

## Validation

All commands ran in this worker clone. Lean outputs were confined to disposable `/tmp` directories
and removed. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was run.
The automation-provided untracked `.lake` symlink was reused read-only, so this is nonrelease
evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; planned; L0/rework-required; theorem incomplete |
| isolated trust-zero `lake env lean` chain below | 0 | exact statement, conditional composition, and blocker probe elaborated; each axiom report was `[propext, Classical.choice, Quot.sound]`; all three `proof_wanted` names were absent |
| isolated direct trust-zero statement-expression checks | 0 | reproduced canonical expression SHA-256 `938ef54298273a011a66395812b53e6bf8071b0925b84cd94ae5fb4f9a6eb664`; all four declared mutations had distinct expression hashes |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root remains open at M4 |
| forbidden-construct `rg` scan of the four Lean modules | 1 | expected no-match status; no prohibited proof construct was found |
| `git diff --check -- Stage1_Instances/THM-M-0580` | 0 | no whitespace error |
| `python3 Stage1_Instances/THM-M-0580/check_statement.py` | interrupted | an initial helper run stalled under shared-host saturation; equivalent isolated direct elaborations subsequently passed for the canonical statement and all four mutations |
| `python3 Stage1_Instances/THM-M-0580/check_anchor_audit.py` | 1 | `HTTP Error 403: rate limit exceeded`; no moving network result is used for this blocker conclusion |

The successful narrow Lean check used the pinned executable and a manually assembled read-only
`LEAN_PATH`:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0580
tmp=$(mktemp -d /tmp/thm-m-0580-slot21-heade27b85e1.XXXXXX)
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
```

The new probe's SHA-256 is
`5824782a90bcade9b6ba41b24ba3cc07d0d858cfff7e767930f5dfe4fce3d333`.
All pre-existing proof-relevant source, registry, graph, anchor, validation-specification, and Lake
manifest hashes match the preceding current-target receipt.

## Retry Condition

First return `M0580-N-SMOOTH` to the obligation-tree authority for an append-only correction that
carries a replacement smooth atlas and checked compatibility/assembly bridge. Then implement the
corrected smoothing package and the complete smooth-Poincare package without placeholders.
Alternatively, integrate an immutable compatible Lean 4 proof of the exact root with a complete
dependency lock and license after a new graph revision is accepted.

Assuming either package, treating `proof_wanted` as an axiom, or presenting the conditional
composition as root closure would violate the exact-target and proof-body gates. This is an owned
blocker artifact, not a proof receipt. It does not satisfy `S56-M-0580-PROOF`, propose state
promotion, or support theorem completion. Because the assigned proof phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` remains absent.
