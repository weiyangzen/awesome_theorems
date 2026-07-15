# THM-M-1277 proof-phase recheck at current base

Item: `S56-M-1277-PROOF`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

## Verdict

`blocked`. The exact frozen Lean proposition cannot have the requested
positive proof body. A fresh trust-level-zero replay checks the tracked,
placeholder-free countertheorem

```text
Stage1Rev56.THMM1277.not_statement :
  Not Stage1Rev56.THMM1277.Statement
```

The first failed gate is exact canonical statement correctness.
`SmoothCompactIn` uses `ContDiff Real top`; at the inferred order, this `top`
is mathlib's analytic order `omega`, not smooth order `infinity`. Analytic
uniqueness makes every globally analytic compactly supported approximant
identically zero. The encoded completion therefore forces every admitted
scalar field to vanish almost everywhere. Every admissible exponential
integral then equals the finite volume of the bounded domain for every
exponent. The supercritical clause on the unit ball, with `C` equal to that
volume, requires the volume to be strictly less than itself.

This refutes the frozen encoding, not the mathematical Moser-Trudinger
theorem. Correcting it inside this proof phase would substitute a new target.
The repair belongs to the statement phase and changes every fingerprint-bound
downstream artifact. No positive proof receipt, root closure, audit
completion, validation, release, or theorem completion is claimed.

## Dependency context

The required schema-1.1 dependency ledger was added and checked against DAG
digest `73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`
and context digest
`a27c6d321f87a3db44085d50ec9ba7b3c5a343bf53227b1c17c7922356046a57`.
There are no hard parents, transitive ancestors, hard edges, or reuse hints.

The sole shared group is a nonblocking co-mention of
`Mathlib.Analysis.FunctionalSpaces.SobolevInequality`. The inspected member
`THM-M-1245` proves a finite-`q` first-order Sobolev norm estimate using
`MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq_inner`. It supplies neither
the critical two-dimensional exponential endpoint at `4 * pi` nor the
supercritical unboundedness branch, and there is no checked transport. The
ledger therefore records `not_applicable`, with no proof credit or reused
declaration.

The phase dependency also fails independently:
`S56-M-1277-OBLIGATION_TREE` is only provisional `[_]`, not master-accepted
`[x]`. Its registry checker passes structurally with 24 obligations and 48
typed edges, but reports the root open at `M3`.

## Validation

All Lean checks reused the existing pinned `.lake` artifacts read-only. No
update, build, dependency clone/fetch, network access, or `.lake` mutation was
performed. The automation-provided untracked `.lake` symlink makes this
nonrelease blocker evidence.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 1 after evidence write | Propagated the v2 DAG inventory mismatch described below; master regeneration is required |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 after evidence write | It passed before edits; afterward the generated inventory sees the newly required proof-recheck JSON, so only master DAG regeneration can restore global freshness |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1277` | 0 | Rank 328, planned, legacy artifacts unaccepted, theorem incomplete |
| Direct `validate_dependency_reuse_ledger` invocation | 0 | Exact graph, context, empty hard closure, and one shared-group decision passed |
| `python3 Stage1_Instances/THM-M-1277/check_obligation_tree.py` | 0 | 24 obligations and 48 typed edges pass structurally; root remains open `M3` |
| Fresh temporary-olean recipe below | 0 | Statement and Proof elaborated; exact `Not Statement` witness checked; all 13 axiom reports contained exactly `propext`, `Classical.choice`, `Quot.sound` |
| Prohibited-token scan over target Lean files | 1, expected | No `sorry`, `admit`, `sorryAx`, declared `axiom`, or `unsafe` declaration |
| Pinned toolchain and mathlib check | 0 | Lean 4.29.0 commit `98dc76e...fab16740`; mathlib commit `8a178386...44a9d50`, tree `bdc39a31...2c19e5c2b`, clean package worktree |
| `git diff --check` | 0 | No whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | No positive proof self-test manifest was written |

The DAG freshness failure is an integration boundary, not a request to change
the graph in this worker. The task explicitly forbids edits to
`Docs/Stage1_Theorem_DAG_v2.json`; the integration lane must regenerate its
inventory after accepting or otherwise handling this target-owned evidence.

The exact fresh elaboration recipe ran from `Formalizations/Lean`:

```bash
set -u
TMP=$(mktemp -d /tmp/thm-m-1277-proof-6bf9ee93-slot28.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
BASE=$(timeout --foreground --kill-after=5s 60 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 300 \
  lake env lean --trust=0 -t0 --root=../.. \
  -o "$TMP/Statement.olean" \
  ../../Stage1_Instances/THM-M-1277/Statement.lean \
  >"$TMP/statement.out" 2>&1
statement_rc=$?
if [ "$statement_rc" -ne 0 ]; then
  exit "$statement_rc"
fi
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE" \
  timeout --foreground --kill-after=5s 300 \
  lake env lean --trust=0 -t0 --root=../.. \
  -o "$TMP/Proof.olean" \
  ../../Stage1_Instances/THM-M-1277/Proof.lean \
  >"$TMP/proof.out" 2>&1
proof_rc=$?
sha256sum "$TMP/Statement.olean" "$TMP/Proof.olean" \
  "$TMP/statement.out" "$TMP/proof.out"
exit "$proof_rc"
```

The replay ran from `2026-07-16T04:46:41+08:00` to
`2026-07-16T04:50:30+08:00` and produced these hashes before deleting the
temporary directory:

| Output | SHA-256 |
|---|---|
| `Statement.olean` | `84f541c01763ee25facdce4cfc28cc3380e52a5f55d9c3c295c0cefe99159e63` |
| `Proof.olean` | `fe8744f2d174c01c443bc4c34ce0f9ed934e5e39b7bba12eed53b718b24c0e91` |
| Statement output | `593f08c48172c08e242b8073f6550e2d3f100806c26d98d9ddb387dc8a1fb3a8` |
| Proof output | `2f47380b9e5a682199aa7e433ad923111d99b9612a1d9bb3a050fa4f8c10d9c8` |

## Handoff

Reopen `S56-M-1277-STATEMENT` and replace the ambiguous analytic order with
the intended smooth order `((top : ENat) : WithTop ENat)`. Reconcile the
nonempty-domain and support conventions, rerun exact-expression identity and
mutation gates, and regenerate the obligation registry, typed graphs, and
validation specifications for the new statement fingerprint before another
proof attempt.

The remaining root cut set is `S56-M-1277-STATEMENT`. Because the assigned
positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent and the item remains
`[ ]`.
