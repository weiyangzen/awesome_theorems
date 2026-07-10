import Mathlib.AlgebraicGeometry.Cover.Directed
import Mathlib.AlgebraicGeometry.Cover.Open
import Mathlib.AlgebraicGeometry.Group.Abelian
import Mathlib.AlgebraicGeometry.Modules.Sheaf
import Mathlib.AlgebraicGeometry.Morphisms.Etale
import Mathlib.AlgebraicGeometry.Morphisms.FlatDescent
import Mathlib.AlgebraicGeometry.Morphisms.FinitePresentation
import Mathlib.AlgebraicGeometry.Morphisms.Flat
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.AlgebraicGeometry.Sites.Etale

/-!
# S1-M-026 / THM-M-0130: Hodge-type Shimura varieties

This Stage1 repair artifact records a conservative Lean 4 boundary for the
construction of Hodge-type Shimura varieties.

The pinned mathlib snapshot contains substantial scheme, morphism-property,
cover, sheaf, site, and adjacent group-scheme infrastructure.  It does not
currently expose a bundled definition of Hodge-type Shimura data, Siegel
embeddings, polarized abelian-scheme moduli with tensors, or a terminal
construction theorem.  The main theorem is therefore represented as a checked
statement shape over explicit predicate fields, with small local wrappers around
the imported substrate.
-/

noncomputable section

open AlgebraicGeometry CategoryTheory CategoryTheory.Limits Opposite

universe u v w

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_026

/-! ## Public statement normalization for THM-M-0130-P01

Canonical Lean namespace:
`AwesomeTheorems.Stage1.S1_M_026`.

Universe policy:
* `u` is the universe of the reflex field and the scheme target.
* `v` is reserved for the Shimura-datum carrier.
* `w` is reserved for the level-structure carrier.
The normalized statement remains universe-polymorphic in `{u, v, w}` and does
not collapse these carriers into a shared universe.

Variable policy:
the public statement has one datum variable
`D : HodgeTypeShimuraDatum.{u, v, w}` and five audited hypothesis variables:
`D.hasShimuraDatum`, `D.hasHodgeTypeEmbedding`, `D.hasAdmissibleLevel`,
`D.hasReflexFieldCompatibility`, and `D.hasHodgeTensorPackage`.

Statement shape:
`StatementShape : Prop` is the canonical repo-local normalized theorem target
for this Stage1 slot.  It asserts existence of a model package satisfying the
geometric and moduli/canonical predicates defined below, conditional on the
audited datum predicates.  This section is statement normalization only; it is
not a proof of the Hodge-type Shimura-variety construction.
-/

/-- Public canonical Lean namespace for the normalized THM-M-0130 target. -/
def normalizedLeanNamespace : String :=
  "AwesomeTheorems.Stage1.S1_M_026"

/-- Public universe policy for the normalized THM-M-0130 target. -/
def normalizedUniversePolicy : List String := [
  "universe u: reflex field and scheme target universe",
  "universe v: Shimura-datum carrier universe",
  "universe w: level-structure carrier universe",
  "StatementShape is universe-polymorphic in {u, v, w}"
]

/-- Public variable and hypothesis policy for the normalized statement shape. -/
def normalizedVariablePolicy : List String := [
  "D : HodgeTypeShimuraDatum.{u, v, w}",
  "hdatum : D.hasShimuraDatum",
  "hemb : D.hasHodgeTypeEmbedding",
  "hlevel : D.hasAdmissibleLevel",
  "hreflex : D.hasReflexFieldCompatibility",
  "htensors : D.hasHodgeTensorPackage"
]

/--
Input data for a future precise Hodge-type Shimura-variety construction.

The proposition fields are intentionally explicit placeholders.  Later work
must replace them by concrete local definitions or pinned upstream declarations
for Shimura data, Hodge-type embeddings, reflex fields, levels, Hodge tensors,
and the chosen generic or integral model target.
-/
structure HodgeTypeShimuraDatum where
  ReflexField : Type u
  field_reflexField : Field ReflexField
  shimuraDatum : Type v
  levelStructure : Type w
  hasShimuraDatum : Prop
  hasHodgeTypeEmbedding : Prop
  hasAdmissibleLevel : Prop
  hasReflexFieldCompatibility : Prop
  hasHodgeTensorPackage : Prop

attribute [instance] HodgeTypeShimuraDatum.field_reflexField

namespace HodgeTypeShimuraDatum

/-- The affine scheme over the reflex field attached to the datum. -/
abbrev baseScheme (D : HodgeTypeShimuraDatum.{u, v, w}) : Scheme.{u} :=
  Spec (.of D.ReflexField)

end HodgeTypeShimuraDatum

/--
Candidate output object for the Hodge-type Shimura construction.

The `Prop` fields name the theorem-specific obligations that are not present as
mathlib objects in the current dependency closure.
-/
structure HodgeTypeShimuraModel (D : HodgeTypeShimuraDatum.{u, v, w}) where
  X : Scheme.{u}
  structureMap : X ⟶ D.baseScheme
  representsAbelianSchemeModuli : Prop
  realizesHodgeTensors : Prop
  levelStructureCompatible : Prop
  satisfiesCanonicalModelProperty : Prop
  satisfiesIntegralModelProperty : Prop

/--
Scheme-side local properties expected from a usable Hodge-type Shimura model in
this Stage1 boundary.

This is only substrate: it does not assert the moduli interpretation.
-/
def GeometricModelPackage {D : HodgeTypeShimuraDatum.{u, v, w}}
    (M : HodgeTypeShimuraModel D) : Prop :=
  IsProper M.structureMap ∧ Smooth M.structureMap ∧ Flat M.structureMap

/-- The moduli/canonical obligations still missing from the local mathlib API. -/
def ModuliConstructionPackage {D : HodgeTypeShimuraDatum.{u, v, w}}
    (M : HodgeTypeShimuraModel D) : Prop :=
  M.representsAbelianSchemeModuli ∧
    M.realizesHodgeTensors ∧
      M.levelStructureCompatible ∧
        M.satisfiesCanonicalModelProperty ∧
          M.satisfiesIntegralModelProperty

/-! ## THM-M-0130-P04 split moduli branch

The following structures split the moduli branch into the six child packages
requested by P04: abelian schemes, polarizations, tensors, level structure,
functor definition, and representability.  They are checked statement-boundary
objects only.  The proposition fields must later be replaced by concrete
mathlib or pinned-upstream definitions before any construction theorem can be
claimed.
-/

/-- Abelian-scheme part of the Hodge-type moduli branch. -/
structure AbelianSchemeModuliBranch
    (D : HodgeTypeShimuraDatum.{u, v, w}) (M : HodgeTypeShimuraModel D) where
  abelianSchemeFamilyExists : Prop
  familyOverModel : Prop
  compatibleWithReflexBase : Prop

/-- Polarization part of the Hodge-type moduli branch. -/
structure PolarizationModuliBranch
    (D : HodgeTypeShimuraDatum.{u, v, w}) (M : HodgeTypeShimuraModel D) where
  polarizationExists : Prop
  polarizationPrimeToLevel : Prop
  polarizationCompatibleWithFamily : Prop

/-- Tensor/Hodge-cycle part of the Hodge-type moduli branch. -/
structure TensorModuliBranch
    (D : HodgeTypeShimuraDatum.{u, v, w}) (M : HodgeTypeShimuraModel D) where
  tensorPackageExists : Prop
  tensorsCutOutHodgeTypeLocus : Prop
  realizesHodgeTensors : M.realizesHodgeTensors

/-- Level-structure part of the Hodge-type moduli branch. -/
structure LevelStructureModuliBranch
    (D : HodgeTypeShimuraDatum.{u, v, w}) (M : HodgeTypeShimuraModel D) where
  levelStructureExists : Prop
  levelIsAdmissible : Prop
  levelStructureCompatible : M.levelStructureCompatible

/-- Functor-definition part of the Hodge-type moduli branch. -/
structure ModuliFunctorDefinitionBranch
    (D : HodgeTypeShimuraDatum.{u, v, w}) (M : HodgeTypeShimuraModel D) where
  functorOnTestSchemesDefined : Prop
  isomorphismRelationDefined : Prop
  functorialPullbackDefined : Prop

/-- Representability part of the Hodge-type moduli branch. -/
structure RepresentabilityModuliBranch
    (D : HodgeTypeShimuraDatum.{u, v, w}) (M : HodgeTypeShimuraModel D) where
  representsFunctor : M.representsAbelianSchemeModuli
  representedByModelScheme : Prop
  universalFamilyCompatible : Prop

/--
Checked P04 split package for the moduli branch.

This is stronger bookkeeping than the earlier flat `ModuliConstructionPackage`,
but it is still only a statement-boundary object: the fields are obligations,
not construction proofs.
-/
structure SplitModuliBranch
    (D : HodgeTypeShimuraDatum.{u, v, w}) (M : HodgeTypeShimuraModel D) where
  abelianSchemes : AbelianSchemeModuliBranch D M
  polarizations : PolarizationModuliBranch D M
  tensors : TensorModuliBranch D M
  levelStructure : LevelStructureModuliBranch D M
  functorDefinition : ModuliFunctorDefinitionBranch D M
  representability : RepresentabilityModuliBranch D M
  canonicalModelProperty : M.satisfiesCanonicalModelProperty
  integralModelProperty : M.satisfiesIntegralModelProperty

/--
A completed split P04 package refines the older flat moduli package.
This theorem proves only the bookkeeping implication between local predicates.
-/
theorem SplitModuliBranch.toModuliConstructionPackage
    {D : HodgeTypeShimuraDatum.{u, v, w}} {M : HodgeTypeShimuraModel D}
    (h : SplitModuliBranch D M) :
    ModuliConstructionPackage M :=
  ⟨h.representability.representsFunctor,
    h.tensors.realizesHodgeTensors,
    h.levelStructure.levelStructureCompatible,
    h.canonicalModelProperty,
    h.integralModelProperty⟩

