import Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0995 validation adapters

This module checks the exact type of both proof-phase root routes and their transport to the
expanded frozen statement. It deliberately reuses `Proof.lean`; it is same-worker corroboration,
not a distinct proof body or an independent-runner attestation.
-/

namespace Stage1Instances.THM_M_0995.Validation

open Stage1Instances.THM_M_0995

universe u

/-- Exact-type validation adapter for the corrected registry-v2 composition route. -/
theorem exactRootViaRegistry : StatementShape.{u} :=
  Proof.bernsteinInequality_via_registry_v2

/-- Exact-type validation adapter for the separately assembled direct proof-phase route. -/
theorem exactRootDirect : StatementShape.{u} :=
  Proof.bernsteinInequality

/-- Checked transport of the validated root to the direct quantified encoding. -/
theorem expandedRoot : ExpandedSourceShape.{u} :=
  statementShape_iff_expandedSourceShape.mp exactRootViaRegistry

#check exactRootViaRegistry
#check exactRootDirect
#check expandedRoot
assert_no_sorry Proof.bernsteinInequality_via_registry_v2
assert_no_sorry Proof.bernsteinInequality
assert_no_sorry Proof.not_optimizeExponentPackage
assert_no_sorry exactRootViaRegistry
assert_no_sorry exactRootDirect
assert_no_sorry expandedRoot
#print sorries exactRootViaRegistry
#print sorries exactRootDirect
#print sorries expandedRoot
#print axioms Proof.bernsteinInequality_via_registry_v2
#print axioms Proof.bernsteinInequality
#print axioms Proof.not_optimizeExponentPackage
#print axioms exactRootViaRegistry
#print axioms exactRootDirect
#print axioms expandedRoot

end Stage1Instances.THM_M_0995.Validation
