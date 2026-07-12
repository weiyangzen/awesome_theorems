# Scope map

## Included topic boundary

- A subset of real three-dimensional Euclidean space specified by an exact source, most likely a
  solid ball, sphere, or all of space.
- A finite partition/equidecomposition of that set and one or two congruent copies.
- The exact allowed transformations: rotations, translations, orientation-preserving rigid
  motions, or all Euclidean isometries.
- The nonconstructive selection principles actually used by the accepted proof.

## Ambiguities to resolve at statement freeze

The repository record does not decide:

1. whether "ball" means the open ball, closed ball, boundary sphere, or a colloquial solid ball;
2. whether the target is a ball equidecomposable with two balls, a sphere version, or the stronger
   result that any two bounded subsets of `R^3` with nonempty interior are equidecomposable;
3. whether the two target copies live in one ambient space as disjoint translated balls or in a
   tagged disjoint union;
4. which congruence group acts and whether reflections are allowed;
5. whether a specific number of pieces, such as five, belongs to the claimed theorem;
6. whether `Axiom of Choice` names a foundation profile or is intended as an explicit premise.

The statement phase must inspect an immutable source passage and freeze these choices, all ordered
binders, the positive-radius condition, the ambient dimension, and the exact conclusion.

## Explicit exclusions

- The two-dimensional circle-squaring theorem or any measurable/equal-volume decomposition.
- Hilbert's hotel or a bare cardinal equivalence as a substitute for finite congruent pieces.
- A generic equidecomposition theorem with the paradoxicality premise assumed rather than proved
  for the intended three-dimensional object.
- A sphere-boundary result silently substituted for a solid-ball result, or conversely.
- A theorem asserting only that the pieces are nonmeasurable.
- The repository label `已验证`, an API probe, or a historical attribution as proof credit.

No canonical Lean target is frozen at intake because the source record does not select one exact
version.