/-- Projection wrapper for the P04 abelian-scheme branch. -/
def splitModuliBranch_abelianSchemes
    {D : HodgeTypeShimuraDatum.{u, v, w}} {M : HodgeTypeShimuraModel D}
    (h : SplitModuliBranch D M) :
    AbelianSchemeModuliBranch D M :=
  h.abelianSchemes

/-- Projection wrapper for the P04 polarization branch. -/
def splitModuliBranch_polarizations
    {D : HodgeTypeShimuraDatum.{u, v, w}} {M : HodgeTypeShimuraModel D}
    (h : SplitModuliBranch D M) :
    PolarizationModuliBranch D M :=
  h.polarizations

/-- Projection wrapper for the P04 tensor branch. -/
def splitModuliBranch_tensors
    {D : HodgeTypeShimuraDatum.{u, v, w}} {M : HodgeTypeShimuraModel D}
    (h : SplitModuliBranch D M) :
    TensorModuliBranch D M :=
  h.tensors

/-- Projection wrapper for the P04 level-structure branch. -/
def splitModuliBranch_levelStructure
    {D : HodgeTypeShimuraDatum.{u, v, w}} {M : HodgeTypeShimuraModel D}
    (h : SplitModuliBranch D M) :
    LevelStructureModuliBranch D M :=
  h.levelStructure

/-- Projection wrapper for the P04 moduli-functor branch. -/
def splitModuliBranch_functorDefinition
    {D : HodgeTypeShimuraDatum.{u, v, w}} {M : HodgeTypeShimuraModel D}
    (h : SplitModuliBranch D M) :
    ModuliFunctorDefinitionBranch D M :=
  h.functorDefinition

/-- Projection wrapper for the P04 representability branch. -/
def splitModuliBranch_representability
    {D : HodgeTypeShimuraDatum.{u, v, w}} {M : HodgeTypeShimuraModel D}
    (h : SplitModuliBranch D M) :
    RepresentabilityModuliBranch D M :=
  h.representability

/-! ## THM-M-0130-P05 local-property proof plan

The following checked objects split the local-property branch into proper,
smooth, flat, etale, and finite-presentation obligations.  The finite
presentation branch follows the convention in mathlib's
`Morphism.FinitePresentation`: finite presentation of a scheme morphism is
represented by `LocallyOfFinitePresentation f` together with `QuasiCompact f`,
not by a separate bundled predicate.
-/

/-- Properness branch for a scheme morphism in the P05 local-property plan. -/
structure ProperLocalPropertyBranch {X Y : Scheme.{u}} (f : X ⟶ Y) where
  proper : IsProper f

/-- Smoothness branch for a scheme morphism in the P05 local-property plan. -/
structure SmoothLocalPropertyBranch {X Y : Scheme.{u}} (f : X ⟶ Y) where
  smooth : Smooth f

/-- Flatness branch for a scheme morphism in the P05 local-property plan. -/
structure FlatLocalPropertyBranch {X Y : Scheme.{u}} (f : X ⟶ Y) where
  flat : Flat f

/-- Etaleness branch for a scheme morphism in the P05 local-property plan. -/
structure EtaleLocalPropertyBranch {X Y : Scheme.{u}} (f : X ⟶ Y) where
  etale : Etale f

/--
Finite-presentation branch for a scheme morphism.

mathlib represents finite presentation for morphisms as locally finite
presentation plus quasi-compactness.
-/
structure FinitePresentationLocalPropertyBranch {X Y : Scheme.{u}} (f : X ⟶ Y) where
  locallyOfFinitePresentation : LocallyOfFinitePresentation f
  quasiCompact : QuasiCompact f

/--
Combined P05 proof-plan obligations for one morphism.

This is a branch ledger, not an existence theorem: a future construction proof
must supply these fields for the relevant model or level morphisms.
-/
structure LocalPropertyProofPlan {X Y : Scheme.{u}} (f : X ⟶ Y) where
  properBranch : ProperLocalPropertyBranch f
  smoothBranch : SmoothLocalPropertyBranch f
  flatBranch : FlatLocalPropertyBranch f
  etaleBranch : EtaleLocalPropertyBranch f
  finitePresentationBranch : FinitePresentationLocalPropertyBranch f

/--
Structure-map part of the P05 plan.

The etale branch is intentionally kept separate, since for Shimura applications
it may belong to a level cover or local chart rather than to the model
structure morphism.
-/
structure StructureMapLocalPropertyProofPlan {X Y : Scheme.{u}} (f : X ⟶ Y) where
  properBranch : ProperLocalPropertyBranch f
  smoothBranch : SmoothLocalPropertyBranch f
  flatBranch : FlatLocalPropertyBranch f
  finitePresentationBranch : FinitePresentationLocalPropertyBranch f

/-- An auxiliary etale morphism branch for level covers or local charts. -/
structure AuxiliaryEtaleLocalPropertyBranch where
  X : Scheme.{u}
  Y : Scheme.{u}
  f : X ⟶ Y
  etaleBranch : EtaleLocalPropertyBranch f

/-- The smooth branch supplies the mathlib flatness predicate. -/
theorem SmoothLocalPropertyBranch.toFlat {X Y : Scheme.{u}} {f : X ⟶ Y}
    (h : SmoothLocalPropertyBranch f) :
    Flat f := by
  letI : Smooth f := h.smooth
  infer_instance

/-- The smooth branch supplies the mathlib locally-finite-presentation predicate. -/
theorem SmoothLocalPropertyBranch.toLocallyOfFinitePresentation
    {X Y : Scheme.{u}} {f : X ⟶ Y} (h : SmoothLocalPropertyBranch f) :
    LocallyOfFinitePresentation f := by
  letI : Smooth f := h.smooth
  infer_instance

/-- The etale branch supplies the mathlib smoothness predicate. -/
theorem EtaleLocalPropertyBranch.toSmooth {X Y : Scheme.{u}} {f : X ⟶ Y}
    (h : EtaleLocalPropertyBranch f) :
    Smooth f := by
  letI : Etale f := h.etale
  infer_instance

/-- The etale branch supplies the mathlib flatness predicate. -/
theorem EtaleLocalPropertyBranch.toFlat {X Y : Scheme.{u}} {f : X ⟶ Y}
    (h : EtaleLocalPropertyBranch f) :
    Flat f := by
  letI : Etale f := h.etale
  infer_instance

/-- The etale branch supplies the mathlib locally-finite-presentation predicate. -/
theorem EtaleLocalPropertyBranch.toLocallyOfFinitePresentation
    {X Y : Scheme.{u}} {f : X ⟶ Y} (h : EtaleLocalPropertyBranch f) :
    LocallyOfFinitePresentation f := by
  letI : Etale f := h.etale
  infer_instance

/-- The proper branch supplies the mathlib locally-finite-type predicate. -/
theorem ProperLocalPropertyBranch.toLocallyOfFiniteType
    {X Y : Scheme.{u}} {f : X ⟶ Y} (h : ProperLocalPropertyBranch f) :
    LocallyOfFiniteType f := by
  letI : IsProper f := h.proper
  infer_instance

/-- The finite-presentation branch exposes its two mathlib components as a conjunction. -/
theorem FinitePresentationLocalPropertyBranch.asPair
    {X Y : Scheme.{u}} {f : X ⟶ Y} (h : FinitePresentationLocalPropertyBranch f) :
    LocallyOfFinitePresentation f ∧ QuasiCompact f :=
  ⟨h.locallyOfFinitePresentation, h.quasiCompact⟩

/-- The finite-presentation branch supplies the mathlib locally-finite-type predicate. -/
theorem FinitePresentationLocalPropertyBranch.toLocallyOfFiniteType
    {X Y : Scheme.{u}} {f : X ⟶ Y} (h : FinitePresentationLocalPropertyBranch f) :
    LocallyOfFiniteType f := by
  letI : LocallyOfFinitePresentation f := h.locallyOfFinitePresentation
  infer_instance

/-- Smoothness plus quasi-compactness gives the P05 finite-presentation branch. -/
def FinitePresentationLocalPropertyBranch.of_smooth_of_quasiCompact
    {X Y : Scheme.{u}} {f : X ⟶ Y} (hs : SmoothLocalPropertyBranch f)
    (hqc : QuasiCompact f) :
    FinitePresentationLocalPropertyBranch f where
  locallyOfFinitePresentation := by
    letI : Smooth f := hs.smooth
    infer_instance
  quasiCompact := hqc

/-- Etaleness plus quasi-compactness gives the P05 finite-presentation branch. -/
def FinitePresentationLocalPropertyBranch.of_etale_of_quasiCompact
    {X Y : Scheme.{u}} {f : X ⟶ Y} (he : EtaleLocalPropertyBranch f)
    (hqc : QuasiCompact f) :
    FinitePresentationLocalPropertyBranch f where
  locallyOfFinitePresentation := by
    letI : Etale f := he.etale
    infer_instance
  quasiCompact := hqc

/-- The P05 plan refines the existing geometric package for a Hodge-type model. -/
theorem LocalPropertyProofPlan.toGeometricModelPackage
    {D : HodgeTypeShimuraDatum.{u, v, w}} {M : HodgeTypeShimuraModel D}
    (h : LocalPropertyProofPlan M.structureMap) :
    GeometricModelPackage M :=
  ⟨h.properBranch.proper, h.smoothBranch.smooth, h.flatBranch.flat⟩

