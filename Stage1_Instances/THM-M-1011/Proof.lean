import Statement
import Mathlib.MeasureTheory.Measure.Prokhorov

/-!
# THM-M-1011: Prokhorov's theorem on a pseudometric space

The separation quotient of a complete second-countable pseudometric space is a
complete second-countable metric space.  Borel probability measures on the
original space and on this quotient are homeomorphic: Borel sets cannot
distinguish topologically inseparable points, so any choice of representatives
is continuous and gives the inverse pushforward.  We apply the pinned
Prokhorov theorem on the quotient and transport compactness back.
-/

open MeasureTheory Set Topology

namespace Stage1Instances.THM_M_1011.Proof

universe u

variable (X : Type u) [MeasurableSpace X] [PseudoMetricSpace X] [BorelSpace X]
  [SecondCountableTopology X] [CompleteSpace X]

local instance : SecondCountableTopology (SeparationQuotient X) :=
  SeparationQuotient.isQuotientMap_mk.secondCountableTopology
    SeparationQuotient.isOpenMap_mk

local instance : MeasurableSpace (SeparationQuotient X) :=
  borel (SeparationQuotient X)

local instance : BorelSpace (SeparationQuotient X) :=
  ⟨rfl⟩

noncomputable def representative : SeparationQuotient X → X :=
  Function.surjInv (SeparationQuotient.surjective_mk (X := X))

omit [MeasurableSpace X] [BorelSpace X] [SecondCountableTopology X] [CompleteSpace X] in
theorem quotient_representative (z : SeparationQuotient X) :
    SeparationQuotient.mk (representative X z) = z :=
  Function.surjInv_eq _ z

omit [MeasurableSpace X] [BorelSpace X] [SecondCountableTopology X] [CompleteSpace X] in
theorem continuous_representative : Continuous (representative X) := by
  apply SeparationQuotient.isInducing_mk.continuous_iff.2
  simpa only [Function.comp_def, quotient_representative] using
    (continuous_id : Continuous (id : SeparationQuotient X → SeparationQuotient X))

noncomputable def quotientMap :
    ProbabilityMeasure X → ProbabilityMeasure (SeparationQuotient X) :=
  fun P => P.map SeparationQuotient.continuous_mk.measurable.aemeasurable

noncomputable def sectionMap :
    ProbabilityMeasure (SeparationQuotient X) → ProbabilityMeasure X :=
  fun P => P.map (continuous_representative X).measurable.aemeasurable

omit [SecondCountableTopology X] [CompleteSpace X] in
theorem continuous_quotientMap : Continuous (quotientMap X) :=
  ProbabilityMeasure.continuous_map SeparationQuotient.continuous_mk

omit [SecondCountableTopology X] [CompleteSpace X] in
theorem continuous_sectionMap : Continuous (sectionMap X) :=
  ProbabilityMeasure.continuous_map (continuous_representative X)

omit [SecondCountableTopology X] [CompleteSpace X] in
theorem sectionMap_quotientMap (P : ProbabilityMeasure X) :
    sectionMap X (quotientMap X P) = P := by
  apply ProbabilityMeasure.toMeasure_injective
  simp only [sectionMap, quotientMap, ProbabilityMeasure.toMeasure_map]
  rw [Measure.map_map (continuous_representative X).measurable
    SeparationQuotient.continuous_mk.measurable]
  apply Measure.ext
  intro A hA
  rw [Measure.map_apply]
  · congr 1
    apply Set.ext
    intro x
    simp only [Function.comp_apply, Set.mem_preimage]
    exact Inseparable.mem_measurableSet_iff
      (SeparationQuotient.mk_eq_mk.mp
        (quotient_representative X (SeparationQuotient.mk x))) hA
  · exact (continuous_representative X).measurable.comp
      SeparationQuotient.continuous_mk.measurable
  · exact hA

omit [SecondCountableTopology X] [CompleteSpace X] in
theorem quotientMap_sectionMap (P : ProbabilityMeasure (SeparationQuotient X)) :
    quotientMap X (sectionMap X P) = P := by
  apply ProbabilityMeasure.toMeasure_injective
  simp only [sectionMap, quotientMap, ProbabilityMeasure.toMeasure_map]
  rw [Measure.map_map SeparationQuotient.continuous_mk.measurable
    (continuous_representative X).measurable]
  simpa only [Function.comp_def, quotient_representative] using
    (Measure.map_id (μ := (P : Measure (SeparationQuotient X))))

noncomputable def probabilityMeasureHomeomorph :
    ProbabilityMeasure X ≃ₜ ProbabilityMeasure (SeparationQuotient X) where
  toEquiv := {
    toFun := quotientMap X
    invFun := sectionMap X
    left_inv := sectionMap_quotientMap X
    right_inv := quotientMap_sectionMap X
  }
  continuous_toFun := continuous_quotientMap X
  continuous_invFun := continuous_sectionMap X

omit [SecondCountableTopology X] [CompleteSpace X] in
theorem quotientMap_underlyingMeasures (S : Set (ProbabilityMeasure X)) :
    THM_M_1011.underlyingMeasures (quotientMap X '' S) =
      Measure.map SeparationQuotient.mk '' THM_M_1011.underlyingMeasures S := by
  ext m
  constructor
  · rintro ⟨Q, ⟨P, hPS, rfl⟩, rfl⟩
    exact ⟨(P : Measure X), ⟨P, hPS, rfl⟩, rfl⟩
  · rintro ⟨m, ⟨P, hPS, rfl⟩, rfl⟩
    exact ⟨quotientMap X P, ⟨P, hPS, rfl⟩, rfl⟩

omit [SecondCountableTopology X] [CompleteSpace X] in
theorem quotientMap_isUniformlyTight (S : Set (ProbabilityMeasure X))
    (hS : THM_M_1011.IsUniformlyTight S) :
    THM_M_1011.IsUniformlyTight (quotientMap X '' S) := by
  rw [THM_M_1011.IsUniformlyTight, quotientMap_underlyingMeasures]
  exact hS.map SeparationQuotient.continuous_mk

omit [SecondCountableTopology X] [CompleteSpace X] in
theorem isCompact_closure_iff_quotientMap (S : Set (ProbabilityMeasure X)) :
    IsCompact (closure S) ↔ IsCompact (closure (quotientMap X '' S)) := by
  rw [← (probabilityMeasureHomeomorph X).isCompact_image]
  rw [(probabilityMeasureHomeomorph X).image_closure]
  rfl

omit [SecondCountableTopology X] [CompleteSpace X] in
theorem tight_to_compact (S : Set (ProbabilityMeasure X))
    (hS : THM_M_1011.IsUniformlyTight S) : IsCompact (closure S) := by
  apply (isCompact_closure_iff_quotientMap X S).2
  exact isCompact_closure_of_isTightMeasureSet
    (quotientMap_isUniformlyTight X S hS)

/-- The exact frozen THM-M-1011 root theorem. -/
theorem canonical : THM_M_1011.CanonicalStatement X := by
  intro S
  constructor
  · exact tight_to_compact X S
  · exact isTightMeasureSet_of_isCompact_closure

#print axioms canonical

end Stage1Instances.THM_M_1011.Proof
