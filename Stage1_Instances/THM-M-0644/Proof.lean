import Mathlib.ModelTheory.Satisfiability

/-!
# THM-M-0644 proof execution

This module closes the frozen compactness target by importing the exact theorem body from the
pinned mathlib dependency.  The two named direction lemmas make the composition boundary explicit
while retaining mathlib's audited ultraproduct proof as the terminal body of the hard direction.
-/

namespace Stage1.THM_M_0644.Proof

open FirstOrder

universe u v

/-- A model of the whole theory restricts to a model of every finite subtheory. -/
theorem restrictionDirection {L : Language.{u, v}} {T : L.Theory}
    (h : T.IsSatisfiable) : T.IsFinitelySatisfiable :=
  h.isFinitelySatisfiable

/-- The hard compactness direction, pinned to mathlib's audited ultraproduct proof body. -/
theorem ultraproductDirection {L : Language.{u, v}} {T : L.Theory}
    (h : T.IsFinitelySatisfiable) : T.IsSatisfiable :=
  FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable.mpr h

/-- Exact proof of the canonical compactness proposition frozen by `Statement.lean`. -/
theorem compactnessTarget :
    forall {L : Language.{u, v}} {T : L.Theory},
      T.IsSatisfiable <-> T.IsFinitelySatisfiable := by
  intro L T
  exact Iff.intro restrictionDirection ultraproductDirection

#check compactnessTarget
#print axioms restrictionDirection
#print axioms ultraproductDirection
#print axioms compactnessTarget

end Stage1.THM_M_0644.Proof
