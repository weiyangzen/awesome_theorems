# THM-M-0612 proof recheck at `78df0e1c`

Item: `S56-M-0612-PROOF`

Date: `2026-07-15T07:46:54+08:00`

Base revision: `78df0e1ce628d7e18e48441678ad85f9552d1b77`

Base tree: `f6355c949fed70817ee3929831406a4b454a0977`

## Verdict

`blocked`. No eligible positive proof body was implemented or found for the
exact target `Stage1.THM_M_0612.StatementShape`. The remaining root cut is
`M0612-T-SQUARED`, which must derive `r ^ 2 <= R ^ 2` from the canonical local
symplectic-embedding and cylinder hypotheses; the absence of an eligible exact
body for that node is the first failed gate. The first deep unavailable
package is `M0612-C-CAPACITY`: neither this repository nor the complete pinned
Lean package closure constructs a compatible symplectic capacity with the
invariance, monotonicity, conformality, ball, and cylinder results required by
the frozen route. The local-embedding transport, scaling normalization, and
both geometric branches also remain open.

`ObligationTree.lean` contains two real but nonterminal bodies.
`radius_le_of_sq_le` proves the elementary ordered-field transport, while
`root_of_radiusSquaredObstruction` accepts the complete missing geometric
obstruction as a premise. Introducing that premise as an axiom, bodyless
declaration, or assumed package would be a prohibited placeholder.

`LocalEncoding.lean` contains six placeholder-free sanity lemmas. They show
that the embedding hypotheses are inhabited at equal radii, that the source
ball is nonempty and open, and that local smoothness supplies the ambient
derivative used by the statement. `EncodingSanityProbe.lean` additionally
checked that `standardForm` is nondegenerate and that form preservation forces
each on-ball derivative to be injective. These checks rule out the enumerated
dimension, empty-domain, degenerate-form, and derivative-collapse shortcuts.
These facts still do not derive `RadiusSquaredObstruction` or close a frozen
root-cut obligation. Every open geometric obligation currently has only a
planned prose fingerprint, so no exact typed obligation closure can be
inferred from the auxiliary lemmas. The new file is retained as non-credit
diagnostic evidence only: it is not bound into `instance.json`, the frozen
registry or typed graphs, or `validation-specs.json`.

The legacy `S1_M_256.lean` module supplies a different global-map interface,
an order-theoretic Gromov-width lemma, and conditional reductions. Its
embedding composition and geometric ball/cylinder bounds remain open, so it
does not exact-type close the local-domain target. A fresh complete pinned-
package search found no terminal theorem. The prerequisite external audit
found one named nonsqueezing declaration, but its body and dependencies are
admitted. A separate discovery-only capacity interface assumes monotonicity
and normalization as structure fields rather than constructing them; it is
not an immutable dependency proposal. Neither source is eligible for proof
credit.

Two auxiliary encoding-audit proof bodies were added, but no root-relevant or
root-closing proof body and no positive proof receipt was added. The root vector remains
`[H2, M3, R4]`, `root_closed=false`, and `theorem_complete=false`. Since the
assigned positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All Lean checks reused the automation-provided canonical pinned artifacts
read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was requested. Generated Lean output was isolated under `/tmp` and
removed. The untracked `.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0612` | 0 | rank 256; planned hard-mathlib-anchor-and-wrapper lane; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0612/check_obligation_tree.py` | 0 | `PASS THM-M-0612 obligation tree: 26 obligations, 58 typed edges`; denominator `2cad29b7...a4bc8`; root open M3 |
| isolated pinned `lake env lean --trust=0 -t0` dossier replay below | 0 | statement and the two existing proof-fragment sources elaborated; every one of the eight declaration reports was exactly `[propext, Classical.choice, Quot.sound]` |
| isolated `EncodingSanityProbe.lean` replay | 0 | nondegeneracy of `standardForm` and injectivity of every form-preserving on-ball derivative elaborated; both declarations reported exactly `[propext, Classical.choice, Quot.sound]` |
| owned Lean prohibited-construct scan | 1 | expected no-match exit; no `sorry`, `admit`, axiom/bodyless declaration, unsafe/oracle construct, or native decision shortcut occurs |
| complete pinned-package topical scan | 1 | expected no-match exit for nonsqueezing, Gromov width, symplectic capacity, or pseudoholomorphic declarations |
| repo-local topical inventory | 0 | hits were this dossier, legacy `S1_M_256`, and unrelated `THM-M-0611`; inspection found no exact terminal body |
| pinned environment checks | 0 | Lean 4.29.0 commit `98dc76e...16740`; Lake 5.0.0; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`; pinned file hashes matched |
| scoped input audit since `5558ec5b` | 0 | no pre-existing proof input, frozen graph/registry, audit receipt, validation spec, or pin changed after the latest integrated recheck |
| JSON parse and blocker-invariant assertions | 0 | `PASS blocker identity, hashes, fail-closed state, cut set, changed paths, and absent selftest` |
| scoped and per-new-file whitespace checks | 0 aggregate | `PASS JSON, structural, whitespace, fresh-file, and absent-selftest checks` |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

The isolated dossier replay generated outputs only under `/tmp` and removed
them:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0612
tmp=$(mktemp -d /tmp/thm-m-0612-proof-slot45-78df0e1c.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
base_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
(cd "$lean_root" && LEAN_NUM_THREADS=1 timeout 300 lake env lean \
  --trust=0 -t0 -R "$target" -o "$tmp/Statement.olean" \
  "$target/Statement.lean")
(cd "$lean_root" && LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" \
  timeout 300 lake env lean --trust=0 -t0 -R "$target" \
  "$target/ObligationTree.lean")
(cd "$lean_root" && LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" \
  timeout 300 lake env lean --trust=0 -t0 -R "$target" \
  "$target/LocalEncoding.lean")
(cd "$lean_root" && LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" \
  timeout 300 lake env lean --trust=0 -t0 -R "$target" \
  "$target/EncodingSanityProbe.lean")
```

The statement, obligation-tree, local-encoding, and encoding-probe output
SHA-256 values were `e3b0c442...b855`, `039f16b7...35a`,
`4515cf76...0a3c5`, and `94de4565...81e`. The proof-relevant source SHA-256
values are `2de623b5...f919` for `Statement.lean`, `0392a18a...07007` for
`ObligationTree.lean`, `278177c5...a117` for `LocalEncoding.lean`,
`1b61df00...ed82` for `EncodingSanityProbe.lean`,
`635af26d...38850` for the obligation registry, and `def70532...50b2` for the
typed graphs. The pinned toolchain and Lake manifest hashes are
`651c8acc...b1d2` and `321626c8...2d81`.

The structured blocker was parsed with `python3 -m json.tool`. An inline
read-only assertion script recomputed every `source_hashes` entry, checked the
item, theorem, base revision and tree, required all completion flags and proof-
credit arrays to remain empty or false, required the exact root cut and
unchanged debt vector, checked the three fresh changed paths, and required the
completion self-test manifest to be absent.

## Retry Condition

Resume after a placeholder-free implementation of `M0612-T-SQUARED` and its
frozen nonlinear dependencies, or after discovery of an immutable compatible
Lean 4 terminal proof that can be pinned, exact-type transported, and checked
without changing the dependency lock.

This is an owned blocker artifact, not a proof receipt. It does not satisfy
`S56-M-0612-PROOF`, propose checklist state, or support audit completion,
theorem completion, validation, release, or master acceptance.