/-- The structure-map part of the P05 plan refines the existing geometric package. -/
theorem StructureMapLocalPropertyProofPlan.toGeometricModelPackage
    {D : HodgeTypeShimuraDatum.{u, v, w}} {M : HodgeTypeShimuraModel D}
    (h : StructureMapLocalPropertyProofPlan M.structureMap) :
    GeometricModelPackage M :=
  ⟨h.properBranch.proper, h.smoothBranch.smooth, h.flatBranch.flat⟩

/--
Hodge-type P05 plan: structure-map properties plus a separate etale branch.

The separate etale branch avoids forcing the model structure morphism itself to
be etale before the normalized theorem fixes where etaleness is needed.
-/
structure HodgeTypeLocalPropertyProofPlan
    {D : HodgeTypeShimuraDatum.{u, v, w}} (M : HodgeTypeShimuraModel D) where
  structureMapPlan : StructureMapLocalPropertyProofPlan M.structureMap
  auxiliaryEtaleBranch : AuxiliaryEtaleLocalPropertyBranch.{u}

/-! ## THM-M-0130-P06 descent and gluing branch

This section records the checked repo-local boundary for the descent/gluing
branch.  It deliberately exposes the imported `Scheme.Cover`/`OpenCover`
gluing API and `MorphismProperty.DescendsAlong` API, but it does not construct
Shimura moduli objects or prove that their descent data are effective.
-/

/-- The fpqc-style morphism property used by mathlib's flat-descent API. -/
abbrev fpqcDescentProperty : MorphismProperty Scheme.{u} :=
  @Surjective ⊓ @Flat ⊓ @QuasiCompact

/--
Directed-open-cover gluing branch for morphisms out of a scheme.

The branch is parameterized by an existing locally directed open cover.  The
glued morphism below is a genuine mathlib construction; the two `Prop` fields
are theorem-specific obligations for future Shimura moduli data.
-/
structure DirectedOpenCoverGluingBranch {X : Scheme.{u}} (𝒰 : X.OpenCover)
    [Category 𝒰.I₀] [𝒰.LocallyDirected] (Y : Scheme.{u}) where
  localMorphism : ∀ i, 𝒰.X i ⟶ Y
  transitionCompatible :
    ∀ {i j : 𝒰.I₀} (hij : i ⟶ j), 𝒰.trans hij ≫ localMorphism j = localMorphism i
  localModuliCompatibility : ∀ _i : 𝒰.I₀, Prop
  transitionModuliCompatibility : Prop

/-- The global morphism obtained by mathlib directed-open-cover gluing. -/
def DirectedOpenCoverGluingBranch.gluedMorphism
    {X : Scheme.{u}} {𝒰 : X.OpenCover} [Category 𝒰.I₀] [𝒰.LocallyDirected]
    {Y : Scheme.{u}} (h : DirectedOpenCoverGluingBranch 𝒰 Y) :
    X ⟶ Y :=
  𝒰.glueMorphismsOfLocallyDirected h.localMorphism h.transitionCompatible

/-- The glued morphism restricts to the local morphism on each cover member. -/
theorem DirectedOpenCoverGluingBranch.restricts
    {X : Scheme.{u}} {𝒰 : X.OpenCover} [Category 𝒰.I₀] [𝒰.LocallyDirected]
    {Y : Scheme.{u}} (h : DirectedOpenCoverGluingBranch 𝒰 Y) (i : 𝒰.I₀) :
    𝒰.f i ≫ h.gluedMorphism = h.localMorphism i := by
  simp [DirectedOpenCoverGluingBranch.gluedMorphism]

/--
Directed-open-cover gluing branch for morphisms over a fixed base scheme.

This is the over-category version needed by later moduli and canonical-model
branches, where local charts must glue compatibly with the structure map.
-/
structure DirectedOpenCoverOverGluingBranch {S : Scheme.{u}} {X : Over S}
    (𝒰 : X.left.OpenCover) [Category 𝒰.I₀] [𝒰.LocallyDirected] (Y : Over S) where
  localMorphism : ∀ i, 𝒰.X i ⟶ Y.left
  transitionCompatible :
    ∀ {i j : 𝒰.I₀} (hij : i ⟶ j), 𝒰.trans hij ≫ localMorphism j = localMorphism i
  overCompatible : ∀ i, localMorphism i ≫ Y.hom = 𝒰.f i ≫ X.hom
  localModuliCompatibility : ∀ _i : 𝒰.I₀, Prop
  transitionModuliCompatibility : Prop

/-- The global over-morphism obtained by mathlib directed-open-cover gluing. -/
def DirectedOpenCoverOverGluingBranch.gluedOverMorphism
    {S : Scheme.{u}} {X : Over S} {𝒰 : X.left.OpenCover}
    [Category 𝒰.I₀] [𝒰.LocallyDirected] {Y : Over S}
    (h : DirectedOpenCoverOverGluingBranch 𝒰 Y) :
    X ⟶ Y :=
  𝒰.glueMorphismsOverOfLocallyDirected h.localMorphism h.transitionCompatible h.overCompatible

/-- The glued over-morphism restricts to the local morphism on each cover member. -/
theorem DirectedOpenCoverOverGluingBranch.restricts_left
    {S : Scheme.{u}} {X : Over S} {𝒰 : X.left.OpenCover}
    [Category 𝒰.I₀] [𝒰.LocallyDirected] {Y : Over S}
    (h : DirectedOpenCoverOverGluingBranch 𝒰 Y) (i : 𝒰.I₀) :
    𝒰.f i ≫ h.gluedOverMorphism.left = h.localMorphism i := by
  simp [DirectedOpenCoverOverGluingBranch.gluedOverMorphism]

/--
Generic morphism-property descent branch.

Given a cover morphism satisfying `Q`, a property `P` on the pullback, and a
`P.DescendsAlong Q` instance, this branch proves the descended property on the
original morphism through mathlib's `MorphismProperty` API.
-/
structure CoverDescentBranch (P Q : MorphismProperty Scheme.{u})
    {X Y Z : Scheme.{u}} (f : X ⟶ Z) (g : Y ⟶ Z) [HasPullback f g] where
  descentCoverProperty : Q f
  pullbackLocalProperty : P (pullback.fst f g)
  propertyDescends : P.DescendsAlong Q

/-- A checked wrapper around `MorphismProperty.of_pullback_fst_of_descendsAlong`. -/
theorem CoverDescentBranch.descendedProperty
    {P Q : MorphismProperty Scheme.{u}} {X Y Z : Scheme.{u}}
    {f : X ⟶ Z} {g : Y ⟶ Z} [HasPullback f g]
    (h : CoverDescentBranch P Q f g) :
    P g := by
  letI : P.DescendsAlong Q := h.propertyDescends
  exact MorphismProperty.of_pullback_fst_of_descendsAlong
    h.descentCoverProperty h.pullbackLocalProperty

/-- fpqc-specialized morphism-property descent branch. -/
structure FpqcDescentBranch (P : MorphismProperty Scheme.{u})
    {X Y Z : Scheme.{u}} (f : X ⟶ Z) (g : Y ⟶ Z) [HasPullback f g] where
  coverSurjective : Surjective f
  coverFlat : Flat f
  coverQuasiCompact : QuasiCompact f
  pullbackHasProperty : P (pullback.fst f g)
  descendsAlongFpqc : P.DescendsAlong fpqcDescentProperty

/-- The component predicates assemble into the fpqc descent-cover property. -/
theorem FpqcDescentBranch.coverProperty
    {P : MorphismProperty Scheme.{u}} {X Y Z : Scheme.{u}}
    {f : X ⟶ Z} {g : Y ⟶ Z} [HasPullback f g]
    (h : FpqcDescentBranch P f g) :
    fpqcDescentProperty f :=
  ⟨⟨h.coverSurjective, h.coverFlat⟩, h.coverQuasiCompact⟩

/-- A checked fpqc-specialized wrapper around morphism-property descent. -/
theorem FpqcDescentBranch.descendedProperty
    {P : MorphismProperty Scheme.{u}} {X Y Z : Scheme.{u}}
    {f : X ⟶ Z} {g : Y ⟶ Z} [HasPullback f g]
    (h : FpqcDescentBranch P f g) :
    P g := by
  letI : P.DescendsAlong fpqcDescentProperty := h.descendsAlongFpqc
  exact MorphismProperty.of_pullback_fst_of_descendsAlong
    h.coverProperty h.pullbackHasProperty

/-- mathlib anchor: open immersions descend along fpqc morphisms. -/
theorem openImmersion_descendsAlong_fpqc :
    (@IsOpenImmersion : MorphismProperty Scheme.{u}).DescendsAlong fpqcDescentProperty := by
  infer_instance

/-- fpqc descent branch specialized to open immersions, used for gluing charts. -/
structure FpqcOpenImmersionDescentBranch
    {X Y Z : Scheme.{u}} (f : X ⟶ Z) (g : Y ⟶ Z) [HasPullback f g] where
  coverSurjective : Surjective f
  coverFlat : Flat f
  coverQuasiCompact : QuasiCompact f
  pullbackOpenImmersion : IsOpenImmersion (pullback.fst f g)

/-- The component predicates assemble into the fpqc descent-cover property. -/
theorem FpqcOpenImmersionDescentBranch.coverProperty
    {X Y Z : Scheme.{u}} {f : X ⟶ Z} {g : Y ⟶ Z} [HasPullback f g]
    (h : FpqcOpenImmersionDescentBranch f g) :
    fpqcDescentProperty f :=
  ⟨⟨h.coverSurjective, h.coverFlat⟩, h.coverQuasiCompact⟩

