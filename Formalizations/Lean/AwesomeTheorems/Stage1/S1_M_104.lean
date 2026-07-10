/-
Copyright (c) 2026 Awesome Theorems contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/

import Mathlib.Algebra.Category.ModuleCat.Descent
import Mathlib.Algebra.Homology.ShortComplex.ModuleCat
import Mathlib.RingTheory.Flat.FaithfullyFlat.Basic
import Mathlib.RingTheory.Flat.FaithfullyFlat.Descent
import Mathlib.RingTheory.Finiteness.Descent
import Mathlib.AlgebraicGeometry.Morphisms.FlatDescent
import Mathlib.CategoryTheory.Sites.Descent.IsStack

/-!
# S1-M-104 / THM-M-0011: flat descent theorem

This Stage1 artifact records a conservative Lean 4 boundary for the broad
"flat descent theorem" entry.  The local mathlib snapshot contains strong
faithfully-flat descent anchors for modules, tensor exactness, ring properties,
algebraic-geometry morphism properties, and abstract descent data.  It does not
by itself provide a single terminal theorem packaging all homological flat
base-change/descent consequences.

The declarations below are therefore checked wrappers and statement shapes.
They contain no proof placeholders and should not be read as a completed proof
of the full theorem item.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits ModuleCat

universe u v w x y z

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_104

/--
Module-category core of the flat descent theorem.

For a faithfully flat ring homomorphism, extension of scalars reflects
isomorphisms, preserves finite limits, and is comonadic.  This is a checked
mathlib-backed boundary for effective descent of modules, not a terminal
derived or sheaf-cohomological flat base-change theorem.
-/
def ModuleCategoryDescentShape (A B : Type u) [CommRing A] [CommRing B]
    (f : A →+* B) : Prop :=
  f.FaithfullyFlat →
    (ModuleCat.extendScalars.{u, u, u} f).ReflectsIsomorphisms ∧
      PreservesFiniteLimits (ModuleCat.extendScalars.{u, u, u} f) ∧
      Nonempty (ComonadicLeftAdjoint (ModuleCat.extendScalars.{u, u, u} f))

/-- Repo-local checked wrapper for the module-category faithfully-flat descent anchors. -/
theorem moduleCategoryDescentShape_of_faithfullyFlat
    {A B : Type u} [CommRing A] [CommRing B] (f : A →+* B) :
    ModuleCategoryDescentShape A B f := by
  intro hf
  exact ⟨ModuleCat.reflectsIsomorphisms_extendScalars_of_faithfullyFlat hf,
    ModuleCat.preservesFiniteLimits_extendScalars_of_flat hf.flat,
    ⟨comonadicExtendScalars hf⟩⟩

/--
Stage1 statement-shape candidate for the flat descent theorem.

This only states the module-category effective-descent core that is already
available in mathlib.  Later integrators should replace or extend it with a
terminal theorem only after the derived/exactness/base-change branches are
locally imported or proved.
-/
def StatementShape : Prop :=
  ∀ {A B : Type u} [CommRing A] [CommRing B] (f : A →+* B),
    ModuleCategoryDescentShape A B f

/-- The current repo-local statement shape is closed by mathlib module descent. -/
theorem statementShape_mathlib_moduleCategory : StatementShape.{u} := by
  intro A B _ _ f
  exact moduleCategoryDescentShape_of_faithfullyFlat f

/--
Statement-normalization marker for the public Stage1 backfill.

`AwesomeTheorems.Stage1.S1_M_104.StatementShape` is the current repo-local
module-category statement boundary for THM-M-0011.  It is intentionally the
checked effective-descent core supplied by mathlib, not the terminal flat
descent theorem with all derived, exactness, base-change, and sheaf-level
branches packaged into one statement.
-/
theorem statementShape_current_moduleCategory_boundary : StatementShape.{u} :=
  statementShape_mathlib_moduleCategory

/--
Checked tensor-exactness reflection wrapper.  This is the short-exact/long-exact
ledger branch at the level currently exposed by mathlib: exactness of linear
maps is reflected after tensoring with a faithfully flat module.
-/
theorem faithfullyFlat_lTensor_exact_iff_exact
    {R : Type u} [CommRing R] {M : Type v} [AddCommGroup M] [Module R M]
    {N₁ : Type w} [AddCommGroup N₁] [Module R N₁]
    {N₂ : Type x} [AddCommGroup N₂] [Module R N₂]
    {N₃ : Type y} [AddCommGroup N₃] [Module R N₃]
    [Module.FaithfullyFlat R M] (l₁₂ : N₁ →ₗ[R] N₂) (l₂₃ : N₂ →ₗ[R] N₃) :
    Function.Exact (LinearMap.lTensor M l₁₂) (LinearMap.lTensor M l₂₃) ↔
      Function.Exact l₁₂ l₂₃ :=
  Module.FaithfullyFlat.lTensor_exact_iff_exact R M l₁₂ l₂₃

/-- Right tensor version of the exactness reflection anchor. -/
theorem faithfullyFlat_rTensor_exact_iff_exact
    {R : Type u} [CommRing R] {M : Type v} [AddCommGroup M] [Module R M]
    {N₁ : Type w} [AddCommGroup N₁] [Module R N₁]
    {N₂ : Type x} [AddCommGroup N₂] [Module R N₂]
    {N₃ : Type y} [AddCommGroup N₃] [Module R N₃]
    [Module.FaithfullyFlat R M] (l₁₂ : N₁ →ₗ[R] N₂) (l₂₃ : N₂ →ₗ[R] N₃) :
    Function.Exact (LinearMap.rTensor M l₁₂) (LinearMap.rTensor M l₂₃) ↔
      Function.Exact l₁₂ l₂₃ :=
  Module.FaithfullyFlat.rTensor_exact_iff_exact R M l₁₂ l₂₃

