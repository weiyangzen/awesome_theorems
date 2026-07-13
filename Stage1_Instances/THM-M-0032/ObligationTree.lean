import Statement
import Mathlib.RingTheory.UniqueFactorizationDomain.Kaplansky

/-!
# THM-M-0032 conditional obligation composition

This module checks the exact root composition selected by the frozen obligation graph.  The two
Auslander-Buchsbaum engines remain explicit premises.  The local Kaplansky wrapper is checked at
the pinned mathlib revision, but this file neither supplies the engines nor proves the root.
-/

namespace Stage1Instances.THM_M_0032.ObligationTree

universe u

/-- The first open mathematical package: regular local rings are domains. -/
def RegularLocalDomainPackage : Prop :=
  forall (R : Type u) [CommRing R] [IsRegularLocalRing R], IsDomain R

/-- The second open package, expressed at Kaplansky's exact nonzero-prime-ideal interface. -/
def RegularLocalPrimeElementPackage : Prop :=
  forall (R : Type u) [CommRing R] [IsRegularLocalRing R] [IsDomain R],
    forall I : Ideal R, I ≠ ⊥ -> I.IsPrime -> ∃ x ∈ I, Prime x

/-- The pinned generic Kaplansky interface, kept separate from the theorem-specific packages. -/
def KaplanskyCriterionPackage : Prop :=
  forall (R : Type u) [CommRing R] [IsDomain R],
    (forall I : Ideal R, I ≠ ⊥ -> I.IsPrime -> ∃ x ∈ I, Prime x) ->
      UniqueFactorizationMonoid R

/-- A checked wrapper around the pinned generic Kaplansky criterion. -/
theorem pinnedKaplanskyCriterionPackage : KaplanskyCriterionPackage.{u} := by
  intro R _ _ h
  exact UniqueFactorizationMonoid.iff_exists_prime_mem_of_isPrime.mpr h

/--
Checked child-to-root composition.  All three proof children are consumed, while both
theorem-specific packages remain hypotheses rather than hidden declarations.
-/
theorem root_of_domain_primeElement_and_kaplansky
    (domain : RegularLocalDomainPackage.{u})
    (primeElement : RegularLocalPrimeElementPackage.{u})
    (kaplansky : KaplanskyCriterionPackage.{u}) :
    Stage1Instances.THM_M_0032.AuslanderBuchsbaumUFDTarget.{u} := by
  intro R _ _
  letI : IsDomain R := domain R
  exact kaplansky R (primeElement R)

#check UniqueFactorizationMonoid.iff_exists_prime_mem_of_isPrime
#print axioms pinnedKaplanskyCriterionPackage
#print axioms root_of_domain_primeElement_and_kaplansky

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0032.AuslanderBuchsbaumUFDTarget

end Stage1Instances.THM_M_0032.ObligationTree
