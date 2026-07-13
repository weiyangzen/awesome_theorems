import ObligationTree

/-!
# THM-M-0025 proof-phase installation

This module installs the exact pinned mathlib Hilbert-basis theorem at the frozen anchor interface
and composes it through the registered finite-generation route to the canonical target. The direct
root declaration is a second exact-type check over the same deduplicated upstream proof body.
-/

namespace Stage1Instances.THM_M_0025.Proof

open Stage1Instances.THM_M_0025
open Stage1Instances.THM_M_0025.ObligationTree

universe u

/-- The pinned mathlib proof body installed at the frozen exact-anchor interface. -/
theorem exactPolynomialAnchor : ExactPolynomialAnchor.{u} := by
  intro R _ _
  exact Polynomial.isNoetherianRing

/-- Direct exact-root wrapper over the same pinned terminal proof body. -/
theorem hilbertBasisTheorem_direct : HilbertBasisTheoremTarget.{u} := by
  intro R _ _
  exact Polynomial.isNoetherianRing

/-- Exact root obtained by consuming the frozen child-to-parent composition interfaces. -/
theorem hilbertBasisTheorem_via_frozen_composition :
    HilbertBasisTheoremTarget.{u} :=
  root_of_exactPolynomialAnchor exactPolynomialAnchor

#check Polynomial.isNoetherianRing
#print sorries Polynomial.isNoetherianRing
#print sorries exactPolynomialAnchor
#print sorries hilbertBasisTheorem_direct
#print sorries hilbertBasisTheorem_via_frozen_composition
#print axioms Polynomial.isNoetherianRing
#print axioms exactPolynomialAnchor
#print axioms hilbertBasisTheorem_direct
#print axioms hilbertBasisTheorem_via_frozen_composition

end Stage1Instances.THM_M_0025.Proof
