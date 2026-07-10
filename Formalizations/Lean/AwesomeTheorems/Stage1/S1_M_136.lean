import Mathlib.CategoryTheory.Limits.HasLimits
import Mathlib.CategoryTheory.Limits.Opposites
import Mathlib.CategoryTheory.Limits.Creates
import Mathlib.CategoryTheory.Limits.Preserves.Limits
import Mathlib.CategoryTheory.Limits.Constructions.LimitsOfProductsAndEqualizers
import Mathlib.CategoryTheory.Limits.Shapes.Products
import Mathlib.CategoryTheory.Limits.Types.Limits
import Mathlib.CategoryTheory.Limits.Types.Colimits
import Mathlib.Topology.Category.TopCat.Limits.Basic
import Mathlib.Topology.Category.CompHaus.Basic
import Mathlib.Algebra.Category.ModuleCat.Limits
import Mathlib.Algebra.Category.ModuleCat.Colimits
import Mathlib.Algebra.Homology.HomologySequenceLemmas

/-!
# S1-M-136 / THM-M-0084: Limits and colimits theorem

This Stage1 artifact records a conservative Lean boundary for the category-
theoretic theorem family around existence, functoriality, and homological
uses of limits and colimits.

The pinned mathlib snapshot already has the core `HasLimit`/`HasColimit`
interface, selected existence instances such as limits and colimits in `Type`,
and homological-algebra API for short exact sequences of complexes.  The source
slot is broad, so this file avoids claiming a terminal theorem.  It provides a
checked statement shape and low-risk wrappers around exact mathlib anchors.
-/

noncomputable section

open CategoryTheory
open CategoryTheory.Limits

universe vJ uJ vC uC vD uD uι

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_136

/--
Shape-level statement boundary for the limits-and-colimits theorem family.

For a fixed diagram shape `J` and category `C`, the normalized existence claim is
that every diagram `J ⥤ C` has both a limit and a colimit.  This is intentionally
expressed through mathlib's propositional typeclasses, not through a chosen
object-level construction.
-/
def ShapeStatement (J : Type uJ) [Category.{vJ} J]
    (C : Type uC) [Category.{vC} C] : Prop :=
  HasLimitsOfShape J C ∧ HasColimitsOfShape J C

/--
Size-level statement boundary: `C` has all limits and colimits of a specified
universe size.  This is the broadest category-level shape that can be stated
without adding mathematical hypotheses that are false for arbitrary categories.
-/
def StatementShape (C : Type uC) [Category.{vC} C] : Prop :=
  HasLimitsOfSize.{vJ, uJ} C ∧ HasColimitsOfSize.{vJ, uJ} C

/--
Decision surface for the terminal target shape considered by the public
Stage1 child task.
-/
inductive TerminalTargetKind where
  | shapeLevel
  | sizeLevel
  | wrapperBundle
  deriving DecidableEq, Repr

/--
Current child-task decision: the safe terminal Lean target is a bundle of
mathlib wrapper theorem families.

`ShapeStatement` and `StatementShape` remain useful statement boundaries, but a
single theorem asserting unrestricted existence of limits and colimits would be
false for arbitrary categories.  The repo-local target should therefore expose
hypothesis-sensitive wrappers around mathlib's `HasLimit`/`HasColimit`,
`HasLimitsOfShape`/`HasColimitsOfShape`, size-level instances where available,
and concrete category instances such as `Type`.
-/
def terminalTargetDecision : TerminalTargetKind :=
  TerminalTargetKind.wrapperBundle

/-- The terminal-target decision is the wrapper-bundle option. -/
theorem terminalTargetDecision_eq_wrapperBundle :
    terminalTargetDecision = TerminalTargetKind.wrapperBundle := rfl

/--
Concrete category families considered for the public theorem surface.

The broad limits/colimits theorem is not a single unrestricted theorem about
arbitrary categories.  The useful public surface should therefore expose
concrete checked families separately from hypothesis-driven abelian and
homological wrappers.
-/
inductive ConcreteCategorySurfaceKind where
  | typeUniverse
  | topologicalSpaces
  | moduleCategories
  | compactHausdorffSpaces
  | abelianHomologicalContext
  deriving DecidableEq, Repr

/--
Current child-task decision for concrete instances.

`Type`, `TopCat`, `ModuleCat R`, and `CompHaus` have checked repo-local
mathlib wrappers below.  The abelian/homological part remains a parameterized
context `[Category C] [Abelian C]` for homology-sequence wrappers instead of a
new concrete category instance.
-/
def concreteCategorySurfaceDecision : List ConcreteCategorySurfaceKind := [
  ConcreteCategorySurfaceKind.typeUniverse,
  ConcreteCategorySurfaceKind.topologicalSpaces,
  ConcreteCategorySurfaceKind.moduleCategories,
  ConcreteCategorySurfaceKind.compactHausdorffSpaces,
  ConcreteCategorySurfaceKind.abelianHomologicalContext
]

/-- The concrete-category surface selected for the Stage1 public task. -/
theorem concreteCategorySurfaceDecision_eq :
    concreteCategorySurfaceDecision = [
      ConcreteCategorySurfaceKind.typeUniverse,
      ConcreteCategorySurfaceKind.topologicalSpaces,
      ConcreteCategorySurfaceKind.moduleCategories,
      ConcreteCategorySurfaceKind.compactHausdorffSpaces,
      ConcreteCategorySurfaceKind.abelianHomologicalContext
    ] := rfl

/-- Extract `HasLimit F` from the shape-level statement boundary. -/
theorem hasLimit_of_shapeStatement
    {J : Type uJ} [Category.{vJ} J]
    {C : Type uC} [Category.{vC} C]
    (h : ShapeStatement J C) (F : J ⥤ C) :
    HasLimit F := by
  haveI : HasLimitsOfShape J C := h.1
  infer_instance

