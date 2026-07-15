# THM-M-0580 proof-phase recheck at base 714fb3bb (slot 24)

Item: `S56-M-0580-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `714fb3bb6a070c2f659ece069f1a7219f9c045a0`

Base tree: `2c99a78c5fa247aebc885f31e6818fc029f17a60`

## Verdict

`blocked`. No eligible terminal Lean 4 proof body exists in the repository or pinned dependency
closure for `Stage1Instances.THM_M_0580.PerelmanPoincareTarget`. No proof body or receipt was added.
The proof item remains `[ ]`, the root vector remains `[H2, M4, R4]`, and the audit, exact root, and
theorem remain incomplete.

The immediate frozen root cut set remains:

- `M0580-N-SMOOTH`, the proposed topological smoothing package;
- `M0580-T-SMOOTH-POINCARE`, the proposed smooth three-dimensional Poincare package.

`root_of_smoothing_and_smooth_poincare` assumes both packages and only composes them. The diagnostic
`smoothThreeDimensionalPoincare_of_perelmanPoincareTarget` runs from the root back to the second
package, so using it to construct a root premise would be circular.

Pinned mathlib supplies the matching generalized, topological, and smooth signatures only through
`proof_wanted`. Batteries elaborates those signatures inside `withoutModifyingEnv`, deliberately
discarding them. The trust-zero check after import confirms all three names are unknown. Scoped
repo and pinned-package searches found no alternate retained root or cut-set body. The immutable
external audit contains only a dimension-three statement and an unrelated dimension-zero proof.

## First Failed Gate

The prerequisite obligation-tree contract is neither master-accepted nor executable as a faithful
proof architecture. `task-dag.json` has `accepted_states: []` and records
`S56-M-0580-OBLIGATION_TREE` as open; the generated checklist's `[_]` marker is provisional.

The frozen contracts also require an append-only prerequisite correction:

- `TopologicalThreeManifoldSmoothable` receives an already selected `ChartedSpace` and requires
  `Nonempty (IsManifold ... M)` for that atlas. It does not construct a compatible replacement
  smooth atlas; wrapping the proposition in `Nonempty` chooses no atlas.
- `SmoothThreeDimensionalPoincare` concludes the same homeomorphism as the root under one extra
  `IsManifold` instance. The root implies this package directly, so it is not a distinct smooth
  theorem.
- The metric, Ricci-flow, surgery, extinction, decomposition, and topology children have planned
  fingerprints rather than exact Lean propositions and own no proof bodies.

Silently replacing those contracts is outside this proof worker's authority. Even after correction,
the Ricci-flow, surgery, extinction, decomposition, and fundamental-group packages remain major
unformalized work in the pinned closure.

## Validation

All commands ran in this worker clone. The automation-provided canonical `.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, or dependency mutation was run.
Lean outputs were confined to a disposable `/tmp` directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; planned; L0/rework-required; theorem incomplete |
| `git status --short && git rev-parse HEAD HEAD^{tree}` | 0 | base `714fb3bb6a070c2f659ece069f1a7219f9c045a0`; tree `2c99a78c5fa247aebc885f31e6818fc029f17a60`; only the automation-provided `.lake` symlink was initially untracked |
| isolated trust-zero `lake env lean` chain below | 0 | exact statement, conditional composition, and blocker probe elaborated; local theorem axiom reports were `[propext, Classical.choice, Quot.sound]`; all three `proof_wanted` names were absent |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root open at M4 |
| `timeout 90 python3 Stage1_Instances/THM-M-0580/check_anchor_audit.py` | 0, then 1 | initial run confirmed exact pinned statement anchors bodyless, immutable external root statement-only, and root M4; final repeat passed the immutable local checks but GitHub returned HTTP 403 rate limit exceeded, so no external data was accepted or changed |
| `timeout 120 python3 Stage1_Instances/THM-M-0580/check_statement.py` | 124 | timed out under shared-runner Lake contention before producing a validator result; the owned temporary source was removed; this non-result supplies no proof credit |
| scoped retained-declaration search | 0 | no alternate exact-root or cut-set body and no retained declaration for the three `proof_wanted` names |
| `ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| pinned mathlib and Batteries revision/tree/status probes | 0 | mathlib `8a178386...` / tree `bdc39a31...`; Batteries `756e3321...` / tree `02666252...`; both clean |
| `python3 -m json.tool Stage1_Instances/THM-M-0580/proof-recheck-2026-07-15-head-714fb3bb-slot24.json` | 0 | owned blocker ledger parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-0580` | 0 | no whitespace errors in the owned artifacts |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest is absent because the proof phase is blocked |

The narrow Lean check was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0580
tmp=$(mktemp -d /tmp/thm-m-0580-slot24-head714fb3bb.XXXXXX)
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

First publish and master-accept an append-only obligation-tree revision with a replacement-atlas
smoothing contract, faithful smooth-theorem semantics, exact Lean targets for every child, checked
composition, and declaration-covering recipes. Then implement those packages without placeholders.
Alternatively, integrate an immutable, licensed, compatible exact-root Lean 4 proof with a complete
dependency lock and exact-type, provenance, and trust checks.

Assuming either missing package, treating `proof_wanted` as an axiom, or presenting conditional
composition as root closure would violate the exact-target and proof-body gates. This is an owned
blocker artifact, not a proof receipt; it does not satisfy `S56-M-0580-PROOF`, propose state
promotion, or support theorem completion. Because the phase is not genuinely complete,
`.stage1-worker-selftest.json` remains absent.
