# THM-M-0161 current-base proof blocker recheck

Item: `S56-M-0161-PROOF`

Intent: `prove`

Base revision: `88a5a5c6fe6bac0d813a74ca20fa553eaf2a6d68`

Base tree: `a0a75048a918a3bf566c3dbcf6b4352c3b2ee8e4`

Rechecked: `2026-07-15T20:00:00+08:00`

## Verdict

`blocked`. The exact frozen positive target is false, so no placeholder-free positive proof body
can truthfully inhabit it. The tracked `Counterexample.lean` kernel-checks

```text
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
```

The proof item remains `[ ]`, with `root_closed=false` and `theorem_complete=false`. Its
obligation-tree prerequisite is only provisional `[_]`, pending master acceptance. No positive
proof body, receipt, provisional completion, audit completion, validation, release, theorem
completion, or master acceptance is claimed. Because the assigned phase is not genuinely
complete, `.stage1-worker-selftest.json` is deliberately absent.

## Checked obstruction

The target assumes only `DifferentiableOn Real kappa (Set.Ioo a b)` while demanding a `C^3`
realizing curve. `curvature_is_contDiffOn_one` proves that the positive curvature of such a curve
must be `C^1` on the interval. The exact counterexample takes

```text
kappa161(x) = 2 + x^2 * sin(1/x),    tau(x) = 0,    interval = (-1, 1).
```

This `kappa161` is differentiable everywhere and strictly positive on `(-1, 1)`, but its
derivative is zero at zero and `-1` along `1 / ((n + 1) * 2*pi)`, which tends to zero. Hence it is
not `C^1`, contradicting the regularity forced by the existence conclusion. This refutes only the
under-regularized frozen Lean proposition, not the classical theorem with source-faithful
coefficient regularity.

The negative declaration is a repo-local, kernel-checked body for the exact negation and an
`M0-L` candidate pending a node-specific receipt and master acceptance. It supplies no
positive-root credit. Rev-5.6 section 3 directs a refuted target to `H5` handling, so this report
proposes `H5/M5/R4` for authorized reconciliation. It does not rewrite the predecessor statement,
registry, graph, instance, or scheduler authority. The existing
`root_of_existence_and_uniqueness` is conditional composition: it assumes both open packages and
proves neither.

## Validation

All commands ran in this worker clone. The narrow Lean replay reused the automation-provided
pinned Lake closure without running `lake update`, `lake build`, dependency clone/fetch, checkout
repair, or any `.lake` mutation. Oleans were generated only under a disposable `/tmp` directory
and removed on exit. The untracked `Formalizations/Lean/.lake` symlink points to the shared
canonical cache, so this is warm-cache nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0161` | 0 | rank 660; lifecycle planned; theorem incomplete |
| assigned proof/prerequisite DAG query | 0 | proof `[ ]`, attempts 0; prerequisite `[_]`, attempts 1 |
| `python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py` | 0 | 21 obligations and 44 typed edges passed; denominator `48173f90...dadbe`; positive root remains open |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-0161/check_statement.py` | 0 | canonical expression `c140d1d1...f82`; all four structural mutations killed |
| isolated `lake env which lean` plus direct Lean `--trust=0` replay below | 0 | statement and exact refutation elaborated; exact negation and source/output gates passed |
| refutation axiom and prohibited-construct scan | 0 | both key declarations use exactly `propext`, `Classical.choice`, and `Quot.sound`; zero prohibited matches |
| read-only pinned dependency identity checks | 0 | mathlib remained at `8a178386...a95`, its tracked status did not change, and the `.lake` symlink target was unchanged |
| `python3 -m json.tool` plus semantic blocker assertions | 0 | fresh JSON is valid and records blocked/open/no-selftest state |
| wrapped new-file and scoped `git diff --check` commands | 0 | both fresh artifacts and the complete scoped delta have no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test deliberately absent because the positive proof phase is blocked |

The exact core replay, run from the repository root, was:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-0161
lean_root=$root/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0161-slot58.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
before_link=$(readlink "$lean_root/.lake")
before_mathlib=$(git -C "$lean_root/.lake/packages/mathlib" rev-parse HEAD)
before_status=$(git -C "$lean_root/.lake/packages/mathlib" status --porcelain=v1)
lean_bin=$(cd "$lean_root" && env -u LEAN_PATH timeout 300 lake env which lean)
lean_path=$(cd "$lean_root" && env -u LEAN_PATH timeout 300 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -R "$target" -o "$tmp/Statement.olean" \
  "$target/Statement.lean" >"$tmp/statement.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -R "$target" -o "$tmp/Counterexample.olean" \
  "$target/Counterexample.lean" >"$tmp/counterexample.out" 2>&1
```

Before elaboration, the executed recipe required the tracked statement and counterexample hashes
to equal `82f74a6f...a43060` and `2f306383...710f9`. An executed Python gate stripped comments,
rejected `sorry`, `admit`, `sorryAx`, bodyless declarations, unsafe/oracle constructs, Lean errors,
and sorry warnings; required the exact negation type; and required the exact allowed axiom set for
`curvature_is_contDiffOn_one` and `frozen_target_false`. The successful replay printed:

```text
SOURCE_AND_OUTPUT_SCAN=PASS
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
'Stage1Instances.THM_M_0161.curvature_is_contDiffOn_one' depends on axioms:
  [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_0161.frozen_target_false' depends on axioms:
  [propext, Classical.choice, Quot.sound]
Lean (version 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740)
MATHLIB_REVISION=8a178386ffc0f5fef0b77738bb5449d50efeea95
PINNED_TRUST_ZERO_REFUTATION=PASS
```

The only diagnostic was a non-failing `unnecessarySeqFocus` linter warning at
`Counterexample.lean:70`; there was no Lean error or incomplete proof diagnostic.

## Retry condition

Do not retry the unchanged positive root. Authorized source and statement review must first repair
the target with source-faithful `C^1` or stronger coefficient regularity, or replace the positive
item with an accepted counterexample or barrier target. A repaired target then needs a new
canonical expression fingerprint, an append-only obligation-registry and typed-graph version
delta, and fresh statement mutation testing, source review, anchor audit, obligation-tree
construction, and proof execution in dependency order.

This report is current-base negative evidence only. It does not satisfy `S56-M-0161-PROOF` and
supports no theorem-completion claim.
