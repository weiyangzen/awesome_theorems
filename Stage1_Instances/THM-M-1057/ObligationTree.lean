import Statement

/-!
# THM-M-1057 conditional obligation composition

This module kernel-checks the final child-to-root composition.  The pointwise
limit package is an explicit premise; this file does not prove Kingman's
subadditive ergodic theorem.
-/

noncomputable section

open Filter Function MeasureTheory Set
open scoped MeasureTheory Topology

namespace Stage1Instances.THM_M_1057

universe u

/-- Output required from the maximal-inequality, convergence, invariance, and
ergodic-identification branches.  Keeping the witness `g` explicit prevents
the final wrapper from hiding those substantive obligations. -/
def PointwiseLimitPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega] (P : KingmanData Omega),
    exists g : Omega -> Real,
      (∀ᵐ omega ∂P.measure,
        Tendsto (fun n => normalizedProcess P n omega) atTop (𝓝 (g omega))) /\
      g ∘ P.transformation =ᵐ[P.measure] g /\
      g =ᵐ[P.measure] fun _ => kingmanValue P

/-- Checked composition of an explicitly supplied pointwise-limit package into
the exact frozen root.  This proves only the implication shown in its type. -/
theorem root_of_pointwiseLimitPackage
    (limitPackage : PointwiseLimitPackage.{u}) : KingmanTarget.{u} := by
  intro Omega _ P
  obtain ⟨g, hlimit, _hinvariant, hvalue⟩ := limitPackage Omega P
  filter_upwards [hlimit, hvalue] with omega hconverges hidentifies
  simpa [hidentifies] using hconverges

#print axioms root_of_pointwiseLimitPackage

end Stage1Instances.THM_M_1057
