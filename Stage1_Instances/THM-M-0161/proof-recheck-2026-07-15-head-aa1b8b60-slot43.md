# THM-M-0161 current-base proof blocker recheck

Item: `S56-M-0161-PROOF`

Intent: `prove`

Base revision: `aa1b8b60828300c7a1f4abb7719e7e5f03558f8a`

Base tree: `0ef03022f6fa297c9acf726f2537a413997e233d`

Rechecked: `2026-07-15T22:06:13+08:00` (`Asia/Shanghai`)

## Verdict

`blocked`. No positive proof body can truthfully inhabit the exact frozen target. The tracked,
placeholder-free `Counterexample.lean` kernel-checks

```text
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
```

Therefore a positive inhabitant of the unchanged proposition would derive `False` in the same
pinned environment. This worker added no positive proof body and changed no statement, registry,
typed graph, dependency, scheduler authority, or other target. The assigned proof item remains
`[ ]`; its obligation-tree prerequisite is only provisional `[_]` pending master acceptance.

No proof receipt, provisional completion, accepted state, audit completion, validation completion,
release evidence, theorem completion, or master acceptance is claimed. Because the assigned
positive proof phase is not genuinely complete, `.stage1-worker-selftest.json` is deliberately
absent.

## Checked obstruction

The frozen target assumes only `DifferentiableOn` curvature and torsion but requires a `C^3`
realizing curve. `curvature_is_contDiffOn_one` proves that every positive realized curvature is
`C^1`. The checked counterexample uses

```text
kappa161(x) = 2 + x^2 * sin(1/x),    tau(x) = 0,    interval = (-1, 1).
```

`kappa161` is differentiable everywhere and strictly positive on the interval, but its derivative
is discontinuous at zero. Existence would make it both `C^1` and not `C^1`. This refutes only the
under-regularized frozen Lean proposition, not the classical theorem with source-faithful
coefficient regularity.

The negative declaration is an `M0-L` candidate for the exact negation only and grants no positive
root proof credit. Rev-5.6 classifies a refuted target as `H5` and blocks ordinary positive proof
execution. This packet proposes `H5/M5/R4` for authorized reconciliation but does not rewrite the
predecessor statement, source record, instance, registry, typed graph, or task-state authority.
`root_of_existence_and_uniqueness` remains conditional composition: it assumes both complete
packages and proves neither one.

## Validation

All commands ran in this worker clone. Lean reused the automation-provided pinned Lake closure. No
`lake update`, `lake build`, dependency clone/fetch, checkout repair, or other `.lake` mutation was
run. Generated oleans existed only in a disposable `/tmp` directory and were removed by a trap.
The pre-existing untracked `Formalizations/Lean/.lake` symlink points to the canonical shared cache,
so this is narrow warm-cache nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0161` | 0 | rank 660; lifecycle planned; theorem incomplete |
| assigned proof/prerequisite DAG query | 0 | proof item `[ ]`, attempts 0; obligation-tree prerequisite `[_]`, attempts 1 |
| `python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py` | 0 | 21 obligations and 44 typed edges passed; denominator `48173f90...dadbe`; positive root remains M3 and both exact packages remain M4 |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-0161/check_statement.py` | 0 | exact expression `c140d1d1...f82`; all four structural mutations killed; pinned mathlib revision matched |
| isolated pinned Lake-environment Lean `--trust=0` replay | 0 | `Statement.lean` and `Counterexample.lean` elaborated; exact negation and axioms printed |
| read-only dependency identity/status checks | 0 | mathlib revision `8a178386...a95`, tree `bdc39a3...1e5c2b`, with clean tracked status |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test absent because the positive proof phase is blocked |

The isolated replay was:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-0161
lean_root=$root/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0161-aa1b8b60-slot43.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_bin=$(cd "$lean_root" && env -u LEAN_PATH timeout 300 lake env which lean)
lean_path=$(cd "$lean_root" && env -u LEAN_PATH timeout 300 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -R "$target" -o "$tmp/Statement.olean" \
  "$target/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -R "$target" -o "$tmp/Counterexample.olean" \
  "$target/Counterexample.lean"
```

It printed the exact negation and reported exactly `propext`, `Classical.choice`, and `Quot.sound`
for both `curvature_is_contDiffOn_one` and `frozen_target_false`. Source hashes were
`82f74a6f...a43060` and `2f306383...f710f9`; disposable olean hashes were
`85d9e8d7...4884e` and `ed0dbd7d...61ca`. The Lean binary was version 4.29.0, commit
`98dc76e3...b16740`, SHA-256 `3e0d0d3d...28bbf`. The only diagnostic was the non-failing
`unnecessarySeqFocus` linter warning at `Counterexample.lean:70`; there was no Lean error, sorry
warning, or unsolved goal.

## Retry condition

Do not retry the unchanged positive root. Authorized source and statement review must first repair
the target with source-faithful `C^1` or stronger coefficient regularity, or replace the positive
item with an accepted counterexample/barrier target. A repaired target then requires a new canonical
expression fingerprint, an append-only obligation-registry and typed-graph version delta, and fresh
statement mutation testing, source review, anchor audit, obligation-tree construction, and proof
execution in dependency order.

This current-base report is actionable negative evidence only. It does not satisfy
`S56-M-0161-PROOF` and supports no theorem-completion claim.
