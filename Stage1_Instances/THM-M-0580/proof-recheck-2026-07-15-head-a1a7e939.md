# THM-M-0580 proof-phase recheck at base a1a7e939

Item: `S56-M-0580-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `a1a7e939e58f103f5ff5d23af51437fa8658aa04`

Base tree: `d881fd9641fa3e5f3ebe5082b35672981e90adcf`

## Verdict

`blocked`. No eligible terminal Lean 4 proof body exists in the repository or pinned dependency
closure for the exact frozen proposition
`Stage1Instances.THM_M_0580.PerelmanPoincareTarget`. This attempt adds no proof body and leaves the
root vector at `[H2, M4, R4]`. The proof item remains `[ ]`; the audit, root, and theorem remain
incomplete.

The frozen immediate root cut set is unchanged:

- `M0580-N-SMOOTH`, the proposed topological smoothing package;
- `M0580-T-SMOOTH-POINCARE`, the full smooth three-dimensional Poincare package.

The checked theorem `root_of_smoothing_and_smooth_poincare` assumes both packages and only composes
them into the exact root. It constructs neither package and supplies no root proof credit. The
smooth branch still requires metric construction, short-time Ricci flow, noncollapsing, canonical
neighborhoods, surgery construction and iteration, finite extinction, decomposition, and
fundamental-group elimination.

Pinned mathlib contains the generalized, topological, and smooth Poincare signatures only as
`proof_wanted` source markers. Importing the module retains none of those declarations: the direct
trust-zero probe below reports all three names as unknown constants. A scoped repository and pinned
dependency search found no alternate retained root or cut-set declaration. The immutable external
candidate recorded by the prerequisite audit has only a dimension-three statement and an unrelated
dimension-zero proof, not a terminal dimension-three proof. As a supplementary non-credit-bearing
check, the locally cached mathlib `origin/master` at
`4efb186f102ebfd2eea1545c151d6fbcfdff0e43` still carries the topological name as `proof_wanted`.

There is also an earlier fail-closed defect in `M0580-N-SMOOTH`. Its Lean contract receives an
already selected arbitrary `ChartedSpace Euclidean3 M` and asks for
`Nonempty (IsManifold ... infinity M)`. Mathlib defines `ChartedSpace` as the selected atlas and
`IsManifold` as compatibility of that atlas with a differentiability groupoid. `Nonempty` around
the proposition does not choose a replacement atlas. This is stronger than a Moise-style
smoothability theorem. Correcting the obligation requires a replacement smooth atlas, its
`IsManifold` proof, and a topology or C0-atlas compatibility bridge, recorded by an append-only
registry revision from the prerequisite authority. This proof worker did not rewrite that frozen
registry.

Since the latest integrated recheck at commit `608b64de`, neither this target nor the Lean
toolchain/manifest changed. All proof-relevant hashes remain unchanged, and no new eligible proof
candidate appeared at the current base.

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
| `python3 Stage1_Instances/THM-M-0580/check_statement.py` | 0 | all four mutations killed; exact expression hash, toolchain, and mathlib revision matched |
| isolated trust-zero `lake env lean` recipe below | 0 | exact statement and conditional composition elaborated; `#print axioms` reported `[propext, Classical.choice, Quot.sound]` |
| direct trust-zero probe of the three matching mathlib names | 1 | expected negative evidence: every name was `Unknown constant` |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root remains open at M4 |
| forbidden-construct `rg` scan of the three Lean modules | 1 | expected no-match status; no `sorry`, `admit`, `axiom`, or `sorryAx` token was found |
| scoped retained-declaration `rg` search | 0 | only unrelated Poincare names, audit declarations, and statement transport were found; no alternate root or cut-set terminal body exists |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |

The successful isolated elaboration used the pinned `lake env lean` executable with a manually
assembled read-only `LEAN_PATH`:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0580
tmp=$(mktemp -d /tmp/thm-m-0580-slot21-heada1a7e939.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
paths=("$lean_root/.lake/build/lib/lean")
for p in "$lean_root"/.lake/packages/*/.lake/build/lib/lean; do paths+=("$p"); done
lean_path=$(IFS=:; printf '%s' "${paths[*]}")
cd "$target"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$lean_path" timeout 300 lake env lean --trust=0 -t0 ObligationTree.lean
```

The direct probe imported `Mathlib.Geometry.Manifold.PoincareConjecture` and checked:

```text
ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere
SimplyConnectedSpace.nonempty_homeomorph_sphere_three
SimplyConnectedSpace.nonempty_diffeomorph_sphere_three
```

Each check returned `Unknown constant`. The current proof-relevant SHA-256 values are:

```text
Statement.lean              612007bf5f9ef681b3866d829cb8d2c0d05e31a4fa2fed6830f3643c04d959b3
ObligationTree.lean         18be2e2a48c6add87f31cf4490b51952ddc43337d7767ed18ba3bbba0f90af41
obligation-registry.json    b19c7be9bd2bd1051d0e147c1b3efb247094e17f2451feace0697c756e57fdef
typed-graphs.json           a300ce79eb8557b4aea9dbfe84dd2e3a14dc34d88ef472567b8219d3b2609a6c
anchor-audit.json           4ee03f80cb99a3c33885a6a107da1489d3d359089db5b6194fb8397a98d924e4
validation-specs.json       1da6dd0adb434cae3d0623bdfde4f6906d8cbc239f1158f7932f416247169e69
lake-manifest.json          321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81
```

The network-backed anchor replay was not rerun. The relied-on immutable candidate is already
content-addressed, and no conclusion in this local proof recheck needs a moving network response.

## Retry Condition

First return `M0580-N-SMOOTH` to the obligation-tree authority for an append-only correction that
carries a replacement smooth atlas and checked assembly bridge. Then resume proof execution only
after placeholder-free implementations of the corrected smoothing package and the full
smooth-Poincare package. Alternatively, an immutable compatible Lean 4 proof of the exact root,
with a complete dependency lock and license, could bypass that route after a new graph revision is
accepted.

Assuming either package, treating `proof_wanted` as an axiom, or presenting the conditional
composition as root closure would violate the exact-target and proof-body gates. This is an owned
blocker artifact, not a proof receipt. It does not satisfy `S56-M-0580-PROOF`, propose state
promotion, or support theorem completion. Because the assigned proof phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` remains absent.
