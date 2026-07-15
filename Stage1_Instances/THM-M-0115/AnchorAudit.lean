import Mathlib.Algebra.Homology.DerivedCategory.HomologySequence
import Mathlib.AlgebraicGeometry.Modules.Tilde
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.AlgebraicGeometry.QuasiAffine
import Mathlib.CategoryTheory.Sites.SheafCohomology.Basic
import Mathlib.GroupTheory.MonoidLocalization.GrothendieckGroup

/-!
# THM-M-0115 pinned anchor-audit probes

These checks bind the strongest adjacent APIs found in the pinned mathlib
snapshot. They cover the scheme, morphism, sheaf, derived-category, and generic
commutative-monoid group-completion substrate. None supplies scheme `K_0`,
rational Chow homology, Chern character, Todd class, or the frozen
Grothendieck-Riemann-Roch equality.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits AlgebraicGeometry

universe u v w w'

namespace Stage1Instances.THMM0115.AnchorAudit

def auditedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

def retainedSupportNames : List String := [
  "AlgebraicGeometry.Scheme",
  "AlgebraicGeometry.IsProper",
  "AlgebraicGeometry.Smooth",
  "AlgebraicGeometry.Scheme.IsQuasiAffine",
  "AlgebraicGeometry.Scheme.Modules",
  "AlgebraicGeometry.Scheme.Modules.pushforward",
  "AlgebraicGeometry.Scheme.Modules.pullback",
  "SheafOfModules.IsQuasicoherent",
  "CategoryTheory.Sheaf.H",
  "CategoryTheory.Sheaf.cohomologyFunctor",
  "DerivedCategory",
  "DerivedCategory.homologyFunctor",
  "Algebra.GrothendieckGroup"
]

def missingTerminalInterfaces : List String := [
  "quasi-projectivity of a scheme morphism or variety over a field",
  "scheme K_0 or G-theory with exact-sequence relations",
  "proper K-theory pushforward",
  "rational Chow homology or Chow ring with proper pushforward and cap product",
  "Chern character from the selected K-theory to the selected Chow theory",
  "algebraic tangent-bundle and Todd-class interfaces",
  "terminal Grothendieck-Riemann-Roch theorem"
]

/-- Checked wrapper for the ordinary sheaf-of-modules direct image. -/
noncomputable def modulesPushforward {X Y : Scheme.{u}} (f : X ⟶ Y) :=
  Scheme.Modules.pushforward f

/-- Checked wrapper for the ordinary sheaf-of-modules inverse image. -/
noncomputable def modulesPullback {X Y : Scheme.{u}} (f : X ⟶ Y) :=
  Scheme.Modules.pullback f

/-- The checked pullback/pushforward adjunction is only sheaf substrate. -/
noncomputable def modulesAdjunction {X Y : Scheme.{u}} (f : X ⟶ Y) :
    Scheme.Modules.pullback f ⊣ Scheme.Modules.pushforward f :=
  Scheme.Modules.pullbackPushforwardAdjunction f

/-- Affine tilde modules give a concrete quasi-coherent support example. -/
theorem tildeIsQuasicoherent (R : CommRingCat.{u}) (M : ModuleCat.{u} R) :
    (tilde M).IsQuasicoherent :=
  inferInstance

/-- Pinned sheaf cohomology carrier, not a Chow-homology carrier. -/
def sheafCohomology {C : Type u} [Category.{v} C]
    (J : GrothendieckTopology C) (F : Sheaf J AddCommGrpCat.{w})
    [HasSheafify J AddCommGrpCat.{w}]
    [HasExt.{w'} (Sheaf J AddCommGrpCat.{w})] (n : Nat) : Type w' :=
  F.H n

/-- Pinned derived-category homology substrate. -/
noncomputable def derivedHomology (C : Type u) [Category.{v} C] [Abelian C]
    [HasDerivedCategory.{w} C] (n : Int) :=
  DerivedCategory.homologyFunctor C n

/-- Mathlib's same-named object is group completion of a commutative monoid. -/
abbrev GenericMonoidGroupCompletion (M : Type u) [CommMonoid M] :=
  Algebra.GrothendieckGroup M

#check Scheme
#check Scheme.Spec
#check Scheme.Over
#check Scheme.Hom.IsOver
#check Scheme.Hom.isOver_iff
#check @IsProper
#check @Smooth
#check Scheme.IsQuasiAffine
#check Scheme.Modules
#check Scheme.Modules.pushforward
#check Scheme.Modules.pullback
#check Scheme.Modules.pullbackPushforwardAdjunction
#check SheafOfModules.IsQuasicoherent
#check tilde
#check CategoryTheory.Sheaf.H
#check CategoryTheory.Sheaf.cohomologyFunctor
#check DerivedCategory
#check DerivedCategory.homologyFunctor
#check Algebra.GrothendieckGroup
#check modulesPushforward
#check modulesPullback
#check modulesAdjunction
#check tildeIsQuasicoherent
#check sheafCohomology
#check derivedHomology
#check GenericMonoidGroupCompletion

#print axioms tildeIsQuasicoherent

end Stage1Instances.THMM0115.AnchorAudit
