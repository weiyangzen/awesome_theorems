import Mathlib.Analysis.Asymptotics.SpecificAsymptotics
import Mathlib.Analysis.Fourier.AddCircle
import Mathlib.Order.Filter.AtTopBot.Interval

/-!
# THM-M-0347 proof-phase bodies

This module records the largest proof body presently obtainable from the pinned
Fourier API without assuming the Fejer-kernel estimate.  It proves the exact
canonical conclusion for the (strictly smaller) class whose Fourier
coefficients are summable.  It does not claim the unrestricted Fejer theorem.
-/

namespace Stage1Instances.THM_M_0347

open Filter Topology
open scoped BigOperators

/-- The exact definitions repeated from the frozen statement module so this
standalone proof artifact can be checked without creating build products. -/
noncomputable def symmetricFourierPartialSum {T : Real} [Fact (0 < T)]
    (f : C(AddCircle T, Complex)) (n : Nat) : C(AddCircle T, Complex) :=
  Finset.sum (Finset.Icc (-(n : Int)) (n : Int))
    (fun k => fourierCoeff f k • fourier k)

noncomputable def fejerMean {T : Real} [Fact (0 < T)]
    (f : C(AddCircle T, Complex)) (n : Nat) : C(AddCircle T, Complex) :=
  ((n + 1 : Nat) : Complex)⁻¹ •
    Finset.sum (Finset.range (n + 1)) (symmetricFourierPartialSum f)

/-- A summable bilateral Fourier series has convergent symmetric partial sums. -/
theorem tendsto_symmetricFourierPartialSum_of_summable {T : Real} [Fact (0 < T)]
    (f : C(AddCircle T, Complex)) (h : Summable (fourierCoeff f)) :
    Tendsto (symmetricFourierPartialSum f) atTop (nhds f) := by
  exact (hasSum_fourier_series_of_summable h).comp Finset.tendsto_Icc_neg

/-- Consequently the exact Fejer means converge whenever the Fourier
coefficients are summable.  This discharges the generic Cesaro bridge while
leaving the unrestricted continuous-function estimate open. -/
theorem tendsto_fejerMean_of_summable {T : Real} [Fact (0 < T)]
    (f : C(AddCircle T, Complex)) (h : Summable (fourierCoeff f)) :
    Tendsto (fejerMean f) atTop (nhds f) := by
  have hc := (tendsto_symmetricFourierPartialSum_of_summable f h).cesaro_smul
  have hc' : Tendsto
      (fun n : Nat => ((n : Real) : Complex)⁻¹ •
        Finset.sum (Finset.range n) (symmetricFourierPartialSum f))
      atTop (nhds f) := by
    convert hc using 1
    ext n
    change (((n : Real) : Complex)⁻¹ * _) = (n : Real)⁻¹ • _
    rw [Complex.real_smul]
    simp
  have hs := hc'.comp (tendsto_add_atTop_nat 1)
  convert hs using 1

end Stage1Instances.THM_M_0347

#print axioms Stage1Instances.THM_M_0347.tendsto_symmetricFourierPartialSum_of_summable
#print axioms Stage1Instances.THM_M_0347.tendsto_fejerMean_of_summable
