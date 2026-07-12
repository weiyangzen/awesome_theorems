# Statement freeze

Item: `S56-M-1143-STATEMENT`

The canonical target is
`Stage1Instances.THM_M_1143.BoundedHarmonicIsConstant`. It states that for every positive
dimension `n`, a real-valued function on all of `EuclideanSpace Real (Fin n)` that is harmonic at
every point and has bounded range takes the same value at every pair of points.

## Encoding decisions

- The PDE reading is the classical Euclidean theorem in arbitrary finite positive dimension, not
  a version fixed to the plane or any of the unrelated theorems called Liouville's theorem.
- `HarmonicOnNhd f univ` uses mathlib's Fréchet-Laplacian definition and includes the required
  twice-differentiable local regularity.
- `Bornology.IsBounded (range f)` is global norm boundedness. For a real-valued function this is a
  two-sided bound; it does not silently replace boundedness with only an upper or lower bound.
- `forall x y, f x = f y` states constancy without choosing a base point. The explicit `0 < n`
  matches the standard positive-dimensional formulation. Dimension zero would be a trivially true
  boundary extension, not a counterexample.

The direct imports are
`Mathlib.Analysis.InnerProductSpace.Harmonic.Basic` and
`Mathlib.Analysis.InnerProductSpace.PiL2`. The first supplies the harmonic predicate and the second
the finite Euclidean-space inner-product instance. Neither imports the complex-plane Liouville
theorem. Five separately elaborated mutations check that boundedness, harmonicity, domain,
dimension, and the interpretation of boundedness have not been collapsed by the encoding.

This phase freezes and elaborates a proposition only. It does not establish a primary-source
pinpoint, provide a proof, or claim theorem completion.