/-- Extract `HasColimit F` from the shape-level statement boundary. -/
theorem hasColimit_of_shapeStatement
    {J : Type uJ} [Category.{vJ} J]
    {C : Type uC} [Category.{vC} C]
    (h : ShapeStatement J C) (F : J ⥤ C) :
    HasColimit F := by
  haveI : HasColimitsOfShape J C := h.2
  infer_instance

/--
mathlib anchor: the chosen limit cone for a diagram is limiting whenever
`HasLimit F` is available.
-/
def limit_isLimit_mathlib
    {J : Type uJ} [Category.{vJ} J]
    {C : Type uC} [Category.{vC} C]
    (F : J ⥤ C) [HasLimit F] :
    IsLimit (limit.cone F) :=
  limit.isLimit F

/--
mathlib anchor: the chosen colimit cocone for a diagram is colimiting whenever
`HasColimit F` is available.
-/
def colimit_isColimit_mathlib
    {J : Type uJ} [Category.{vJ} J]
    {C : Type uC} [Category.{vC} C]
    (F : J ⥤ C) [HasColimit F] :
    IsColimit (colimit.cocone F) :=
  colimit.isColimit F

/-- mathlib anchor: functoriality/naturality square for maps of limits. -/
theorem limMap_π_naturality_mathlib
    {J : Type uJ} [Category.{vJ} J]
    {C : Type uC} [Category.{vC} C]
    {F G : J ⥤ C} [HasLimit F] [HasLimit G]
    (α : F ⟶ G) (j : J) :
    limMap α ≫ limit.π G j = limit.π F j ≫ α.app j := by
  exact limMap_π α j

/-- mathlib anchor: functoriality/naturality square for maps of colimits. -/
theorem ι_colimMap_naturality_mathlib
    {J : Type uJ} [Category.{vJ} J]
    {C : Type uC} [Category.{vC} C]
    {F G : J ⥤ C} [HasColimit F] [HasColimit G]
    (α : F ⟶ G) (j : J) :
    colimit.ι F j ≫ colimMap α = α.app j ≫ colimit.ι G j := by
  exact ι_colimMap α j

/-! ## Preserved and created (co)limit wrappers -/

/--
Preserved-limit comparison square: if a functor preserves the limit of `F`,
the canonical comparison isomorphism has projections given by applying the
functor to the original limit projections.
-/
theorem preservesLimitIso_hom_π_naturality_mathlib
    {J : Type uJ} [Category.{vJ} J]
    {C : Type uC} [Category.{vC} C]
    {D : Type uD} [Category.{vD} D]
    (G : C ⥤ D) (F : J ⥤ C) [HasLimit F] [PreservesLimit F G]
    (j : J) :
    (preservesLimitIso G F).hom ≫ limit.π (F ⋙ G) j =
      G.map (limit.π F j) := by
  exact preservesLimitIso_hom_π G F j

/--
Preserved-limit inverse comparison square: the inverse comparison isomorphism
recovers the limit projection of the image diagram.
-/
theorem preservesLimitIso_inv_π_naturality_mathlib
    {J : Type uJ} [Category.{vJ} J]
    {C : Type uC} [Category.{vC} C]
    {D : Type uD} [Category.{vD} D]
    (G : C ⥤ D) (F : J ⥤ C) [HasLimit F] [PreservesLimit F G]
    (j : J) :
    (preservesLimitIso G F).inv ≫ G.map (limit.π F j) =
      limit.π (F ⋙ G) j := by
  exact preservesLimitIso_inv_π G F j

/--
Preserved-colimit comparison square: if a functor preserves the colimit of
`F`, applying the functor to the original coprojections agrees with the
canonical colimit coprojections after the comparison isomorphism.
-/
theorem ι_preservesColimitIso_hom_naturality_mathlib
    {J : Type uJ} [Category.{vJ} J]
    {C : Type uC} [Category.{vC} C]
    {D : Type uD} [Category.{vD} D]
    (G : C ⥤ D) (F : J ⥤ C) [HasColimit F] [PreservesColimit F G]
    (j : J) :
    G.map (colimit.ι F j) ≫ (preservesColimitIso G F).hom =
      colimit.ι (F ⋙ G) j := by
  exact ι_preservesColimitIso_hom G F j

/--
Preserved-colimit inverse comparison square: the canonical coprojection into
the image colimit followed by the inverse comparison is the image of the
original coprojection.
-/
theorem ι_preservesColimitIso_inv_naturality_mathlib
    {J : Type uJ} [Category.{vJ} J]
    {C : Type uC} [Category.{vC} C]
    {D : Type uD} [Category.{vD} D]
    (G : C ⥤ D) (F : J ⥤ C) [HasColimit F] [PreservesColimit F G]
    (j : J) :
    colimit.ι (F ⋙ G) j ≫ (preservesColimitIso G F).inv =
      G.map (colimit.ι F j) := by
  exact ι_preservesColimitIso_inv G F j

/--
Creation route: if `G` creates the limit of `F` and the image diagram has a
limit, then the source diagram has a limit.
-/
theorem hasLimit_of_created_mathlib
    {J : Type uJ} [Category.{vJ} J]
    {C : Type uC} [Category.{vC} C]
    {D : Type uD} [Category.{vD} D]
    (F : J ⥤ C) (G : C ⥤ D) [HasLimit (F ⋙ G)] [CreatesLimit F G] :
    HasLimit F :=
  hasLimit_of_created F G

/--
Creation route: if `G` creates the colimit of `F` and the image diagram has a
colimit, then the source diagram has a colimit.
-/
theorem hasColimit_of_created_mathlib
    {J : Type uJ} [Category.{vJ} J]
    {C : Type uC} [Category.{vC} C]
    {D : Type uD} [Category.{vD} D]
    (F : J ⥤ C) (G : C ⥤ D) [HasColimit (F ⋙ G)] [CreatesColimit F G] :
    HasColimit F :=
  hasColimit_of_created F G

