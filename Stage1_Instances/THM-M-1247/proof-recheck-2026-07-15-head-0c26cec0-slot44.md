# THM-M-1247 proof recheck at `0c26cec0` (slot44)

Item: `S56-M-1247-PROOF`

Base revision: `0c26cec0be4f7fada10abc2c6ed0b213656d1708`

Base tree: `52417604a8aaccfac38ae970ef94337e6f38d033`

Run date: `2026-07-15T20:14:31+08:00`

## Verdict

`blocked`. The assigned proof phase is not complete, so no
`.stage1-worker-selftest.json` was emitted.

The existing placeholder-free `Proof.lean` re-elaborates at trust level zero
and proves the exact frozen Lean proposition. It cannot receive proof credit
for the canonical human Rellich inequality because that proposition has two
exact-statement mapping defects:

1. `ContDiff Real top` infers `top : WithTop ENat`, mathlib's analytic order
   `omega`; smooth infinity is `((top : ENat) : WithTop ENat)`.
2. `Euclidean n := Fin n -> Real` carries the finite Pi supremum norm;
   `EuclideanSpace Real (Fin n)` is `PiLp 2` with the Euclidean `L2` norm.

Support avoidance makes every function admitted by the malformed analytic
statement vanish near the origin. Analytic uniqueness makes it identically
zero, after which the encoded inequality simplifies to `0 <= 0`. This is a
real kernel proof of the frozen backend encoding, not a proof of the
source-mapped smooth Euclidean Rellich theorem. Rev-5.6 section 5 forbids
canonical proof credit until the exact backend-to-canonical mapping passes.

The first failed gate remains that statement mapping, proposed at
`M1247-S-DOMAIN`. Accordingly the truthful proposed root vector is
`[H1, M5, R3]`; the older frozen records still display `[H1, M3, R3]` and are
not authority this worker may rewrite. The prerequisite
`S56-M-1247-OBLIGATION_TREE` remains only provisional `[_]`, not
master-accepted. Its registry is structurally valid but
semantically stale, and `root_of_coreRellichEstimate` still consumes an open
`CoreRellichEstimate` premise. The direct analytic-vacuity proof bypasses, and
therefore does not close, the frozen weighted IBP/Hardy composition route.

The current pinned dependency cache is usable; the earlier partial
`flt-regular` cache issue is no longer a blocker. Pinned mathlib also contains
general multidimensional integration-by-parts substrate, including
`integral_mul_fderiv_eq_neg_fderiv_mul_of_integrable`, but no exact
Rellich/Hardy-Rellich theorem was found. That substrate does not repair the
statement or supply the missing sharp weighted estimate.

The dossier's human-source crosswalk is also not acceptance-ready: its DOI
`10.1007/PL00004387` resolves to an unrelated paper; the Davies-Hinz Rellich
paper at volume 227, pages 511-523 uses DOI `10.1007/PL00004389`. This leaves
the existing `H1` boundary intact and must be corrected by an authorized
source/statement task, not by this proof worker.

## Current-Base Delta

The immediately preceding integrated target packet was based at
`b366bdd9f72217b5465ccd19133760b911ed0b58`. Between that base and this base,
only that packet pair changed under `Stage1_Instances/THM-M-1247`. Target
semantics, the target-manifest entry, execution skill, and THM-M-1247 task
states are unchanged. Authority-file changes promote unrelated items only.

There are now 36 integrated `proof-recheck-*.json` reports, while the
master-owned proof item still records attempts zero and no children. Packet
count is not itself the authoritative execution-tick count, but rev-5.6
section 10.2 requires a split after five unresolved ticks. The master must
reconcile these packets instead of dispatching the same unsplit proof item
again.

## Validation

