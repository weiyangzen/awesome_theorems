/-!
# THM-M-1061 differential validation probes

This file is appended after `Statement.lean` by the validation runner.  It
deliberately imports neither `Proof` nor `ObligationTree` and reconstructs only
two partial order-theoretic/boundary results.  It does not state or prove the
open Varadhan root, and a same-worker replay is not independent release
evidence.
-/

namespace Stage1Instances.THM_M_1061.Validation

open Filter MeasureTheory
open Set Topology
open scoped ENNReal

universe u

variable {X : Type u} [MeasurableSpace X] [TopologicalSpace X]
variable {mu : Nat -> Measure X} {a : Nat -> Real} {I : X -> ENNReal}

/-- Independently project the exact open-set half of the frozen full-LDP
interface.  This is not the missing exponential-integral localization lemma. -/
theorem independentlyProjectedOpenLower
    (h : Stage1Instances.THM_M_1061.SatisfiesLDP mu a I) :
    forall G : Set X, IsOpen G ->
      -⨅ x ∈ G, (I x : EReal) <=
        liminf (fun n => (a n : EReal) * ENNReal.log (mu n G)) atTop :=
  h.2.2.2.2

/-- Independently reconstruct the generic conditional limit merge.  Its two
analytic premises remain assumptions and therefore provide no root closure. -/
theorem independentlyMergedLiminfLimsup
    {v : Nat -> EReal} {s : EReal}
    (hlower : s <= liminf v atTop)
    (hupper : limsup v atTop <= s) :
    Tendsto v atTop (nhds s) :=
  tendsto_of_le_liminf_of_limsup_le hlower hupper

#check independentlyProjectedOpenLower
#check independentlyMergedLiminfLimsup

#print axioms independentlyProjectedOpenLower
#print axioms independentlyMergedLiminfLimsup

end Stage1Instances.THM_M_1061.Validation
