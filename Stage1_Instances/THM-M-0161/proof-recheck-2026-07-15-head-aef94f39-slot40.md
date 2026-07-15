# THM-M-0161 current-base proof refutation recheck

Item: `S56-M-0161-PROOF`

Intent: `prove`

Base revision: `aef94f39853f9222e48f83b2358a6822aafd3c50`

Base tree: `8c42e198fdbcc36b0f5cc0f865e0961715a35c17`

Validated: `2026-07-15T20:22:08+08:00` (`Asia/Shanghai`)

## Verdict

`blocked`. No positive proof body can truthfully be implemented for the exact frozen target because
the current base contains a placeholder-free kernel proof of its exact negation:

```text
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
```

`Counterexample.lean` is tracked at SHA-256
`2f306383c91022b4767de275a59be8fbb987da4d765f2d72e632a83d34f710f9`. This worker did not
change it. A fresh disposable consistency probe additionally checked

```text
positive_candidate_implies_false :
  FundamentalTheoremOfSpaceCurvesTarget -> False
```

by applying `frozen_target_false`. Thus a purported positive inhabitant of the unchanged target
would close `False` in the same pinned environment. This recheck adds only the two current-base
blocker reports. It does not change the statement, proof body, obligation registry, typed graphs,
scheduler authority, dependencies, or another target.

The frozen proposition assumes only `DifferentiableOn` curvature and torsion but requires a `C^3`
realizing curve. The checked counterexample selects the interval `(-1, 1)`, zero torsion, and

```text
kappa161(x) = 2 + x^2 * sin(1/x).
```

This curvature is differentiable everywhere and positive on the interval, but its derivative is
discontinuous at zero. Conversely, `curvature_is_contDiffOn_one` proves that positive curvature
realized by a `C^3` curve is `C^1`. The existence conclusion would therefore make `kappa161` both
`C^1` and not `C^1`. This refutes only the under-regularized frozen Lean proposition, not the
classical theorem with source-faithful coefficient regularity.

The exact-target truth and consistency gate is the first failed gate. The historical conditional
composition in `ObligationTree.lean` still requires complete `ExistencePackage` and
`UniquenessPackage` premises and gives no positive proof credit. The obligation-tree prerequisite
remains `[_]` pending master acceptance, and this proof item remains `[ ]`.

No proof receipt, accepted state, audit completion, validation completion, release evidence, or
theorem completion is claimed. The current structured authorities remain unchanged: the instance
records `[H1, M4, R4]`, the v1 typed graph records `[H3, M3, R4]`, and both report
`theorem_complete=false`. The checked refutation supports a proposed exact-frozen-target
classification of `[H5, M5, R4]`, but reconciliation belongs to authorized statement/source review
and a versioned graph update, not this proof worker.

## Validation

All commands ran from this automation clone. The Lean replay reused the existing pinned `.lake`
closure read-only, wrote oleans and the consistency probe only to a disposable `/tmp` directory,
used `--trust=0`, and removed the directory on exit. No `lake update`, `lake build`, dependency
clone/fetch, checkout repair, network access, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0161` | 0 | rank 660; planned; L0/rework-required; theorem incomplete |
| structured query of the proof and obligation-tree DAG items | 0 | prerequisite `[_]`, attempts 1; proof `[ ]`, attempts 0; exact assigned metadata confirmed |
| `python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py` | 0 | 21 obligations and 44 typed edges passed; denominator `48173f90...dadbe`; root open M3 and both exact packages M4 |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-0161/check_statement.py` | 0 | exact target expression `c140d1d1...f82`; all four structural mutations killed |
| isolated pinned direct Lean recipe below | 0 | `Statement.lean`, `Counterexample.lean`, and the positive-candidate-implies-`False` probe elaborated under `--trust=0` |
| source/output/type/axiom gates in the recipe | 0 | exact negation and probe types passed; all three declarations use exactly `propext`, `Classical.choice`, and `Quot.sound`; prohibited matches were zero |
| read-only dependency identity checks in the recipe | 0 | mathlib stayed at revision `8a178386...a95`, tree `bdc39a3...1e5c2b`, with unchanged status and `.lake` symlink target |
| `python3 -m json.tool` plus semantic blocker assertions | 0 | structured report is valid and records blocked/open/no-selftest state |
| wrapped new-file and scoped `git diff --check` commands | 0 | both fresh artifacts and the complete scoped worker delta have no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test deliberately absent because the positive proof phase is blocked |

