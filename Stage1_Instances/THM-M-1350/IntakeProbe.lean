import Mathlib.Analysis.Complex.CoveringMap
import Mathlib.Analysis.SpecialFunctions.Complex.CircleMap
import Mathlib.Topology.Homotopy.Lifting

/-!
# THM-M-1350 discovery-only intake probe

These checks authenticate pinned path, homotopy, covering-map, and complex-circle interfaces that
could support a later source-selected encoding of a curve index. They do not define an index,
select one of the catalog's possible meanings, state THM-M-1350, or prove it.
-/

#check Path
#check Path.Homotopic
#check IsCoveringMap.liftPath
#check IsCoveringMap.liftPath_lifts
#check Complex.isCoveringMap_exp
#check circleMap
#check periodic_circleMap
#check circleMap_mem_sphere'
