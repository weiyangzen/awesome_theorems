import Mathlib.FieldTheory.IsRealClosed.Basic
import Mathlib.FieldTheory.IsAlgClosed.Basic
import Mathlib.Algebra.Order.Ring.Ordering.Basic

/-!
Discovery-only checks for vocabulary near a later source-selected Artin-Schreier statement.

The repository has not selected one proposition from the real-closed-field theorem family. This
file therefore declares no target theorem and supplies no proof credit.
-/

namespace Stage1Instances.THM_M_0018

#check IsRealClosed
#check IsRealClosed.isSquare_or_isSquare_neg
#check IsRealClosed.exists_isRoot_of_odd_natDegree
#check IsSemireal
#check IsSemireal.not_isSumSq_neg_one
#check isSemireal_iff_not_isSumSq_neg_one
#check RingPreordering
#check RingPreordering.IsOrdering
#check IsAlgClosed
#check IsAlgClosure
#check Algebra.IsAlgebraic
#check Module.finrank

end Stage1Instances.THM_M_0018
