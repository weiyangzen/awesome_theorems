import Mathlib.RingTheory.Finiteness.Basic

example : CommRing PUnit := inferInstance

example : forall I : Ideal PUnit, I.FG := fun I => by
  rw [Subsingleton.elim I ⊥]
  exact Submodule.fg_bot

example : (0 : PUnit) = 1 := rfl
