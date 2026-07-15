import ProofBlockerCurrent

/-!
# THM-M-1045 frozen-target characterization

The existing obstruction refutes the frozen target for every supplied `WienerData`.  Consequently,
the target holds exactly when `WienerData` is empty.  The reverse implication is deliberately
vacuous and is not eligible as a proof of the mathematical Cameron-Martin theorem.
-/

noncomputable section

namespace Stage1Instances.THM_M_1045

/-- The frozen target has no nonvacuous model: it is equivalent to emptiness of `WienerData`. -/
theorem target_iff_isEmpty_wienerData : CameronMartinTarget ↔ IsEmpty WienerData := by
  constructor
  · intro target
    exact ⟨fun W => no_target_of_wienerData W target⟩
  · rintro ⟨empty⟩ W
    exact (empty W).elim

#print axioms target_iff_isEmpty_wienerData

end Stage1Instances.THM_M_1045