section TensorShortExact

variable {R : Type u} [CommRing R]
variable {M : Type v} [AddCommGroup M] [Module R M]

/--
The explicit short complex obtained by left-tensoring a short complex of
`R`-modules with `M`.

This is intentionally a concrete `ModuleCat` wrapper around the linear-map
tensor API, so the Stage1 exactness branch can bridge
`Function.Exact` to `ShortComplex.ShortExact`.
-/
abbrev lTensorShortComplex (S : ShortComplex (ModuleCat.{w} R)) :
    ShortComplex (ModuleCat.{max v w} R) :=
  ShortComplex.moduleCatMk (S.f.hom.lTensor M) (S.g.hom.lTensor M) (by
    rw [← LinearMap.lTensor_comp]
    have hfg : S.g.hom.comp S.f.hom = 0 := by
      ext x
      exact S.zero_apply x
    rw [hfg, LinearMap.lTensor_zero])

/--
Faithfully-flat left tensoring preserves and reflects short exactness of
short complexes in `ModuleCat`.

The proof is the requested bridge from mathlib's `Function.Exact` tensor
wrappers to `ShortComplex.ShortExact`: exactness is transported through
`ShortComplex.ShortExact.moduleCat_exact_iff_function_exact`, and the mono/epi
ends are transported through the faithfully-flat injective/surjective tensor
reflection lemmas.
-/
theorem faithfullyFlat_lTensor_shortExact_iff_shortExact
    [Module.FaithfullyFlat R M] (S : ShortComplex (ModuleCat.{w} R)) :
    (lTensorShortComplex (M := M) S).ShortExact ↔ S.ShortExact := by
  constructor
  · intro hS
    exact ModuleCat.shortComplex_shortExact S
      ((Module.FaithfullyFlat.lTensor_exact_iff_exact R M S.f.hom S.g.hom).mp
        ((ShortComplex.ShortExact.moduleCat_exact_iff_function_exact
          (lTensorShortComplex (M := M) S)).mp hS.exact))
      ((Module.FaithfullyFlat.lTensor_injective_iff_injective R M S.f.hom).mp
        (ShortComplex.ShortExact.moduleCat_injective_f hS))
      ((Module.FaithfullyFlat.lTensor_surjective_iff_surjective R M S.g.hom).mp
        (ShortComplex.ShortExact.moduleCat_surjective_g hS))
  · intro hS
    exact ModuleCat.shortComplex_shortExact (lTensorShortComplex (M := M) S)
      ((Module.FaithfullyFlat.lTensor_exact_iff_exact R M S.f.hom S.g.hom).mpr
        ((ShortComplex.ShortExact.moduleCat_exact_iff_function_exact S).mp hS.exact))
      ((Module.FaithfullyFlat.lTensor_injective_iff_injective R M S.f.hom).mpr
        (ShortComplex.ShortExact.moduleCat_injective_f hS))
      ((Module.FaithfullyFlat.lTensor_surjective_iff_surjective R M S.g.hom).mpr
        (ShortComplex.ShortExact.moduleCat_surjective_g hS))

/--
Local right-tensor injectivity bridge used by the short-exact wrapper below.

