import Mathlib.SetTheory.Cardinal.SchroederBernstein

/-!
# THM-M-0768 pinned anchor audit

This file checks the exact mathlib candidate through a local wrapper. It is
candidate-audit evidence only; downstream obligation, proof, and release gates
remain separate.
-/

namespace Stage1Instances.THM_M_0768.AnchorAudit

universe u v

/-- The frozen raw-function target, repeated here without importing a proof artifact. -/
def AuditedTarget : Prop :=
  forall {alpha : Type u} {beta : Type v} {f : alpha -> beta} {g : beta -> alpha},
    Function.Injective f -> Function.Injective g ->
      exists h : alpha -> beta, Function.Bijective h

/-- Exact checked wrapper around the terminal theorem in pinned mathlib. -/
theorem pinnedSchroederBernstein : AuditedTarget.{u, v} := by
  intro alpha beta f g hf hg
  exact Function.Embedding.schroeder_bernstein hf hg

#check Function.Embedding.schroeder_bernstein
#check Function.Embedding.schroeder_bernstein_of_rel
#check Function.Embedding.antisymm
#print axioms Function.Embedding.schroeder_bernstein
#print axioms pinnedSchroederBernstein

end Stage1Instances.THM_M_0768.AnchorAudit
