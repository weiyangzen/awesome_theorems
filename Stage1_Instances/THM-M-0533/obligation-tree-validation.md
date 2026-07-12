# Obligation-tree validation record

Item: `S56-M-0533-OBLIGATION_TREE`  
Theorem: `THM-M-0533`  
Validation date: `2026-07-12`  
Base revision: `30d893623b4b974bbae53b781eacf4f8b4391787`

Registry version 1 contains 19 unique obligations and seven separate typed
graphs with 37 edges. The frozen denominator digest is
`238242dfcb6274343a6413ed2628d0944bf0882c280b42608d8e19bad2c88dfc`.
The structural checker verifies hashes, denominators, unique IDs, reciprocal
proof edges, incidence, proof reachability, step budgets, source binding, and
the fail-closed root status.

`ObligationTree.lean` checks only final conditional composition. Construction
and exactness are explicit open premises. `#print axioms` reports `propext`,
`Classical.choice`, and `Quot.sound`; no new axiom is declared.

All commands ran in the worker clone using the existing pinned closure. No
dependency update, build, clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0533/build_obligation_artifacts.py` | 0 | wrote 19 obligations, 37 edges, and the digest above |
| `python3 Stage1_Instances/THM-M-0533/check_obligation_tree.py` | 0 | PASS; root open at M3 |
| `cd Formalizations/Lean && lake env lean -R ../.. ../../Stage1_Instances/THM-M-0533/Statement.lean -o ../../Stage1_Instances/THM-M-0533/Statement.olean` | 0 | exact statement elaborated; three known fixture warnings |
| `cd Formalizations/Lean && LEAN_PATH=../../Stage1_Instances/THM-M-0533 lake env lean -R ../.. ../../Stage1_Instances/THM-M-0533/ObligationTree.lean` | 0 | conditional composition elaborated; expected axioms printed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1,546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546 |
| `python3 scripts/stage1_target.py show THM-M-0533` | 0 | rank 590; planned; theorem incomplete |
| `rg -n '\\bsorry\\b|\\badmit\\b|^[[:space:]]*(axiom|constant)[[:space:]]' Stage1_Instances/THM-M-0533 --glob '*.lean'` | 1 | no forbidden match |
| `git diff --check -- Stage1_Instances/THM-M-0533 .stage1-worker-selftest.json` | 0 | no output |

The validation-only `Statement.olean` was removed after the import check. The
remaining cut includes subdivision, small-chain quasi-isomorphism, chain
exactness, map naturality, and degree zero. This receipt self-tests only the
architecture freeze pending master acceptance; theorem completion is false.
