import Statement

/-!
# THM-M-1055 conditional obligation composition

This module checks the final composition boundary. The invariant-limit package
is an explicit premise; no pointwise ergodic theorem is asserted here.
-/

noncomputable section

open Filter MeasureTheory
open scoped Topology

namespace Stage1Instances.THM_M_1055

universe u

/-- The analytic output required before the exact ergodic specialization can close. -/
def InvariantLimitPackage : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega] (mu : Measure Omega)
    [IsProbabilityMeasure mu] (T : Omega → Omega) (f : Omega → ℝ),
    Ergodic T mu → Integrable f mu →
      ∃ g : Omega → ℝ,
        (∀ᵐ x ∂mu, Tendsto (fun n : ℕ ↦ birkhoffAverage ℝ T f n x) atTop (nhds (g x))) ∧
        g =ᵐ[mu] fun _ ↦ ∫ y, f y ∂mu

/-- Checked final composition: pointwise convergence plus ergodic identification
of the limit gives the exact frozen target. -/
theorem root_of_invariantLimitPackage
    (limits : InvariantLimitPackage.{u}) : BirkhoffErgodicTarget.{u} := by
  intro Omega _ mu _ T f hT hf
  obtain ⟨g, hconv, hconst⟩ := limits Omega mu T f hT hf
  filter_upwards [hconv, hconst] with x hx hgx
  simpa [hgx] using hx

#print axioms root_of_invariantLimitPackage

end Stage1Instances.THM_M_1055
