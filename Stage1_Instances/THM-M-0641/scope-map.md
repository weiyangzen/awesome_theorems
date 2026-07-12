# Scope map

## Received scope

The repository fixes only the name `莱夫谢茨不动点定理`, Solomon Lefschetz, the year 1926, and the
topic gloss `莱夫谢茨数与不动点`. This identifies the classical Lefschetz fixed-point family, but
not one binder-complete proposition. The point-set-topology category, execution rank, intake score,
and lane are scheduling metadata and add no mathematical assumptions.

## Candidate mathematical boundary

A source-faithful target may use the familiar implication "nonzero Lefschetz number implies a fixed
point" only after an accepted source fixes all of the following:

- the space class: finite simplicial complex, compact polyhedron, finite CW complex, compact ENR,
  or another admissible fixed-point-theorem category;
- whether the map is a continuous self-map, a simplicial map, or a map equipped with a selected
  approximation and invariance theorem;
- singular or simplicial homology versus cohomology, the coefficient ring or field, and whether
  torsion or a free-part/rationalization convention is used;
- finiteness conditions ensuring that every trace exists and only finitely many degrees contribute;
- the exact Lefschetz-number formula, degree indexing, alternating-sign and reduced/unreduced
  conventions, and transport invariance;
- whether the conclusion is `Exists (Function.IsFixedPt f)`, nonemptiness of `fixedPoints f`, a
  coincidence statement, or a stronger fixed-point index/local contribution identity;
- every ordered binder, universe, topology, compactness, finiteness, continuity, and nonzero
  hypothesis, plus all degenerate cases.

These bullets inventory the theorem family. They are not a selected canonical statement.

## Ambiguities and boundary cases

1. A finite complex can be represented combinatorially, geometrically, or only up to homotopy;
   these produce materially different Lean interfaces.
2. Rational homology makes the trace straightforward on finite-dimensional vector spaces, while
   integral homology requires an explicit convention for torsion or rationalization.
3. Singular and simplicial formulations require a checked comparison, not a name-level equation.
4. The identity-map specialization relates the Lefschetz number to Euler characteristic but does
   not replace the general self-map theorem.
5. A fixed point does not imply a nonzero Lefschetz number, so no converse may be silently added.
6. Empty spaces, empty complexes, disconnected spaces, zero-dimensional spaces, constant maps,
   identity maps, zero homology, and vanishing alternating trace require explicit treatment.
7. A fixed-point index equality or sum of local indices is stronger data than the catalog gloss
   necessarily selects and must not be folded into the root without a source decision.

## Explicit exclusions

- Brouwer, Schauder, Kakutani, Nielsen, or Banach fixed-point theorems as substitutes.
- The Atiyah-Bott fixed-point formula, an equivariant index formula, a coincidence theorem, or a
  local index formula silently substituted for the classical global implication.
- An arbitrary compact Hausdorff space without the source-selected finiteness or admissibility
  conditions needed for a Lefschetz number and theorem.
- Only the Euler-characteristic identity-map corollary, a contractible-space corollary, a finite-set
  trace identity, or one explicit self-map presented as the general root.
- A structure that stores the desired implication, fixed point, homology map, trace formula, or
  finiteness facts as fields and then projects them as a purported proof.
- The catalog label `已验证`, a bibliography record, an API probe, or an unrelated passing Lean
  declaration treated as statement or proof evidence.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the modules
`Mathlib.AlgebraicTopology.SingularHomology.Basic`, `Mathlib.LinearAlgebra.Trace`, and
`Mathlib.Dynamics.FixedPoints.Basic` expose adjacent substrate. The bounded topic search found no
classical `LefschetzNumber` definition or terminal Lefschetz fixed-point theorem in pinned mathlib
or the repo-local Lean tree. Exact imports, expression and environment fingerprints, transports,
and mutations belong to the statement phase after a primary proposition is selected and reviewed.
