import Mathlib.SetTheory.Cardinal.SchroederBernstein

open Function

universe u v

#check Function.Embedding.schroeder_bernstein
#check Function.Embedding.antisymm
#check Function.Embedding.schroeder_bernstein_of_rel

-- Proposition-only spelling used to check the intake crosswalk, not a proof declaration.
#check (show Prop from
  ∀ {α : Type u} {β : Type v} {f : α → β} {g : β → α},
    Injective f → Injective g → ∃ h : α → β, Bijective h)

