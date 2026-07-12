# Scope map

## Included claim

- A connected compact smooth manifold `W` whose boundary is identified with the disjoint union of
  closed smooth manifolds `M0` and `M1`.
- The two boundary inclusions are homotopy equivalences, making `(W; M0, M1)` an h-cobordism.
- `dim W >= 6` (equivalently, boundary dimension at least five).
- The Whitehead torsion of the incoming inclusion `M0 -> W` is zero.
- Equivalence with a diffeomorphism `W ~= M0 x [0,1]` that is relative to the incoming boundary.

This freezes the standard smooth high-dimensional product-recognition formulation as the intended
human theorem. It does not yet freeze a formal proposition: the statement phase must choose exact
manifold-with-boundary, collar, fundamental-group, simple-homotopy, Whitehead-group, torsion, and
relative-diffeomorphism interfaces and elaborate the complete binder/hypothesis list.

## Boundary decisions

- The dimension bound belongs to the cobordism dimension. A source phrased with
  `dim M0 >= 5` must be transported explicitly.
- Connectedness is included. Disconnected componentwise variants require a checked extension.
- No orientation hypothesis is silently assumed; the statement audit must decide whether the
  selected source formulation needs one.
- The zero-torsion and simple-homotopy formulations are intended equivalents, but only after the
  Whitehead-torsion definition and a checked transport are fixed.
- The product diffeomorphism must restrict to the prescribed identification on `M0`. Claims only
  of abstract diffeomorphism or homotopy equivalence are weaker and cannot replace it.

## Explicit exclusions

- Smale's simply connected h-cobordism theorem alone; it is a specialization, not the general
  Whitehead-torsion classification.
- The converse implication alone (a product cobordism has zero torsion).
- PL or topological s-cobordism variants, dimension four results, controlled s-cobordism, and
  surgery-theoretic analogues.
- A classification merely asserting that h-cobordisms correspond to a Whitehead group unless its
  hypotheses and relative product consequence compose to the canonical claim.
- Any abstract structure that carries productness or zero torsion as an assumption.

## Expected formal surface

The formal target needs substantial infrastructure spanning smooth manifolds with boundary,
relative homotopy equivalences, finite CW or chain-complex models, fundamental groups and group
rings, Whitehead groups and torsion, handle decompositions/cancellation, and relative
diffeomorphisms. Intake located no exact target in pinned mathlib. No surrogate proposition may be
introduced merely because these interfaces are absent.
