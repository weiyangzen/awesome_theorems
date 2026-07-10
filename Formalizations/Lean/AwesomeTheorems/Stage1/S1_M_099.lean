import Mathlib.Algebra.Homology.HomologySequenceLemmas
import Mathlib.Algebra.Homology.Bifunctor
import Mathlib.CategoryTheory.Monoidal.Tor
import Mathlib.Algebra.Homology.DerivedCategory.Ext.Basic
import Mathlib.Algebra.Homology.DerivedCategory.SmallShiftedHom

/-!
# Stage1 statement shape for S1-M-099 / THM-M-0004

This file records a conservative Lean 4 boundary for the universal coefficient
theorem.  The present mathlib checkout provides homological complexes, homology
functors, short exact complexes, long exact sequence naturality, bifunctorial
total complexes, monoidal-category `Tor`, and `Ext` groups in abelian
categories.  This file does not claim a proof of the classical universal
coefficient theorem; the tensor, `Tor`, `Hom`, and `Ext` comparison terms are
kept as explicit output data until a later integrator pins the exact object
model and proof body.

## Mathlib anchor audit at revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`

| anchor | mathlib module | role for a future UCT formalization | repo-local status |
|---|---|---|---|
| `HomologicalComplex.homologyFunctor` | `Mathlib.Algebra.Homology.ShortComplex.HomologicalComplex` | functorial homology in a fixed degree | checked by this file |
| `HomologicalComplex.homologyMap` | `Mathlib.Algebra.Homology.ShortComplex.HomologicalComplex` | maps induced on homology by chain maps | checked by this file |
| `HomologicalComplex.HomologySequence.δ_naturality` | `Mathlib.Algebra.Homology.HomologySequenceLemmas` | naturality of long-exact-sequence boundary morphisms | checked by this file |
| `ShortComplex.ShortExact` | `Mathlib.Algebra.Homology.ShortComplex.ShortExact` | short exact complex API for the UCT output shape | checked by this file |
| `Functor.mapBifunctorHomologicalComplex` | `Mathlib.Algebra.Homology.Bifunctor` | bifunctorial double/total complex substrate for tensor-like constructions | checked by this file |
| `Functor.map₂HomologicalComplex` | `Mathlib.Algebra.Homology.Bifunctor` | binary functor lift to homological complexes | checked by this file |
| `CategoryTheory.Tor` | `Mathlib.CategoryTheory.Monoidal.Tor` | left-derived tensor endpoint for the homological branch | checked by this file |
| `CategoryTheory.isZero_Tor_succ_of_projective` | `Mathlib.CategoryTheory.Monoidal.Tor` | projective-coefficient vanishing probe for higher `Tor` | checked by this file |
| `Abelian.Ext` | `Mathlib.Algebra.Homology.DerivedCategory.Ext.Basic` | Ext endpoint for the cohomological branch | checked by this file |
| `Abelian.Ext.addEquiv₀` | `Mathlib.Algebra.Homology.DerivedCategory.Ext.Basic` | zero-degree Ext comparison with morphisms | checked by this file |

This table is only a mathlib substrate audit.  It identifies tensor and `Tor`
APIs, but it does not close the terminal universal coefficient theorem.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits CategoryTheory.Localization

universe u v uι w uι₁ uι₂ uJ

namespace Stage1.THMM0004

/--
Input data for a universal-coefficient-theorem statement in a category with
homology.

The hypothesis fields deliberately remain abstract.  A later integrator should
instantiate them with the chosen category-level, homology, abelian-category,
complex-shape, chain-complex boundedness/projectivity/flatness, coefficient,
and universe assumptions for the homology or cohomology version being
formalized.
-/
structure UniversalCoefficientInput (C : Type u) [Category.{v} C] [HasZeroMorphisms C] where
  ι : Type uι
  c : ComplexShape ι
  K : HomologicalComplex C c
  coefficient : C
  categoryHypotheses : Prop
  homologyHypotheses : Prop
  abelianCategoryHypotheses : Prop
  complexShapeHypotheses : Prop
  chainComplexHypotheses : Prop
  coefficientHypotheses : Prop

/--
The explicit assumption bundle required by the Stage1 statement shape.

The category, homology, and abelian-category constraints are also present as
Lean typeclass assumptions in `StatementShape`; these propositional fields are
where a later proof pass can record extra side conditions such as enough
projectives/injectives, chosen resolutions, boundedness, flatness, or universe
compatibility without changing the statement skeleton.
-/
def UniversalCoefficientInput.Assumptions {C : Type u} [Category.{v} C] [HasZeroMorphisms C]
    (D : UniversalCoefficientInput.{u, v, uι} C) : Prop :=
  D.categoryHypotheses ∧
  D.homologyHypotheses ∧
  D.abelianCategoryHypotheses ∧
  D.complexShapeHypotheses ∧
  D.chainComplexHypotheses ∧
  D.coefficientHypotheses

/--
Output contract for a universal coefficient package.

The fields separate the homological short exact sequence
`0 -> H(K) ⊗ A -> H(K ⊗ A) -> Tor(H(K[-1]), A) -> 0` from the cohomological
short exact sequence involving `Ext` and `Hom`.  They are intentionally encoded
as category-level terms and short complexes rather than as a false terminal
proof, because the UCT comparison maps, exactness proof, and coefficient model
are not constructed in this audit.
-/
structure UniversalCoefficientOutput (C : Type u) [Category.{v} C] [HasZeroMorphisms C]
    (D : UniversalCoefficientInput.{u, v, uι} C) where
  tensorHomologyTerm : D.ι → C
  tensorComplexHomologyTerm : D.ι → C
  torCorrectionTerm : D.ι → C
  homTerm : D.ι → C
  cohomologyTerm : D.ι → C
  extCorrectionTerm : D.ι → C
  homologicalUCTSequence : D.ι → ShortComplex C
  cohomologicalUCTSequence : D.ι → ShortComplex C
  homologicalUCTShortExact : ∀ i, (homologicalUCTSequence i).ShortExact
  cohomologicalUCTShortExact : ∀ i, (cohomologicalUCTSequence i).ShortExact
  naturalitySquare : D.ι → Prop
  naturalitySquare_holds : ∀ i, naturalitySquare i
  termIdentifications : Prop
  termIdentifications_holds : termIdentifications

/--
Statement-shape candidate for the universal coefficient theorem.

For every suitable chain complex and coefficient object in an abelian category
with homology, there should be a package of natural short exact universal
coefficient sequences with the expected tensor/Tor and Hom/Ext terms.
-/
def StatementShape : Prop :=
  ∀ (C : Type u) [Category.{v} C] [HasZeroMorphisms C] [CategoryWithHomology C] [Abelian C],
    ∀ D : UniversalCoefficientInput.{u, v, uι} C,
      D.Assumptions →
      Nonempty (UniversalCoefficientOutput.{u, v, uι} C D)

/--
Final tensor API selected for the homological UCT branch.

