# Scope map

## Included theorem family

- A complete first-order theory `T` in a language `L`, with stability understood in an exact
  source-selected cardinal or type-counting formulation.
- Complete types of tuples over parameter sets and their restriction/extension behavior.
- Dividing of a formula over a base, normally witnessed by an indiscernible sequence and an
  inconsistent family of instances.
- Forking of formulas and types over a base, and the induced ternary notation saying a tuple is
  independent from one parameter set over another.
- A source-selected proposition about that relation. The leading candidate is the stable-theory
  independence calculus: invariance, finite character, symmetry, transitivity, extension, and
  local character.

This is a theorem-family boundary, not an exact root. The repository phrase only says "an
independence concept" and therefore cannot determine whether the desired result is a definition,
one property, an equivalence of definitions, or the whole calculus.

## Statement-phase decisions

The statement phase must first select and inspect a primary theorem. It must then freeze the
one-sorted or many-sorted convention, complete theory, stability definition, monster model or
explicit saturated-model interface, smallness cardinal, tuple arity, set inclusions, formula/type
definitions of dividing and forking, and the exact list and order of conclusions.

Boundary tests must include the empty base, algebraic types, `A = B`, singleton versus arbitrary
tuples, removal of stability, removal of saturation, reversal of symmetry, and both directions of
transitivity. Each independence axiom in a packaged conclusion must later receive its own
obligation; a structure populated by assumed fields would not prove the theorem.

## Explicit exclusions

- Probability-theoretic conditional independence, linear independence, and set-theoretic
  independence.
- Arbitrary ternary relations merely postulated to satisfy independence axioms.
- Defining a `Forking` predicate and presenting the definition itself as the theorem.
- Simplicity-theory independence without distinguishing the hypotheses and conclusions that differ
  from stable theory.
- Algebraic independence as a substitute, absent a checked theorem identifying it with nonforking
  in a particular theory.
- The repository date/attribution/status label, the existence of complete types in mathlib, or the
  intake elaboration probe as source or proof evidence.