/--
Shape-level creation route for limits.
-/
theorem hasLimitsOfShape_of_created_mathlib
    {J : Type uJ} [Category.{vJ} J]
    {C : Type uC} [Category.{vC} C]
    {D : Type uD} [Category.{vD} D]
    (G : C ⥤ D) [HasLimitsOfShape J D] [CreatesLimitsOfShape J G] :
    HasLimitsOfShape J C :=
  hasLimitsOfShape_of_hasLimitsOfShape_createsLimitsOfShape G

/--
Shape-level creation route for colimits.
-/
theorem hasColimitsOfShape_of_created_mathlib
    {J : Type uJ} [Category.{vJ} J]
    {C : Type uC} [Category.{vC} C]
    {D : Type uD} [Category.{vD} D]
    (G : C ⥤ D) [HasColimitsOfShape J D] [CreatesColimitsOfShape J G] :
    HasColimitsOfShape J C :=
  hasColimitsOfShape_of_hasColimitsOfShape_createsColimitsOfShape G

/--
Creation implies preservation of a specific limit once the image diagram has
the corresponding limit.
-/
theorem preservesLimit_of_created_mathlib
    {J : Type uJ} [Category.{vJ} J]
    {C : Type uC} [Category.{vC} C]
    {D : Type uD} [Category.{vD} D]
    (F : J ⥤ C) (G : C ⥤ D) [HasLimit (F ⋙ G)] [CreatesLimit F G] :
    PreservesLimit F G := by
  infer_instance

/--
Creation implies preservation of a specific colimit once the image diagram has
the corresponding colimit.
-/
theorem preservesColimit_of_created_mathlib
    {J : Type uJ} [Category.{vJ} J]
    {C : Type uC} [Category.{vC} C]
    {D : Type uD} [Category.{vD} D]
    (F : J ⥤ C) (G : C ⥤ D) [HasColimit (F ⋙ G)] [CreatesColimit F G] :
    PreservesColimit F G := by
  infer_instance

/--
Shape-level creation implies shape-level preservation of limits under the
usual image-side existence hypothesis.
-/
theorem preservesLimitsOfShape_of_created_mathlib
    {J : Type uJ} [Category.{vJ} J]
    {C : Type uC} [Category.{vC} C]
    {D : Type uD} [Category.{vD} D]
    (G : C ⥤ D) [HasLimitsOfShape J D] [CreatesLimitsOfShape J G] :
    PreservesLimitsOfShape J G := by
  infer_instance

/--
Shape-level creation implies shape-level preservation of colimits under the
usual image-side existence hypothesis.
-/
theorem preservesColimitsOfShape_of_created_mathlib
    {J : Type uJ} [Category.{vJ} J]
    {C : Type uC} [Category.{vC} C]
    {D : Type uD} [Category.{vD} D]
    (G : C ⥤ D) [HasColimitsOfShape J D] [CreatesColimitsOfShape J G] :
    PreservesColimitsOfShape J G := by
  infer_instance

/-- mathlib anchor: `Type u` has limits of the requested small shape. -/
theorem type_hasLimit_mathlib
    {J : Type uJ} [Category.{vJ} J] [Small.{uC} J] (F : J ⥤ Type uC) :
    HasLimit F := by
  infer_instance

/-- mathlib anchor: `Type u` has colimits of the requested small shape. -/
theorem type_hasColimit_mathlib
    {J : Type uJ} [Category.{vJ} J] [Small.{uC} J] (F : J ⥤ Type uC) :
    HasColimit F := by
  infer_instance

/-! ## Concrete category instance wrappers -/

/-- mathlib anchor: `TopCat` has all limits. -/
theorem topCat_hasLimits_mathlib : HasLimits TopCat.{uC} := by
  infer_instance

/-- mathlib anchor: `TopCat` has all colimits. -/
theorem topCat_hasColimits_mathlib : HasColimits TopCat.{uC} := by
  infer_instance

/-- mathlib anchor: `TopCat` has limits of a small requested shape. -/
theorem topCat_hasLimit_mathlib
    {J : Type uJ} [Category.{vJ} J] [Small.{uC} J] (F : J ⥤ TopCat.{uC}) :
    HasLimit F := by
  infer_instance

/-- mathlib anchor: `TopCat` has colimits of a small requested shape. -/
theorem topCat_hasColimit_mathlib
    {J : Type uJ} [Category.{vJ} J] [Small.{uC} J] (F : J ⥤ TopCat.{uC}) :
    HasColimit F := by
  infer_instance

/-- mathlib anchor: module categories have all limits. -/
theorem moduleCat_hasLimits_mathlib (R : Type uC) [Ring R] :
    HasLimits (ModuleCat.{uC} R) := by
  infer_instance

/-- mathlib anchor: module categories have all colimits. -/
theorem moduleCat_hasColimits_mathlib (R : Type uC) [Ring R] :
    HasColimits (ModuleCat.{uC} R) := by
  infer_instance

/-- mathlib anchor: compact Hausdorff spaces have all limits. -/
theorem compHaus_hasLimits_mathlib : HasLimits CompHaus.{uC} := by
  infer_instance

/-- mathlib anchor: compact Hausdorff spaces have all colimits. -/
theorem compHaus_hasColimits_mathlib : HasColimits CompHaus.{uC} := by
  infer_instance

/-- Product existence is a specialization of discrete-shape limit existence. -/
theorem hasProduct_of_shapeStatement
    {β : Type uJ} {C : Type uC} [Category.{vC} C]
    (h : ShapeStatement (Discrete β) C) (f : β → C) :
    HasProduct f :=
  hasLimit_of_shapeStatement h (Discrete.functor f)

/-- Coproduct existence is a specialization of discrete-shape colimit existence. -/
theorem hasCoproduct_of_shapeStatement
    {β : Type uJ} {C : Type uC} [Category.{vC} C]
    (h : ShapeStatement (Discrete β) C) (f : β → C) :
    HasCoproduct f :=
  hasColimit_of_shapeStatement h (Discrete.functor f)

/-! ## Finite (co)limit construction-route wrappers -/

