# THM-M-1272 proof-phase validation

Item: `S56-M-1272-PROOF`  
Date: `2026-07-14` (`Asia/Shanghai`)  
Base revision: `4990a9d6fa09beb7747e6822c6543c6123ca7504`

## Implemented proof bodies

`Proof.lean` closes the compactness branch of the frozen architecture. It
proves the bounded-value bridge (`M1272-L-LEVEL-BOUNDED`), global
Palais-Smale subsequence extraction (`M1272-L-PS-SUBSEQUENCE`), value and
Frechet-derivative limit passage (`M1272-L-LIMIT-PASSAGE`), and the exact
`FountainLimitPackage` parent (`M1272-T-CRITICAL-LEVELS`).

The last declaration composes that package with the previously checked frozen
composer, but it keeps `FountainMinimaxPackage` as an explicit premise. Thus it
is not an unconditional proof of `FountainTheoremTarget`. The symmetric
minimax, linking, and odd-deformation branch ending at
`M1272-T-LOWER-BOUND` remains open, so the accepted root remains `M3` and
theorem completion is false.

## Commands and exact results

The worker reused the existing pinned Lake artifacts. No update, build, clone,
fetch, or `.lake` mutation was performed.

The existing `check_statement.py` was started during preflight, but concurrent
worker load made its repeated full elaborations outlive the command-capture
window, so no result from that run is credited here. The proof checker itself
independently elaborated the unchanged canonical `Statement.lean` at trust
zero before elaborating the proof.

```text
bash Stage1_Instances/THM-M-1272/check_proof.sh
  exit 0
  Statement.lean, ObligationTree.lean, and Proof.lean elaborated in an
  isolated temporary directory with `--trust=0 -t0`.
  fountainLimitPackage_proof : FountainLimitPackage
  fountainTheoremTarget_of_minimax :
    FountainMinimaxPackage -> FountainTheoremTarget
  All five printed proof declarations depend exactly on:
    [propext, Classical.choice, Quot.sound]
  check_proof.py reported:
    PASS THM-M-1272 proof phase: compactness package closed;
    symmetric minimax package remains explicit and open

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1272
  exit 0: rank 165, planned, L0/rework_required, theorem_complete=false

python3 Stage1_Instances/THM-M-1272/check_anchor_audit.py
  exit 0: bounded immutable candidate audit passed; no eligible terminal
  Fountain proof exists in the pinned closure

python3 Stage1_Instances/THM-M-1272/check_obligation_tree.py
  exit 0: 16 obligations and 29 typed edges passed; frozen root remains M3

python3 Stage1_Instances/THM-M-1272/check_lean_composition.py
  exit 0: conditional exact-root composition elaborated; axiom report was
  [propext, Classical.choice, Quot.sound]

python3 -m json.tool Stage1_Instances/THM-M-1272/proof-receipt.json
  exit 0: valid JSON

rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|unsafe|opaque)\b' \
  Stage1_Instances/THM-M-1272/Proof.lean
  exit 1 with empty output: expected clean no-match result

git diff --check -- Stage1_Instances/THM-M-1272 \
  .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

Pinned environment: Lean `4.29.0` at
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The pre-existing untracked
canonical `.lake` symlink makes this warm evidence nonrelease evidence.

## Reopen condition

Resume by implementing the exact `FountainMinimaxPackage`, including its
frozen normalization, minimax-class construction, linking, and odd-deformation
children, or by locating an immutable exact Lean 4 body whose full provenance
and trust closure can be pinned and checked. A conditional wrapper, a weaker
mountain-pass theorem, or an assumed deformation interface does not close the
remaining branch.
