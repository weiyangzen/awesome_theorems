# Statement validation record

Item: `S56-M-0651-STATEMENT`  
Base revision: `bdd92f30d924027320c18f282eed9ed56478eba5`

## Frozen target

`Stage1Instances.THM_M_0651.OmittingTypesTarget` elaborates the simultaneous countable omitting
types claim selected at intake. Symbol types and the family are countable; each family member has
its own finite arity. `IsPartialType`, `Isolates`, `IsNonprincipal`, and `Omits` are explicit local
definitions over pinned mathlib semantics. The only direct import is
`Mathlib.ModelTheory.Satisfiability`. The checked transport
`omits_iff_no_realizing_tuple` verifies that universal tuple-wise omission equals absence of a
realizing tuple.

## Commands and results

Lean commands ran from `Formalizations/Lean` using the existing pinned `.lake` environment.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0651/Statement.lean` | 0 | definitions, omission transport, canonical target, and mutation probes elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-0651/check_statement.py` | 0 | expression SHA-256 `789c281a89ba5947476cb2189ae3e216de0eeaa0b5d016549489d8c1553d8c43`; both mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0651/Statement.lean lean-toolchain lake-manifest.json` | 0 | `39b095...8ea`, `651c8a...1d2`, and `321626...d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets accepted |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0651` | 0 | rank 697, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0651/statement.json` | 0 | JSON valid |
| `git diff --check -- Stage1_Instances/THM-M-0651` | 0 | no whitespace errors |

## Boundary

The mutations show that deleting nonprincipality and weakening universal omission produce distinct
elaborated propositions. Nullary and varying arities are retained, family repetitions are harmless,
and `Countable M` admits finite models. This is statement-only evidence pending master acceptance;
it neither proves the theorem nor advances any dependent node.
