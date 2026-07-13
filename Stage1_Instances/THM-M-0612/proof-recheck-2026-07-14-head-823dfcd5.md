# THM-M-0612 proof recheck at `823dfcd5`

Item: `S56-M-0612-PROOF`

Date: `2026-07-14T02:10:25+08:00`

Base revision: `823dfcd5e231e84436ac3d88948d8e669c168fdb`

Base tree: `a87f5f99350f49ddeb9d7df23dc6e0fe6fe3011f`

## Verdict

`blocked`. This current-base retry found no eligible positive proof body for
the exact target `Stage1.THM_M_0612.StatementShape`. The remaining root cut is
`M0612-T-SQUARED`, which must derive `r ^ 2 <= R ^ 2` from the local
symplectic embedding and cylinder hypotheses. The first unavailable package is
still `M0612-C-CAPACITY`: neither the repository nor pinned mathlib constructs
a compatible symplectic capacity with invariance, monotonicity, conformality,
and the required ball and cylinder computations. The alternate frozen route
also lacks compatible almost-complex structures, pseudoholomorphic-curve
existence and compactness, energy identities, and monotonicity.

The two bodies in `ObligationTree.lean` remain valid but nonterminal.
`radius_le_of_sq_le` is the elementary ordered-field transport, while
`root_of_radiusSquaredObstruction` accepts `RadiusSquaredObstruction` as a
premise rather than constructing it. Treating that premise as an axiom,
bodyless declaration, or assumed package would violate the proof-body gate.

A fresh sanity probe also ruled out an accidental-vacuity shortcut. In a
disposable module that manually copied the target definitions, Lean checked
that the identity map is an
`IsSymplecticEmbeddingOnBall r` for every finite coordinate type and that it
maps `ball r` into `cylinder i r`. Thus the frozen hypotheses are inhabited at
the sharp boundary. This rules out the suspected inconsistent-premise shortcut;
the probe receives neither statement-identity nor proof credit.

No source or proof receipt was added. The root vector remains
`[H2, M3, R4]`, `root_closed=false`, and `theorem_complete=false`. Because the
assigned positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All local checks reused the automation-provided canonical pinned `.lake`
artifacts read-only. No `lake update`, `lake build`, dependency clone/fetch, or
`.lake` mutation was performed. The untracked `.lake` symlink makes this
nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0612` | 0 | rank 256, planned, hard-mathlib-anchor-and-wrapper lane, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0612/check_obligation_tree.py` | 0 | 26 obligations and 58 typed edges passed; denominator `2cad29b7...a4bc8`; root open M3 |
| isolated trust-zero Lean recipe below | 0 | exact statement and conditional composition elaborated; both axiom reports were `[propext, Classical.choice, Quot.sound]` |
| `cd Formalizations/Lean && lake env lean --trust=0 /tmp/Probe0612.lean` | 0 | disposable identity-map probe elaborated with no output; it received no obligation or proof credit |
| scoped repo, legacy, and pinned-package terminal search | 0 | hits were owned statement/audit text and legacy definitions or interfaces; pinned Mathlib itself returned no match |
| prohibited-construct scan of all owned Lean sources | 1 | expected no-match exit for `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, and `native_decide` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386...95`; tree `bdc39a31...b2b` |
| JSON parse and blocker invariant assertions | 0 | fresh record is valid and its blocked/open flags, unchanged vector, empty receipts, cut set, and absent completion self-test agree |
| per-file new-file whitespace checks | 0 aggregate | each file returned the expected difference status with no whitespace diagnostic |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test manifest deliberately absent |

The isolated replay ran from the repository root and wrote only to a disposable
`/tmp` directory:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0612
tmp=$(mktemp -d /tmp/thm-m-0612-proof-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_PATH="$lean_path" "$lean" --trust=0 -o "$tmp/Statement.olean" Statement.lean
LEAN_PATH="$tmp:$lean_path" "$lean" --trust=0 ObligationTree.lean
```

The checked source SHA-256 values were `2de623b5...f919` for
`Statement.lean`, `0392a18a...07007` for `ObligationTree.lean`,
`635af26d...38850` for `obligation-registry.json`, and
`def70532...50b2` for `typed-graphs.json`. The pinned toolchain and Lake
manifest hashes were `651c8acc...b1d2` and `321626c8...2d81`.

## Retry Condition

Resume after a placeholder-free implementation of `M0612-T-SQUARED` and its
frozen nonlinear dependencies, or after discovery of an immutable compatible
Lean 4 terminal proof that can be pinned, exact-type transported, and checked
without changing the dependency lock.

This is an owned blocker artifact, not a proof receipt. It does not satisfy
`S56-M-0612-PROOF`, propose checklist state, or support audit, theorem,
validation, release, or master-completion claims.
