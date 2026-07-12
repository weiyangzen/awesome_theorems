import Mathlib.Analysis.Fourier.AddCircle

open Filter MeasureTheory
open scoped Topology

namespace Stage1.THM_M_0346

noncomputable section

/-- The symmetric Fourier sum with frequencies `-N, ..., N` on the unit additive circle. -/
def symmetricPartialSum
    (f : Lp ℂ 2 (@AddCircle.haarAddCircle (1 : ℝ) inferInstance))
    (N : ℕ) (x : AddCircle (1 : ℝ)) : ℂ :=
  ∑ n ∈ Finset.Icc (-(N : ℤ)) (N : ℤ), fourierCoeff f n * fourier n x

/-- The exact unit-circle `L²` target meant by the repository's Carleson-theorem entry. -/
def CarlesonTarget : Prop :=
  ∀ f : Lp ℂ 2 (@AddCircle.haarAddCircle (1 : ℝ) inferInstance),
    ∀ᵐ x ∂(@AddCircle.haarAddCircle (1 : ℝ) inferInstance),
      Tendsto (fun N : ℕ ↦ symmetricPartialSum f N x) atTop (nhds (f x))

#check CarlesonTarget
#check (CarlesonTarget : Prop)

end

end Stage1.THM_M_0346
