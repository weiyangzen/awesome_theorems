# Statement freeze

Item: `S56-M-0669-STATEMENT`

The canonical declaration is `Stage1.THM_M_0669.TarskiQuantifierEliminationTarget`. For every
free-variable index type `alpha` and every pure-ring formula with those free variables, it asserts
the existence of a quantifier-free formula with exactly the same free-variable interface that is
semantically equivalent in every model of `realClosedFieldTheory`.

## Encoding decisions

- The language is the pure ring language `(+,-,*,0,1)`. Order is not a primitive. Over real closed
  fields it is definable by squares; proving and source-checking that presentation bridge belongs
  to the later source and obligation phases.
- `realClosedFieldTheory` is the complete pure-ring theory of `Real`. The standard mathematical
  identification of its models with characteristic-zero real closed fields is deliberately an
  explicit downstream bridge, not an assumed Lean typeclass conversion.
- `BoundedFormula alpha 0` permits arbitrary indexed free variables and has no loose de Bruijn
  variables. The witness uses the identical type. This covers sentences (`alpha = Empty`) and
  nullary/empty contexts without a special exception.
- `BoundedFormula.IsQF` is mathlib's inductive predicate excluding both universal and existential
  quantifiers.
- `Theory.Iff` is semantic equivalence over every model of the selected theory and every free and
  bound valuation. The target asserts existence, not a computable elimination procedure.

This is an elaborated target only. It has no proof body and gives no theorem-completion credit.

## Mutation boundary

Four separately elaborated mutations remove the theory, change the loose-bound-variable domain
from `0` to `1`, restrict the outer binder to sentences, and exclude the empty free-variable type.
The validation recipe compares their printed kernel expressions with the canonical declaration;
all four must differ. These tests guard statement identity but do not purport to prove or refute
the mutated propositions.
