# THM-M-0580 proof-phase recheck at base bbe7a5bd

Item: `S56-M-0580-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `bbe7a5bd1c72a12f3f43b79b6a4cac3f62d2085a`

Base tree: `aa558ed6f23779c7d2d9a8427775f709d8b7e31b`

## Verdict

`blocked`. No eligible terminal Lean 4 proof body exists in the repository or pinned dependency
closure for the exact proposition
`Stage1Instances.THM_M_0580.PerelmanPoincareTarget`. No proof body or receipt was added. The proof
item remains `[ ]`, the root vector remains `[H2, M4, R4]`, and the audit, root, and theorem remain
incomplete.

The frozen immediate root cut set remains:

- `M0580-N-SMOOTH`, the proposed topological smoothing package;
- `M0580-T-SMOOTH-POINCARE`, the full smooth three-dimensional Poincare package.

The checked theorem `root_of_smoothing_and_smooth_poincare` assumes both packages and only composes
them into the exact root. It constructs neither. The diagnostic
`smoothThreeDimensionalPoincare_of_perelmanPoincareTarget` goes in the converse direction, from the
root to the frozen smooth package, so using it to manufacture a root premise would be circular.

Pinned mathlib contains the matching generalized, topological, and smooth Poincare signatures only
as `proof_wanted` markers. Importing the module retains none of those declarations, as the
trust-zero probe confirms. A current repo-local scoped search found no alternate terminal body, and
the pinned source search returned only the same three markers. The immutable anchor audit's external
candidate defines the dimension-three target but proves only a dimension-zero generalized special
case, so it supplies no proof body to import.

There is also an earlier fail-closed defect in `M0580-N-SMOOTH`. Its Lean contract receives an
already selected `ChartedSpace Euclidean3 M` and requires `Nonempty (IsManifold ... infinity M)`
for that same atlas. Wrapping the proposition in `Nonempty` does not choose a replacement compatible
smooth atlas. Correcting this belongs to the prerequisite obligation-tree authority and requires an
append-only graph revision carrying a replacement atlas, a smoothness proof, and a checked
compatibility bridge. This proof worker did not alter the frozen registry.

The exact proof inputs and pins are unchanged since the immediately preceding integrated recheck at
base `ed919316`: the only target-path delta through this base is that recheck's own JSON/Markdown
evidence pair.

## Validation

All commands ran in this worker clone. Lean outputs were confined to a disposable `/tmp` directory
and removed. The automation-provided untracked `.lake` symlink was reused read-only. No `lake
update`, `lake build`, dependency clone/fetch, or dependency mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; planned; L0/rework-required; theorem incomplete |
| isolated trust-zero `lake env lean` chain below | 0 | exact statement, conditional composition, and blocker probe elaborated; both local theorem axiom reports were `[propext, Classical.choice, Quot.sound]`; all three `#check_failure` probes passed, confirming that the `proof_wanted` names were absent |
| `python3 Stage1_Instances/THM-M-0580/check_statement.py` | 0 | expression hash `938ef54298273a011a66395812b53e6bf8071b0925b84cd94ae5fb4f9a6eb664`; all four statement mutations killed; pinned toolchain and mathlib revision matched |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root remains open at M4 |
| scoped exact-root and cut-set `rg` search below | 0 | `PASS: no alternate exact-root or cut-set declaration found` |
| inverted forbidden-construct `rg --pcre2` scan below | 0 | `PASS: no prohibited proof construct in four owned Lean modules` |
| pinned marker `rg` search below | 0 | exactly three matching `proof_wanted` entries at lines 43, 47, and 52 of `PoincareConjecture.lean` |
| `cd Formalizations/Lean && timeout 60 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |

The narrow Lean check was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0580
tmp=$(mktemp -d /tmp/thm-m-0580-slot26-headbbe7a5bd.XXXXXX)
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

The scoped source checks were:

```bash
hits=$(rg -n --glob '*.lean' \
  --glob '!Stage1_Instances/THM-M-0580/Statement.lean' \
  --glob '!Stage1_Instances/THM-M-0580/ObligationTree.lean' \
  --glob '!Stage1_Instances/THM-M-0580/ProofBlockerProbe.lean' \
  '(PerelmanPoincareTarget|TopologicalThreeManifoldSmoothable|SmoothThreeDimensionalPoincare)' \
  Stage1_Instances Formalizations/Lean/AwesomeTheorems 2>/dev/null || true)
if [ -n "$hits" ]; then printf '%s\n' "$hits"; exit 1; else
  echo 'PASS: no alternate exact-root or cut-set declaration found'
fi

if rg -n --pcre2 \
  '(?<![A-Za-z0-9_])(sorry|admit|axiom|sorryAx|unsafe|implemented_by|native_decide|external)(?![A-Za-z0-9_])' \
  Stage1_Instances/THM-M-0580/{Statement.lean,AnchorAudit.lean,ObligationTree.lean,ProofBlockerProbe.lean};
then echo 'FORBIDDEN TOKEN FOUND'; exit 1; else
  echo 'PASS: no prohibited proof construct in four owned Lean modules'
fi

rg -n 'proof_wanted (ContinuousMap\.HomotopyEquiv\.nonempty_homeomorph_sphere|SimplyConnectedSpace\.nonempty_homeomorph_sphere_three|SimplyConnectedSpace\.nonempty_diffeomorph_sphere_three)' \
  Formalizations/Lean/.lake/packages/mathlib/Mathlib/Geometry/Manifold/PoincareConjecture.lean
```

The canonical `.lake` symlink remains the only pre-existing untracked path outside this owned
directory, so this is nonrelease evidence.

## Retry Condition

First return `M0580-N-SMOOTH` to the obligation-tree authority for an append-only correction. Then
implement the corrected smoothing package and complete the smooth-Poincare package without
placeholders. Alternatively, integrate an immutable, licensed, compatible Lean 4 terminal proof of
the exact root with a complete dependency lock after a graph revision is accepted.

Assuming either missing package, treating `proof_wanted` as an axiom, or presenting conditional
composition as root closure would violate the exact-target and proof-body gates. This is an owned
blocker artifact, not a proof receipt; it does not satisfy `S56-M-0580-PROOF` or support theorem
completion. Because the phase is not genuinely complete, `.stage1-worker-selftest.json` remains
absent.
