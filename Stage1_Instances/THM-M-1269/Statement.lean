import Mathlib.Topology.Algebra.Ring.Real

open Filter Set Topology

universe u

/-- The exact rev-5.6 target for THM-M-1269.  This is a statement declaration only. -/
def THM_M_1269_statement (X : Type u) (F : X → ℝ) : Prop :=
  Nonempty X →
    BddBelow (Set.range F) →
      ∃ sequence : ℕ → X,
        Tendsto (fun n => F (sequence n)) atTop (nhds (sInf (Set.range F)))

-- Mutation surfaces: these deliberately differ from the canonical declaration.
def THM_M_1269_without_nonempty (X : Type u) (F : X → ℝ) : Prop :=
  BddBelow (Set.range F) →
    ∃ sequence : ℕ → X,
      Tendsto (fun n => F (sequence n)) atTop (nhds (sInf (Set.range F)))

def THM_M_1269_without_bddBelow (X : Type u) (F : X → ℝ) : Prop :=
  Nonempty X →
    ∃ sequence : ℕ → X,
      Tendsto (fun n => F (sequence n)) atTop (nhds (sInf (Set.range F)))

def THM_M_1269_attainment_strengthening (X : Type u) (F : X → ℝ) : Prop :=
  Nonempty X → BddBelow (Set.range F) → ∃ x : X, F x = sInf (Set.range F)

#check THM_M_1269_statement
#check THM_M_1269_without_nonempty
#check THM_M_1269_without_bddBelow
#check THM_M_1269_attainment_strengthening
#print THM_M_1269_statement
