import Mathlib.ModelTheory.DirectLimit
import Mathlib.ModelTheory.ElementaryMaps
import Mathlib.ModelTheory.ElementarySubstructures

open FirstOrder

namespace Stage1.THM_M_0649.AnchorAuditProbe

open FirstOrder.Language

-- These are the nearest pinned mathlib ingredients.  None has the frozen root type.
#check Language.DirectLimit.of
#check Language.DirectLimit.exists_of
#check Language.DirectLimit.iSup_range_of_eq_top
#check Language.DirectLimit.Equiv_iSup
#check Language.Embedding.isElementary_of_exists
#check Language.Substructure.isElementary_of_exists
#check Language.ElementaryEmbedding.comp

end Stage1.THM_M_0649.AnchorAuditProbe
