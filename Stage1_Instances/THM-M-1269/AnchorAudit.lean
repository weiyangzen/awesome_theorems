import Mathlib.Topology.Algebra.Ring.Real

open Filter Set Topology

universe u

/-! A scoped applicability check for the pinned mathlib anchor.  This is audit
evidence, not the canonical proof-phase declaration. -/
example (X : Type u) (F : X → ℝ) :
    Nonempty X →
      BddBelow (Set.range F) →
        ∃ sequence : ℕ → X,
          Tendsto (fun n => F (sequence n)) atTop (nhds (sInf (Set.range F))) := by
  intro hX hbelow
  obtain ⟨values, _, hvalues, hmem⟩ :=
    exists_seq_tendsto_sInf (Set.range_nonempty F) hbelow
  choose sequence hsequence using hmem
  have heq : (fun n => F (sequence n)) = values := funext hsequence
  exact ⟨sequence, heq ▸ hvalues⟩

#check exists_seq_tendsto_sInf
#print axioms exists_seq_tendsto_sInf
