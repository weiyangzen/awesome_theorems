# Statement receipt

Item: `S56-M-0554-STATEMENT`

Base revision: `9e3fd02a2a952da7031bb1dd61387443dd4c1cc7`

The canonical proposition elaborates with the two pinned mathlib imports in
`Statement.lean`. It quantifies all universes and mathematical inputs, makes
the finite-CW skeletal data explicit, and requires the cohomological AHSS
`E₂` page, differential bidegree `(r, 1-r)`, naturality, and convergence to the
skeletal associated graded of generalized cohomology. It defines a target and
does not provide an inhabitant.

| Command (from `Formalizations/Lean`) | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0554/Statement.lean` | 0 | Printed `Statement.{uC,vC,w} : Prop`, `StatementShape`, and the explicit binder expansion. |
| `lake env lean ../../Stage1_Instances/THM-M-0554/minimality/WithoutSpectralSequence.lean` | 1 expected | Unknown `CategoryTheory.E₂CohomologicalSpectralSequence`; the spectral-sequence import is required. |
| `lake env lean ../../Stage1_Instances/THM-M-0554/minimality/WithoutTopCat.lean` | 1 expected | Unknown `TopCat`; the topology import is required. |
| `python3 -m json.tool Stage1_Instances/THM-M-0554/statement.json` (repository root) | 0 | Structured statement record parses. |
| `rg -n 'sorry\|axiom' Stage1_Instances/THM-M-0554 --glob '*.lean'` (repository root) | 1 | No forbidden declaration or placeholder occurs. |
| `git diff --check -- Stage1_Instances/THM-M-0554 .stage1-worker-selftest.json` (repository root) | 0 | No whitespace errors. |

Source SHA-256:
`8bd29893b87ad6991854c311ef1e80cab11f1fc0d6b63ab82e3bfeb1c5f89970`.
Captured elaborator-output SHA-256:
`f1690fd11232bafbe452f7a63a140204ae23ca3a0f90e0126f4b22dacfd54d30`.

This is provisional worker evidence pending master acceptance. It is not proof
closure, anchor audit, obligation-tree completion, or theorem completion.
