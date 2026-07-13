import Statement

/-!
# THM-M-0741 conditional obligation composition

This module checks the target-owned child-to-parent interfaces selected by the
frozen obligation graph. The pinned fixed-input halting theorem and Rice bridge
remain explicit premises. Adopting either imported theorem belongs to the proof
phase, not this obligation-tree phase.
-/

namespace Stage1Instances.THM_M_0741.ObligationTree

open Nat.Partrec

/-- Halting of a code at the normalized input zero. -/
def FixedInputZeroHalts (code : Code) : Prop :=
  (Code.eval code 0).Dom

/-- The exact fixed-input theorem exported by the pinned mathlib candidate. -/
def FixedInputZeroUndecidable : Prop :=
  Not (ComputablePred FixedInputZeroHalts)

/-- Computability of the section which embeds a code at input zero. -/
def PairZeroEmbeddingComputable : Prop :=
  Computable (fun code : Code => (code, 0))

/-- Restriction of a hypothetical pair decider to the input-zero section. -/
def PairToFixedRestriction : Prop :=
  ComputablePred Stage1Instances.THM_M_0741.Halts ->
    ComputablePred FixedInputZeroHalts

/-- The exact reduction interface consumed by the root composition. -/
def FixedInputReduction : Prop :=
  FixedInputZeroUndecidable ->
    Stage1Instances.THM_M_0741.HaltingProblemUndecidable

/-- The central semantic transfer interface supplied by Rice's theorem. -/
def RiceBridge : Prop :=
  forall C : Set (Nat →. Nat),
    ComputablePred (fun code : Code => Code.eval code ∈ C) ->
      forall {f g : Nat →. Nat},
        Nat.Partrec f -> Nat.Partrec g -> f ∈ C -> g ∈ C

/-- Represented positive and negative witnesses for definedness at zero. -/
def FixedZeroWitnessPackage : Prop :=
  exists f g : Nat →. Nat,
    Nat.Partrec f /\ Nat.Partrec g /\ (f 0).Dom /\ Not (g 0).Dom

/-- The computable input-zero section. -/
theorem pairZeroEmbedding_computable : PairZeroEmbeddingComputable := by
  exact Computable.id.pair (Computable.const 0)

/-- Checked restriction of both the decision witness and its computable
Boolean characteristic along the input-zero section. -/
theorem pairToFixedRestriction_of_embedding
    (embedding : PairZeroEmbeddingComputable) : PairToFixedRestriction := by
  intro pairDecider
  obtain ⟨pairDecidable, pairComputable⟩ := pairDecider
  let fixedDecidable : DecidablePred FixedInputZeroHalts :=
    fun code => pairDecidable (code, 0)
  refine ⟨fixedDecidable, ?_⟩
  simpa [fixedDecidable, FixedInputZeroHalts,
    Stage1Instances.THM_M_0741.Halts] using
      pairComputable.comp embedding

/-- Checked normalization from decider restriction to the implication needed
by the exact root. -/
theorem fixedInputReduction_of_restriction
    (restriction : PairToFixedRestriction) : FixedInputReduction := by
  intro fixedInputImpossible pairDecider
  exact fixedInputImpossible (restriction pairDecider)

/-- Concrete witnesses used by the one-line fixed-input halting proof. -/
theorem fixedZeroWitnessPackage : FixedZeroWitnessPackage := by
  refine ⟨fun _ => Part.some 0, fun _ => Part.none, ?_, ?_, ?_, ?_⟩
  · exact Nat.Partrec.zero
  · exact Nat.Partrec.none
  · exact Part.some_dom 0
  · simp

/-- Checked terminal composition from an explicit Rice bridge and explicit
semantic witnesses to the fixed-input theorem. The bridge itself is not
installed here. -/
theorem fixedInputZeroUndecidable_of_rice
    (riceBridge : RiceBridge)
    (witnesses : FixedZeroWitnessPackage) : FixedInputZeroUndecidable := by
  intro fixedDecider
  obtain ⟨f, g, hf, hg, hfDefined, hgUndefined⟩ := witnesses
  apply hgUndefined
  exact riceBridge {partialFunction | (partialFunction 0).Dom}
    fixedDecider hf hg hfDefined

/-- Exact child-to-root composition. Both required children are explicit and
consumed; the pinned fixed-input theorem remains a premise. -/
theorem root_of_reduction_and_fixedInput
    (reduction : FixedInputReduction)
    (fixedInputImpossible : FixedInputZeroUndecidable) :
    Stage1Instances.THM_M_0741.HaltingProblemUndecidable :=
  reduction fixedInputImpossible

#check ComputablePred.rice
#check ComputablePred.halting_problem
#check pairZeroEmbedding_computable
#check pairToFixedRestriction_of_embedding
#check fixedInputReduction_of_restriction
#check fixedZeroWitnessPackage
#check fixedInputZeroUndecidable_of_rice
#check root_of_reduction_and_fixedInput

#print axioms ComputablePred.rice
#print axioms ComputablePred.halting_problem
#print axioms pairZeroEmbedding_computable
#print axioms pairToFixedRestriction_of_embedding
#print axioms fixedInputReduction_of_restriction
#print axioms fixedZeroWitnessPackage
#print axioms fixedInputZeroUndecidable_of_rice
#print axioms root_of_reduction_and_fixedInput

end Stage1Instances.THM_M_0741.ObligationTree
