import Statement
import Proof

/-!
# THM-M-1270 independent validation probe

This module checks that the proof-phase target is definitionally identical to
the frozen statement and independently reconstructs one admitted maximality
lemma. It intentionally does not construct the open descent-maximal point.
-/

namespace Stage1Instances.THM_M_1270.Validation

open Proof

universe u

/-- Exact-type bridge between the separately authored statement and proof
modules. -/
theorem proofTarget_iff_frozen :
    ProofTarget.{u} <-> EkelandVariationalPrincipleTarget.{u} := by
  rfl

/-- Independent reconstruction of strict penalized minimality from descent
maximality, using an order split rather than the proof-phase contradiction
argument. -/
theorem independentlyStrictOfMaximal {X : Type u} [PseudoMetricSpace X]
    {f : X -> Real} {epsilon lambda : Real} {x0 v : X}
    (hmax : DescentMaximalPoint f epsilon lambda x0 v) :
    forall y : X, Ne y v ->
      f v < f y + (epsilon / lambda) * dist v y := by
  intro y hy
  rcases lt_or_ge (f v) (f y + (epsilon / lambda) * dist v y) with h | h
  · exact h
  · exact False.elim (hy (hmax.2.2 y h))

#check proofTarget_iff_frozen
#check independentlyStrictOfMaximal
#print axioms proofTarget_iff_frozen
#print axioms independentlyStrictOfMaximal

end Stage1Instances.THM_M_1270.Validation
