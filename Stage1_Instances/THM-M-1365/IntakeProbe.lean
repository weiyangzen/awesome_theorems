import Mathlib.Data.Stream.Init
import Mathlib.Dynamics.PeriodicPts.Defs
import Mathlib.Topology.Homeomorph.Defs

/-!
# THM-M-1365 discovery-only intake probe

These checks authenticate generic pinned symbolic-dynamics interfaces. They neither define a
horseshoe map nor select or prove any Smale-horseshoe theorem.
-/

#check Stream'
#check Stream'.tail
#check Stream'.get_tail
#check Function.Semiconj
#check Function.Semiconj.iterate_right
#check Function.Semiconj.mapsTo_periodicPts
#check Function.IsPeriodicPt
#check Homeomorph
