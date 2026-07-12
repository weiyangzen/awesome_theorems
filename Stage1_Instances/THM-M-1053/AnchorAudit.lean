import Mathlib.Dynamics.BirkhoffSum.Average
import Mathlib.Dynamics.Ergodic.Function
import Mathlib.MeasureTheory.Integral.Bochner.Basic

open Filter Function MeasureTheory

namespace Stage1.THM_M_1053.AnchorAudit

universe u

/-- Verbatim copy of the frozen target's average, used because dossier modules are checked as
standalone Lean sources rather than installed library modules. -/
noncomputable def auditedTimeAverage {X : Type u} (T : X → X) (f : X → ℝ)
    (n : ℕ) (x : X) : ℝ :=
  (n : ℝ)⁻¹ * ∑ k ∈ Finset.range n, f ((T^[k]) x)

/-- The frozen average encoding is definitionally the pinned mathlib `birkhoffAverage` encoding. -/
theorem auditedTimeAverage_eq_birkhoffAverage {X : Type u} (T : X → X) (f : X → ℝ)
    (n : ℕ) (x : X) :
    auditedTimeAverage T f n x = birkhoffAverage ℝ T f n x := by
  rfl

-- These are genuine adjacent anchors, but none asserts pointwise convergence.
#check birkhoffAverage_apply_sub_birkhoffAverage
#check MeasurePreserving.integrable_comp_emb
#check Ergodic.ae_eq_const_of_ae_eq_comp_ae

#print axioms auditedTimeAverage_eq_birkhoffAverage

end Stage1.THM_M_1053.AnchorAudit
