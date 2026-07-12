import Mathlib.Data.Complex.Basic
import Mathlib.Algebra.Algebra.Spectrum.Basic

/-!
# THM-M-1550 anchor elaboration audit

This file checks the pinned mathlib terminal body that can discharge the
conjugation-to-spectrum leaf of the frozen statement. It does not construct a
conjugating evolution from the Lax differential equation.
-/

noncomputable section

namespace Stage1Instances.THM_M_1550.AnchorAudit

universe u

/-- Exact candidate shape needed after unpacking `ConjugatesAt`. -/
theorem spectrum_eq_of_units_conjugate {A : Type u} [Ring A] [Algebra Complex A]
    (a : A) (U : Aˣ) :
    spectrum Complex ((U : A) * a * ((U⁻¹ : Aˣ) : A)) = spectrum Complex a := by
  exact spectrum.units_conjugate

end Stage1Instances.THM_M_1550.AnchorAudit

#check @spectrum.units_conjugate
