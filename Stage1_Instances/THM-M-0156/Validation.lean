import Statement

/-!
# THM-M-0156 independent validation probe

This module reconstructs the frozen rectangular divergence theorem directly
from the pinned mathlib declaration without importing `Proof`. It is a local
implementation-diverse probe, not a distinct-runner attestation.
-/

noncomputable section

open Finset MeasureTheory Set
open scoped BigOperators

namespace Stage1Instances.THM_M_0156.Validation

open Stage1Instances.THM_M_0156

/-- Independent reconstruction of the exact frozen target. -/
theorem independentlyReconstructedDivergenceTheorem : DivergenceTheoremTarget := by
  intro n a b hab f f' hcont hderiv hint
  exact MeasureTheory.integral_divergence_of_hasFDerivAt_off_countable
    a b hab f f' (∅ : Set (Euclidean n)) Set.countable_empty hcont
      (fun x hx => hderiv x hx.1) hint

#print axioms independentlyReconstructedDivergenceTheorem
#print axioms MeasureTheory.integral_divergence_of_hasFDerivAt_off_countable

end Stage1Instances.THM_M_0156.Validation
