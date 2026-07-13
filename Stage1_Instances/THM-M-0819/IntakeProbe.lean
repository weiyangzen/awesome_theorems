import Mathlib.Order.Height
import Mathlib.Order.Antichain

-- Discovery only: authenticate adjacent pinned order and cardinality interfaces.
#check IsChain
#check IsAntichain
#check subsingleton_of_isChain_of_isAntichain
#check inter_subsingleton_of_isChain_of_isAntichain
#check Set.chainHeight
#check Set.exists_eq_chainHeight_of_finite
#check Set.encard
#check ENat.card