/--
mathlib route: terminal object plus binary products gives finite products.

This is the first finite-limit construction branch requested by the Stage1
child audit; it is a local wrapper around
`CategoryTheory.hasFiniteProducts_of_has_binary_and_terminal`.
-/
theorem hasFiniteProducts_of_terminal_binaryProducts_mathlib
    {C : Type uC} [Category.{vC} C] [HasTerminal C] [HasBinaryProducts C] :
    HasFiniteProducts C :=
  hasFiniteProducts_of_has_binary_and_terminal

/--
mathlib route: finite products plus equalizers gives finite limits.
-/
theorem hasFiniteLimits_of_finiteProducts_equalizers_mathlib
    {C : Type uC} [Category.{vC} C] [HasFiniteProducts C] [HasEqualizers C] :
    HasFiniteLimits C :=
  hasFiniteLimits_of_hasEqualizers_and_finite_products

/--
Combined finite-limit route from terminal object, binary products, and
equalizers.
-/
theorem hasFiniteLimits_of_terminal_binaryProducts_equalizers_mathlib
    {C : Type uC} [Category.{vC} C] [HasTerminal C] [HasBinaryProducts C]
    [HasEqualizers C] :
    HasFiniteLimits C := by
  haveI : HasFiniteProducts C := hasFiniteProducts_of_terminal_binaryProducts_mathlib
  exact hasFiniteLimits_of_finiteProducts_equalizers_mathlib

/--
mathlib dual route: initial object plus binary coproducts gives finite
coproducts.
-/
theorem hasFiniteCoproducts_of_initial_binaryCoproducts_mathlib
    {C : Type uC} [Category.{vC} C] [HasInitial C] [HasBinaryCoproducts C] :
    HasFiniteCoproducts C :=
  hasFiniteCoproducts_of_has_binary_and_initial

/--
mathlib dual route: finite coproducts plus coequalizers gives finite colimits.
-/
theorem hasFiniteColimits_of_finiteCoproducts_coequalizers_mathlib
    {C : Type uC} [Category.{vC} C] [HasFiniteCoproducts C]
    [HasCoequalizers C] :
    HasFiniteColimits C :=
  hasFiniteColimits_of_hasCoequalizers_and_finite_coproducts

/--
Combined finite-colimit route from initial object, binary coproducts, and
coequalizers.
-/
theorem hasFiniteColimits_of_initial_binaryCoproducts_coequalizers_mathlib
    {C : Type uC} [Category.{vC} C] [HasInitial C] [HasBinaryCoproducts C]
    [HasCoequalizers C] :
    HasFiniteColimits C := by
  haveI : HasFiniteCoproducts C :=
    hasFiniteCoproducts_of_initial_binaryCoproducts_mathlib
  exact hasFiniteColimits_of_finiteCoproducts_coequalizers_mathlib

/-! ## Opposite-category duality wrappers -/

/--
mathlib duality route: a limit of `F : J ⥤ C` gives a colimit of the opposite
diagram `F.op : Jᵒᵖ ⥤ Cᵒᵖ`.
-/
theorem hasColimit_op_of_hasLimit_mathlib
    {J : Type uJ} [Category.{vJ} J]
    {C : Type uC} [Category.{vC} C]
    (F : J ⥤ C) [HasLimit F] :
    HasColimit F.op := by
  infer_instance

/--
mathlib duality route: a colimit of `F : J ⥤ C` gives a limit of the opposite
diagram `F.op : Jᵒᵖ ⥤ Cᵒᵖ`.
-/
theorem hasLimit_op_of_hasColimit_mathlib
    {J : Type uJ} [Category.{vJ} J]
    {C : Type uC} [Category.{vC} C]
    (F : J ⥤ C) [HasColimit F] :
    HasLimit F.op := by
  infer_instance

/--
mathlib duality route in the reverse direction: a colimit of `F.op` in `Cᵒᵖ`
recovers a limit of `F` in `C`.
-/
theorem hasLimit_of_hasColimit_op_mathlib
    {J : Type uJ} [Category.{vJ} J]
    {C : Type uC} [Category.{vC} C]
    (F : J ⥤ C) [HasColimit F.op] :
    HasLimit F :=
  hasLimit_of_hasColimit_op F

/--
mathlib duality route in the reverse direction: a limit of `F.op` in `Cᵒᵖ`
recovers a colimit of `F` in `C`.
-/
theorem hasColimit_of_hasLimit_op_mathlib
    {J : Type uJ} [Category.{vJ} J]
    {C : Type uC} [Category.{vC} C]
    (F : J ⥤ C) [HasLimit F.op] :
    HasColimit F :=
  hasColimit_of_hasLimit_op F

/--
Shape-level duality route: limits of shape `Jᵒᵖ` in `C` give colimits of shape
`J` in `Cᵒᵖ`.
-/
theorem hasColimitsOfShape_op_of_hasLimitsOfShape_mathlib
    {J : Type uJ} [Category.{vJ} J]
    {C : Type uC} [Category.{vC} C]
    [HasLimitsOfShape Jᵒᵖ C] :
    HasColimitsOfShape J Cᵒᵖ := by
  infer_instance

/--
Shape-level duality route: colimits of shape `Jᵒᵖ` in `C` give limits of shape
`J` in `Cᵒᵖ`.
-/
theorem hasLimitsOfShape_op_of_hasColimitsOfShape_mathlib
    {J : Type uJ} [Category.{vJ} J]
    {C : Type uC} [Category.{vC} C]
    [HasColimitsOfShape Jᵒᵖ C] :
    HasLimitsOfShape J Cᵒᵖ :=
  hasLimitsOfShape_op_of_hasColimitsOfShape

/--
Size-level duality route: limits of a universe size in `C` give colimits of the
same size in `Cᵒᵖ`.
-/
theorem hasColimitsOfSize_op_of_hasLimitsOfSize_mathlib
    {C : Type uC} [Category.{vC} C] [HasLimitsOfSize.{vJ, uJ} C] :
    HasColimitsOfSize.{vJ, uJ} Cᵒᵖ := by
  infer_instance

