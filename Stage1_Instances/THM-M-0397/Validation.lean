import Statement

/-!
# THM-M-0397 independent validation probe

This module does not import `Proof` or `ObligationTree`. It independently
reconstructs both directions of the frozen finite-search statement from the
fields of `Application` and the pinned `Finset.mem_filter` API.
-/

noncomputable section

namespace Stage1Rev56.THMM0397.Validation

open Stage1Rev56.THMM0397

universe u

theorem independent_listed_is_solution (A : Application.{u}) (x : A.Solution)
    (hx : x ∈ solutionList A) : A.isSolution x := by
  exact (Finset.mem_filter.mp hx).2

theorem independent_solution_is_listed (A : Application.{u})
    (hLower : HasBakerLowerBound A.logData A.lowerBound)
    (x : A.Solution) (hx : A.isSolution x) : x ∈ solutionList A := by
  apply Finset.mem_filter.mpr
  exact ⟨(A.heightBall_spec A.searchBound x).mpr
    (A.reduce_solution hLower x hx), hx⟩

theorem independent_root : Statement.{u} := by
  intro A hLower x
  constructor
  · exact independent_listed_is_solution A x
  · exact independent_solution_is_listed A hLower x

theorem independent_root_exact_type :
    (Statement.{u}) := independent_root

#print axioms independent_listed_is_solution
#print axioms independent_solution_is_listed
#print axioms independent_root
#print axioms independent_root_exact_type

end Stage1Rev56.THMM0397.Validation
