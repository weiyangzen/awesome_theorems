import Statement
import Mathlib.Combinatorics.SimpleGraph.Regularity.Lemma

/-!
# THM-M-0843 obligation composition harness

This module gives the frozen root and the pinned mathlib terminal separate
interfaces, then checks that the adapter consumes both required root children.
The remaining obligation nodes describe the internal proof architecture of
`szemeredi_regularity`; they receive no separate closure credit here.
-/

namespace Stage1Instances.THM_M_0843_Obligations

open Finpartition Finset Fintype Function SzemerediRegularity

universe u

/-- Literal proposition delivered by the pinned terminal declaration. -/
def MathlibTerminal : Prop :=
  ∀ {alpha : Type u} [DecidableEq alpha] [Fintype alpha]
    (G : SimpleGraph alpha) [DecidableRel G.Adj] {epsilon : Real} {l : Nat},
    0 < epsilon ->
    l <= Fintype.card alpha ->
    ∃ P : Finpartition (Finset.univ : Finset alpha),
      P.IsEquipartition /\
      l <= P.parts.card /\
      P.parts.card <= SzemerediRegularity.bound epsilon l /\
      P.IsUniform G epsilon

/-- Checked transport from the terminal interface to the frozen statement. -/
theorem terminal_adapter :
    MathlibTerminal.{u} ->
      Stage1Instances.THM_M_0843.SzemerediRegularityTarget.{u} := by
  intro terminal alpha _ _ G _ epsilon l hEpsilon hCard
  exact terminal G hEpsilon hCard

/-- The actual pinned terminal candidate, with terminal-body provenance kept
at `szemeredi_regularity` rather than duplicated at this wrapper. -/
theorem pinned_mathlib_terminal : MathlibTerminal.{u} := by
  intro alpha _ _ G _ epsilon l hEpsilon hCard
  exact szemeredi_regularity G hEpsilon hCard

/-- Root composition certificate. Both graph children are explicit and used. -/
theorem compose_root
    (adapter : MathlibTerminal.{u} ->
      Stage1Instances.THM_M_0843.SzemerediRegularityTarget.{u})
    (terminal : MathlibTerminal.{u}) :
    Stage1Instances.THM_M_0843.SzemerediRegularityTarget.{u} :=
  adapter terminal

#check SzemerediRegularity.bound
#check Finpartition.exists_equipartition_card_eq
#check Finpartition.bot_isEquipartition
#check Finpartition.bot_isUniform
#check Finpartition.energy_nonneg
#check Finpartition.energy_le_one
#check SzemerediRegularity.increment
#check SzemerediRegularity.card_increment
#check SzemerediRegularity.increment_isEquipartition
#check SzemerediRegularity.energy_increment
#check szemeredi_regularity
#check terminal_adapter
#check pinned_mathlib_terminal
#check compose_root

#print sorries szemeredi_regularity
#print axioms szemeredi_regularity
#print axioms terminal_adapter
#print axioms pinned_mathlib_terminal
#print axioms compose_root

end Stage1Instances.THM_M_0843_Obligations