The tensor product is the monoidal-category tensor, exposed as the curried
binary functor `MonoidalCategory.curriedTensor C`.  Chain-level tensor products
should be built from this functor through mathlib's homological bifunctor API
below, not through an ad hoc object-level encoding.
-/
def selectedTensorBifunctor (C : Type u) [Category.{v} C] [MonoidalCategory C] :
    C ⥤ (C ⥤ C) :=
  MonoidalCategory.curriedTensor C

/--
Selected `Tor` API for the homological UCT branch.

mathlib defines `CategoryTheory.Tor C n` as the left-derived functor of tensoring
in the second variable.  This is now a concrete API endpoint in the pinned
mathlib checkout, not an absent placeholder.
-/
noncomputable def selectedTorBifunctor (C : Type u) [Category.{v} C]
    [MonoidalCategory C] [Abelian C] [MonoidalPreadditive C] [HasProjectiveResolutions C]
    (n : ℕ) : C ⥤ C ⥤ C :=
  CategoryTheory.Tor C n

/--
Selected alternate `Tor` API deriving in the first variable.

mathlib names this endpoint `CategoryTheory.Tor'`; the pinned API notes that
the natural comparison with `Tor` remains future theory.
-/
noncomputable def selectedTorLeftVariant (C : Type u) [Category.{v} C]
    [MonoidalCategory C] [Abelian C] [MonoidalPreadditive C] [HasProjectiveResolutions C]
    (n : ℕ) : C ⥤ C ⥤ C :=
  CategoryTheory.Tor' C n

/--
Selected tensor API lifted to bicomplexes.

The zero-morphism preservation hypotheses are left explicit because they are
part of the eventual coefficient/category assumptions for a terminal UCT
statement.
-/
def selectedTensorBicomplexFunctor {C : Type u} [Category.{v} C] [HasZeroMorphisms C]
    [MonoidalCategory C]
    [tensorPreservesZero : (selectedTensorBifunctor C).PreservesZeroMorphisms]
    [tensorObjPreservesZero : ∀ X, ((selectedTensorBifunctor C).obj X).PreservesZeroMorphisms]
    {ι₁ : Type uι₁} {ι₂ : Type uι₂} (c₁ : ComplexShape ι₁) (c₂ : ComplexShape ι₂) :
    HomologicalComplex C c₁ ⥤
      (HomologicalComplex C c₂ ⥤ HomologicalComplex₂ C c₁ c₂) :=
  (selectedTensorBifunctor C).mapBifunctorHomologicalComplex c₁ c₂

/--
Selected tensor API lifted to total complexes.

This is the final chain-level tensor target for the homological UCT branch once
the concrete total-complex shape and totalization hypotheses are supplied.
-/
def selectedTensorTotalComplexFunctor {C : Type u} [Category.{v} C] [Preadditive C]
    [MonoidalCategory C]
    [tensorPreservesZero : (selectedTensorBifunctor C).PreservesZeroMorphisms]
    [tensorObjPreservesZero : ∀ X, ((selectedTensorBifunctor C).obj X).PreservesZeroMorphisms]
    {ι₁ : Type uι₁} {ι₂ : Type uι₂} {J : Type uJ}
    (c₁ : ComplexShape ι₁) (c₂ : ComplexShape ι₂) (c : ComplexShape J)
    [DecidableEq J] [TotalComplexShape c₁ c₂ c]
    [∀ (K₁ : HomologicalComplex C c₁) (K₂ : HomologicalComplex C c₂),
      ((((selectedTensorBifunctor C).mapBifunctorHomologicalComplex c₁ c₂).obj K₁).obj K₂).HasTotal c] :
    HomologicalComplex C c₁ ⥤
      (HomologicalComplex C c₂ ⥤ HomologicalComplex C c) :=
  (selectedTensorBifunctor C).map₂HomologicalComplex c₁ c₂ c

/--
Repo-local gate for the homological tensor/Tor API selection.

Tensor is selected as `selectedTensorBifunctor`; `Tor` is selected as
`selectedTorBifunctor`, mathlib's left-derived functor of tensoring in the
second variable.  This still does not prove the homological UCT sequence: the
remaining terminal blocker is the comparison/exactness theorem connecting
homology of the tensor total complex with the selected `Tor` endpoint.
-/
structure HomologicalTensorTorAPIBoundary (C : Type u) [Category.{v} C]
    [MonoidalCategory C] [Abelian C] [MonoidalPreadditive C] [HasProjectiveResolutions C] where
  tensorBifunctor : C ⥤ (C ⥤ C)
  tensorBifunctor_eq_selected : tensorBifunctor = selectedTensorBifunctor C
  torBifunctor : ℕ → C ⥤ C ⥤ C
  torBifunctor_eq_selected : torBifunctor = selectedTorBifunctor C
  torLeftVariant : ℕ → C ⥤ C ⥤ C
  torLeftVariant_eq_selected : torLeftVariant = selectedTorLeftVariant C
  higherTorVanishesOnProjectiveCoefficients : ∀ X Y : C, ∀ [Projective Y], ∀ n : ℕ,
    IsZero (((torBifunctor (n + 1)).obj X).obj Y)
  terminalUCTBlockedUntilTorComparisonSequence : Prop
  terminalUCTBlockedUntilTorComparisonSequence_holds :
    terminalUCTBlockedUntilTorComparisonSequence

/-- The selected homological tensor/Tor API boundary for this Stage1 artifact. -/
noncomputable def selectedHomologicalTensorTorAPIBoundary (C : Type u) [Category.{v} C]
    [MonoidalCategory C] [Abelian C] [MonoidalPreadditive C] [HasProjectiveResolutions C] :
    HomologicalTensorTorAPIBoundary C where
  tensorBifunctor := selectedTensorBifunctor C
  tensorBifunctor_eq_selected := rfl
  torBifunctor := selectedTorBifunctor C
  torBifunctor_eq_selected := rfl
  torLeftVariant := selectedTorLeftVariant C
  torLeftVariant_eq_selected := rfl
  higherTorVanishesOnProjectiveCoefficients := fun X Y _ n =>
    CategoryTheory.isZero_Tor_succ_of_projective C X Y n
  terminalUCTBlockedUntilTorComparisonSequence := True
  terminalUCTBlockedUntilTorComparisonSequence_holds := trivial

/--
Machine-checkable gate: this file has selected the tensor and `Tor` APIs and
records the UCT comparison/exactness theorem as the remaining repo-local
formalization debt.
-/
def HomologicalTensorTorAPIGate : Prop :=
  ∀ (C : Type u) [Category.{v} C] [MonoidalCategory C] [Abelian C]
    [MonoidalPreadditive C] [HasProjectiveResolutions C],
    Nonempty (HomologicalTensorTorAPIBoundary C)

