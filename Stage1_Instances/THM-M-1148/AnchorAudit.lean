import Mathlib.Analysis.Complex.Harmonic.Poisson

/-!
# THM-M-1148: pinned anchor probes

These probes check the nearest declarations at the pinned mathlib revision.
They reproduce a harmonic function from its boundary values; they do not
construct the harmonic extension required by `PoissonIntegralFormula`.
-/

open InnerProductSpace Metric Real Set

namespace Stage1Instances.THM_M_1148.AnchorAudit

#check poissonKernel
#check poissonKernel_def
#check HarmonicOnNhd.circleAverage_poissonKernel_smul
#check HarmonicContOnCl.circleAverage_poissonKernel_smul
#check HarmonicOnNhd.circleAverage_re_herglotzRieszKernel_smul
#check HarmonicContOnCl.circleAverage_re_herglotzRieszKernel_smul

#print axioms HarmonicOnNhd.circleAverage_poissonKernel_smul
#print axioms HarmonicContOnCl.circleAverage_poissonKernel_smul

example {f : ℂ → ℝ} {c w : ℂ} {R : ℝ}
    (hf : HarmonicOnNhd f (closedBall c R)) (hw : w ∈ ball c R) :
    circleAverage (poissonKernel c w • f) c R = f w :=
  hf.circleAverage_poissonKernel_smul hw

example {f : ℂ → ℝ} {c w : ℂ} {R : ℝ}
    (hf : HarmonicContOnCl f (ball c R)) (hw : w ∈ ball c R) :
    circleAverage (poissonKernel c w • f) c R = f w :=
  hf.circleAverage_poissonKernel_smul hw

end Stage1Instances.THM_M_1148.AnchorAudit
