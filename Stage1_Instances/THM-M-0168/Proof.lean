import ObligationTree
import Statement
import Mathlib.Analysis.Calculus.MeanValue

/-!
# THM-M-0168 proof-phase bodies

This module closes the calculus package that integrates constant coordinate
partials to an affine formula.  The geometric derivative-rigidity package is
still an explicit premise; Bernstein's analytic core is not asserted here.
-/

namespace Stage1Instances.THM_M_0168_Obligations

/-- The affine comparison function with the prescribed coordinate slopes. -/
private def affineModel (a b : Real) : Plane -> Real :=
  fun p => a * p.1 + b * p.2

/-- A continuously differentiable function on the plane whose two coordinate
partials are constant has the corresponding global affine formula. -/
theorem constantPartials_to_affine
    (u : Plane -> Real)
    (hu : ContDiff Real 2 u)
    (a b : Real)
    (hab : forall p : Plane,
      partialDeriv u 0 p = a /\ partialDeriv u 1 p = b) :
    exists c : Real, forall p : Plane, u p = a * p.1 + b * p.2 + c := by
  let g := affineModel a b
  have hu_diff : Differentiable Real u := hu.differentiable (by norm_num)
  have hg_diff : Differentiable Real g := by
    change Differentiable Real (fun p : Plane => a * p.1 + b * p.2)
    fun_prop
  have hg_fderiv (p : Plane) :
      fderiv Real g p =
        (a • ContinuousLinearMap.fst Real Real Real) +
          (b • ContinuousLinearMap.snd Real Real Real) := by
    change fderiv Real (fun p : Plane => a * p.1 + b * p.2) p = _
    convert (show HasFDerivAt (fun p : Plane => a * p.1 + b * p.2)
      ((a • ContinuousLinearMap.fst Real Real Real) +
        (b • ContinuousLinearMap.snd Real Real Real)) p by fun_prop).fderiv
  have hderiv : forall p, fderiv Real u p = fderiv Real g p := by
    intro p
    apply ContinuousLinearMap.ext
    rintro ⟨x, y⟩
    have hdecomp : (x, y) = x • coordinateVector 0 + y • coordinateVector 1 := by
      ext <;> simp [coordinateVector]
    rw [hdecomp]
    simp only [map_add, map_smul]
    rw [show fderiv Real u p (coordinateVector 0) = a from (hab p).1]
    rw [show fderiv Real u p (coordinateVector 1) = b from (hab p).2]
    rw [hg_fderiv]
    simp [coordinateVector, mul_comm]
  have hfun : u = fun p => g p + (u (0, 0) - g (0, 0)) := by
    obtain ⟨c, hc⟩ := isOpen_univ.exists_eq_add_of_fderiv_eq isPreconnected_univ
      hu_diff.differentiableOn hg_diff.differentiableOn
      (fun p _ => hderiv p)
    funext p
    rw [hc (Set.mem_univ p)]
    have hc0 := hc (Set.mem_univ (0, 0))
    linarith
  refine ⟨u (0, 0) - g (0, 0), ?_⟩
  intro p
  have hfun0 := congrFun hfun (0, 0)
  rw [congrFun hfun p]
  dsimp [g, affineModel] at hfun0 ⊢

/-- Closed body for the frozen affine-integration package. -/
theorem constantPartialsToAffine_proof : ConstantPartialsToAffine :=
  constantPartials_to_affine

/-- Root composition with only the geometric rigidity package remaining. -/
theorem bernstein_of_derivativeRigidity
    (rigidity : DerivativeRigidity) :
    BernsteinMinimalGraphTarget :=
  compose_root rigidity constantPartialsToAffine_proof

/-- The frozen obligation harness and the canonical statement are
definitionally the same proposition.  Keeping this transport explicit prevents
the duplicated harness namespace from receiving accidental root credit. -/
theorem canonicalTarget_iff_obligationTarget :
    Stage1Instances.THM_M_0168.BernsteinMinimalGraphTarget ↔
      BernsteinMinimalGraphTarget := by
  rfl

/-- Conditional composition into the canonical target.  The geometric
derivative-rigidity package remains an explicit premise. -/
theorem canonical_bernstein_of_derivativeRigidity
    (rigidity : DerivativeRigidity) :
    Stage1Instances.THM_M_0168.BernsteinMinimalGraphTarget :=
  canonicalTarget_iff_obligationTarget.mpr
    (bernstein_of_derivativeRigidity rigidity)

#print axioms constantPartials_to_affine
#print axioms constantPartialsToAffine_proof
#print axioms bernstein_of_derivativeRigidity
#print axioms canonicalTarget_iff_obligationTarget
#print axioms canonical_bernstein_of_derivativeRigidity

end Stage1Instances.THM_M_0168_Obligations