/-- The tensor/Tor API gate is closed only as an API-boundary selection. -/
theorem homologicalTensorTorAPIGate_checked : HomologicalTensorTorAPIGate := by
  intro C _ _ _ _ _
  exact ⟨selectedHomologicalTensorTorAPIBoundary C⟩

/-- A short exact complex exposes its exactness field in mathlib. -/
theorem shortExact_exact {C : Type u} [Category.{v} C] [HasZeroMorphisms C]
    {S : ShortComplex C} (hS : S.ShortExact) : S.Exact :=
  hS.exact

/-- mathlib substrate probe: homology objects are available when `HasHomology` is available. -/
theorem homology_object_available {C : Type u} [Category.{v} C] [HasZeroMorphisms C]
    [CategoryWithHomology C] {ι : Type uι} {c : ComplexShape ι}
    (K : HomologicalComplex C c) (i : ι) [K.HasHomology i] :
    Nonempty C :=
  ⟨K.homology i⟩

/-- mathlib substrate wrapper for the homology functor at a fixed degree. -/
def homologyFunctorWrapper {C : Type u} [Category.{v} C] [HasZeroMorphisms C]
    [CategoryWithHomology C] {ι : Type uι} (c : ComplexShape ι) (i : ι) :
    HomologicalComplex C c ⥤ C :=
  HomologicalComplex.homologyFunctor C c i

/--
Stage1 probe for the `Ext^0` endpoint used by cohomological universal
coefficient statements.  mathlib has `Abelian.Ext` and the zero-degree
comparison `Abelian.Ext.addEquiv₀`, but this artifact does not identify it with
the full universal coefficient sequence.
-/
def extZeroStatementShape {C : Type u} [Category.{v} C] [Abelian C] [HasExt.{w} C]
    (X Y : C) : Type w :=
  Abelian.Ext X Y 0

/--
Selected Hom-complex cohomology API for the cohomological UCT branch.

mathlib's `HomComplex.CohomologyClass K L n` is the repo-local endpoint for
the cohomology of the Hom complex between two `ℤ`-indexed cochain complexes.
This is stronger than an anchor-only reference: the type is imported and used
below to construct an `Abelian.Ext` endpoint for single complexes.
-/
abbrev selectedHomComplexCohomology {C : Type u} [Category.{v} C] [Preadditive C]
    (K L : CochainComplex C ℤ) (n : ℤ) : Type v :=
  CochainComplex.HomComplex.CohomologyClass K L n

/--
Selected Ext endpoint API for the cohomological UCT branch.

The endpoint is exactly mathlib's `Abelian.Ext`, not a local placeholder.
-/
abbrev selectedExtEndpoint {C : Type u} [Category.{v} C] [Abelian C] [HasExt.{w} C]
    (X Y : C) (n : ℕ) : Type w :=
  Abelian.Ext X Y n

/-- The zero-degree selected Ext endpoint is additively equivalent to morphisms. -/
noncomputable def extEndpointAddEquivZero {C : Type u} [Category.{v} C] [Abelian C]
    [HasExt.{w} C] (X Y : C) : selectedExtEndpoint X Y 0 ≃+ (X ⟶ Y) :=
  Abelian.Ext.addEquiv₀

/-- The inverse of the zero-degree endpoint equivalence is `Abelian.Ext.mk₀`. -/
theorem extEndpointAddEquivZero_mk₀ {C : Type u} [Category.{v} C] [Abelian C]
    [HasExt.{w} C] {X Y : C} (f : X ⟶ Y) :
    (extEndpointAddEquivZero X Y).symm f = Abelian.Ext.mk₀ f :=
  Abelian.Ext.addEquiv₀_symm_apply f

/-- The selected zero-degree Ext endpoint sends `Abelian.Ext.mk₀ f` back to `f`. -/
theorem extEndpointAddEquivZero_apply_mk₀ {C : Type u} [Category.{v} C] [Abelian C]
    [HasExt.{w} C] {X Y : C} (f : X ⟶ Y) :
    extEndpointAddEquivZero X Y (Abelian.Ext.mk₀ f) = f := by
  rw [← extEndpointAddEquivZero_mk₀ f]
  exact (extEndpointAddEquivZero X Y).right_inv f

/--
Connection from Hom-complex cohomology classes of single complexes to the
selected `Abelian.Ext` endpoint.

This is the concrete repo-local bridge currently available in mathlib:
cohomology classes in the Hom complex map to the small shifted Hom type whose
definition is used by `Abelian.Ext`.
-/
noncomputable def homComplexCohomologyClassToExt {C : Type u} [Category.{v} C]
    [Abelian C] [HasExt.{w} C] (X Y : C) (n : ℕ) :
    selectedHomComplexCohomology ((CochainComplex.singleFunctor C 0).obj X)
      ((CochainComplex.singleFunctor C 0).obj Y) (n : ℤ) → selectedExtEndpoint X Y n :=
  fun x => x.toSmallShiftedHom

/-- On cocycle representatives, the Hom-complex-to-Ext bridge is mathlib's constructor. -/
lemma homComplexCohomologyClassToExt_mk {C : Type u} [Category.{v} C]
    [Abelian C] [HasExt.{w} C] {X Y : C} {n : ℕ}
    (x : CochainComplex.HomComplex.Cocycle ((CochainComplex.singleFunctor C 0).obj X)
      ((CochainComplex.singleFunctor C 0).obj Y) (n : ℤ)) :
    homComplexCohomologyClassToExt X Y n (CochainComplex.HomComplex.CohomologyClass.mk x) =
      SmallShiftedHom.mk (HomologicalComplex.quasiIso C (ComplexShape.up ℤ))
        (CochainComplex.HomComplex.Cocycle.equivHomShift.symm x) := rfl

/--
Repo-local gate for the cohomological Hom/Ext API selection.

The Hom-complex API and the `Abelian.Ext` endpoint are selected and connected
for single complexes.  This does not prove the cohomological UCT short exact
sequence; the remaining bridge is the identification of the UCT Hom complex
and its cohomology with the selected single-complex Ext endpoint in the chosen
coefficient model.
-/
structure CohomologicalHomExtAPIBoundary (C : Type u) [Category.{v} C] [Abelian C]
    [HasExt.{w} C] where
  homComplexToExtForSingles : ∀ X Y : C, ∀ n : ℕ,
    Nonempty (selectedHomComplexCohomology ((CochainComplex.singleFunctor C 0).obj X)
      ((CochainComplex.singleFunctor C 0).obj Y) (n : ℤ) → selectedExtEndpoint X Y n)
  extZeroEndpointMatchesMorphisms : ∀ X Y : C, Nonempty (selectedExtEndpoint X Y 0 ≃+ (X ⟶ Y))
  terminalUCTBlockedUntilCohomologyBridge : Prop
  terminalUCTBlockedUntilCohomologyBridge_holds : terminalUCTBlockedUntilCohomologyBridge

