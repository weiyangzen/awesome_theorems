import Statement

/-!
# THM-M-0085 proof execution

This module proves the exact creates-`G`-split-coequalizers target frozen in
`Statement.lean`. The explicit premise is installed as the local instance
expected by the pinned mathlib Beck constructor.
-/

noncomputable section

open CategoryTheory

namespace Stage1.THM_M_0085

/-- Beck's monadicity theorem in the exact fixed-adjunction form frozen by
`Statement`: the comparison functor for that same adjunction is an
equivalence. -/
theorem beckMonadicity : Statement := by
  intro C D _ _ F G adj creates
  letI : CategoryTheory.Monad.CreatesColimitOfIsSplitPair G := creates
  exact (CategoryTheory.Monad.monadicOfCreatesGSplitCoequalizers adj).eqv

#print axioms beckMonadicity

end Stage1.THM_M_0085
