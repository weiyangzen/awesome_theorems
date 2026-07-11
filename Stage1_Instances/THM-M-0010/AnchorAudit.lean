import Mathlib.RingTheory.Filtration

/-!
# THM-M-0010: pinned anchor audit

This module checks that the mathlib candidate inhabits the already frozen exact
target. It is audit evidence, not acceptance of the later proof node.
-/

namespace Stage1Instances.THM_M_0010

universe u v

/-- Exact-type check for the Artin-Rees declaration at the pinned mathlib revision.
The type repeats the frozen standalone statement because the dossier path is
not a Lean module path (it contains a hyphen). -/
theorem mathlibCandidateChecksExactTarget :
    ∀ (R : Type u) [CommRing R] [IsNoetherianRing R]
      (I : Ideal R) (M : Type v) [AddCommGroup M] [Module R M] [Module.Finite R M]
      (N : Submodule R M),
        ∃ k : Nat, ∀ n : Nat, k ≤ n →
          I ^ n • (⊤ : Submodule R M) ⊓ N =
            I ^ (n - k) • (I ^ k • (⊤ : Submodule R M) ⊓ N) := by
  intro R _ _ I M _ _ _ N
  exact Ideal.exists_pow_inf_eq_pow_smul I N

end Stage1Instances.THM_M_0010

#check Ideal.exists_pow_inf_eq_pow_smul
#print axioms Ideal.exists_pow_inf_eq_pow_smul
#print axioms Stage1Instances.THM_M_0010.mathlibCandidateChecksExactTarget
