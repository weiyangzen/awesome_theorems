import ObligationTree

/-!
# THM-M-0985 proof execution

This module integrates the pinned mathlib strong-law proof body with the
frozen obligation interface and closes the exact canonical proposition.
-/

noncomputable section

open Filter Finset MeasureTheory
open scoped MeasureTheory ProbabilityTheory Topology

namespace Stage1Instances.THMM0985.Proof

universe u

/-- The frozen terminal package, inhabited by the proof body in the pinned
`Mathlib.Probability.StrongLaw` module. -/
theorem pairwiseStrongLawPackage_proof :
    ObligationTree.PairwiseStrongLawPackage.{u} := by
  intro Omega _ mu X hIntegrable hPairwise hIdent
  simpa [smul_eq_mul] using
    (ProbabilityTheory.strong_law_ae X hIntegrable hPairwise hIdent)

/-- Exact root proof obtained by composing the pinned terminal body through
the mutual-to-pairwise bridge frozen in `ObligationTree.lean`. -/
theorem kolmogorovStrongLaw : KolmogorovStrongLaw.{u} :=
  ObligationTree.root_of_pairwiseStrongLawPackage
    pairwiseStrongLawPackage_proof

#print axioms pairwiseStrongLawPackage_proof
#print axioms kolmogorovStrongLaw

end Stage1Instances.THMM0985.Proof
