import Mathlib.Analysis.Complex.Harmonic.MeanValue
import Mathlib.Analysis.Complex.Harmonic.Poisson
import Mathlib.Analysis.InnerProductSpace.PiL2

/-!
# THM-M-1141 anchor probe

This file checks the closest pinned mathlib declarations found by the anchor
audit.  They are supporting or two-dimensional local-disc results, not a proof
of the compact-subset target in `Statement.lean`.
-/

open Set Metric
open InnerProductSpace

namespace Stage1Instances.THM_M_1141.AnchorAudit

#check HarmonicOnNhd
#check HarmonicOnNhd.continuousOn
#check HarmonicOnNhd.circleAverage_eq
#check HarmonicOnNhd.circleAverage_poissonKernel_smul

example {n : Nat} {s : Set (EuclideanSpace Real (Fin n))}
    {u : EuclideanSpace Real (Fin n) → Real} (hu : HarmonicOnNhd u s) :
    ContinuousOn u s :=
  hu.continuousOn

example {f : ℂ → Real} {c : ℂ} {R : Real}
    (hf : HarmonicOnNhd f (closedBall c |R|)) :
    Real.circleAverage f c R = f c :=
  HarmonicOnNhd.circleAverage_eq hf

end Stage1Instances.THM_M_1141.AnchorAudit
