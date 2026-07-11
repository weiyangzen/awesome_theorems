import Statement

/-!
# THM-M-0183 proof-phase result

The frozen proposition quantifies over every `KahlerMetricInterface`, including
interfaces whose metric carrier is empty.  This file gives a kernel-checked
countermodel.  Consequently the frozen target has no proof body: it must be
repaired at the statement phase before Yau's theorem can be formalized.
-/

noncomputable section

open scoped Manifold

namespace Stage1Instances.THMM0183

/-- The zero-dimensional compact complex manifold, with trivial abstract
cohomology and class carriers. -/
def counterexampleDomain :
    CalabiYauDomain (Fin 0 → ℂ) (Fin 0 → ℂ)
      (modelWithCornersSelf ℂ (Fin 0 → ℂ)) (Fin 0 → ℂ) where
  smoothComplexManifold := inferInstance
  hausdorff := inferInstance
  realDegreeTwoCohomology := PUnit
  zeroClass := PUnit.unit
  firstChernClassReal := PUnit.unit
  kahlerClass := PUnit
  isKahlerClass := fun _ => True

/-- The statement permits this interface even though it has no metric. -/
def emptyMetricInterface : KahlerMetricInterface counterexampleDomain where
  metric := Empty
  representsClass := fun _ _ => True
  compatibleWithComplexStructure := fun _ => True
  isKahlerMetric := fun _ => True
  ricciTensorVanishes := fun _ => True

/-- The exact frozen target is false because it demands a metric from an
arbitrary, possibly empty metric interface. -/
theorem not_yauCalabiConjectureTarget :
    ¬ YauCalabiConjectureTarget.{0} := by
  intro target
  have h := target (Fin 0 → ℂ) (Fin 0 → ℂ)
    (modelWithCornersSelf ℂ (Fin 0 → ℂ)) (Fin 0 → ℂ)
    counterexampleDomain emptyMetricInterface PUnit.unit rfl trivial
  rcases h with ⟨g, _⟩
  exact Empty.elim g

#print axioms not_yauCalabiConjectureTarget

end Stage1Instances.THMM0183
