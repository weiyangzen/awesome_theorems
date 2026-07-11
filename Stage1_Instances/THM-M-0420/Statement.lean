import Mathlib.NumberTheory.NumberField.ClassNumber
import Mathlib.NumberTheory.RamificationInertia.Unramified

/-!
# THM-M-0420: exact Hilbert class field statement

This module freezes and tests the statement boundary only. It does not prove
the existence of a Hilbert class field.
-/

open scoped NumberField

namespace Stage1Instances.THM_M_0420

universe uK uH uM

/-- An extension of number fields is unramified at every finite prime. Infinite
places are deliberately not part of this predicate. -/
def IsEverywhereUnramifiedAtFinitePrimes
    (K : Type uK) (H : Type uH) [Field K] [NumberField K] [Field H]
    [NumberField H] [Algebra K H] : Prop :=
  ∀ (P : Ideal (𝓞 H)) [P.IsPrime], P ≠ ⊥ →
    Algebra.IsUnramifiedAt (𝓞 K) P

/-- A finite extension is Galois and its group of `K`-algebra automorphisms is
abelian. -/
def IsAbelianGaloisExtension
    (K : Type uK) (H : Type uH) [Field K] [Field H] [Algebra K H] : Prop :=
  IsGalois K H ∧ ∀ σ τ : H ≃ₐ[K] H, σ * τ = τ * σ

/-- The complete property required of an explicit Hilbert class field
candidate. Maximality means that every finite unramified abelian extension in
the comparison universe admits a `K`-algebra embedding into the candidate. -/
structure HilbertClassFieldProperty
    (K : Type uK) (H : Type uH) [Field K] [NumberField K] [Field H]
    [NumberField H] [Algebra K H] [Module.Finite K H] : Prop where
  isAbelianGalois : IsAbelianGaloisExtension K H
  unramifiedAtFinitePrimes : IsEverywhereUnramifiedAtFinitePrimes K H
  artinReciprocity : Nonempty ((H ≃ₐ[K] H) ≃* ClassGroup (𝓞 K))
  maximal :
    ∀ (M : Type uM) [Field M] [NumberField M] [Algebra K M]
      [Module.Finite K M],
      IsAbelianGaloisExtension K M →
      IsEverywhereUnramifiedAtFinitePrimes K M →
      Nonempty (M →ₐ[K] H)

/-- Exact target: every number field has a finite Hilbert class field with the
finite-prime unramifiedness, abelian Galois, Artin reciprocity, and maximality
properties frozen above. -/
def HilbertClassFieldTarget
    (K : Type uK) [Field K] [NumberField K] : Prop :=
  ∃ (H : Type uH) (_fieldH : Field H) (_numberFieldH : NumberField H)
    (_algebraKH : Algebra K H) (_finiteKH : Module.Finite K H),
            Nonempty (HilbertClassFieldProperty.{uK, uH, uM} K H)

/-- Direct local expansion of the unaccepted historical candidate. -/
def PinnedCandidateSourceShape
    (K : Type uK) [Field K] [NumberField K] : Prop :=
  ∃ (H : Type uH) (_ : Field H) (_ : NumberField H) (_ : Algebra K H)
    (_ : Module.Finite K H),
    Nonempty (HilbertClassFieldProperty.{uK, uH, uM} K H)

/-- Checked transport from the selected exact target to the direct historical
candidate expansion. -/
theorem hilbertClassFieldTarget_iff_pinnedCandidateSourceShape
    (K : Type uK) [Field K] [NumberField K] :
    HilbertClassFieldTarget.{uK, uH, uM} K ↔
      PinnedCandidateSourceShape.{uK, uH, uM} K := by
  rfl

/-- The group-isomorphism orientation is conventional: reversing it is a
checked transport, not a change to the mathematical claim. -/
theorem reciprocity_orientation_transport
    (K : Type uK) (H : Type uH) [Field K] [NumberField K] [Field H]
    [Algebra K H] :
    Nonempty ((H ≃ₐ[K] H) ≃* ClassGroup (𝓞 K)) ↔
      Nonempty (ClassGroup (𝓞 K) ≃* (H ≃ₐ[K] H)) := by
  constructor <;> rintro ⟨e⟩ <;> exact ⟨e.symm⟩

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationRemovedReciprocity
    (K : Type uK) [Field K] [NumberField K] : Prop :=
  ∃ (H : Type uH) (_ : Field H) (_ : NumberField H) (_ : Algebra K H)
    (_ : Module.Finite K H),
    IsAbelianGaloisExtension K H ∧ IsEverywhereUnramifiedAtFinitePrimes K H

def mutationRemovedMaximality
    (K : Type uK) [Field K] [NumberField K] : Prop :=
  ∃ (H : Type uH) (_ : Field H) (_ : NumberField H) (_ : Algebra K H)
    (_ : Module.Finite K H),
    IsAbelianGaloisExtension K H ∧
      IsEverywhereUnramifiedAtFinitePrimes K H ∧
      Nonempty ((H ≃ₐ[K] H) ≃* ClassGroup (𝓞 K))

def mutationRemovedAbelianity
    (K : Type uK) [Field K] [NumberField K] : Prop :=
  ∃ (H : Type uH) (_ : Field H) (_ : NumberField H) (_ : Algebra K H)
    (_ : Module.Finite K H), IsGalois K H

def mutationAllowsRamification
    (K : Type uK) [Field K] [NumberField K] : Prop :=
  ∃ (H : Type uH) (_ : Field H) (_ : NumberField H) (_ : Algebra K H)
    (_ : Module.Finite K H), IsAbelianGaloisExtension K H

end Stage1Instances.THM_M_0420

set_option pp.explicit true in
#print Stage1Instances.THM_M_0420.HilbertClassFieldTarget
