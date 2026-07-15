# THM-M-0580 proof-phase recheck at base d5ab961c (slot 24)

Item: `S56-M-0580-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `d5ab961cb3cd92c7febcf21fb9ab746fde231c24`

Base tree: `5f3d5abbfee8a0f11198a295ecf024aca301867f`

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
`proof_wanted`. The pinned Batteries implementation elaborates those signatures inside
`withoutModifyingEnv` and discards them. The trust-zero probe after import confirms all three names
are unknown. Scoped retained-declaration searches found no alternate root or cut-set proof body. The
immutable prerequisite audit contains only statement-level or support-only external candidates.

## First Failed Gate

The prerequisite obligation-tree contract is not master-accepted or executable as a faithful proof
architecture. `task-dag.json` has `accepted_states: []` and records every prerequisite task as open;
the generated `[_]` markers are provisional, not master acceptance.

The frozen contracts also require an append-only prerequisite correction:

- `TopologicalThreeManifoldSmoothable` receives an already selected `ChartedSpace` and requires
  `Nonempty (IsManifold ... M)` for that atlas. It does not construct a compatible replacement
  smooth atlas; wrapping the proposition in `Nonempty` chooses no atlas.
- `SmoothThreeDimensionalPoincare` concludes the same homeomorphism as the root under an extra
  `IsManifold` instance. The root implies this package directly, so it is not a distinct smooth
  theorem.
- The metric, Ricci-flow, surgery, extinction, decomposition, and topology children have planned
  fingerprints rather than exact Lean propositions and own no proof bodies.

Changing these prerequisite contracts in the proof phase would violate the frozen registry and this
worker's ownership boundary. Even after a corrected tree is accepted, the Ricci-flow, surgery,
finite-extinction, decomposition, and fundamental-group packages remain unformalized in the pinned
closure.

## Validation

All commands ran in this worker clone. The automation-provided canonical `.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, or dependency mutation was run.
Lean outputs were confined to a disposable `/tmp` directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; planned; L0/rework-required; theorem incomplete |
| `git rev-parse HEAD HEAD^{tree} && git status --short` | 0 | base `d5ab961cb3cd92c7febcf21fb9ab746fde231c24`; tree `5f3d5abbfee8a0f11198a295ecf024aca301867f`; only the automation-provided `.lake` symlink was initially untracked |
| isolated trust-zero `lake env lean` chain below | 0 | exact statement, conditional composition, and blocker probe elaborated; local theorem axiom reports were `[propext, Classical.choice, Quot.sound]`; all three `proof_wanted` names were absent |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root open at M4 |
| `timeout 180 python3 Stage1_Instances/THM-M-0580/check_statement.py` | 1 | Lake stopped before elaboration because the preexisting pinned `flt-regular` package checkout has an invalid HEAD; the direct isolated statement elaboration passed |
| `timeout 120 python3 Stage1_Instances/THM-M-0580/check_anchor_audit.py` | 1 | immutable local assertions ran first, then GitHub returned HTTP 403 rate limit exceeded; no external result was accepted or changed |
| scoped retained-declaration search | 0 | no alternate exact-root or cut-set body; no retained theorem, lemma, or axiom for the three `proof_wanted` names |
| inverted prohibited-construct scan | 0 | no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `external` token in the four owned Lean modules |
| `ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| pinned mathlib and Batteries revision/tree/status probes | 0 | mathlib `8a178386...` / tree `bdc39a31...`; Batteries `756e3321...` / tree `02666252...`; both clean |

The narrow Lean check was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0580
tmp=$(mktemp -d /tmp/thm-m-0580-slot24-headd5ab961c.XXXXXX)
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

The statement helper's failure is a separate pinned-environment blocker: the preexisting
`Formalizations/Lean/.lake/packages/flt-regular` directory contains only an incomplete Git checkout
whose HEAD is `refs/heads/.invalid`. The worker left this shared dependency untouched. The direct
isolated check does not require Lake to resolve that unused package and verifies the target modules
against the existing pinned oleans.

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
