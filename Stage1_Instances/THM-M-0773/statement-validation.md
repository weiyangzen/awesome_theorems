# Statement validation record

Item: `S56-M-0773-STATEMENT`  
Base revision: `c72bad9e8827ffb1ba1a585dbe346c88393b4a3f`

## Frozen target

`Stage1Instances.THM_M_0773.TeichmullerTukeyTarget` is the intake-selected nonempty-family
formulation. Its binders are `alpha : Type u` and `F : Set (Set alpha)`; finite character and
nonemptiness are explicit hypotheses; the conclusion is existence of a member maximal relative to
`F` under subset inclusion. The only direct import is `Mathlib.Order.TeichmullerTukey`, the pinned
module defining the exact finite-character predicate.

`pointed_implies_unpointed` checks one direction from the stronger pointed encoding without invoking
the candidate mathlib theorem. The reverse direction is deliberately not credited in this phase.

## Commands and results

All commands ran in this worker clone with the existing pinned `.lake` artifacts read-only. No
update, build, clone, fetch, or dependency mutation command was run.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0773/Statement.lean` | 0 | canonical target, checked transport, four mutations, and two boundary theorems elaborated; explicit target printed |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0773/check_statement.py` | 0 | expression SHA-256 `68aa26cd5bfd9033298490cc521d4c26b0fd5bd62f6431259532573d1a699f14`; all four mutations distinguished |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Stage1_Instances/THM-M-0773/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `49682139...49264`, `651c8acc...b1d2`, and `321626c8...b2d81`, matching `statement.json` |

## Mutation and status boundary

The validator hashes the fully explicit elaborated expression and rejects identity with mutations
that remove nonemptiness, change the family domain, change binder scope, or exclude the empty
carrier. `emptyFamily_boundary` proves why the omitted premise is invalid; `emptyCarrier_boundary`
confirms that an empty carrier remains included.

This is statement-only, nonrelease evidence pending master acceptance. It does not inspect or
credit `Order.IsOfFiniteCharacter.exists_maximal`, prove the canonical target, close the anchor
audit, or establish audit/theorem completion.
