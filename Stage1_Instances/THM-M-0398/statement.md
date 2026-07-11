# Canonical Lean statement

## Declaration

The canonical target is `Stage1Instances.THMM0398.ThueSiegelRoth` in
`Statement.lean`. Its ordered binders and expanded expression are:

```lean
∀ α : ℝ,
  IsAlgebraic ℚ α →
  Irrational α →
  ∀ ε : ℝ,
    0 < ε →
    {r : ℚ |
      |α - (r : ℝ)| < 1 / (r.den : ℝ) ^ ((2 : ℝ) + ε)}.Finite
```

The checked theorem `thueSiegelRoth_iff` proves by definitional equality that
the named target expands to exactly this expression.

## Encoding decisions

- Algebraicity uses mathlib's `IsAlgebraic ℚ α`, not the legacy custom
  integer-polynomial predicate.
- Approximants are rationals, so equivalent integer pairs cannot create
  duplicate solutions. `Rat.den` supplies the unique positive normalized
  denominator; `denominator_pos` checks its positivity after coercion to `ℝ`.
- The exponent is real and the denominator power is `Real.rpow`, selected by
  the real exponent. The bound is strict and exactly `1 / q^(2 + ε)`.
- The conclusion is finiteness of the subtype-defining set of rationals.
- `ε = 0`, rational `α`, and non-algebraic `α` are outside the hypotheses.
  A zero or negative denominator is unrepresentable through normalized
  `Rat.den`.

## Imports and environment

The source directly imports only:

```lean
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.NumberTheory.Real.Irrational
```

These are the narrow feature modules for real powers and the irrational/
algebraic predicates. The project pins Lean `v4.29.0` and mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Status boundary

Elaboration establishes that the exact proposition is well typed. The file
contains definitions plus only reflexive/denominator interface checks. It does
not declare an axiom, use `sorry`, or construct a proof of `ThueSiegelRoth`.
Anchor, obligation, proof, trust-closure, and release gates remain open.
