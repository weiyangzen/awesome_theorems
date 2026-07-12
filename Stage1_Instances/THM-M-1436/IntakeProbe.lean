import Mathlib.Dynamics.PeriodicPts.Defs
import Mathlib.Topology.ContinuousMap.Basic
import Mathlib.Topology.Homeomorph.Defs

/-!
# THM-M-1436 discovery-only intake probe

These checks authenticate generic pinned APIs for iteration, changes of coordinates, fixed and
periodic points, and continuous maps. They neither define a renormalization operator nor select or
prove a theorem about one.
-/

#check Function.iterate_succ_apply
#check Function.iterate_add_apply
#check Function.Semiconj
#check Function.Semiconj.iterate_right
#check Function.Commute.iterate_iterate
#check Function.IsFixedPt
#check Function.IsFixedPt.map
#check Function.IsPeriodicPt
#check Function.IsPeriodicPt.map
#check Homeomorph.trans
#check Homeomorph.trans_apply
#check ContinuousMap.comp
#check ContinuousMap.comp_apply