/--
Size-level duality route: colimits of a universe size in `C` give limits of the
same size in `Cᵒᵖ`.
-/
theorem hasLimitsOfSize_op_of_hasColimitsOfSize_mathlib
    {C : Type uC} [Category.{vC} C] [HasColimitsOfSize.{vJ, uJ} C] :
    HasLimitsOfSize.{vJ, uJ} Cᵒᵖ := by
  infer_instance

/--
Homological-algebra anchor: the connecting morphism in the homology sequence is
natural with respect to a morphism of short exact sequences of complexes.

This is a checked wrapper around mathlib's
`HomologicalComplex.HomologySequence.δ_naturality`; it is adjacent evidence for
the Stage1 scope involving naturality squares and short-exact/long-exact
sequence subresults, not a proof of every broad limit/colimit theorem.
-/
theorem homologySequence_δ_naturality_mathlib
    {C : Type uC} [Category.{vC} C] [Abelian C]
    {ι : Type uι} {c : ComplexShape ι}
    {S₁ S₂ : ShortComplex (HomologicalComplex C c)} (φ : S₁ ⟶ S₂)
    (hS₁ : S₁.ShortExact) (hS₂ : S₂.ShortExact)
    (i j : ι) (hij : c.Rel i j) :
    hS₁.δ i j hij ≫ HomologicalComplex.homologyMap φ.τ₁ _ =
      HomologicalComplex.homologyMap φ.τ₃ _ ≫ hS₂.δ i j hij := by
  simpa using
    (HomologicalComplex.HomologySequence.δ_naturality φ hS₁ hS₂ i j hij)

/--
Homological-algebra anchor: the length-five homology sequence attached to a
short exact sequence of complexes is exact.
-/
theorem homologySequence_composableArrows₅_exact_mathlib
    {C : Type uC} [Category.{vC} C] [Abelian C]
    {ι : Type uι} {c : ComplexShape ι}
    {S₁ : ShortComplex (HomologicalComplex C c)}
    (hS₁ : S₁.ShortExact) (i j : ι) (hij : c.Rel i j) :
    (HomologicalComplex.HomologySequence.composableArrows₅ hS₁ i j hij).Exact := by
  exact HomologicalComplex.HomologySequence.composableArrows₅_exact hS₁ i j hij

/-! ## Homology-sequence theorem-tree wrappers -/

/--
The homological branch of the limits-and-colimits public surface is not a new
terminal theorem about arbitrary limits.  It is a checked theorem tree around a
short exact sequence of complexes and the long exact homology sequence windows
that mathlib already exposes.
-/
inductive HomologySequenceTheoremTreeNode where
  | shortExactSequenceOfComplexes
  | connectingMorphism
  | lengthTwoExactWindow
  | lengthFiveLongExactWindow
  | naturalityForMorphismOfShortExactSequences
  deriving DecidableEq, Repr

/-- Stage1 child `S1-M-136-C006` theorem-tree route for the homology branch. -/
def homologySequenceTheoremTreeRoute : List HomologySequenceTheoremTreeNode := [
  HomologySequenceTheoremTreeNode.shortExactSequenceOfComplexes,
  HomologySequenceTheoremTreeNode.connectingMorphism,
  HomologySequenceTheoremTreeNode.lengthTwoExactWindow,
  HomologySequenceTheoremTreeNode.lengthFiveLongExactWindow,
  HomologySequenceTheoremTreeNode.naturalityForMorphismOfShortExactSequences
]

/-- The checked homology-sequence route selected by child `S1-M-136-C006`. -/
theorem homologySequenceTheoremTreeRoute_eq :
    homologySequenceTheoremTreeRoute = [
      HomologySequenceTheoremTreeNode.shortExactSequenceOfComplexes,
      HomologySequenceTheoremTreeNode.connectingMorphism,
      HomologySequenceTheoremTreeNode.lengthTwoExactWindow,
      HomologySequenceTheoremTreeNode.lengthFiveLongExactWindow,
      HomologySequenceTheoremTreeNode.naturalityForMorphismOfShortExactSequences
    ] := rfl

/--
Short-exact input node: the homology-sequence branch starts from a short exact
short complex in the category of homological complexes.
-/
theorem homologySequence_shortExact_input_mathlib
    {C : Type uC} [Category.{vC} C] [Abelian C]
    {ι : Type uι} {c : ComplexShape ι}
    {S : ShortComplex (HomologicalComplex C c)}
    (hS : S.ShortExact) :
    S.ShortExact := hS

/--
Connecting-morphism node: a short exact sequence of complexes supplies the
boundary map `Hᵢ(S.X₃) ⟶ Hⱼ(S.X₁)` whenever the complex shape relates `i` to
`j`.
-/
noncomputable def homologySequence_δ_mathlib
    {C : Type uC} [Category.{vC} C] [Abelian C]
    {ι : Type uι} {c : ComplexShape ι}
    {S : ShortComplex (HomologicalComplex C c)}
    (hS : S.ShortExact) (i j : ι) (hij : c.Rel i j) :
    S.X₃.homology i ⟶ S.X₁.homology j :=
  hS.δ i j hij

/--
Length-two exact-window node: exactness of
`Hᵢ(S.X₁) ⟶ Hᵢ(S.X₂) ⟶ Hᵢ(S.X₃)`.
-/
theorem homologySequence_composableArrows₂_exact_mathlib
    {C : Type uC} [Category.{vC} C] [Abelian C]
    {ι : Type uι} {c : ComplexShape ι}
    {S : ShortComplex (HomologicalComplex C c)}
    (hS : S.ShortExact) (i : ι) :
    (HomologicalComplex.HomologySequence.composableArrows₂ S i).Exact := by
  exact HomologicalComplex.HomologySequence.composableArrows₂_exact hS i

