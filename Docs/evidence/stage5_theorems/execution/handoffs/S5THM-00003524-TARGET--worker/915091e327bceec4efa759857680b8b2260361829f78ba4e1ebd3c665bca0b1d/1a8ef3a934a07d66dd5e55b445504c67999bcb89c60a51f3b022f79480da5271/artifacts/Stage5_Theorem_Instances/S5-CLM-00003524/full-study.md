# S5-CLM-00003524 full study

Let `D` be the distance matrix, `Z(t)ᵢⱼ = exp (-t Dᵢⱼ)`, and
`w(t) = Z(t)⁻¹ 1`.  A gauging is a vector `g` with `Σ g = 1` and
`Dg = c1`.  The following fragments reconstruct every node of the proof DAG.

<a id="h-n0"></a>
## H-N0 — the similarity equations

For every sufficiently small positive scale at which `Z(t)` is invertible,
the definition of matrix inverse gives `Z(t) w(t) = 1`.  Invertibility is
eventual in the proof below because a row-reduced version of `Z(t)` converges
to a nonsingular matrix.  Thus no value assigned by `Matrix.inv` at a singular
matrix affects the filter limit.

<a id="h-n1"></a>
## H-N1 — row differences expose the distance matrix

Choose a base point.  Keep its row, and for every other row subtract the base
row and divide by `t`.  These are invertible row operations when `t > 0`.
Since `(exp (-t a) - exp (-t b))/t → b-a`, the transformed coefficient matrix
converges entrywise to one normalization row together with all corresponding
row differences of `D`.  The transformed right hand side is one in the base
row and zero in all difference rows.

<a id="h-n2"></a>
## H-N2 — nonsingularity of the limiting system

The limiting equations say `Σ x = 1` and that all coordinates of `D x` are
equal.  If the associated homogeneous system has solution `x`, then `Σ x=0`
and `D x = c1`.  Applying the inverse of `D` gives `x = c D⁻¹1`; substituting
in the row-difference and normalization presentation shows `c=0`, hence
`x=0`.  Equivalently, elementary row/column operations identify this
augmented limit with the invertible distance-matrix system used by the
Mathlib lemma.  Nonemptiness is used to choose the base row.

<a id="h-n3"></a>
## H-N3 — continuous inversion gives the microscopic limit

If `g` is a gauging of concentration `c`, its equations are precisely the
limiting row-reduced system: the normalization row is `Σ g=1`, and every
distance-row difference vanishes because `Dg=c1`.  By H-N2 the limiting
coefficient matrix is nonsingular.  Determinant and inverse are continuous on
finite matrices, so the transformed solutions converge to the unique limiting
solution `g`.  Undoing the row operations does not change the unknown vector;
hence `w(t) → g` as `t → 0+`.

<a id="h-n4"></a>
## H-N4 — microscopic weighting implies concentration

Conversely, assume `w(t) → w`.  Pass the equations of H-N0 through the row
operations of H-N1.  Their limits give `Σ w=1` and equality of every coordinate
of `Dw`.  Calling this common coordinate `c` yields `Dw=c1`; therefore `(w,c)`
is a gauging.  This direction does not require invertibility of `D`.

<a id="h-n5"></a>
## H-N5 — concentration implies microscopic weighting

Assume `det D` is a unit and choose the gauging promised by finite
concentration.  H-N3 proves that `w(t)` tends to that gauging on the right of
zero, which is exactly `HasMicroscopicWeighting X`.  The concentration scalar
need not be nonzero and is never divided by.

<a id="h-n6"></a>
## H-N6 — semantic transport

The target proposition uses the frozen provider's fully qualified
`distanceMatrix`, `HasMicroscopicWeighting`, and `HasFiniteConcentration`
constants.  `source_to_target` and `target_to_source` transport the same
elaborated proposition in both directions.  The source theorem body (which
contains `sorryAx`) is never referenced.  The canonical Master must recompute
the root expression and the complete non-foundation constant census.

<a id="h-n7"></a>
## H-N7 — composition and release boundary

H-N4 proves the forward implication, H-N5 proves the reverse implication under
the stated determinant hypothesis, and H-N6 binds both to the frozen source
type.  Introducing the biconditional and composing these implications proves
the claim-owned root.  Worker validation is only a semantic/evidence preflight;
the canonical Master remains responsible for trust-zero cold compilation and
the final Stage6-bound acceptance decision.
