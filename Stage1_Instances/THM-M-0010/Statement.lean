import Mathlib.RingTheory.Filtration

/-!
# THM-M-0010: exact Artin-Rees statement

This module freezes and tests the statement boundary only. It does not add a
proof of the Artin-Rees lemma.
-/

namespace Stage1Instances.THM_M_0010

universe u v

/-- The exact Artin-Rees equality selected at intake. -/
def ArtinReesTarget : Prop :=
  ∀ (R : Type u) [CommRing R] [IsNoetherianRing R]
    (I : Ideal R) (M : Type v) [AddCommGroup M] [Module R M] [Module.Finite R M]
    (N : Submodule R M),
      ∃ k : Nat, ∀ n : Nat, k ≤ n →
        I ^ n • (⊤ : Submodule R M) ⊓ N =
          I ^ (n - k) • (I ^ k • (⊤ : Submodule R M) ⊓ N)

/-- The binder and notation shape of the pinned mathlib declaration
`Ideal.exists_pow_inf_eq_pow_smul`. -/
def PinnedMathlibSourceShape : Prop :=
  ∀ (R : Type u) [CommRing R] [IsNoetherianRing R]
    (I : Ideal R) (M : Type v) [AddCommGroup M] [Module R M] [Module.Finite R M]
    (N : Submodule R M),
      ∃ k : ℕ, ∀ n ≥ k,
        I ^ n • ⊤ ⊓ N = I ^ (n - k) • (I ^ k • ⊤ ⊓ N)

/-- Checked identity between the canonical target and the pinned source shape. -/
theorem artinReesTarget_iff_pinnedMathlibSourceShape :
    ArtinReesTarget.{u, v} ↔ PinnedMathlibSourceShape.{u, v} :=
  Iff.rfl

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationRemovedNoetherianity : Prop :=
  ∀ (R : Type u) [CommRing R]
    (I : Ideal R) (M : Type v) [AddCommGroup M] [Module R M] [Module.Finite R M]
    (N : Submodule R M),
      ∃ k : Nat, ∀ n : Nat, k ≤ n →
        I ^ n • (⊤ : Submodule R M) ⊓ N =
          I ^ (n - k) • (I ^ k • (⊤ : Submodule R M) ⊓ N)

def mutationRemovedModuleFiniteness : Prop :=
  ∀ (R : Type u) [CommRing R] [IsNoetherianRing R]
    (I : Ideal R) (M : Type v) [AddCommGroup M] [Module R M]
    (N : Submodule R M),
      ∃ k : Nat, ∀ n : Nat, k ≤ n →
        I ^ n • (⊤ : Submodule R M) ⊓ N =
          I ^ (n - k) • (I ^ k • (⊤ : Submodule R M) ⊓ N)

def mutationRemovedLowerBound : Prop :=
  ∀ (R : Type u) [CommRing R] [IsNoetherianRing R]
    (I : Ideal R) (M : Type v) [AddCommGroup M] [Module R M] [Module.Finite R M]
    (N : Submodule R M),
      ∃ k : Nat, ∀ n : Nat,
        I ^ n • (⊤ : Submodule R M) ⊓ N =
          I ^ (n - k) • (I ^ k • (⊤ : Submodule R M) ⊓ N)

def mutationChangedEqualityToContainment : Prop :=
  ∀ (R : Type u) [CommRing R] [IsNoetherianRing R]
    (I : Ideal R) (M : Type v) [AddCommGroup M] [Module R M] [Module.Finite R M]
    (N : Submodule R M),
      ∃ k : Nat, ∀ n : Nat, k ≤ n →
        I ^ n • (⊤ : Submodule R M) ⊓ N ≤ I ^ (n - k) • N

-- Retained boundary instantiations. These are expressions, not root proofs.
def boundaryBottomIdeal : Prop :=
  ∀ (R : Type u) [CommRing R] [IsNoetherianRing R]
    (M : Type v) [AddCommGroup M] [Module R M] [Module.Finite R M]
    (N : Submodule R M),
      ∃ k : Nat, ∀ n : Nat, k ≤ n →
        (⊥ : Ideal R) ^ n • (⊤ : Submodule R M) ⊓ N =
          (⊥ : Ideal R) ^ (n - k) • ((⊥ : Ideal R) ^ k • ⊤ ⊓ N)

def boundaryTopIdeal : Prop :=
  ∀ (R : Type u) [CommRing R] [IsNoetherianRing R]
    (M : Type v) [AddCommGroup M] [Module R M] [Module.Finite R M]
    (N : Submodule R M),
      ∃ k : Nat, ∀ n : Nat, k ≤ n →
        (⊤ : Ideal R) ^ n • (⊤ : Submodule R M) ⊓ N =
          (⊤ : Ideal R) ^ (n - k) • ((⊤ : Ideal R) ^ k • ⊤ ⊓ N)

def boundaryBottomSubmodule : Prop :=
  ∀ (R : Type u) [CommRing R] [IsNoetherianRing R]
    (I : Ideal R) (M : Type v) [AddCommGroup M] [Module R M] [Module.Finite R M],
      ∃ k : Nat, ∀ n : Nat, k ≤ n →
        I ^ n • (⊤ : Submodule R M) ⊓ ⊥ =
          I ^ (n - k) • (I ^ k • (⊤ : Submodule R M) ⊓ ⊥)

def boundaryAtWitness : Prop :=
  ∀ (R : Type u) [CommRing R] [IsNoetherianRing R]
    (I : Ideal R) (M : Type v) [AddCommGroup M] [Module R M] [Module.Finite R M]
    (N : Submodule R M) (k : Nat),
      I ^ k • (⊤ : Submodule R M) ⊓ N =
        I ^ (k - k) • (I ^ k • (⊤ : Submodule R M) ⊓ N)

end Stage1Instances.THM_M_0010

set_option pp.explicit true in
#print Stage1Instances.THM_M_0010.ArtinReesTarget
