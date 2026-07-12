import Mathlib.ModelTheory.Satisfiability

/-!
# THM-M-0657: exact Morley categoricity statement

This module freezes the statement boundary only. It does not prove Morley's
categoricity theorem.
-/

namespace Stage1Instances.THM_M_0657

open FirstOrder FirstOrder.Language

universe u v w

/-- A theory has a nonempty bundled model of exactly the specified cardinality. -/
def HasModelCardinality (L : Language.{u, v}) (T : L.Theory) (kappa : Cardinal.{w}) : Prop :=
  Exists fun M : Theory.ModelType.{u, v, w} T => Cardinal.mk M = kappa

/-- Categoricity with existence made explicit, so an empty cardinal slice cannot
satisfy the definition vacuously. -/
def CategoricalWithExistence (L : Language.{u, v}) (T : L.Theory)
    (kappa : Cardinal.{w}) : Prop :=
  HasModelCardinality L T kappa ∧ Cardinal.Categorical kappa T

/-- The exact intake-selected form of Morley's categoricity theorem: for a
countable first-order language, categoricity in one uncountable cardinal
transfers to every uncountable cardinal. -/
def MorleyCategoricityTarget : Prop :=
  ∀ (L : Language.{u, v}) (T : L.Theory),
    L.card ≤ Cardinal.aleph0 →
    ∀ kappa : Cardinal.{w}, Cardinal.aleph0 < kappa →
      CategoricalWithExistence L T kappa →
      ∀ lambda : Cardinal.{w}, Cardinal.aleph0 < lambda →
        CategoricalWithExistence L T lambda

/-- Equivalent existential-source-cardinal presentation of the canonical root. -/
def ExistentialSourceShape : Prop :=
  ∀ (L : Language.{u, v}) (T : L.Theory),
    L.card ≤ Cardinal.aleph0 →
    (∃ kappa : Cardinal.{w}, Cardinal.aleph0 < kappa ∧
      CategoricalWithExistence L T kappa) →
    ∀ lambda : Cardinal.{w}, Cardinal.aleph0 < lambda →
      CategoricalWithExistence L T lambda

/-- Checked transport between the curried and existential source-cardinal forms. -/
theorem morleyCategoricityTarget_iff_existentialSourceShape :
    MorleyCategoricityTarget.{u, v, w} ↔ ExistentialSourceShape.{u, v, w} := by
  constructor
  · intro h L T hL hex lambda hlambda
    obtain ⟨kappa, hkappa, hcat⟩ := hex
    exact h L T hL kappa hkappa hcat lambda hlambda
  · intro h L T hL kappa hkappa hcat
    exact h L T hL ⟨kappa, hkappa, hcat⟩

-- Structural mutations elaborated and distinguished by `check_statement.py`.
def mutationRemovedCountableLanguage : Prop :=
  ∀ (L : Language.{u, v}) (T : L.Theory),
    ∀ kappa : Cardinal.{w}, Cardinal.aleph0 < kappa →
      CategoricalWithExistence L T kappa →
      ∀ lambda : Cardinal.{w}, Cardinal.aleph0 < lambda →
        CategoricalWithExistence L T lambda

def mutationChangedCardinalDomain : Prop :=
  ∀ (L : Language.{u, v}) (T : L.Theory),
    L.card ≤ Cardinal.aleph0 →
    ∀ kappa : Cardinal.{w}, Cardinal.aleph0 ≤ kappa →
      CategoricalWithExistence L T kappa →
      ∀ lambda : Cardinal.{w}, Cardinal.aleph0 ≤ lambda →
        CategoricalWithExistence L T lambda

def mutationChangedBinderScope : Prop :=
  ∀ (L : Language.{u, v}), L.card ≤ Cardinal.aleph0 →
    ∀ kappa : Cardinal.{w}, Cardinal.aleph0 < kappa →
      (∀ T : L.Theory, CategoricalWithExistence L T kappa) →
      ∀ lambda : Cardinal.{w}, Cardinal.aleph0 < lambda →
        ∀ T : L.Theory,
          CategoricalWithExistence L T lambda

def mutationAllowsCountableTarget : Prop :=
  ∀ (L : Language.{u, v}) (T : L.Theory),
    L.card ≤ Cardinal.aleph0 →
    ∀ kappa : Cardinal.{w}, Cardinal.aleph0 < kappa →
      CategoricalWithExistence L T kappa →
      CategoricalWithExistence L T (Cardinal.aleph0 : Cardinal.{w})

/-- The existence conjunct is available independently of uniqueness. -/
theorem categoricalWithExistence_hasModel {L : Language.{u, v}} {T : L.Theory}
    {kappa : Cardinal.{w}} (h : CategoricalWithExistence L T kappa) :
    HasModelCardinality L T kappa :=
  h.1

/-- The countably infinite cardinal is outside the strict target range. -/
theorem aleph0_not_uncountable : ¬ Cardinal.aleph0 < Cardinal.aleph0 :=
  lt_irrefl _

end Stage1Instances.THM_M_0657

set_option pp.explicit true in
#print Stage1Instances.THM_M_0657.MorleyCategoricityTarget
