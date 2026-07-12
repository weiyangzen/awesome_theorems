import Statement
import ObligationTree

/-!
# THM-M-0311 proof-phase integration

This module admits the pinned mathlib `MeasureTheory.Lp.instCompleteSpace` body for each frozen
scalar branch, checks their composition through the obligation-tree theorem, and closes the exact
statement-phase target. No measure restriction or alternate notion of `Lp` is introduced.
-/

namespace Stage1Instances.THM_M_0311

open MeasureTheory
open scoped ENNReal

universe u

/-- The real-scalar frozen branch, discharged by pinned mathlib's `Lp` completeness instance. -/
theorem realL2Complete_proof : RealL2Complete.{u} := by
  intro _ _ _
  infer_instance

/-- The complex-scalar frozen branch, using the same upstream terminal instance body. -/
theorem complexL2Complete_proof : ComplexL2Complete.{u} := by
  intro _ _ _
  infer_instance

/-- Both admitted scalar bodies compose through the frozen obligation-tree certificate. -/
theorem obligationTreeTarget_proof : ObligationTreeTarget.{u} :=
  obligationTreeTarget_of_scalar_children realL2Complete_proof complexL2Complete_proof

/-- Exact proof of the statement-phase Riesz-Fischer target. -/
theorem rieszFischerTarget_proof : RieszFischerTarget.{u} := by
  intro alpha _ mu
  exact ⟨realL2Complete_proof alpha mu, complexL2Complete_proof alpha mu⟩

#check MeasureTheory.Lp.instCompleteSpace
#check rieszFischerTarget_proof
#print axioms realL2Complete_proof
#print axioms complexL2Complete_proof
#print axioms obligationTreeTarget_proof
#print axioms rieszFischerTarget_proof

end Stage1Instances.THM_M_0311
