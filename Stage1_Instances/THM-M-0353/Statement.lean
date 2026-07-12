import Mathlib.RingTheory.Polynomial.Hermite.Gaussian
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic
import Mathlib.Analysis.InnerProductSpace.l2Space

/-!
# THM-M-0353: completeness of the Hermite functions

This module freezes only the exact statement. The normalization is the standard
Lebesgue-measure normalization expressed through mathlib's probabilists'
Hermite polynomial `Polynomial.hermite`:

`psi n x = pi^(-1/4) / sqrt(n!) * He_n(sqrt 2 * x) * exp(-x^2/2)`.

The target says both that these concrete functions represent `L^2` vectors and
that those vectors are exactly the vectors of a Hilbert basis.
-/

namespace Stage1Instances.THM_M_0353

open scoped ENNReal NNReal
open MeasureTheory

/-- Lebesgue measure on the real line, named to keep every target parameter explicit. -/
noncomputable def leb : Measure Real := MeasureTheory.volume

/-- The normalized, complex-valued `n`th Hermite function on the real line. -/
noncomputable def hermiteFunction (n : Nat) (x : Real) : Complex :=
  ((Real.pi ^ (-(1 : Real) / 4) / Real.sqrt (n.factorial : Real)) *
    Polynomial.aeval (Real.sqrt 2 * x) (Polynomial.hermite n) *
    Real.exp (-(x ^ 2 / 2)) : Real)

/-- Canonical rev-5.6 target: the normalized Hermite functions form a complete
orthonormal basis of complex `L^2(Real, volume)`. -/
def HermiteCompletenessTarget : Prop :=
  (∀ n : Nat, MemLp (hermiteFunction n) (2 : ENNReal) leb) ∧
    ∃ b : HilbertBasis Nat Complex (Lp Complex (2 : ENNReal) leb),
      ∀ n : Nat, (b n : Real → Complex) =ᵐ[leb] hermiteFunction n

-- Structural mutations: each deliberately changes one part of the target.
def mutationRemovedIntegrability : Prop :=
  Nonempty (HilbertBasis Nat Complex (Lp Complex (2 : ENNReal) leb))

def mutationChangedDomain : Prop :=
  (∀ n : Nat, MemLp (hermiteFunction n) (2 : ENNReal) (Measure.dirac 0)) ∧ True

def mutationChangedBinderScope : Prop :=
  ∃ b : HilbertBasis Nat Complex (Lp Complex (2 : ENNReal) leb),
    ∃ n : Nat, (b n : Real → Complex) =ᵐ[leb] hermiteFunction n

def mutationFiniteTruncation (N : Nat) : Prop :=
  ∀ n : Nat, n ≤ N → MemLp (hermiteFunction n) (2 : ENNReal) leb

#check HermiteCompletenessTarget

end Stage1Instances.THM_M_0353

set_option pp.explicit true in
#print Stage1Instances.THM_M_0353.HermiteCompletenessTarget