/-- fpqc descent of an open immersion from its pullback. -/
theorem FpqcOpenImmersionDescentBranch.descendedOpenImmersion
    {X Y Z : Scheme.{u}} {f : X ⟶ Z} {g : Y ⟶ Z} [HasPullback f g]
    (h : FpqcOpenImmersionDescentBranch f g) :
    IsOpenImmersion g := by
  exact MorphismProperty.of_pullback_fst_of_descendsAlong
    (P := @IsOpenImmersion) (Q := fpqcDescentProperty)
    h.coverProperty h.pullbackOpenImmersion

/--
P06 branch attached to a candidate Hodge-type model.

It combines directed open-cover gluing for local chart morphisms with an
fpqc/open-immersion descent branch.  The remaining `Prop` fields are the
Shimura-specific effectiveness obligations: local abelian-scheme moduli data,
Hodge tensors, and level structures still need concrete definitions and proofs.
-/
structure HodgeTypeDescentGluingBranch
    {D : HodgeTypeShimuraDatum.{u, v, w}} (M : HodgeTypeShimuraModel D)
    (𝒰 : M.X.OpenCover) [Category 𝒰.I₀] [𝒰.LocallyDirected] where
  gluingTarget : Scheme.{u}
  directedChartGluing : DirectedOpenCoverGluingBranch 𝒰 gluingTarget
  fpqcDescentTarget : Scheme.{u}
  fpqcCover : Scheme.{u}
  fpqcCoverMap : fpqcCover ⟶ fpqcDescentTarget
  fpqcModelMap : M.X ⟶ fpqcDescentTarget
  fpqcOpenImmersionDescent : FpqcOpenImmersionDescentBranch fpqcCoverMap fpqcModelMap
  moduliObjectsGlueAcrossCover : Prop
  hodgeTensorsDescendAcrossCover : Prop
  levelStructureDescendsAcrossCover : Prop

/-- The P06 branch provides the globally glued chart morphism. -/
def HodgeTypeDescentGluingBranch.gluedChartMorphism
    {D : HodgeTypeShimuraDatum.{u, v, w}} {M : HodgeTypeShimuraModel D}
    {𝒰 : M.X.OpenCover} [Category 𝒰.I₀] [𝒰.LocallyDirected]
    (h : HodgeTypeDescentGluingBranch M 𝒰) :
    M.X ⟶ h.gluingTarget :=
  h.directedChartGluing.gluedMorphism

/-- The P06 branch provides an fpqc-descended open immersion for the model map. -/
theorem HodgeTypeDescentGluingBranch.fpqcModelMap_openImmersion
    {D : HodgeTypeShimuraDatum.{u, v, w}} {M : HodgeTypeShimuraModel D}
    {𝒰 : M.X.OpenCover} [Category 𝒰.I₀] [𝒰.LocallyDirected]
    (h : HodgeTypeDescentGluingBranch M 𝒰) :
    IsOpenImmersion h.fpqcModelMap :=
  h.fpqcOpenImmersionDescent.descendedOpenImmersion

/-! ## THM-M-0130-P07 optional cohomological realization branch

The normalized `StatementShape` below is a construction statement for the model
package over the reflex-field base.  It does not require an ell-adic,
pro-etale, or other cohomological realization package.  This section records
that branch as optional unless a future normalized statement explicitly asks
for it.
-/

/-- P07 status for the ell-adic/cohomological realization branch. -/
inductive CohomologicalRealizationBranchStatus where
  | optionalUnlessRequiredByNormalizedStatement
  | requiredByNormalizedStatement
deriving DecidableEq, Repr

/-- Stable text label for a P07 cohomological-realization status. -/
def CohomologicalRealizationBranchStatus.label :
    CohomologicalRealizationBranchStatus → String
  | .optionalUnlessRequiredByNormalizedStatement =>
      "optional_unless_required_by_normalized_statement"
  | .requiredByNormalizedStatement => "required_by_normalized_statement"

/--
Future optional realization package for a Hodge-type model.

These fields intentionally remain theorem-specific obligations.  They are not
part of the current normalized construction statement.
-/
structure CohomologicalRealizationBranch
    (D : HodgeTypeShimuraDatum.{u, v, w}) (M : HodgeTypeShimuraModel D) where
  ellAdicRealizationData : Prop
  cohomologyComparisonCompatible : Prop
  canonicalModelActionCompatible : Prop

/--
Optional wrapper for the cohomological branch.

If a future normalized statement requires such a branch, `branchIfRequired`
must supply it.  For the current normalized statement the requirement predicate
is false, so this wrapper carries no extra theorem obligation.
-/
structure OptionalCohomologicalRealizationPackage
    (D : HodgeTypeShimuraDatum.{u, v, w}) (M : HodgeTypeShimuraModel D) where
  requiredByNormalizedStatement : Prop
  branchIfRequired :
    requiredByNormalizedStatement → CohomologicalRealizationBranch D M

/-- Current P07 decision for the normalized THM-M-0130 statement. -/
def p07CohomologicalRealizationBranchStatus :
    CohomologicalRealizationBranchStatus :=
  .optionalUnlessRequiredByNormalizedStatement

/--
The current normalized construction statement does not require a
cohomological-realization package.
-/
def p07CurrentStatementRequiresCohomologicalRealization : Prop :=
  False

/-- Checked P07 status label for public backfill. -/
theorem p07CohomologicalRealizationBranchStatus_is_optional :
    p07CohomologicalRealizationBranchStatus =
      .optionalUnlessRequiredByNormalizedStatement :=
  rfl

/-- The current statement has no required cohomological-realization branch. -/
theorem p07_currentStatement_doesNotRequireCohomologicalRealization :
    ¬ p07CurrentStatementRequiresCohomologicalRealization := by
  intro h
  exact h

/-- The vacuous optional P07 package attached to the current statement shape. -/
def optionalCohomologicalRealizationPackage
    (D : HodgeTypeShimuraDatum.{u, v, w}) (M : HodgeTypeShimuraModel D) :
    OptionalCohomologicalRealizationPackage D M where
  requiredByNormalizedStatement :=
    p07CurrentStatementRequiresCohomologicalRealization
  branchIfRequired := by
    intro h
    exact False.elim h

/--
Variant statement shape for a future theorem version that explicitly requires
the cohomological-realization branch.
-/
def StatementShapeWithRequiredCohomologicalRealization : Prop :=
  ∀ D : HodgeTypeShimuraDatum.{u, v, w},
    D.hasShimuraDatum →
      D.hasHodgeTypeEmbedding →
        D.hasAdmissibleLevel →
          D.hasReflexFieldCompatibility →
            D.hasHodgeTensorPackage →
              Nonempty { M : HodgeTypeShimuraModel D //
                GeometricModelPackage M ∧ ModuliConstructionPackage M ∧
                  Nonempty (CohomologicalRealizationBranch D M) }

/--
Normalized Stage1 statement shape for THM-M-0130.

It says that every fully specified Hodge-type datum with compatible level,
reflex field, and Hodge tensor package admits a scheme over the reflex field
with the expected geometric and moduli/canonical properties.  This is not a
repo-local proof of the construction.
-/
def StatementShape : Prop :=
  ∀ D : HodgeTypeShimuraDatum.{u, v, w},
    D.hasShimuraDatum →
      D.hasHodgeTypeEmbedding →
        D.hasAdmissibleLevel →
          D.hasReflexFieldCompatibility →
            D.hasHodgeTensorPackage →
              Nonempty { M : HodgeTypeShimuraModel D //
                GeometricModelPackage M ∧ ModuliConstructionPackage M }

/--
Checked wrapper: a proof of the statement shape supplies the model package for
any resolved datum satisfying the audited input predicates.
-/
theorem modelPackage_of_statementShape
    (h : StatementShape.{u, v, w}) (D : HodgeTypeShimuraDatum.{u, v, w})
    (hdatum : D.hasShimuraDatum)
    (hemb : D.hasHodgeTypeEmbedding)
    (hlevel : D.hasAdmissibleLevel)
    (hreflex : D.hasReflexFieldCompatibility)
    (htensors : D.hasHodgeTensorPackage) :
    Nonempty { M : HodgeTypeShimuraModel D //
      GeometricModelPackage M ∧ ModuliConstructionPackage M } :=
  h D hdatum hemb hlevel hreflex htensors

/--
A proof of the current statement shape automatically gives the same model
package with the P07 optional realization wrapper attached.
-/
theorem modelPackageWithOptionalCohomologicalRealization_of_statementShape
    (h : StatementShape.{u, v, w}) (D : HodgeTypeShimuraDatum.{u, v, w})
    (hdatum : D.hasShimuraDatum)
    (hemb : D.hasHodgeTypeEmbedding)
    (hlevel : D.hasAdmissibleLevel)
    (hreflex : D.hasReflexFieldCompatibility)
    (htensors : D.hasHodgeTensorPackage) :
    Nonempty { M : HodgeTypeShimuraModel D //
      GeometricModelPackage M ∧ ModuliConstructionPackage M ∧
        Nonempty (OptionalCohomologicalRealizationPackage D M) } := by
  rcases h D hdatum hemb hlevel hreflex htensors with ⟨M, hM⟩
  exact ⟨⟨M, hM.1, hM.2, ⟨optionalCohomologicalRealizationPackage D M⟩⟩⟩

/--
If a future normalized theorem proves the stronger required-realization
variant, then it also proves the current construction statement.
-/
theorem statementShape_of_statementShapeWithRequiredCohomologicalRealization
    (h : StatementShapeWithRequiredCohomologicalRealization.{u, v, w}) :
    StatementShape.{u, v, w} := by
  intro D hdatum hemb hlevel hreflex htensors
  rcases h D hdatum hemb hlevel hreflex htensors with ⟨M, hM⟩
  exact ⟨⟨M, hM.1, hM.2.1⟩⟩

/-- Projection wrapper for the properness component of the geometric package. -/
theorem geometricModel_proper {D : HodgeTypeShimuraDatum.{u, v, w}}
    {M : HodgeTypeShimuraModel D} (h : GeometricModelPackage M) :
    IsProper M.structureMap :=
  h.1

