# Statement validation record

Item: `S56-M-0698-STATEMENT`
Base revision: `6d9089613f4343925b2ff1ec1a221f0575a93b5f`

## Frozen target

`Stage1Instances.THM_M_0698.FirstOrderCompactnessTarget` quantifies over arbitrary universe-polymorphic
first-order languages and theories. Its conclusion is exactly `T.IsSatisfiable <->
T.IsFinitelySatisfiable`. The sole direct import is `Mathlib.ModelTheory.Satisfiability`.

`firstOrderCompactnessTarget_iff_pinnedMathlibType` checks identity with the displayed type of
`FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable` at pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The expansion transport checks that finite
satisfiability means every finite `Finset` subtheory contained in `T` is satisfiable. These are
statement witnesses only and do not credit the imported theorem's proof.

## Commands and results

All commands ran inside this worker clone. Lean commands used the existing canonical `.lake`
artifacts read-only; no update, build, fetch, clone, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0698` | 0 | rank 739, planned, L0/rework-required, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0698/Statement.lean)` | 0 | target, pinned-type identity, expanded-finite-subtheory identity, and four mutations elaborated; explicit universe-aware target printed |
| `(cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0698/check_statement.py)` | 0 | expression SHA-256 `3531c40508e8728e24c5d55f887988faa083c8c1e4f9ae73b5dd920bdfb48ec5`; all four attempted mutation equalities rejected |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-0698/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `14d196...681a`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0698 -g '*.lean'` | 1 | expected no-match result; no prohibited placeholder or axiom declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0698/statement.json` | 0 | statement receipt JSON valid |
| explicit `git diff --no-index --check` over changed owned files | 0 | no whitespace errors |

The removed-containment, finite-domain, binder-scope, and empty-subtheory mutations all elaborate as
independent propositions but fail definitional equality against the canonical target. The empty
finite subtheory therefore remains in scope, as do the empty theory and arbitrary symbol families.

This is statement-only evidence pending master acceptance. The source audit, anchor proof-body and
dependency audit, obligation tree, proof, release validation, and theorem completion remain open.
