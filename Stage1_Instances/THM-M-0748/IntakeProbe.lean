import Mathlib.Computability.Halting
import Mathlib.Computability.TuringDegree

/-!
# THM-M-0748 discovery-only intake probe

These checks authenticate pinned computable-enumerability and partial-function Turing-degree APIs
adjacent to Post's problem. They do not define the c.e. bottom or complete degree, bridge c.e. sets
to partial-function degrees, select a canonical target, or prove an intermediate degree exists.
-/

open scoped Computability

#check REPred
#check ComputablePred
#check Nat.Partrec
#check RecursiveIn
#check TuringReducible
#check TuringEquivalent
#check TuringDegree
#check TuringDegree.instPartialOrder
#check partrec_iff_forall_turingReducible
#check toAntisymmetrization

-- Prospective order shape only; the endpoints and c.e. predicate are deliberately abstract.
#check (fun (IsCE : TuringDegree -> Prop) (computable complete : TuringDegree) =>
  exists degree, IsCE degree /\ computable < degree /\ degree < complete)
