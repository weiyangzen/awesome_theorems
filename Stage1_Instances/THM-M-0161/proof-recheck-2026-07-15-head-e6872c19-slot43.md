# THM-M-0161 current-base proof blocker recheck

Item: `S56-M-0161-PROOF`

Intent: `prove`

Base revision: `e6872c1982a47e873d9578f7e8a8fe0d38ffab60`

Base tree: `dd5d4bee8309bdc401f02862404a59f401c0636b`

Rechecked: `2026-07-15T21:35:45+08:00` (`Asia/Shanghai`)

## Verdict

`blocked`. No positive proof body can truthfully inhabit the exact frozen target. The tracked,
placeholder-free [Counterexample.lean](Counterexample.lean) kernel-checks

```text
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
```

A fresh trust-zero replay also checked the disposable consistency probe

```lean
theorem positive_candidate_implies_false
    (h : FundamentalTheoremOfSpaceCurvesTarget) : False :=
  frozen_target_false h
```

Thus a positive inhabitant of the unchanged proposition would close `False` in the same pinned
environment. This worker added no positive proof body and changed no statement, registry, typed
graph, dependency, scheduler authority, or other target. The assigned proof item remains `[ ]`;
its obligation-tree prerequisite is only provisional `[_]` pending master acceptance.

No proof receipt, provisional completion, accepted state, audit completion, validation completion,
release evidence, theorem completion, or master acceptance is claimed. Because the requested proof
phase is not genuinely complete, `.stage1-worker-selftest.json` is deliberately absent.

## Checked obstruction

The frozen target assumes only `DifferentiableOn` curvature and torsion but requires a `C^3`
realizing curve. `curvature_is_contDiffOn_one` proves that every positive realized curvature is
`C^1`. The checked counterexample uses

```text
kappa161(x) = 2 + x^2 * sin(1/x),    tau(x) = 0,    interval = (-1, 1).
```

`kappa161` is differentiable everywhere and strictly positive on the interval, but its derivative
is discontinuous at zero, so it is not `C^1`. Existence would make it both `C^1` and not `C^1`.
This refutes only the under-regularized frozen Lean proposition, not the classical theorem with
source-faithful coefficient regularity.

The negative declaration is an `M0-L` candidate for the exact negation only. It grants no positive
root proof credit. Rev-5.6 classifies a refuted or ill-posed target as `H5` and blocks ordinary
positive proof execution. This proof worker therefore proposes `H5/M5/R4` for authorized
reconciliation but does not rewrite predecessor statement, source, instance, registry, graph, or
DAG authority. `root_of_existence_and_uniqueness` remains conditional composition: it assumes the
complete existence and uniqueness packages and proves neither one.

The predecessor status surfaces are themselves unreconciled: `instance.json` says `H1/M4/R4`,
while the typed root says `H3/M3/R4`. Neither vector is changed or treated as accepted here.

## Validation

All commands ran in this worker clone. The Lean replay reused the automation-provided pinned Lake
closure. It did not run `lake update`, `lake build`, dependency clone/fetch, checkout repair, or any
other `.lake` mutation. Generated oleans and the consistency probe existed only in a disposable
`/tmp` directory and were removed by a trap. The pre-existing untracked
`Formalizations/Lean/.lake` symlink points to the canonical shared cache, so this is narrow,
warm-cache, nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0161` | 0 | rank 660; planned; L0/rework-required; theorem incomplete |
| assigned proof/prerequisite DAG query | 0 | proof item `[ ]`, attempts 0; obligation-tree prerequisite `[_]`, attempts 1 |
| `python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py` | 0 | 21 obligations and 44 typed edges passed; denominator `48173f90...dadbe`; positive root stays M3 and both exact packages stay M4 |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-0161/check_statement.py` | 0 | exact expression `c140d1d1...f82`; all four structural mutations killed; pinned mathlib revision matched |
| isolated pinned Lake-environment Lean `--trust=0` replay below | 0 | statement, exact refutation, and positive-candidate-implies-`False` probe elaborated |
| replay source/output/type/axiom gates | 0 | zero prohibited matches; exact negation and probe types passed; the three declarations use exactly `propext`, `Classical.choice`, and `Quot.sound` |
| read-only dependency identity/status checks | 0 | mathlib `8a178386...a95`, tree `bdc39a3...1e5c2b`; flt-regular `56161b6...1a27`, tree `32c9eac...c893`; both tracked dependency worktrees clean |
| `python3 -m json.tool` plus semantic assertions for the companion JSON | 0 | fresh packet is valid and records blocked/open/no-selftest state |
| wrapped new-file and scoped `git diff --check` commands | 0 | both fresh reports and the complete scoped worker delta have no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test absent because the positive proof phase is blocked |

The isolated replay was:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-0161
lean_root=$root/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0161-e6872c19-slot43.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_bin=$(cd "$lean_root" && env -u LEAN_PATH timeout 300 lake env which lean)
lean_path=$(cd "$lean_root" && env -u LEAN_PATH timeout 300 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -R "$target" -o "$tmp/Statement.olean" \
  "$target/Statement.lean" >"$tmp/statement.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -R "$target" -o "$tmp/Counterexample.olean" \
  "$target/Counterexample.lean" >"$tmp/counterexample.out" 2>&1
```

Before elaboration, the executed recipe required the statement and counterexample SHA-256 values
to equal `82f74a6f...a43060` and `2f306383...f710f9`. It generated and compiled the consistency probe
above. An executed parser stripped comments and rejected `sorry`, `admit`, `sorryAx`,
`implemented_by`, `native_decide`, bodyless `axiom`/`constant` declarations, unsafe/oracle
constructs, Lean errors, sorry warnings, unsolved goals, and metavariable diagnostics. It also
required the exact refutation/probe types and exact three-axiom output. The replay printed:

```text
SOURCE_OUTPUT_TYPE_AXIOM_GATES=PASS
Lean (version 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740)
LEAN_BINARY_SHA256=3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf
STATEMENT_OLEAN_SHA256=85d9e8d765dfc11a9464016ac7714555ed312173ef123c656518af20d574884e
COUNTEREXAMPLE_OLEAN_SHA256=ed0dbd7d960391498d8c364ac750ca3d3e552e4b4682ac5fff119e2eb2bd61ca
CONSISTENCY_PROBE_OLEAN_SHA256=b21e31ab2cd14b6df9740b7904f65f6a2afab2dd24bd9343d7ce7565db389bb5
MATHLIB_REVISION=8a178386ffc0f5fef0b77738bb5449d50efeea95
MATHLIB_TREE=bdc39a3123201dae413a9d9be56ec242c19e5c2b
FLT_REGULAR_REVISION=56161b6eb5281fbfe9c38f2bcec0f429ebc11a27
FLT_REGULAR_TREE=32c9eace926573a9981787ae97643e520353c893
PINNED_TRUST_ZERO_REFUTATION_AND_CONSISTENCY_PROBE=PASS
```

The only diagnostic was the non-failing `unnecessarySeqFocus` linter warning at
`Counterexample.lean:70`; there was no incomplete-proof diagnostic.

## Retry condition

Do not retry the unchanged positive root. Authorized source and statement review must first repair
the target with source-faithful `C^1` or stronger coefficient regularity, or replace the positive
item with an accepted counterexample/barrier target. A repaired target then requires a new
canonical expression fingerprint, an append-only obligation-registry and typed-graph version
delta, and fresh statement mutation testing, source review, anchor audit, obligation-tree
construction, and proof execution in dependency order.

This current-base report is actionable negative evidence only. It does not satisfy
`S56-M-0161-PROOF` and supports no theorem-completion claim.
