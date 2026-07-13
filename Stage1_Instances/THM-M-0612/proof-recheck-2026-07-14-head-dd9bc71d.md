# THM-M-0612 proof recheck at `dd9bc71d`

Item: `S56-M-0612-PROOF`

Date: `2026-07-14T03:10:00+08:00`

Base revision: `dd9bc71d70586d022d87833d780fbe15959b89b0`

Base tree: `d096d4ef8804532c9165b75d369f49b7b74945d8`

## Verdict

`blocked`. No eligible positive proof body was implemented or found for the
exact target `Stage1.THM_M_0612.StatementShape`. The remaining root cut is
`M0612-T-SQUARED`, which must derive `r ^ 2 <= R ^ 2` from the local
symplectic-embedding and cylinder hypotheses. The first unavailable package
is `M0612-C-CAPACITY`: neither this repository nor pinned mathlib constructs a
compatible symplectic capacity together with invariance, monotonicity,
conformality, and the necessary ball and cylinder computations. The alternate
frozen route likewise lacks almost-complex structures, pseudoholomorphic-curve
existence and compactness, energy identities, and monotonicity.

`ObligationTree.lean` still contains two real but nonterminal bodies.
`radius_le_of_sq_le` proves the elementary ordered-field transport, while
`root_of_radiusSquaredObstruction` accepts the complete geometric obstruction
as a premise. Introducing that premise as an axiom, bodyless declaration, or
assumed package would be a prohibited placeholder.

Current HEAD also contains `LocalEncoding.lean`. Its six placeholder-free
bodies establish identity-map nonvacuity, the sharp two-dimensional identity
example, origin membership, continuity and openness of the ball, and the
ambient derivative supplied by local smoothness. They strengthen the checked
local encoding but do not derive `RadiusSquaredObstruction`. Moreover, the
frozen registry, typed graphs, and `instance.json` inventory do not map these
bodies to new terminal obligations. This recheck therefore records no newly
closed obligation, receipt, composition certificate, or debt change.

No proof source or proof receipt was added. The root vector remains
`[H2, M3, R4]`, `root_closed=false`, and `theorem_complete=false`. Since the
assigned positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All accepted checks reused the automation-provided canonical pinned artifacts
read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
repair was requested. The untracked `.lake` symlink makes this nonrelease
evidence. During the run, concurrent workers left the unrelated optional
`flt-regular` checkout without a resolvable `HEAD`; to remain fail-closed and
avoid Lake's fetch path, the final replay used the pinned Lean executable and
the same prebuilt pinned library directories directly.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0612` | 0 | rank 256; planned hard-mathlib-anchor-and-wrapper lane; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0612/check_obligation_tree.py` | 0 | 26 obligations and 58 typed edges passed; denominator `2cad29b7...a4bc8`; root open M3 |
| isolated pinned trust-zero replay below | 0 | `Statement.lean`, `ObligationTree.lean`, and `LocalEncoding.lean` elaborated; each of the eight source axiom reports was exactly `[propext, Classical.choice, Quot.sound]` |
| owned Lean prohibited-construct scan | 1 | expected no-match exit for `sorry`, `admit`, declared axioms/constants/opaque/extern, `sorryAx`, `unsafe`, `implemented_by`, and `native_decide` |
| pinned Mathlib topical scan | 1 | expected no-match exit for nonsqueezing, Gromov width, symplectic capacity, or pseudoholomorphic-curve declarations |
| pinned environment checks | 0 | Lean 4.29.0 commit `98dc76e...16740`; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b` |
| JSON parse, hash, and blocker invariant assertions | 0 | current base/hashes, unchanged vector, empty proof-credit arrays, open flags, exact cut set, and absent completion manifest agree |
| scoped and per-new-file whitespace checks | 0 aggregate | both fresh files differ from `/dev/null` and have no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

The final isolated replay generated outputs only under `/tmp` and removed them:

```bash
set -euo pipefail
root=$PWD/Formalizations/Lean
lean=/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
paths=("$root/.lake/build/lib/lean")
for path in "$root"/.lake/packages/*/.lake/build/lib/lean; do
  paths+=("$path")
done
lean_path=$(IFS=:; echo "${paths[*]}")
target=$PWD/Stage1_Instances/THM-M-0612
tmp=$(mktemp -d /tmp/thm-m-0612-proof-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" --trust=0 \
  -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" --trust=0 \
  ObligationTree.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" --trust=0 \
  LocalEncoding.lean
```

The proof-relevant source SHA-256 values are `2de623b5...f919` for
`Statement.lean`, `0392a18a...07007` for `ObligationTree.lean`,
`278177c5...a117` for `LocalEncoding.lean`, `635af26d...38850` for the
obligation registry, and `def70532...50b2` for the typed graphs. The pinned
toolchain and Lake manifest hashes are `651c8acc...b1d2` and
`321626c8...2d81`.

## Retry Condition

Resume after a placeholder-free implementation of `M0612-T-SQUARED` and its
frozen nonlinear dependencies, or after discovery of an immutable compatible
Lean 4 terminal proof that can be pinned, exact-type transported, and checked
without changing the dependency lock.

This is an owned blocker artifact, not a proof receipt. It does not satisfy
`S56-M-0612-PROOF`, propose checklist state, or support audit completion,
theorem completion, validation, release, or master acceptance.
