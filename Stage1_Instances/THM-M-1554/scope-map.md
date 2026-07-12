# Scope map

## Included claim family

- A named, explicitly normalized integrable PDE on a fixed domain and scalar field.
- A source solution and a candidate transformed solution with enough regularity for every
  derivative appearing in the PDE and first-order Bäcklund relations.
- A fixed transformation parameter satisfying all source-required nondegeneracy conditions.
- Explicit first-order relations between the two functions, with signs and scale factors frozen.
- The preservation result: the transformed function satisfies the same PDE.
- The compatibility calculation relating the first-order system to the nonlinear PDE, but only in
  the direction or equivalence justified by the selected source and domain hypotheses.

This is an auto-Bäcklund scope. If source review instead establishes that the repository intended a
hetero-Bäcklund transformation between two distinct equations, changing to that target is a scope
change requiring a new reviewed intake rather than a quiet restatement.

## Statement-phase decisions

The next phase must choose the equation and a versioned source theorem. A natural candidate is the
classical sine-Gordon auto-Bäcklund transformation, but this intake does not promote that candidate
to the canonical statement. Source review must freeze:

- the PDE normalization and independent variables;
- the exact pair of first-order Bäcklund equations and parameter domain;
- real- or complex-valued solutions and the open set or global domain;
- the differentiability class and any mixed-partial interchange premise;
- whether the theorem assumes both source and target Bäcklund relations or constructs the target;
- whether the conclusion is local preservation, compatibility, existence, uniqueness, or
  invertibility, and which of these are actually in scope;
- zero/singular parameter behavior, constants, boundary conditions, and topology of the domain;
- ordered Lean binders, universes, typeclass assumptions, minimal imports, and alternate encodings.

## Explicit exclusions

- Treating the words "Bäcklund transformation" as a theorem without naming an equation.
- Defining `IsBacklundTransform u v` to contain the desired conclusion and then projecting it.
- Assuming that the transformed function satisfies the PDE in order to prove preservation.
- Proving only a generic algebraic rewrite with arbitrary predicates standing for the PDE and
  transformation relations.
- Substituting a Darboux transform, Miura transform, inverse-scattering construction, soliton
  formula, or unrelated transformation theorem.
- Claiming global existence, uniqueness, invertibility, permutability, or soliton generation when
  the reviewed statement establishes only local compatibility or preservation.

The exact Lean target, expression fingerprint, mutation suite, obligation registry, and proof
architecture belong to later nodes and remain deliberately open.
