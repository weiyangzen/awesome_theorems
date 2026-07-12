# Scope map

## Included theorem family

- First-order formulas interpreted in the standard natural numbers, or in the models of one
  precisely specified Presburger theory if that is what the primary source proves.
- Addition, constants, equality, and every order or congruence/divisibility symbol required for
  the selected quantifier-elimination theorem.
- A transformation or existence result assigning every formula an equivalent quantifier-free
  formula, preserving all free variables and equivalence for every assignment.
- The attribution-specific Ackermann result only after its original statement, language, and
  proof boundary have been inspected.

## Decisions deferred to the statement gate

The repository gloss is insufficient to choose between standard-model and theory-relative
equivalence, between semantic existence and a verified elimination algorithm, or among language
expansions. These are mathematically material choices. In particular, pinned mathlib defines
`FirstOrder.Language.presburger` using only `(0, 1, +)` and no relation symbols. Ordinary syntactic
quantifier elimination does not hold in that bare language: divisibility/congruence conditions
arising from existential formulas are not generally expressible quantifier-free there. A later
statement must therefore freeze a source-faithful expansion rather than assert the convenient but
false bare-language version.

The exact formula type (`Formula`, `BoundedFormula`, or sentences), free-variable type, treatment
of parameters, output-language closure, semantic evaluator, and equivalence relation remain open.
The statement phase must include closed sentences and the zero-free-variable boundary, and must
mutation-test removal of congruence predicates, weakening of assignment-uniform equivalence, and
changing the standard-model/theory boundary.

## Explicit exclusions

- The mathlib theorem that definable sets are semilinear as the root without checked equivalence
  to the selected quantifier-elimination statement.
- Decidability of Presburger arithmetic, completeness, or a normal-form theorem as a substitute.
- Elimination for one chosen formula rather than all formulas.
- An output formula that retains quantifiers or uses undeclared extra predicates.
- Quantifier elimination for real closed fields, generic theories, or an Ackermann-function result.
- The repository labels `已验证`, the intake probe, or a module TODO as proof evidence.
