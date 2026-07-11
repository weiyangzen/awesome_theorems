# Statement validation record

Item: `S56-M-0082-STATEMENT`  
Base revision: `2cbc2e53e5feb845c1045f812f0814ffa1711d5a`

## Frozen target

`Stage1Instances.THM_M_0082.GeneralRightAdjointTarget` is the intake-selected general
right-adjoint theorem. It quantifies independently over the object and morphism universes of
`C` and `D`; requires `HasLimits D`, `PreservesLimitsOfSize.{vD, vD} G`, and
`SolutionSetCondition.{vD} G`; and concludes `G.IsRightAdjoint`. Its sole direct import is
`Mathlib.CategoryTheory.Adjunction.AdjointFunctorTheorems`.

The explicit-value hypothesis form preserves every premise in the serialized proposition.
`generalRightAdjointTarget_iff_typeclassTarget` kernel-checks its equivalence with the instance-form
interface used by mathlib, without using the adjoint functor theorem itself.

## Commands and results

All commands ran inside this worker clone. Lean commands ran from `Formalizations/Lean` with the
existing pinned toolchain and canonical `.lake` artifacts.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0082/Statement.lean` | 0 | exact target, checked instance-form iff, and four structural mutations elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0082/check_statement.py` | 0 | expression SHA-256 `7650acd20b1eb8822d24997cddb64fd35dd1a316cee5976171588cf4bc5c541f`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0082/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `27d313...ff72`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |

## Mutation and boundary policy

The validator compares explicit elaborated expressions and rejects removal of completeness,
removal of the solution-set condition, relocation of the functor binder with conjunction of its
premises, and addition of `Nonempty D`. The last mutation exercises the boundary policy: the target
does not silently exclude empty categories. No local-smallness, well-poweredness, coseparating set,
or equal object-universe assumption is added. The precise solution-set indexing universe is `vD`.

This is statement-only evidence pending master acceptance. It does not prove the adjoint functor
theorem or advance anchor-audit, obligation-tree, proof, validation, or release nodes.