/-- The selected cohomological Hom/Ext API boundary for this Stage1 artifact. -/
noncomputable def selectedCohomologicalHomExtAPIBoundary (C : Type u) [Category.{v} C]
    [Abelian C] [HasExt.{w} C] : CohomologicalHomExtAPIBoundary C where
  homComplexToExtForSingles := fun X Y n => ⟨homComplexCohomologyClassToExt X Y n⟩
  extZeroEndpointMatchesMorphisms := fun X Y => ⟨extEndpointAddEquivZero X Y⟩
  terminalUCTBlockedUntilCohomologyBridge := True
  terminalUCTBlockedUntilCohomologyBridge_holds := trivial

/--
Machine-checkable gate: this file has selected the Hom-complex and Ext endpoint
APIs for the cohomological branch and has connected Hom-complex cohomology of
single complexes to `Abelian.Ext`.
-/
def CohomologicalHomExtAPIGate : Prop :=
  ∀ (C : Type u) [Category.{v} C] [Abelian C] [HasExt.{w} C],
    Nonempty (CohomologicalHomExtAPIBoundary C)

/-- The Hom/Ext API gate is closed only as an API-boundary selection. -/
theorem cohomologicalHomExtAPIGate_checked : CohomologicalHomExtAPIGate := by
  intro C _ _ _
  exact ⟨selectedCohomologicalHomExtAPIBoundary C⟩

/--
Naturality square for any comparison map out of homology under a chain-complex
map.

This is the reusable shape needed by the UCT naturality branch in the
chain-complex variable.  It is intentionally parameterized by the comparison
maps and target map, because this Stage1 artifact has not selected a terminal
UCT comparison morphism.
-/
def HomologyComparisonNaturalitySquare {C : Type u} [Category.{v} C] [HasZeroMorphisms C]
    [CategoryWithHomology C] {ι : Type uι} {c : ComplexShape ι}
    {K L : HomologicalComplex C c} (i : ι) [K.HasHomology i] [L.HasHomology i]
    {T_K T_L : C} (κK : K.homology i ⟶ T_K) (κL : L.homology i ⟶ T_L)
    (f : K ⟶ L) (targetMap : T_K ⟶ T_L) : Prop :=
  κK ≫ targetMap = HomologicalComplex.homologyMap f i ≫ κL

/-- The homology-comparison naturality predicate unfolds to its square equation. -/
theorem homologyComparisonNaturalitySquare_iff {C : Type u} [Category.{v} C]
    [HasZeroMorphisms C] [CategoryWithHomology C] {ι : Type uι} {c : ComplexShape ι}
    {K L : HomologicalComplex C c} (i : ι) [K.HasHomology i] [L.HasHomology i]
    {T_K T_L : C} (κK : K.homology i ⟶ T_K) (κL : L.homology i ⟶ T_L)
    (f : K ⟶ L) (targetMap : T_K ⟶ T_L) :
    HomologyComparisonNaturalitySquare i κK κL f targetMap ↔
      κK ≫ targetMap = HomologicalComplex.homologyMap f i ≫ κL :=
  Iff.rfl

/--
Checked wrapper around mathlib's long-exact-sequence naturality theorem.

This is the chain-complex-map naturality anchor requested for the UCT branch:
the connecting morphisms commute with the homology maps induced by a morphism
of short exact sequences of complexes.
-/
theorem homologySequence_delta_naturality
    {C : Type u} [Category.{v} C] [Abelian C] {ι : Type uι} {c : ComplexShape ι}
    {S₁ S₂ : ShortComplex (HomologicalComplex C c)} (φ : S₁ ⟶ S₂)
    (hS₁ : S₁.ShortExact) (hS₂ : S₂.ShortExact)
    (i j : ι) (hij : c.Rel i j) :
    hS₁.δ i j hij ≫ HomologicalComplex.homologyMap φ.τ₁ j =
      HomologicalComplex.homologyMap φ.τ₃ i ≫ hS₂.δ i j hij :=
  HomologicalComplex.HomologySequence.δ_naturality φ hS₁ hS₂ i j hij

/-- The selected tensor functor's map in the coefficient object variable. -/
def selectedTensorCoefficientMap {C : Type u} [Category.{v} C] [MonoidalCategory C]
    (X : C) {A B : C} (α : A ⟶ B) :
    ((selectedTensorBifunctor C).obj X).obj A ⟶ ((selectedTensorBifunctor C).obj X).obj B :=
  ((selectedTensorBifunctor C).obj X).map α

/--
Naturality square in the coefficient object for tensor-shaped comparison maps.

This object-level square is the coefficient-variable analogue of
`HomologyComparisonNaturalitySquare`.  It uses the selected tensor bifunctor
and keeps the eventual UCT comparison maps explicit.
-/
def TensorCoefficientComparisonNaturalitySquare {C : Type u} [Category.{v} C]
    [MonoidalCategory C] (X : C) {A B T_A T_B : C}
    (α : A ⟶ B)
    (κA : ((selectedTensorBifunctor C).obj X).obj A ⟶ T_A)
    (κB : ((selectedTensorBifunctor C).obj X).obj B ⟶ T_B)
    (targetMap : T_A ⟶ T_B) : Prop :=
  κA ≫ targetMap = selectedTensorCoefficientMap X α ≫ κB

/-- The coefficient-object naturality predicate unfolds to its square equation. -/
theorem tensorCoefficientComparisonNaturalitySquare_iff {C : Type u} [Category.{v} C]
    [MonoidalCategory C] (X : C) {A B T_A T_B : C}
    (α : A ⟶ B)
    (κA : ((selectedTensorBifunctor C).obj X).obj A ⟶ T_A)
    (κB : ((selectedTensorBifunctor C).obj X).obj B ⟶ T_B)
    (targetMap : T_A ⟶ T_B) :
    TensorCoefficientComparisonNaturalitySquare X α κA κB targetMap ↔
      κA ≫ targetMap = selectedTensorCoefficientMap X α ≫ κB :=
  Iff.rfl

/--
Chain-level coefficient naturality square after the selected tensor API is
lifted to total complexes.

The coefficient object is represented by the second homological-complex
variable.  The statement stays at API-boundary level because the eventual UCT
coefficient model and total-complex comparison maps remain future work.
-/
def TensorTotalCoefficientComplexNaturalitySquare {C : Type u} [Category.{v} C]
    [Preadditive C] [MonoidalCategory C]
    [tensorPreservesZero : (selectedTensorBifunctor C).PreservesZeroMorphisms]
    [tensorObjPreservesZero : ∀ X, ((selectedTensorBifunctor C).obj X).PreservesZeroMorphisms]
    {ι₁ : Type uι₁} {ι₂ : Type uι₂} {J : Type uJ}
    {c₁ : ComplexShape ι₁} {c₂ : ComplexShape ι₂} {c : ComplexShape J}
    [DecidableEq J] [TotalComplexShape c₁ c₂ c]
    [∀ (K₁ : HomologicalComplex C c₁) (K₂ : HomologicalComplex C c₂),
      ((((selectedTensorBifunctor C).mapBifunctorHomologicalComplex c₁ c₂).obj K₁).obj K₂).HasTotal c]
    (K : HomologicalComplex C c₁) {A B : HomologicalComplex C c₂}
    (α : A ⟶ B) {T_A T_B : HomologicalComplex C c}
    (κA : (((selectedTensorTotalComplexFunctor c₁ c₂ c).obj K).obj A) ⟶ T_A)
    (κB : (((selectedTensorTotalComplexFunctor c₁ c₂ c).obj K).obj B) ⟶ T_B)
    (targetMap : T_A ⟶ T_B) : Prop :=
  κA ≫ targetMap = (((selectedTensorTotalComplexFunctor c₁ c₂ c).obj K).map α) ≫ κB

