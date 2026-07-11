import ObligationTree

/-!
# THM-M-0397 proof execution

This module proves the frozen method-level theorem. The result is conditional
on the concrete Baker lower bound named in `Statement`; the application-specific
reduction and exact height-ball enumeration are data in `Application`.
-/

noncomputable section

namespace Stage1Rev56.THMM0397.Proof

open Stage1Rev56.THMM0397

universe u

/-- The forward half of the finite-search specification: every listed object
really satisfies the selected Diophantine predicate. -/
theorem listed_is_solution (A : Application.{u}) (x : A.Solution)
    (hx : x ∈ solutionList A) : A.isSolution x := by
  exact (Finset.mem_filter.mp hx).2

/-- The reverse half: the Baker reduction puts every solution in the exact
height ball, after which the executable filter retains it. -/
theorem solution_is_listed (A : Application.{u})
    (hLower : HasBakerLowerBound A.logData A.lowerBound)
    (x : A.Solution) (hx : A.isSolution x) : x ∈ solutionList A := by
  apply Finset.mem_filter.mpr
  exact ⟨(A.heightBall_spec A.searchBound x).mpr
    (A.reduce_solution hLower x hx), hx⟩

/-- Exact local proof body for the frozen canonical root. -/
theorem baker_method : Statement.{u} := by
  intro A hLower x
  constructor
  · exact listed_is_solution A x
  · exact solution_is_listed A hLower x

/-- Checked identity between the proof-phase declaration and the canonical
proposition. This prevents crediting a broadened or substituted target. -/
theorem baker_method_exact_type :
    (Statement.{u}) := baker_method

#print axioms listed_is_solution
#print axioms solution_is_listed
#print axioms baker_method
#print axioms baker_method_exact_type

end Stage1Rev56.THMM0397.Proof
