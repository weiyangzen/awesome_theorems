import Mathlib.AlgebraicGeometry.EllipticCurve.Reduction
import Mathlib.NumberTheory.ModularForms.Basic
import Mathlib.NumberTheory.ModularForms.CongruenceSubgroups
import Mathlib.NumberTheory.ModularForms.QExpansion

open Matrix
open scoped MatrixGroups ModularForm

#check WeierstrassCurve
#check WeierstrassCurve.IsElliptic
#check WeierstrassCurve.HasGoodReduction
#check WeierstrassCurve.HasMultiplicativeReduction
#check WeierstrassCurve.HasAdditiveReduction
#check ModularForm
#check CuspForm
#check CongruenceSubgroup.Gamma0
#check ModularFormClass.qExpansion

/-- A local encoding ingredient only. This is not global semistability over `Q`. -/
def IntakeLocalSemistableAt
    (R : Type*) [CommRing R] [IsDomain R] [IsDiscreteValuationRing R]
    {K : Type*} [Field K] [Algebra R K] [IsFractionRing R K]
    (W : WeierstrassCurve K) : Prop :=
  W.HasGoodReduction R ∨ W.HasMultiplicativeReduction R

#check IntakeLocalSemistableAt