The exact core replay was:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-0161
lean_root=$root/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0161-aef94f39-slot40.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
before_link=$(readlink "$lean_root/.lake")
before_mathlib=$(git -C "$lean_root/.lake/packages/mathlib" rev-parse HEAD)
before_tree=$(git -C "$lean_root/.lake/packages/mathlib" rev-parse HEAD^{tree})
before_status=$(git -C "$lean_root/.lake/packages/mathlib" status --porcelain=v1)
lean_bin=$(cd "$lean_root" && env -u LEAN_PATH timeout 300 lake env which lean)
lean_path=$(cd "$lean_root" && env -u LEAN_PATH timeout 300 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -R "$target" -o "$tmp/Statement.olean" \
  "$target/Statement.lean" >"$tmp/statement.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -R "$target" -o "$tmp/Counterexample.olean" \
  "$target/Counterexample.lean" >"$tmp/counterexample.out" 2>&1
printf '%s\n' 'import Counterexample' \
  'namespace Stage1Instances.THM_M_0161' \
  'theorem positive_candidate_implies_false' \
  '    (h : FundamentalTheoremOfSpaceCurvesTarget) : False :=' \
  '  frozen_target_false h' \
  '#check positive_candidate_implies_false' \
  '#print axioms positive_candidate_implies_false' \
  'end Stage1Instances.THM_M_0161' >"$tmp/ConsistencyProbe.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -R "$tmp" -o "$tmp/ConsistencyProbe.olean" \
  "$tmp/ConsistencyProbe.lean" >"$tmp/probe.out" 2>&1
```

Before elaboration, the executed recipe required the tracked statement and counterexample hashes to
equal `82f74a6f...a43060` and `2f306383...710f9`. An executed Python gate stripped comments, rejected
`sorry`, `admit`, `sorryAx`, bodyless declarations, unsafe/oracle constructs, Lean errors, sorry
warnings, unsolved goals, and metavariables; required the exact negation and probe types; and
required the exact allowed axiom set for all three checked declarations. It printed:

```text
SOURCE_OUTPUT_TYPE_AXIOM_GATES=PASS
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
Stage1Instances.THM_M_0161.positive_candidate_implies_false
  (h : FundamentalTheoremOfSpaceCurvesTarget) : False
'Stage1Instances.THM_M_0161.curvature_is_contDiffOn_one' depends on axioms:
  [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_0161.frozen_target_false' depends on axioms:
  [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_0161.positive_candidate_implies_false' depends on axioms:
  [propext, Classical.choice, Quot.sound]
Lean (version 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740)
LEAN_BINARY_SHA256=3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf
MATHLIB_REVISION=8a178386ffc0f5fef0b77738bb5449d50efeea95
MATHLIB_TREE=bdc39a3123201dae413a9d9be56ec242c19e5c2b
PINNED_TRUST_ZERO_REFUTATION_AND_CONSISTENCY_PROBE=PASS
```

The only diagnostic was a non-failing `unnecessarySeqFocus` linter warning at
`Counterexample.lean:70`; there was no Lean error or incomplete-proof diagnostic. The untracked
`Formalizations/Lean/.lake` symlink was present before report changes, so this is narrow,
warm-cache, nonrelease blocker evidence.

## Retry condition

Do not retry the unchanged positive root. Authorized source and statement review must first repair
the target with source-faithful `C^1` or stronger coefficient regularity, or replace the positive
item with an accepted counterexample or barrier target. The integration lane must then accept a new
canonical expression fingerprint and an append-only obligation-registry and typed-graph version
delta, followed by fresh statement mutation testing, source review, anchor audit, obligation-tree
construction, and proof execution in dependency order.

Because the assigned positive proof phase is not genuinely self-tested, the required completion
manifest `.stage1-worker-selftest.json` is deliberately absent. This packet is actionable blocker
evidence only and does not satisfy `S56-M-0161-PROOF`.
