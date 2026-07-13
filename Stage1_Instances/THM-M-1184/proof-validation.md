# THM-M-1184 proof-phase validation

Item: `S56-M-1184-PROOF`. Base revision:
`c45f3c7090cb4adf616d45e5414985f956e807b2`.

## Implemented bodies

`Proof.lean` supplies a real product probability coupling, both marginal
integral transports, fixed-plan weak duality, and the complete uniform
`WeakDualityPackage`. This provisionally closes the frozen machine obligations
`M1184-C-PRODUCT`, `M1184-C-CONSTANT`, `M1184-W-INTEGRATE`,
`M1184-W-ORDER`, and `M1184-T-WEAK`. Its final theorem composes that local weak branch with an
explicit `ReverseDualityPackage` premise.

The reverse branch (`M1184-S-SEPARATION`, `M1184-C-POTENTIALS`,
`M1184-L-GAP`, `M1184-W-REVERSE`, and `M1184-T-STRONG`) remains open
formalization debt. Accordingly the canonical root remains open at `M2`; the
conditional `kantorovichDuality_of_reverse` theorem is not counted as a proof
of strong duality or of the root.

## Commands and results

Validation ran in this worker clone on 2026-07-14 (Asia/Shanghai). It reused
the existing canonical pinned Lake artifacts. No Lake update/build, dependency
clone/fetch, or `.lake` mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0
  check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy
  slots, 1546 uniform-L0 Lean 4 targets, execution skill present)

python3 scripts/stage1_target.py check
  exit 0
  stage1_target: ok (1546 unique targets, ranks 1..1546, all
  L0/rework_required)

python3 scripts/stage1_target.py show THM-M-1184
  exit 0
  rank 169; lane hard_mathlib_anchor_and_wrapper; lifecycle planned;
  theorem_complete false

cd Formalizations/Lean
LEAN_PATH_BASE="$(lake env printenv LEAN_PATH)"
lake env lean -R ../../Stage1_Instances/THM-M-1184 \
  -o /tmp/thm-m-1184-proof-test/Statement.olean \
  ../../Stage1_Instances/THM-M-1184/Statement.lean
LEAN_PATH="/tmp/thm-m-1184-proof-test:$LEAN_PATH_BASE" lake env lean \
  -R ../../Stage1_Instances/THM-M-1184 \
  -o /tmp/thm-m-1184-proof-test/ObligationTree.olean \
  ../../Stage1_Instances/THM-M-1184/ObligationTree.lean
LEAN_PATH="/tmp/thm-m-1184-proof-test:$LEAN_PATH_BASE" lake env lean \
  -R ../../Stage1_Instances/THM-M-1184 \
  ../../Stage1_Instances/THM-M-1184/Proof.lean
  exit 0
  All eight proof declarations report exactly:
    [propext, Classical.choice, Quot.sound]
  The only diagnostics are three unused-section-variable linter warnings on
  the two marginal integral lemmas and the constant-pair lemma.

python3 Stage1_Instances/THM-M-1184/check_proof.py
  exit 0
  PASS THM-M-1184 proof phase: product coupling and weak-duality package
  closed; reverse-duality package and root remain open

rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|unsafe|opaque|extern)\b|implemented_by|native_decide' \
  Stage1_Instances/THM-M-1184/Proof.lean
  exit 1 with empty output: pass; no prohibited proof construct

git diff --check -- Stage1_Instances/THM-M-1184 .stage1-worker-selftest.json
  exit 0; no output
```

## Boundary

This is a provisional worker proof receipt for a genuine proper branch. It is
not master acceptance, validation/release evidence, H0, R0, M0 root closure,
AUDIT-Z, THEOREM-Z, or theorem completion. The pre-existing untracked
`Formalizations/Lean/.lake` link was reused read-only and makes this warm-cache,
nonrelease evidence.
