# THM-M-0161 current-base proof blocker recheck

Item: `S56-M-0161-PROOF`

Intent: `prove`

Base revision: `a8046f38588db115e52af68ccc9f31b855cbf61f`

Base tree: `f746ea13f155c2032d23a9a3c798bcc4096ef166`

Rechecked: `2026-07-15T22:38:31+08:00` (`Asia/Shanghai`)

## Verdict

`blocked`. No positive proof body can truthfully inhabit the exact frozen target. The tracked,
placeholder-free `Counterexample.lean` kernel-checks

```text
Stage1Instances.THM_M_0161.frozen_target_false :
  Not FundamentalTheoremOfSpaceCurvesTarget
```

A fresh trust-zero replay also checked the disposable consequence

```lean
theorem positive_candidate_implies_false
    (h : FundamentalTheoremOfSpaceCurvesTarget) : False :=
  frozen_target_false h
```

Thus a positive inhabitant of the unchanged proposition would close `False` in the same pinned
environment. This worker added no positive proof body and changed no statement, registry, typed
graph, dependency, scheduler authority, or other target. The proof item remains `[ ]`; its
obligation-tree prerequisite is only provisional `[_]` pending master acceptance.

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
is discontinuous at zero. Existence would therefore make it both `C^1` and not `C^1`. This refutes
only the under-regularized frozen Lean proposition, not the classical theorem with source-faithful
coefficient regularity.

The negative declaration is an `M0-L` body for the exact negation only; it grants no positive-root
proof credit. Rev-5.6 classifies a refuted target as `H5` and blocks ordinary positive proof
execution. This proof worker proposes `H5/M5/R4` for authorized reconciliation but does not rewrite
predecessor statement, source, instance, registry, graph, or DAG authority.
`root_of_existence_and_uniqueness` remains conditional composition: it assumes the complete
existence and uniqueness packages and proves neither one. The predecessor instance says
`H1/M4/R4`, while the typed root says `H3/M3/R4`; neither unreconciled vector is changed here.

## Workflow escalation

The target directory already contains 23 earlier `proof-recheck-*.json` reports, while the
authoritative DAG still records `attempts: 0` and no children for this proof item. Rev-5.6 section
10.2 requires splitting an item after five unresolved execution ticks rather than repeatedly
dispatching the same oversized task. The master must reconcile the attempt ledger and redirect
work to an authorized statement-repair or counterexample/barrier node. This proof worker cannot
edit the DAG, generated blueprint, checklist state, or predecessor-owned phases.

## Validation

All commands ran in this worker clone. The Lean replay reused the automation-provided pinned Lake
closure. It did not run `lake update`, `lake build`, dependency clone/fetch, checkout repair, or any
other `.lake` mutation. Generated oleans and the consistency probe existed only under `/tmp` and
were removed by a trap. The pre-existing untracked `Formalizations/Lean/.lake` symlink points to
the canonical shared cache, so this is narrow warm-cache, nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0161` | 0 | rank 660; planned; L0/rework-required; theorem incomplete |
| assigned proof/prerequisite DAG query | 0 | proof item `[ ]`, attempts 0; obligation-tree prerequisite `[_]`, attempts 1 |
| `python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py` | 0 | 21 obligations and 44 typed edges passed; denominator `48173f90...dadbe`; positive root stays M3 and both exact packages stay M4 |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-0161/check_statement.py` | 0 | exact expression `c140d1d1...7f82`; all four structural mutations killed; pinned mathlib revision matched |
| isolated pinned Lake-environment Lean `--trust=0 -t0` replay | 0 | statement, exact refutation, and positive-candidate-implies-`False` probe elaborated |
| replay source/output/type/axiom gates | 0 | zero prohibited matches; exact negation and probe types passed; all three declarations use exactly `propext`, `Classical.choice`, and `Quot.sound` |
| read-only dependency identity/status checks | 0 | mathlib `8a178386...a95`, tree `bdc39a3...1e5c2b`; flt-regular `56161b6...1a27`, tree `32c9eac...c893`; both tracked dependency worktrees clean |
| blocker-count and section-10.2 inspection | 0 | 23 earlier recheck JSON packets coexist with authoritative `attempts: 0`; mandatory five-tick escalation is unreconciled |
| companion JSON parsing and semantic assertions | 0 | blocked/open/refuted/no-completion/no-selftest fields passed |
| wrapped new-file and scoped `git diff --check` commands | 0 | both fresh reports and the complete scoped worker delta have no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test absent because the positive proof phase is blocked |

The successful core replay, run from the repository root, was:

```bash
set -euo pipefail
root=$PWD
target=$root/Stage1_Instances/THM-M-0161
lean_root=$root/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0161-a8046f38-slot12.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_bin=$(cd "$lean_root" && env -u LEAN_PATH timeout 300 lake env which lean)
lean_path=$(cd "$lean_root" && env -u LEAN_PATH timeout 300 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -t0 -R "$target" -o "$tmp/Statement.olean" \
  "$target/Statement.lean" >"$tmp/statement.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -t0 -R "$target" -o "$tmp/Counterexample.olean" \
  "$target/Counterexample.lean" >"$tmp/counterexample.out" 2>&1
```

The executed recipe prechecked source SHA-256 values, generated and compiled the consistency probe
above, stripped comments before scanning the counterexample, and rejected `sorry`, `admit`,
`sorryAx`, `implemented_by`, `native_decide`, bodyless declarations, unsafe/oracle constructs,
Lean errors, sorry warnings, unsolved goals, and metavariable diagnostics. It required the exact
negation/probe types and the exact three-axiom closure. It printed:

```text
SOURCE_OUTPUT_TYPE_AXIOM_GATES=PASS
Lean (version 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740)
LEAN_BINARY_SHA256=3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf
STATEMENT_OLEAN_SHA256=85d9e8d765dfc11a9464016ac7714555ed312173ef123c656518af20d574884e
COUNTEREXAMPLE_OLEAN_SHA256=ed0dbd7d960391498d8c364ac750ca3d3e552e4b4682ac5fff119e2eb2bd61ca
CONSISTENCY_PROBE_OLEAN_SHA256=52f0a56e1f24af0df5e066e967d9612dc74ffbe596a09d1f40a7400f76fca4ec
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
