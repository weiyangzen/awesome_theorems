import Mathlib.Data.Finset.Filter
import Mathlib.Analysis.SpecialFunctions.Complex.Log
import Mathlib.FieldTheory.AlgebraicClosure

/-!
# THM-M-0397 anchor-audit checks

These probes identify the pinned APIs that can compose the frozen method-level
target. They do not declare or prove `Stage1Rev56.THMM0397.Statement`.
-/

#check Finset.mem_filter
#check Complex.exp
#check IsAlgebraic

namespace Stage1Rev56.THMM0397.AnchorAudit

universe u

/-- Type-only model of the application fields consumed by the candidate route. -/
structure ApplicationInterface where
  Solution : Type u
  instDecidableEq : DecidableEq Solution
  isSolution : Solution -> Prop
  instDecidableSolution : DecidablePred isSolution
  height : Solution -> Nat
  searchBound : Nat
  heightBall : Nat -> Finset Solution
  heightBall_spec : forall B x, x ∈ heightBall B <-> height x <= B
  lowerBoundForcesHeight : forall x, isSolution x -> height x <= searchBound

attribute [instance] ApplicationInterface.instDecidableEq
attribute [instance] ApplicationInterface.instDecidableSolution

/--
Checked composition shape for the pinned `Finset.mem_filter` candidate.

The substantive lower-bound-to-height implication remains an input; this lemma
only verifies that filter membership and the enumerator specification provide
the final finite-search interface.
-/
theorem filter_candidate_composes (A : ApplicationInterface.{u}) (x : A.Solution) :
    x ∈ (A.heightBall A.searchBound).filter A.isSolution <-> A.isSolution x := by
  constructor
  · exact fun h => (Finset.mem_filter.mp h).2
  · intro hx
    exact Finset.mem_filter.mpr
      ⟨(A.heightBall_spec A.searchBound x).mpr (A.lowerBoundForcesHeight x hx), hx⟩

end Stage1Rev56.THMM0397.AnchorAudit
