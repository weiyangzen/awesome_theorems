# THM-M-0580 proof-phase recheck at base dafb8b51 (slot 27)

Item: `S56-M-0580-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `dafb8b51c4561eee5fcf162a8d5ee49555584bdb`

Base tree: `cca569d6bbc491441652aae678232353fb385a74`

## Verdict

`blocked`. No eligible terminal Lean 4 proof body exists in this checkout or its pinned
dependency closure for the exact proposition
`Stage1Instances.THM_M_0580.PerelmanPoincareTarget`. No proof body or proof receipt was added. The
proof item remains `[ ]`, the root vector remains `[H2, M4, R4]`, and the audit, exact root, and
theorem remain incomplete.

Proof execution is not dependency-legal. The structured target authority, `task-dag.json`, has
`accepted_states: []` and records `S56-M-0580-OBLIGATION_TREE` as open. The generated blueprint's
`[_]` entry is provisional worker output, not master acceptance.

Independently, the frozen immediate cut set is still open:

- `M0580-N-SMOOTH`, the proposed topological smoothing package;
- `M0580-T-SMOOTH-POINCARE`, the proposed smooth three-dimensional Poincare package.

`root_of_smoothing_and_smooth_poincare` assumes both packages and only checks their conditional
composition. `smoothThreeDimensionalPoincare_of_perelmanPoincareTarget` proves the second package
from the exact root; using that converse to construct a root premise would be circular.

The prerequisite proof architecture also needs append-only correction before node-level proof
work can be credited:

- `TopologicalThreeManifoldSmoothable` quantifies over an already selected `ChartedSpace` instance
  and asks whether that atlas is smooth. `Nonempty` around the proposition `IsManifold` neither
  selects a replacement atlas nor records compatibility with the original topological atlas.
- `SmoothThreeDimensionalPoincare` concludes the same homeomorphism as the root under one extra
  `IsManifold` instance. It is not a distinct diffeomorphism-valued smooth theorem.
- `M0580-C-METRIC` through `M0580-L-PI1-ELIMINATION` have planned fingerprints rather than exact Lean
  propositions, no owned terminal proof bodies, and recipes that cover no Lean declarations.

Pinned mathlib contains the generalized, topological, and smooth signatures only as
`proof_wanted`. Batteries elaborates those statements inside `withoutModifyingEnv` and explicitly
discards them, so they are not declarations or axioms. The trust-zero probe below confirms that all
three matching names are unknown. Scoped repository and pinned-package searches found no alternate
terminal body.

An independent bounded discovery recheck observed the active external repository
`frenzymeath/Poincare-Conjecture` at commit
`d39331c2e614bd4828213b6fa15f894ff6c03633` on 2026-07-15. Its immutable tree contains foundation
work and Morgan-Tian Chapters 1-2, while the project describes itself as incomplete and contains no
Poincare, surgery, extinction, or exact-root terminal declaration. It therefore supplies no proof
body and is not an integration candidate. No dependency was fetched or added to this clone.

## Validation

All commands ran in this worker clone. The automation-provided untracked `.lake` symlink was reused
read-only. The normal `lake env lean` preflight is currently blocked because the shared pinned
`.lake/packages/flt-regular` directory is an incomplete Git repository whose `HEAD` points to
`refs/heads/.invalid`. The worker did not repair, fetch, build, or otherwise mutate `.lake`.

The smallest real elaboration check therefore invoked the exact pinned Lean executable directly
while using only the existing compiled library paths. Its outputs were confined to and removed with
a disposable `/tmp` directory. This is a successful kernel elaboration check, but it is not proof
closure and does not cure the missing shared artifact.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; lifecycle `planned`; baseline L0/rework-required; theorem incomplete |
| `timeout 600 python3 Stage1_Instances/THM-M-0580/check_statement.py` | 1 | shared `.lake/packages/flt-regular` could not resolve `HEAD`; environmental artifact blocker, not a statement mismatch |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root open at M4 |
| direct pinned Lean 4.29.0 `--trust=0` chain below | 0 | statement, conditional composition, and blocker probe elaborated; both local theorem axiom reports were `[propext, Classical.choice, Quot.sound]`; all three `proof_wanted` names were unknown |
| inverted prohibited-construct scan over the four owned Lean modules | 0 | no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `external` token matched |
| pinned Poincare-module and Batteries implementation searches | 0 | exactly three relevant `proof_wanted` entries; Batteries says they are discarded and cannot be used as axioms |
| `~/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |

The narrow Lean check was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0580
tmp=$(mktemp -d /tmp/thm-m-0580-slot27-headdafb8b51.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
paths=("$lean_root/.lake/build/lib/lean")
for p in "$lean_root"/.lake/packages/*/.lake/build/lib/lean; do paths+=("$p"); done
lean_path=$(IFS=:; printf '%s' "${paths[*]}")
lean_bin=$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
cd "$target"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout 300 "$lean_bin" --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout 300 "$lean_bin" --trust=0 -t0 -o "$tmp/ObligationTree.olean" ObligationTree.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout 300 "$lean_bin" --trust=0 -t0 ProofBlockerProbe.lean
sha256sum "$tmp/Statement.olean" "$tmp/ObligationTree.olean"
```

The temporary olean SHA-256 values were
`8c69718898cfefd3f33ccce0ac95ca8f4e9a82bc28fda79b6b91ae01b7cffba6` for
`Statement.olean` and
`6f2ad414a2fe0d0dd9544cc489751163408ac7b85a9823e3935ff1663af7dcb8` for
`ObligationTree.olean`.

## Retry Condition

First reconcile and master-accept the prerequisite state. Then publish an append-only
obligation-tree revision with replacement-atlas smoothing data and compatibility, faithful
diffeomorphism-valued smooth-package semantics, exact Lean targets for every child, checked
composition, and declaration-covering recipes. Implement those corrected packages without
placeholders. Alternatively, integrate an immutable, licensed, compatible exact-root Lean 4 proof
with a complete dependency lock and exact-type/provenance checks. The shared pinned
`flt-regular` artifact must also be restored by the automation owner before normal `lake env lean`
validation can replay.

Assuming either missing package, treating `proof_wanted` as an axiom, or presenting conditional
composition as root closure would violate the exact-target and proof-body gates. This is an owned
blocker artifact, not a proof receipt; it does not satisfy `S56-M-0580-PROOF`, propose state
promotion, or support theorem completion. Because the phase is not genuinely self-tested,
`.stage1-worker-selftest.json` remains absent.
