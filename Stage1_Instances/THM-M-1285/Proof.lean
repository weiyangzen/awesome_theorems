import Statement

/-!
# THM-M-1285 proof-lane lemmas

These lemmas discharge the radiality and radial-antitonicity obligations for
any candidate defined by a one-variable decreasing radial profile.  They do
not construct the profile or prove equimeasurability.
-/

namespace Stage1Instances.THM_M_1285

/-- A function obtained by applying a profile to the norm is radial. -/
theorem isRadial_profile {n : Nat} (profile : ℝ → ENNReal) :
    IsRadial (fun x : Euclidean n => profile ‖x‖) := by
  intro x y hxy
  exact congrArg profile hxy

/-- An antitone profile gives a radially nonincreasing function. -/
theorem isRadiallyNonincreasing_profile {n : Nat} (profile : ℝ → ENNReal)
    (hprofile : Antitone profile) :
    IsRadiallyNonincreasing (fun x : Euclidean n => profile ‖x‖) := by
  intro x y hxy
  exact hprofile hxy

/-- A measurable profile gives a measurable radial candidate. -/
theorem measurable_profile {n : Nat} (profile : ℝ → ENNReal)
    (hprofile : Measurable profile) :
    Measurable (fun x : Euclidean n => profile ‖x‖) := by
  exact hprofile.comp measurable_norm

#print axioms isRadial_profile
#print axioms isRadiallyNonincreasing_profile
#print axioms measurable_profile

end Stage1Instances.THM_M_1285
