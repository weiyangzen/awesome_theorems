import Statement
import Mathlib.Combinatorics.SimpleGraph.Tutte

set_option autoImplicit false

/-!
# THM-M-0856 obligation composition harness

This module gives the pinned mathlib terminal proposition and the frozen local target separate
interfaces. It checks the exact adapter and a root composition that consumes both required root
children. The internal obligation tree is a source-body decomposition plan; those internal
child-to-parent compositions remain deliberately unproved in this phase.
-/

namespace Stage1Instances.THM_M_0856.ObligationTree

universe u

open SimpleGraph

/-- The literal no-violator proposition delivered by the pinned terminal declaration. -/
def MathlibTerminal : Prop :=
  forall {V : Type u} (G : SimpleGraph V),
    [Finite V] ->
      (Exists fun M : G.Subgraph => M.IsPerfectMatching) <->
        forall U : Set V, Not (G.IsTutteViolator U)

/-- Checked transport from the pinned terminal interface to the exact frozen inequality target. -/
theorem terminal_adapter :
    MathlibTerminal.{u} -> Stage1Instances.THM_M_0856.TutteOneFactorTarget.{u} := by
  intro terminal V G _
  simpa only [Stage1Instances.THM_M_0856.TutteOneFactorTarget,
    Stage1Instances.THM_M_0856.OddComponentCondition, SimpleGraph.IsTutteViolator, not_lt]
    using (terminal G)

/-- The actual pinned terminal candidate. Its proof body remains owned by pinned mathlib. -/
theorem pinned_mathlib_terminal : MathlibTerminal.{u} := by
  intro V G _
  exact SimpleGraph.tutte (G := G)

/-- Exact root composition. Both graph children are explicit and consumed. -/
theorem compose_root
    (adapter : MathlibTerminal.{u} ->
      Stage1Instances.THM_M_0856.TutteOneFactorTarget.{u})
    (terminal : MathlibTerminal.{u}) :
    Stage1Instances.THM_M_0856.TutteOneFactorTarget.{u} :=
  adapter terminal

#check @SimpleGraph.not_isTutteViolator_of_isPerfectMatching
#check @SimpleGraph.IsTutteViolator.empty
#check @SimpleGraph.exists_isTutteViolator
#check @SimpleGraph.tutte
#check terminal_adapter
#check pinned_mathlib_terminal
#check compose_root

#print sorries SimpleGraph.tutte
#print sorries pinned_mathlib_terminal
#print axioms SimpleGraph.not_isTutteViolator_of_isPerfectMatching
#print axioms SimpleGraph.exists_isTutteViolator
#print axioms SimpleGraph.tutte
#print axioms terminal_adapter
#print axioms pinned_mathlib_terminal
#print axioms compose_root

end Stage1Instances.THM_M_0856.ObligationTree

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0856.TutteOneFactorTarget
