# Scope map

## Preserved theorem family

The intake preserves the catalog's classical local-global principle for quadratic forms. A common
candidate reading is the Hasse-Minkowski isotropy criterion: a quadratic form over a number field
has a nonzero isotropic vector globally exactly when it has one after scalar extension to every
completion. This is a scope locator, not the canonical claim selected by the catalog.

## Decisions required at statement freeze

1. Preserve and hash one lawful complete primary source, select a pinpoint theorem and proof
   boundary, map all incorporated definitions and assumptions, audit corrections and translations,
   and obtain independent source review.
2. Fix whether the root concerns isotropy/nontrivial zeros, representation of a scalar, rational
   equivalence of forms, classification by invariants, or an explicit checked relationship among
   these results. None may substitute for another by name alone.
3. Fix the base field: the rational numbers, an arbitrary number field, or another global field;
   state its characteristic and all algebraic structures.
4. Fix the quadratic object: a coordinate polynomial, quadratic form, or quadratic space; the
   vector-space dimension; finite-dimensionality; regularity/nondegeneracy; and any characteristic
   or invertibility-of-two assumptions.
5. Fix the local family: all finite and infinite places, the construction of each completion, the
   scalar-extension convention, and whether complex places are vacuous or remain explicit.
6. Define isotropy and exclude the zero vector. Decide whether zero-dimensional spaces, the zero
   form, degenerate forms, one-dimensional forms, and empty or redundant place families are in
   scope or separate boundary cases.
7. Fix the logical conclusion: an `iff`, only local-to-global, only global-to-local, or a stronger
   equivalence/classification statement. Any alternate encoding needs a checked transport.
8. Freeze ordered binders, universes, typeclass assumptions, foundation/choice policy, minimal
   imports, exact Lean expression, environment fingerprint, and the required mutation suite.

## Candidate architecture, not yet obligations

- define nonzero isotropy and scalar extension of a quadratic form;
- model finite and archimedean number-field completions;
- prove the functorial global-to-local direction;
- develop or import local classification, Hilbert symbols, local invariants, and reciprocity;
- prove the hard local-to-global direction; and
- compose checked transports back to the exact source-selected root.

This list is orientation only. No obligation registry, denominator, typed graph, or proof status is
frozen during intake.

## Substitution and ownership exclusions

- `THM-M-0423` owns the catalog's broader "Hasse principle" item. Its rev-5.6 files selected a
  classical quadratic scope because unrestricted Hasse principles can fail. The resulting semantic
  overlap must be resolved by the integration lane; its artifacts and status are not inherited.
- The generic implication "local points imply a global point" is false for arbitrary varieties and
  cannot replace a quadratic-form theorem.
- A theorem for rational numbers alone does not prove an arbitrary number-field root without a
  checked generalization or transport.
- The easy global-to-local direction, completion APIs, a product formula, real diagonalization, or
  a structure storing the hard implication is substrate, not Hasse-Minkowski closure.
- A coordinate polynomial, scalar-representation theorem, equivalence theorem, and isotropy theorem
  are proposition-changing variants until exact relationships are checked.
- The repository's `verified` label, a famous theorem name, prose, and this intake probe provide no
  source-fidelity or machine-proof credit.

## Formal boundary

Pinned mathlib supplies quadratic forms, anisotropy and nondegeneracy predicates, base change, and
finite/infinite number-field place infrastructure. The probe authenticates only those adjacent
interfaces. It does not select the source proposition, elaborate the canonical root, inspect a
terminal proof body, or establish an exhaustive anchor search. Exact statement identity,
fingerprints, transports, and mutations belong to `S56-M-0020-STATEMENT`.
