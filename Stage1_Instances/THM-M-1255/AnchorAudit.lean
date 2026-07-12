import Mathlib.Analysis.Distribution.TemperedDistribution
import Mathlib.RingTheory.MvPolynomial.Basic

/-!
# THM-M-1255 anchor audit probes

This file checks the useful declarations present in the pinned mathlib revision.
It deliberately contains no Malgrange-Ehrenpreis existence theorem.
-/

noncomputable section

open scoped SchwartzMap

namespace Stage1Instances.THM_M_1255.AnchorAudit

universe u

abbrev Space (ι : Type u) [Fintype ι] := EuclideanSpace ℝ ι
abbrev TemperedDist (ι : Type u) [Fintype ι] := 𝓢'(Space ι, ℂ)

/-- The pinned Dirac anchor has the evaluation behavior required at the root equation. -/
theorem delta_zero_apply
    {ι : Type u} [Fintype ι] (f : 𝓢(Space ι, ℂ)) :
    TemperedDistribution.delta (0 : Space ι) f = f 0 :=
  TemperedDistribution.delta_apply (0 : Space ι) f

/-- The pinned continuous derivative operator reduces to mathlib's line derivative. -/
theorem lineDerivOpCLM_apply
    {ι : Type u} [Fintype ι] (v : Space ι) (T : TemperedDist ι) :
    LineDeriv.lineDerivOpCLM ℂ (TemperedDist ι) v T = LineDeriv.lineDerivOp v T :=
  LineDeriv.lineDerivOpCLM_apply v T

/-- The pinned Fourier convention for a distributional directional derivative. -/
theorem fourier_lineDerivOp_eq
    {ι : Type u} [Fintype ι] (v : Space ι) (T : TemperedDist ι) :
    FourierTransform.fourier (LineDeriv.lineDerivOp v T) =
      (2 * Real.pi * Complex.I) •
        TemperedDistribution.smulLeftCLM ℂ (fun x : Space ι => (inner ℝ x v : ℂ))
          (FourierTransform.fourier T) :=
  TemperedDistribution.fourier_lineDerivOp_eq T v

-- Object-layer probes. None has the terminal fundamental-solution quantifiers.
#check MvPolynomial
#check MvPolynomial.X
#check TemperedDistribution.delta
#check TemperedDistribution.delta_apply
#check LineDeriv.lineDerivOpCLM
#check LineDeriv.lineDerivOpCLM_apply
#check FourierTransform.fourier
#check TemperedDistribution.fourier_lineDerivOp_eq
#check TemperedDistribution.smulLeftCLM

end Stage1Instances.THM_M_1255.AnchorAudit
