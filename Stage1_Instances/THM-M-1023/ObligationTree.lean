import Statement

/-!
# THM-M-1023 conditional obligation composition

This module checks only how the two mathematical directions compose into the
exact frozen biconditional. Both directions remain explicit assumptions.
-/

noncomputable section

open MeasureTheory

namespace Stage1Instances.THM_M_1023

/-- Complete forward direction, including existence and uniqueness of the
selected Levy-Khinchin data. -/
def ForwardPackage : Prop :=
  forall mu : Measure Real,
    IsInfinitelyDivisible mu -> HasLevyKhintchineRepresentation mu

/-- Complete converse direction for the same truncation and Fourier-sign
convention. -/
def ReversePackage : Prop :=
  forall mu : Measure Real,
    HasLevyKhintchineRepresentation mu -> IsInfinitelyDivisible mu

/-- Kernel-checked composition boundary for the frozen root. -/
theorem root_of_directionPackages
    (forward : ForwardPackage) (reverse : ReversePackage) :
    InfinitelyDivisibleIffLevyKhintchine := by
  intro mu
  exact ⟨forward mu, reverse mu⟩

#print axioms root_of_directionPackages

end Stage1Instances.THM_M_1023
