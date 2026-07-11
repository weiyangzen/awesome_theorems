import Statement

/-!
# Independent kernel probe for THM-M-0085

This module reimplements the exact canonical proof without importing the proof
module. It is an independent implementation probe inside the same worker
checkout, not a release-grade independent runner attestation.
-/

noncomputable section

open CategoryTheory

namespace Stage1.THM_M_0085.Validation

theorem independentBeckMonadicity : Stage1.THM_M_0085.Statement := by
  intro C D _ _ F G adj creates
  letI : CategoryTheory.Monad.CreatesColimitOfIsSplitPair G := creates
  exact (CategoryTheory.Monad.monadicOfCreatesGSplitCoequalizers adj).eqv

#print axioms independentBeckMonadicity

end Stage1.THM_M_0085.Validation
