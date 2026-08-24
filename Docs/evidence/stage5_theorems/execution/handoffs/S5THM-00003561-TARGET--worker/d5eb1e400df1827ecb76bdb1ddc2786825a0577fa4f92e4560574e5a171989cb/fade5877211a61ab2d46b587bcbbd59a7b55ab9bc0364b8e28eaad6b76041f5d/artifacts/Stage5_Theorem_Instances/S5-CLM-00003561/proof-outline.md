# Proof outline for S5-CLM-00003561

The frozen claim says that both the complete graph `K₆` and the complete
tripartite graph `K₁,₃,₃` have unit-distance dimension five and fifteen edges.

1. `K₆` has fifteen edges.  A regular simplex on six vertices embeds it in
   five dimensions.  Conversely, after translating one vertex to the origin,
   the other five displacement vectors have Gram matrix with diagonal `1` and
   off-diagonal `1/2`.  Its quadratic form is
   `1/2 * ∑ xᵢ² + 1/2 * (∑ xᵢ)²`, so the five vectors are independent.  Hence
   no lower-dimensional realization exists.
2. `K₁,₃,₃` has `1·3 + 1·3 + 3·3 = 15` edges.  In an orthogonal decomposition
   of dimensions `1 + 2 + 2`, put the singleton at zero, use a common vector of
   squared norm `1/2`, and add two orthogonal equilateral triples of squared
   norm `1/2`.  Cross-part distances are one and same-part distances have
   square `3/2`, giving a faithful five-dimensional realization.
3. For the lower bound, translate the singleton to zero.  Each three-vertex
   part lies on the unit sphere, and three distinct points on that sphere are
   not collinear.  Their two-dimensional difference spaces are orthogonal by
   the cross-edge equations.  The common component forced by cross inner
   product `1/2` is outside their four-dimensional direct sum.  Thus any
   faithful realization needs at least five dimensions.

The detailed hypotheses, exceptional cases, formal anchors, and downstream
uses are recorded once in `proof-units.json` and reconstructed in
`full-study.md`.
