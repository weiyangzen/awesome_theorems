import «Stage1_Instances».«THM-M-0420».ObligationTree

/-!
# THM-M-0420 partial proof execution

This module implements the finite-prime normalization leaf from the frozen
obligation tree. The global class-field-theory construction and its substantive
properties remain open.
-/

open scoped NumberField

namespace Stage1Instances.THM_M_0420.Proof

universe uK uH

/-- Ramification-index-one formulation indexed first by a nonzero prime of the
base field and then by every prime above it. -/
def AllPrimesOverHaveRamificationIdxOne
    (K : Type uK) (H : Type uH) [Field K] [NumberField K] [Field H]
    [NumberField H] [Algebra K H] : Prop :=
  ∀ (p : Ideal (𝓞 K)) [p.IsPrime], p ≠ ⊥ → ∀ P : Ideal.primesOver p (𝓞 H),
    Ideal.ramificationIdx p (P : Ideal (𝓞 H)) = 1

/-- `M0420-N1`: the target's prime-of-the-extension predicate agrees with the
standard ramification-index-one formulation over every finite base prime. -/
theorem everywhereUnramifiedAtFinitePrimes_iff_allPrimesOver
    (K : Type uK) (H : Type uH) [Field K] [NumberField K] [Field H]
    [NumberField H] [Algebra K H] [Module.Finite K H] :
    IsEverywhereUnramifiedAtFinitePrimes K H ↔
      AllPrimesOverHaveRamificationIdxOne K H := by
  constructor
  · intro h p hpprime hp P
    have hPne : (P : Ideal (𝓞 H)) ≠ ⊥ :=
      Ideal.ne_bot_of_mem_primesOver hp P.2
    have hram :=
      (Algebra.isUnramifiedAt_iff_of_isDedekindDomain
        (R := 𝓞 K) (S := 𝓞 H) (p := (P : Ideal (𝓞 H))) hPne).mp
        (h (P : Ideal (𝓞 H)) hPne)
    have hunder : Ideal.under (𝓞 K) (P : Ideal (𝓞 H)) = p :=
      (Ideal.LiesOver.over (P := (P : Ideal (𝓞 H))) (p := p)).symm
    simpa [hunder] using hram
  · intro h P hPprime hPne
    let p : Ideal (𝓞 K) := Ideal.under (𝓞 K) P
    have hpne : p ≠ ⊥ := Ideal.under_ne_bot (A := 𝓞 K) hPne
    have hram : Ideal.ramificationIdx p P = 1 :=
      h p hpne (Ideal.primesOver.mk p P)
    exact
      (Algebra.isUnramifiedAt_iff_of_isDedekindDomain
        (R := 𝓞 K) (S := 𝓞 H) (p := P) hPne).mpr hram

#check everywhereUnramifiedAtFinitePrimes_iff_allPrimesOver
#print axioms everywhereUnramifiedAtFinitePrimes_iff_allPrimesOver

end Stage1Instances.THM_M_0420.Proof
