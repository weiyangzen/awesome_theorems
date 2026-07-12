import Mathlib.Data.Setoid.Partition
import Mathlib.Data.Stream.Init
import Mathlib.Dynamics.PeriodicPts.Defs

/-! Generic API checks only; this file states no Markov-partition theorem. -/

#check Setoid.IsPartition
#check Setoid.IsPartition.pairwiseDisjoint
#check Stream'
#check Stream'.tail
#check Function.Semiconj
#check Function.Semiconj.iterate_right
#check Function.Semiconj.mapsTo_periodicPts
