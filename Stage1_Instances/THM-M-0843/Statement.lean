import Mathlib.Combinatorics.SimpleGraph.Regularity.Bound
import Mathlib.Combinatorics.SimpleGraph.Regularity.Uniform

/-!
# THM-M-0843: Szemeredi regularity statement

This module freezes the effective Lean-facing formulation displayed by
Dillies and Mehta. It also checks its one-way transport to the conventional
existential-bound form. It deliberately does not import the proof-bearing
regularity-lemma module.
-/

namespace Stage1Instances.THM_M_0843

universe u

/--
The effective equitable form of Szemeredi's regularity lemma.

For every finite simple graph, positive real tolerance, and requested lower
bound no larger than the vertex count, there is an equitable uniform partition
of all vertices whose number of parts lies between the requested lower bound
and the graph-independent explicit bound.
-/
def SzemerediRegularityTarget : Prop :=
  ∀ {alpha : Type u} [DecidableEq alpha] [Fintype alpha]
    (G : SimpleGraph alpha) [DecidableRel G.Adj] {epsilon : Real} {l : Nat},
    0 < epsilon ->
    l <= Fintype.card alpha ->
    ∃ P : Finpartition (Finset.univ : Finset alpha),
      P.IsEquipartition /\
      l <= P.parts.card /\
      P.parts.card <= SzemerediRegularity.bound epsilon l /\
      P.IsUniform G epsilon

/--
The conventional existential-bound form, using the same checked uniformity
predicate as the effective target.
-/
def ExistentialBoundTarget : Prop :=
  ∀ (epsilon : Real) (l : Nat), 0 < epsilon ->
    ∃ L : Nat, ∀ {alpha : Type u} [DecidableEq alpha] [Fintype alpha]
      (G : SimpleGraph alpha) [DecidableRel G.Adj],
      l <= Fintype.card alpha ->
      ∃ P : Finpartition (Finset.univ : Finset alpha),
        P.IsEquipartition /\
        l <= P.parts.card /\
        P.parts.card <= L /\
        P.IsUniform G epsilon

/-- The effective target implies the conventional existential-bound form. -/
theorem szemerediRegularityTarget_implies_existentialBoundTarget :
    SzemerediRegularityTarget.{u} -> ExistentialBoundTarget.{u} := by
  intro hTarget epsilon l hEpsilon
  refine ⟨SzemerediRegularity.bound epsilon l, ?_⟩
  intro alpha _ _ G _ hCard
  exact hTarget G hEpsilon hCard

/-! Structural mutations used only by the statement-identity checker. -/

/-- Removed-hypothesis mutation: positivity of the tolerance is absent. -/
def mutationRemovedPositiveTolerance : Prop :=
  ∀ {alpha : Type u} [DecidableEq alpha] [Fintype alpha]
    (G : SimpleGraph alpha) [DecidableRel G.Adj] {epsilon : Real} {l : Nat},
    l <= Fintype.card alpha ->
    ∃ P : Finpartition (Finset.univ : Finset alpha),
      P.IsEquipartition /\
      l <= P.parts.card /\
      P.parts.card <= SzemerediRegularity.bound epsilon l /\
      P.IsUniform G epsilon

/-- Changed-domain mutation: the tolerance and uniformity predicate are rational. -/
def mutationRationalTolerance : Prop :=
  ∀ {alpha : Type u} [DecidableEq alpha] [Fintype alpha]
    (G : SimpleGraph alpha) [DecidableRel G.Adj] {epsilon : Rat} {l : Nat},
    0 < epsilon ->
    l <= Fintype.card alpha ->
    ∃ P : Finpartition (Finset.univ : Finset alpha),
      P.IsEquipartition /\
      l <= P.parts.card /\
      P.parts.card <= SzemerediRegularity.bound (epsilon : Real) l /\
      P.IsUniform G epsilon

/-- Changed-scope mutation: the requested lower bound becomes existential. -/
def mutationExistentialLowerBound : Prop :=
  ∀ {alpha : Type u} [DecidableEq alpha] [Fintype alpha]
    (G : SimpleGraph alpha) [DecidableRel G.Adj] {epsilon : Real},
    0 < epsilon ->
    ∃ l : Nat, l <= Fintype.card alpha /\
      ∃ P : Finpartition (Finset.univ : Finset alpha),
        P.IsEquipartition /\
        l <= P.parts.card /\
        P.parts.card <= SzemerediRegularity.bound epsilon l /\
        P.IsUniform G epsilon

/-- Boundary mutation: the valid `l = 0` input is excluded. -/
def mutationPositiveLowerBoundOnly : Prop :=
  ∀ {alpha : Type u} [DecidableEq alpha] [Fintype alpha]
    (G : SimpleGraph alpha) [DecidableRel G.Adj] {epsilon : Real} {l : Nat},
    0 < l ->
    0 < epsilon ->
    l <= Fintype.card alpha ->
    ∃ P : Finpartition (Finset.univ : Finset alpha),
      P.IsEquipartition /\
      l <= P.parts.card /\
      P.parts.card <= SzemerediRegularity.bound epsilon l /\
      P.IsUniform G epsilon

#check_failure
  (rfl : SzemerediRegularityTarget.{u} = mutationRemovedPositiveTolerance.{u})
#check_failure
  (rfl : SzemerediRegularityTarget.{u} = mutationRationalTolerance.{u})
#check_failure
  (rfl : SzemerediRegularityTarget.{u} = mutationExistentialLowerBound.{u})
#check_failure
  (rfl : SzemerediRegularityTarget.{u} = mutationPositiveLowerBoundOnly.{u})

#print axioms Stage1Instances.THM_M_0843.szemerediRegularityTarget_implies_existentialBoundTarget

end Stage1Instances.THM_M_0843

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1Instances.THM_M_0843.SzemerediRegularityTarget
