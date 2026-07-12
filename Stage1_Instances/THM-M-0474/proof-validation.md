# THM-M-0474 proof-phase validation

Item: `S56-M-0474-PROOF`. Base revision:
`8c50139eafcb1c2e29e7ca69379648590820bf53`.

## Implemented closure

`Proof.lean` imports the exact frozen statement and composition interface through a temporary,
isolated module path. It gives exact typed bodies for the ten semantic children from natural-to-
integer normalization through the finite-group cardinal theorem, then checks four explicit parent
composition certificates. `fermatLittleTheorem_via_frozen_composition` consumes that complete route
through `ObligationTree.root_of_exactNatAnchor`; `fermatLittleTheorem` and `exactNatAnchor` separately
check the exact pinned upstream declaration at the canonical interfaces. These are multiple
exact-type and composition checks over one upstream proof chain, not duplicate mathematical credit.

The terminal body is in `Mathlib/FieldTheory/Finite/Basic.lean` lines 663-666 at mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; the source SHA-256 is
`808bb4eddb8a4b48785e4430f944fe0827c96842dffa0c08cd21b5659bd85d44`. The visible proof chain
reaches `pow_card_eq_one` in `Mathlib/GroupTheory/OrderOfElement.lean`, SHA-256
`42bef2580b87cd0fa6367cd2d57d30fb25fce373576a856cc84d27dad23fae23`. The proof phase therefore
proposes `M0-W` for the exact root and its 13-node frozen proof subgraph, pending master acceptance.

## Commands and exact results

Validation ran on 2026-07-13 (Asia/Shanghai), reusing the pre-existing canonical pinned `.lake`
symlink. No update, build, dependency clone, fetch, network action, or `.lake` mutation was run.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0474
  exit 0: rank 938, planned, L0/rework_required, theorem_complete=false

cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0474/check_proof.sh
  exit 0: isolated Statement.olean and ObligationTree.olean elaborated; all ten semantic child
  bodies, four parent composition certificates, the direct root, exact child, and composed root
  were sorry-free. Every axiom report was a subset of
  [propext, Classical.choice, Quot.sound]; normalized stdout SHA-256
  e93a6aac362ef0bef36790185b57e998f5ae687f1be4cb5aa39c9b8a194648ea

python3 Stage1_Instances/THM-M-0474/check_proof.py
  exit 0: exact source fragments, frozen hashes, pin and source hashes, receipt boundary,
  owned inventory, and no-completion claim passed

python3 Stage1_Instances/THM-M-0474/check_obligation_tree.py
  exit 0: 21 frozen obligations, 43 typed edges, denominator and visible terminal chain passed;
  the freeze artifact truthfully retains its pre-proof H1/M3/R4 status overlay

python3 Stage1_Instances/THM-M-0474/check_anchor_audit.py
  exit 0: exact pinned candidate, source chain, hashes, and provisional downstream handoff passed

cd Formalizations/Lean &&
  python3 ../../Stage1_Instances/THM-M-0474/check_statement.py
  exit 0: exact expression, checked transport, minimal imports, and four mutations passed

python3 Stage1_Instances/THM-M-0474/check_intake.py
  exit 0: planned dossier, empty accepted state, and six open local tasks remain fail-closed

rg -n -i --glob '*.lean' '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|unsafe)[[:space:]]|implemented_by|native_decide' \
  Stage1_Instances/THM-M-0474/Proof.lean
  exit 1 with empty output: expected pass, no prohibited construct found

git diff --check -- Stage1_Instances/THM-M-0474 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

This is narrow proof-phase evidence only. The planned instance and frozen architecture retain empty
accepted proof state until the integration lane acts. H0, R0, full transitive provenance and TCB
acceptance, hermetic replay, deterministic evidence, independent verification, validation, release,
audit completion, and theorem completion remain unclaimed.