/-- The chain-level coefficient naturality predicate unfolds to its square equation. -/
theorem tensorTotalCoefficientComplexNaturalitySquare_iff {C : Type u} [Category.{v} C]
    [Preadditive C] [MonoidalCategory C]
    [tensorPreservesZero : (selectedTensorBifunctor C).PreservesZeroMorphisms]
    [tensorObjPreservesZero : ∀ X, ((selectedTensorBifunctor C).obj X).PreservesZeroMorphisms]
    {ι₁ : Type uι₁} {ι₂ : Type uι₂} {J : Type uJ}
    {c₁ : ComplexShape ι₁} {c₂ : ComplexShape ι₂} {c : ComplexShape J}
    [DecidableEq J] [TotalComplexShape c₁ c₂ c]
    [∀ (K₁ : HomologicalComplex C c₁) (K₂ : HomologicalComplex C c₂),
      ((((selectedTensorBifunctor C).mapBifunctorHomologicalComplex c₁ c₂).obj K₁).obj K₂).HasTotal c]
    (K : HomologicalComplex C c₁) {A B : HomologicalComplex C c₂}
    (α : A ⟶ B) {T_A T_B : HomologicalComplex C c}
    (κA : (((selectedTensorTotalComplexFunctor c₁ c₂ c).obj K).obj A) ⟶ T_A)
    (κB : (((selectedTensorTotalComplexFunctor c₁ c₂ c).obj K).obj B) ⟶ T_B)
    (targetMap : T_A ⟶ T_B) :
    TensorTotalCoefficientComplexNaturalitySquare K α κA κB targetMap ↔
      κA ≫ targetMap = (((selectedTensorTotalComplexFunctor c₁ c₂ c).obj K).map α) ≫ κB :=
  Iff.rfl

/--
Repo-local API boundary for the UCT naturality branch.

The branch is checked for reusable mathlib functoriality anchors:
homology maps, long-exact-sequence connecting-map naturality, and tensor maps
in the coefficient variable.  The terminal UCT naturality theorem is still
blocked until the actual UCT comparison morphisms and coefficient model are
constructed.
-/
structure UniversalCoefficientNaturalityAPIBoundary (C : Type u) [Category.{v} C]
    [Abelian C] [CategoryWithHomology C] [MonoidalCategory C] where
  homologyMapsAvailable : ∀ {ι : Type uι} {c : ComplexShape ι}
    {K L : HomologicalComplex C c} (_f : K ⟶ L) (i : ι)
    [K.HasHomology i] [L.HasHomology i], Nonempty (K.homology i ⟶ L.homology i)
  homologySequenceDeltaNaturality : ∀ {ι : Type uι} {c : ComplexShape ι}
    {S₁ S₂ : ShortComplex (HomologicalComplex C c)} (φ : S₁ ⟶ S₂)
    (hS₁ : S₁.ShortExact) (hS₂ : S₂.ShortExact)
    (i j : ι) (hij : c.Rel i j),
      hS₁.δ i j hij ≫ HomologicalComplex.homologyMap φ.τ₁ j =
        HomologicalComplex.homologyMap φ.τ₃ i ≫ hS₂.δ i j hij
  tensorCoefficientMapsAvailable : ∀ (X A B : C) (_α : A ⟶ B),
    Nonempty (((selectedTensorBifunctor C).obj X).obj A ⟶
      ((selectedTensorBifunctor C).obj X).obj B)
  terminalUCTNaturalityBlockedUntilComparisonMaps : Prop
  terminalUCTNaturalityBlockedUntilComparisonMaps_holds :
    terminalUCTNaturalityBlockedUntilComparisonMaps

/-- The selected naturality API boundary for this Stage1 artifact. -/
def selectedUniversalCoefficientNaturalityAPIBoundary (C : Type u) [Category.{v} C]
    [Abelian C] [CategoryWithHomology C] [MonoidalCategory C] :
    UniversalCoefficientNaturalityAPIBoundary C where
  homologyMapsAvailable := fun f i => ⟨HomologicalComplex.homologyMap f i⟩
  homologySequenceDeltaNaturality := fun φ hS₁ hS₂ i j hij =>
    homologySequence_delta_naturality φ hS₁ hS₂ i j hij
  tensorCoefficientMapsAvailable := fun X _ _ α => ⟨selectedTensorCoefficientMap X α⟩
  terminalUCTNaturalityBlockedUntilComparisonMaps := True
  terminalUCTNaturalityBlockedUntilComparisonMaps_holds := trivial

/--
Machine-checkable gate: this file has formalized the reusable naturality API
boundary for chain-complex maps and coefficient-object maps, without claiming a
terminal UCT naturality theorem.
-/
def UniversalCoefficientNaturalityAPIGate : Prop :=
  ∀ (C : Type u) [Category.{v} C] [Abelian C] [CategoryWithHomology C] [MonoidalCategory C],
    Nonempty (UniversalCoefficientNaturalityAPIBoundary.{u, v, uι} C)

/-- The naturality gate is closed only as an API-boundary selection. -/
theorem universalCoefficientNaturalityAPIGate_checked :
    UniversalCoefficientNaturalityAPIGate := by
  intro C _ _ _ _
  exact ⟨selectedUniversalCoefficientNaturalityAPIBoundary C⟩

/-! ## External Lean proof-search audit -/

/--
One row in the Stage1 C006 external proof-search ledger for the universal
coefficient theorem.

Rows with `terminalUCTProofBodyFound = false` are negative or blocked audit
evidence, not a global proof of absence.  A positive row may support completion
only after the named proof body is pinned, imported, and checked locally, or
after a concrete Lake/toolchain/license blocker is recorded.
-/
structure ExternalUniversalCoefficientSearchRow where
  searchSurface : String
  query : String
  repositoryUrl : String
  commit : String
  modules : List String
  theoremNames : List String
  terminalUCTProofBodyFound : Bool
  lakeCompatibility : String
  result : String
  integrationStatus : String
deriving Repr

/-- Date of the Stage1 C006 external proof-search pass. -/
def universalCoefficientExternalProofSearchDate : String :=
  "2026-05-01"

/--
Stage1 C006 external proof-search rows.

