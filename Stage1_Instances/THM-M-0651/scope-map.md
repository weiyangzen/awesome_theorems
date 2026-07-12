# Scope map

## Included claim

- A first-order language `L` with countably many symbols (or an explicitly equivalent encodable
  presentation selected during statement work).
- A consistent `L`-theory `T`.
- A countable indexed family of partial types over the empty parameter set, with one fixed finite
  tuple arity per indexed type unless the selected source justifies a more general encoding.
- Each type is nonprincipal over `T`: no single formula consistent with `T` isolates that type.
- Existence of a countable `L`-structure satisfying `T` in which no tuple realizes any member of
  the family.

## Quantifier and hypothesis map

The intended order is: language, its countability evidence, theory, consistency evidence, index
type/family, countability evidence for the family, arities and partial types, and nonprincipality
evidence; the conclusion then existentially quantifies a countable model, its `L`-structure, its
model-of-`T` witness, and simultaneous omission. The statement phase must freeze whether
countability means `Countable` or a concrete enumeration and whether the model carrier is literally
`Nat` or only admits a countability witness.

## Boundary cases to freeze

- The empty family should reduce to the downward countable-model/existence case; satisfiability of
  an empty or consistent theory must not be silently assumed through an inhabited model type.
- Empty and finite types, varying finite arities, nullary types, and duplicate family entries need
  explicit treatment.
- "Nonprincipal" must be relative to `T`; syntactic non-isolation and the chosen semantic
  formulation require a checked bridge before either receives credit.
- If finite languages or finite models are admitted, the formulation must preserve the theorem and
  not introduce an unintended requirement that the carrier be countably infinite.

## Explicit exclusions

- The single-type theorem unless a checked reduction establishes the countable simultaneous form.
- The complete-theory/complete-type variant without a checked transport from partial types over an
  arbitrary consistent theory.
- The uncountable omitting types theorem, atomic model theorem, Ryll-Nardzewski theorem, or a Baire
  category lemma standing alone.
- A structure that stores the desired model or omission property as an input field.
- Replacing omission by non-realization of one chosen tuple, or replacing `T`-relative
  nonprincipality by mere non-finite-generation of a set of formulas.

## Lean boundary

Pinned mathlib provides `FirstOrder.Language`, theories, satisfiability/semantics, and complete-type
infrastructure under `Mathlib.ModelTheory`. A repository-local text search found no omitting-types
result. The statement phase must determine whether partial types and omission can be expressed
directly using existing formula/theory APIs or need conservative local definitions, then elaborate
the exact target with minimal imports. No declaration or proof is credited at intake.
