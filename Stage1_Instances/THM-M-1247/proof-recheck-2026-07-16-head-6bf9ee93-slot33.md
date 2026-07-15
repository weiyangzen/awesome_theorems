# THM-M-1247 proof-phase blocker after v2 dependency audit

Item: `S56-M-1247-PROOF`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

Worker: Stage1 rev-5.6 slot33

Verdict: **blocked**

## Result

The assigned proof phase is not complete, and no worker self-test manifest was
written. The new schema-1.1 dependency ledger successfully audits the empty
hard-parent and reuse-hint closure. Its sole weak shared-module group was
inspected through the other member, `THM-M-1465`, and rejected as not
applicable: the shared `Mathlib.Analysis.InnerProductSpace.Laplacian` import is
only a module co-mention and supplies no Rellich statement, terminal body,
checked transport, or proof evidence.

The existing `Proof.lean` remains a real, placeholder-free kernel proof of the
exact frozen Lean proposition, but that proposition is not the canonical
classical Rellich claim. The isolated trust-zero replay exposes both defects:

1. `ContDiff Real top` infers `top : WithTop ENat`, mathlib's analytic order
   `omega`, rather than the smooth order `infinity`.
2. `Fin n -> Real` has the finite Pi supremum norm, whereas the classical
   Euclidean target requires `EuclideanSpace Real (Fin n) = PiLp 2` and its L2
   norm.

Support avoidance makes an admitted analytic function vanish near the origin;
analytic uniqueness then makes it identically zero. The current proof therefore
closes only this malformed encoding by reducing both integrals to zero. It earns
no proof credit for the smooth Euclidean Rellich inequality, and the worker is
not authorized to rewrite the already provisional statement or its downstream
registry during the proof phase.

## Dependency ledger

- Path: `Stage1_Instances/THM-M-1247/dependency-reuse-ledger.json`
- Schema: `stage1-dependency-reuse-ledger/1.1`
- Graph SHA-256: `73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`
- Context SHA-256: `4b0604303ce139c1d808f60c9ca31e07b11d23e340f73d9cb54da1684fd6ae08`
- Hard parents, transitive ancestors, hard edges, and reuse hints: none
- Shared group: `SHARED-MODULE-512cf2e7078a412f`
- Decision: `not_applicable`, provider inspected as `THM-M-1465`
- Reused declarations: none
- Unresolved compatibility obligations: none

## Lean replay

All outputs were written to a disposable `/tmp` directory and removed. The
existing pinned cache was read only; no update, build, clone, fetch, or cache
repair was run.

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-1247
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-1247-proof-head-6bf9ee93-slot33.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$target/Statement.lean" "$target/Proof.lean" "$target/ObligationTree.lean" "$tmp/"
cd "$lean_root"
lean_path=$(timeout --foreground --kill-after=5s 120s env LEAN_NUM_THREADS=1 lake env printenv LEAN_PATH)
timeout --foreground --kill-after=10s 600s env LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  lake env lean --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
timeout --foreground --kill-after=10s 600s env LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  lake env lean --trust=0 -t0 --root="$tmp" -o "$tmp/Proof.olean" "$tmp/Proof.lean"
timeout --foreground --kill-after=10s 600s env LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  lake env lean --trust=0 -t0 --root="$tmp" -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
```

All three elaborations exited `0`. `#print axioms` reported exactly
`propext`, `Classical.choice`, and `Quot.sound` for the proof declarations and
the conditional composition declaration. The replay also printed the expanded
target with `Top.top (WithTop ENat)` and the finite Pi normed-group instance.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 1 | Blocked: checked-in v2 theorem DAG differs from fresh deterministic generation |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | Same deterministic-generation mismatch; authority regeneration is master-owned |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1247` | 0 | Rank 427, planned, legacy evidence unaccepted, theorem incomplete |
| inline `validate_dependency_reuse_ledger(...)` with the supplied graph/base bindings | 0 | Schema 1.1 ledger passed; zero inspections, one decision, zero unresolved obligations |
| `python3 Stage1_Instances/THM-M-1247/check_obligation_tree.py` | 0 | 13 obligations, 34 edges; root open at M3 and six analytic obligations M4 |
| `python3 Stage1_Instances/THM-M-1247/check_anchor_audit.py` | 0 | Three pinned candidate families; zero exact candidates; terminal open |
| isolated `lake env lean --trust=0` replay above | 0 | Statement, proof, and conditional composition elaborated |
| `rg -n -i 'Rellich\|Hardy[-_ ]?Rellich\|HardyRellich' Formalizations/Lean/.lake/packages --glob '*.lean'` | 1 | Expected no match in readable pinned Lean sources |
| prohibited-token scan over `Statement.lean`, `Proof.lean`, and `ObligationTree.lean` | 1 | Expected no lexical match |

The interrupted legacy `check_statement.py` run is not credited: under current
shared host load it did not terminate promptly, was stopped, and its temporary
file was removed. The isolated exact-target replay above is the narrower real
kernel check used here.

## First failed gate and retry

The first theorem-specific failure is the exact backend-to-canonical statement
mapping gate: analytic regularity and the Pi supremum norm do not encode the
smooth Euclidean L2 theorem. Under an authorized statement assignment, replace
the domain with `EuclideanSpace Real (Fin n)`, use smooth infinity explicitly,
rerun the statement and mutation gates, and publish a versioned registry/graph
delta with downstream invalidations before proof execution resumes.

There is also an authority preflight mismatch: fresh deterministic v2 graph
generation disagrees with the checked-in graph, even though its bytes match the
scheduler-supplied digest used by this ledger. The master must reconcile that
artifact. Finally, 43 integrated blocked recheck pairs coexist with proof
attempts `0` and no children; the master must reconcile execution ticks and
apply the five-tick split rule if applicable.

This is dependency-audit and blocker evidence only. It does not advance the
proof item, close the canonical root, validate or release the target, complete
its audit, or claim theorem completion.