The audit found mathlib substrate APIs, including `Tor`, `Ext`, homology
functors, and bifunctorial homological complexes.  It did not find a terminal
Lean 4 proof body for the classical universal coefficient theorem that could be
pin/import/checked in this repository.  Authenticated GitHub code search was
blocked by missing credentials in the worker environment.
-/
def universalCoefficientExternalProofSearchRows :
    List ExternalUniversalCoefficientSearchRow := [
  {
    searchSurface := "GitHub CLI authenticated code search"
    query := "UniversalCoefficient; \"universal coefficient theorem\"; UCT; Tor; Ext; HomologicalComplex; mapBifunctor; homologyFunctor"
    repositoryUrl := "https://github.com/search"
    commit := "blocked"
    modules := []
    theoremNames := []
    terminalUCTProofBodyFound := false
    lakeCompatibility := "blocked: no authenticated GitHub session was available, so no candidate Lake project could be checked"
    result := "`gh auth status` reported no logged-in GitHub hosts on 2026-05-01; `gh search code` requested GH auth"
    integrationStatus := "integration blocker: rerun the exact query set with an authenticated `gh` session or `GH_TOKEN`, then pin/import/check any real proof body found"
  },
  {
    searchSurface := "GitHub REST code search"
    query := "UniversalCoefficient language:Lean; \"universal coefficient theorem\" language:Lean; homologyFunctor UniversalCoefficient language:Lean"
    repositoryUrl := "https://api.github.com/search/code"
    commit := "blocked"
    modules := []
    theoremNames := []
    terminalUCTProofBodyFound := false
    lakeCompatibility := "blocked: unauthenticated REST code search did not provide Lean source evidence"
    result := "GitHub REST code search returned HTTP 401 Requires authentication on 2026-05-01"
    integrationStatus := "integration blocker: provide GitHub authentication and rerun before upgrading this C006 search gate"
  },
  {
    searchSurface := "Reservoir package-index metadata"
    query := "UniversalCoefficient; universal coefficient; UCT; Tor; Ext; HomologicalComplex; mapBifunctor; homologyFunctor"
    repositoryUrl := "https://github.com/leanprover/reservoir-index.git"
    commit := "b178d80d731ec2e744c6ce9a83968a9648464baa"
    modules := []
    theoremNames := []
    terminalUCTProofBodyFound := false
    lakeCompatibility := "no Reservoir package metadata matched a terminal UCT proof body, so no external Lake dependency was selected"
    result := "local clone of the Reservoir index had no exact metadata hit for UniversalCoefficient/universal coefficient/UCT/HomologicalComplex/mapBifunctor/homologyFunctor as a UCT proof package"
    integrationStatus := "no Reservoir package was pin-ready for THM-M-0004"
  },
  {
    searchSurface := "repo-local pinned mathlib grep"
    query := "UniversalCoefficient; universal coefficient; UCT; Tor; Ext; HomologicalComplex; mapBifunctor; homologyFunctor"
    repositoryUrl := "https://github.com/leanprover-community/mathlib4.git"
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
    modules := [
      "Mathlib.Algebra.Homology.ShortComplex.HomologicalComplex",
      "Mathlib.Algebra.Homology.HomologySequenceLemmas",
      "Mathlib.Algebra.Homology.Bifunctor",
      "Mathlib.CategoryTheory.Monoidal.Tor",
      "Mathlib.Algebra.Homology.DerivedCategory.Ext.Basic"
    ]
    theoremNames := [
      "HomologicalComplex.homologyFunctor",
      "HomologicalComplex.homologyMap",
      "HomologicalComplex.HomologySequence.δ_naturality",
      "Functor.mapBifunctorHomologicalComplex",
      "Functor.map₂HomologicalComplex",
      "CategoryTheory.Tor",
      "CategoryTheory.Tor'",
      "CategoryTheory.isZero_Tor_succ_of_projective",
      "Abelian.Ext",
      "Abelian.Ext.addEquiv₀"
    ]
    terminalUCTProofBodyFound := false
    lakeCompatibility := "Lake-compatible in this repository via pinned mathlib; this file imports and checks the listed substrate declarations"
    result := "substrate APIs found, but no terminal universal coefficient theorem proof body was found in pinned mathlib"
    integrationStatus := "local_wrapper_upstream_mathlib for substrate only; terminal THM-M-0004 remains formalization_debt, not repo-local completed"
  }
]

/-- Current C006 result: no terminal external Lean 4 UCT proof body was found. -/
def universalCoefficientExternalProofBodyFound : Bool :=
  universalCoefficientExternalProofSearchRows.any
    (fun row => row.terminalUCTProofBodyFound)

/-- Current C006 result: no external UCT proof has been pinned/imported/checked here. -/
def universalCoefficientExternalProofPinnedImportedChecked : Bool :=
  false

/--
M0387 gate: this C006 audit does not leave repo-local integration debt in a
completed state.  Since no external terminal proof body was found or claimed,
the theorem remains open formalization debt.
-/
def universalCoefficientExternalSearchRepoLocalIntegrationDebtRetainedInCompletedState :
    Bool :=
  false

/-- Checked negative external-proof finding for the current C006 pass. -/
theorem universalCoefficientExternalProofBodyFound_eq_false :
    universalCoefficientExternalProofBodyFound = false :=
  rfl

/-- Checked non-integration result for the current C006 pass. -/
theorem universalCoefficientExternalProofPinnedImportedChecked_eq_false :
    universalCoefficientExternalProofPinnedImportedChecked = false :=
  rfl

/-- Checked M0387 repo-local integration-debt gate for this C006 pass. -/
theorem universalCoefficientExternalSearchRepoLocalIntegrationDebtRetained_eq_false :
    universalCoefficientExternalSearchRepoLocalIntegrationDebtRetainedInCompletedState = false :=
  rfl

/-! ## Proof-tree backfill ledger -/

/--
Top-level proof-tree branches for the Stage1 universal coefficient theorem
backfill.

These are process branches, not mathematical theorem claims.  Each branch below
has its own local leaf ledger with all leaf budgets checked at `<= 100`.
-/
inductive UniversalCoefficientProofBranch where
  | statementNormalization
  | tensorTor
  | homExt
  | exactnessNaturality
  | spectralResolutionBridge
  | repoLocalClosureGate
deriving DecidableEq, Repr

/--
One local proof-tree leaf for the C007 backfill.

The `budget_le_100` field is the machine-checkable part of the M0387 leaf
budget discipline.  A leaf with `completionClaim = false` may still record
checked API-boundary progress, but it cannot be used as a terminal UCT proof.
-/
structure UniversalCoefficientProofLeafLedger where
  branch : UniversalCoefficientProofBranch
  leafId : String
  task : String
  budget : Nat
  budget_le_100 : budget ≤ 100
  status : String
  completionClaim : Bool

