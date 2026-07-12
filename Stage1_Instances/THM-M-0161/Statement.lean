import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.LinearAlgebra.CrossProduct

/-!
# THM-M-0161: exact fundamental theorem of space curves statement

This module freezes a classical open-interval formulation. It only elaborates
the target; it does not prove the fundamental theorem.
-/

namespace Stage1Instances.THM_M_0161

open Set Matrix

abbrev E3 := Fin 3 → ℝ

/-- The Euclidean dot product in the fixed, oriented coordinates of `E3`. -/
def dot (u v : E3) : ℝ := ∑ i, u i * v i

/-- Euclidean length, stated explicitly so the coordinate representation does
not accidentally use the Pi space's supremum norm. -/
noncomputable def length (u : E3) : ℝ := Real.sqrt (dot u u)

/-- The derivative along an open interval. -/
noncomputable def dWithin (a b : ℝ) (c : ℝ → E3) (s : ℝ) : E3 :=
  derivWithin c (Ioo a b) s

noncomputable def d2Within (a b : ℝ) (c : ℝ → E3) (s : ℝ) : E3 :=
  derivWithin (dWithin a b c) (Ioo a b) s

noncomputable def d3Within (a b : ℝ) (c : ℝ → E3) (s : ℝ) : E3 :=
  derivWithin (d2Within a b c) (Ioo a b) s

/-- Unit-speed curves use curvature `|c''|`. -/
noncomputable def curvature (a b : ℝ) (c : ℝ → E3) (s : ℝ) : ℝ :=
  length (d2Within a b c s)

/-- Signed torsion in the standard orientation. Positivity of curvature and
unit speed make the denominator nonzero for curves admitted by the target. -/
noncomputable def torsion (a b : ℝ) (c : ℝ → E3) (s : ℝ) : ℝ :=
  dot (crossProduct (dWithin a b c s) (d2Within a b c s))
      (d3Within a b c s) /
    dot (crossProduct (dWithin a b c s) (d2Within a b c s))
      (crossProduct (dWithin a b c s) (d2Within a b c s))

def IsUnitSpeed (a b : ℝ) (c : ℝ → E3) : Prop :=
  ∀ s ∈ Ioo a b, length (dWithin a b c s) = 1

/-- An orientation-preserving Euclidean rigid motion in fixed coordinates. -/
def RelatedByProperRigidMotion (a b : ℝ) (c₁ c₂ : ℝ → E3) : Prop :=
  ∃ (Q : E3 ≃ₗ[ℝ] E3) (t : E3),
    (∀ u v, dot (Q u) (Q v) = dot u v) ∧
    Matrix.det (fun i j : Fin 3 => Q (Pi.single j 1) i) = 1 ∧
    ∀ s ∈ Ioo a b, c₂ s = Q (c₁ s) + t

/-- A `C^3` unit-speed curve on `(a,b)` realizing prescribed curvature and
signed torsion there. -/
def RealizesInvariants (a b : ℝ) (κ τ : ℝ → ℝ) (c : ℝ → E3) : Prop :=
  ContDiffOn ℝ 3 c (Ioo a b) ∧ IsUnitSpeed a b c ∧
    (∀ s ∈ Ioo a b, curvature a b c s = κ s) ∧
    ∀ s ∈ Ioo a b, torsion a b c s = τ s

/-- The open-interval fundamental theorem of space curves: differentiable positive
curvature and differentiable signed torsion are realized, uniquely up to a proper
rigid motion. -/
def FundamentalTheoremOfSpaceCurvesTarget : Prop :=
  ∀ (a b : ℝ), a < b → ∀ (κ τ : ℝ → ℝ),
    DifferentiableOn ℝ κ (Ioo a b) → DifferentiableOn ℝ τ (Ioo a b) →
    (∀ s ∈ Ioo a b, 0 < κ s) →
    (∃ c : ℝ → E3, RealizesInvariants a b κ τ c) ∧
    ∀ c₁ c₂ : ℝ → E3,
      RealizesInvariants a b κ τ c₁ → RealizesInvariants a b κ τ c₂ →
      RelatedByProperRigidMotion a b c₁ c₂

-- Separately elaborated structural mutations, compared by the validator.
def mutationAllowsZeroCurvature : Prop :=
  ∀ (a b : ℝ), a < b → ∀ (κ τ : ℝ → ℝ),
    DifferentiableOn ℝ κ (Ioo a b) → DifferentiableOn ℝ τ (Ioo a b) →
    (∀ s ∈ Ioo a b, 0 ≤ κ s) →
    (∃ c : ℝ → E3, RealizesInvariants a b κ τ c) ∧
    ∀ c₁ c₂, RealizesInvariants a b κ τ c₁ → RealizesInvariants a b κ τ c₂ →
      RelatedByProperRigidMotion a b c₁ c₂

def mutationOmitsExistence : Prop :=
  ∀ (a b : ℝ), a < b → ∀ (κ τ : ℝ → ℝ),
    DifferentiableOn ℝ κ (Ioo a b) → DifferentiableOn ℝ τ (Ioo a b) →
    (∀ s ∈ Ioo a b, 0 < κ s) →
    ∀ c₁ c₂, RealizesInvariants a b κ τ c₁ → RealizesInvariants a b κ τ c₂ →
      RelatedByProperRigidMotion a b c₁ c₂

def mutationAllowsReflections : Prop :=
  ∀ (a b : ℝ), a < b → ∀ (κ τ : ℝ → ℝ),
    DifferentiableOn ℝ κ (Ioo a b) → DifferentiableOn ℝ τ (Ioo a b) →
    (∀ s ∈ Ioo a b, 0 < κ s) →
    (∃ c : ℝ → E3, RealizesInvariants a b κ τ c) ∧
    ∀ c₁ c₂, RealizesInvariants a b κ τ c₁ → RealizesInvariants a b κ τ c₂ →
      ∃ (Q : E3 ≃ₗ[ℝ] E3) (t : E3),
        (∀ u v, dot (Q u) (Q v) = dot u v) ∧
        ∀ s ∈ Ioo a b, c₂ s = Q (c₁ s) + t

def mutationUsesClosedInterval : Prop :=
  ∀ (a b : ℝ), a < b → ∀ (κ τ : ℝ → ℝ),
    DifferentiableOn ℝ κ (Icc a b) → DifferentiableOn ℝ τ (Icc a b) →
    (∀ s ∈ Icc a b, 0 < κ s) →
    (∃ c : ℝ → E3, RealizesInvariants a b κ τ c) ∧
    ∀ c₁ c₂, RealizesInvariants a b κ τ c₁ → RealizesInvariants a b κ τ c₂ →
      RelatedByProperRigidMotion a b c₁ c₂

end Stage1Instances.THM_M_0161

set_option pp.explicit true in
#print Stage1Instances.THM_M_0161.FundamentalTheoremOfSpaceCurvesTarget
