import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.LinearAlgebra.CrossProduct

/-!
# THM-M-0152: exact Theorema Egregium statement

This file freezes a regular-parametrized-surface encoding of the pointwise
local-isometry invariance claim. It contains no proof of that claim.
-/

namespace Stage1Instances.THM_M_0152

abbrev Plane := Fin 2 → ℝ
abbrev Space := Fin 3 → ℝ

noncomputable def dot (a b : Space) : ℝ := ∑ i, a i * b i

/-- The differential of a parametrized surface. -/
noncomputable def tangent (X : Plane → Space) (p v : Plane) : Space :=
  fderiv ℝ X p v

/-- The second differential of a parametrized surface. -/
noncomputable def second (X : Plane → Space) (p u v : Plane) : Space :=
  fderiv ℝ (fun q ↦ fderiv ℝ X q) p u v

/-- A parametrization is regular when its differential is injective everywhere. -/
def Regular (X : Plane → Space) : Prop :=
  ContDiff ℝ ⊤ X ∧ ∀ p, Function.Injective (fderiv ℝ X p)

/-- The first fundamental form induced by a parametrized surface. -/
noncomputable def firstFundamentalForm (X : Plane → Space) (p u v : Plane) : ℝ :=
  dot (tangent X p u) (tangent X p v)

/-- Gaussian curvature from the first and second fundamental forms.

The denominator is nonzero for `Regular X`; keeping this as a total Lean
function makes its value outside the regular locus irrelevant to the target.
-/
noncomputable def gaussianCurvature (X : Plane → Space) (p : Plane) : ℝ :=
  let e0 : Plane := Pi.single 0 1
  let e1 : Plane := Pi.single 1 1
  let xu := tangent X p e0
  let xv := tangent X p e1
  let normal := (‖crossProduct xu xv‖⁻¹) • crossProduct xu xv
  let E := dot xu xu
  let F := dot xu xv
  let G := dot xv xv
  let L := dot (second X p e0 e0) normal
  let M := dot (second X p e0 e1) normal
  let N := dot (second X p e1 e1) normal
  (L * N - M ^ 2) / (E * G - F ^ 2)

/-- `phi` is a local coordinate diffeomorphism at `p`, with the displayed
local inverse. -/
def IsLocalCoordinateEquivAt (phi psi : Plane → Plane) (p : Plane) : Prop :=
  ContDiffAt ℝ ⊤ phi p ∧ ContDiffAt ℝ ⊤ psi (phi p) ∧
    (psi ∘ phi) =ᶠ[nhds p] id ∧ (phi ∘ psi) =ᶠ[nhds (phi p)] id

/-- The coordinate map preserves the induced metric on a neighborhood of `p`. -/
def IsLocalIsometryAt (X Y : Plane → Space) (phi : Plane → Plane) (p : Plane) : Prop :=
  ∀ᶠ q in nhds p, ∀ u v,
    firstFundamentalForm Y (phi q) (fderiv ℝ phi q u) (fderiv ℝ phi q v) =
      firstFundamentalForm X q u v

/-- Gauss's Theorema Egregium: every smooth local isometry between regular
surface parametrizations preserves Gaussian curvature pointwise. -/
def TheoremaEgregiumTarget : Prop :=
  ∀ (X Y : Plane → Space), Regular X → Regular Y →
    ∀ (phi psi : Plane → Plane) (p : Plane),
      IsLocalCoordinateEquivAt phi psi p → IsLocalIsometryAt X Y phi p →
        gaussianCurvature Y (phi p) = gaussianCurvature X p

/-- Expanded spelling used to check binder order and the two local hypotheses. -/
def ExpandedTarget : Prop :=
  ∀ (X Y : Plane → Space),
    (ContDiff ℝ ⊤ X ∧ ∀ p, Function.Injective (fderiv ℝ X p)) →
    (ContDiff ℝ ⊤ Y ∧ ∀ p, Function.Injective (fderiv ℝ Y p)) →
    ∀ (phi psi : Plane → Plane) (p : Plane),
      (ContDiffAt ℝ ⊤ phi p ∧ ContDiffAt ℝ ⊤ psi (phi p) ∧
        (psi ∘ phi) =ᶠ[nhds p] id ∧ (phi ∘ psi) =ᶠ[nhds (phi p)] id) →
      (∀ᶠ q in nhds p, ∀ u v,
        firstFundamentalForm Y (phi q) (fderiv ℝ phi q u) (fderiv ℝ phi q v) =
          firstFundamentalForm X q u v) →
      gaussianCurvature Y (phi p) = gaussianCurvature X p

theorem theoremaEgregiumTarget_iff_expandedTarget :
    TheoremaEgregiumTarget ↔ ExpandedTarget := Iff.rfl

-- Structural mutations, elaborated separately and compared by the validator.
def mutationDropsRegularity : Prop :=
  ∀ (X Y : Plane → Space) (phi psi : Plane → Plane) (p : Plane),
    IsLocalCoordinateEquivAt phi psi p → IsLocalIsometryAt X Y phi p →
      gaussianCurvature Y (phi p) = gaussianCurvature X p

def mutationPointMetricOnly : Prop :=
  ∀ (X Y : Plane → Space), Regular X → Regular Y →
    ∀ (phi psi : Plane → Plane) (p : Plane), IsLocalCoordinateEquivAt phi psi p →
      (∀ u v, firstFundamentalForm Y (phi p) (fderiv ℝ phi p u) (fderiv ℝ phi p v) =
        firstFundamentalForm X p u v) →
      gaussianCurvature Y (phi p) = gaussianCurvature X p

def mutationIdentityCoordinates : Prop :=
  ∀ (X Y : Plane → Space), Regular X → Regular Y →
    IsLocalIsometryAt X Y id 0 → gaussianCurvature Y 0 = gaussianCurvature X 0

def mutationPreservesMeanCurvature : Prop :=
  ∀ (X Y : Plane → Space), Regular X → Regular Y →
    ∀ (phi psi : Plane → Plane) (p : Plane),
      IsLocalCoordinateEquivAt phi psi p → IsLocalIsometryAt X Y phi p →
        gaussianCurvature Y (phi p) + 1 = gaussianCurvature X p + 1

set_option pp.explicit true in
#print Stage1Instances.THM_M_0152.TheoremaEgregiumTarget

end Stage1Instances.THM_M_0152