/-- Projection wrapper for the smoothness component of the geometric package. -/
theorem geometricModel_smooth {D : HodgeTypeShimuraDatum.{u, v, w}}
    {M : HodgeTypeShimuraModel D} (h : GeometricModelPackage M) :
    Smooth M.structureMap :=
  h.2.1

/-- Projection wrapper for the flatness component of the geometric package. -/
theorem geometricModel_flat {D : HodgeTypeShimuraDatum.{u, v, w}}
    {M : HodgeTypeShimuraModel D} (h : GeometricModelPackage M) :
    Flat M.structureMap :=
  h.2.2

/-- Projection wrapper for the moduli-representability component. -/
theorem moduliPackage_represents {D : HodgeTypeShimuraDatum.{u, v, w}}
    {M : HodgeTypeShimuraModel D} (h : ModuliConstructionPackage M) :
    M.representsAbelianSchemeModuli :=
  h.1

/-- Projection wrapper for the Hodge-tensor component. -/
theorem moduliPackage_hodgeTensors {D : HodgeTypeShimuraDatum.{u, v, w}}
    {M : HodgeTypeShimuraModel D} (h : ModuliConstructionPackage M) :
    M.realizesHodgeTensors :=
  h.2.1

/-- Projection wrapper for the level-structure component. -/
theorem moduliPackage_level {D : HodgeTypeShimuraDatum.{u, v, w}}
    {M : HodgeTypeShimuraModel D} (h : ModuliConstructionPackage M) :
    M.levelStructureCompatible :=
  h.2.2.1

/-- Projection wrapper for the canonical-model component. -/
theorem moduliPackage_canonical {D : HodgeTypeShimuraDatum.{u, v, w}}
    {M : HodgeTypeShimuraModel D} (h : ModuliConstructionPackage M) :
    M.satisfiesCanonicalModelProperty :=
  h.2.2.2.1

/-- Projection wrapper for the integral-model component. -/
theorem moduliPackage_integral {D : HodgeTypeShimuraDatum.{u, v, w}}
    {M : HodgeTypeShimuraModel D} (h : ModuliConstructionPackage M) :
    M.satisfiesIntegralModelProperty :=
  h.2.2.2.2

/-! ## Imported mathlib substrate anchors -/

/-- Pinned mathlib revision used for the THM-M-0130-P02 anchor audit. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- One checked mathlib anchor row for the THM-M-0130-P02 substrate table. -/
structure MathlibAnchorRow where
  area : String
  moduleName : String
  checkedAnchor : String
  roleForShimuraBoundary : String
  completionBoundary : String

/--
Mathlib anchor table for THM-M-0130-P02 at the pinned mathlib revision.

Each row names a module that is either imported directly above or checked
through a declaration used by this file.  These anchors are substrate only:
they do not provide a Hodge-type Shimura-variety construction theorem.
-/
def mathlibAnchorTable : List MathlibAnchorRow := [
  {
    area := "scheme",
    moduleName := "Mathlib.AlgebraicGeometry.Scheme",
    checkedAnchor := "Scheme, Spec (.of K), scheme morphisms",
    roleForShimuraBoundary := "base object and model target for the normalized statement",
    completionBoundary := "scheme infrastructure only; no Shimura datum or canonical model construction"
  },
  {
    area := "scheme-cover",
    moduleName := "Mathlib.AlgebraicGeometry.Cover.Open",
    checkedAnchor := "Scheme.OpenCover and X.affineCover",
    roleForShimuraBoundary := "cover substrate for later descent and gluing branches",
    completionBoundary := "cover infrastructure only; no moduli representability proof"
  },
  {
    area := "cover-gluing",
    moduleName := "Mathlib.AlgebraicGeometry.Cover.Directed",
    checkedAnchor := "Scheme.OpenCover.glueMorphismsOfLocallyDirected",
    roleForShimuraBoundary := "directed open-cover substrate for P06 local-to-global gluing",
    completionBoundary := "glues scheme morphisms only; no Shimura moduli object is constructed"
  },
  {
    area := "morphism-property",
    moduleName := "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
    checkedAnchor := "Smooth f",
    roleForShimuraBoundary := "smoothness predicate for geometric model packages",
    completionBoundary := "local property predicate only; no proof that the Shimura model is smooth"
  },
  {
    area := "morphism-property",
    moduleName := "Mathlib.AlgebraicGeometry.Morphisms.Proper",
    checkedAnchor := "IsProper f",
    roleForShimuraBoundary := "properness predicate for geometric model packages",
    completionBoundary := "local property predicate only; no proof that the Shimura model is proper"
  },
  {
    area := "morphism-property",
    moduleName := "Mathlib.AlgebraicGeometry.Morphisms.Flat",
    checkedAnchor := "Flat f",
    roleForShimuraBoundary := "flatness predicate for geometric model packages",
    completionBoundary := "local property predicate only; no proof that the Shimura model is flat"
  },
  {
    area := "morphism-property",
    moduleName := "Mathlib.AlgebraicGeometry.Morphisms.FinitePresentation",
    checkedAnchor := "LocallyOfFinitePresentation f and QuasiCompact f",
    roleForShimuraBoundary := "finite-presentation branch for local-property proof plans",
    completionBoundary := "API substrate only; finite presentation of the Shimura model is not proved"
  },
  {
    area := "morphism-property",
    moduleName := "Mathlib.AlgebraicGeometry.Morphisms.Etale",
    checkedAnchor := "Etale f",
    roleForShimuraBoundary := "etale predicate for level and optional local-property branches",
    completionBoundary := "local property predicate only; no level-structure theorem"
  },
  {
    area := "morphism-property-descent",
    moduleName := "Mathlib.AlgebraicGeometry.Morphisms.FlatDescent",
    checkedAnchor := "MorphismProperty.DescendsAlong and fpqc descent of IsOpenImmersion",
    roleForShimuraBoundary := "fpqc/descent substrate for P06 morphism-property descent branches",
    completionBoundary := "descent API only; no Hodge-type Shimura descent data are proved effective"
  },
  {
    area := "site",
    moduleName := "Mathlib.AlgebraicGeometry.Sites.Etale",
    checkedAnchor := "Scheme.etaleTopology",
    roleForShimuraBoundary := "site substrate for sheaf and descent formulations",
    completionBoundary := "topology infrastructure only; no Shimura descent proof"
  },
  {
    area := "sheaf",
    moduleName := "Mathlib.AlgebraicGeometry.Modules.Sheaf",
    checkedAnchor := "X.Modules",
    roleForShimuraBoundary := "module-sheaf substrate for later sheaf-theoretic packages",
    completionBoundary := "sheaf category infrastructure only; no automorphic or Hodge sheaf construction"
  },
  {
    area := "group-scheme",
    moduleName := "Mathlib.AlgebraicGeometry.Group.Abelian",
    checkedAnchor := "isCommMonObj_of_isProper_of_geometricallyIntegral",
    roleForShimuraBoundary := "adjacent abelian group-scheme substrate for abelian-scheme moduli work",
    completionBoundary := "group-scheme theorem only; no polarized abelian-scheme moduli construction"
  }
]

/-- Extract just the module names from the checked THM-M-0130-P02 anchor table. -/
def mathlibAnchorTableModules : List String :=
  mathlibAnchorTable.map MathlibAnchorRow.moduleName

/-- mathlib anchor: affine open covers of schemes are available. -/
def affineOpenCoverAnchor (X : Scheme.{u}) : X.OpenCover :=
  X.affineCover

/-- mathlib anchor: sheaves of modules on a scheme are available. -/
def moduleSheafCategoryAnchor (X : Scheme.{u}) : Type (u + 1) :=
  X.Modules

/-- mathlib anchor: the big etale topology on schemes is available. -/
def etaleTopologyAnchor : GrothendieckTopology Scheme.{u} :=
  Scheme.etaleTopology

/--
Import-level target for later local-property packages.  This checks that the
scheme morphism-property predicates needed by the Stage1 split are in scope.
-/
def ImportedLocalPropertyPredicatesAvailable : Prop :=
  ∀ {X Y : Scheme.{u}} (f : X ⟶ Y),
    Smooth f → IsProper f → Flat f → Etale f →
      LocallyOfFinitePresentation f → QuasiCompact f → True

/-- The imported local-property predicates can be used together in this module. -/
theorem importedLocalPropertyPredicatesAvailable :
    ImportedLocalPropertyPredicatesAvailable := by
  intro _X _Y _f _hsmooth _hproper _hflat _hetale _hfp _hqc
  trivial

/--
mathlib adjacent group-scheme anchor.  This is useful substrate for abelian
scheme work, but it is not a Shimura-variety construction theorem.
-/
theorem proper_geometricallyIntegral_group_commutative
    (K : Type u) [Field K] (G : Over (Spec (.of K)))
    [IsProper G.hom] [GeometricallyIntegral G.hom] [GrpObj G] :
    IsCommMonObj G :=
  isCommMonObj_of_isProper_of_geometricallyIntegral G

/-! ## Repo-local integration-debt gate -/

/-- Audit shape for a possible external Lean 4 theorem anchor. -/
structure ExternalLeanAnchorAudit where
  exactTheoremFound : Prop
  importedIntoLakeClosure : Prop
  concreteIntegrationBlockerRecorded : Prop

/--
If an exact external Lean 4 proof is found, it must either enter this Lake
closure or be blocked by a concrete integration reason.  Anchor-only evidence is
not a completed state for this slot.
-/
def RepoLocalIntegrationDebtGate (A : ExternalLeanAnchorAudit) : Prop :=
  A.exactTheoremFound →
    A.importedIntoLakeClosure ∨ A.concreteIntegrationBlockerRecorded

