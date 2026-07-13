import Statement

/-!
# THM-M-1228 proof-phase blocker

The frozen statement exposes the unavailable analytic notions through an
unconstrained `CKNSourceSemantics`. A theorem uniform in that interface cannot
be implemented: one permitted interpretation makes suitability true and the
claimed measure-zero conclusion false.

This module checks that obstruction. It does not refute the mathematical CKN
theorem and supplies no proof credit for a concrete source-faithful semantics.
-/

namespace Stage1Instances.THMM1228

/-- Concrete data used only to exhibit the semantic-interface obstruction. -/
def counterexampleData : SolutionData where
  domain := Set.univ
  velocity := fun _ _ => 0
  pressure := fun _ => 0
  force := fun _ _ => 0

/-- An allowed interface interpretation in which the root conclusion fails. -/
def counterexampleSemantics : CKNSourceSemantics where
  IsSuitableWeakSolution := fun _ => True
  RegularAt := fun _ _ => False
  ParabolicHausdorffOneMeasureZero := fun _ => False

/-- The canonical proposition fails at the explicit counterexample semantics. -/
theorem counterexampleTargetIsFalse :
    Not (CaffarelliKohnNirenbergTarget counterexampleSemantics) := by
  intro target
  exact target counterexampleData trivial

/-- There is no proof of the target that is uniform over the unconstrained
statement interface. Concrete source semantics are required before execution
of the analytic CKN proof can begin. -/
theorem noUniformTargetProof :
    Not (forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S) := by
  intro target
  exact counterexampleTargetIsFalse (target counterexampleSemantics)

#print axioms counterexampleTargetIsFalse
#print axioms noUniformTargetProof

end Stage1Instances.THMM1228
