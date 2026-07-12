import «Stage1_Instances».«THM-M-0989».Statement

/-!
# Checked composition surface for the THM-M-0989 obligation tree

This file proves only that row-sum measurability and convergence of the exact
row-law characteristic functions compose, through Levy convergence, to the
frozen target.  The two inputs remain explicit obligations.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory Real Topology

namespace Stage1Instances.THM_M_0989

universe u

def RowSumsAEMeasurable {Omega : Type u} [MeasurableSpace Omega]
    (A : NormalizedTriangularArray Omega) : Prop :=
  forall n, AEMeasurable (rowSum A n) A.probabilityMeasure

def RowLawCharFunConverges {Omega : Type u} [MeasurableSpace Omega]
    (A : NormalizedTriangularArray Omega) : Prop :=
  forall t : Real,
    Tendsto
      (fun n => charFun (A.probabilityMeasure.map (rowSum A n)) t)
      atTop
      (nhds (charFun (gaussianReal 0 1) t))

/-- Exact checked final composition. Its hypotheses are deliberately not
proved here, so this declaration gives no proof credit to the root. -/
theorem root_of_row_charFun_packages
    {Omega : Type u} [MeasurableSpace Omega]
    (A : NormalizedTriangularArray Omega)
    (hmeas : RowSumsAEMeasurable A)
    (hchar : RowLawCharFunConverges A) :
    letI : IsProbabilityMeasure A.probabilityMeasure := A.isProbabilityMeasure
    TendstoInDistribution
      (fun n => rowSum A n)
      atTop
      (id : Real -> Real)
      (fun _ => A.probabilityMeasure)
      (gaussianReal 0 1) := by
  letI : IsProbabilityMeasure A.probabilityMeasure := A.isProbabilityMeasure
  refine {
    forall_aemeasurable := hmeas
    aemeasurable_limit := measurable_id.aemeasurable
    tendsto := ?_
  }
  apply ProbabilityMeasure.tendsto_iff_tendsto_charFun.2
  simpa using hchar

end Stage1Instances.THM_M_0989