/--
Naturality-map node for the length-two exact windows induced by a morphism of
short complexes of complexes.
-/
noncomputable def homologySequence_mapComposableArrows₂_mathlib
    {C : Type uC} [Category.{vC} C] [Abelian C]
    {ι : Type uι} {c : ComplexShape ι}
    {S₁ S₂ : ShortComplex (HomologicalComplex C c)} (φ : S₁ ⟶ S₂)
    (i : ι) :
    HomologicalComplex.HomologySequence.composableArrows₂ S₁ i ⟶
      HomologicalComplex.HomologySequence.composableArrows₂ S₂ i :=
  HomologicalComplex.HomologySequence.mapComposableArrows₂ φ i

/--
Naturality-map node for the length-five long-exact-sequence windows induced by
a morphism of short exact sequences of complexes.
-/
noncomputable def homologySequence_mapComposableArrows₅_mathlib
    {C : Type uC} [Category.{vC} C] [Abelian C]
    {ι : Type uι} {c : ComplexShape ι}
    {S₁ S₂ : ShortComplex (HomologicalComplex C c)} (φ : S₁ ⟶ S₂)
    (hS₁ : S₁.ShortExact) (hS₂ : S₂.ShortExact)
    (i j : ι) (hij : c.Rel i j) :
    HomologicalComplex.HomologySequence.composableArrows₅ hS₁ i j hij ⟶
      HomologicalComplex.HomologySequence.composableArrows₅ hS₂ i j hij :=
  HomologicalComplex.HomologySequence.mapComposableArrows₅ φ hS₁ hS₂ i j hij

/-- mathlib modules checked as positive anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.CategoryTheory.Limits.HasLimits",
  "Mathlib.CategoryTheory.Limits.Opposites",
  "Mathlib.CategoryTheory.Limits.Creates",
  "Mathlib.CategoryTheory.Limits.Preserves.Limits",
  "Mathlib.CategoryTheory.Limits.Shapes.Products",
  "Mathlib.CategoryTheory.Limits.Types.Limits",
  "Mathlib.CategoryTheory.Limits.Types.Colimits",
  "Mathlib.Topology.Category.TopCat.Limits.Basic",
  "Mathlib.Topology.Category.CompHaus.Basic",
  "Mathlib.Algebra.Category.ModuleCat.Limits",
  "Mathlib.Algebra.Category.ModuleCat.Colimits",
  "Mathlib.CategoryTheory.Abelian.Basic",
  "Mathlib.Algebra.Homology.HomologySequenceLemmas"
]

/-- Search terms used for terminal/broad theorem audit in the pinned tree. -/
def auditSearchTerms : List String := [
  "HasLimits",
  "HasColimits",
  "HasFiniteLimits",
  "HasFiniteColimits",
  "hasFiniteProducts_of_has_binary_and_terminal",
  "hasFiniteLimits_of_hasEqualizers_and_finite_products",
  "hasFiniteCoproducts_of_has_binary_and_initial",
  "hasFiniteColimits_of_hasCoequalizers_and_finite_coproducts",
  "hasColimit_op_of_hasLimit",
  "hasLimit_op_of_hasColimit",
  "hasLimit_of_hasColimit_op",
  "hasColimit_of_hasLimit_op",
  "hasColimitsOfShape_op_of_hasLimitsOfShape",
  "hasLimitsOfShape_op_of_hasColimitsOfShape",
  "hasColimits_op_of_hasLimits",
  "hasLimits_op_of_hasColimits",
  "limMap_π",
  "ι_colimMap",
  "preservesLimitIso_hom_π",
  "preservesLimitIso_inv_π",
  "ι_preservesColimitIso_hom",
  "ι_preservesColimitIso_inv",
  "hasLimit_of_created",
  "hasColimit_of_created",
  "preservesLimit_of_createsLimit_and_hasLimit",
  "preservesColimit_of_createsColimit_and_hasColimit",
  "TopCat.topCat_hasLimits",
  "TopCat.topCat_hasColimits",
  "ModuleCat.hasLimits",
  "ModuleCat.hasColimits",
  "CompHaus.hasLimits",
  "CompHaus.hasColimits",
  "HomologySequence.δ_naturality",
  "HomologySequence.composableArrows₂_exact",
  "composableArrows₅_exact",
  "HomologySequence.mapComposableArrows₂",
  "HomologySequence.mapComposableArrows₅",
  "limit colimit theorem",
  "existence of limits"
]

/-! ## Audit metadata retained in the checked file. -/

/-- Current repo-local machine status for the broad terminal theorem. -/
def machineCheckedStatus : String :=
  "not_repo_local_closed"

/-- Current machine proof debt classification for the terminal theorem. -/
def machineProofDebtClassification : String :=
  "formalization_debt"

/--
Completion gate for this slot: no completed state may retain
`repo_local_integration_debt`; a discovered external Lean 4 proof must be
pinned/imported/checked or recorded as a concrete blocker before completion.
-/
def repoLocalIntegrationDebtGate : String :=
  "not completed; no completed state retains repo_local_integration_debt"

/-- External terminal closure status recorded for this repair pass. -/
def externalLean4ClosureStatus : String :=
  "no external terminal Lean 4 closure integrated into this Lake environment"

/-! ## Child C008 external Lean 4 primary-source audit metadata -/

/--
Outcome vocabulary for child `S1-M-136-C008`.

This child is an external-primary-source audit and integration-gate task.  It
does not add a new dependency, because no pin-ready terminal limits/colimits
package was identified inside this worker's write scope.
-/
inductive ExternalLean4TerminalPackageAuditOutcome where
  | noPinReadyTerminalPackageLocated
  | authenticatedCodeSearchBlocked
  | candidateIntegrationBlocked
  | externalUpstreamPinned
  deriving DecidableEq, Repr

/-- Date of the C008 external-primary-source audit record. -/
def externalLean4TerminalPackageAuditDate : String :=
  "2026-05-01"