/-- If no exact external anchor is found, the integration-debt gate is vacuous. -/
theorem repoLocalIntegrationDebtGate_of_no_external_anchor
    (A : ExternalLeanAnchorAudit) (h : ¬ A.exactTheoremFound) :
    RepoLocalIntegrationDebtGate A := by
  intro hfound
  exact False.elim (h hfound)

/-! ## THM-M-0130-P03 datum-definition decision -/

/--
Decision route for defining the Shimura-datum/Hodge-type input layer.

This records the P03 choice only.  The local skeleton route is a checked
statement-boundary device; it is not a mathematical construction of Shimura
data, Hodge embeddings, or Shimura varieties.
-/
inductive DatumDefinitionRoute where
  | localStatementSkeleton
  | pinnedExternalLeanProject
  | blockedExternalAnchor
deriving DecidableEq, Repr

/-- Stable text label for the P03 datum-definition route. -/
def DatumDefinitionRoute.label : DatumDefinitionRoute → String
  | .localStatementSkeleton => "local_statement_skeleton"
  | .pinnedExternalLeanProject => "pinned_external_lean_project"
  | .blockedExternalAnchor => "blocked_external_anchor"

/-- One primary-source or local-closure check used by the P03 decision. -/
structure ExternalAnchorSearchRow where
  query : String
  source : String
  result : String
  completionImpact : String

/--
External-anchor audit rows for THM-M-0130-P03.

The rows intentionally record negative evidence as audit data, not as proof of
nonexistence.  The completion rule remains: an exact future Lean 4 proof must be
pinned/imported/checked or blocked by a concrete integration reason.
-/
def p03ExternalAnchorSearchRows : List ExternalAnchorSearchRow := [
  {
    query := "rg Shimura/HodgeTypeShimura/ShimuraDatum in local Lake packages",
    source := "Formalizations/Lean/.lake/packages/mathlib and flt-regular",
    result := "no bundled Shimura-datum, Hodge-type embedding, or Shimura-variety construction theorem in the local dependency closure",
    completionImpact := "do not pin an existing local dependency as P03 closure"
  },
  {
    query := "GitHub repository search: Shimura Lean language:Lean",
    source := "https://api.github.com/search/repositories",
    result := "total_count 0 on 2026-05-01",
    completionImpact := "no candidate upstream Lean repository found for pinning"
  },
  {
    query := "GitHub repository search: \"Shimura variety\" Lean",
    source := "https://api.github.com/search/repositories",
    result := "total_count 0 on 2026-05-01",
    completionImpact := "no candidate upstream Lean repository found for pinning"
  },
  {
    query := "GitHub repository search: HodgeTypeShimura Lean",
    source := "https://api.github.com/search/repositories",
    result := "total_count 0 on 2026-05-01",
    completionImpact := "no candidate upstream Lean repository found for pinning"
  }
]

/--
P03 decision: keep the local statement skeleton for now rather than pinning an
external Lean project.
-/
def p03DatumDefinitionDecision : DatumDefinitionRoute :=
  .localStatementSkeleton

/-- Text summary of the P03 decision for ledger/public backfill. -/
def p03DatumDefinitionDecisionSummary : List String := [
  "decision date: 2026-05-01",
  "route: local_statement_skeleton",
  "reason: no exact upstream Lean 4 project defining Shimura datum/Hodge-type embedding and proving the Hodge-type Shimura-variety construction was found in the checked local closure or GitHub repository searches",
  "repo-local artifact: HodgeTypeShimuraDatum remains a checked local statement-boundary structure with explicit Prop obligations",
  "completion boundary: the local skeleton is formalization_debt / not_repo_local_closed and must not be treated as theorem completion"
]

/-- P03 audit object: no exact external Lean theorem anchor was found in this pass. -/
def p03ExternalAnchorAudit : ExternalLeanAnchorAudit where
  exactTheoremFound := False
  importedIntoLakeClosure := False
  concreteIntegrationBlockerRecorded := False

/--
The P03 repo-local integration-debt gate is satisfied only in the narrow sense
that this pass found no exact external proof anchor to integrate.  It does not
complete the theorem.
-/
theorem p03RepoLocalIntegrationDebtGate :
    RepoLocalIntegrationDebtGate p03ExternalAnchorAudit := by
  exact repoLocalIntegrationDebtGate_of_no_external_anchor
    p03ExternalAnchorAudit (by
      intro hfound
      exact hfound)

/-- Checked route label for the P03 decision. -/
theorem p03DatumDefinitionDecision_is_localSkeleton :
    p03DatumDefinitionDecision = .localStatementSkeleton :=
  rfl

/-! ## THM-M-0130-P08 repo-local closure target

P08 chooses a concrete repo-local closure target without pretending that the
target is already closed.  Since P03 found no exact external Lean 4 proof to
pin and the imported mathlib substrate has no terminal Shimura-variety theorem,
the current target is a future local proof body of `StatementShape`.
-/

/-- The three M0387-allowed closure routes for this Stage1 slot. -/
inductive RepoLocalClosureKind where
  | localProofBody
  | mathlibWrapper
  | pinnedExternalDependency
deriving DecidableEq, Repr

/-- Stable text label for a P08 repo-local closure route. -/
def RepoLocalClosureKind.label : RepoLocalClosureKind → String
  | .localProofBody => "local_proof_body"
  | .mathlibWrapper => "local_wrapper_upstream_mathlib"
  | .pinnedExternalDependency => "external_upstream_pinned"

/-- Metadata for the selected P08 repo-local closure target. -/
structure RepoLocalClosureTarget where
  closureKind : RepoLocalClosureKind
  targetDeclaration : String
  statementDeclaration : String
  validationCommand : String
  currentBlockingReason : String

/--
The concrete local proof-body target for P08.

A completed future proof of this proposition is exactly a completed proof of
the normalized `StatementShape`; this declaration is a target, not a proof.
-/
def p08LocalProofClosureTarget : Prop :=
  StatementShape.{u, v, w}

/-- The P08 local proof-body target is definitionally the normalized statement. -/
theorem p08LocalProofClosureTarget_iff_statementShape :
    p08LocalProofClosureTarget.{u, v, w} ↔ StatementShape.{u, v, w} :=
  Iff.rfl

/--
Selected P08 closure target.

The route is `local_proof_body` because no terminal mathlib theorem or exact
pinned external Lean dependency is currently available in this Lake closure.
-/
def p08RepoLocalClosureTarget : RepoLocalClosureTarget where
  closureKind := .localProofBody
  targetDeclaration :=
    "AwesomeTheorems.Stage1.S1_M_026.p08LocalProofClosureTarget"
  statementDeclaration :=
    "AwesomeTheorems.Stage1.S1_M_026.StatementShape"
  validationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_026.lean"
  currentBlockingReason :=
    "future proof must construct a HodgeTypeShimuraModel with GeometricModelPackage and ModuliConstructionPackage for every audited HodgeTypeShimuraDatum; no terminal mathlib wrapper or pinned external dependency is present"

/-- Current P08 completion flag.  This is deliberately false in this artifact. -/
def p08RepoLocalClosureCompleted : Bool :=
  false

/-- Checked P08 status: the closure target exists, but theorem completion is not claimed. -/
theorem p08RepoLocalClosureCompleted_eq_false :
    p08RepoLocalClosureCompleted = false :=
  rfl

/--
P08 reuses the P03 external-anchor audit for the repo-local integration-debt
gate: no exact external Lean proof was found in this pass, so no anchor-only
evidence is being counted as completed.
-/
theorem p08RepoLocalIntegrationDebtGate :
    RepoLocalIntegrationDebtGate p03ExternalAnchorAudit :=
  p03RepoLocalIntegrationDebtGate

/-- Ledger-facing summary of the P08 repo-local closure target. -/
def p08RepoLocalClosureTargetSummary : List String := [
  "selected closure target: local_proof_body",
  "target declaration: p08LocalProofClosureTarget, definitionally equal to StatementShape",
  "mathlib wrapper route: not selected because the imported substrate has no terminal Hodge-type Shimura-variety theorem",
  "pinned external dependency route: not selected because P03 found no exact external Lean 4 project/proof to pin",
  "current status: formalization_debt / not_repo_local_closed; p08RepoLocalClosureCompleted is false",
  "repo_local_integration_debt gate: no exact external anchor is being left as anchor-only completed evidence"
]

/-! ## THM-M-0130-P09 build-validation instructions

P09 is now allowed to record a build-validation command because the repo-local
Lean artifact has an actual target declaration: `p08LocalProofClosureTarget`,
definitionally equal to `StatementShape`.  The command below validates the
statement-boundary module and wrappers only; it is not a proof-completion gate
for Hodge-type Shimura varieties.
-/

/-- Checked build-validation instruction row for the P09 backfill. -/
structure BuildValidationInstruction where
  targetDeclaration : String
  targetKind : String
  workingDirectory : String
  command : String
  validationScope : String
  completionBoundary : String

/-- P09 build-validation instruction for the existing repo-local Lean target. -/
def p09BuildValidationInstruction : BuildValidationInstruction where
  targetDeclaration := p08RepoLocalClosureTarget.targetDeclaration
  targetKind := RepoLocalClosureKind.label p08RepoLocalClosureTarget.closureKind
  workingDirectory := "Formalizations/Lean"
  command := p08RepoLocalClosureTarget.validationCommand
  validationScope :=
    "checks AwesomeTheorems/Stage1/S1_M_026.lean, including StatementShape, p08LocalProofClosureTarget, substrate wrappers, and audit constants"
  completionBoundary :=
    "passing this command validates the Stage1 statement-boundary artifact only; it does not prove THM-M-0130 and does not close p08RepoLocalClosureCompleted"

