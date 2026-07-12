import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic

/-!
# THM-M-1553: exact KdV Hirota statement

This module freezes and elaborates the statement boundary only. It contains no
proof of the bilinear-to-KdV implication.
-/

noncomputable section

namespace Stage1Instances.THM_M_1553

/-- A real field depending on space and time. -/
abbrev Field := ℝ × ℝ → ℝ

/-- Partial differentiation in the first (space) coordinate. -/
def partialX (f : Field) : Field :=
  fun z => deriv (fun x : ℝ => f (x, z.2)) z.1

/-- Partial differentiation in the second (time) coordinate. -/
def partialT (f : Field) : Field :=
  fun z => deriv (fun t : ℝ => f (z.1, t)) z.2

/-- Iterate an operator on real space-time fields. -/
def iterate (op : Field → Field) : ℕ → Field → Field
  | 0 => id
  | n + 1 => op ∘ iterate op n

/-- The mixed derivative `partialX^xOrder partialT^tOrder f`. -/
def mixedDerivative (xOrder tOrder : ℕ) (f : Field) : Field :=
  iterate partialX xOrder (iterate partialT tOrder f)

/--
The concrete Hirota operator
`D_x^m D_t^n f . g`, expanded by the two binomial formulas and evaluated on
the diagonal.
-/
def hirotaD (xOrder tOrder : ℕ) (f g : Field) : Field :=
  fun z =>
    ∑ i ∈ Finset.range (xOrder + 1),
      ∑ j ∈ Finset.range (tOrder + 1),
        ((-1 : ℝ) ^ (i + j) * (Nat.choose xOrder i : ℝ) *
            (Nat.choose tOrder j : ℝ)) *
          mixedDerivative (xOrder - i) (tOrder - j) f z *
          mixedDerivative i j g z

/-- The selected KdV bilinear equation `(D_x^4 + D_x D_t) tau . tau = 0`. -/
def SatisfiesKdVBilinearEquation (tau : Field) : Prop :=
  ∀ z : ℝ × ℝ, hirotaD 4 0 tau tau z + hirotaD 1 1 tau tau z = 0

/-- The dependent-variable transform `u = 2 partial_x^2 (log tau)`. -/
def tauTransform (tau : Field) : Field :=
  fun z => 2 * iterate partialX 2 (fun w => Real.log (tau w)) z

/-- The KdV residual `u_t + 6 u u_x + u_xxx`. -/
def kdvResidual (u : Field) : Field :=
  fun z => partialT u z + 6 * u z * partialX u z + iterate partialX 3 u z

/--
The exact first theorem selected at intake for the Hirota bilinear method.

It is the forward KdV bridge over real space-time: a five-times continuously
differentiable, everywhere-positive tau function satisfying the concrete
Hirota identity transforms to a solution of
`u_t + 6 u u_x + u_xxx = 0`.
-/
def HirotaKdVTarget : Prop :=
  ∀ tau : Field,
    ContDiff ℝ 5 tau →
    (∀ z : ℝ × ℝ, 0 < tau z) →
    SatisfiesKdVBilinearEquation tau →
    ∀ z : ℝ × ℝ, kdvResidual (tauTransform tau) z = 0

/-- Directly expanded source-facing form of the frozen target. -/
def ExpandedHirotaKdVTarget : Prop :=
  ∀ tau : ℝ × ℝ → ℝ,
    ContDiff ℝ 5 tau →
    (∀ z : ℝ × ℝ, 0 < tau z) →
    (∀ z : ℝ × ℝ,
      hirotaD 4 0 tau tau z + hirotaD 1 1 tau tau z = 0) →
    ∀ z : ℝ × ℝ,
      partialT (tauTransform tau) z +
          6 * tauTransform tau z * partialX (tauTransform tau) z +
          iterate partialX 3 (tauTransform tau) z = 0

/-- Checked transport between the canonical and source-expanded encodings. -/
theorem hirotaKdVTarget_iff_expanded :
    HirotaKdVTarget ↔ ExpandedHirotaKdVTarget := by
  rfl

-- Structural mutations: these elaborate, but are intentionally not the target.
def mutationNonnegativeTau : Prop :=
  ∀ tau : Field, ContDiff ℝ 5 tau → (∀ z, 0 ≤ tau z) →
    SatisfiesKdVBilinearEquation tau →
    ∀ z, kdvResidual (tauTransform tau) z = 0

def mutationChangedKdVSign : Prop :=
  ∀ tau : Field, ContDiff ℝ 5 tau → (∀ z, 0 < tau z) →
    SatisfiesKdVBilinearEquation tau →
    ∀ z, partialT (tauTransform tau) z -
      6 * tauTransform tau z * partialX (tauTransform tau) z +
      iterate partialX 3 (tauTransform tau) z = 0

def mutationDroppedMixedHirotaTerm : Prop :=
  ∀ tau : Field, ContDiff ℝ 5 tau → (∀ z, 0 < tau z) →
    (∀ z, hirotaD 4 0 tau tau z = 0) →
    ∀ z, kdvResidual (tauTransform tau) z = 0

end Stage1Instances.THM_M_1553

set_option pp.explicit true in
#print Stage1Instances.THM_M_1553.HirotaKdVTarget

set_option pp.explicit true in
#print Stage1Instances.THM_M_1553.mutationNonnegativeTau

set_option pp.explicit true in
#print Stage1Instances.THM_M_1553.mutationChangedKdVSign

set_option pp.explicit true in
#print Stage1Instances.THM_M_1553.mutationDroppedMixedHirotaTerm
