import «Stage1_Instances».«THM-M-0420».Statement

/-!
# THM-M-0420 obligation-tree composition harness

This module checks only that the frozen construction and property obligations
compose to the exact Hilbert class field target. It proves none of those inputs.
-/

open scoped NumberField

namespace Stage1Instances.THM_M_0420.ObligationTree

universe uK uH uM

/-- Data needed to name one prospective finite extension without asserting any
Hilbert class field property. -/
structure Candidate (K : Type uK) [Field K] [NumberField K] where
  carrier : Type uH
  fieldCarrier : Field carrier
  numberFieldCarrier : NumberField carrier
  algebra : Algebra K carrier
  finite : Module.Finite K carrier

def ConstructionObligation : Prop :=
  ∀ (K : Type uK) [Field K] [NumberField K], Nonempty (Candidate.{uK, uH} K)

def AbelianGaloisObligation : Prop :=
  ∀ (K : Type uK) [Field K] [NumberField K] (c : Candidate.{uK, uH} K),
    letI := c.fieldCarrier
    letI := c.numberFieldCarrier
    letI := c.algebra
    letI := c.finite
    IsAbelianGaloisExtension K c.carrier

def UnramifiedObligation : Prop :=
  ∀ (K : Type uK) [Field K] [NumberField K] (c : Candidate.{uK, uH} K),
    letI := c.fieldCarrier
    letI := c.numberFieldCarrier
    letI := c.algebra
    letI := c.finite
    IsEverywhereUnramifiedAtFinitePrimes K c.carrier

def ReciprocityObligation : Prop :=
  ∀ (K : Type uK) [Field K] [NumberField K] (c : Candidate.{uK, uH} K),
    letI := c.fieldCarrier
    letI := c.numberFieldCarrier
    letI := c.algebra
    letI := c.finite
    Nonempty ((c.carrier ≃ₐ[K] c.carrier) ≃* ClassGroup (𝓞 K))

def MaximalityObligation : Prop :=
  ∀ (K : Type uK) [Field K] [NumberField K] (c : Candidate.{uK, uH} K),
    letI := c.fieldCarrier
    letI := c.numberFieldCarrier
    letI := c.algebra
    letI := c.finite
    ∀ (M : Type uM) [Field M] [NumberField M] [Algebra K M]
      [Module.Finite K M],
      IsAbelianGaloisExtension K M →
      IsEverywhereUnramifiedAtFinitePrimes K M →
      Nonempty (M →ₐ[K] c.carrier)

/-- Checked child-to-parent composition. All five hypotheses are deliberately
open obligations; this theorem is not a Hilbert class field existence proof. -/
theorem root_composition
    (construction : ConstructionObligation.{uK, uH})
    (abelianGalois : AbelianGaloisObligation.{uK, uH})
    (unramified : UnramifiedObligation.{uK, uH})
    (reciprocity : ReciprocityObligation.{uK, uH})
    (maximality : MaximalityObligation.{uK, uH, uM}) :
    ∀ (K : Type uK) [Field K] [NumberField K],
      HilbertClassFieldTarget.{uK, uH, uM} K := by
  intro K _ _
  let ⟨c⟩ := construction K
  letI := c.fieldCarrier
  letI := c.numberFieldCarrier
  letI := c.algebra
  letI := c.finite
  exact ⟨c.carrier, c.fieldCarrier, c.numberFieldCarrier, c.algebra, c.finite,
    ⟨{
      isAbelianGalois := abelianGalois K c
      unramifiedAtFinitePrimes := unramified K c
      artinReciprocity := reciprocity K c
      maximal := maximality K c
    }⟩⟩

#check root_composition

end Stage1Instances.THM_M_0420.ObligationTree
