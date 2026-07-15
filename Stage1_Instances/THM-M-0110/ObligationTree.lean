import Statement

/-!
# THM-M-0110 conditional obligation composition

This module checks the child-to-parent interfaces frozen by the obligation
registry. The scheme-level semantic transport and the substantive Kodaira
vanishing argument are explicit premises. No declaration below constructs
either package or proves the canonical theorem.
-/

namespace Stage1Instances.THMM0110.ObligationTree

universe u

open Stage1Instances.THMM0110

/--
An explicit interface for the missing native geometric witness. The predicate
must later be replaced, through a versioned registry delta, by a structure
containing the actual projective/canonical/ample/tensor transports.
-/
structure NativeSemanticTransportPackage where
  NativeKodairaDatum : forall (k : Type u) [Field k] [CharZero k],
    KodairaVanishingData.{u} k -> Prop
  transport : forall (k : Type u) [Field k] [CharZero k]
      (D : KodairaVanishingData.{u} k),
    D.Hypotheses -> NativeKodairaDatum k D

/-- The substantive proof must consume the native witness produced above. -/
def KodairaVanishingArgumentPackage
    (native : NativeSemanticTransportPackage.{u}) : Prop :=
  forall (k : Type u) [Field k] [CharZero k]
      (D : KodairaVanishingData.{u} k),
    native.NativeKodairaDatum k D -> D.VanishingConclusion

/-- The exact final assembly interface for the frozen root. -/
def RootAssemblyPackage : Prop :=
  forall (native : NativeSemanticTransportPackage.{u}),
    KodairaVanishingArgumentPackage.{u} native ->
      KodairaVanishingTarget.{u}

/--
Checked conditional composition into the exact target. The native transport is
consumed to keep that root-relevant boundary explicit, but its `Prop` result is
not treated as a Kodaira proof.
-/
theorem checkedRootAssembly : RootAssemblyPackage.{u} := by
  intro nativeTransport vanishing k _ _ D hD
  exact vanishing k D (nativeTransport.transport k D hD)

/-- Bind the checked assembly package to the exact frozen declaration. -/
theorem root_of_packages
    (nativeTransport : NativeSemanticTransportPackage.{u})
    (vanishing : KodairaVanishingArgumentPackage.{u} nativeTransport)
    (assembly : RootAssemblyPackage.{u}) :
    KodairaVanishingTarget.{u} :=
  assembly nativeTransport vanishing

#check NativeSemanticTransportPackage
#check KodairaVanishingArgumentPackage
#check KodairaVanishingTarget

#print axioms checkedRootAssembly
#print axioms root_of_packages

end Stage1Instances.THMM0110.ObligationTree
