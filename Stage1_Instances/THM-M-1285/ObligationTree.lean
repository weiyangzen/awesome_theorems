import Statement

/-!
# THM-M-1285 conditional obligation composition

This file checks only the final composition boundary of the frozen proof
architecture. The construction package is an explicit premise, not a proof of
Schwarz rearrangement.
-/

namespace Stage1Instances.THM_M_1285

open MeasureTheory
open scoped ENNReal

/-- The output required from the distribution, inverse-radius, and witness
construction obligations. -/
def SchwarzConstructionPackage : Prop :=
  ∀ (n : Nat), 0 < n → ∀ f : Euclidean n → ENNReal,
    Measurable f →
      (∀ t : ENNReal, 0 < t → volume {x | t < f x} ≠ ∞) →
        ∃ fstar : Euclidean n → ENNReal,
          Measurable fstar ∧ IsRadial fstar ∧
            IsRadiallyNonincreasing fstar ∧ Equimeasurable f fstar

/-- Checked conditional composition into the exact frozen root. -/
theorem schwarzRearrangementTarget_of_construction
    (construction : SchwarzConstructionPackage) :
    SchwarzRearrangementTarget := by
  intro n hn f hf hfinite
  exact construction n hn f hf hfinite

#print axioms schwarzRearrangementTarget_of_construction

end Stage1Instances.THM_M_1285
