import Mathlib.CategoryTheory.RepresentedBy
import Mathlib.CategoryTheory.Preadditive.Yoneda.Limits
import Mathlib.CategoryTheory.Preadditive.Yoneda.Projective
import Mathlib.CategoryTheory.Preadditive.Yoneda.Injective
import Mathlib.Algebra.Homology.HomologySequence
import Mathlib.Algebra.Homology.SpectralSequence.Basic
import Mathlib.CategoryTheory.Triangulated.Yoneda

/-!
# S1-M-138 / THM-M-0081: Yoneda lemma

This Stage1 file records the category-level Lean 4/mathlib closure point for
the statement that an object is determined, up to isomorphism, by its
representable presheaf.

The proof body is supplied by the pinned mathlib Yoneda API:
`CategoryTheory.Yoneda.fullyFaithful`,
`CategoryTheory.Functor.FullyFaithful.preimageIso`, and
`CategoryTheory.Functor.RepresentableBy.uniqueUpToIso`.  The declarations below
are repo-local wrappers and statement-shape checks; they do not introduce proof
placeholders.
-/

noncomputable section

open CategoryTheory Opposite CategoryTheory.Limits CategoryTheory.Pretriangulated.Opposite

universe w v u

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_138

/--
Stage1 statement shape for the Yoneda lemma in the object-detection form.

For any category `C`, if the representable presheaves `yoneda.obj X` and
`yoneda.obj Y` are naturally isomorphic, then the objects `X` and `Y` are
isomorphic.
-/
def StatementShape (C : Type u) [Category.{v} C] : Prop :=
  ∀ X Y : C, Nonempty (yoneda.obj X ≅ yoneda.obj Y) → Nonempty (X ≅ Y)

/--
Checked repo-local wrapper: an isomorphism of representable presheaves reflects
to an isomorphism of the representing objects.
-/
def objectIsoOfRepresentableIso {C : Type u} [Category.{v} C]
    {X Y : C} (e : yoneda.obj X ≅ yoneda.obj Y) : X ≅ Y :=
  Yoneda.fullyFaithful.preimageIso e

/-- The forward direction: an object isomorphism induces an isomorphism of representables. -/
def representableIsoOfObjectIso {C : Type u} [Category.{v} C]
    {X Y : C} (e : X ≅ Y) : yoneda.obj X ≅ yoneda.obj Y :=
  yoneda.mapIso e

/--
The normalized object-detection form of the Yoneda lemma.

This is the precise local statement for "objects are uniquely determined by
their representable functors", with uniqueness understood up to isomorphism.
-/
theorem yoneda_obj_iso_iff_object_iso {C : Type u} [Category.{v} C]
    (X Y : C) : Nonempty (yoneda.obj X ≅ yoneda.obj Y) ↔ Nonempty (X ≅ Y) := by
  constructor
  · rintro ⟨e⟩
    exact ⟨objectIsoOfRepresentableIso e⟩
  · rintro ⟨e⟩
    exact ⟨representableIsoOfObjectIso e⟩

/-- The Stage1 statement shape is closed by the pinned mathlib Yoneda API. -/
theorem statementShape (C : Type u) [Category.{v} C] :
    StatementShape C := by
  intro X Y h
  exact (yoneda_obj_iso_iff_object_iso X Y).mp h

/--
Canonical Stage1 machine-status wrapper for the public blueprint.

The proof body is upstream mathlib's Yoneda fully-faithful API, checked here
through `statementShape`.
-/
theorem local_wrapper_upstream_mathlib (C : Type u) [Category.{v} C] :
    StatementShape C :=
  statementShape C

/--
Representing objects for the same presheaf are unique up to isomorphism.

This exposes mathlib's bundled representability uniqueness theorem as the
second standard Yoneda-lemma formulation.
-/
def representingObjectUnique {C : Type u} [Category.{v} C]
    {F : Cᵒᵖ ⥤ Type v} {X Y : C}
    (hX : F.RepresentableBy X) (hY : F.RepresentableBy Y) : X ≅ Y :=
  hX.uniqueUpToIso hY

/--
Universal-element variant from `Mathlib.CategoryTheory.RepresentedBy`.

