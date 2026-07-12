import Mathlib.NumberTheory.LSeries.PrimesInAP

/-!
# THM-M-0500 proof-phase body

This module integrates the exact proof-bearing declaration from the repository's pinned mathlib
dependency. The wrapper repeats the frozen target verbatim because this dossier is outside the Lake
source root.
-/

namespace Stage1Instances.THM_M_0500

/-- The exact frozen target: every unit residue class modulo a nonzero natural contains infinitely
many primes. -/
def DirichletPrimesInAPTarget : Prop :=
  forall (q : Nat) [NeZero q] (a : ZMod q), IsUnit a ->
    {p : Nat | p.Prime ∧ (p : ZMod q) = a}.Infinite

/-- Repo-local exact wrapper around the proof body in pinned mathlib. -/
theorem dirichletPrimesInAP_proof : DirichletPrimesInAPTarget := by
  intro q _ a ha
  exact Nat.infinite_setOf_prime_and_eq_mod ha

#check Nat.infinite_setOf_prime_and_eq_mod
#check dirichletPrimesInAP_proof
#print axioms Nat.infinite_setOf_prime_and_eq_mod
#print axioms dirichletPrimesInAP_proof

end Stage1Instances.THM_M_0500
