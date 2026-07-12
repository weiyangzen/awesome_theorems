import Statement

/-!
# THM-M-0769 proof-phase body

This module implements the frozen fiber-selector obligation using Lean's
explicit foundational `Classical.choice` axiom and composes it into the exact
indexed-family target. The axiom dependency is intentional and exposed.
-/

universe u v

namespace Stage1Instances.THM_M_0769

/-- The frozen substantive bridge: select one inhabitant from each nonempty
fiber. -/
noncomputable def fiberSelector_proof
    (ι : Sort u) (A : ι -> Sort v) (h : forall i, Nonempty (A i)) :
    forall i, A i :=
  fun i => Classical.choice (h i)

/-- The exact frozen axiom-of-choice target, closed by the selector bridge and
`Nonempty` packaging. -/
theorem axiomOfChoice_proof : AxiomOfChoiceTarget.{u, v} := by
  intro ι A h
  exact Nonempty.intro (fiberSelector_proof ι A h)

#check fiberSelector_proof
#check axiomOfChoice_proof
#print axioms fiberSelector_proof
#print axioms axiomOfChoice_proof

end Stage1Instances.THM_M_0769
