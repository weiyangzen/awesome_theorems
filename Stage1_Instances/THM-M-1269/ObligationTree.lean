import Mathlib.Topology.Algebra.Ring.Real

open Filter Set Topology

universe u

def THM_M_1269_statement (X : Type u) (F : X -> Real) : Prop :=
  Nonempty X -> BddBelow (Set.range F) ->
    exists sequence : Nat -> X,
      Tendsto (fun n => F (sequence n)) atTop (nhds (sInf (Set.range F)))

/-!
# THM-M-1269 conditional obligation composition

This file checks the composition boundary selected by the frozen obligation
architecture. The range-approximation package remains an explicit premise, so
this module does not install the canonical proof-phase declaration.
-/

/-- The exact output expected from the pinned infimum-sequence bridge. -/
def THM_M_1269_RangeApproximation (F : X -> Real) : Prop :=
  exists values : Nat -> Real,
    Tendsto values atTop (nhds (sInf (Set.range F))) /\
      forall n, values n ∈ Set.range F

/-- Checked choice of preimages and transport of convergence back to `F`. -/
theorem THM_M_1269_root_of_rangeApproximation
    (X : Type u) (F : X -> Real)
    (happrox : Nonempty X -> BddBelow (Set.range F) ->
      THM_M_1269_RangeApproximation F) :
    THM_M_1269_statement X F := by
  intro hX hbelow
  obtain ⟨values, hvalues, hmem⟩ := happrox hX hbelow
  choose sequence hsequence using hmem
  have heq : (fun n => F (sequence n)) = values := funext hsequence
  exact ⟨sequence, heq ▸ hvalues⟩

#check exists_seq_tendsto_sInf
#print axioms THM_M_1269_root_of_rangeApproximation
