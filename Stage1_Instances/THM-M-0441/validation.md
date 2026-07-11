# Statement validation record

Item: `S56-M-0441-STATEMENT`
Base revision: `5437588d542b33fbc37b068e31cde251774e2f4d`.

The selected claim is Pila-Wilkie Theorem 1.8 (first version), interpreted with Definitions 1.3
and 1.5 from the inspected MIMS copy (SHA-256 `810719...d2f`). The direct Lean target is
`Stage1Instances.THM_M_0441.PilaWilkie`; the legacy arbitrary-predicate boundary is uncredited.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0441/Statement.lean` from `Formalizations/Lean` | 0 | exact target, definitional expansion, three mutations, and two boundary checks elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-0441/check_statement.py` from `Formalizations/Lean` | 0 | expression SHA-256 `103f282f...a475`; all three mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Statement.lean lean-toolchain lake-manifest.json` | 0 | `a0a7c7...563b`, `651c8a...1d2`, `321626...d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard and 1546-target coverage OK |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0441` | 0 | rank 87, planned, L0/rework-required, theorem incomplete |

Known failures: source proof/errata audit and independent review remain open. No proof inhabitant,
anchor audit, obligation tree, transitive trust closure, hermetic replay, or release evidence exists.
Those gates do not invalidate the self-tested statement node, but they prevent theorem completion.
