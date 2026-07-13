import Mathlib.SetTheory.Ordinal.Basic
import Mathlib.SetTheory.ZFC.Ordinal
import Mathlib.Computability.RecursiveIn

/-!
# THM-M-0757 discovery-only intake probe

These checks authenticate generic pinned ordinal, set-theoretic ordinal, and ordinary oracle-
computability APIs. They neither define admissibility or alpha-recursion nor select or prove a
theorem for THM-M-0757.
-/

#check Ordinal
#check Ordinal.ToType
#check ZFSet.IsOrdinal
#check ZFSet.isOrdinal_toZFSet
#check RecursiveIn
#check recursiveIn_empty_iff_partrec
