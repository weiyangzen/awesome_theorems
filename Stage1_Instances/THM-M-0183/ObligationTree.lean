import Statement

/-!
# THM-M-0183 conditional composition certificate

This module checks the final logical composition only. The analytic existence
package is deliberately a premise: no proof of the Calabi conjecture is claimed.
-/

noncomputable section

namespace Stage1Instances.THMM0183

universe u

/-- The exact analytic output needed after the geometric and PDE constructions.
This is an obligation interface, not an assumed field of the statement data. -/
def PrescribedClassRicciFlatPackage : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [NormedSpace Complex E]
    (H : Type u) [TopologicalSpace H] (I : ModelWithCorners Complex E H)
    (M : Type u) [TopologicalSpace M] [ChartedSpace H M] [CompactSpace M]
    (X : CalabiYauDomain E H I M) (G : KahlerMetricInterface X)
    (kappa : X.kahlerClass),
      X.firstChernClassReal = X.zeroClass ->
      X.isKahlerClass kappa ->
      exists g : G.metric,
        G.representsClass g kappa /\
        G.compatibleWithComplexStructure g /\
        G.isKahlerMetric g /\
        G.ricciTensorVanishes g

/-- Checked child-to-root composition. Its sole premise remains open. -/
theorem yauCalabiConjectureTarget_of_analyticPackage
    (analytic : PrescribedClassRicciFlatPackage.{u}) :
    YauCalabiConjectureTarget.{u} := by
  intro E _ _ H _ I M _ _ _ X G kappa hc1 hkappa
  exact analytic E H I M X G kappa hc1 hkappa

#print axioms yauCalabiConjectureTarget_of_analyticPackage

end Stage1Instances.THMM0183
