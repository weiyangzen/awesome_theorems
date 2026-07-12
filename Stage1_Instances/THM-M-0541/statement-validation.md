# Statement validation record

Item: `S56-M-0541-STATEMENT`  
Base revision: `bb527c7e738104d62e96393dc253bdc9025dbecc`

## Frozen target

`Stage1Instances.THM_M_0541.StatementShape` fixes Hatcher's standard ordered, unreduced integral
boundary-square construction as the exact root. An `n`-simplex is a face with `n + 1` vertices;
the vertex order gives its orientation; face `i` deletes the `i`th increasing vertex. Chains are
finite-support integer combinations. The conclusion asks for the alternating boundary maps and
their consecutive-composition law.

This resolves the intake's coefficient, orientation, reducedness, empty-simplex, degree, and
finiteness choices. It does not credit functoriality: maps that identify or reorder vertices need a
separate signed chain-map construction, which must not be assumed at the statement gate.

## Commands and results

Commands ran inside the worker clone. Lean commands used the existing pinned Lake environment and
did not modify `.lake`.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0541/Statement.lean` | 0 | target, face construction, alternating-boundary predicate, square-zero conclusion, and four mutations elaborated; explicit target expression printed |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0541/check_statement.py` | 0 | expression SHA-256 `95f44477f9ef04eb9bc5f787b4697e678fb760dd5024ec29d1233450577b44e1`; all four structural mutations distinguished |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-0541/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `5e799f...c32d`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0541` | 0 | rank 598, planned, L0/rework-required, theorem incomplete |

The mutation validator distinguishes removal of the vertex-order typeclass, coefficient
specialization from integers to rationals, existential relocation of the vertex binder, and a
changed degree-zero boundary convention. These are expression-identity tests, not proofs that a
mutation is mathematically false.

This is statement-only evidence pending master acceptance. Source pinpointing, anchor provenance,
the obligation registry, proof, trust closure, hermetic replay, independent review, and theorem
completion remain open.
