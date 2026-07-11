import Statement

/-!
# THM-M-0397 obligation composition

This module checks the two semantic directions of the frozen finite-search
claim.  It uses only fields already present in a specified `Application`; it
does not supply a Baker lower bound for any concrete logarithmic form.
-/

noncomputable section

namespace Stage1Rev56.THMM0397.ObligationTree

open Stage1Rev56.THMM0397

universe u

/-- The parameterwise obligation whose universal closure is `Statement`. -/
def ApplicationClosure (A : Application.{u}) : Prop :=
  HasBakerLowerBound A.logData A.lowerBound ->
    forall x, x ∈ solutionList A <-> A.isSolution x

/-- Checked child-to-parent composition for one specified application. -/
theorem application_compose (A : Application.{u}) : ApplicationClosure A := by
  intro hLower x
  constructor
  · intro hx
    exact (Finset.mem_filter.mp hx).2
  · intro hx
    apply Finset.mem_filter.mpr
    exact ⟨(A.heightBall_spec A.searchBound x).mpr
      (A.reduce_solution hLower x hx), hx⟩

/-- Binder-preserving transport from all application closures to the root. -/
theorem root_compose
    (closures : forall A : Application.{u}, ApplicationClosure A) :
    Statement.{u} := by
  exact closures

/-- Exact closure of the frozen method-level root from its quantified interface. -/
theorem exact_root : Statement.{u} := by
  exact application_compose

theorem application_closure_iff_expanded (A : Application.{u}) :
    ApplicationClosure A <->
      HasBakerLowerBound A.logData A.lowerBound ->
        forall x, x ∈ (A.heightBall A.searchBound).filter A.isSolution <->
          A.isSolution x := by
  rfl

#print axioms application_compose
#print axioms root_compose
#print axioms exact_root

end Stage1Rev56.THMM0397.ObligationTree
