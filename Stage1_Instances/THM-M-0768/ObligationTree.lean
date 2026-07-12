import Statement

/-!
# THM-M-0768 conditional obligation composition

This module checks the composition selected by the frozen architecture.  The
relational package is an explicit premise, so this file gives it no proof
credit and does not claim the canonical theorem.
-/

namespace Stage1Instances.THM_M_0768

open Function

universe u v

/-- Exact interface of the stronger relational bridge used by pinned mathlib. -/
def RelationalPackage : Prop :=
  forall {alpha : Type u} {beta : Type v} {f : alpha -> beta} {g : beta -> alpha},
    Injective f -> Injective g ->
      forall (R : alpha -> beta -> Prop),
        (forall a, R a (f a)) -> (forall b, R (g b) b) ->
          exists h : alpha -> beta, Bijective h /\ forall a, R a (h a)

/-- Checked specialization of the stronger relational bridge to `True`. -/
theorem root_of_relational_package
    (bridge : RelationalPackage.{u, v}) : CantorBernsteinSchroederTarget.{u, v} := by
  intro alpha beta f g hf hg
  obtain ⟨h, hh, _⟩ := bridge hf hg (fun _ _ => True) (fun _ => trivial) (fun _ => trivial)
  exact ⟨h, hh⟩

#print axioms root_of_relational_package

end Stage1Instances.THM_M_0768