/-- Primary-source search surface used by child `S1-M-136-C008`. -/
def externalLean4TerminalPackageAuditScope : List String := [
  "pinned mathlib4 dependency already in this Lake closure",
  "GitHub primary-source code search for HasLimitsOfShape and HasColimitsOfShape",
  "public Lean 4 category-theory repositories surfaced by web/source search",
  "Lake pin feasibility against Lean v4.29.0 and mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95"
]

/--
C008 audit result: no external terminal limits/colimits theorem package was
available to pin/import/check in this child pass.

The broad limits/colimits surface remains represented by local wrappers over
the pinned mathlib dependency, not by an additional external dependency.
-/
def externalLean4TerminalPackageAuditOutcome :
    ExternalLean4TerminalPackageAuditOutcome :=
  ExternalLean4TerminalPackageAuditOutcome.noPinReadyTerminalPackageLocated

/-- Concrete C008 blockers before any external package can be completed. -/
def externalLean4TerminalPackageAuditBlockers : List String := [
  "GitHub CLI is not authenticated and unauthenticated GitHub REST code search is rate-limited",
  "no repository/commit/module/theorem tuple for a terminal external Lean 4 limits-colimits package was identified",
  "any future candidate must be pinned or vendored and checked in this Lake environment before it can be completion evidence"
]

/- C008 does not claim theorem completion and leaves no completed anchor-only state. -/
def externalLean4TerminalPackageNoCompletedIntegrationDebt : Bool :=
  true

/-- The C008 result is the no-pin-ready-package outcome. -/
theorem externalLean4TerminalPackageAuditOutcome_eq :
    externalLean4TerminalPackageAuditOutcome =
      ExternalLean4TerminalPackageAuditOutcome.noPinReadyTerminalPackageLocated := rfl

/--
C008 gate: this child did not put an external Lean 4 source into a completed
anchor-only state.
-/
theorem externalLean4TerminalPackageNoCompletedIntegrationDebt_eq_true :
    externalLean4TerminalPackageNoCompletedIntegrationDebt = true := rfl

/-- Finite-limit construction route audited by child `S1-M-136-C002`. -/
def finiteLimitConstructionRoute : List String := [
  "HasTerminal C",
  "HasBinaryProducts C",
  "HasFiniteProducts C",
  "HasEqualizers C",
  "HasFiniteLimits C"
]

/-- Finite-colimit construction route audited by child `S1-M-136-C002`. -/
def finiteColimitConstructionRoute : List String := [
  "HasInitial C",
  "HasBinaryCoproducts C",
  "HasFiniteCoproducts C",
  "HasCoequalizers C",
  "HasFiniteColimits C"
]

/-- Opposite-category duality anchors audited by child `S1-M-136-C003`. -/
def oppositeCategoryDualityRoute : List String := [
  "HasLimit F",
  "HasColimit F.op",
  "HasColimit F",
  "HasLimit F.op",
  "HasLimitsOfShape Jᵒᵖ C",
  "HasColimitsOfShape J Cᵒᵖ",
  "HasColimitsOfShape Jᵒᵖ C",
  "HasLimitsOfShape J Cᵒᵖ",
  "HasLimitsOfSize C",
  "HasColimitsOfSize Cᵒᵖ",
  "HasColimitsOfSize C",
  "HasLimitsOfSize Cᵒᵖ"
]

/-- Preserved/created naturality anchors audited by child `S1-M-136-C004`. -/
def preservedCreatedNaturalityRoute : List String := [
  "limMap_π",
  "ι_colimMap",
  "PreservesLimit F G",
  "preservesLimitIso G F",
  "preservesLimitIso_hom_π",
  "preservesLimitIso_inv_π",
  "PreservesColimit F G",
  "preservesColimitIso G F",
  "ι_preservesColimitIso_hom",
  "ι_preservesColimitIso_inv",
  "CreatesLimit F G",
  "hasLimit_of_created F G",
  "preservesLimit_of_createsLimit_and_hasLimit",
  "CreatesColimit F G",
  "hasColimit_of_created F G",
  "preservesColimit_of_createsColimit_and_hasColimit"
]

/-- Concrete category surface audited by child `S1-M-136-C005`. -/
def concreteCategoryInstanceRoute : List String := [
  "Type u: checked shape-level wrappers under the required smallness hypotheses",
  "TopCat: checked all-limits and all-colimits wrappers",
  "ModuleCat R: checked all-limits and all-colimits wrappers for rings R",
  "CompHaus: checked all-limits and all-colimits wrappers",
  "Abelian/homological categories: retained as parameterized [Category C] [Abelian C] context"
]

/-- Homology-sequence theorem-tree anchors audited by child `S1-M-136-C006`. -/
def homologySequenceTheoremTreeAnchors : List String := [
  "input: S.ShortExact for S : ShortComplex (HomologicalComplex C c)",
  "boundary: ShortComplex.ShortExact.δ",
  "local exactness: HomologySequence.composableArrows₂_exact",
  "long exact window: HomologySequence.composableArrows₅_exact",
  "naturality square: HomologySequence.δ_naturality",
  "window maps: HomologySequence.mapComposableArrows₂ and mapComposableArrows₅"
]

/-! ## Child C007 unchecked-leaf split ledger metadata -/

/--
Unchecked parent leaves that must be split into independent `<=100` step
ledgers before any public status upgrade.
-/
inductive UncheckedLeafId where
  | u001
  | u002
  | u003
  | u004
  | u005
  | u006
  | u007
  | u008
  | u009
  deriving DecidableEq, Repr

/-- Child `S1-M-136-C007` split target list for the unchecked `S1M136-U*` leaves. -/
def uncheckedLeafSplitLedgerIds : List UncheckedLeafId := [
  UncheckedLeafId.u001,
  UncheckedLeafId.u002,
  UncheckedLeafId.u003,
  UncheckedLeafId.u004,
  UncheckedLeafId.u005,
  UncheckedLeafId.u006,
  UncheckedLeafId.u007,
  UncheckedLeafId.u008,
  UncheckedLeafId.u009
]

