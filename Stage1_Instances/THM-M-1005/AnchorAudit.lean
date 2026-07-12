import Mathlib.Probability.Martingale.OptionalStopping

/-!
# THM-M-1005 pinned anchor probes

The frozen target is the strong finite-horizon `L^p` estimate.  The pinned
library theorem checked here is the related weak maximal inequality for a
nonnegative submartingale; this file deliberately does not assert a bridge
from that theorem to the canonical target.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal NNReal MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_1005.AnchorAudit

universe u

/-- The exact shape supplied by the pinned mathlib declaration. -/
def PinnedWeakMaximalShape : Prop :=
  forall (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
    [IsFiniteMeasure mu] (G : Filtration Nat mOmega) (f : Nat -> Omega -> Real),
      Submartingale f G mu -> 0 <= f -> forall (epsilon : NNReal) (n : Nat),
        epsilon * mu {omega | (epsilon : Real) <=
          (Finset.range (n + 1)).sup' Finset.nonempty_range_add_one (fun k => f k omega)} <=
          ENNReal.ofReal
            (∫ omega in {omega | (epsilon : Real) <=
              (Finset.range (n + 1)).sup' Finset.nonempty_range_add_one
                (fun k => f k omega)}, f n omega ∂mu)

/-- A direct checked wrapper around the related pinned theorem. -/
theorem pinnedWeakMaximal : PinnedWeakMaximalShape.{u} := by
  intro Omega _ mu _ G f hsub hnonneg epsilon n
  exact MeasureTheory.maximal_ineq (𝒢 := G) (f := f) hsub hnonneg n

#check MeasureTheory.maximal_ineq
#check MeasureTheory.smul_le_stoppedValue_hittingBtwn
#check MeasureTheory.Submartingale.expected_stoppedValue_mono
#check MeasureTheory.Martingale.submartingale
#check MeasureTheory.eLpNorm
#print axioms pinnedWeakMaximal

end Stage1Instances.THM_M_1005.AnchorAudit
