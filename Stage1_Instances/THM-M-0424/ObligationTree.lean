import Mathlib.Algebra.BrauerGroup.Defs
import Mathlib.RingTheory.TensorProduct.Basic

/-!
# THM-M-0424 conditional obligation composition

This module checks that the frozen terminal package has exactly the canonical
root type.  It deliberately supplies no inhabitant of that package: all
substantive Brauer-group construction obligations remain open.
-/

noncomputable section

namespace Stage1Instances.THM_M_0424

universe u v

abbrev BrauerClass (K : Type u) [Field K] (A : CSA.{u, v} K) : BrauerGroup K :=
  Quotient.mk (Brauer.CSA_Setoid K) A

structure BrauerGroupLawData (K : Type u) [Field K] where
  tensorRep : CSA.{u, v} K -> CSA.{u, v} K -> CSA.{u, v} K
  tensorRep_equiv : forall A B : CSA.{u, v} K,
    Nonempty ((tensorRep A B : Type v) ≃ₐ[K] TensorProduct K A B)
  tensor_congr : forall {A A' B B' : CSA.{u, v} K},
    IsBrauerEquivalent A A' -> IsBrauerEquivalent B B' ->
      IsBrauerEquivalent (tensorRep A B) (tensorRep A' B')
  oneRep : CSA.{u, v} K
  oneRep_equiv_base : Nonempty ((oneRep : Type v) ≃ₐ[K] K)
  invRep : CSA.{u, v} K -> CSA.{u, v} K
  invRep_equiv_opposite : forall A : CSA.{u, v} K,
    Nonempty ((invRep A : Type v) ≃ₐ[K] MulOpposite A)
  [commGroup : CommGroup (BrauerGroup K)]
  mul_mk : forall A B : CSA.{u, v} K,
    BrauerClass K A * BrauerClass K B = BrauerClass K (tensorRep A B)
  one_mk : (1 : BrauerGroup K) = BrauerClass K oneRep
  inv_mk : forall A : CSA.{u, v} K,
    (BrauerClass K A)⁻¹ = BrauerClass K (invRep A)

def BrauerGroupStatement : Prop :=
  forall (K : Type u) [Field K], Nonempty (BrauerGroupLawData.{u, v} K)

/-- Exact conditional composition certificate for the frozen root. -/
theorem brauerGroupStatement_of_lawData
    (h : forall (K : Type u) [Field K],
      Nonempty (BrauerGroupLawData.{u, v} K)) :
    BrauerGroupStatement.{u, v} := by
  exact h

#check BrauerGroupLawData.tensorRep_equiv
#check BrauerGroupLawData.tensor_congr
#check BrauerGroupLawData.oneRep_equiv_base
#check BrauerGroupLawData.invRep_equiv_opposite
#check BrauerGroupLawData.mul_mk
#check BrauerGroupLawData.one_mk
#check BrauerGroupLawData.inv_mk
#print axioms brauerGroupStatement_of_lawData

end Stage1Instances.THM_M_0424