If the same presheaf is represented by explicit universal elements on `X` and
`Y`, then the representing objects are isomorphic.  The proof converts each
`IsRepresentedBy` witness to mathlib's bundled `RepresentableBy` form and then
uses `RepresentableBy.uniqueUpToIso`.
-/
def representingObjectUniqueOfIsRepresentedBy {C : Type u} [Category.{v} C]
    {F : Cᵒᵖ ⥤ Type w} {X Y : C}
    {x : F.obj (op X)} {y : F.obj (op Y)}
    (hX : F.IsRepresentedBy x) (hY : F.IsRepresentedBy y) : X ≅ Y :=
  hX.representableBy.uniqueUpToIso hY.representableBy

/-- Element-level Yoneda equivalence exposed by mathlib. -/
def yonedaElementEquiv {C : Type u} [Category.{v} C]
    {X : C} {F : Cᵒᵖ ⥤ Type v} :
    (yoneda.obj X ⟶ F) ≃ F.obj (op X) :=
  yonedaEquiv

/-- Natural-isomorphism form of the Yoneda lemma exposed by mathlib. -/
def yonedaLemmaIso (C : Type u) [Category.{v} C] :
    yonedaPairing C ≅ yonedaEvaluation C :=
  yonedaLemma C

/-- Naturality square for a natural transformation between representable presheaves. -/
theorem yoneda_naturality_square {C : Type u} [Category.{v} C]
    {X Y Z Z' : C} (α : yoneda.obj X ⟶ yoneda.obj Y) (f : Z ⟶ Z')
    (h : Z' ⟶ X) :
    f ≫ α.app (op Z') h = α.app (op Z) (f ≫ h) :=
  Yoneda.naturality α f h

/--
Checked collateral wrapper: the preadditive Yoneda embedding is faithful.

This is not a homological-algebra terminal statement; it records a nearby
mathlib anchor for later exactness and long-exact-sequence backfill.
-/
theorem preadditive_yoneda_faithful (C : Type u) [Category.{v} C] [Preadditive C] :
    (preadditiveYoneda (C := C)).Faithful := by
  infer_instance

/--
Checked collateral wrapper: each preadditive representable presheaf preserves
limits in the pinned mathlib API.
-/
theorem preadditive_yoneda_preservesLimits_obj
    (C : Type u) [Category.{v} C] [Preadditive C] (X : C) :
    PreservesLimits (preadditiveYoneda.obj X) := by
  infer_instance

/--
Checked collateral wrapper: each preadditive corepresentable copresheaf
preserves limits in the pinned mathlib API.
-/
theorem preadditive_coyoneda_preservesLimits_obj
    (C : Type u) [Category.{v} C] [Preadditive C] (X : Cᵒᵖ) :
    PreservesLimits (preadditiveCoyoneda.obj X) := by
  infer_instance

/--
Audit anchor from `Mathlib.CategoryTheory.Preadditive.Yoneda.Projective`.

This is a projectivity/coyoneda collateral theorem, not a completion of any
homological Yoneda branch.
-/
theorem preadditive_coyoneda_projective_iff_preservesEpimorphisms
    {C : Type u} [Category.{v} C] [Preadditive C] (P : C) :
    Projective P ↔ (preadditiveCoyoneda.obj (op P)).PreservesEpimorphisms :=
  Projective.projective_iff_preservesEpimorphisms_preadditiveCoyoneda_obj P

/--
Audit anchor from `Mathlib.CategoryTheory.Preadditive.Yoneda.Injective`.

This is an injectivity/yoneda collateral theorem, not a completion of any
homological Yoneda branch.
-/
theorem preadditive_yoneda_injective_iff_preservesEpimorphisms
    {C : Type u} [Category.{v} C] [Preadditive C] (J : C) :
    Injective J ↔ (preadditiveYoneda.obj J).PreservesEpimorphisms :=
  Injective.injective_iff_preservesEpimorphisms_preadditiveYoneda_obj J

/--
Checked homological-Yoneda anchor from `Mathlib.CategoryTheory.Triangulated.Yoneda`.

For a pretriangulated category, preadditive representable presheaves are
homological functors.  This is still collateral for S1-M-138: it supplies a
validated machine anchor for later child packages, but it does not close the
long-exact, derived-category, or spectral-sequence public branches.
-/
theorem preadditive_yoneda_isHomological
    {C : Type u} [Category.{v} C] [Preadditive C] [HasShift C ℤ]
    [HasZeroObject C] [∀ n : ℤ, Functor.Additive (shiftFunctor C n)]
    [Pretriangulated C] (B : C) :
    (preadditiveYoneda.obj B).IsHomological := by
  infer_instance

/--
Checked homological-Coyoneda anchor from `Mathlib.CategoryTheory.Triangulated.Yoneda`.

For a pretriangulated category, preadditive corepresentable copresheaves are
homological functors.
-/
theorem preadditive_coyoneda_isHomological
    {C : Type u} [Category.{v} C] [Preadditive C] [HasShift C ℤ]
    [HasZeroObject C] [∀ n : ℤ, Functor.Additive (shiftFunctor C n)]
    [Pretriangulated C] (A : Cᵒᵖ) :
    (preadditiveCoyoneda.obj A).IsHomological := by
  infer_instance

/--
Checked exactness anchor for distinguished triangles after applying
preadditive Yoneda.

This records the local theorem surface needed by later homological Yoneda child
tasks.  It is not, by itself, a public long-exact-sequence completion.
-/
theorem preadditive_yoneda_map_distinguished_exact
    {C : Type u} [Category.{v} C] [Preadditive C] [HasShift C ℤ]
    [HasZeroObject C] [∀ n : ℤ, Functor.Additive (shiftFunctor C n)]
    [Pretriangulated C]
    (T : Pretriangulated.Triangle C)
    (hT : T ∈ Pretriangulated.distinguishedTriangles) (B : C) :
    ((Pretriangulated.shortComplexOfDistTriangle T hT).op.map
      (preadditiveYoneda.obj B)).Exact :=
  Pretriangulated.preadditiveYoneda_map_distinguished T hT B

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.CategoryTheory.Yoneda",
  "Mathlib.CategoryTheory.Functor.FullyFaithful",
  "Mathlib.CategoryTheory.RepresentedBy",
  "Mathlib.CategoryTheory.Preadditive.Yoneda.Basic",
  "Mathlib.CategoryTheory.Preadditive.Yoneda.Limits",
  "Mathlib.CategoryTheory.Preadditive.Yoneda.Projective",
  "Mathlib.CategoryTheory.Preadditive.Yoneda.Injective",
  "Mathlib.CategoryTheory.Limits.Yoneda",
  "Mathlib.Algebra.Homology.ShortComplex.Basic",
  "Mathlib.Algebra.Homology.ShortComplex.Exact",
  "Mathlib.Algebra.Homology.ShortComplex.ShortExact",
  "Mathlib.Algebra.Homology.ShortComplex.PreservesHomology",
  "Mathlib.Algebra.Homology.HomologySequence",
  "Mathlib.Algebra.Homology.SpectralSequence.Basic",
  "Mathlib.CategoryTheory.Triangulated.Pretriangulated",
  "Mathlib.CategoryTheory.Triangulated.HomologicalFunctor",
  "Mathlib.CategoryTheory.Triangulated.Yoneda"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "CategoryTheory.yoneda",
  "CategoryTheory.yonedaEquiv",
  "CategoryTheory.yonedaLemma",
  "CategoryTheory.Yoneda.fullyFaithful",
  "CategoryTheory.Yoneda.naturality",
  "CategoryTheory.Functor.FullyFaithful.preimageIso",
  "CategoryTheory.Functor.FullyFaithful.isoEquiv",
  "CategoryTheory.Functor.RepresentableBy.uniqueUpToIso",
  "CategoryTheory.Functor.RepresentableBy.yoneda",
  "CategoryTheory.Functor.IsRepresentedBy",
  "CategoryTheory.Functor.IsRepresentedBy.representableBy",
  "CategoryTheory.Functor.IsRepresentedBy.iff_exists_representableBy",
  "CategoryTheory.preadditiveYoneda",
  "CategoryTheory.preadditiveCoyoneda",
  "CategoryTheory.preservesLimits_preadditiveYoneda_obj",
  "CategoryTheory.preservesLimits_preadditiveCoyoneda_obj",
  "CategoryTheory.Projective.projective_iff_preservesEpimorphisms_preadditiveCoyoneda_obj",
  "CategoryTheory.Injective.injective_iff_preservesEpimorphisms_preadditiveYoneda_obj",
  "CategoryTheory.Functor.IsHomological",
  "CategoryTheory.Pretriangulated.preadditiveYoneda_map_distinguished",
  "CategoryTheory.Pretriangulated.preadditiveYoneda_homologySequenceδ_apply",
  "CategoryTheory.Pretriangulated.preadditiveCoyoneda_homologySequenceδ_apply",
  "CategoryTheory.ShortComplex.Exact",
  "CategoryTheory.ShortComplex.ShortExact",
  "CategoryTheory.ShortComplex.HasHomology",
  "HomologicalComplex",
  "CategoryTheory.SpectralSequence"
]

/-- Canonical machine anchors for THM-M-0081 required by the Stage1 public backfill. -/
def canonicalMachineAnchors : List String := [
  "CategoryTheory.Yoneda.fullyFaithful",
  "CategoryTheory.Functor.FullyFaithful.preimageIso",
  "CategoryTheory.Functor.RepresentableBy.uniqueUpToIso"
]

/-- Search terms used for absent or not-yet-integrated homological collateral. -/
def collateralSearchTerms : List String := [
  "Yoneda lemma",
  "Yoneda.fullyFaithful",
  "RepresentableBy.uniqueUpToIso",
  "preadditiveYoneda",
  "preservesLimits_preadditiveYoneda_obj",
  "preadditiveYoneda IsHomological",
  "preadditiveCoyoneda IsHomological",
  "preadditiveYoneda map distinguished exact",
  "preadditiveYoneda exact",
  "coyoneda_exact",
  "long exact sequence",
  "homology sequence",
  "spectral sequence"
]

/--
Collateral branches that remain unchecked for this Stage1 slot.

These names are workflow leaves only.  They must not be treated as completed
theorems until a future child package adds explicit Lean wrappers and validates
them in this repository.
-/
def uncheckedCollateralBranches : List String := [
  "exactness collateral",
  "short-exact collateral",
  "long-exact collateral",
  "derived-category collateral",
  "spectral-sequence collateral"
]

/--
Parent-level completion gates for S1-M-138.

This is a machine-readable guard for the public merge-back process.  The
category-level Yoneda wrapper may be locally checked, but the whole Stage1 slot
must not be closed until every gate listed here is closed in the public audit
surface.
-/
def parentCompletionGates : List String := [
  "local validation: cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_138.lean",
  "machine anchor audit: canonicalMachineAnchors checked against pinned mathlib",
  "<=100 leaf ledger: category-level branch has an explicit local budget ledger",
  "public merge-back: blueprint and mirrored todo surfaces updated serially",
  "collateral boundary: uncheckedCollateralBranches remain open unless future wrappers validate"
]

#check Yoneda.fullyFaithful
#check Functor.FullyFaithful.preimageIso
#check Functor.FullyFaithful.isoEquiv
#check Functor.RepresentableBy.uniqueUpToIso
#check Functor.RepresentableBy.yoneda
#check Functor.IsRepresentedBy
#check Functor.IsRepresentedBy.representableBy
#check representingObjectUniqueOfIsRepresentedBy
#check yonedaEquiv
#check yonedaLemma
#check preadditiveYoneda
#check preservesLimits_preadditiveYoneda_obj
#check preservesLimits_preadditiveCoyoneda_obj
#check Projective.projective_iff_preservesEpimorphisms_preadditiveCoyoneda_obj
#check Injective.injective_iff_preservesEpimorphisms_preadditiveYoneda_obj
#check Functor.IsHomological
#check Pretriangulated.preadditiveYoneda_map_distinguished
#check Pretriangulated.preadditiveYoneda_homologySequenceδ_apply
#check Pretriangulated.preadditiveCoyoneda_homologySequenceδ_apply
#check ShortComplex.Exact
#check ShortComplex.ShortExact
#check ShortComplex.HasHomology
#check HomologicalComplex
#check CategoryTheory.SpectralSequence
#check preadditive_yoneda_isHomological
#check preadditive_coyoneda_isHomological
#check preadditive_yoneda_map_distinguished_exact
#check canonicalMachineAnchors
#check uncheckedCollateralBranches
#check parentCompletionGates
#check StatementShape
#check local_wrapper_upstream_mathlib

end S1_M_138
end Stage1
end AwesomeTheorems