/-- Statement-normalization branch ledger. -/
def universalCoefficientStatementNormalizationLedger :
    List UniversalCoefficientProofLeafLedger := [
  {
    branch := UniversalCoefficientProofBranch.statementNormalization
    leafId := "M0004-P00-L001"
    task := "Normalize input data with category, homology, abelian, complex-shape, chain-complex, and coefficient assumptions"
    budget := 30
    budget_le_100 := by decide
    status := "checked local: UniversalCoefficientInput and UniversalCoefficientInput.Assumptions"
    completionClaim := false
  },
  {
    branch := UniversalCoefficientProofBranch.statementNormalization
    leafId := "M0004-P00-L002"
    task := "Normalize output package with tensor/Tor and Hom/Ext terms, short exact sequences, naturality, and term identifications"
    budget := 50
    budget_le_100 := by decide
    status := "checked local: UniversalCoefficientOutput"
    completionClaim := false
  },
  {
    branch := UniversalCoefficientProofBranch.statementNormalization
    leafId := "M0004-P00-L003"
    task := "State the package-valued UCT skeleton without claiming the terminal theorem"
    budget := 30
    budget_le_100 := by decide
    status := "checked local: StatementShape"
    completionClaim := false
  }
]

/-- Tensor/Tor branch ledger. -/
def universalCoefficientTensorTorLedger :
    List UniversalCoefficientProofLeafLedger := [
  {
    branch := UniversalCoefficientProofBranch.tensorTor
    leafId := "M0004-P01-L001"
    task := "Select tensor as MonoidalCategory.curriedTensor"
    budget := 40
    budget_le_100 := by decide
    status := "checked local API boundary: selectedTensorBifunctor"
    completionClaim := false
  },
  {
    branch := UniversalCoefficientProofBranch.tensorTor
    leafId := "M0004-P01-L002"
    task := "Select Tor endpoint as CategoryTheory.Tor and record Tor' as the first-variable variant"
    budget := 60
    budget_le_100 := by decide
    status := "checked local wrapper upstream mathlib: selectedTorBifunctor and selectedTorLeftVariant"
    completionClaim := false
  },
  {
    branch := UniversalCoefficientProofBranch.tensorTor
    leafId := "M0004-P01-L003"
    task := "Lift the selected tensor bifunctor to bicomplexes and total complexes"
    budget := 90
    budget_le_100 := by decide
    status := "checked local API boundary: selectedTensorBicomplexFunctor and selectedTensorTotalComplexFunctor"
    completionClaim := false
  },
  {
    branch := UniversalCoefficientProofBranch.tensorTor
    leafId := "M0004-P01-L004"
    task := "Construct the homological UCT comparison and short exact sequence for tensor homology and Tor"
    budget := 100
    budget_le_100 := by decide
    status := "unchecked formalization_debt: terminal comparison and exactness theorem not constructed"
    completionClaim := false
  }
]

/-- Hom/Ext branch ledger. -/
def universalCoefficientHomExtLedger :
    List UniversalCoefficientProofLeafLedger := [
  {
    branch := UniversalCoefficientProofBranch.homExt
    leafId := "M0004-P02-L001"
    task := "Select Hom-complex cohomology as CochainComplex.HomComplex.CohomologyClass"
    budget := 50
    budget_le_100 := by decide
    status := "checked local API boundary: selectedHomComplexCohomology"
    completionClaim := false
  },
  {
    branch := UniversalCoefficientProofBranch.homExt
    leafId := "M0004-P02-L002"
    task := "Connect the selected Ext endpoint to Abelian.Ext, including the zero-degree morphism comparison"
    budget := 80
    budget_le_100 := by decide
    status := "checked local wrapper upstream mathlib: selectedExtEndpoint and extEndpointAddEquivZero"
    completionClaim := false
  },
  {
    branch := UniversalCoefficientProofBranch.homExt
    leafId := "M0004-P02-L003"
    task := "Bridge Hom-complex cohomology classes of single complexes to Abelian.Ext"
    budget := 80
    budget_le_100 := by decide
    status := "checked local API boundary: homComplexCohomologyClassToExt"
    completionClaim := false
  },
  {
    branch := UniversalCoefficientProofBranch.homExt
    leafId := "M0004-P02-L004"
    task := "Construct the cohomological UCT short exact sequence for Hom and Ext in the chosen coefficient model"
    budget := 100
    budget_le_100 := by decide
    status := "unchecked formalization_debt: terminal cohomological UCT sequence not constructed"
    completionClaim := false
  }
]

/-- Exactness and naturality branch ledger. -/
def universalCoefficientExactnessNaturalityLedger :
    List UniversalCoefficientProofLeafLedger := [
  {
    branch := UniversalCoefficientProofBranch.exactnessNaturality
    leafId := "M0004-P03-L001"
    task := "Expose ShortComplex.ShortExact.exact for exactness-facing sequence checks"
    budget := 20
    budget_le_100 := by decide
    status := "checked local wrapper: shortExact_exact"
    completionClaim := false
  },
  {
    branch := UniversalCoefficientProofBranch.exactnessNaturality
    leafId := "M0004-P03-L002"
    task := "Encode chain-complex-map naturality through HomologicalComplex.homologyMap"
    budget := 60
    budget_le_100 := by decide
    status := "checked local API boundary: HomologyComparisonNaturalitySquare"
    completionClaim := false
  },
  {
    branch := UniversalCoefficientProofBranch.exactnessNaturality
    leafId := "M0004-P03-L003"
    task := "Wrap long-exact-sequence boundary naturality"
    budget := 60
    budget_le_100 := by decide
    status := "checked local wrapper upstream mathlib: homologySequence_delta_naturality"
    completionClaim := false
  },
  {
    branch := UniversalCoefficientProofBranch.exactnessNaturality
    leafId := "M0004-P03-L004"
    task := "Encode coefficient-object naturality for tensor-shaped comparison maps and total complexes"
    budget := 90
    budget_le_100 := by decide
    status := "checked local API boundary: TensorCoefficientComparisonNaturalitySquare and TensorTotalCoefficientComplexNaturalitySquare"
    completionClaim := false
  },
  {
    branch := UniversalCoefficientProofBranch.exactnessNaturality
    leafId := "M0004-P03-L005"
    task := "Instantiate exactness and naturality for the final homological and cohomological UCT comparison morphisms"
    budget := 100
    budget_le_100 := by decide
    status := "unchecked formalization_debt: final UCT comparison morphisms not constructed"
    completionClaim := false
  }
]

