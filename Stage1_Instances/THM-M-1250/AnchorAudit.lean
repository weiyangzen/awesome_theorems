import Mathlib.Analysis.Distribution.SchwartzSpace.Basic

/-!
# THM-M-1250 anchor-audit probes

These commands check the immutable mathlib candidates against the same import
used by the frozen statement.  This file inventories anchors; it does not prove
`SchwartzSpaceCharacterization`.
-/

open scoped SchwartzMap

#check SchwartzMap
#check SchwartzMap.mk
#check SchwartzMap.smooth
#check SchwartzMap.decay
#check SchwartzMap.le_seminorm
#check SchwartzMap.seminorm_le_bound

#print axioms SchwartzMap.smooth
#print axioms SchwartzMap.decay
#print axioms SchwartzMap.le_seminorm
#print axioms SchwartzMap.seminorm_le_bound
