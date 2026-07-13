import Mathlib.Computability.Halting
import Mathlib.Computability.Reduce
import Mathlib.Computability.TuringDegree

/-!
# THM-M-0758 discovery-only intake probe

These checks authenticate adjacent pinned computable-enumerability and degree APIs. They neither
define the class of c.e. Turing degrees nor select or prove a structural theorem for THM-M-0758.
-/

open scoped Computability

#check REPred
#check Partrec.dom_re
#check TuringReducible
#check TuringEquivalent
#check TuringDegree
#check TuringDegree.instPartialOrder
#check ManyOneReducible
#check ManyOneDegree
#check ManyOneDegree.instPartialOrder
#check ManyOneDegree.instSemilatticeSup

-- Prospective representation shapes only; neither is the canonical target.
#check (fun p : Nat -> Prop => REPred p)
#check (fun _f : Nat →. Nat => (inferInstance : PartialOrder TuringDegree))
