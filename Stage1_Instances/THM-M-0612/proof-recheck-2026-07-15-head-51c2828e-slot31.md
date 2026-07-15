# THM-M-0612 proof recheck at `51c2828e` (slot31)

Item: `S56-M-0612-PROOF`

Date: `2026-07-15T16:11:39+08:00`

Base revision: `51c2828e82ffb19860830f78b771f80e13ad7dff`

Base tree: `4655b8b40829513de6fb5661344b33fc7cd17cd1`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact target
`Stage1.THM_M_0612.StatementShape`. The frozen immediate root cut remains
`M0612-T-SQUARED`, represented by
`Stage1.THM_M_0612.RadiusSquaredObstruction`: derive `r ^ 2 <= R ^ 2` from the
canonical local smooth symplectic-embedding and cylinder hypotheses.

The first deep unavailable package is `M0612-C-CAPACITY`. Neither the repository
nor the pinned package closure constructs a compatible symplectic capacity
together with invariance, monotonicity, conformality, and ball and cylinder
computations. The frozen alternative branch also lacks compatible
almost-complex structures and pseudoholomorphic-curve existence, compactness,
energy, and monotonicity results.

`ObligationTree.lean` supplies only the real ordered-field transport
`radius_le_of_sq_le` and the conditional final composition
`root_of_radiusSquaredObstruction`. The latter accepts the entire missing
geometric obstruction as a premise; it does not construct that premise. The
local-encoding and sanity declarations prove nonvacuity, openness,
differentiability, form nondegeneracy, and derivative injectivity, but none
closes the frozen root cut.

A fresh source inventory found no terminal declaration in the target, legacy
module, pinned packages, or available worker-clone sources. Pinned mathlib has
finite symplectic-matrix infrastructure, not nonlinear nonsqueezing. The legacy
`S1_M_256.lean` interface uses global embedding data and leaves its capacity
computations open. The immutable prerequisite audit's only named external Lean
4 theorem has an admitted body and admitted dependencies, so it is ineligible
for pinning or proof credit.

No proof source or positive receipt was added. The root vector remains
`[H2, M3, R4]`, `root_closed=false`, and `theorem_complete=false`. The
prerequisite obligation-tree item is worker-provisional `[_]`, not
master-accepted `[x]`. Because the assigned proof phase is not complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was used read-only. No `lake update`, `lake
build`, dependency clone/fetch, checkout, repair, or other `.lake` mutation was
performed. Temporary Lean output was isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0612` | 0 | Rank 256; planned hard-mathlib-anchor-and-wrapper lane; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short --untracked-files=all` before edits | 0 | Only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present. |
| `python3 Stage1_Instances/THM-M-0612/check_obligation_tree.py` | 0 | `PASS THM-M-0612 obligation tree: 26 obligations, 58 typed edges`; denominator `2cad29b7...a4bc8`; root open M3. |
| isolated pinned `lake env lean --trust=0 -t0` replay of all four proof-relevant owned modules | 0 | `Statement.lean`, `ObligationTree.lean`, `LocalEncoding.lean`, and `EncodingSanityProbe.lean` elaborated under Lean 4.29.0; each of ten axiom reports was exactly `[propext, Classical.choice, Quot.sound]`; temporary outputs were removed. |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 AwesomeTheorems/Stage1/S1_M_256.lean` | 0 | The legacy interface elaborated and printed `StatementShape : Prop`, but no theorem proving it. |
| owned Lean prohibited-construct scan | 1 | Expected no-match exit; no `sorry`, `admit`, axiom/bodyless declaration, unsafe declaration, or native-decision shortcut occurs. |
| complete pinned-package topical scan | 1 | Expected no-match exit with zero lines for nonsqueezing, Gromov width, symplectic capacity, or pseudoholomorphic declarations. |
| exact-target and worker-clone inventory | 0 | Only the conditional `root_of_radiusSquaredObstruction` returns the root; all available proof-relevant worker sources have the same hashes and no terminal body. |
| pinned environment checks | 0 | Lean 4.29.0 commit `98dc76e...16740`; Lake 5.0.0; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`; flt-regular `56161b6e...1a27`. |
| source and frozen-artifact SHA-256 checks | 0 | Statement `2de623b5...f919`; conditional composition `0392a18a...07007`; registry file `635af26d...8850`; typed graphs `def70532...50b2`; pins unchanged. |
| JSON parse plus fail-closed identity, hash, cut-set, and changed-path assertions | 0 | `PASS blocker identity, current base/tree, hashes, fail-closed state, exact cut, changed paths, and absent selftest`. |
| tracked-diff and per-fresh-file whitespace checks | 0 aggregate | Both target-owned evidence files passed. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent because the positive proof phase is blocked. |

The isolated replay used this exact command shape:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0612
tmp=$(mktemp -d /tmp/thm-m-0612-proof-slot31.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cd "$lean_root"
base_path=$(lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 -R "$target" \
  -o "$tmp/Statement.olean" "$target/Statement.lean"
for module in ObligationTree LocalEncoding EncodingSanityProbe; do
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" timeout 300 lake env lean \
    --trust=0 -t0 -R "$target" "$target/$module.lean"
done
```

Output SHA-256 values were `e3b0c442...b855`, `039f16b7...35a`,
`4515cf76...0a3c5`, and `94de4565...81e`, respectively. Proof-input hashes
remain `2de623b5...f919` for `Statement.lean`, `0392a18a...07007` for
`ObligationTree.lean`, `278177c5...a117` for `LocalEncoding.lean`, and
`1b61df00...ed82` for `EncodingSanityProbe.lean`.

## Retry Condition

Resume after a placeholder-free implementation of `M0612-T-SQUARED` and its
frozen nonlinear dependencies, or discovery of an immutable compatible Lean 4
terminal proof that can be pinned, exact-type transported, and checked without
changing the dependency lock.

This is fresh target-owned nonrelease blocker evidence, not a proof receipt. It
does not satisfy `S56-M-0612-PROOF`, propose checklist state, or support audit
completion, theorem completion, validation, release, or master acceptance.
