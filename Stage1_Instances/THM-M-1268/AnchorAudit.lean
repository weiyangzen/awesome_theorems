import Mathlib.Analysis.LocallyConvex.WeakSpace
import Mathlib.Topology.Semicontinuity.Basic
import Mathlib.Data.EReal.Basic

/-!
# THM-M-1268 anchor probes

These checks bind the two principal support bridges to the installed mathlib
revision. Neither declaration directly proves the frozen functional theorem.
-/

#check Convex.toWeakSpace_closure
#check lowerSemicontinuous_iff_isClosed_preimage
#check LowerSemicontinuous.isClosed_preimage
#check toWeakSpaceCLM
#check map_continuous

