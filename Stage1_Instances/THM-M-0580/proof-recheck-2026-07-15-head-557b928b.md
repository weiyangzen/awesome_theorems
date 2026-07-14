# THM-M-0580 proof-phase recheck at base 557b928b

Item: `S56-M-0580-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `557b928b377b386864527c9fb4831d45857837aa`

Base tree: `e677879a6eb4cb9d6795ba1bd78726af06ab9465`

## Verdict

`blocked`. No eligible terminal Lean 4 proof body exists in the repository or pinned dependency
closure for the exact proposition
`Stage1Instances.THM_M_0580.PerelmanPoincareTarget`. No proof body or proof receipt was added. The
proof item remains `[ ]`, the root vector remains `[H2, M4, R4]`, and the exact root and theorem
remain incomplete.

The frozen immediate root cut set remains:

- `M0580-N-SMOOTH`, the proposed topological smoothing package;
- `M0580-T-SMOOTH-POINCARE`, the full smooth three-dimensional Poincare package.

The checked theorem `root_of_smoothing_and_smooth_poincare` consumes both packages and only
composes them into the canonical root. It constructs neither. The checked diagnostic
`smoothThreeDimensionalPoincare_of_perelmanPoincareTarget` runs in the converse direction, from the
root to the frozen smooth package, so using it to manufacture a premise for the root would be
circular.

Pinned mathlib contains the matching generalized, topological, and smooth Poincare signatures only
as `proof_wanted` source markers. Batteries documents that such declarations are elaborated under
`withoutModifyingEnv`, discarded, and unavailable as axioms. The trust-zero probe confirms that all
three names are unknown after import. A scoped current-base search found no alternate exact-root or
cut-set body. The immutable anchor audit's external candidate merely defines a dimension-three
proposition and proves an unrelated dimension-zero generalized special case.

There is also a fail-closed defect in the frozen `M0580-N-SMOOTH` contract. It receives an already
selected `ChartedSpace Euclidean3 M` and requires `Nonempty (IsManifold ... infinity M)` for that
same atlas. `Nonempty` around a proposition does not choose a replacement compatible smooth atlas.
Correcting the obligation requires an append-only prerequisite graph revision with a replacement
atlas, its smoothness proof, and a checked compatibility/assembly bridge. This proof worker did not
alter the frozen registry.

## Validation

All commands ran in this worker clone. The automation-provided untracked `.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, or dependency mutation was run.
Lean outputs were confined to a disposable `/tmp` directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; planned; L0/rework-required; theorem incomplete |
| isolated trust-zero `lake env lean` chain below | 0 | exact statement, conditional composition, and blocker probe elaborated; both local theorem axiom reports were `[propext, Classical.choice, Quot.sound]`; all three `#check_failure` probes confirmed that the `proof_wanted` names were absent |
| `timeout 300 python3 Stage1_Instances/THM-M-0580/check_statement.py` | interrupted | stopped without a result under heavy shared-runner contention; the helper left no temporary source behind, and this non-result supplies no validation credit |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root remains open at M4 |
| scoped exact-root and cut-set `rg` search | 0 | `PASS: no alternate exact-root or cut-set declaration found` |
| inverted forbidden-construct `rg --pcre2` scan | 0 | `PASS: no prohibited proof construct in four owned Lean modules` |
| pinned `proof_wanted` marker `rg` search | 0 | exactly three matching markers at lines 43, 47, and 52 of `PoincareConjecture.lean` |
| `cd Formalizations/Lean && timeout 60 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |

The narrow Lean check was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0580
tmp=$(mktemp -d /tmp/thm-m-0580-slot27-head557b928b.XXXXXX)
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

The emitted temporary oleans had SHA-256
`8c69718898cfefd3f33ccce0ac95ca8f4e9a82bc28fda79b6b91ae01b7cffba6` for
`Statement.olean` and
`6f2ad414a2fe0d0dd9544cc489751163408ac7b85a9823e3935ff1663af7dcb8` for
`ObligationTree.olean`.

The owned `check_statement.py` helper was started but deliberately stopped without a result under
heavy shared-runner contention. It left no file behind. Exact statement elaboration still passed in
the isolated trust-zero chain above; the unchanged statement and environment hashes match the
already integrated mutation result, canonical expression SHA-256
`938ef54298273a011a66395812b53e6bf8071b0925b84cd94ae5fb4f9a6eb664`. No proof-completion claim
depends on that prior mutation evidence.

## Retry Condition

First return `M0580-N-SMOOTH` to the obligation-tree authority for an append-only correction. Then
implement the corrected smoothing package and complete smooth-Poincare package without
placeholders. Alternatively, integrate an immutable, licensed, compatible Lean 4 terminal proof of
the exact root with a complete dependency lock after a graph revision is accepted.

Assuming either missing package, treating `proof_wanted` as an axiom, or presenting conditional
composition as root closure would violate the exact-target and proof-body gates. This is an owned
blocker artifact, not a proof receipt; it does not satisfy `S56-M-0580-PROOF`, propose state
promotion, or support theorem completion. Because the assigned proof phase is not genuinely
complete, `.stage1-worker-selftest.json` remains absent.
