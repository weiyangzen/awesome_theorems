# Scope map

## Included claim

- The first-order theory of real closed fields, not merely the single structure of real numbers.
- A fixed finite-signature presentation supporting polynomial equalities and order/sign conditions.
- For every formula with any finite or arbitrary indexed family of free variables, existence of a
  formula with no bound quantifiers and the same free-variable interface.
- Equivalence in every model of the real-closed-field theory, with all valuations quantified.
- Parameters only through the declared free-variable/constant interface; no hidden parameters.

## Decisions required at statement freeze

The statement phase must select and source-check the language: ordered rings with `<` or `<=`, or
the pure ring language after a checked proof that order is definable in real closed fields. It must
freeze the exact axiom theory, characteristic convention, formula representation, definition of
quantifier-free, free-variable type and binder order, whether elimination returns a witness or only
asserts existence, and whether equivalence is semantic over all models or derivability modulo the
theory. The selected form must include sentences, nullary formulas, empty variable contexts, and
all real closed fields; boundary cases must not be discarded for convenience.

## Explicit exclusions

- Quantifier elimination only for `Real`, algebraically closed fields, Presburger arithmetic, or
  one-variable formulas as a substitute for the real-closed-field theorem.
- Decidability of elementary algebra and geometry without a checked bridge to the exact
  formula-elimination claim.
- A semantic restatement that assumes a quantifier-free equivalent formula as a hypothesis or
  structure field.
- Fourier-Motzkin elimination for linear inequalities or cylindrical algebraic decomposition alone.
- Treating mathlib's algebraic `IsRealClosed` class plus generic formula syntax as proof closure.
- The manifest label `\u5df2\u9a8c\u8bc1` as human-proof or machine-proof evidence.

The later Lean statement must connect a concrete first-order language and theory to concrete real
closed field structures. An abstract predicate named `HasQuantifierElimination` is acceptable only
when its definition is unfolded and crosswalked, never when the desired conclusion is supplied as
data.
