import Statement

/-!
# THM-M-0012 conditional obligation composition

This file checks the three child-to-parent interfaces in the frozen obligation graph. The
analytic engines and the positive-degree root theorem remain explicit premises, so this module
does not install the audited candidate or prove the fundamental theorem of algebra.
-/

namespace Stage1Instances.THM_M_0012.ObligationTree

open Filter Polynomial
open scoped Topology

/-- Exact positive-degree interface exported by the audited mathlib candidate. -/
def PositiveDegreeAnchor : Prop :=
  forall f : Polynomial Complex, 0 < degree f ->
    exists z : Complex, IsRoot f z

/-- The normalization required by the exact target-to-anchor composition. -/
def NonconstantDegreeBridge : Prop :=
  forall f : Polynomial Complex,
    Stage1Instances.THM_M_0012.Nonconstant f -> 0 < degree f

/-- The single contradiction branch hidden by a short invocation of the anchor theorem. -/
def NoRootContradictionEngine : Prop :=
  forall f : Polynomial Complex, 0 < degree f ->
    (forall z : Complex, Not (IsRoot f z)) -> False

/-- Root-free polynomial evaluation has a differentiable reciprocal. -/
def ReciprocalDifferentiabilityEngine : Prop :=
  forall f : Polynomial Complex, (forall z : Complex, eval z f ≠ 0) ->
    Differentiable Complex fun z : Complex => (eval z f)⁻¹

/-- Positive degree forces reciprocal evaluation to tend to zero at complex infinity. -/
def ReciprocalDecayEngine : Prop :=
  forall f : Polynomial Complex, 0 < degree f ->
    Tendsto (fun z : Complex => (eval z f)⁻¹) (cocompact Complex) (nhds 0)

/-- The exact Liouville consequence used by the pinned terminal proof. -/
def LiouvilleZeroEngine : Prop :=
  forall g : Complex -> Complex, Differentiable Complex g ->
    Tendsto g (cocompact Complex) (nhds 0) -> forall z : Complex, g z = 0

/-- Pointwise vanishing of inverse evaluations forces the polynomial to be `C 0`. -/
def PolynomialConstantEngine : Prop :=
  forall f : Polynomial Complex,
    (forall z : Complex, (eval z f)⁻¹ = 0) -> f = C 0

/-- Checked composition of every analytic engine into the no-root contradiction branch. -/
theorem noRootContradiction_of_engines
    (reciprocalDifferentiable : ReciprocalDifferentiabilityEngine)
    (reciprocalDecay : ReciprocalDecayEngine)
    (liouvilleZero : LiouvilleZeroEngine)
    (polynomialConstant : PolynomialConstantEngine) :
    NoRootContradictionEngine := by
  intro f hdegree hnoRoot
  have hEvalNe (z : Complex) : eval z f ≠ 0 := by
    intro hz
    exact hnoRoot z (IsRoot.def.mpr hz)
  have hInverseZero : forall z : Complex, (eval z f)⁻¹ = 0 :=
    liouvilleZero (fun z : Complex => (eval z f)⁻¹)
      (reciprocalDifferentiable f hEvalNe) (reciprocalDecay f hdegree)
  have hconstant : f = C 0 := polynomialConstant f hInverseZero
  exact (not_lt_of_ge (hconstant.symm ▸ degree_C_le)) hdegree

/-- Checked branch recomposition from contradiction under root-freeness to root existence. -/
theorem positiveDegreeAnchor_of_noRootContradiction
    (contradictionEngine : NoRootContradictionEngine) : PositiveDegreeAnchor := by
  intro f hdegree
  by_contra hnoRoot
  exact contradictionEngine f hdegree fun z hz => hnoRoot <| Exists.intro z hz

/-- Checked transport and root composition. Both explicit children are consumed. -/
theorem root_of_degreeBridge_and_positiveDegreeAnchor
    (degreeBridge : NonconstantDegreeBridge)
    (anchor : PositiveDegreeAnchor) :
    Stage1Instances.THM_M_0012.FundamentalTheoremOfAlgebraTarget := by
  intro f hf
  exact anchor f (degreeBridge f hf)

#check Complex.exists_root
#check Polynomial.differentiable
#check Differentiable.inv
#check Polynomial.tendsto_norm_atTop
#check Filter.tendsto_inv₀_cobounded
#check Differentiable.apply_eq_of_tendsto_cocompact
#check Polynomial.funext
#print axioms noRootContradiction_of_engines
#print axioms positiveDegreeAnchor_of_noRootContradiction
#print axioms root_of_degreeBridge_and_positiveDegreeAnchor

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0012.FundamentalTheoremOfAlgebraTarget

end Stage1Instances.THM_M_0012.ObligationTree
