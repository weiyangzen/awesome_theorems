import Mathlib.Analysis.Asymptotics.SpecificAsymptotics
import Mathlib.Analysis.Fourier.AddCircle

/-!
# THM-M-0347: pinned mathlib anchor audit

This module checks the nearest declarations found in pinned mathlib.  Neither
declaration proves `FejerTheoremTarget`: the Fourier result adds summability of
the coefficients, while the Cesaro result assumes convergence of the sequence
being averaged.
-/

namespace Stage1Instances.THM_M_0347

open Filter Topology
open scoped BigOperators

#check @hasSum_fourier_series_of_summable
#check @Filter.Tendsto.cesaro_smul

/-- The pinned Fourier candidate has a strictly stronger coefficient-summability
hypothesis than the canonical Fejer target. -/
theorem summableFourierCandidate {T : Real} [Fact (0 < T)]
    (f : C(AddCircle T, Complex))
    (h : Summable (fourierCoeff f)) :
    HasSum (fun i : Int => fourierCoeff f i • fourier i) f := by
  exact hasSum_fourier_series_of_summable h

/-- The generic Cesaro lemma is available for real normed spaces, but requires
the input sequence to converge; it does not establish convergence of Fourier
partial sums for an arbitrary continuous function. -/
theorem cesaroCandidate {E : Type*} [NormedAddCommGroup E] [NormedSpace Real E]
    {u : Nat → E} {l : E} (h : Tendsto u atTop (nhds l)) :
    Tendsto (fun n : Nat => (n⁻¹ : Real) • ∑ i ∈ Finset.range n, u i)
      atTop (nhds l) := by
  exact h.cesaro_smul

end Stage1Instances.THM_M_0347

#print axioms Stage1Instances.THM_M_0347.summableFourierCandidate
#print axioms Stage1Instances.THM_M_0347.cesaroCandidate
