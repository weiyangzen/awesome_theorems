import Statement
import ObligationTree
import Mathlib.GroupTheory.Descent

/-!
# THM-M-0450 proof execution

This module supplies two checked bridges for the frozen Mordell-Weil target:

* finite generation transports across an additive equivalence;
* the generic descent packages assemble directly into the canonical
  `Stage1Instances.THM_M_0450.ExactTarget` imported from `Statement.lean`.

The arithmetic inputs themselves remain open.  In particular, this file does
not prove weak Mordell-Weil or construct an elliptic height package.
-/

noncomputable section

universe u

namespace Stage1Instances.THM_M_0450.Proof

open Stage1Instances.THM_M_0450

/-- Finite generation is invariant under an additive equivalence.  This is the
checked group-theoretic part of the affine/Jacobian model transport. -/
theorem fg_iff_of_addEquiv {A B : Type*} [AddGroup A] [AddGroup B]
    (e : A ≃+ B) : AddGroup.FG A ↔ AddGroup.FG B := by
  constructor
  · intro hA
    letI : AddGroup.FG A := hA
    exact AddGroup.fg_of_surjective (f := e.toAddMonoidHom) e.surjective
  · intro hB
    letI : AddGroup.FG B := hB
    exact AddGroup.fg_of_surjective (f := e.symm.toAddMonoidHom) e.symm.surjective

/-- Finite index is invariant under an additive equivalence. -/
theorem finiteIndex_iff_of_addEquiv {A B : Type*} [AddGroup A] [AddGroup B]
    (e : A ≃+ B) (H : AddSubgroup B) :
    (H.comap e.toAddMonoidHom).FiniteIndex ↔ H.FiniteIndex := by
  rw [AddSubgroup.finiteIndex_iff, AddSubgroup.finiteIndex_iff,
    H.index_comap_of_surjective e.surjective]

/-- The doubling subgroup is carried to the doubling subgroup by every
additive equivalence. -/
theorem comap_doubling_range {A B : Type*} [AddCommGroup A] [AddCommGroup B]
    (e : A ≃+ B) :
    (nsmulAddMonoidHom (α := B) 2).range.comap e.toAddMonoidHom =
      (nsmulAddMonoidHom (α := A) 2).range := by
  ext a
  constructor
  · rintro ⟨b, hb⟩
    refine ⟨e.symm b, ?_⟩
    apply e.injective
    simpa using hb
  · rintro ⟨a', ha'⟩
    refine ⟨e a', ?_⟩
    simpa using congrArg e ha'

/-- The weak-Mordell-Weil finite-index condition transports across an additive
equivalence, including the exact doubling subgroups on both sides. -/
theorem doubling_finiteIndex_iff_of_addEquiv
    {A B : Type*} [AddCommGroup A] [AddCommGroup B] (e : A ≃+ B) :
    (nsmulAddMonoidHom (α := A) 2).range.FiniteIndex ↔
      (nsmulAddMonoidHom (α := B) 2).range.FiniteIndex := by
  rw [← finiteIndex_iff_of_addEquiv e, comap_doubling_range]

/-- Pulling a height back along an equivalence preserves the Northcott
property. -/
theorem northcott_comp_addEquiv {A B : Type*} [AddGroup A] [AddGroup B]
    (e : A ≃+ B) (h : B -> Real) [Northcott h] : Northcott (h ∘ e) where
  finite_le bound := by
    change (e ⁻¹' {b : B | h b <= bound}).Finite
    exact (Northcott.finite_le bound).preimage e.injective.injOn

/-- The nonnegativity part of a descent height package pulls back along an
additive equivalence. -/
theorem nonnegative_comp_addEquiv {A B : Type*} [AddGroup A] [AddGroup B]
    (e : A ≃+ B) (h : B -> Real) (hnonnegative : forall b, 0 <= h b) :
    forall a, 0 <= (h ∘ e) a := by
  intro a
  exact hnonnegative (e a)

/-- The approximate parallelogram law is unchanged by pullback along an
additive equivalence. -/
theorem parallelogram_comp_addEquiv {A B : Type*} [AddCommGroup A]
    [AddCommGroup B] (e : A ≃+ B) (h : B -> Real) (C : Real)
    (hparallelogram :
      forall x y, |h (x + y) + h (x - y) - 2 * (h x + h y)| <= C) :
    forall x y,
      |(h ∘ e) (x + y) + (h ∘ e) (x - y) -
        2 * ((h ∘ e) x + (h ∘ e) y)| <= C := by
  intro x y
  simpa only [Function.comp_apply, e.map_add, e.map_sub] using hparallelogram (e x) (e y)

/-- The pinned Jacobian-to-affine additive equivalence preserves the exact
finite-generation conclusion used by the frozen target. -/
theorem jacobian_fg_iff_affine_fg {K : Type u} [Field K] [DecidableEq K]
    (E : WeierstrassCurve K) [E.IsElliptic] :
    AddGroup.FG E.toJacobian.Point ↔ AddGroup.FG E.toAffine.Point := by
  exact fg_iff_of_addEquiv (WeierstrassCurve.Jacobian.Point.toAffineAddEquiv E.toJacobian)

/-- The same pinned point-model equivalence preserves the finite-index
doubling condition required by weak Mordell-Weil descent. -/
theorem jacobian_doubling_finiteIndex_iff_affine
    {K : Type u} [Field K] [DecidableEq K]
    (E : WeierstrassCurve K) [E.IsElliptic] :
    (nsmulAddMonoidHom (α := E.toJacobian.Point) 2).range.FiniteIndex ↔
      (nsmulAddMonoidHom (α := E.toAffine.Point) 2).range.FiniteIndex := by
  exact doubling_finiteIndex_iff_of_addEquiv
    (WeierstrassCurve.Jacobian.Point.toAffineAddEquiv E.toJacobian)

/-- Exact canonical-root assembly.  Unlike the earlier standalone obligation
module, this theorem consumes that module's frozen package types but concludes
the imported `ExactTarget` rather than a namespace-local duplicate. -/
theorem exactTarget_of_descent_packages
    (weakMW : forall (K : Type u) [Field K] [NumberField K]
      (E : WeierstrassCurve K), E.IsElliptic -> ObligationTree.WeakMordellWeil K E)
    (heights : forall (K : Type u) [Field K] [NumberField K]
      (E : WeierstrassCurve K), E.IsElliptic -> ObligationTree.HeightPackage K E) :
    ExactTarget.{u} := by
  intro K _ _ E hE
  let package := heights K E hE
  letI : Northcott package.height := package.northcott
  exact AddCommGroup.fg_of_descent' (weakMW K E hE)
    package.nonnegative package.parallelogram

#print axioms fg_iff_of_addEquiv
#print axioms finiteIndex_iff_of_addEquiv
#print axioms comap_doubling_range
#print axioms doubling_finiteIndex_iff_of_addEquiv
#print axioms northcott_comp_addEquiv
#print axioms nonnegative_comp_addEquiv
#print axioms parallelogram_comp_addEquiv
#print axioms jacobian_fg_iff_affine_fg
#print axioms jacobian_doubling_finiteIndex_iff_affine
#print axioms exactTarget_of_descent_packages

end Stage1Instances.THM_M_0450.Proof
