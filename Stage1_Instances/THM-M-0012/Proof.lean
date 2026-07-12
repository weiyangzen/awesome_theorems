import ObligationTree

/-!
# THM-M-0012: proof of the fundamental theorem of algebra target

The direct declaration installs the exact pinned `Complex.exists_root` body at the frozen target.
The second declaration independently checks the frozen child-to-parent architecture by supplying
the four analytic engines, recomposing the no-root contradiction and positive-degree anchor, and
finally applying the nonconstant-to-positive-degree bridge.
-/

namespace Stage1Instances.THM_M_0012.Proof

open Filter Polynomial
open scoped Topology
open Stage1Instances.THM_M_0012
open Stage1Instances.THM_M_0012.ObligationTree

/-- The canonical target, discharged by the exact theorem at the pinned mathlib revision. -/
theorem fundamentalTheoremOfAlgebra : FundamentalTheoremOfAlgebraTarget := by
  intro f hf
  exact Complex.exists_root ((nonconstant_iff_degree_pos f).1 hf)

/-- The frozen nonconstancy normalization as an architecture-level proof body. -/
theorem nonconstantDegreeBridge : NonconstantDegreeBridge := by
  intro f hf
  exact (nonconstant_iff_degree_pos f).1 hf

/-- Root-free polynomial evaluation has a differentiable reciprocal. -/
theorem reciprocalDifferentiability : ReciprocalDifferentiabilityEngine := by
  intro f hrootFree
  exact f.differentiable.inv hrootFree

/-- Positive polynomial degree makes reciprocal evaluation tend to zero at infinity. -/
theorem reciprocalDecay : ReciprocalDecayEngine := by
  intro f hdegree
  exact Metric.cobounded_eq_cocompact (α := Complex) ▸
    (Filter.tendsto_inv₀_cobounded.comp <| by
      simpa only [tendsto_norm_atTop_iff_cobounded]
        using f.tendsto_norm_atTop hdegree tendsto_norm_cobounded_atTop)

/-- Liouville's theorem identifies a differentiable function with its limit at infinity. -/
theorem liouvilleZero : LiouvilleZeroEngine := by
  intro g hg hlimit z
  exact hg.apply_eq_of_tendsto_cocompact z hlimit

/-- If every inverse evaluation vanishes, polynomial extensionality forces the zero constant. -/
theorem polynomialConstant : PolynomialConstantEngine := by
  intro f hinverse
  exact Polynomial.funext fun z => inv_injective <| by simp [hinverse z]

/-- The four analytic engines compose into the frozen root-free contradiction branch. -/
theorem noRootContradiction : NoRootContradictionEngine :=
  noRootContradiction_of_engines reciprocalDifferentiability reciprocalDecay
    liouvilleZero polynomialConstant

/-- The expanded Liouville route independently constructs the positive-degree anchor. -/
theorem positiveDegreeAnchor_expanded : PositiveDegreeAnchor :=
  positiveDegreeAnchor_of_noRootContradiction noRootContradiction

/-- The pinned terminal theorem installed at the exact architecture-level anchor interface. -/
theorem positiveDegreeAnchor_mathlib : PositiveDegreeAnchor := by
  intro f hdegree
  exact Complex.exists_root hdegree

/-- Exact root proof obtained by supplying and consuming every frozen proof-graph child. -/
theorem fundamentalTheoremOfAlgebra_via_frozen_composition :
    FundamentalTheoremOfAlgebraTarget :=
  root_of_degreeBridge_and_positiveDegreeAnchor nonconstantDegreeBridge
    positiveDegreeAnchor_expanded

/-- The root composition also consumes the explicitly pinned positive-degree anchor. -/
theorem fundamentalTheoremOfAlgebra_via_pinned_composition :
    FundamentalTheoremOfAlgebraTarget :=
  root_of_degreeBridge_and_positiveDegreeAnchor nonconstantDegreeBridge
    positiveDegreeAnchor_mathlib

#print axioms fundamentalTheoremOfAlgebra
#print axioms fundamentalTheoremOfAlgebra_via_frozen_composition
#print axioms Complex.exists_root
#print axioms nonconstantDegreeBridge
#print axioms reciprocalDifferentiability
#print axioms reciprocalDecay
#print axioms liouvilleZero
#print axioms polynomialConstant
#print axioms noRootContradiction
#print axioms positiveDegreeAnchor_expanded
#print axioms positiveDegreeAnchor_mathlib
#print axioms fundamentalTheoremOfAlgebra_via_pinned_composition

end Stage1Instances.THM_M_0012.Proof
