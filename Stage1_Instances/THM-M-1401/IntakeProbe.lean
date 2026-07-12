import Mathlib.Data.Stream.Init
import Mathlib.Dynamics.PeriodicPts.Defs

/-! Bounded API checks only; this file states no symbolic-dynamics theorem. -/

#check Stream'
#check Stream'.tail
#check Stream'.get_tail
#check Function.Semiconj
#check Function.Semiconj.iterate_right
#check Function.Semiconj.mapsTo_periodicPts
