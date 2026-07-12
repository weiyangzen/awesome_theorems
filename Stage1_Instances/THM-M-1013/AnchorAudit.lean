import Mathlib.MeasureTheory.Measure.LevyConvergence
import Mathlib.Analysis.InnerProductSpace.PiL2

/-!
# THM-M-1013 anchor audit

This file checks that the repository-local Stage1 candidate at the frozen base
revision has exactly the measure-level biconditional frozen by `Statement.lean`.
It is candidate evidence for the anchor-audit phase, not acceptance of a proof
or theorem-completion gate.
-/

open Filter MeasureTheory
open scoped Topology

namespace Stage1Instances.THM_M_1013.AnchorAudit

noncomputable section

abbrev Vector (d : Nat) := EuclideanSpace Real (Fin d)

def projection {d : Nat} (t x : Vector d) : Real := inner Real x t

lemma continuous_projection {d : Nat} (t : Vector d) : Continuous (projection t) := by
  unfold projection
  exact continuous_id.inner continuous_const

lemma projection_charFun_one_measure {d : Nat} (mu : Measure (Vector d))
    (t : Vector d) :
    charFun (mu.map (projection t)) 1 = charFun mu t := by
  rw [charFun_apply_real, charFun_apply]
  rw [integral_map ((continuous_projection t).aemeasurable) (by fun_prop)]
  simp [projection]

/-- Exact-type wrapper around the immutable repository-local candidate. -/
theorem repoLocalCandidate :
    forall (d : Nat) (mu : Nat -> ProbabilityMeasure (Vector d))
      (mu0 : ProbabilityMeasure (Vector d)),
      Tendsto mu atTop (nhds mu0) <->
        forall t : Vector d,
          Tendsto
            (fun n => (mu n).map ((continuous_projection t).measurable.aemeasurable))
            atTop
            (nhds (mu0.map ((continuous_projection t).measurable.aemeasurable))) := by
  intro d mu mu0
  constructor
  · intro h t
    exact ProbabilityMeasure.tendsto_map_of_tendsto_of_continuous
      mu mu0 h (continuous_projection t)
  · intro h
    apply ProbabilityMeasure.tendsto_iff_tendsto_charFun.mpr
    intro t
    have hchar := (ProbabilityMeasure.tendsto_iff_tendsto_charFun.mp (h t)) 1
    simpa only [ProbabilityMeasure.toMeasure_map, projection_charFun_one_measure]
      using hchar

#check repoLocalCandidate
#print axioms repoLocalCandidate

end

end Stage1Instances.THM_M_1013.AnchorAudit
