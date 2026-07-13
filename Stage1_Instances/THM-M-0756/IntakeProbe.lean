import Mathlib.Computability.Halting
import Mathlib.Computability.TuringDegree
import Mathlib.SetTheory.Ordinal.Basic

/-!
Discovery-only checks for pinned APIs adjacent to the hyperarithmetic-theory topic. No declaration
below defines, freezes, or proves a source-identical hyperarithmetic theorem.
-/

open Nat.Partrec
open scoped Computability

#check Nat.Partrec
#check Partrec
#check ComputablePred
#check REPred
#check RecursiveIn
#check TuringReducible
#check TuringEquivalent
#check recursiveIn_empty_iff_partrec
#check TuringReducible.trans
#check WellFounded
#check WellFounded.fix
#check Ordinal
