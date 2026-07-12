import Statement

/-!
# THM-M-1566 conditional obligation composition

This module checks the final logical composition chosen by the frozen proof
architecture. The analytic existence and uniqueness packages remain explicit
premises. Consequently this file proves no instance of Corollary 5.9.
-/

namespace Stage1Instances.THMM1566

universe u

/-- The output required from the analytic construction, renormalization,
stopping-time, and convergence packages. -/
def Corollary59ExistencePackage : Prop :=
  forall (Omega : Type u) (_m : MeasurableSpace Omega) (mu : Measure Omega),
    IsProbabilityMeasure mu ->
      forall (api : GIPCorollary59API Omega) (D : GIPCorollary59Data Omega api),
        exists u : api.Solution, IsCorollary59Solution mu api D u

/-- The output required from the fixed-point stability and uniqueness package. -/
def Corollary59UniquenessPackage : Prop :=
  forall (Omega : Type u) (_m : MeasurableSpace Omega) (mu : Measure Omega),
    IsProbabilityMeasure mu ->
      forall (api : GIPCorollary59API Omega) (D : GIPCorollary59Data Omega api)
        (u v : api.Solution),
          IsCorollary59Solution mu api D u ->
          IsCorollary59Solution mu api D v -> u = v

/-- Checked conditional composition of the two root-critical packages into the
exact canonical target. Both premises are consumed. -/
theorem root_of_existence_and_uniqueness
    (existence : Corollary59ExistencePackage.{u})
    (uniqueness : Corollary59UniquenessPackage.{u}) :
    GIPCorollary59Target.{u} := by
  intro Omega measurable mu probability api D
  obtain ⟨u, hu⟩ := existence Omega measurable mu probability api D
  exact ⟨u, hu, fun v hv => uniqueness Omega measurable mu probability api D v u hv hu⟩

#print axioms root_of_existence_and_uniqueness

end Stage1Instances.THMM1566
