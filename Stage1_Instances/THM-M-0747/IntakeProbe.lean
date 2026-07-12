import Mathlib.Computability.Halting

/-!
Discovery-only checks for the pinned computability APIs adjacent to the simple-set existence
target. These declarations do not define a simple or immune set and supply no theorem-proof credit.
-/

#check REPred
#check ComputablePred
#check ComputablePred.to_re
#check ComputablePred.computable_iff_re_compl_re
#check Set.Infinite
#check Set.compl
#check Set.Nonempty
#check Set.mem_setOf_eq

-- A prospective statement shape only. It is not frozen as the source-identical canonical target.
#check (fun A : Nat -> Prop =>
  REPred A /\
    Set.Infinite {n : Nat | Not (A n)} /\
    forall W : Nat -> Prop,
      REPred W -> Set.Infinite {n : Nat | W n} -> exists n, W n /\ A n)