/-- The P09 instruction validates the concrete P08 target declaration. -/
theorem p09BuildValidation_targets_p08ClosureTarget :
    p09BuildValidationInstruction.targetDeclaration =
      p08RepoLocalClosureTarget.targetDeclaration :=
  rfl

/-- The P09 instruction reuses the P08 repo-local validation command. -/
theorem p09BuildValidation_uses_p08ValidationCommand :
    p09BuildValidationInstruction.command =
      p08RepoLocalClosureTarget.validationCommand :=
  rfl

/-- P09 validation does not change the current theorem-completion flag. -/
theorem p09BuildValidation_doesNotCompleteTheorem :
    p08RepoLocalClosureCompleted = false :=
  p08RepoLocalClosureCompleted_eq_false

/-- Ledger-facing checklist for P09 build-validation backfill. -/
def p09BuildValidationChecklist : List String := [
  "actual Lean target exists: AwesomeTheorems.Stage1.S1_M_026.p08LocalProofClosureTarget, definitionally equal to StatementShape",
  "recommended command: cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_026.lean",
  "rerun after every edit to the Stage1 S1_M_026 Lean artifact or any future dependency/wrapper change",
  "record absolute date, command, target declaration, result, and any failure summary before changing public status surfaces",
  "treat a pass as statement-boundary validation only until a local proof body, mathlib wrapper, or pinned external dependency supplies the construction proof",
  "do not mark completed while p08RepoLocalClosureCompleted remains false or while any exact external Lean proof is anchor-only"
]

/-! ## THM-M-0130-P10 public-status backfill gate

P10 is a public-doc integration gate, not a construction proof.  It records the
rule that public status surfaces may be backfilled only after the machine
anchor/closure target and the `<=100` leaf-ledger surface are both closed.
The current Stage1 artifact keeps the gate closed.
-/

/-- Public-status backfill is allowed exactly when both required gates are closed. -/
def publicStatusBackfillAllowed (machineAnchorClosed leafLedgersClosed : Bool) : Bool :=
  machineAnchorClosed && leafLedgersClosed

/-- Boolean characterization of the P10 public-status backfill gate. -/
theorem publicStatusBackfillAllowed_iff
    (machineAnchorClosed leafLedgersClosed : Bool) :
    publicStatusBackfillAllowed machineAnchorClosed leafLedgersClosed = true ↔
      machineAnchorClosed = true ∧ leafLedgersClosed = true := by
  cases machineAnchorClosed <;> cases leafLedgersClosed <;>
    simp [publicStatusBackfillAllowed]

/-- Checked public-status backfill instruction for later serial integrators. -/
structure PublicStatusBackfillInstruction where
  authoritativeSurfaces : List String
  prerequisites : List String
  prohibitedPrematureClaims : List String
  currentAction : String
  currentGateOpen : Bool

/-- Current machine-anchor gate for P10: the P08 closure target is not proved. -/
def p10MachineAnchorClosed : Bool :=
  p08RepoLocalClosureCompleted

/-- Current leaf-ledger gate for P10: theorem-completion leaf ledgers remain open. -/
def p10LeafLedgersClosed : Bool :=
  false

/-- Current P10 public-status backfill gate. -/
def p10PublicStatusBackfillAllowed : Bool :=
  publicStatusBackfillAllowed p10MachineAnchorClosed p10LeafLedgersClosed

/-- The current Stage1 artifact explicitly keeps public completion backfill disabled. -/
theorem p10PublicStatusBackfillAllowed_eq_false :
    p10PublicStatusBackfillAllowed = false := by
  simp [p10PublicStatusBackfillAllowed, publicStatusBackfillAllowed,
    p10MachineAnchorClosed, p10LeafLedgersClosed, p08RepoLocalClosureCompleted]

/-- P10 cannot be opened in the current artifact. -/
theorem p10PublicStatusBackfillBlocked :
    p10PublicStatusBackfillAllowed = true → False := by
  intro h
  rw [p10PublicStatusBackfillAllowed_eq_false] at h
  contradiction

/-- Ledger-facing P10 instruction for serial public-doc merge-back. -/
def p10PublicStatusBackfillInstruction : PublicStatusBackfillInstruction where
  authoritativeSurfaces := [
    "Docs/Stage1_Blueprint.md Backfill S1-M-026 / THM-M-0130 section",
    "Docs/todos_20260430.md if it has a matching public status row",
    "README.md only if it has a matching authoritative status summary"
  ]
  prerequisites := [
    "repo-local machine anchor closed by local_proof_body, local_wrapper_upstream_mathlib, or external_upstream_pinned",
    "validation command passes for the exact repo-local Lean target",
    "all public theorem-tree leaves have independent <=100 local ledgers",
    "public merge-back text is synchronized across authoritative surfaces",
    "no exact external Lean proof remains external_upstream_anchor_only"
  ]
  prohibitedPrematureClaims := [
    "do not mark THM-M-0130 completed while p08RepoLocalClosureCompleted is false",
    "do not treat this Stage1 statement-boundary file as a Hodge-type Shimura-variety construction proof",
    "do not use private runtime ledgers alone as the public completion surface",
    "do not leave repo_local_integration_debt in any completed state"
  ]
  currentAction :=
    "keep public status open; merge only the checked P01-P09 backfill notes and this P10 gate, without a completion claim"
  currentGateOpen := p10PublicStatusBackfillAllowed

/-- P10 instruction agrees with the checked closed gate. -/
theorem p10PublicStatusBackfillInstruction_gate :
    p10PublicStatusBackfillInstruction.currentGateOpen = false :=
  p10PublicStatusBackfillAllowed_eq_false

/-! ## Audit constants retained for Stage1 repair bookkeeping -/

/-- mathlib modules checked as useful substrate for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.AlgebraicGeometry.Scheme",
  "Mathlib.AlgebraicGeometry.Cover.Open",
  "Mathlib.AlgebraicGeometry.Modules.Sheaf",
  "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
  "Mathlib.AlgebraicGeometry.Morphisms.Proper",
  "Mathlib.AlgebraicGeometry.Morphisms.Flat",
  "Mathlib.AlgebraicGeometry.Morphisms.FinitePresentation",
  "Mathlib.AlgebraicGeometry.Morphisms.Etale",
  "Mathlib.AlgebraicGeometry.Sites.Etale",
  "Mathlib.AlgebraicGeometry.Group.Abelian"
]

/-- Search terms retained for the later authenticated external audit. -/
def externalAnchorSearchTerms : List String := [
  "ShimuraVariety",
  "Shimura variety Lean 4",
  "Hodge type Shimura Lean",
  "HodgeTypeShimura",
  "Siegel Shimura datum Lean",
  "abelian scheme moduli Lean",
  "polarized abelian variety moduli Lean",
  "canonical model Shimura variety Lean"
]

/--
Statement-boundary components that are fixed by this Stage1 artifact before a
future construction proof can be attempted.
-/
def statementBoundaryComponents : List String := [
  "input datum: HodgeTypeShimuraDatum with reflex field, Shimura-datum carrier, and level carrier",
  "audited hypotheses: Shimura datum, Hodge-type embedding, admissible level, reflex-field compatibility, Hodge tensors",
  "base: Scheme.Spec over the reflex field of the datum",
  "output: HodgeTypeShimuraModel with a scheme and structure morphism to the reflex-field base",
  "geometric package: proper, smooth, and flat structure morphism predicates",
  "moduli package: abelian-scheme moduli, Hodge tensors, level compatibility, canonical model, integral model",
  "P04 split package: abelian schemes, polarizations, tensors, level structure, functor definition, and representability",
  "P05 local-property plan: proper, smooth, flat, etale, and finite-presentation branches, with finite presentation represented as LocallyOfFinitePresentation plus QuasiCompact",
  "P06 descent/gluing branch: directed open-cover gluing plus fpqc morphism-property descent wrappers around mathlib Cover and DescendsAlong APIs",
  "P07 optional cohomological-realization branch: ell-adic/pro-etale/cohomological data are not required by the current StatementShape unless a future normalized statement explicitly switches to StatementShapeWithRequiredCohomologicalRealization",
  "P08 repo-local closure target: p08LocalProofClosureTarget is definitionally StatementShape; completion requires a future local proof body or replacement by a checked mathlib wrapper/pinned external dependency",
  "P09 build-validation instruction: run cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_026.lean for the existing p08LocalProofClosureTarget; a pass validates this statement-boundary artifact only",
  "P10 public-status backfill gate: p10PublicStatusBackfillAllowed is false until machine anchor closure and <=100 leaf-ledger closure are both checked",
  "completion gate: exact construction proof or pinned/imported external Lean proof, plus local validation"
]

/--
Concrete blockers that prevent this checked statement-boundary file from being
claimed as a construction theorem for Hodge-type Shimura varieties.
-/
def formalizationBlockers : List String := [
  "no bundled mathlib definition of Shimura datum or Hodge-type Shimura datum was identified in the imported substrate",
  "no bundled mathlib construction of the Siegel embedding target for Hodge-type data is present here",
  "abelian-scheme moduli with polarizations, tensors, and level structures is represented only by explicit Prop fields",
  "representability of the relevant moduli functor by a scheme over the reflex field is not proved in this module",
  "canonical-model and integral-model properties are named obligations, not imported theorem bodies",
  "local-property branches are checked as a proof plan only; no construction supplies the proper, smooth, flat, etale, or finite-presentation proofs for a Shimura model",
  "descent and gluing branches are checked only as API-aligned proof plans; no Shimura-specific effective descent data are constructed",
  "P07 marks ell-adic/pro-etale/cohomological realization data as optional for the current StatementShape; they become required only under the stronger StatementShapeWithRequiredCohomologicalRealization variant",
  "P08 has selected p08LocalProofClosureTarget as the repo-local closure target, but the proof body of StatementShape is not present",
  "P09 build validation checks the local Stage1 artifact and wrappers only; it is not evidence of a terminal construction proof",
  "P10 public status backfill is blocked because p08RepoLocalClosureCompleted is false and theorem-completion <=100 leaf ledgers are not closed",
  "no exact external Lean 4 proof has been pinned, imported, and checked in this Lake closure"
]

