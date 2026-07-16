import Statement

/-!
# THM-M-0115 proof-phase consistency check

The frozen statement stores each semantic compatibility assertion as an
unconnected proposition.  Consequently those assertions do not constrain the
operations appearing in the GRR formula.  The concrete datum below satisfies
every frozen hypothesis while making the two sides of the formula unequal.

This refutes only the current abstract encoding, not the mathematical
Grothendieck-Riemann-Roch theorem.  It is a proof-phase blocker: a positive body
for the frozen target cannot exist in a consistent kernel.
-/

noncomputable section

open CategoryTheory AlgebraicGeometry

namespace Stage1Instances.THMM0115.Proof

/-- A concrete model exposing that the frozen semantic propositions do not
constrain any of the operations in the formula. -/
def counterexampleData :
    GrothendieckRiemannRochData.{0, 0} Rat where
  X := SpecOf Rat
  Y := SpecOf Rat
  sourceStructureMap := 𝟙 _
  targetStructureMap := 𝟙 _
  map := 𝟙 _
  sourceIsVarietyOverBase := True
  targetIsVarietyOverBase := True
  sourceIsQuasiProjectiveOverBase := True
  targetIsQuasiProjectiveOverBase := True
  KZero := fun _ => Int
  ChowHomologyQ := fun _ => Int
  kTheoryPushforward := id
  chowPushforward := id
  chernCharacterX := id
  chernCharacterY := id
  tangentClassX := Unit
  tangentClassY := Unit
  toddClassX := fun _ => 0
  toddClassY := fun _ => 0
  tangentBundleX := ()
  tangentBundleY := ()
  capX := fun _ _ => 0
  capY := fun _ _ => 1
  kZeroModelsGrothendieckGroup := True
  chowHomologyQModelsRationalChowHomology := True
  kTheoryPushforwardModelsProperPushforward := True
  chowPushforwardModelsProperPushforward := True
  chernCharactersModelChernCharacter := True
  tangentClassesModelTangentBundles := True
  toddClassesModelToddClasses := True
  capActionsModelChowCapProduct := True

/-- Every hypothesis of the frozen target holds for `counterexampleData`. -/
theorem counterexampleData_hypotheses :
    counterexampleData.Hypotheses := by
  letI : IsFinite (𝟙 (SpecOf Rat)) := inferInstance
  letI : IsProper (𝟙 (SpecOf Rat)) := inferInstance
  letI : IsOpenImmersion (𝟙 (SpecOf Rat)) := inferInstance
  letI : Smooth (𝟙 (SpecOf Rat)) := inferInstance
  change
    (𝟙 (SpecOf Rat) = 𝟙 (SpecOf Rat) ≫ 𝟙 (SpecOf Rat)) ∧
      True ∧ True ∧ Smooth (𝟙 (SpecOf Rat)) ∧
        Smooth (𝟙 (SpecOf Rat)) ∧ True ∧ True ∧
          IsProper (𝟙 (SpecOf Rat)) ∧ True ∧ True ∧ True ∧ True ∧
            True ∧ True ∧ True ∧ True
  exact ⟨by simp, trivial, trivial, inferInstance, inferInstance, trivial,
    trivial, inferInstance, trivial, trivial, trivial, trivial, trivial,
    trivial, trivial, trivial⟩

/-- The exact frozen target is false because its semantic compatibility
propositions do not constrain the formula operations. -/
theorem not_grothendieckRiemannRochTarget :
    ¬ GrothendieckRiemannRochTarget.{0, 0} := by
  intro target
  have formula := target Rat counterexampleData counterexampleData_hypotheses (0 : Int)
  change (1 : Int) = 0 at formula
  norm_num at formula

#check counterexampleData_hypotheses
#check not_grothendieckRiemannRochTarget
#print axioms counterexampleData_hypotheses
#print axioms not_grothendieckRiemannRochTarget
#print sorries counterexampleData_hypotheses
#print sorries not_grothendieckRiemannRochTarget

end Stage1Instances.THMM0115.Proof
