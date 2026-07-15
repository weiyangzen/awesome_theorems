# THM-M-0580 proof-phase recheck at base 443b8bbc (slot 26)

Item: `S56-M-0580-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

## Verdict

`blocked`. No eligible terminal Lean 4 proof body exists in the repository or pinned dependency
closure for the exact proposition `Stage1Instances.THM_M_0580.PerelmanPoincareTarget`. No proof body
or proof receipt was added. The proof item remains `[ ]`, the root vector remains `[H2, M4, R4]`,
and the audit, exact root, and theorem remain incomplete.

The immediate frozen root cut set remains:

- `M0580-N-SMOOTH`, the proposed topological smoothing package;
- `M0580-T-SMOOTH-POINCARE`, the proposed smooth three-dimensional Poincare package.

`root_of_smoothing_and_smooth_poincare` assumes both packages and only composes them. The diagnostic
`smoothThreeDimensionalPoincare_of_perelmanPoincareTarget` goes from the root back to the second
package, so using it to construct a root premise would be circular.

Pinned mathlib supplies the matching generalized, topological, and smooth signatures only through
`proof_wanted`. The pinned Batteries implementation elaborates these signatures inside
`withoutModifyingEnv`; it deliberately discards them, and they cannot be used as axioms. The
trust-zero check after import confirms that all three names are unknown. Current scoped searches
found no alternate retained body. The immutable external audit contains only a dimension-three
statement and an unrelated dimension-zero proof.

## First Failed Gate

The structured prerequisite is not accepted. `task-dag.json` has `accepted_states: []` and records
`S56-M-0580-OBLIGATION_TREE` as `open`; the generated checklist's `[_]` marker is provisional rather
than master acceptance. Proof execution is therefore not dependency-legal.

The frozen proof architecture also requires an append-only prerequisite revision before node-level
implementation:

- `TopologicalThreeManifoldSmoothable` receives an already selected `ChartedSpace` and requires
  `Nonempty (IsManifold ... M)` for that atlas. This does not express existence of a replacement
  compatible smooth atlas; wrapping a proposition in `Nonempty` chooses no atlas.
- `SmoothThreeDimensionalPoincare` concludes the same homeomorphism as the root under one extra
  `IsManifold` instance. The root therefore implies this package directly. It does not encode a
  distinct diffeomorphism-valued smooth theorem.
- `C-METRIC` through `L-PI1-ELIMINATION` have planned fingerprints rather than exact Lean targets,
  no owned proof sources, and structural recipes covering no Lean declarations.

Silently replacing those frozen contracts would violate the registry rule and this worker's proof
phase authority. Even after correction, Ricci flow, surgery, extinction, decomposition, and
fundamental-group packages remain unformalized in the pinned closure.

## Validation

All commands ran in this worker clone. Lean outputs were confined to a disposable `/tmp` directory
and removed. The automation-provided untracked `.lake` symlink was reused read-only. No `lake
update`, `lake build`, dependency clone/fetch, or dependency mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; planned; L0/rework-required; theorem incomplete |
| isolated trust-zero `lake env lean` chain below | 0 | exact statement, conditional composition, and blocker probe elaborated; both local theorem axiom reports were `[propext, Classical.choice, Quot.sound]`; all three `proof_wanted` names were absent |
| `timeout 300 python3 Stage1_Instances/THM-M-0580/check_statement.py` | 1 | pinned dependency infrastructure failure: Lake could not resolve `HEAD` for the shared `flt-regular` package; the direct isolated statement elaboration above passed and no dependency was mutated |
| `python3 Stage1_Instances/THM-M-0580/check_anchor_audit.py` | 0 | exact statement anchors bodyless; external root statement-only; root M4 |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root remains open at M4 |
| scoped retained-declaration searches | 0 | no alternate exact-root or cut-set body; no retained theorem, lemma, or axiom for the three `proof_wanted` names |
| inverted prohibited-construct scan | 0 | no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `external` token in the four owned Lean modules |
| pinned marker and Batteries implementation searches | 0 | exactly three relevant `proof_wanted` entries; Batteries states that they are discarded and cannot be used as axioms |
| `cd Formalizations/Lean && timeout 60 lake env lean --version` | 1 | shared dependency preflight failed before Lean launch because canonical `flt-regular` could not resolve `HEAD` |
| `ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 timeout 60 lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release; the isolated checks used this pinned toolchain |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `python3 -m json.tool Stage1_Instances/THM-M-0580/proof-recheck-2026-07-15-head-443b8bbc-slot26.json` | 0 | companion blocker ledger parsed successfully |
| trailing-whitespace scan of the two current-base artifacts | 0 | no trailing whitespace was found |
| `git diff --check -- Stage1_Instances/THM-M-0580` | 0 | no tracked-diff whitespace errors; new untracked artifacts were checked separately |
| `test ! -e .stage1-worker-selftest.json` | 0 | required self-test manifest is absent because proof completion failed |

The narrow Lean check was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0580
tmp=$(mktemp -d /tmp/thm-m-0580-slot26-head443b8bbc.XXXXXX)
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

First reconcile and master-accept the prerequisite task state. Then publish an append-only
obligation-tree revision with a replacement-atlas smoothing contract, faithful smooth-package
semantics, exact Lean targets for every child, checked composition, and declaration-covering
recipes. Implement those corrected packages without placeholders. Alternatively, integrate an
immutable, licensed, compatible exact-root Lean 4 proof with a complete dependency lock and
exact-type/provenance checks.

Assuming either missing package, treating `proof_wanted` as an axiom, or presenting conditional
composition as root closure would violate the exact-target and proof-body gates. This is an owned
blocker artifact, not a proof receipt; it does not satisfy `S56-M-0580-PROOF`, propose state
promotion, or support theorem completion. Because the phase is not genuinely complete,
`.stage1-worker-selftest.json` remains absent.
