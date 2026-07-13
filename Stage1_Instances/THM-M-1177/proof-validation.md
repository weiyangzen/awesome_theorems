# THM-M-1177 proof-phase validation

Item: `S56-M-1177-PROOF`. Base revision:
`3bb4cb3ae15dff8b48c93242019edec3bf858e48`.

## Implemented bodies

`Proof.lean` supplies a real proof of the complete frozen
`M1177-B-DEGENERATE` package. It transports the statement's coordinate
positive-definiteness predicate to `Matrix.PosDef`, obtains determinant and
integrand nonnegativity, and proves the set integral nonnegative without
assuming that the frozen contact set is measurable. The latter step uses
boundedness to prove finite volume and
`Measure.restrict_inter_toMeasurable` to replace the arbitrary contact-set
restriction by the restriction to its measurable hull intersected with the
open domain.

The exact right side is therefore nonnegative, so a nonpositive domain
supremum satisfies the frozen ABP bound. The final declaration composes this
local branch with an explicit uniform `PositiveMaximumPackage` premise. That
premise is not an ABP proof and receives no root credit.

`M1177-T-POSITIVE` remains open formalization debt. Its contact construction,
slope-ball and gradient-image geometry, Hessian sign, matrix determinant/trace
estimate, area/integration route, ball-volume normalization, and positive
supremum algebra have no exact local or pinned proof body. Thus the root moves
only to proposed `M2` after master acceptance; it is not kernel-closed, and
theorem completion is false.

## Commands and results

Validation ran in this worker clone on 2026-07-14 (Asia/Shanghai). It reused
the pre-existing canonical pinned Lake artifacts. No Lake update/build,
dependency clone/fetch, or `.lake` mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0
  check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy
  slots, 1546 uniform-L0 Lean 4 targets, execution skill present)

python3 scripts/stage1_target.py check
  exit 0
  stage1_target: ok (1546 unique targets, ranks 1..1546, all
  L0/rework_required)

python3 scripts/stage1_target.py show THM-M-1177
  exit 0
  rank 377; lane hard_mathlib_anchor_and_wrapper; lifecycle planned;
  theorem_complete false

python3 Stage1_Instances/THM-M-1177/check_obligation_tree.py
  exit 0
  PASS THM-M-1177 obligation tree: 21 obligations, 69 typed edges;
  denominator fdee2b8b...ef1; predecessor root open M4

python3 Stage1_Instances/THM-M-1177/check_proof.py
  exit 0
  PASS THM-M-1177 proof phase: degenerate package closed;
  positive-maximum package and root remain open

cd /tmp/thm-m-1177-final
LEAN_NUM_THREADS=1 LEAN_PATH="$PINNED_LEAN_PATH" \
  "$PINNED_LEAN" --trust=0 -t0 -o Statement.olean Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$PWD:$PINNED_LEAN_PATH" \
  "$PINNED_LEAN" --trust=0 -t0 -o ObligationTree.olean ObligationTree.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$PWD:$PINNED_LEAN_PATH" \
  "$PINNED_LEAN" --trust=0 -t0 Proof.lean
  exits 0, 0, 0
  All eight proof declarations report exactly the allowed mathlib foundation
  axioms [propext, Classical.choice, Quot.sound]. No sorryAx occurs.

rg -n '\b(sorry|admit|sorryAx|native_decide|implemented_by)\b|^[[:space:]]*(axiom|unsafe|opaque|extern)[[:space:]]' \
  Stage1_Instances/THM-M-1177/Proof.lean
  exit 1 with empty output: pass; no prohibited proof construct

python3 -m json.tool Stage1_Instances/THM-M-1177/proof-receipt.json >/dev/null
  exit 0

git diff --check -- Stage1_Instances/THM-M-1177 .stage1-worker-selftest.json
  exit 0; no output
```

Pinned environment: Lean `4.29.0` at
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). `Proof.lean` SHA-256 is
`aaf7f1e17f07d4665aba005aea7d4226257c6ba04ede5eeb1be035ea788e10be`.

## Boundary

This is provisional worker proof evidence for one genuine frozen branch. It
is not master acceptance, a premise-free proof of the exact target, H0, R0,
M0 root closure, validation/release evidence, AUDIT-Z, THEOREM-Z, or theorem
completion. After accepting this branch, the exact minimal machine cut is
`M1177-T-POSITIVE`.
