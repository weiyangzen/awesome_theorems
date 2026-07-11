# THM-M-0416 obligation-tree validation

Item: `S56-M-0416-OBLIGATION_TREE`. Base revision:
`58aff8cd11df342da3e7b717b7ceb39afc50d609`.

Validation ran from the worker clone on 2026-07-12. It reused the existing
pinned Lake artifacts and Lean 4.29.0 toolchain; no update, build, fetch, or
clone command was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0416/build_obligation_artifacts.py` | 0 | denominator `03ee8a6d4f406ce15db68263014f0d37b61a09082b6e94b337709d2226fd0bcb` |
| `python3 Stage1_Instances/THM-M-0416/check_obligation_tree.py` | 0 | 9 obligations and 19 typed edges passed; root remains open at M3 |
| `cd Stage1_Instances/THM-M-0416 && ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_PATH="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" lake env lean -o Statement.olean Statement.lean && LEAN_PATH=.:$LEAN_PATH lake env lean ObligationTree.lean` | 0 | conditional composition elaborated; axioms were exactly `propext`, `Classical.choice`, `Quot.sound`; temporary `Statement.olean` removed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0416` | 0 | rank 71, planned, legacy artifacts unaccepted, theorem incomplete |

An initial scoped Lean command from `Formalizations/Lean` exited nonzero because
Lean 4.29 rejects an input outside the project root and consequently could not
find `Statement`. The successful command above ran inside the owned directory,
using the same Lake-derived pinned `LEAN_PATH`; no dependency state changed.

The checks validate frozen input hashes and denominators, node ledgers and
budgets, graph adjacency, reciprocal proof edges, validation-recipe coverage,
source hygiene, and exact child-to-parent composition. Candidate proof bodies,
typeclass-provider provenance, source acceptance, proof integration, trust,
hermetic replay, and master acceptance remain later gates. No theorem
completion is claimed.
