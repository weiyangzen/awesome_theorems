import Statement
import Mathlib.MeasureTheory.Measure.Prokhorov
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1011 same-worker differential validation

This module deliberately imports neither `Proof` nor `ObligationTree`. It
independently reconstructs the quotient transport used to prove the exact
frozen root. This is a differential kernel check in the same worker and over
the same mathlib bodies, not a distinct-runner attestation or a second
independent mathematical proof.
-/

noncomputable section

open MeasureTheory Set Topology

namespace Stage1Instances.THM_M_1011.Validation

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

private noncomputable def chooseRepresentative : SeparationQuotient X -> X :=
  Function.surjInv (SeparationQuotient.surjective_mk (X := X))

omit [MeasurableSpace X] [BorelSpace X] [SecondCountableTopology X] [CompleteSpace X] in
private theorem mk_chooseRepresentative (z : SeparationQuotient X) :
    SeparationQuotient.mk (chooseRepresentative X z) = z :=
  Function.surjInv_eq _ z

omit [MeasurableSpace X] [BorelSpace X] [SecondCountableTopology X] [CompleteSpace X] in
private theorem continuous_chooseRepresentative : Continuous (chooseRepresentative X) := by
  apply SeparationQuotient.isInducing_mk.continuous_iff.2
  simpa only [Function.comp_def, mk_chooseRepresentative] using
    (continuous_id : Continuous (id : SeparationQuotient X -> SeparationQuotient X))

private noncomputable def toQuotient :
    ProbabilityMeasure X -> ProbabilityMeasure (SeparationQuotient X) :=
  fun P => P.map SeparationQuotient.continuous_mk.measurable.aemeasurable

private noncomputable def fromQuotient :
    ProbabilityMeasure (SeparationQuotient X) -> ProbabilityMeasure X :=
  fun P => P.map (continuous_chooseRepresentative X).measurable.aemeasurable

omit [SecondCountableTopology X] [CompleteSpace X] in
private theorem continuous_toQuotient : Continuous (toQuotient X) :=
  ProbabilityMeasure.continuous_map SeparationQuotient.continuous_mk

omit [SecondCountableTopology X] [CompleteSpace X] in
private theorem continuous_fromQuotient : Continuous (fromQuotient X) :=
  ProbabilityMeasure.continuous_map (continuous_chooseRepresentative X)

omit [SecondCountableTopology X] [CompleteSpace X] in
private theorem fromQuotient_toQuotient (P : ProbabilityMeasure X) :
    fromQuotient X (toQuotient X P) = P := by
  apply ProbabilityMeasure.toMeasure_injective
  simp only [fromQuotient, toQuotient, ProbabilityMeasure.toMeasure_map]
  rw [Measure.map_map (continuous_chooseRepresentative X).measurable
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
        (mk_chooseRepresentative X (SeparationQuotient.mk x))) hA
  · exact (continuous_chooseRepresentative X).measurable.comp
      SeparationQuotient.continuous_mk.measurable
  · exact hA

omit [SecondCountableTopology X] [CompleteSpace X] in
private theorem toQuotient_fromQuotient
    (P : ProbabilityMeasure (SeparationQuotient X)) :
    toQuotient X (fromQuotient X P) = P := by
  apply ProbabilityMeasure.toMeasure_injective
  simp only [fromQuotient, toQuotient, ProbabilityMeasure.toMeasure_map]
  rw [Measure.map_map SeparationQuotient.continuous_mk.measurable
    (continuous_chooseRepresentative X).measurable]
  simpa only [Function.comp_def, mk_chooseRepresentative] using
    (Measure.map_id (μ := (P : Measure (SeparationQuotient X))))

private noncomputable def probabilityMeasureEquiv :
    ProbabilityMeasure X ≃ₜ ProbabilityMeasure (SeparationQuotient X) where
  toEquiv := {
    toFun := toQuotient X
    invFun := fromQuotient X
    left_inv := fromQuotient_toQuotient X
    right_inv := toQuotient_fromQuotient X
  }
  continuous_toFun := continuous_toQuotient X
  continuous_invFun := continuous_fromQuotient X

omit [SecondCountableTopology X] [CompleteSpace X] in
private theorem mappedUnderlyingMeasures (S : Set (ProbabilityMeasure X)) :
    THM_M_1011.underlyingMeasures (toQuotient X '' S) =
      Measure.map SeparationQuotient.mk '' THM_M_1011.underlyingMeasures S := by
  ext m
  constructor
  · rintro ⟨Q, ⟨P, hPS, rfl⟩, rfl⟩
    exact ⟨(P : Measure X), ⟨P, hPS, rfl⟩, rfl⟩
  · rintro ⟨m, ⟨P, hPS, rfl⟩, rfl⟩
    exact ⟨toQuotient X P, ⟨P, hPS, rfl⟩, rfl⟩

omit [SecondCountableTopology X] [CompleteSpace X] in
private theorem mappedTightness (S : Set (ProbabilityMeasure X))
    (hS : THM_M_1011.IsUniformlyTight S) :
    THM_M_1011.IsUniformlyTight (toQuotient X '' S) := by
  rw [THM_M_1011.IsUniformlyTight, mappedUnderlyingMeasures]
  exact hS.map SeparationQuotient.continuous_mk

omit [SecondCountableTopology X] [CompleteSpace X] in
private theorem compactClosureEquiv (S : Set (ProbabilityMeasure X)) :
    IsCompact (closure S) <-> IsCompact (closure (toQuotient X '' S)) := by
  rw [<- (probabilityMeasureEquiv X).isCompact_image]
  rw [(probabilityMeasureEquiv X).image_closure]
  rfl

/-- A separately written reconstruction of the exact frozen Prokhorov root. -/
theorem independentlyReconstructedCanonical : THM_M_1011.CanonicalStatement X := by
  intro S
  constructor
  · intro hS
    apply (compactClosureEquiv X S).2
    exact isCompact_closure_of_isTightMeasureSet (mappedTightness X S hS)
  · exact isTightMeasureSet_of_isCompact_closure

#check independentlyReconstructedCanonical
assert_no_sorry independentlyReconstructedCanonical
assert_no_sorry isCompact_closure_of_isTightMeasureSet
assert_no_sorry isTightMeasureSet_of_isCompact_closure
#print sorries independentlyReconstructedCanonical
#print axioms independentlyReconstructedCanonical
#print axioms isCompact_closure_of_isTightMeasureSet
#print axioms isTightMeasureSet_of_isCompact_closure

end Stage1Instances.THM_M_1011.Validation
