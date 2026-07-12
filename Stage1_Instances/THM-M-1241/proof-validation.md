# THM-M-1241 proof-phase blocker

Item: `S56-M-1241-PROOF`  
Date: `2026-07-12`  
Base revision: `c198d8dd5bd64a4d487ed7455874705d67fd300f`

## Verdict

`blocked`: no eligible proof body for the exact Gagliardo-Nirenberg target
exists in the repository or pinned mathlib closure. The kernel-checked theorem
`root_of_finite_and_endpoint_packages` is conditional: it consumes
`FiniteExponentPackage` and `InfiniteEndpointPackage`, but proves neither.

The first failed proof gate is `M1241-T-FINITE`. Pinned mathlib's
Gagliardo-Nirenberg-Sobolev declarations cover strict first-order special
cases. They do not cover arbitrary `m` and `j`, the two-factor interpolation
power, all finite exponents, or the integer-critical branch. The independent
cut obligation `M1241-T-ENDPOINT` is also open: no available body handles the
infinite exponents and Nirenberg's exact zero-order exceptional hypothesis.

The frozen root cut therefore remains `M1241-T-FINITE` plus
`M1241-T-ENDPOINT`. No package premise, axiom, placeholder, weaker Sobolev
special case, or altered endpoint theorem was added. Machine status remains
`M3`, and theorem completion remains false.

Because the assigned proof phase is not self-tested complete, this attempt
deliberately does not create `.stage1-worker-selftest.json`.

## Narrow validation evidence

All commands ran from the worker clone. The existing `Formalizations/Lean/.lake`
symlink reuses the canonical pinned artifacts and was not modified. No Lake
update/build, dependency clone/fetch, or network action was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard passes: 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1241` | 0 | Rank 422, planned, hard-mathlib-anchor lane, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1241/check_obligation_tree.py` | 0 | 15 obligations and 31 typed edges pass; denominator `d2173828bd656ec7e4545903a4fdd42a5c759de71b31e46f8c4c189be864991e`; root remains M3 and both package obligations remain open. |
| `export ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0; BASE_LEAN_PATH="$(cd Formalizations/Lean && lake env printenv LEAN_PATH)"; cd Stage1_Instances/THM-M-1241; LEAN_PATH="$BASE_LEAN_PATH" lake env lean -o Statement.olean Statement.lean; LEAN_PATH=".:$BASE_LEAN_PATH" lake env lean -o ObligationTree.olean ObligationTree.lean; rm -f Statement.olean ObligationTree.olean` | 0 | The exact statement and conditional composition elaborate. `#print axioms` reports `[propext, Classical.choice, Quot.sound]`; no generated olean remains. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `rg -l -i -e 'GagliardoNirenbergTarget' -e 'Gagliardo.Nirenberg' -e 'Nirenberg.*interpolation' -e 'interpolation.*Nirenberg' --glob '*.lean' Stage1_Instances Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | Matches reduce to this dossier, historical adjacent Stage1 analysis surfaces, a neighboring Sobolev proof, and mathlib's strict special-case Sobolev module; none supplies either exact package. |
| `rg -n '^\s*(sorry\|admit\|axiom)(\s\|$)' Stage1_Instances/THM-M-1241 --glob '*.lean'` | 1 | No prohibited Lean declaration token occurs; exit 1 is the expected no-match result. |

The retry condition is a placeholder-free implementation or immutable compatible
import for both frozen analytic packages, including the finite critical and
infinite zero-order branches, with exact-type transports and provenance.