/-- The M0387 local proof/process budget assigned to each split leaf. -/
def uncheckedLeafSplitLedgerBudget : Nat := 100

/--
Repo-local gate recorded by child `S1-M-136-C007`: every unchecked parent leaf
must have its own independent split ledger before a public status upgrade.
-/
def uncheckedLeafSplitLedgerGate : String :=
  "status upgrade blocked until each S1M136-U* leaf has an independent <=100-step ledger"

/-- The split-ledger budget is the M0387 `<=100` budget. -/
theorem uncheckedLeafSplitLedgerBudget_eq :
    uncheckedLeafSplitLedgerBudget = 100 := rfl

/-- The C007 split target list contains all nine unchecked parent leaves. -/
theorem uncheckedLeafSplitLedgerIds_eq :
    uncheckedLeafSplitLedgerIds = [
      UncheckedLeafId.u001,
      UncheckedLeafId.u002,
      UncheckedLeafId.u003,
      UncheckedLeafId.u004,
      UncheckedLeafId.u005,
      UncheckedLeafId.u006,
      UncheckedLeafId.u007,
      UncheckedLeafId.u008,
      UncheckedLeafId.u009
    ] := rfl

/-! ## Audit probes -/

#check ShapeStatement
#check StatementShape
#check TerminalTargetKind
#check terminalTargetDecision
#check terminalTargetDecision_eq_wrapperBundle
#check ConcreteCategorySurfaceKind
#check concreteCategorySurfaceDecision
#check concreteCategorySurfaceDecision_eq
#check hasLimit_of_shapeStatement
#check hasColimit_of_shapeStatement
#check limit_isLimit_mathlib
#check colimit_isColimit_mathlib
#check limMap_π_naturality_mathlib
#check ι_colimMap_naturality_mathlib
#check preservesLimitIso_hom_π_naturality_mathlib
#check preservesLimitIso_inv_π_naturality_mathlib
#check ι_preservesColimitIso_hom_naturality_mathlib
#check ι_preservesColimitIso_inv_naturality_mathlib
#check hasLimit_of_created_mathlib
#check hasColimit_of_created_mathlib
#check hasLimitsOfShape_of_created_mathlib
#check hasColimitsOfShape_of_created_mathlib
#check preservesLimit_of_created_mathlib
#check preservesColimit_of_created_mathlib
#check preservesLimitsOfShape_of_created_mathlib
#check preservesColimitsOfShape_of_created_mathlib
#check type_hasLimit_mathlib
#check type_hasColimit_mathlib
#check topCat_hasLimits_mathlib
#check topCat_hasColimits_mathlib
#check topCat_hasLimit_mathlib
#check topCat_hasColimit_mathlib
#check moduleCat_hasLimits_mathlib
#check moduleCat_hasColimits_mathlib
#check compHaus_hasLimits_mathlib
#check compHaus_hasColimits_mathlib
#check hasProduct_of_shapeStatement
#check hasCoproduct_of_shapeStatement
#check hasFiniteProducts_of_terminal_binaryProducts_mathlib
#check hasFiniteLimits_of_finiteProducts_equalizers_mathlib
#check hasFiniteLimits_of_terminal_binaryProducts_equalizers_mathlib
#check hasFiniteCoproducts_of_initial_binaryCoproducts_mathlib
#check hasFiniteColimits_of_finiteCoproducts_coequalizers_mathlib
#check hasFiniteColimits_of_initial_binaryCoproducts_coequalizers_mathlib
#check hasColimit_op_of_hasLimit_mathlib
#check hasLimit_op_of_hasColimit_mathlib
#check hasLimit_of_hasColimit_op_mathlib
#check hasColimit_of_hasLimit_op_mathlib
#check hasColimitsOfShape_op_of_hasLimitsOfShape_mathlib
#check hasLimitsOfShape_op_of_hasColimitsOfShape_mathlib
#check hasColimitsOfSize_op_of_hasLimitsOfSize_mathlib
#check hasLimitsOfSize_op_of_hasColimitsOfSize_mathlib
#check homologySequence_δ_naturality_mathlib
#check homologySequence_composableArrows₅_exact_mathlib
#check HomologySequenceTheoremTreeNode
#check homologySequenceTheoremTreeRoute
#check homologySequenceTheoremTreeRoute_eq
#check homologySequence_shortExact_input_mathlib
#check homologySequence_δ_mathlib
#check homologySequence_composableArrows₂_exact_mathlib
#check homologySequence_mapComposableArrows₂_mathlib
#check homologySequence_mapComposableArrows₅_mathlib
#check HasLimit
#check HasColimit
#check HasLimitsOfShape
#check HasColimitsOfShape
#check machineCheckedStatus
#check machineProofDebtClassification
#check repoLocalIntegrationDebtGate
#check externalLean4ClosureStatus
#check ExternalLean4TerminalPackageAuditOutcome
#check externalLean4TerminalPackageAuditDate
#check externalLean4TerminalPackageAuditScope
#check externalLean4TerminalPackageAuditOutcome
#check externalLean4TerminalPackageAuditBlockers
#check externalLean4TerminalPackageNoCompletedIntegrationDebt
#check externalLean4TerminalPackageAuditOutcome_eq
#check externalLean4TerminalPackageNoCompletedIntegrationDebt_eq_true
#check finiteLimitConstructionRoute
#check finiteColimitConstructionRoute
#check oppositeCategoryDualityRoute
#check preservedCreatedNaturalityRoute
#check concreteCategoryInstanceRoute
#check homologySequenceTheoremTreeAnchors
#check UncheckedLeafId
#check uncheckedLeafSplitLedgerIds
#check uncheckedLeafSplitLedgerBudget
#check uncheckedLeafSplitLedgerGate
#check uncheckedLeafSplitLedgerBudget_eq
#check uncheckedLeafSplitLedgerIds_eq

end S1_M_136
end Stage1
end AwesomeTheorems
