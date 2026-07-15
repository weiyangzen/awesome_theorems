# THM-M-1286 proof-phase refutation recheck

Item: `S56-M-1286-PROOF`

Recorded: `2026-07-16T04:49:26+08:00` (`Asia/Shanghai`)

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

## Verdict

`blocked`. A positive proof body cannot truthfully be implemented for the exact frozen target.
`Counterexample.lean` contains the placeholder-free theorem
`Stage1Instances.THM_M_1286.Counterexample.not_polyaSzegoTarget` with exact type
`Not PolyaSzegoTarget`. A fresh trust-zero Lean replay at this base elaborated it and reported only
`propext`, `Classical.choice`, and `Quot.sound`.

The refutation specializes to `n = 1`, `p = 1`, zero gradient, and `-log x` on `(0, 1)`. In the
frozen statement, `ContDiff Real top` is analytic, so every compactly supported test function is
zero and `HasWeakGradient` is vacuous. Every pointwise real-valued symmetric-decreasing witness is
bounded above by its value at zero, while the log spike has a positive-measure superlevel above
every positive threshold. Equimeasurability gives a contradiction at threshold `uStar 0 + 1`.

This refutes the frozen Lean encoding, not the classical Polya-Szego theorem. The encoding also
uses the ordinary Pi supremum norm on `Fin n -> Real` rather than Euclidean `l2` geometry. The
conditional declaration `ObligationTree.exactTarget_of_packages` earns no positive proof credit:
its premises cannot both be implemented consistently because their composition would contradict
the checked negation.

## Dependency context

The required schema-1.1 ledger records graph digest
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca` and target context
`a27c6d321f87a3db44085d50ec9ba7b3c5a343bf53227b1c17c7922356046a57`. The target has no hard
parents, transitive hard ancestors, hard edges, or direct reuse hints. Its sole context item is weak
shared-module group `SHARED-MODULE-279c180c9a767195`.

Member `THM-M-1245` and its use of
`Mathlib.Analysis.FunctionalSpaces.SobolevInequality` were inspected. Its Gagliardo-Nirenberg-
Sobolev norm estimate neither constructs a Schwarz rearrangement nor establishes equimeasurability,
a rearranged weak gradient, or the required energy comparison. The ledger therefore records this
weak co-mention as `not_applicable`; it transfers no proof credit.

## Narrow validation

Pinned Lake artifacts were reused read-only. No `lake update`, `lake build`, dependency clone/fetch,
network action, or `.lake` mutation was performed. Generated oleans were isolated below `/tmp` and
removed.

| Command | Exit | Result |
|---|---:|---|
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | Rank 457, lifecycle `planned`, theorem incomplete. |
| `python3 Docs/tools/check_stage1_standard.py` | 1 | Pre-existing repository failure: the checked-in v2 theorem DAG differs from fresh deterministic generation. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | Same checked-in-versus-generated DAG mismatch; no authoritative DAG was modified. |
| `python3 Stage1_Instances/THM-M-1286/check_obligation_tree.py` | 0 | 18 obligations and 23 typed edges passed; positive root remains open M4. |
| Target-scoped `validate_dependency_reuse_ledger` invocation | 0 | Exact graph/base/context binding passed; zero hard-parent inspections and one weak-group decision. |
| Isolated `lake env lean --trust=0 -t0` replay below | 0 | Statement and counterexample elaborated; olean sizes 67,392 and 218,384 bytes; exact negation and three allowed axioms printed. |
| Prohibited-construct `rg` scan over owned Lean sources | 1, expected | No `sorry`, `admit`, `axiom`, `sorryAx`, unsafe injection, or native decision occurs. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0-src. |
| Pinned package revisions and `diff --quiet` | 0 | Mathlib and flt-regular revisions match the manifest and both worktrees are unmodified. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test is absent because the proof phase is blocked. |

Exact Lean replay from the repository root:

```bash
set -euo pipefail
ROOT=$PWD
TMP=$(mktemp -d /tmp/thm-m-1286-slot35-6bf9ee93.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/Stage1_Instances/THM-M-1286"
cd "$ROOT/Formalizations/Lean"
LEAN_NUM_THREADS=1 timeout --foreground --kill-after=10s 600s \
  lake env lean --trust=0 -t0 -R ../.. \
  -o "$TMP/Stage1_Instances/THM-M-1286/Statement.olean" \
  ../../Stage1_Instances/THM-M-1286/Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP" timeout --foreground --kill-after=10s 600s \
  lake env lean --trust=0 -t0 -R ../.. \
  -o "$TMP/Counterexample.olean" \
  ../../Stage1_Instances/THM-M-1286/Counterexample.lean
```

The repository-wide standard and theorem-DAG validators fail because the checked-in authoritative
v2 DAG differs from a fresh deterministic generation. This is a pre-existing authority-level
inconsistency outside the assigned owned path; this worker did not modify or regenerate either DAG.
The scheduler-supplied graph digest still exactly matches the checked-in DAG, and the target-scoped
ledger validator passes against that supplied context.

## Retry condition

Reopen `S56-M-1286-STATEMENT`: use measure-compatible Euclidean `l2` geometry, replace analytic
order `top` with the intended smooth order, and choose a rearrangement representation that admits
essentially unbounded finite-`p` inputs. Publish a new statement fingerprint and refreeze every
dependent artifact before resuming positive proof execution. Alternatively, explicitly redirect
execution to the checked counterexample target.

## Status boundary

The proof item remains `[ ]`. This packet is current-base, target-scoped, nonrelease refutation
evidence. It does not satisfy `S56-M-1286-PROOF` and claims no proof completion, audit completion,
theorem completion, validation, release, receipt acceptance, or master acceptance. No
`.stage1-worker-selftest.json` is written because the assigned positive proof phase is not complete.
