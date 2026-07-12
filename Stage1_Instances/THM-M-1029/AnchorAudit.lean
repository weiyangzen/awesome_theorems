import Mathlib.Probability.Distributions.Gaussian.Real
import Mathlib.Probability.Martingale.Basic

/-!
# THM-M-1029 anchor-audit probe

This file checks the pinned mathlib interfaces used by the frozen statement.
The pinned dependency has no Brownian-motion or quadratic-variation declaration,
so this probe deliberately does not assert Levy's characterization.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped NNReal ProbabilityTheory

namespace Stage1Instances.THM_M_1029.AnchorAudit

universe u

/-- A checked inventory of the exact interface types needed by the frozen target. -/
example {Omega : Type u} [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (F : Filtration NNReal (inferInstance : MeasurableSpace Omega))
    (X : NNReal -> Omega -> Real) : Prop :=
  Martingale X F P /\
    (forall {s t : NNReal}, s <= t ->
      Indep (F s)
        (MeasurableSpace.comap (fun omega => X t omega - X s omega) (borel Real)) P /\
      HasLaw (fun omega => X t omega - X s omega) (gaussianReal 0 (t - s)) P)

end Stage1Instances.THM_M_1029.AnchorAudit

#check Martingale
#check ProbabilityTheory.Indep
#check ProbabilityTheory.HasLaw
#check ProbabilityTheory.gaussianReal
