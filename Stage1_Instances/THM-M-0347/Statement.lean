import Mathlib.Analysis.Fourier.AddCircle

/-!
# THM-M-0347: exact Fejer-theorem statement

This module freezes the periodic complex-valued statement only. It contains no
proof of Fejer's theorem.
-/

namespace Stage1Instances.THM_M_0347

open Filter Topology
open scoped BigOperators ComplexConjugate

/-- The symmetric Fourier partial sum with frequencies from `-n` through `n`. -/
noncomputable def symmetricFourierPartialSum {T : Real} [Fact (0 < T)]
    (f : C(AddCircle T, Complex)) (n : Nat) : C(AddCircle T, Complex) :=
  Finset.sum (Finset.Icc (-(n : Int)) (n : Int))
    (fun k => fourierCoeff f k • fourier k)

/-- The arithmetic mean of the first `n + 1` symmetric Fourier partial sums. -/
noncomputable def fejerMean {T : Real} [Fact (0 < T)]
    (f : C(AddCircle T, Complex)) (n : Nat) : C(AddCircle T, Complex) :=
  ((n + 1 : Nat) : Complex)⁻¹ •
    Finset.sum (Finset.range (n + 1)) (symmetricFourierPartialSum f)

/-- The exact target selected for Fejer's theorem: the first-order Cesaro means
of the symmetric Fourier sums of every continuous complex-valued function on a
positive-period additive circle converge in the continuous-map sup norm. -/
def FejerTheoremTarget : Prop :=
  ∀ (T : Real) [Fact (0 < T)] (f : C(AddCircle T, Complex)),
    Tendsto (fejerMean f) atTop (nhds f)

/-- Direct expansion of the selected target, used to check its encoding. -/
def ExpandedFejerTheoremTarget : Prop :=
  ∀ (T : Real) [Fact (0 < T)] (f : C(AddCircle T, Complex)),
    Tendsto
      (fun n : Nat =>
        ((n + 1 : Nat) : Complex)⁻¹ •
          Finset.sum (Finset.range (n + 1)) (fun k =>
            Finset.sum (Finset.Icc (-(k : Int)) (k : Int))
              (fun j => fourierCoeff f j • fourier j)))
      atTop (nhds f)

/-- The named definitions are definitionally the direct finite-sum encoding. -/
theorem fejerTheoremTarget_iff_expanded :
    FejerTheoremTarget ↔ ExpandedFejerTheoremTarget := by
  rfl

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationFixedPeriod : Prop :=
  ∀ (f : C(AddCircle (1 : Real), Complex)),
    Tendsto (fejerMean f) atTop (nhds f)

def mutationPointwiseConclusion : Prop :=
  ∀ (T : Real) [Fact (0 < T)] (f : C(AddCircle T, Complex)) (x : AddCircle T),
    Tendsto (fun n => fejerMean f n x) atTop (nhds (f x))

def mutationChangedBinderScope : Prop :=
  ∀ (T : Real) [Fact (0 < T)],
    Tendsto (fun n => fun f : C(AddCircle T, Complex) => fejerMean f n)
      atTop (nhds fun f => f)

def mutationOmitsInitialPartialSum : Prop :=
  ∀ (T : Real) [Fact (0 < T)] (f : C(AddCircle T, Complex)),
    Tendsto
      (fun n : Nat =>
        ((n + 1 : Nat) : Complex)⁻¹ •
          Finset.sum (Finset.Icc 1 (n + 1)) (symmetricFourierPartialSum f))
      atTop (nhds f)

/-- At index zero the symmetric partial sum contains exactly frequency zero. -/
theorem symmetricFourierPartialSum_zero {T : Real} [Fact (0 < T)]
    (f : C(AddCircle T, Complex)) :
    symmetricFourierPartialSum f 0 = fourierCoeff f 0 • fourier 0 := by
  simp [symmetricFourierPartialSum]

/-- The zeroth Fejer mean is the zeroth symmetric Fourier partial sum. -/
theorem fejerMean_zero {T : Real} [Fact (0 < T)]
    (f : C(AddCircle T, Complex)) :
    fejerMean f 0 = symmetricFourierPartialSum f 0 := by
  simp [fejerMean]

end Stage1Instances.THM_M_0347

set_option pp.explicit true in
#print Stage1Instances.THM_M_0347.FejerTheoremTarget
