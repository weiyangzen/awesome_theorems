import Mathlib.Dynamics.BirkhoffSum.QuasiMeasurePreserving
import Mathlib.Dynamics.BirkhoffSum.NormedSpace
import Mathlib.Dynamics.Ergodic.Function
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.Analysis.InnerProductSpace.MeanErgodic

/-!
# THM-M-1522 anchor audit

Checked names for the pinned mathlib support surface. This file deliberately
does not assert the pointwise ergodic theorem.
-/

open Filter MeasureTheory
open scoped Topology

namespace Stage1Instances.THM_M_1522.AnchorAudit

def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

def externalCandidateRevision : String :=
  "fc06094ca0506d8d74eba8b45b34882ce5930bf4"

def externalCandidateImported : Bool := false

theorem pinnedMathlibRevision_eq :
    pinnedMathlibRevision = "8a178386ffc0f5fef0b77738bb5449d50efeea95" := rfl

theorem externalCandidateRevision_eq :
    externalCandidateRevision = "fc06094ca0506d8d74eba8b45b34882ce5930bf4" := rfl

theorem externalCandidateImported_eq_false :
    externalCandidateImported = false := rfl

#check birkhoffSum
#check birkhoffAverage
#check MeasurePreserving
#check Ergodic
#check Integrable
#check Measure.QuasiMeasurePreserving.birkhoffAverage_ae_eq_of_ae_eq
#check Ergodic.ae_eq_const_of_ae_eq_comp_ae
#check ContinuousLinearMap.tendsto_birkhoffAverage_orthogonalProjection

end Stage1Instances.THM_M_1522.AnchorAudit
