# THM-M-0612 proof recheck at `3551812a`

Item: `S56-M-0612-PROOF`

Date: `2026-07-14T04:08:30+08:00`

Base revision: `3551812aeaf826b94804e464b34511a7bbc7f6ff`

Base tree: `6ed6612d0a642e6879579700427c67045c1a34d7`

## Verdict

`blocked`. No eligible positive proof body was implemented or found for the
exact target `Stage1.THM_M_0612.StatementShape`. The remaining root cut is
`M0612-T-SQUARED`, which must derive `r ^ 2 <= R ^ 2` from the frozen local
symplectic-embedding and cylinder hypotheses. The first unavailable package
is `M0612-C-CAPACITY`: neither this repository nor pinned mathlib constructs a
compatible symplectic capacity together with invariance, monotonicity,
conformality, and the required ball and cylinder computations. The alternate
frozen route likewise lacks almost-complex structures, pseudoholomorphic-curve
existence and compactness, energy identities, and monotonicity.

`ObligationTree.lean` contains two real but nonterminal bodies.
`radius_le_of_sq_le` proves the elementary ordered-field transport, while
`root_of_radiusSquaredObstruction` accepts the complete geometric obstruction
as a premise. Introducing that premise as an axiom, bodyless declaration, or
assumed package would be a prohibited placeholder.

The legacy `S1_M_256.lean` module supplies only a stronger global embedding
interface, elementary supremum facts, and conditional Gromov-width transfers.
It leaves embedding transitivity and the hard ball/cylinder width bounds open,
so it cannot exact-type transport to the frozen local-domain root. The only
named external Lean 4 nonsqueezing candidate found by the prerequisite audit
has a `sorry` body and admitted dependencies, and therefore receives no proof
credit.

`LocalEncoding.lean` has six placeholder-free bodies establishing identity-map
nonvacuity, the sharp two-dimensional identity example, origin membership,
continuity and openness of the ball, and the ambient derivative supplied by
local smoothness. An independent disposable probe also checked a nontrivial
anisotropic symplectic scaling and found no encoding inconsistency or
counterexample shortcut. These facts do not derive `RadiusSquaredObstruction`,
and the frozen registry maps none to a newly closed terminal obligation.

No proof source, newly closed obligation, receipt, or composition certificate
was added. The root vector remains `[H2, M3, R4]`, `root_closed=false`, and
`theorem_complete=false`. Since the assigned positive proof phase is not
genuinely self-tested as complete, `.stage1-worker-selftest.json` is
deliberately absent.

## Validation

All checks reused the automation-provided canonical pinned artifacts read-only.
No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was
requested. Generated Lean output was isolated under `/tmp` and removed. The
untracked `.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0612` | 0 | rank 256; planned hard-mathlib-anchor-and-wrapper lane; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0612/check_obligation_tree.py` | 0 | 26 obligations and 58 typed edges passed; denominator `2cad29b7...a4bc8`; root open M3 |
| isolated pinned `lake env` Lean replay below | 0 | `Statement.lean`, `ObligationTree.lean`, and `LocalEncoding.lean` elaborated with `--trust=0`; each of the eight source axiom reports was exactly `[propext, Classical.choice, Quot.sound]` |
| owned Lean prohibited-construct scan | 1 | expected no-match exit for `sorry`, `admit`, declared axioms/constants/opaque/extern, `sorryAx`, `unsafe`, `implemented_by`, and `native_decide` |
| pinned Mathlib topical scan | 1 | expected no-match exit for nonsqueezing, Gromov width, symplectic capacity, or pseudoholomorphic-curve declarations |
| independent disposable scaling probe | 0 | a nontrivial symplectic anisotropic scaling elaborated; no inconsistency or counterexample shortcut was found |
| pinned environment checks | 0 | Lean 4.29.0 commit `98dc76e...16740`; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b` |
| JSON parse and blocker invariant assertions | 0 | identity, current base/tree, unchanged vector, open-root flags, empty proof-credit arrays, and exact cut set agree |
| scoped whitespace checks | 0 | no whitespace diagnostics in the owned diff or either fresh file |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

The isolated replay wrote only temporary files and removed them:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0612
tmp=$(mktemp -d /tmp/thm-m-0612-proof-slot55-sequential.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/ObligationTree.lean" "$tmp/ObligationTree.lean"
cp "$target/LocalEncoding.lean" "$tmp/LocalEncoding.lean"
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" \
  --trust=0 -t0 -j1 -o Statement.olean Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH=".:$lean_path" timeout 300 "$lean" \
  --trust=0 -t0 -j1 -o ObligationTree.olean ObligationTree.lean
LEAN_NUM_THREADS=1 LEAN_PATH=".:$lean_path" timeout 300 "$lean" \
  --trust=0 -t0 -j1 LocalEncoding.lean
```

The proof-relevant source SHA-256 values are `2de623b5...f919` for
`Statement.lean`, `0392a18a...07007` for `ObligationTree.lean`,
`278177c5...a117` for `LocalEncoding.lean`, `635af26d...38850` for the
obligation registry, and `def70532...50b2` for the typed graphs. The pinned
toolchain and Lake manifest hashes are `651c8acc...b1d2` and
`321626c8...2d81`. The three Lean output hashes were `e3b0c442...b855`,
`039f16b7...35a`, and `4515cf76...3c5`.

## Retry Condition

Resume after a placeholder-free implementation of `M0612-T-SQUARED` and its
frozen nonlinear dependencies, or after discovery of an immutable compatible
Lean 4 terminal proof that can be pinned, exact-type transported, and checked
without changing the dependency lock.

This is an owned blocker artifact, not a proof receipt. It does not satisfy
`S56-M-0612-PROOF`, propose checklist state, or support audit completion,
theorem completion, validation, release, or master acceptance.