/-- Spectral-sequence or resolution bridge branch ledger. -/
def universalCoefficientSpectralResolutionBridgeLedger :
    List UniversalCoefficientProofLeafLedger := [
  {
    branch := UniversalCoefficientProofBranch.spectralResolutionBridge
    leafId := "M0004-P04-L001"
    task := "Choose the terminal proof route: spectral sequence, projective resolution, flat resolution, or derived-functor bridge"
    budget := 100
    budget_le_100 := by decide
    status := "unchecked formalization_debt: route not selected as a checked local theorem"
    completionClaim := false
  },
  {
    branch := UniversalCoefficientProofBranch.spectralResolutionBridge
    leafId := "M0004-P04-L002"
    task := "Identify the selected route with the tensor/Tor and Hom/Ext endpoints"
    budget := 100
    budget_le_100 := by decide
    status := "unchecked formalization_debt: endpoint comparison theorem not constructed"
    completionClaim := false
  },
  {
    branch := UniversalCoefficientProofBranch.spectralResolutionBridge
    leafId := "M0004-P04-L003"
    task := "Extract the short exact UCT sequence from the selected filtration or resolution argument"
    budget := 100
    budget_le_100 := by decide
    status := "unchecked formalization_debt: short exact extraction theorem not constructed"
    completionClaim := false
  }
]

/-- Repo-local closure-gate branch ledger. -/
def universalCoefficientRepoLocalClosureGateLedger :
    List UniversalCoefficientProofLeafLedger := [
  {
    branch := UniversalCoefficientProofBranch.repoLocalClosureGate
    leafId := "M0004-P05-L001"
    task := "Record external proof-search rows without treating blocked or negative rows as theorem completion"
    budget := 60
    budget_le_100 := by decide
    status := "checked local audit ledger: universalCoefficientExternalProofSearchRows"
    completionClaim := false
  },
  {
    branch := UniversalCoefficientProofBranch.repoLocalClosureGate
    leafId := "M0004-P05-L002"
    task := "Prove no completed state retains repo_local_integration_debt in the current artifact"
    budget := 40
    budget_le_100 := by decide
    status := "checked local gate: universalCoefficientExternalSearchRepoLocalIntegrationDebtRetained_eq_false"
    completionClaim := false
  },
  {
    branch := UniversalCoefficientProofBranch.repoLocalClosureGate
    leafId := "M0004-P05-L003"
    task := "Close the terminal theorem by local proof body, pinned mathlib wrapper, or pinned/imported external dependency"
    budget := 100
    budget_le_100 := by decide
    status := "unchecked formalization_debt: no terminal UCT proof body is present"
    completionClaim := false
  }
]

/-- A branch-level ledger with an independent local leaf list. -/
structure UniversalCoefficientProofBranchLedger where
  branch : UniversalCoefficientProofBranch
  branchSummary : String
  leaves : List UniversalCoefficientProofLeafLedger
  independentLeafLedger : Bool
  terminalUCTCompletionClaim : Bool

/-- The C007 proof-tree backfill split requested by the Stage1 child task. -/
def universalCoefficientProofTreeBackfill :
    List UniversalCoefficientProofBranchLedger := [
  {
    branch := UniversalCoefficientProofBranch.statementNormalization
    branchSummary := "statement normalization"
    leaves := universalCoefficientStatementNormalizationLedger
    independentLeafLedger := true
    terminalUCTCompletionClaim := false
  },
  {
    branch := UniversalCoefficientProofBranch.tensorTor
    branchSummary := "tensor/Tor branch"
    leaves := universalCoefficientTensorTorLedger
    independentLeafLedger := true
    terminalUCTCompletionClaim := false
  },
  {
    branch := UniversalCoefficientProofBranch.homExt
    branchSummary := "Hom/Ext branch"
    leaves := universalCoefficientHomExtLedger
    independentLeafLedger := true
    terminalUCTCompletionClaim := false
  },
  {
    branch := UniversalCoefficientProofBranch.exactnessNaturality
    branchSummary := "exactness/naturality branch"
    leaves := universalCoefficientExactnessNaturalityLedger
    independentLeafLedger := true
    terminalUCTCompletionClaim := false
  },
  {
    branch := UniversalCoefficientProofBranch.spectralResolutionBridge
    branchSummary := "spectral/resolution bridge"
    leaves := universalCoefficientSpectralResolutionBridgeLedger
    independentLeafLedger := true
    terminalUCTCompletionClaim := false
  },
  {
    branch := UniversalCoefficientProofBranch.repoLocalClosureGate
    branchSummary := "repo-local closure gate"
    leaves := universalCoefficientRepoLocalClosureGateLedger
    independentLeafLedger := true
    terminalUCTCompletionClaim := false
  }
]

/--
C007 non-completion gate: proof-tree backfill exists, but it does not claim the
terminal universal coefficient theorem.
-/
def universalCoefficientProofTreeBackfillClaimsTerminalCompletion : Bool :=
  universalCoefficientProofTreeBackfill.any
    (fun branch => branch.terminalUCTCompletionClaim)

/--
M0387 repo-local integration-debt gate for C007.  The proof-tree split records
open formalization debt; it does not leave anchor-only external evidence in a
completed state.
-/
def universalCoefficientProofTreeRepoLocalIntegrationDebtRetainedInCompletedState :
    Bool :=
  false

/-- Checked C007 non-completion result. -/
theorem universalCoefficientProofTreeBackfillClaimsTerminalCompletion_eq_false :
    universalCoefficientProofTreeBackfillClaimsTerminalCompletion = false :=
  rfl

/-- Checked C007 repo-local integration-debt gate. -/
theorem universalCoefficientProofTreeRepoLocalIntegrationDebtRetained_eq_false :
    universalCoefficientProofTreeRepoLocalIntegrationDebtRetainedInCompletedState = false :=
  rfl

#check HomologicalComplex.homologyFunctor
#check HomologicalComplex.homologyMap
#check HomologicalComplex.HomologySequence.δ_naturality
#check MonoidalCategory.curriedTensor
#check MonoidalCategory.tensorLeft
#check MonoidalCategory.tensorRight
#check Functor.mapBifunctorHomologicalComplex
#check Functor.map₂HomologicalComplex
#check CategoryTheory.Tor
#check CategoryTheory.Tor'
#check CategoryTheory.isZero_Tor_succ_of_projective
#check ShortComplex.ShortExact
#check CochainComplex.HomComplex.CohomologyClass
#check CochainComplex.HomComplex.CohomologyClass.toSmallShiftedHom
#check Abelian.Ext
#check Abelian.Ext.addEquiv₀
#check HomologyComparisonNaturalitySquare
#check homologySequence_delta_naturality
#check selectedTensorCoefficientMap
#check TensorCoefficientComparisonNaturalitySquare
#check TensorTotalCoefficientComplexNaturalitySquare
#check universalCoefficientNaturalityAPIGate_checked
#check ExternalUniversalCoefficientSearchRow
#check universalCoefficientExternalProofSearchRows
#check universalCoefficientExternalProofBodyFound_eq_false
#check universalCoefficientExternalProofPinnedImportedChecked_eq_false
#check UniversalCoefficientProofBranch
#check UniversalCoefficientProofLeafLedger
#check universalCoefficientProofTreeBackfill
#check universalCoefficientProofTreeBackfillClaimsTerminalCompletion_eq_false
#check universalCoefficientProofTreeRepoLocalIntegrationDebtRetained_eq_false

end Stage1.THMM0004
