import Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point
import Mathlib.NumberTheory.Height.NumberField

/-!
# THM-M-0451: exact Neron-Tate canonical-height statement

This module freezes the existence-and-properties statement selected at intake.
It contains no proof that the package is inhabited.
-/

noncomputable section

open Filter
open scoped Topology WeierstrassCurve.Affine

namespace Stage1Instances.THM_M_0451

universe u

/-- The absolute logarithmic height of the projective x-coordinate.  Mathlib's
`xRep` convention sends the point at infinity to `[1, 0]`, so this definition
also freezes the identity-point boundary case. -/
def xHeight {K : Type u} [Field K] [NumberField K]
    {E : WeierstrassCurve K} (P : E⟮K⟯) : ℝ :=
  Height.logHeight P.xRep

/-- Data and all terminal properties in the Neron-Tate canonical-height
theorem.  `naiveHeight` is exactly one half of the x-coordinate height, matching
the normalization in Silverman, Chapter VIII, Theorem 9.3. -/
structure NeronTateHeightPackage (K : Type u) [Field K] [DecidableEq K] [NumberField K]
    (E : WeierstrassCurve K) [E.IsElliptic] where
  canonicalHeight : E⟮K⟯ → ℝ
  limit_formula : ∀ P : E⟮K⟯,
    Tendsto (λ n : ℕ => (4 : ℝ) ^ (-(n : ℤ)) *
      xHeight (((2 : ℕ) ^ n) • P) / 2) atTop (nhds (canonicalHeight P))
  bounded_difference : ∃ C : ℝ, ∀ P : E⟮K⟯,
    |canonicalHeight P - xHeight P / 2| ≤ C
  quadratic_zsmul : ∀ (m : ℤ) (P : E⟮K⟯),
    canonicalHeight (m • P) = (m : ℝ) ^ 2 * canonicalHeight P
  parallelogram : ∀ P Q : E⟮K⟯,
    canonicalHeight (P + Q) + canonicalHeight (P - Q) =
      2 * canonicalHeight P + 2 * canonicalHeight Q
  nonnegative : ∀ P : E⟮K⟯, 0 ≤ canonicalHeight P
  torsion_iff_height_zero : ∀ P : E⟮K⟯,
    IsOfFinAddOrder P ↔ canonicalHeight P = 0

/-- Every elliptic curve over every number field admits the normalized
Neron-Tate canonical-height package. -/
def NeronTateCanonicalHeightTarget : Prop :=
  ∀ {K : Type u} [Field K] [DecidableEq K] [NumberField K],
    ∀ (E : WeierstrassCurve K) [E.IsElliptic],
      Nonempty (NeronTateHeightPackage K E)

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationRemovedNumberField : Prop :=
  ∀ {K : Type u} [Field K] [DecidableEq K],
    ∀ (E : WeierstrassCurve K) [E.IsElliptic],
      ∃ h : E⟮K⟯ → ℝ, ∀ P, 0 ≤ h P

def mutationNaturalScalarsOnly : Prop :=
  ∀ {K : Type u} [Field K] [DecidableEq K] [NumberField K],
    ∀ (E : WeierstrassCurve K) [E.IsElliptic], ∃ h : E⟮K⟯ → ℝ,
      ∀ (m : ℕ) (P : E⟮K⟯), h (m • P) = (m : ℝ) ^ 2 * h P

def mutationOneWayTorsionKernel : Prop :=
  ∀ {K : Type u} [Field K] [DecidableEq K] [NumberField K],
    ∀ (E : WeierstrassCurve K) [E.IsElliptic], ∃ h : E⟮K⟯ → ℝ,
      ∀ P : E⟮K⟯, IsOfFinAddOrder P → h P = 0

def mutationOmittedLimit : Prop :=
  ∀ {K : Type u} [Field K] [DecidableEq K] [NumberField K],
    ∀ (E : WeierstrassCurve K) [E.IsElliptic], ∃ h : E⟮K⟯ → ℝ,
      (∃ C : ℝ, ∀ P : E⟮K⟯, |h P - xHeight P / 2| ≤ C) ∧
      ∀ P : E⟮K⟯, 0 ≤ h P

/-- The identity convention is definitionally the height of `[1, 0]`. -/
example {K : Type u} [Field K] [NumberField K] {E : WeierstrassCurve K} :
    xHeight (0 : E⟮K⟯) = Height.logHeight (![1, 0] : Fin 2 → K) := by
  simp [xHeight]

end Stage1Instances.THM_M_0451

set_option pp.explicit true in
#print Stage1Instances.THM_M_0451.NeronTateCanonicalHeightTarget
