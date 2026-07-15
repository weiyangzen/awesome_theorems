# THM-M-0580 proof-phase recheck at base dc0f0264 (slot 14)

Item: `S56-M-0580-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `dc0f0264c1db312ac95025747d3212b689facb5e`

Base tree: `633bea3a2e72674768ee426a035a1850b9940ae7`

## Verdict

`blocked`. No eligible terminal Lean 4 proof body exists in the repository or pinned dependency
closure for the exact proposition
`Stage1Instances.THM_M_0580.PerelmanPoincareTarget`. No proof body or proof receipt was added. The
proof item remains `[ ]`, the root vector remains `[H2, M4, R4]`, and the audit, exact root, and
theorem remain incomplete.

Proof acceptance is not dependency-legal under the structured authority. `task-dag.json` has
`accepted_states: []` and records `S56-M-0580-OBLIGATION_TREE` as `open`; the generated checklist's
`[_]` marker is provisional rather than master acceptance.

Independently, the frozen immediate root cut set remains:

- `M0580-N-SMOOTH`, the proposed topological smoothing package;
- `M0580-T-SMOOTH-POINCARE`, the proposed smooth three-dimensional Poincare package.

`root_of_smoothing_and_smooth_poincare` assumes both packages and only composes them. It constructs
neither. The diagnostic `smoothThreeDimensionalPoincare_of_perelmanPoincareTarget` proves the second
package from the root, so using it to obtain a root premise would be circular.

The prerequisite architecture also requires an append-only correction before implementation.
`TopologicalThreeManifoldSmoothable` receives an already selected `ChartedSpace` and asks for
`Nonempty (IsManifold ... M)` for that atlas. It does not select a replacement smooth atlas or
provide a compatibility bridge. `SmoothThreeDimensionalPoincare` concludes the same homeomorphism
as the root under one extra `IsManifold` instance, rather than encoding a distinct smooth theorem.
The Ricci-flow and surgery descendants still have planned fingerprints instead of exact executable
Lean targets. This proof worker did not alter the frozen prerequisite registry.

Pinned mathlib exposes the generalized, topological-three, and smooth-three signatures only as
`proof_wanted` markers. Batteries elaborates such markers under `withoutModifyingEnv`, discards
them, and explicitly says that they cannot be used as axioms. The trust-zero probe confirms all
three names are unknown. Scoped repository and pinned-dependency searches found no alternate
retained exact-root or cut-set body.

## Validation

All commands ran in this worker clone. Lean outputs were confined to a disposable `/tmp` directory
and removed. The automation-provided untracked `.lake` symlink was reused read-only. No `lake
update`, `lake build`, dependency clone/fetch, or dependency mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; lifecycle planned; L0/rework-required; theorem incomplete |
| isolated pinned Lean 4.29.0 trust-zero chain below | 0 | `Statement.lean`, `ObligationTree.lean`, and `ProofBlockerProbe.lean` elaborated; local theorem axiom reports were `[propext, Classical.choice, Quot.sound]`; all three `proof_wanted` names were unknown |
| `timeout 180 python3 Stage1_Instances/THM-M-0580/check_statement.py` | 1 | shared pinned `flt-regular` checkout cannot resolve `HEAD`; this is a missing-artifact blocker in Lake preflight, not a statement mismatch |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root remains open at M4 |
| inverted prohibited-construct scan over the four owned Lean modules | 0 | no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, or `external` token |
| retained-declaration search and pinned source inspection | 0 | no matching theorem, lemma, opaque declaration, or axiom body; exactly three relevant `proof_wanted` markers, whose implementation discards them |
| `cd Formalizations/Lean && timeout 60 lake env lean --version` | 1 | shared pinned `flt-regular` checkout cannot resolve `HEAD`; no fetch or repair was attempted |
| `~/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |

The narrow elaboration used `lake env lean` with the exact pinned toolchain and only existing
compiled artifacts. Supplying the explicit `LEAN_PATH` avoids Lake's unrelated project dependency
preflight while preserving the requested narrow invocation:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0580
tmp=$(mktemp -d /tmp/thm-m-0580-slot14-headdc0f0264.XXXXXX)
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

The master must first accept or repair the prerequisite task. The obligation-tree authority must
publish an append-only revision with replacement-atlas smoothing data and compatibility, a
faithful smooth theorem, exact Lean targets for every required child, checked composition, and
declaration-covering recipes. Then the corrected smoothing and full smooth-Poincare packages must
be implemented without placeholders. Alternatively, integrate an immutable, licensed, compatible
Lean 4 terminal proof of the exact root with a complete dependency lock and provenance/trust checks.

The owned dossier now contains 30 earlier structured blocker attempts for this same proof item, so
the master should split the oversized proof item into dependency-legal child tasks rather than
rescheduling the unchanged root. This worker has no authority to edit the DAG.

Assuming a missing package, treating `proof_wanted` as an axiom, or presenting conditional
composition as root closure would violate the exact-target and proof-body gates. This is an owned
blocker artifact, not a proof receipt; it does not satisfy `S56-M-0580-PROOF` or support theorem
completion. Because the assigned phase is not genuinely complete,
`.stage1-worker-selftest.json` remains absent.
