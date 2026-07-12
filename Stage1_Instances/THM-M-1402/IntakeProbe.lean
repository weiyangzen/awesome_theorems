import Mathlib.Data.Stream.Init
import Mathlib.Topology.Homeomorph.Lemmas
import Mathlib.Dynamics.PeriodicPts.Defs

/-! Discovery-only API checks for a later exact symbolic-shift statement. -/

#check Stream'
#check Stream'.tail
#check Stream'.get_tail
#check continuous_pi
#check continuous_apply
#check Homeomorph.piCongrLeft
#check Pi.continuous_precomp'
#check Function.IsPeriodicPt
