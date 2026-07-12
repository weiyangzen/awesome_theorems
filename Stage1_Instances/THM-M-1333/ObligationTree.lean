import Statement

/-!
# THM-M-1333 obligation interfaces

This module checks a definitional packaging edge in the frozen architecture.
It contains no existence proof and deliberately accepts the solution
components as hypotheses.
-/

namespace Stage1Instances.THM_M_1333

/-- Checked packaging from the component conclusions used by the architecture
to the exact `IsSolutionWithin` predicate. This is composition evidence for
the interface only, not evidence that any solution exists. -/
theorem isSolutionWithin_of_components {n : Nat}
    {U : Set (Real × StateSpace n)}
    {f : Real -> StateSpace n -> StateSpace n} {I : Set Real}
    {x : Real -> StateSpace n}
    (hgraph : ∀ t, t ∈ I -> (t, x t) ∈ U)
    (hderiv : ∀ t, t ∈ I -> HasDerivWithinAt x (f t (x t)) I t) :
    IsSolutionWithin U f I x := by
  intro t ht
  exact ⟨hgraph t ht, hderiv t ht⟩

#print axioms isSolutionWithin_of_components

end Stage1Instances.THM_M_1333
