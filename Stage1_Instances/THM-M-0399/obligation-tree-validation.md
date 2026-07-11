# THM-M-0399 obligation-tree validation

Item: `S56-M-0399-OBLIGATION_TREE`. Base revision:
`5b92800f89b8900950954fb12b77c0c56fbce942`.

The structural checker recomputes the canonical-ID denominator hash, verifies exact registry/node
coverage, required node fields and leaf budgets, reciprocal typed proof edges, proof reachability
and acyclicity, recipe references, and the explicit open-root boundary.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0399` | exit 0; rank 12, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0399/check_obligation_tree.py` | exit 0; 11 obligations, 11 nodes, and 7 graph families passed |
| `python3 -m json.tool` on all four new JSON artifacts | exit 0 for each |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0399/RothStatement.lean` | exit 1; `unknown module prefix 'Mathlib'`; the reused cache has no `Mathlib.olean` |
| `git diff --check -- Stage1_Instances/THM-M-0399 .stage1-worker-selftest.json` | exit 0; no output |

The Lean failure is a known pinned-cache limitation, not repaired by a prohibited build/update or
dependency mutation. This phase changes no Lean source and relies on the predecessor's frozen exact
expression fingerprint. It supplies no proof, composition certificate, axiom report, or accepted
receipt. Root debt remains `[H1, M4, R4]`; theorem completion remains false.
