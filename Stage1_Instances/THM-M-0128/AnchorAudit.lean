import Mathlib.NumberTheory.NumberField.AdeleRing
import Mathlib.NumberTheory.NumberField.CMField

/-!
# THM-M-0128 anchor-audit probe

This module checks only pinned object-level substrate for the bounded anchor
inventory. The exact Shimura reciprocity proposition is not frozen, so this
module deliberately declares no replacement target and proves no reciprocity
claim.
-/

open scoped NumberField

namespace Stage1Instances.THM_M_0128_AnchorAudit

#check NumberField.IsCMField
#check NumberField.AdeleRing
#check NumberField.AdeleRing.algebraMap_injective

#print axioms NumberField.AdeleRing.algebraMap_injective

end Stage1Instances.THM_M_0128_AnchorAudit
