import KunnethStatement
import Mathlib.Algebra.Category.ModuleCat.Products

/-!
# Direct-sum grading proof bodies for THM-M-0005

This module checks the exact relationship between the subtraction-free `TorDegrees` index used by
the frozen target and the conventional total degree one lower. It supplies only grading and
reindexing bodies; it does not construct the missing Kunneth maps or exact sequence.
-/

noncomputable section

open AlgebraicTopology CategoryTheory CategoryTheory.Limits
open CategoryTheory.MonoidalCategory

universe u

namespace AwesomeTheorems.Stage1.THM_M_0005.ProofDirectSum20260715Head5bb51543Slot21

open AwesomeTheorems.Stage1.THM_M_0005

/-- In positive total degree, `p + q + 1 = n + 1` is exactly `p + q = n`. -/
def torDegreesSuccEquivTensorDegrees (n : ℕ) :
    TorDegrees (n + 1) ≃ TensorDegrees n where
  toFun pq := ⟨pq.1, by omega⟩
  invFun pq := ⟨pq.1, by omega⟩
  left_inv pq := Subtype.ext rfl
  right_inv pq := Subtype.ext rfl

@[simp]
theorem torDegreesSuccEquivTensorDegrees_apply (n : ℕ) (pq : TorDegrees (n + 1)) :
    (torDegreesSuccEquivTensorDegrees n pq).1 = pq.1 :=
  rfl

@[simp]
theorem torDegreesSuccEquivTensorDegrees_symm_apply (n : ℕ) (pq : TensorDegrees n) :
    ((torDegreesSuccEquivTensorDegrees n).symm pq).1 = pq.1 :=
  rfl

/-- There are no `Tor₁` bidegrees in total degree zero. -/
theorem torDegrees_zero_empty : IsEmpty (TorDegrees 0) := by
  constructor
  intro pq
  omega

/-- Consequently, the degree-zero right-hand Kunneth term is a zero module. -/
theorem torTerm_zero_isZero
    (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R]
    (X Y : TopCat.{u}) :
    IsZero (TorTerm R X Y 0) := by
  letI : IsEmpty (TorDegrees 0) := torDegrees_zero_empty
  let Z : TorDegrees 0 → ModuleCat.{u} R := fun pq ↦
    ((CategoryTheory.Tor (ModuleCat.{u} R) 1).obj
      (Homology R pq.1.1 X)).obj (Homology R pq.1.2 Y)
  apply (ModuleCat.coprodIsoDirectSum Z).isZero_iff.mpr
  exact ModuleCat.isZero_of_subsingleton _

/-- The right-hand Kunneth term in degree `n + 1`, reindexed without subtraction. -/
def torTermSuccIso
    (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R]
    (X Y : TopCat.{u}) (n : ℕ) :
    TorTerm R X Y (n + 1) ≅
      ∐ fun pq : TensorDegrees n ↦ ((CategoryTheory.Tor (ModuleCat.{u} R) 1).obj
        (Homology R pq.1.1 X)).obj (Homology R pq.1.2 Y) :=
  Sigma.whiskerEquiv (torDegreesSuccEquivTensorDegrees n) (fun pq ↦ by
    change ((CategoryTheory.Tor (ModuleCat.{u} R) 1).obj
        (Homology R pq.1.1 X)).obj (Homology R pq.1.2 Y) ≅
      ((CategoryTheory.Tor (ModuleCat.{u} R) 1).obj
        (Homology R pq.1.1 X)).obj (Homology R pq.1.2 Y)
    exact Iso.refl _)

/-- The reindexing isomorphism sends each canonical injection to the same bidegree injection. -/
@[reassoc (attr := simp)]
theorem torTermSuccIso_hom_ι
    (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R]
    (X Y : TopCat.{u}) (n : ℕ) (pq : TorDegrees (n + 1)) :
    Sigma.ι (fun pq : TorDegrees (n + 1) ↦
        ((CategoryTheory.Tor (ModuleCat.{u} R) 1).obj
          (Homology R pq.1.1 X)).obj (Homology R pq.1.2 Y)) pq ≫
      (torTermSuccIso R X Y n).hom =
    Sigma.ι (fun pq : TensorDegrees n ↦
      ((CategoryTheory.Tor (ModuleCat.{u} R) 1).obj
        (Homology R pq.1.1 X)).obj (Homology R pq.1.2 Y))
      (torDegreesSuccEquivTensorDegrees n pq) := by
  simp [torTermSuccIso]

/-- The inverse reindexing also preserves every canonical bidegree injection. -/
@[reassoc (attr := simp)]
theorem torTermSuccIso_inv_ι
    (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R]
    (X Y : TopCat.{u}) (n : ℕ) (pq : TensorDegrees n) :
    Sigma.ι (fun pq : TensorDegrees n ↦
        ((CategoryTheory.Tor (ModuleCat.{u} R) 1).obj
          (Homology R pq.1.1 X)).obj (Homology R pq.1.2 Y)) pq ≫
      (torTermSuccIso R X Y n).inv =
    Sigma.ι (fun pq : TorDegrees (n + 1) ↦
      ((CategoryTheory.Tor (ModuleCat.{u} R) 1).obj
        (Homology R pq.1.1 X)).obj (Homology R pq.1.2 Y))
      ((torDegreesSuccEquivTensorDegrees n).symm pq) := by
  rw [show (torTermSuccIso R X Y n).inv =
      Sigma.map' (torDegreesSuccEquivTensorDegrees n).symm (fun pq : TensorDegrees n ↦
        𝟙 (((CategoryTheory.Tor (ModuleCat.{u} R) 1).obj
          (Homology R pq.1.1 X)).obj (Homology R pq.1.2 Y))) by rfl]
  rw [Sigma.ι_comp_map']
  simp

#print axioms torDegreesSuccEquivTensorDegrees
#print axioms torDegreesSuccEquivTensorDegrees_apply
#print axioms torDegreesSuccEquivTensorDegrees_symm_apply
#print axioms torDegrees_zero_empty
#print axioms torTerm_zero_isZero
#print axioms torTermSuccIso
#print axioms torTermSuccIso_hom_ι
#print axioms torTermSuccIso_inv_ι

end AwesomeTheorems.Stage1.THM_M_0005.ProofDirectSum20260715Head5bb51543Slot21