/-- External-anchor audit summary for this child pass. -/
def externalAnchorAuditSummary : List String := [
  "audit date: 2026-05-01",
  "web search terms matched mathematical references and expository/research pages, not an exact Lean 4 theorem body",
  "local repository search did not identify a pinned external Shimura-variety Lean proof imported by this module",
  "status remains formalization_debt / not_repo_local_closed rather than repo_local completed"
]

/-- Current machine-proof debt classification for this repaired Stage1 module. -/
def machineProofDebtClassification : List String := [
  "formalization_debt: the human mathematical construction is known but no Lean 4 proof closure is present here",
  "not_repo_local_closed: this module is a checked statement shape plus substrate wrappers",
  "P08 target selected: future local_proof_body for p08LocalProofClosureTarget, definitionally equal to StatementShape",
  "P09 validation command selected for the existing target: cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_026.lean",
  "P10 public-status backfill gate remains closed: p10PublicStatusBackfillAllowed = false",
  "repo_local_integration_debt is not asserted as completed because no exact external Lean 4 proof has been pinned/imported/checked"
]

/-- M0387-level theorem-internal child leaves for the next integrator pass. -/
def theoremInternalChildLeaves : List String := [
  "S1-M-026-leaf-001 statement normalization: exact datum, reflex field, level, model type",
  "S1-M-026-leaf-002 mathlib object model: Scheme, Spec, morphisms, sites, sheaves",
  "S1-M-026-leaf-003 Hodge-type datum and embedding into Siegel datum",
  "S1-M-026-leaf-004 abelian-scheme family branch for the moduli problem",
  "S1-M-026-leaf-005 polarization branch for the moduli problem",
  "S1-M-026-leaf-006 tensor/Hodge-cycle branch for the moduli problem",
  "S1-M-026-leaf-007 level-structure branch for the moduli problem",
  "S1-M-026-leaf-008 moduli-functor definition branch",
  "S1-M-026-leaf-009 representability by a scheme over the reflex field",
  "S1-M-026-leaf-010 local-property proper branch",
  "S1-M-026-leaf-011 local-property smooth branch",
  "S1-M-026-leaf-012 local-property flat branch",
  "S1-M-026-leaf-013 local-property etale branch",
  "S1-M-026-leaf-014 local-property finite-presentation branch",
  "S1-M-026-leaf-015 descent and gluing through covers and morphism-property APIs: checked statement-boundary wrappers present; Shimura-specific effective descent remains open",
  "S1-M-026-leaf-016 optional ell-adic/pro-etale/cohomological realization layer: checked P07 status marks this branch optional for the current StatementShape unless a future normalized statement explicitly requires StatementShapeWithRequiredCohomologicalRealization",
  "S1-M-026-leaf-017 repo-local closure target: checked P08 target p08LocalProofClosureTarget exists; proof body remains formalization_debt / not_repo_local_closed",
  "S1-M-026-leaf-018 build-validation instruction: checked P09 validation record exists for p08LocalProofClosureTarget; command validation is statement-boundary validation only",
  "S1-M-026-leaf-019 public-status backfill gate: checked P10 gate exists and remains closed until repo-local machine anchor and <=100 leaf-ledger closure both pass"
]

#check HodgeTypeShimuraDatum
#check HodgeTypeShimuraDatum.baseScheme
#check HodgeTypeShimuraModel
#check GeometricModelPackage
#check ModuliConstructionPackage
#check AbelianSchemeModuliBranch
#check PolarizationModuliBranch
#check TensorModuliBranch
#check LevelStructureModuliBranch
#check ModuliFunctorDefinitionBranch
#check RepresentabilityModuliBranch
#check SplitModuliBranch
#check SplitModuliBranch.toModuliConstructionPackage
#check splitModuliBranch_abelianSchemes
#check splitModuliBranch_polarizations
#check splitModuliBranch_tensors
#check splitModuliBranch_levelStructure
#check splitModuliBranch_functorDefinition
#check splitModuliBranch_representability
#check ProperLocalPropertyBranch
#check SmoothLocalPropertyBranch
#check FlatLocalPropertyBranch
#check EtaleLocalPropertyBranch
#check FinitePresentationLocalPropertyBranch
#check LocalPropertyProofPlan
#check StructureMapLocalPropertyProofPlan
#check AuxiliaryEtaleLocalPropertyBranch
#check SmoothLocalPropertyBranch.toFlat
#check SmoothLocalPropertyBranch.toLocallyOfFinitePresentation
#check EtaleLocalPropertyBranch.toSmooth
#check EtaleLocalPropertyBranch.toFlat
#check EtaleLocalPropertyBranch.toLocallyOfFinitePresentation
#check ProperLocalPropertyBranch.toLocallyOfFiniteType
#check FinitePresentationLocalPropertyBranch.asPair
#check FinitePresentationLocalPropertyBranch.toLocallyOfFiniteType
#check FinitePresentationLocalPropertyBranch.of_smooth_of_quasiCompact
#check FinitePresentationLocalPropertyBranch.of_etale_of_quasiCompact
#check LocalPropertyProofPlan.toGeometricModelPackage
#check StructureMapLocalPropertyProofPlan.toGeometricModelPackage
#check HodgeTypeLocalPropertyProofPlan
#check fpqcDescentProperty
#check DirectedOpenCoverGluingBranch
#check DirectedOpenCoverGluingBranch.gluedMorphism
#check DirectedOpenCoverGluingBranch.restricts
#check DirectedOpenCoverOverGluingBranch
#check DirectedOpenCoverOverGluingBranch.gluedOverMorphism
#check DirectedOpenCoverOverGluingBranch.restricts_left
#check CoverDescentBranch
#check CoverDescentBranch.descendedProperty
#check FpqcDescentBranch
#check FpqcDescentBranch.coverProperty
#check FpqcDescentBranch.descendedProperty
#check openImmersion_descendsAlong_fpqc
#check FpqcOpenImmersionDescentBranch
#check FpqcOpenImmersionDescentBranch.coverProperty
#check FpqcOpenImmersionDescentBranch.descendedOpenImmersion
#check HodgeTypeDescentGluingBranch
#check HodgeTypeDescentGluingBranch.gluedChartMorphism
#check HodgeTypeDescentGluingBranch.fpqcModelMap_openImmersion
#check CohomologicalRealizationBranchStatus
#check CohomologicalRealizationBranchStatus.label
#check CohomologicalRealizationBranch
#check OptionalCohomologicalRealizationPackage
#check p07CohomologicalRealizationBranchStatus
#check p07CohomologicalRealizationBranchStatus_is_optional
#check p07_currentStatement_doesNotRequireCohomologicalRealization
#check optionalCohomologicalRealizationPackage
#check StatementShapeWithRequiredCohomologicalRealization
#check normalizedLeanNamespace
#check normalizedUniversePolicy
#check normalizedVariablePolicy
#check StatementShape
#check modelPackage_of_statementShape
#check modelPackageWithOptionalCohomologicalRealization_of_statementShape
#check statementShape_of_statementShapeWithRequiredCohomologicalRealization
#check pinnedMathlibRevision
#check MathlibAnchorRow
#check mathlibAnchorTable
#check mathlibAnchorTableModules
#check affineOpenCoverAnchor
#check moduleSheafCategoryAnchor
#check etaleTopologyAnchor
#check importedLocalPropertyPredicatesAvailable
#check proper_geometricallyIntegral_group_commutative
#check RepoLocalIntegrationDebtGate
#check repoLocalIntegrationDebtGate_of_no_external_anchor
#check DatumDefinitionRoute
#check DatumDefinitionRoute.label
#check ExternalAnchorSearchRow
#check p03ExternalAnchorSearchRows
#check p03DatumDefinitionDecision
#check p03DatumDefinitionDecisionSummary
#check p03ExternalAnchorAudit
#check p03RepoLocalIntegrationDebtGate
#check p03DatumDefinitionDecision_is_localSkeleton
#check RepoLocalClosureKind
#check RepoLocalClosureKind.label
#check RepoLocalClosureTarget
#check p08LocalProofClosureTarget
#check p08LocalProofClosureTarget_iff_statementShape
#check p08RepoLocalClosureTarget
#check p08RepoLocalClosureCompleted
#check p08RepoLocalClosureCompleted_eq_false
#check p08RepoLocalIntegrationDebtGate
#check p08RepoLocalClosureTargetSummary
#check BuildValidationInstruction
#check p09BuildValidationInstruction
#check p09BuildValidation_targets_p08ClosureTarget
#check p09BuildValidation_uses_p08ValidationCommand
#check p09BuildValidation_doesNotCompleteTheorem
#check p09BuildValidationChecklist
#check publicStatusBackfillAllowed
#check publicStatusBackfillAllowed_iff
#check PublicStatusBackfillInstruction
#check p10MachineAnchorClosed
#check p10LeafLedgersClosed
#check p10PublicStatusBackfillAllowed
#check p10PublicStatusBackfillAllowed_eq_false
#check p10PublicStatusBackfillBlocked
#check p10PublicStatusBackfillInstruction
#check p10PublicStatusBackfillInstruction_gate
#check statementBoundaryComponents
#check formalizationBlockers
#check externalAnchorAuditSummary
#check machineProofDebtClassification
#check theoremInternalChildLeaves

end S1_M_026
end Stage1
end AwesomeTheorems
