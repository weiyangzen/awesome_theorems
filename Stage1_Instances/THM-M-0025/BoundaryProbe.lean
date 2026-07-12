import Mathlib.Algebra.Polynomial.Basic
import Mathlib.RingTheory.Noetherian.Defs

example : CommRing PUnit := inferInstance

example : IsNoetherianRing PUnit :=
  (isNoetherianRing_iff_ideal_fg PUnit).2 fun I => by
    rw [Subsingleton.elim I ⊥]
    exact Submodule.fg_bot

example : (0 : PUnit) = 1 := rfl
