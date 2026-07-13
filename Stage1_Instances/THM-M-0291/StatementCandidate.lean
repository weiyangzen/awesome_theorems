import Mathlib.Analysis.Fourier.AddCircle

/-!
# THM-M-0291 source-literal elaboration candidate

This file is an elaboration probe for one real-valued, fixed-`2 * pi` encoding suggested by the
intake source lead. It is deliberately namespaced as a candidate because the source-to-`AddCircle`
carrier, complex Fourier normalization, real-part projection, indexing, and topology transports
have not been independently approved. It is not an accepted canonical target or a proof of
Fejer's theorem.
-/

namespace Stage1Instances.THM_M_0291.Candidate

open Filter Topology
open scoped BigOperators ComplexConjugate Real

noncomputable section

local instance instTwoPiPos : Fact (0 < 2 * Real.pi) := Fact.mk Real.two_pi_pos

/-- Regard a real-valued continuous map as complex-valued without changing its domain. -/
def complexify
    (f : C(AddCircle (2 * Real.pi), Real)) : C(AddCircle (2 * Real.pi), Complex) where
  toFun x := (f x : Complex)
  continuous_toFun := Complex.continuous_ofReal.comp f.continuous

/-- Take real parts pointwise from a complex-valued continuous map. -/
def realPart
    (f : C(AddCircle (2 * Real.pi), Complex)) : C(AddCircle (2 * Real.pi), Real) where
  toFun x := (f x).re
  continuous_toFun := Complex.continuous_re.comp f.continuous

/-- The real part of the symmetric Fourier sum with frequencies `-n, ..., n`. -/
noncomputable def symmetricFourierPartialSum
    (f : C(AddCircle (2 * Real.pi), Real)) (n : Nat) :
    C(AddCircle (2 * Real.pi), Real) :=
  realPart <| Finset.sum (Finset.Icc (-(n : Int)) (n : Int))
    (fun k => fourierCoeff (complexify f) k • fourier k)

/-- The arithmetic mean of `S_0, ..., S_n`, a prospective reindexing of the source sequence. -/
noncomputable def fejerMean
    (f : C(AddCircle (2 * Real.pi), Real)) (n : Nat) :
    C(AddCircle (2 * Real.pi), Real) :=
  ((n + 1 : Nat) : Real)⁻¹ •
    Finset.sum (Finset.range (n + 1)) (symmetricFourierPartialSum f)

/-- An elaborated fixed-period, real-valued candidate awaiting source-transport approval. -/
def FejerTheoremTargetCandidate : Prop :=
  ∀ f : C(AddCircle (2 * Real.pi), Real),
    Tendsto (fejerMean f) atTop (nhds f)

/-- The first symmetric partial sum contains only frequency zero. -/
theorem symmetricFourierPartialSum_zero
    (f : C(AddCircle (2 * Real.pi), Real)) :
    symmetricFourierPartialSum f 0 =
      realPart (fourierCoeff (complexify f) 0 • fourier 0) := by
  simp [symmetricFourierPartialSum]

/-- The first Fejer mean is the zeroth symmetric partial sum. -/
theorem fejerMean_zero (f : C(AddCircle (2 * Real.pi), Real)) :
    fejerMean f 0 = symmetricFourierPartialSum f 0 := by
  simp [fejerMean]

end

end Stage1Instances.THM_M_0291.Candidate

set_option pp.explicit true in
#print Stage1Instances.THM_M_0291.Candidate.FejerTheoremTargetCandidate
