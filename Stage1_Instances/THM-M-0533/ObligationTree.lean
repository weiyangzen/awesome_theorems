import Statement

/-!
# THM-M-0533 conditional obligation composition

This module checks only the final child-to-parent composition selected by the
frozen architecture. The construction and exactness packages are explicit
premises; no Mayer-Vietoris proof is asserted here.
-/

open CategoryTheory CategoryTheory.Limits
open TopologicalSpace

namespace AwesomeTheorems.THM_M_0533

universe u

noncomputable section

/-- Data and the three consecutive-zero identities required before exactness
can be stated at every recurring term. -/
structure ConstructionPackage (X : TopCat.{u}) (U V : Opens X) where
  boundary : forall n : Nat, H (n + 1) X ⟶ H n (OpenSpace (U ⊓ V))
  zeroBoundaryFirst : forall n, boundary n ≫ firstMap U V n = 0
  zeroFirstSecond : forall n, firstMap U V n ≫ secondMap U V n = 0
  zeroSecondBoundary : forall n, secondMap U V (n + 1) ≫ boundary n = 0

/-- Exactness conclusions consumed by the final assembly node. -/
def ExactnessPackage {X : TopCat.{u}} {U V : Opens X}
    (c : ConstructionPackage X U V) : Prop :=
  (forall n : Nat, MayerVietorisDegree U V n (c.boundary n)
    (c.zeroBoundaryFirst n) (c.zeroFirstSecond n) (c.zeroSecondBoundary n)) /\
  (ShortComplex.mk (firstMap U V 0) (secondMap U V 0)
    (c.zeroFirstSecond 0)).Exact /\
  (ShortComplex.mk (secondMap U V 0)
    (0 : H 0 X ⟶ AddCommGrpCat.of (ULift.{u} PUnit)) (by simp)).Exact

/-- Kernel-checked composition interface. Both substantive inputs remain open
registered obligations. -/
theorem root_of_construction_and_exactness
    (construction : forall (X : TopCat.{u}) (U V : Opens X), U ⊔ V = ⊤ →
      ConstructionPackage X U V)
    (exactness : forall (X : TopCat.{u}) (U V : Opens X) (h : U ⊔ V = ⊤),
      ExactnessPackage (construction X U V h)) : MayerVietorisSequence.{u} := by
  intro X U V hcover
  let c := construction X U V hcover
  have h := exactness X U V hcover
  exact ⟨c.boundary, c.zeroBoundaryFirst, c.zeroFirstSecond,
    c.zeroSecondBoundary, h.1, h.2.1, h.2.2⟩

#print axioms root_of_construction_and_exactness

end

end AwesomeTheorems.THM_M_0533