Credited Lean checks read the automation-provided pinned Lake artifacts. No
update, build, clone, fetch, network request, or `.lake` mutation was
performed. Fresh Lean outputs existed only in a temporary directory under
`/tmp` and were removed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `15` assurance groups and `1546` uniform-L0 targets; execution skill present. |
| `python3 scripts/stage1_target.py check` | 0 | `1546` unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-1247` | 0 | Rank 427; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1247/check_statement.py` | interrupted | This redundant helper was stopped after its first mutation subprocess exceeded the narrow proof replay; it left no target artifact and receives no credit. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1247/check_anchor_audit.py` | 0 | Three pinned mathlib candidate families checked; exact external candidates `0`; terminal result open. |
| `timeout --foreground --kill-after=5s 300s python3 Stage1_Instances/THM-M-1247/check_obligation_tree.py` | 0 | 13 obligations, 34 typed edges, denominator `9df3b5e9...79a590`; root open at `M3`, with six analytic obligations at `M4`. |
| Isolated pinned `lake env lean --trust=0` recipe below | 0 | Fresh `Statement.olean`, `Proof.olean`, and `ObligationTree.olean` elaborated; exact frozen type checked; axioms exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| `cd Formalizations/Lean/.lake/packages/mathlib && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3...`. |
| `rg -n -i 'Rellich\|Hardy[-_ ]?Rellich\|HardyRellich' Formalizations/Lean/.lake/packages --glob '*.lean'` | 1, expected | No matching theorem in readable pinned package Lean sources. |
| `rg -n '\\b(sorry\|admit\|sorryAx)\\b\|^[[:space:]]*(axiom\|unsafe\|opaque)[[:space:]]' Stage1_Instances/THM-M-1247/{Statement,Proof,ObligationTree}.lean` | 1, expected | No prohibited lexical match; this is defense in depth, not a transitive provenance audit. |
| `git diff --name-status b366bdd9f72217b5465ccd19133760b911ed0b58..HEAD -- Stage1_Instances/THM-M-1247 Docs/Stage1_Targets_rev-5.6.json Docs/Stage1_Blueprint_rev-5.6.md Docs/Stage1_Execution_DAG_rev-5.6.json skills/execute-stage1-rev56/SKILL.md` | 0 | Only the preceding target packet and unrelated authority-state changes; no semantic target or governing-skill change. |
| `jq -c '.items[] \| select(.id \| startswith("S56-M-1247-")) \| {id,phase,state,attempts,depends_on,children}' Docs/Stage1_Execution_DAG_rev-5.6.json` | 0 | Intake through obligation tree remain `[_]`; proof remains `[ ]`, attempts zero, children empty; validation/release remain `[ ]`. |
| `git ls-tree -r --name-only HEAD Stage1_Instances/THM-M-1247 \| rg 'proof-recheck-.*\\.json$' \| wc -l` | 0 | `36`; master reconciliation must determine how many are unresolved execution ticks. |

The narrow kernel replay was:

```bash
set -euo pipefail
ROOT="$PWD"
TARGET="$ROOT/Stage1_Instances/THM-M-1247"
LEAN_ROOT="$ROOT/Formalizations/Lean"
MATHLIB="$LEAN_ROOT/.lake/packages/mathlib"
TMP=$(mktemp -d /tmp/thm-m-1247-proof-head-0c26cec0-slot44.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp "$TARGET"/{Statement,Proof,ObligationTree}.lean "$TMP"/
BASE_LEAN_PATH="$(find -L "$LEAN_ROOT/.lake/packages" -type d \
  -path '*/.lake/build/lib/lean' -print | LC_ALL=C sort | paste -sd:):\
$(readlink -f "$LEAN_ROOT/.lake")/build/lib/lean:\
$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
cd "$MATHLIB"
LEAN_NUM_THREADS=1 LEAN_PATH="$BASE_LEAN_PATH" \
  timeout --foreground --kill-after=5s 300s \
  lake env lean --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_LEAN_PATH" \
  timeout --foreground --kill-after=5s 300s \
  lake env lean --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Proof.olean" "$TMP/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE_LEAN_PATH" \
  timeout --foreground --kill-after=5s 300s \
  lake env lean --trust=0 -t0 --root="$TMP" \
  -o "$TMP/ObligationTree.olean" "$TMP/ObligationTree.lean"
```

The proof-specific output was:

```text
Stage1Instances.THM_M_1247.rellichInequalityTarget : RellichInequalityTarget
'Stage1Instances.THM_M_1247.frozen_top_is_analytic_order' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.analytic_avoidance_eq_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.rellichInequalityTarget' depends on axioms: [propext, Classical.choice, Quot.sound]
'Stage1Instances.THM_M_1247.root_of_coreRellichEstimate' depends on axioms: [propext, Classical.choice, Quot.sound]
STATEMENT_EXIT=0
PROOF_EXIT=0
OBLIGATION_TREE_EXIT=0
```

## Retry Condition

Do not dispatch `S56-M-1247-PROOF` unchanged again. Under an authorized
statement-phase assignment, replace the domain with
`EuclideanSpace Real (Fin n)` and the regularity order with
`((top : ENat) : WithTop ENat)`, rerun exact-expression and mutation gates,
and publish a versioned registry/typed-graph delta with downstream
invalidations. This repair also needs the Euclidean-space measure imports and
`EuclideanSpace.single` coordinate directions; it is not a textual alias
swap. Then implement the weighted integration-by-parts, sharp Hardy,
normalization, core-estimate, and transport obligations as dependency-legal
children if the master confirms the five-tick threshold.

## Status Boundary

This is current-base blocker and scheduler-escalation evidence under the owned
target path. It does not satisfy `S56-M-1247-PROOF`. The item remains `[ ]`;
there is no worker self-test, accepted receipt, canonical root closure, audit
completion, validation, release, or theorem-completion claim.
