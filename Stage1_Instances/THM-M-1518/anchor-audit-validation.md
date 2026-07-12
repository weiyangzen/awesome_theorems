# Anchor audit validation

Item: `S56-M-1518-ANCHOR_AUDIT`  
Base revision: `2b5a356f0d547597e745bab548db0caac12e6c96`

## Result

Pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` has checked prerequisite APIs
for the fundamental theorem of calculus, integration by parts, local extrema, and
test-function integral determination. It has no terminal Euler-Lagrange or stationary-action
declaration matching the frozen target.

Physlib at immutable revision `cd22b0c28882412447d12d5cfde677c4ad999994` has the strongest
external candidates: `euler_lagrange_varGradient` and two fundamental-theorem-of-variational-
calculus lemmas. They are anchor-only, not exact closure. Physlib uses Lean 4.29.1 and mathlib
`5e932f...`, while this repository uses Lean 4.29.0 and mathlib `8a1783...`; a semantic API
transport is also absent. The harmonic oscillator result is only a special case. SciLean's found
material is a documentation demo, not a credible terminal proof.

The exact root therefore remains `formalization_debt`. No `repo_local_integration_debt` is hidden
inside a completion claim because this audit explicitly leaves the theorem open.

## Commands and results

All local commands ran in this worker clone. No Lake dependency state was mutated.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1518` | 0 | rank 187, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact pinned revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'Euler[-_ ]?Lagrange\|stationary action\|least action\|calculus of variations\|first variation\|fundamental lemma' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | only unrelated textual “fundamental lemma” hits; no terminal candidate |
| `lake env lean ../../Stage1_Instances/THM-M-1518/AnchorAudit.lean` from `Formalizations/Lean` | 0 | all eight nearby mathlib declarations kernel-elaborated |
| immutable `curl` reads of the three Physlib modules, `lean-toolchain`, and `lake-manifest.json` | 0 | exact source hashes and dependency pins recorded in `anchor-audit.json`; no clone/fetch performed |
| `python3 -m json.tool Stage1_Instances/THM-M-1518/anchor-audit.json` | 0 | receipt is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1518` | 0 | no whitespace errors |

This is self-tested worker evidence pending master acceptance. It does not accept the statement
dependency, prove the canonical theorem, or satisfy later obligation, proof, validation, or release
nodes.
