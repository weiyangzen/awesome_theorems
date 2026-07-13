import Mathlib.Combinatorics.SimpleGraph.Matching

set_option autoImplicit false

/-!
# THM-M-0856: exact Tutte 1-factor theorem statement

This module freezes the finite-simple-graph statement only. It deliberately imports the
definitions needed to state the target, rather than the proof-bearing `SimpleGraph.Tutte` module.
-/

namespace Stage1Instances.THM_M_0856

universe u

open SimpleGraph

/-- A direct expansion of the odd-component inequality in Tutte's condition. -/
def OddComponentCondition {V : Type u} (G : SimpleGraph V) : Prop :=
  forall U : Set V,
    ((⊤ : G.Subgraph).deleteVerts U).coe.oddComponents.ncard <= U.ncard

/-- The strict negation of Tutte's odd-component condition. -/
def IsTutteViolator {V : Type u} (G : SimpleGraph V) (U : Set V) : Prop :=
  U.ncard < ((⊤ : G.Subgraph).deleteVerts U).coe.oddComponents.ncard

/-- The exact finite-simple-graph form of Tutte's 1-factor theorem selected at intake. -/
def TutteOneFactorTarget : Prop :=
  forall {V : Type u} (G : SimpleGraph V),
    [Finite V] →
      (Exists fun M : G.Subgraph => M.IsPerfectMatching) ↔ OddComponentCondition G

/-- The same target with the odd-component inequality written inline. -/
def ExpandedTutteOneFactorTarget : Prop :=
  forall {V : Type u} (G : SimpleGraph V),
    [Finite V] →
      (Exists fun M : G.Subgraph => M.IsPerfectMatching) ↔
        forall U : Set V,
          ((⊤ : G.Subgraph).deleteVerts U).coe.oddComponents.ncard ≤ U.ncard

/-- Checked definitional transport to the expanded inequality spelling. -/
theorem tutteOneFactorTarget_iff_expanded :
    TutteOneFactorTarget.{u} ↔ ExpandedTutteOneFactorTarget.{u} :=
  Iff.rfl

/-- The no-violator spelling used by the pinned `SimpleGraph.tutte` interface. -/
def NoTutteViolatorTarget : Prop :=
  forall {V : Type u} (G : SimpleGraph V),
    [Finite V] →
      (Exists fun M : G.Subgraph => M.IsPerfectMatching) ↔
        forall U : Set V, Not (IsTutteViolator G U)

/-- Checked transport between the inequality and no-strict-violator spellings. -/
theorem tutteOneFactorTarget_iff_noTutteViolatorTarget :
    TutteOneFactorTarget.{u} ↔ NoTutteViolatorTarget.{u} := by
  simp only [TutteOneFactorTarget, OddComponentCondition, NoTutteViolatorTarget,
    IsTutteViolator, not_lt]

/-! Structural mutations used only by the statement-identity checker. -/

/-- Removes the finiteness contract on the vertex carrier. -/
def mutationRemovedFiniteness : Prop :=
  forall {V : Type u} (G : SimpleGraph V),
    (Exists fun M : G.Subgraph => M.IsPerfectMatching) ↔ OddComponentCondition G

/-- Changes the graph domain to the complete graph on every finite carrier. -/
def mutationChangedDomainToCompleteGraphs : Prop :=
  forall {V : Type u},
    [Finite V] →
      (Exists fun M : (completeGraph V).Subgraph => M.IsPerfectMatching) ↔
        OddComponentCondition (completeGraph V)

/-- Changes the graph binder from universal scope to existential scope. -/
def mutationChangedGraphBinderScope : Prop :=
  forall {V : Type u},
    [Finite V] →
      Exists fun G : SimpleGraph V =>
        (Exists fun M : G.Subgraph => M.IsPerfectMatching) ↔ OddComponentCondition G

/-- Excludes the empty vertex carrier, which the canonical theorem includes. -/
def mutationExcludedEmptyCarrier : Prop :=
  forall {V : Type u} (G : SimpleGraph V),
    [Finite V] →
      Nonempty V →
        ((Exists fun M : G.Subgraph => M.IsPerfectMatching) ↔ OddComponentCondition G)

#check_failure (rfl : TutteOneFactorTarget.{u} = mutationRemovedFiniteness.{u})
#check_failure (rfl : TutteOneFactorTarget.{u} = mutationChangedDomainToCompleteGraphs.{u})
#check_failure (rfl : TutteOneFactorTarget.{u} = mutationChangedGraphBinderScope.{u})
#check_failure (rfl : TutteOneFactorTarget.{u} = mutationExcludedEmptyCarrier.{u})

#check tutteOneFactorTarget_iff_expanded
#check tutteOneFactorTarget_iff_noTutteViolatorTarget
#print axioms tutteOneFactorTarget_iff_expanded
#print axioms tutteOneFactorTarget_iff_noTutteViolatorTarget

end Stage1Instances.THM_M_0856

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0856.TutteOneFactorTarget
