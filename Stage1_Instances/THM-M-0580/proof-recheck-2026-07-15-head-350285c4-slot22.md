# THM-M-0580 proof-phase recheck at base 350285c4 (slot 22)

Item: `S56-M-0580-PROOF`

Recorded: `2026-07-15T15:20:05+08:00`

Base revision: `350285c48208616b6e3ad74154d9183d16523cfa`

Base tree: `c4edebc115ec954e4940ed5faaa3ffacd4e56091`

## Verdict

`blocked`. The proof node is not dependency-legal: its prerequisite
`S56-M-0580-OBLIGATION_TREE` is only worker-self-tested `[_]`, not master-accepted `[x]`.
The target `task-dag.json` also has `accepted_states: []` and records that prerequisite as open.

Independently, no eligible terminal Lean 4 body was found for the exact declaration
`Stage1Instances.THM_M_0580.PerelmanPoincareTarget`. The frozen immediate root cut set remains:

- `M0580-N-SMOOTH`, compatible smoothing of the fixed topological manifold;
- `M0580-T-SMOOTH-POINCARE`, the full smooth three-dimensional Poincare package.

`root_of_smoothing_and_smooth_poincare` assumes both packages and only composes them. The diagnostic
`smoothThreeDimensionalPoincare_of_perelmanPoincareTarget` derives the second package from the root,
so using it to construct a root premise would be circular. Moreover, the current smoothing
proposition checks `IsManifold` for the already-selected atlas; `Nonempty` around that proposition
does not construct a replacement atlas or a compatibility bridge. Correcting this requires an
append-only prerequisite registry revision, not a silent proof-phase substitution. The Ricci-flow,
surgery, extinction, decomposition, and fundamental-group children remain planned signatures
without exact terminal proof bodies.

Pinned mathlib has only discarded `proof_wanted` entries for the matching topological and smooth
statements. The Batteries implementation uses `withoutModifyingEnv`; trust-zero elaboration confirms
that all three relevant names are unknown after import. Repo-local searches found no alternative
exact-root or cut-set theorem.

A fresh external search found `frenzymath/Poincare-Conjecture` at immutable commit
`2d6abb09774efc7c1a5059f7e78b8679db3be6d2`. Its README explicitly calls the project active,
incomplete, preliminary, and non-release. Its Morgan-Tian source currently contains 139 Lean files
only under `Ch01` and `Ch02`, and a source scan found no `Perelman`, `SimplyConnectedSpace`,
`nonempty_homeomorph_sphere_three`, or canonical homeomorphism target. Other project areas contain
documented `sorry` bodies. This is a relevant ongoing formalization, not a proof source to pin.
Fresh public-code searches likewise found only mathlib's `proof_wanted`, statement collections, and
comments, not a terminal declaration.

No proof body or completion receipt was added. The item stays `[ ]`; the root stays
`[H2, M4, R4]`; `audit_complete`, root closure, and theorem completion remain false.

## Validation

All commands ran in this worker clone. The automation-provided canonical `.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, or dependency mutation was run.
Lean outputs and the external snapshot were confined to disposable `/tmp` directories; no external
source was copied into the workspace.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; planned; L0/rework-required; theorem incomplete |
| isolated trust-zero `lake env lean` chain below | 0 | statement, conditional composition, and blocker probe elaborated; local theorem axiom reports were `[propext, Classical.choice, Quot.sound]`; all three `proof_wanted` names were absent |
| `python3 Stage1_Instances/THM-M-0580/check_statement.py` | 0 | expression SHA-256 `938ef54298273a011a66395812b53e6bf8071b0925b84cd94ae5fb4f9a6eb664`; all four mutations killed; pinned toolchain and mathlib revision matched |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations, 42 typed edges, denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root open at M4 |
| `python3 Stage1_Instances/THM-M-0580/check_anchor_audit.py` | 1 | local/pinned checks passed before its only remote replay failed with GitHub API HTTP 403 rate-limit; no anchor conclusion was inferred from this failed replay |
| raw immutable replay of audited candidate C04 | 0 | source SHA-256 `045a97bb2dea46544ca57da7e9e5669c6b160721b1882bc53a8426369352deba`; dimension-three target remains a `def`; only the dimension-zero generalization has a theorem body |
| scoped retained-declaration search | 0 | only the two pinned `proof_wanted` markers and non-proof metadata references matched; no exact-root or cut-set body |
| inverted forbidden-construct scan | 0 | no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `external` token in the four owned Lean modules |
| `cd Formalizations/Lean && timeout 60 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| dependency pin and cleanliness probes | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` / tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; Batteries `756e3321fd3b02a85ffda19fef789916223e578c` / tree `02666252fd943c970ee0b7a66ec65a2e5efe7230`; both clean |
| `git ls-remote https://github.com/frenzymath/Poincare-Conjecture.git HEAD` | 0 | immutable head `2d6abb09774efc7c1a5059f7e78b8679db3be6d2` |
| commit-addressed tarball audit of `frenzymath/Poincare-Conjecture` | 0 | tar SHA-256 `4497ee6853bf55fa6729c5773ab9431828221ec7873f6837cc72dbf889915de1`; reconstructed tracked tree `37a4947961578be969e18b148824bcdcd3beb974`; README SHA-256 `33e4cf91a70801f31aaff13d16b0783c40e667a252b2c68cc8e57d5e2371932c`; 139 Morgan-Tian Lean files under only `Ch01,Ch02`; zero target-like hits; explicit incomplete/beta warning and unrelated placeholder bodies |

The narrow Lean validation command was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0580
tmp=$(mktemp -d /tmp/thm-m-0580-slot22-head350285c4.XXXXXX)
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
`8c69718898cfefd3f33ccce0ac95ca8f4e9a82bc28fda79b6b91ae01b7cffba6` and
`6f2ad414a2fe0d0dd9544cc489751163408ac7b85a9823e3935ff1663af7dcb8`.

## Retry Condition

First publish and master-accept an append-only obligation-tree revision with a compatible
replacement-atlas smoothing contract, exact Lean targets for every proof child, checked
composition, and declaration-covering recipes. Then implement the corrected smoothing package and
the complete smooth-Poincare package without placeholders. Alternatively, integrate an immutable,
licensed, compatible exact-root Lean 4 proof with a complete dependency lock and exact-type,
provenance, and trust checks. The new external project may be re-audited only after it publishes a
terminal declaration covering this exact target and removes all root-critical placeholders.

This dossier contained 34 earlier structured blocker rechecks for this proof item before this
attempt. Under the rev-5.6 five-tick rule, the master must split this oversized item into
dependency-legal child tasks instead of rescheduling the unchanged root. This proof worker has no
authority to edit the execution DAG.

Assuming either missing package, treating `proof_wanted` as an axiom, or presenting conditional
composition as root closure would violate the exact-target and proof-body gates. This is an owned
blocker artifact, not a proof receipt. It does not satisfy `S56-M-0580-PROOF`, propose state
promotion, or support theorem completion. Because the assigned phase is not genuinely complete,
`.stage1-worker-selftest.json` remains absent.
