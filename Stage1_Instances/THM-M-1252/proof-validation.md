# Proof-phase validation

Item: `S56-M-1252-PROOF`  
Base revision: `aae45673b30d1b10288a632168bbf9df19b441b9`  
Validation time: `2026-07-12T03:18:34Z`

## Implemented proof

`Proof.lean` specializes the pinned mathlib theorem `Distribution.dsupport_compl_eq` to the exact
finite-dimensional real-distribution target, passes that result through the frozen
`root_of_specializedAnchor` composition certificate, and derives the separately frozen expanded
test-function form. This closes the root proof spine `M1252-L-UPSTREAM -> M1252-N-SPECIALIZE ->
M1252-T-COMPOSE -> M1252-ROOT` and its definition/transport interfaces without adding premises.
The terminal proof body remains in mathlib at commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; the repo-local declarations are exact wrappers, not
duplicate proof-body credit.

## Commands and results

Commands ran in the worker clone. The Lean command ran from `Formalizations/Lean` against the
existing canonical pinned `.lake` symlink. No update, build, fetch, clone, or `.lake` mutation was
performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1252` | 0 | rank 431, planned, theorem_complete false |
| `cd Formalizations/Lean && bash ../../Stage1_Instances/THM-M-1252/check_proof.sh` | 0 | isolated Statement/ObligationTree oleans and Proof elaborated; all four printed declarations report only `propext`, `Classical.choice`, and `Quot.sound` |
| `rg -n '\\b(sorry|admit)\\b\|^[[:space:]]*axiom\\b\|^[[:space:]]*unsafe\\b\|sorryAx' Stage1_Instances/THM-M-1252/Proof.lean Stage1_Instances/THM-M-1252/check_proof.sh` | 1 | empty output: no prohibited placeholder, new axiom, unsafe declaration, or `sorryAx` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git diff --check -- Stage1_Instances/THM-M-1252` | 0 | no whitespace errors |

`Proof.lean` SHA-256 is `af52cccdca4ab123600997ffaa52c5f40ec52d8b9e0fd3af3dfb1eea968e2086`.
The inputs are `Statement.lean` `507071b9...b9da`, `ObligationTree.lean` `8fd51a4f...cae5`, and
`obligation-registry.json` `54b6a263...d114`. The pinned mathlib support source is
`731a4f0d...9052` and its existing olean is `a5a99ac0...a875`.

## Status boundary

This is provisional worker proof-phase evidence for an exact root wrapper and supports an `M0-W`
proposal pending master acceptance. It is not validation- or release-phase evidence. H0, R0,
complete transitive provenance/TCB review, hermetic cold replay, independent verification, master
acceptance, and theorem completion remain open.