Mathlib exposes the corresponding left-tensor iff directly; the right-tensor
form follows from the faithfully-flat right-tensor exactness reflection theorem
and the standard zero/exact characterization of injectivity.
-/
theorem faithfullyFlat_rTensor_injective_iff_injective
    [Module.FaithfullyFlat R M]
    {N N' : Type w} [AddCommGroup N] [AddCommGroup N'] [Module R N] [Module R N']
    (f : N →ₗ[R] N') :
    Function.Injective (f.rTensor M) ↔ Function.Injective f := by
  rw [← LinearMap.exact_zero_iff_injective (TensorProduct R Unit M),
    ← LinearMap.exact_zero_iff_injective Unit]
  conv_rhs =>
    rw [← Module.FaithfullyFlat.rTensor_exact_iff_exact R M (0 : Unit →ₗ[R] N) f]
  simp

/--
Local right-tensor surjectivity bridge used by the short-exact wrapper below.
-/
theorem faithfullyFlat_rTensor_surjective_iff_surjective
    [Module.FaithfullyFlat R M]
    {N N' : Type w} [AddCommGroup N] [AddCommGroup N'] [Module R N] [Module R N']
    (f : N →ₗ[R] N') :
    Function.Surjective (f.rTensor M) ↔ Function.Surjective f := by
  rw [← LinearMap.exact_zero_iff_surjective (TensorProduct R Unit M),
    ← LinearMap.exact_zero_iff_surjective Unit]
  conv_rhs =>
    rw [← Module.FaithfullyFlat.rTensor_exact_iff_exact R M f (0 : N' →ₗ[R] Unit)]
  simp

/--
The explicit short complex obtained by right-tensoring a short complex of
`R`-modules with `M`.
-/
abbrev rTensorShortComplex (S : ShortComplex (ModuleCat.{w} R)) :
    ShortComplex (ModuleCat.{max w v} R) :=
  ShortComplex.moduleCatMk (S.f.hom.rTensor M) (S.g.hom.rTensor M) (by
    rw [← LinearMap.rTensor_comp]
    have hfg : S.g.hom.comp S.f.hom = 0 := by
      ext x
      exact S.zero_apply x
    rw [hfg, LinearMap.rTensor_zero])

/--
Faithfully-flat right tensoring preserves and reflects short exactness of
short complexes in `ModuleCat`.
-/
theorem faithfullyFlat_rTensor_shortExact_iff_shortExact
    [Module.FaithfullyFlat R M] (S : ShortComplex (ModuleCat.{w} R)) :
    (rTensorShortComplex (M := M) S).ShortExact ↔ S.ShortExact := by
  constructor
  · intro hS
    exact ModuleCat.shortComplex_shortExact S
      ((Module.FaithfullyFlat.rTensor_exact_iff_exact R M S.f.hom S.g.hom).mp
        ((ShortComplex.ShortExact.moduleCat_exact_iff_function_exact
          (rTensorShortComplex (M := M) S)).mp hS.exact))
      ((faithfullyFlat_rTensor_injective_iff_injective (M := M) S.f.hom).mp
        (ShortComplex.ShortExact.moduleCat_injective_f hS))
      ((faithfullyFlat_rTensor_surjective_iff_surjective (M := M) S.g.hom).mp
        (ShortComplex.ShortExact.moduleCat_surjective_g hS))
  · intro hS
    exact ModuleCat.shortComplex_shortExact (rTensorShortComplex (M := M) S)
      ((Module.FaithfullyFlat.rTensor_exact_iff_exact R M S.f.hom S.g.hom).mpr
        ((ShortComplex.ShortExact.moduleCat_exact_iff_function_exact S).mp hS.exact))
      ((faithfullyFlat_rTensor_injective_iff_injective (M := M) S.f.hom).mpr
        (ShortComplex.ShortExact.moduleCat_injective_f hS))
      ((faithfullyFlat_rTensor_surjective_iff_surjective (M := M) S.g.hom).mpr
        (ShortComplex.ShortExact.moduleCat_surjective_g hS))

/--
Stage1 exactness-branch audit row.

`longExactPublicTarget` records whether this row should be treated as part of
the public terminal theorem target for THM-M-0011.  The local decision is that
the short-exact bridge is public Stage1 wrapper work, while long exact sequences
belong to a later derived/homological branch unless the public theorem is
explicitly strengthened beyond module-category flat descent.
-/
structure ExactnessBranchAnchor where
  declaration : String
  module : String
  sourceLine : Nat
  role : String
  repoLocalStatus : String
  localWrapper : String
  longExactPublicTarget : Bool
deriving Repr, DecidableEq

/--
Audit table for `THM-M-0011.exactness`.

The table records the checked short-exact bridge and the public-target decision
for the long-exact-sequence branch.
-/
def exactnessBranchAnchorTable : List ExactnessBranchAnchor :=
  [{ declaration := "Module.FaithfullyFlat.lTensor_exact_iff_exact",
     module := "Mathlib.RingTheory.Flat.FaithfullyFlat.Basic",
     sourceLine := 373,
     role := "Faithfully-flat left tensoring reflects and preserves exactness of the underlying linear maps.",
     repoLocalStatus := "local_wrapper_upstream_mathlib",
     localWrapper := "faithfullyFlat_lTensor_shortExact_iff_shortExact",
     longExactPublicTarget := false },
   { declaration := "Module.FaithfullyFlat.rTensor_exact_iff_exact",
     module := "Mathlib.RingTheory.Flat.FaithfullyFlat.Basic",
     sourceLine := 368,
     role := "Faithfully-flat right tensoring reflects and preserves exactness of the underlying linear maps.",
     repoLocalStatus := "local_wrapper_upstream_mathlib",
     localWrapper := "faithfullyFlat_rTensor_shortExact_iff_shortExact",
     longExactPublicTarget := false },
   { declaration := "ShortComplex.ShortExact.moduleCat_exact_iff_function_exact",
     module := "Mathlib.Algebra.Homology.ShortComplex.ModuleCat",
     sourceLine := 79,
     role := "Identifies `ShortComplex.Exact` in `ModuleCat` with `Function.Exact` of the underlying linear maps.",
     repoLocalStatus := "local_wrapper_upstream_mathlib",
     localWrapper := "faithfullyFlat_lTensor_shortExact_iff_shortExact / faithfullyFlat_rTensor_shortExact_iff_shortExact",
     longExactPublicTarget := false },
   { declaration := "ModuleCat.shortComplex_shortExact",
     module := "Mathlib.Algebra.Homology.ShortComplex.ModuleCat",
     sourceLine := 235,
     role := "Builds `ShortComplex.ShortExact` from `Function.Exact`, injectivity of the first map, and surjectivity of the second map.",
     repoLocalStatus := "local_wrapper_upstream_mathlib",
     localWrapper := "faithfullyFlat_lTensor_shortExact_iff_shortExact / faithfullyFlat_rTensor_shortExact_iff_shortExact",
     longExactPublicTarget := false },
   { declaration := "Module.FaithfullyFlat.lTensor_injective_iff_injective",
     module := "Mathlib.RingTheory.Flat.FaithfullyFlat.Basic",
     sourceLine := 383,
     role := "Faithfully-flat left tensoring reflects and preserves injectivity for the mono end of a short exact sequence.",
     repoLocalStatus := "local_wrapper_upstream_mathlib",
     localWrapper := "faithfullyFlat_lTensor_shortExact_iff_shortExact",
     longExactPublicTarget := false },
   { declaration := "Module.FaithfullyFlat.lTensor_surjective_iff_surjective",
     module := "Mathlib.RingTheory.Flat.FaithfullyFlat.Basic",
     sourceLine := 390,
     role := "Faithfully-flat left tensoring reflects and preserves surjectivity for the epi end of a short exact sequence.",
     repoLocalStatus := "local_wrapper_upstream_mathlib",
     localWrapper := "faithfullyFlat_lTensor_shortExact_iff_shortExact",
     longExactPublicTarget := false }]

/-- The exactness branch table contains the six checked short-exact bridge anchors. -/
theorem exactnessBranchAnchorTable_length :
    exactnessBranchAnchorTable.length = 6 := rfl

/--
Repo-local decision for the long-exact-sequence branch of `THM-M-0011`.

For the current public target, long exact sequences are not part of the terminal
flat-descent statement.  They should remain a later derived/homological
extension branch unless an integrator changes the theorem target explicitly.
-/
def longExactSequenceBranchIsPublicTarget : Bool :=
  false

end TensorShortExact

/--
Checked algebraic flat-descent wrapper: flatness of an `R`-module descends from
flatness of its tensor product over a faithfully flat `R`-algebra.
-/
theorem module_flat_of_flat_tensorProduct_faithfullyFlat
    {R : Type u} [CommRing R] {M : Type v} [AddCommGroup M] [Module R M]
    (S : Type w) [CommRing S] [Algebra R S] [Module.FaithfullyFlat R S]
    [Module.Flat S (TensorProduct R S M)] : Module.Flat R M :=
  Module.Flat.of_flat_tensorProduct R M S

/-- Checked iff form of flatness after faithfully flat scalar extension. -/
theorem module_flat_iff_flat_tensorProduct_faithfullyFlat
    {R : Type u} [CommRing R] {M : Type v} [AddCommGroup M] [Module R M]
    (S : Type w) [CommRing S] [Algebra R S] [Module.FaithfullyFlat R S] :
    Module.Flat S (TensorProduct R S M) ↔ Module.Flat R M :=
  Module.Flat.iff_flat_tensorProduct R M S

/--
The fpqc morphism-property cover class used by mathlib's scheme-level
`FlatDescent` file.

This is intentionally a scheme/morphism-property statement boundary.  It is a
useful public Stage1 wrapper family for THM-M-0011, but it is not a replacement
for the module-category effective-descent core above.
-/
abbrev schemeFpqcCoverProperty : MorphismProperty AlgebraicGeometry.Scheme.{u} :=
  @AlgebraicGeometry.Surjective ⊓ @AlgebraicGeometry.Flat ⊓
    @AlgebraicGeometry.QuasiCompact

/-- The fppf cover class reached from fpqc descent by the neighboring mathlib instance. -/
abbrev schemeFppfCoverProperty : MorphismProperty AlgebraicGeometry.Scheme.{u} :=
  @AlgebraicGeometry.Surjective ⊓ @AlgebraicGeometry.Flat ⊓
    @AlgebraicGeometry.LocallyOfFinitePresentation

/-- Checked wrapper: surjectivity satisfies fpqc descent. -/
theorem scheme_surjective_descendsAlong_fpqc :
    MorphismProperty.DescendsAlong (@AlgebraicGeometry.Surjective)
      schemeFpqcCoverProperty :=
  AlgebraicGeometry.Flat.surjective_descendsAlong_surjective_inf_flat_inf_quasicompact

/-- Checked wrapper: universal closedness satisfies fpqc descent. -/
theorem scheme_universallyClosed_descendsAlong_fpqc :
    MorphismProperty.DescendsAlong (@AlgebraicGeometry.UniversallyClosed)
      schemeFpqcCoverProperty :=
  AlgebraicGeometry.descendsAlong_universallyClosed_surjective_inf_flat_inf_quasicompact

/-- Checked wrapper: universal openness satisfies fpqc descent. -/
theorem scheme_universallyOpen_descendsAlong_fpqc :
    MorphismProperty.DescendsAlong (@AlgebraicGeometry.UniversallyOpen)
      schemeFpqcCoverProperty :=
  AlgebraicGeometry.descendsAlong_universallyOpen_surjective_inf_flat_inf_quasicompact

/-- Checked wrapper: universal injectivity satisfies fpqc descent. -/
theorem scheme_universallyInjective_descendsAlong_fpqc :
    MorphismProperty.DescendsAlong (@AlgebraicGeometry.UniversallyInjective)
      schemeFpqcCoverProperty :=
  AlgebraicGeometry.descendsAlong_universallyInjective_surjective_inf_flat_inf_quasicompact

/-- Checked wrapper: being an isomorphism of schemes satisfies fpqc descent. -/
theorem scheme_isomorphisms_descendsAlong_fpqc :
    MorphismProperty.DescendsAlong
      (MorphismProperty.isomorphisms AlgebraicGeometry.Scheme.{u})
      schemeFpqcCoverProperty :=
  AlgebraicGeometry.descendsAlong_isomorphisms_surjective_inf_flat_inf_quasicompact

/-- Checked wrapper: being an open immersion satisfies fpqc descent. -/
theorem scheme_isOpenImmersion_descendsAlong_fpqc :
    MorphismProperty.DescendsAlong (@AlgebraicGeometry.IsOpenImmersion)
      schemeFpqcCoverProperty :=
  AlgebraicGeometry.descendsAlong_isOpenImmersion_surjective_inf_flat_inf_quasicompact'

/--
Checked wrapper for the neighboring mathlib promotion: an fpqc-descent property
that is Zariski-local at the target also descends along the fppf cover class.
-/
theorem scheme_descendsAlong_fppf_of_fpqc
    (P : MorphismProperty AlgebraicGeometry.Scheme.{u})
    [P.DescendsAlong schemeFpqcCoverProperty]
    [AlgebraicGeometry.IsZariskiLocalAtTarget P] :
    P.DescendsAlong schemeFppfCoverProperty := by
  infer_instance

/-- Checked wrapper: fpqc pullback on over-categories is faithful. -/
theorem scheme_overPullback_faithful_of_surjective_flat_quasiCompact
    {X Y : AlgebraicGeometry.Scheme.{u}} (f : X ⟶ Y)
    [AlgebraicGeometry.Surjective f] [AlgebraicGeometry.Flat f]
    [AlgebraicGeometry.QuasiCompact f] :
    (Over.pullback f).Faithful := by
  infer_instance

/-- Checked wrapper: fppf pullback on over-categories is faithful. -/
theorem scheme_overPullback_faithful_of_surjective_flat_locallyOfFinitePresentation
    {X Y : AlgebraicGeometry.Scheme.{u}} (f : X ⟶ Y)
    [AlgebraicGeometry.Surjective f] [AlgebraicGeometry.Flat f]
    [AlgebraicGeometry.LocallyOfFinitePresentation f] :
    (Over.pullback f).Faithful := by
  infer_instance

section DescentDataNaturality

variable {C : Type u} [Category.{v} C]
variable (F : Pseudofunctor (LocallyDiscrete Cᵒᵖ) Cat.{w, x})
variable {ι : Type y} {S : C} {X : ι → C} (f : ∀ i, X i ⟶ S)

/--
The category of abstract descent data for a pseudofunctor and a family of maps.

This wrapper is the repo-local Stage1 surface for
`CategoryTheory.Pseudofunctor.DescentData`.
-/
abbrev descentDataCategory :=
  F.DescentData f

/--
The comparison functor sending an object over the base to its canonical descent
data along the covering family.

This is the local name for `CategoryTheory.Pseudofunctor.toDescentData`.
-/
abbrev descentDataComparisonFunctor :
    F.obj (.mk (Opposite.op S)) ⥤ F.DescentData f :=
  F.toDescentData f

/--
Concrete naturality square for descent data under a refinement/base-change
diagram.

The square records the checked natural isomorphism
`F.toDescentData f ⋙ pullFunctor F w ≅ (F.map p.op.toLoc).toFunctor ⋙
F.toDescentData f'`.  This is the package requested by
`THM-M-0011.descent-data`.
-/
structure DescentDataNaturalitySquare
    {S' : C} (p : S' ⟶ S) {ι' : Type z} {X' : ι' → C}
    (f' : ∀ j, X' j ⟶ S') {α : ι' → ι}
    (p' : ∀ j, X' j ⟶ X (α j))
    (w : ∀ j, p' j ≫ f (α j) = f' j ≫ p) where
  /-- The original descent-data comparison functor. -/
  top : F.obj (.mk (Opposite.op S)) ⥤ F.DescentData f
  /-- Pullback in the pseudofunctor from `S` to `S'`. -/
  left : F.obj (.mk (Opposite.op S)) ⥤ F.obj (.mk (Opposite.op S'))
  /-- Pullback/refinement functor on descent-data categories. -/
  right : F.DescentData f ⥤ F.DescentData f'
  /-- The refined descent-data comparison functor. -/
  bottom : F.obj (.mk (Opposite.op S')) ⥤ F.DescentData f'
  /-- The natural isomorphism expressing commutativity of the square. -/
  commIso : top ⋙ right ≅ left ⋙ bottom

/-- Constructor for the checked descent-data naturality square supplied by mathlib. -/
def descentDataNaturalitySquare
    {S' : C} (p : S' ⟶ S) {ι' : Type z} {X' : ι' → C}
    (f' : ∀ j, X' j ⟶ S') {α : ι' → ι}
    (p' : ∀ j, X' j ⟶ X (α j))
    (w : ∀ j, p' j ≫ f (α j) = f' j ≫ p) :
    DescentDataNaturalitySquare F f p f' p' w where
  top := F.toDescentData f
  left := (F.map p.op.toLoc).toFunctor
  right := Pseudofunctor.DescentData.pullFunctor F w
  bottom := F.toDescentData f'
  commIso := Pseudofunctor.DescentData.toDescentDataCompPullFunctorIso F w

@[simp]
theorem descentDataNaturalitySquare_top
    {S' : C} (p : S' ⟶ S) {ι' : Type z} {X' : ι' → C}
    (f' : ∀ j, X' j ⟶ S') {α : ι' → ι}
    (p' : ∀ j, X' j ⟶ X (α j))
    (w : ∀ j, p' j ≫ f (α j) = f' j ≫ p) :
    (descentDataNaturalitySquare F f p f' p' w).top = F.toDescentData f := rfl

@[simp]
theorem descentDataNaturalitySquare_left
    {S' : C} (p : S' ⟶ S) {ι' : Type z} {X' : ι' → C}
    (f' : ∀ j, X' j ⟶ S') {α : ι' → ι}
    (p' : ∀ j, X' j ⟶ X (α j))
    (w : ∀ j, p' j ≫ f (α j) = f' j ≫ p) :
    (descentDataNaturalitySquare F f p f' p' w).left =
      (F.map p.op.toLoc).toFunctor := rfl

@[simp]
theorem descentDataNaturalitySquare_right
    {S' : C} (p : S' ⟶ S) {ι' : Type z} {X' : ι' → C}
    (f' : ∀ j, X' j ⟶ S') {α : ι' → ι}
    (p' : ∀ j, X' j ⟶ X (α j))
    (w : ∀ j, p' j ≫ f (α j) = f' j ≫ p) :
    (descentDataNaturalitySquare F f p f' p' w).right =
      Pseudofunctor.DescentData.pullFunctor F w := rfl

@[simp]
theorem descentDataNaturalitySquare_bottom
    {S' : C} (p : S' ⟶ S) {ι' : Type z} {X' : ι' → C}
    (f' : ∀ j, X' j ⟶ S') {α : ι' → ι}
    (p' : ∀ j, X' j ⟶ X (α j))
    (w : ∀ j, p' j ≫ f (α j) = f' j ≫ p) :
    (descentDataNaturalitySquare F f p f' p' w).bottom = F.toDescentData f' := rfl

/--
Stack/effective-descent closure for the local comparison functor.

When the sieve generated by the family `f` is covering for `J`, mathlib's
`Pseudofunctor.isEquivalence_toDescentData` proves that the comparison functor
to descent data is an equivalence.
-/
theorem descentDataComparisonFunctor_isEquivalence_of_isStack
    {J : GrothendieckTopology C} [F.IsStack J]
    (hf : Sieve.ofArrows _ f ∈ J S) :
    (descentDataComparisonFunctor F f).IsEquivalence :=
  Pseudofunctor.isEquivalence_toDescentData F f hf

end DescentDataNaturality

/-- Audit row for the abstract descent-data package used by the Stage1 boundary. -/
structure DescentDataAnchor where
  declaration : String
  module : String
  sourceLine : Nat
  role : String
  repoLocalStatus : String
  localWrapper : String
deriving Repr, DecidableEq

/--
Mathlib anchor table for `THM-M-0011.descent-data`.

The table separates the category of descent data, the comparison functor, the
naturality square, and the stack/effective-descent equivalence gate.
-/
def descentDataAnchorTable : List DescentDataAnchor :=
  [{ declaration := "CategoryTheory.Pseudofunctor.DescentData",
     module := "Mathlib.CategoryTheory.Sites.Descent.DescentData",
     sourceLine := 57,
     role := "Category of descent data for a pseudofunctor along a family of arrows.",
     repoLocalStatus := "local_wrapper_upstream_mathlib",
     localWrapper := "descentDataCategory" },
   { declaration := "CategoryTheory.Pseudofunctor.toDescentData",
     module := "Mathlib.CategoryTheory.Sites.Descent.DescentData",
     sourceLine := 165,
     role := "Comparison functor from objects over the base to canonical descent data.",
     repoLocalStatus := "local_wrapper_upstream_mathlib",
     localWrapper := "descentDataComparisonFunctor" },
   { declaration := "CategoryTheory.Pseudofunctor.DescentData.toDescentDataCompPullFunctorIso",
     module := "Mathlib.CategoryTheory.Sites.Descent.DescentData",
     sourceLine := 264,
     role := "Naturality-square isomorphism for comparison functors and pullback of descent data.",
     repoLocalStatus := "local_wrapper_upstream_mathlib",
     localWrapper := "descentDataNaturalitySquare" },
   { declaration := "CategoryTheory.Pseudofunctor.isEquivalence_toDescentData",
     module := "Mathlib.CategoryTheory.Sites.Descent.IsStack",
     sourceLine := 70,
     role := "Effective descent gate: covering descent data comparison is an equivalence for stacks.",
     repoLocalStatus := "local_wrapper_upstream_mathlib",
     localWrapper := "descentDataComparisonFunctor_isEquivalence_of_isStack" }]

/-- The descent-data package contains the four requested mathlib anchors. -/
theorem descentDataAnchorTable_length : descentDataAnchorTable.length = 4 := rfl

/-- Pinned mathlib revision used by the Stage1 flat-descent anchor audit. -/
def mathlibAnchorRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Audit row for mathlib anchors used by the Stage1 flat-descent boundary. -/
structure MathlibAnchor where
  declaration : String
  module : String
  sourceLine : Nat
  role : String
  repoLocalStatus : String
  localWrapper : String
deriving Repr, DecidableEq

/--
Mathlib anchor table for `THM-M-0011.mathlib`.

The declaration names in this table are also checked below with `#check`.  The
table records the pinned source location and the repo-local wrapper that keeps
the anchor inside this repository's Lean validation closure.
-/
def mathlibAnchorTable : List MathlibAnchor :=
  [{ declaration := "ModuleCat.preservesFiniteLimits_extendScalars_of_flat",
     module := "Mathlib.Algebra.Category.ModuleCat.Descent",
     sourceLine := 42,
     role := "Flat scalar extension preserves finite limits in ModuleCat.",
     repoLocalStatus := "local_wrapper_upstream_mathlib",
     localWrapper := "moduleCategoryDescentShape_of_faithfullyFlat" },
   { declaration := "ModuleCat.reflectsIsomorphisms_extendScalars_of_faithfullyFlat",
     module := "Mathlib.Algebra.Category.ModuleCat.Descent",
     sourceLine := 49,
     role := "Faithfully-flat scalar extension reflects isomorphisms in ModuleCat.",
     repoLocalStatus := "local_wrapper_upstream_mathlib",
     localWrapper := "moduleCategoryDescentShape_of_faithfullyFlat" },
   { declaration := "comonadicExtendScalars",
     module := "Mathlib.Algebra.Category.ModuleCat.Descent",
     sourceLine := 59,
     role := "Faithfully-flat scalar extension is a comonadic left adjoint.",
     repoLocalStatus := "local_wrapper_upstream_mathlib",
     localWrapper := "moduleCategoryDescentShape_of_faithfullyFlat" },
   { declaration := "Module.FaithfullyFlat.lTensor_exact_iff_exact",
     module := "Mathlib.RingTheory.Flat.FaithfullyFlat.Basic",
     sourceLine := 373,
     role := "Left tensoring with a faithfully flat module reflects exactness.",
     repoLocalStatus := "local_wrapper_upstream_mathlib",
     localWrapper := "faithfullyFlat_lTensor_exact_iff_exact" },
   { declaration := "Module.FaithfullyFlat.rTensor_exact_iff_exact",
     module := "Mathlib.RingTheory.Flat.FaithfullyFlat.Basic",
     sourceLine := 368,
     role := "Right tensoring with a faithfully flat module reflects exactness.",
     repoLocalStatus := "local_wrapper_upstream_mathlib",
     localWrapper := "faithfullyFlat_rTensor_exact_iff_exact" },
   { declaration := "Module.Flat.of_flat_tensorProduct",
     module := "Mathlib.RingTheory.Flat.FaithfullyFlat.Basic",
     sourceLine := 586,
     role := "Flatness descends from a tensor product over a faithfully flat algebra.",
     repoLocalStatus := "local_wrapper_upstream_mathlib",
     localWrapper := "module_flat_of_flat_tensorProduct_faithfullyFlat" },
   { declaration := "Module.Flat.iff_flat_tensorProduct",
     module := "Mathlib.RingTheory.Flat.FaithfullyFlat.Basic",
     sourceLine := 599,
     role := "Flatness is equivalent before and after faithfully flat scalar extension.",
     repoLocalStatus := "local_wrapper_upstream_mathlib",
     localWrapper := "module_flat_iff_flat_tensorProduct_faithfullyFlat" }]

/-- The `THM-M-0011.mathlib` backfill table contains exactly the requested anchors. -/
theorem mathlibAnchorTable_length : mathlibAnchorTable.length = 7 := rfl

/--
Audit row for the scheme-level `FlatDescent` wrapper family.

The rows below answer `THM-M-0011.scheme`: the named fpqc morphism-property
descent instances are worth exposing as public Stage1 wrappers, while the
generic fppf promotion and over-pullback faithfulness instances should be
presented as neighboring support rather than as the terminal flat descent
theorem.
-/
structure SchemeFlatDescentAnchor where
  declaration : String
  sourceLine : Nat
  wrapper : String
  publicRole : String
  exposureDecision : String
deriving Repr, DecidableEq

/-- Integration-ready audit table for `Mathlib.AlgebraicGeometry.Morphisms.FlatDescent`. -/
def schemeFlatDescentAnchorTable : List SchemeFlatDescentAnchor :=
  [{ declaration :=
       "AlgebraicGeometry.Flat.surjective_descendsAlong_surjective_inf_flat_inf_quasicompact",
     sourceLine := 40,
     wrapper := "scheme_surjective_descendsAlong_fpqc",
     publicRole := "Surjectivity descends along surjective flat quasi-compact covers.",
     exposureDecision := "public_stage1_wrapper" },
   { declaration :=
       "AlgebraicGeometry.descendsAlong_universallyClosed_surjective_inf_flat_inf_quasicompact",
     sourceLine := 46,
     wrapper := "scheme_universallyClosed_descendsAlong_fpqc",
     publicRole := "Universal closedness descends along surjective flat quasi-compact covers.",
     exposureDecision := "public_stage1_wrapper" },
   { declaration :=
       "AlgebraicGeometry.descendsAlong_universallyOpen_surjective_inf_flat_inf_quasicompact",
     sourceLine := 63,
     wrapper := "scheme_universallyOpen_descendsAlong_fpqc",
     publicRole := "Universal openness descends along surjective flat quasi-compact covers.",
     exposureDecision := "public_stage1_wrapper" },
   { declaration :=
       "AlgebraicGeometry.descendsAlong_universallyInjective_surjective_inf_flat_inf_quasicompact",
     sourceLine := 81,
     wrapper := "scheme_universallyInjective_descendsAlong_fpqc",
     publicRole := "Universal injectivity descends along surjective flat quasi-compact covers.",
     exposureDecision := "public_stage1_wrapper" },
   { declaration :=
       "AlgebraicGeometry.descendsAlong_isomorphisms_surjective_inf_flat_inf_quasicompact",
     sourceLine := 88,
     wrapper := "scheme_isomorphisms_descendsAlong_fpqc",
     publicRole := "Being an isomorphism descends along surjective flat quasi-compact covers.",
     exposureDecision := "public_stage1_wrapper" },
   { declaration :=
       "AlgebraicGeometry.descendsAlong_isOpenImmersion_surjective_inf_flat_inf_quasicompact'",
     sourceLine := 127,
     wrapper := "scheme_isOpenImmersion_descendsAlong_fpqc",
     publicRole := "Being an open immersion descends along surjective flat quasi-compact covers.",
     exposureDecision := "public_stage1_wrapper" },
   { declaration :=
       "AlgebraicGeometry.instDescendsAlongSurjectiveFlatLocallyOfFinitePresentation",
     sourceLine := 157,
     wrapper := "scheme_descendsAlong_fppf_of_fpqc",
     publicRole := "Promotes Zariski-local-at-target fpqc descent to fppf descent.",
     exposureDecision := "supporting_neighbor_wrapper" },
   { declaration :=
       "AlgebraicGeometry.instFaithfulOverPullbackOfSurjectiveFlatQuasiCompact",
     sourceLine := 171,
     wrapper := "scheme_overPullback_faithful_of_surjective_flat_quasiCompact",
     publicRole := "Pullback along a surjective flat quasi-compact morphism is faithful on over-categories.",
     exposureDecision := "supporting_neighbor_wrapper" },
   { declaration :=
       "AlgebraicGeometry.instFaithfulOverPullbackOfSurjectiveFlatLocallyOfFinitePresentation",
     sourceLine := 177,
     wrapper := "scheme_overPullback_faithful_of_surjective_flat_locallyOfFinitePresentation",
     publicRole := "Pullback along a surjective flat locally finitely presented morphism is faithful on over-categories.",
     exposureDecision := "supporting_neighbor_wrapper" }]

/-- The scheme-level `FlatDescent` audit exposes six direct wrappers and three neighbors. -/
theorem schemeFlatDescentAnchorTable_length :
    schemeFlatDescentAnchorTable.length = 9 := rfl

/--
Search terms used for the Stage1 audit.  These are data, not proof assumptions.
-/
def mathlibAuditSearchTerms : List String :=
  ["flat descent", "faithfully flat descent", "flat base change",
    "ModuleCat Descent", "FlatDescent", "DescentData", "IsStack",
    "short exact flat tensor", "long exact sequence flat base change"]

/--
Audit row for `THM-M-0011.integration-gate`.

Rows in this table are external non-mathlib Lean 4 anchors found during the
Stage1 audit.  They are data only: no row counts as repo-local closure unless a
separate integrator patch pins/imports/checks the external project or vendors a
compatible proof body into this repository.
-/
structure ExternalIntegrationGateAnchor where
  repository : String
  commit : String
  module : String
  theoremName : String
  sourceLine : Nat
  leanToolchain : String
  mathlibInputRev : String
  mathlibCommit : String
  mathematicalScope : String
  terminalForTHM_M_0011 : Bool
  repoLocalStatus : String
  proposedValidationCommand : String
  integrationBlocker : String
deriving Repr, DecidableEq

/--
External-anchor audit for `THM-M-0011.integration-gate`.

The Liran Shaul project proves faithfully flat descent of projectivity, a
substantial projectivity-descent branch.  It is not the terminal all-branches
flat descent theorem tracked by this Stage1 parent, and it is not currently
inside this repository's pinned Lean validation closure.
-/
def externalIntegrationGateAnchorTable : List ExternalIntegrationGateAnchor :=
  [{ repository := "https://github.com/LiranShaul/lean-faithfully-flat-descent",
     commit := "f5967aab9067290aed1b7113569c1b9024a9fca4",
     module := "basechange",
     theoremName := "proj_faithfully_flat",
     sourceLine := 2325,
     leanToolchain := "leanprover/lean4:v4.26.0-rc2",
     mathlibInputRev := "v4.26.0-rc2",
     mathlibCommit := "d5c9558e75342a10d6321e6a8c798a14f68ae23c",
     mathematicalScope :=
       "Faithfully flat descent of projectivity: Module.Projective R P iff Module.Projective S (TensorProduct R S P).",
     terminalForTHM_M_0011 := false,
     repoLocalStatus := "external_upstream_anchor_only_nonterminal_branch",
     proposedValidationCommand :=
       "git clone https://github.com/LiranShaul/lean-faithfully-flat-descent.git && cd lean-faithfully-flat-descent && git checkout f5967aab9067290aed1b7113569c1b9024a9fca4 && lake env lean basechange.lean",
     integrationBlocker :=
       "External project uses Lean 4.26.0-rc2 and mathlib d5c9558e75342a10d6321e6a8c798a14f68ae23c, while this repo pins Lean 4.29.0 and mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95; it needs a separate pinned dependency, compatibility port, or vendored proof-body plan.  It is also a projectivity-descent branch, not the terminal flat descent theorem." }]

/-- One non-mathlib external Lean 4 anchor was found, and it is non-terminal. -/
theorem externalIntegrationGateAnchorTable_length :
    externalIntegrationGateAnchorTable.length = 1 := rfl

#check ModuleCat.preservesFiniteLimits_extendScalars_of_flat
#check ModuleCat.reflectsIsomorphisms_extendScalars_of_faithfullyFlat
#check comonadicExtendScalars
#check Module.FaithfullyFlat.lTensor_exact_iff_exact
#check Module.FaithfullyFlat.rTensor_exact_iff_exact
#check ShortComplex.ShortExact.moduleCat_exact_iff_function_exact
#check ModuleCat.shortComplex_shortExact
#check lTensorShortComplex
#check faithfullyFlat_lTensor_shortExact_iff_shortExact
#check faithfullyFlat_rTensor_injective_iff_injective
#check faithfullyFlat_rTensor_surjective_iff_surjective
#check rTensorShortComplex
#check faithfullyFlat_rTensor_shortExact_iff_shortExact
#check exactnessBranchAnchorTable
#check exactnessBranchAnchorTable_length
#check longExactSequenceBranchIsPublicTarget
#check Module.Flat.of_flat_tensorProduct
#check Module.Flat.iff_flat_tensorProduct
#check RingHom.FaithfullyFlat.codescendsAlong_bijective
#check AlgebraicGeometry.Flat.surjective_descendsAlong_surjective_inf_flat_inf_quasicompact
#check AlgebraicGeometry.descendsAlong_universallyClosed_surjective_inf_flat_inf_quasicompact
#check AlgebraicGeometry.descendsAlong_universallyOpen_surjective_inf_flat_inf_quasicompact
#check AlgebraicGeometry.descendsAlong_universallyInjective_surjective_inf_flat_inf_quasicompact
#check AlgebraicGeometry.descendsAlong_isomorphisms_surjective_inf_flat_inf_quasicompact
#check AlgebraicGeometry.descendsAlong_isOpenImmersion_surjective_inf_flat_inf_quasicompact'
#check CategoryTheory.Pseudofunctor.DescentData
#check CategoryTheory.Pseudofunctor.toDescentData
#check CategoryTheory.Pseudofunctor.isEquivalence_toDescentData
#check StatementShape
#check statementShape_current_moduleCategory_boundary
#check mathlibAnchorRevision
#check mathlibAnchorTable
#check mathlibAnchorTable_length
#check schemeFpqcCoverProperty
#check schemeFppfCoverProperty
#check scheme_surjective_descendsAlong_fpqc
#check scheme_universallyClosed_descendsAlong_fpqc
#check scheme_universallyOpen_descendsAlong_fpqc
#check scheme_universallyInjective_descendsAlong_fpqc
#check scheme_isomorphisms_descendsAlong_fpqc
#check scheme_isOpenImmersion_descendsAlong_fpqc
#check scheme_descendsAlong_fppf_of_fpqc
#check scheme_overPullback_faithful_of_surjective_flat_quasiCompact
#check scheme_overPullback_faithful_of_surjective_flat_locallyOfFinitePresentation
#check schemeFlatDescentAnchorTable
#check schemeFlatDescentAnchorTable_length
#check descentDataCategory
#check descentDataComparisonFunctor
#check DescentDataNaturalitySquare
#check descentDataNaturalitySquare
#check descentDataComparisonFunctor_isEquivalence_of_isStack
#check descentDataAnchorTable
#check descentDataAnchorTable_length
#check externalIntegrationGateAnchorTable
#check externalIntegrationGateAnchorTable_length

end S1_M_104
end Stage1
end AwesomeTheorems
