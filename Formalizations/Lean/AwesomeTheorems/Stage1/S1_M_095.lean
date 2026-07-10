import Mathlib.CategoryTheory.Abelian.LeftDerived
import Mathlib.CategoryTheory.Abelian.RightDerived
import Mathlib.CategoryTheory.Functor.Derived.LeftDerived
import Mathlib.CategoryTheory.Functor.Derived.RightDerived
import Mathlib.Algebra.Homology.HomologySequenceLemmas
import Mathlib.Algebra.Homology.DerivedCategory.HomologySequence

/-!
# S1-M-095 / THM-M-0006: Derived functor theorem

This Stage1 artifact records checkable Lean 4 wrappers for the parts of the
derived-functor existence theorem already present in the pinned mathlib tree.

There are two distinct mathlib layers:

* `CategoryTheory.Abelian.LeftDerived` and `CategoryTheory.Abelian.RightDerived`
  define the classical degreewise left/right derived functors of additive functors
  using projective and injective resolutions.
* `CategoryTheory.Functor.Derived.LeftDerived` and
  `CategoryTheory.Functor.Derived.RightDerived` define total derived functors as
  Kan extensions along a localization, assuming the corresponding Kan extension
  exists.

The declarations below are wrappers and statement-shape anchors.  They do not
claim a terminal proof that every functor in every desired homological setting has
the required resolutions, exactness hypotheses, derived category comparison, and
long exact sequence package.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits Pretriangulated

set_option linter.unusedSectionVars false

universe uC vC uD vD uH vH

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_095

section AbelianResolutionDerived

variable {C : Type uC} [Category.{vC} C] [Abelian C]
variable {D : Type uD} [Category.{vD} D] [Abelian D]

/-- Mathlib's left-derived functor of an additive functor, using projective resolutions. -/
abbrev LeftDerivedFunctor [HasProjectiveResolutions C]
    (F : C ⥤ D) [F.Additive] (n : ℕ) : C ⥤ D :=
  F.leftDerived n

/-- Mathlib's right-derived functor of an additive functor, using injective resolutions. -/
abbrev RightDerivedFunctor [HasInjectiveResolutions C]
    (F : C ⥤ D) [F.Additive] (n : ℕ) : C ⥤ D :=
  F.rightDerived n

/--
Degreewise abelian-category statement shape.

Under the standard mathlib hypotheses that the source abelian category has both
projective and injective resolutions, every additive functor has named
degreewise left and right derived functors.  This is a checked existence wrapper
for the available API, not a universal terminal theorem without hypotheses.
-/
def AbelianResolutionStatementShape : Prop :=
  ∀ {C : Type uC} [Category.{vC} C] [Abelian C]
    [HasProjectiveResolutions C] [HasInjectiveResolutions C]
    {D : Type uD} [Category.{vD} D] [Abelian D]
    (F : C ⥤ D) [F.Additive],
      (∀ n : ℕ, Nonempty {G : C ⥤ D // G = F.leftDerived n}) ∧
        (∀ n : ℕ, Nonempty {G : C ⥤ D // G = F.rightDerived n})

/-- The abelian-resolution statement shape is witnessed by mathlib's named functors. -/
theorem abelianResolutionStatementShape_checked :
    AbelianResolutionStatementShape.{uC, vC, uD, vD} := by
  intro C _ _ _ _ D _ _ F _
  constructor
  · intro n
    exact ⟨⟨F.leftDerived n, rfl⟩⟩
  · intro n
    exact ⟨⟨F.rightDerived n, rfl⟩⟩

/--
Public canonical degreewise statement for `THM-M-0006.abelian-derived`.

This selects the abelian-resolution branch as the canonical degreewise public
surface: in abelian source and target categories, with projective and injective
resolutions in the source, every additive functor has the named mathlib
degreewise left and right derived functors.  Total derived functors remain a
separate Kan-extension statement.
-/
def AbelianDerivedCanonicalStatement : Prop :=
  AbelianResolutionStatementShape.{uC, vC, uD, vD}

/-- The selected degreewise canonical statement is checked by mathlib's named functors. -/
theorem abelianDerivedCanonicalStatement_checked :
    AbelianDerivedCanonicalStatement.{uC, vC, uD, vD} :=
  abelianResolutionStatementShape_checked

/-- Public backfill note for the selected degreewise derived-functor statement. -/
def abelianDerivedCanonicalPublicNote : String :=
  "The public canonical degreewise statement for THM-M-0006.abelian-derived is AwesomeTheorems.Stage1.S1_M_095.AbelianDerivedCanonicalStatement: in abelian source and target categories, assuming HasProjectiveResolutions C, HasInjectiveResolutions C, and F.Additive, the degreewise functors F.leftDerived n and F.rightDerived n exist as mathlib named functors for every n : Nat; total derived functors remain a separate Kan-extension branch."

/-- Checked wrapper: higher left-derived functors vanish on projective objects. -/
theorem isZero_leftDerived_obj_projective_succ [HasProjectiveResolutions C]
    (F : C ⥤ D) [F.Additive] (n : ℕ) (X : C) [Projective X] :
    IsZero ((F.leftDerived (n + 1)).obj X) :=
  Functor.isZero_leftDerived_obj_projective_succ F n X

/-- Checked wrapper: higher right-derived functors vanish on injective objects. -/
theorem isZero_rightDerived_obj_injective_succ [HasInjectiveResolutions C]
    (F : C ⥤ D) [F.Additive] (n : ℕ) (X : C) [Injective X] :
    IsZero ((F.rightDerived (n + 1)).obj X) :=
  Functor.isZero_rightDerived_obj_injective_succ F n X

/--
Branch statement shape for `THM-M-0006.acyclic-objects`.

This records the standard projective/injective vanishing branch supplied by
mathlib: higher left-derived functors vanish on projective objects, and higher
right-derived functors vanish on injective objects.
-/
def AcyclicObjectsStatementShape : Prop :=
  (∀ {C : Type uC} [Category.{vC} C] [Abelian C] [HasProjectiveResolutions C]
      {D : Type uD} [Category.{vD} D] [Abelian D]
      (F : C ⥤ D) [F.Additive] (n : ℕ) (X : C) [Projective X],
      IsZero ((F.leftDerived (n + 1)).obj X)) ∧
    (∀ {C : Type uC} [Category.{vC} C] [Abelian C] [HasInjectiveResolutions C]
      {D : Type uD} [Category.{vD} D] [Abelian D]
      (F : C ⥤ D) [F.Additive] (n : ℕ) (X : C) [Injective X],
      IsZero ((F.rightDerived (n + 1)).obj X))

/-- The acyclic-objects branch is checked by mathlib's projective/injective vanishing lemmas. -/
theorem acyclicObjectsStatementShape_checked :
    AcyclicObjectsStatementShape.{uC, vC, uD, vD} := by
  constructor
  · intro C _ _ _ D _ _ F _ n X _
    exact isZero_leftDerived_obj_projective_succ F n X
  · intro C _ _ _ D _ _ F _ n X _
    exact isZero_rightDerived_obj_injective_succ F n X

/-- Public backfill note for the acyclic-objects branch. -/
def acyclicObjectsPublicNote : String :=
  "THM-M-0006.acyclic-objects is backfilled repo-locally by AwesomeTheorems.Stage1.S1_M_095.AcyclicObjectsStatementShape and acyclicObjectsStatementShape_checked, using the pinned mathlib lemmas Functor.isZero_leftDerived_obj_projective_succ and Functor.isZero_rightDerived_obj_injective_succ. The left vanishing branch assumes HasProjectiveResolutions C, F.Additive, and Projective X; the right vanishing branch assumes HasInjectiveResolutions C, F.Additive, and Injective X. This is a checked branch wrapper, not a terminal completion claim for THM-M-0006."

/-- Checked wrapper: a right-exact additive functor agrees with its zeroth left-derived functor. -/
def leftDerivedZeroIsoSelf [HasProjectiveResolutions C]
    (F : C ⥤ D) [F.Additive] [PreservesFiniteColimits F] :
    F.leftDerived 0 ≅ F :=
  F.leftDerivedZeroIsoSelf

/-- Checked wrapper: a left-exact additive functor agrees with its zeroth right-derived functor. -/
def rightDerivedZeroIsoSelf [HasInjectiveResolutions C]
    (F : C ⥤ D) [F.Additive] [PreservesFiniteLimits F] :
    F.rightDerived 0 ≅ F :=
  F.rightDerivedZeroIsoSelf

/--
Branch statement shape for `THM-M-0006.zero-degree`.

This records the standard zeroth comparison branch supplied by mathlib:
right-exact additive functors agree with their zeroth left-derived functor, and
left-exact additive functors agree with their zeroth right-derived functor.
-/
def ZeroDegreeComparisonStatementShape : Prop :=
  (∀ {C : Type uC} [Category.{vC} C] [Abelian C] [HasProjectiveResolutions C]
      {D : Type uD} [Category.{vD} D] [Abelian D]
      (F : C ⥤ D) [F.Additive] [PreservesFiniteColimits F],
      Nonempty (F.leftDerived 0 ≅ F)) ∧
    (∀ {C : Type uC} [Category.{vC} C] [Abelian C] [HasInjectiveResolutions C]
      {D : Type uD} [Category.{vD} D] [Abelian D]
      (F : C ⥤ D) [F.Additive] [PreservesFiniteLimits F],
      Nonempty (F.rightDerived 0 ≅ F))

/-- The zero-degree comparison branch is checked by mathlib's zeroth isomorphisms. -/
theorem zeroDegreeComparisonStatementShape_checked :
    ZeroDegreeComparisonStatementShape.{uC, vC, uD, vD} := by
  constructor
  · intro C _ _ _ D _ _ F _ _
    exact ⟨F.leftDerivedZeroIsoSelf⟩
  · intro C _ _ _ D _ _ F _ _
    exact ⟨F.rightDerivedZeroIsoSelf⟩

/-- Checked triangle identity for the zeroth left-derived comparison isomorphism. -/
theorem leftDerivedZeroIsoSelf_hom_inv_id [HasProjectiveResolutions C]
    (F : C ⥤ D) [F.Additive] [PreservesFiniteColimits F] :
    F.fromLeftDerivedZero ≫ F.leftDerivedZeroIsoSelf.inv = 𝟙 _ :=
  F.leftDerivedZeroIsoSelf_hom_inv_id

/-- Checked triangle identity for the zeroth right-derived comparison isomorphism. -/
theorem rightDerivedZeroIsoSelf_hom_inv_id [HasInjectiveResolutions C]
    (F : C ⥤ D) [F.Additive] [PreservesFiniteLimits F] :
    F.rightDerivedZeroIsoSelf.hom ≫ F.toRightDerivedZero = 𝟙 _ :=
  F.rightDerivedZeroIsoSelf_hom_inv_id

/-- Public backfill note for the zero-degree comparison branch. -/
def zeroDegreeComparisonPublicNote : String :=
  "THM-M-0006.zero-degree is backfilled repo-locally by AwesomeTheorems.Stage1.S1_M_095.ZeroDegreeComparisonStatementShape and zeroDegreeComparisonStatementShape_checked, using the pinned mathlib isomorphisms Functor.leftDerivedZeroIsoSelf and Functor.rightDerivedZeroIsoSelf. The left comparison assumes HasProjectiveResolutions C, F.Additive, and PreservesFiniteColimits F; the right comparison assumes HasInjectiveResolutions C, F.Additive, and PreservesFiniteLimits F. This is a checked branch wrapper, not a terminal completion claim for THM-M-0006."

/-- Checked wrapper: natural transformations induce maps on left-derived functors. -/
def leftDerivedNatTrans [HasProjectiveResolutions C]
    {F G : C ⥤ D} [F.Additive] [G.Additive] (α : F ⟶ G) (n : ℕ) :
    F.leftDerived n ⟶ G.leftDerived n :=
  NatTrans.leftDerived α n

/-- Checked wrapper: natural transformations induce maps on right-derived functors. -/
def rightDerivedNatTrans [HasInjectiveResolutions C]
    {F G : C ⥤ D} [F.Additive] [G.Additive] (α : F ⟶ G) (n : ℕ) :
    F.rightDerived n ⟶ G.rightDerived n :=
  NatTrans.rightDerived α n

end AbelianResolutionDerived

section TotalKanDerived

variable {C : Type uC} {D : Type uD} {H : Type uH}
variable [Category.{vC} C] [Category.{vD} D] [Category.{vH} H]
variable (F : C ⥤ H) (L : C ⥤ D) (W : MorphismProperty C)

/--
Category-level total-derived-functor statement shape.

Mathlib models total derived functors as Kan extensions along a localization.
This shape records the local theorem that, once the relevant localization and
Kan-extension existence typeclasses are available, the total left/right derived
functors and their universal natural transformations are present.
-/
def TotalKanStatementShape : Prop :=
  ∀ {C : Type uC} {D : Type uD} {H : Type uH}
    [Category.{vC} C] [Category.{vD} D] [Category.{vH} H]
    (F : C ⥤ H) (L : C ⥤ D) (W : MorphismProperty C) [L.IsLocalization W],
      (F.HasLeftDerivedFunctor W →
        ∃ (LF : D ⥤ H) (α : L ⋙ LF ⟶ F), LF.IsLeftDerivedFunctor α W) ∧
      (F.HasRightDerivedFunctor W →
        ∃ (RF : D ⥤ H) (β : F ⟶ L ⋙ RF), RF.IsRightDerivedFunctor β W)

/-- The total-Kan statement shape is witnessed by mathlib's total derived functors. -/
theorem totalKanStatementShape_checked :
    TotalKanStatementShape.{uC, vC, uD, vD, uH, vH} := by
  intro C D H _ _ _ F L W hL
  constructor
  · intro hF
    letI := hF
    refine ⟨F.totalLeftDerived L W, F.totalLeftDerivedCounit L W, ?_⟩
    infer_instance
  · intro hF
    letI := hF
    refine ⟨F.totalRightDerived L W, F.totalRightDerivedUnit L W, ?_⟩
    infer_instance

/--
Public child statement for `THM-M-0006.total-derived`.

The total-derived branch should remain a separate Kan-extension child theorem,
not the canonical terminal statement for the whole derived-functor theorem.  The
reason is that mathlib's total-derived API starts from a localization and the
existence classes `F.HasLeftDerivedFunctor W` and `F.HasRightDerivedFunctor W`.
Those hypotheses give a checked total-derived object model, but they do not by
themselves close the degreewise abelian-resolution branch, comparison theorems,
long exact sequence package, or a single terminal theorem for all intended
homological settings.
-/
def TotalDerivedSeparateChildStatement : Prop :=
  TotalKanStatementShape.{uC, vC, uD, vD, uH, vH}

/-- The selected total-derived child statement is checked by mathlib's total Kan API. -/
theorem totalDerivedSeparateChildStatement_checked :
    TotalDerivedSeparateChildStatement.{uC, vC, uD, vD, uH, vH} :=
  totalKanStatementShape_checked

/-- Machine-readable decision: total derived functors stay as a separate child branch. -/
def totalDerivedShouldBeSeparateChild : Bool :=
  true

/-- Machine-readable decision: total Kan-derived functors alone are not the terminal theorem. -/
def totalDerivedIsCanonicalTerminalStatement : Bool :=
  false

theorem totalDerivedShouldBeSeparateChild_eq_true :
    totalDerivedShouldBeSeparateChild = true :=
  rfl

theorem totalDerivedIsCanonicalTerminalStatement_eq_false :
    totalDerivedIsCanonicalTerminalStatement = false :=
  rfl

/-- Public backfill note for the total-derived child decision. -/
def totalDerivedSeparateChildPublicNote : String :=
  "For THM-M-0006.total-derived, total derived functors as Kan extensions along localization should remain a separate child theorem, represented by AwesomeTheorems.Stage1.S1_M_095.TotalDerivedSeparateChildStatement, and should not be used alone as the canonical terminal statement for THM-M-0006. The checked mathlib API assumes L.IsLocalization W and F.HasLeftDerivedFunctor W or F.HasRightDerivedFunctor W, so it validates the total Kan-extension branch but does not close the degreewise abelian-resolution branch, comparison/naturality branches, long-exact sequence branch, or the parent integration gate."

/-- Checked wrapper: existence of the total left derived functor from mathlib hypotheses. -/
theorem exists_total_left_derived [L.IsLocalization W] [F.HasLeftDerivedFunctor W] :
    ∃ (LF : D ⥤ H) (α : L ⋙ LF ⟶ F), LF.IsLeftDerivedFunctor α W := by
  refine ⟨F.totalLeftDerived L W, F.totalLeftDerivedCounit L W, ?_⟩
  infer_instance

/-- Checked wrapper: existence of the total right derived functor from mathlib hypotheses. -/
theorem exists_total_right_derived [L.IsLocalization W] [F.HasRightDerivedFunctor W] :
    ∃ (RF : D ⥤ H) (β : F ⟶ L ⋙ RF), RF.IsRightDerivedFunctor β W := by
  refine ⟨F.totalRightDerived L W, F.totalRightDerivedUnit L W, ?_⟩
  infer_instance

/-- Checked wrapper: the naturality square for morphisms of total left derived functors. -/
theorem leftDerived_naturality_square
    {LF' LF : D ⥤ H} {F' F : C ⥤ H} {L : C ⥤ D}
    {α' : L ⋙ LF' ⟶ F'} {α : L ⋙ LF ⟶ F}
    (W : MorphismProperty C) [L.IsLocalization W]
    [LF.IsLeftDerivedFunctor α W] (τ : F' ⟶ F) (X : C) :
    (Functor.leftDerivedNatTrans LF' LF α' α W τ).app (L.obj X) ≫ α.app X =
      α'.app X ≫ τ.app X :=
  Functor.leftDerivedNatTrans_app LF' LF α' α W τ X

/-- Checked wrapper: the naturality square for morphisms of total right derived functors. -/
theorem rightDerived_naturality_square
    {RF RF' : D ⥤ H} {F F' : C ⥤ H} {L : C ⥤ D}
    {α : F ⟶ L ⋙ RF} {α' : F' ⟶ L ⋙ RF'}
    (W : MorphismProperty C) [L.IsLocalization W]
    [RF.IsRightDerivedFunctor α W] (τ : F ⟶ F') (X : C) :
    α.app X ≫ (Functor.rightDerivedNatTrans RF RF' α α' W τ).app (L.obj X) =
      τ.app X ≫ α'.app X :=
  Functor.rightDerivedNatTrans_app RF RF' α α' W τ X

/--
Branch statement shape for `THM-M-0006.naturality`.

This records the two total-derived naturality squares supplied by mathlib:
`Functor.leftDerivedNatTrans_app` for left derived functors and
`Functor.rightDerivedNatTrans_app` for right derived functors.  It is a checked
branch wrapper, not a terminal theorem for all derived-functor infrastructure.
-/
def NaturalitySquareStatementShape : Prop :=
  (∀ {C : Type uC} {D : Type uD} {H : Type uH}
      [Category.{vC} C] [Category.{vD} D] [Category.{vH} H]
      {LF' LF : D ⥤ H} {F' F : C ⥤ H} {L : C ⥤ D}
      {α' : L ⋙ LF' ⟶ F'} {α : L ⋙ LF ⟶ F}
      (W : MorphismProperty C) [L.IsLocalization W]
      [LF.IsLeftDerivedFunctor α W] (τ : F' ⟶ F) (X : C),
      (Functor.leftDerivedNatTrans LF' LF α' α W τ).app (L.obj X) ≫ α.app X =
        α'.app X ≫ τ.app X) ∧
    (∀ {C : Type uC} {D : Type uD} {H : Type uH}
      [Category.{vC} C] [Category.{vD} D] [Category.{vH} H]
      {RF RF' : D ⥤ H} {F F' : C ⥤ H} {L : C ⥤ D}
      {α : F ⟶ L ⋙ RF} {α' : F' ⟶ L ⋙ RF'}
      (W : MorphismProperty C) [L.IsLocalization W]
      [RF.IsRightDerivedFunctor α W] (τ : F ⟶ F') (X : C),
      α.app X ≫ (Functor.rightDerivedNatTrans RF RF' α α' W τ).app (L.obj X) =
        τ.app X ≫ α'.app X)

/-- The naturality-square branch is checked by mathlib's total-derived app lemmas. -/
theorem naturalitySquareStatementShape_checked :
    NaturalitySquareStatementShape.{uC, vC, uD, vD, uH, vH} := by
  constructor
  · intro C D H _ _ _ LF' LF F' F L α' α W _ _ τ X
    exact leftDerived_naturality_square W τ X
  · intro C D H _ _ _ RF RF' F F' L α α' W _ _ τ X
    exact rightDerived_naturality_square W τ X

/-- Public backfill note for the total-derived naturality-square branch. -/
def naturalitySquarePublicNote : String :=
  "THM-M-0006.naturality is backfilled repo-locally by AwesomeTheorems.Stage1.S1_M_095.NaturalitySquareStatementShape and naturalitySquareStatementShape_checked, using the pinned mathlib lemmas Functor.leftDerivedNatTrans_app and Functor.rightDerivedNatTrans_app for total left and right derived functors. This is a checked branch wrapper, not a terminal completion claim for THM-M-0006."

end TotalKanDerived

section LongExactSequence

/--
Checked wrapper: the middle three homology terms of a short exact sequence of
homological complexes form an exact composable-arrow sequence.
-/
def shortExactHomologySequence₂
    {A : Type uC} [Category.{vC} A] [Abelian A]
    {ι : Type uD} {c : ComplexShape ι}
    {S : ShortComplex (HomologicalComplex A c)} (hS : S.ShortExact) (i : ι) :=
  HomologicalComplex.HomologySequence.composableArrows₂_exact hS i

/--
Checked wrapper: a short exact sequence of homological complexes gives the
five-arrow segment around the connecting homomorphism in the long exact
homology sequence.
-/
def shortExactHomologySequence₅
    {A : Type uC} [Category.{vC} A] [Abelian A]
    {ι : Type uD} {c : ComplexShape ι}
    {S : ShortComplex (HomologicalComplex A c)} (hS : S.ShortExact)
    (i j : ι) (hij : c.Rel i j) :=
  HomologicalComplex.HomologySequence.composableArrows₅_exact hS i j hij

/-- Checked wrapper: the derived-category connecting morphism composes to zero on the left. -/
theorem derivedCategoryHomologySequence_comp_δ
    {A : Type uC} [Category.{vC} A] [Abelian A] [HasDerivedCategory.{uH} A]
    (T : Triangle (DerivedCategory A)) (hT : T ∈ distTriang _)
    (n₀ n₁ : ℤ) (h : n₀ + 1 = n₁ := by omega) :
    (DerivedCategory.homologyFunctor A n₀).map T.mor₂ ≫
      DerivedCategory.HomologySequence.δ T n₀ n₁ h = 0 :=
  DerivedCategory.HomologySequence.comp_δ T hT n₀ n₁ h

/-- Checked wrapper: the derived-category connecting morphism composes to zero on the right. -/
theorem derivedCategoryHomologySequence_δ_comp
    {A : Type uC} [Category.{vC} A] [Abelian A] [HasDerivedCategory.{uH} A]
    (T : Triangle (DerivedCategory A)) (hT : T ∈ distTriang _)
    (n₀ n₁ : ℤ) (h : n₀ + 1 = n₁ := by omega) :
    DerivedCategory.HomologySequence.δ T n₀ n₁ h ≫
      (DerivedCategory.homologyFunctor A n₁).map T.mor₁ = 0 :=
  DerivedCategory.HomologySequence.δ_comp T hT n₀ n₁ h

/-- Checked wrapper: exactness at the first term after the connecting morphism. -/
theorem derivedCategoryHomologySequence_exact₁
    {A : Type uC} [Category.{vC} A] [Abelian A] [HasDerivedCategory.{uH} A]
    (T : Triangle (DerivedCategory A)) (hT : T ∈ distTriang _)
    (n₀ n₁ : ℤ) (h : n₀ + 1 = n₁ := by omega) :
    (ShortComplex.mk _ _ (DerivedCategory.HomologySequence.δ_comp T hT n₀ n₁ h)).Exact :=
  DerivedCategory.HomologySequence.exact₁ T hT n₀ n₁ h

/-- Checked wrapper: exactness of the same-degree two-map homology segment. -/
def derivedCategoryHomologySequence_exact₂
    {A : Type uC} [Category.{vC} A] [Abelian A] [HasDerivedCategory.{uH} A]
    (T : Triangle (DerivedCategory A)) (hT : T ∈ distTriang _) (n : ℤ) :=
  DerivedCategory.HomologySequence.exact₂ T hT n

/-- Checked wrapper: exactness at the connecting morphism. -/
theorem derivedCategoryHomologySequence_exact₃
    {A : Type uC} [Category.{vC} A] [Abelian A] [HasDerivedCategory.{uH} A]
    (T : Triangle (DerivedCategory A)) (hT : T ∈ distTriang _)
    (n₀ n₁ : ℤ) (h : n₀ + 1 = n₁ := by omega) :
    (ShortComplex.mk _ _ (DerivedCategory.HomologySequence.comp_δ T hT n₀ n₁ h)).Exact :=
  DerivedCategory.HomologySequence.exact₃ T hT n₀ n₁ h

/--
Branch statement shape for `THM-M-0006.long-exact`.

This aligns the short-exact and derived-category long-exact sequence branch
with the two pinned mathlib modules.  The short-exact side uses
`HomologicalComplex.HomologySequence.composableArrows₂_exact` and
`HomologicalComplex.HomologySequence.composableArrows₅_exact`; the
derived-category side uses `DerivedCategory.HomologySequence.comp_δ`,
`δ_comp`, `exact₁`, `exact₂`, and `exact₃`.
-/
def LongExactSequenceStatementShape : Prop :=
  (∀ {A : Type uC} [Category.{vC} A] [Abelian A]
      {ι : Type uD} {c : ComplexShape ι}
      {S : ShortComplex (HomologicalComplex A c)} (_hS : S.ShortExact) (i : ι),
      Nonempty ((HomologicalComplex.HomologySequence.composableArrows₂ S i).Exact)) ∧
    (∀ {A : Type uC} [Category.{vC} A] [Abelian A]
      {ι : Type uD} {c : ComplexShape ι}
      {S : ShortComplex (HomologicalComplex A c)} (hS : S.ShortExact)
      (i j : ι) (hij : c.Rel i j),
      Nonempty ((HomologicalComplex.HomologySequence.composableArrows₅ hS i j hij).Exact)) ∧
    (∀ {A : Type uC} [Category.{vC} A] [Abelian A] [HasDerivedCategory.{uH} A]
      (T : Triangle (DerivedCategory A)) (hT : T ∈ distTriang _)
      (n₀ n₁ : ℤ) (h : n₀ + 1 = n₁),
      (DerivedCategory.homologyFunctor A n₀).map T.mor₂ ≫
        DerivedCategory.HomologySequence.δ T n₀ n₁ h = 0 ∧
      DerivedCategory.HomologySequence.δ T n₀ n₁ h ≫
        (DerivedCategory.homologyFunctor A n₁).map T.mor₁ = 0 ∧
      Nonempty ((ShortComplex.mk _ _
        (DerivedCategory.HomologySequence.δ_comp T hT n₀ n₁ h)).Exact) ∧
      Nonempty ((ShortComplex.mk _ _
        (DerivedCategory.HomologySequence.comp_δ T hT n₀ n₁ h)).Exact))

/-- The long-exact branch is checked by the pinned mathlib homology-sequence APIs. -/
theorem longExactSequenceStatementShape_checked :
    LongExactSequenceStatementShape.{uC, vC, uD, uH} := by
  constructor
  · intro A _ _ ι c S hS i
    exact ⟨shortExactHomologySequence₂ hS i⟩
  constructor
  · intro A _ _ ι c S hS i j hij
    exact ⟨shortExactHomologySequence₅ hS i j hij⟩
  · intro A _ _ _ T hT n₀ n₁ h
    exact ⟨derivedCategoryHomologySequence_comp_δ T hT n₀ n₁ h,
      derivedCategoryHomologySequence_δ_comp T hT n₀ n₁ h,
      ⟨derivedCategoryHomologySequence_exact₁ T hT n₀ n₁ h⟩,
      ⟨derivedCategoryHomologySequence_exact₃ T hT n₀ n₁ h⟩⟩

/-- Public backfill note for the short-exact/long-exact sequence branch. -/
def longExactSequencePublicNote : String :=
  "THM-M-0006.long-exact is backfilled repo-locally by AwesomeTheorems.Stage1.S1_M_095.LongExactSequenceStatementShape and longExactSequenceStatementShape_checked. The short-exact complex branch uses Mathlib.Algebra.Homology.HomologySequenceLemmas via HomologicalComplex.HomologySequence.composableArrows₂_exact and composableArrows₅_exact. The derived-category distinguished-triangle branch uses Mathlib.Algebra.Homology.DerivedCategory.HomologySequence via DerivedCategory.HomologySequence.comp_δ, δ_comp, exact₁, exact₂, and exact₃. This is a checked branch wrapper, not a terminal completion claim for THM-M-0006."

end LongExactSequence

/-- Combined Stage1 statement-shape target for this slot. -/
def StatementShape : Prop :=
  AbelianResolutionStatementShape.{uC, vC, uD, vD} ∧
    AcyclicObjectsStatementShape.{uC, vC, uD, vD} ∧
      ZeroDegreeComparisonStatementShape.{uC, vC, uD, vD} ∧
        TotalKanStatementShape.{uC, vC, uD, vD, uH, vH} ∧
          NaturalitySquareStatementShape.{uC, vC, uD, vD, uH, vH} ∧
            LongExactSequenceStatementShape.{uC, vC, uD, uH}

/--
Public Stage1 status note for `THM-M-0006.statement`.

`StatementShape` is a compiled statement-shape/wrapper artifact over pinned
mathlib derived-functor APIs.  It is not a completed terminal theorem for the
full derived functor theorem.
-/
def statementShapePublicNote : String :=
  "AwesomeTheorems.Stage1.S1_M_095.StatementShape compiles as a statement-shape/wrapper artifact, not as a completed terminal theorem."

/-- Pinned mathlib revision audited for `THM-M-0006.mathlib-audit`. -/
def auditedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Primary mathlib anchors requested by `THM-M-0006.mathlib-audit`. -/
def primaryDerivedFunctorAnchors : List String := [
  "Functor.leftDerived",
  "Functor.rightDerived",
  "Functor.totalLeftDerived",
  "Functor.totalRightDerived"
]

/--
Public Stage1 backfill note for `THM-M-0006.mathlib-audit`.

This records the pinned mathlib revision and the four requested declaration
anchors.  The surrounding wrappers provide repo-local checks that the anchors
are available in this Lake closure, but this audit note is not by itself a
terminal proof of the full derived functor theorem.
-/
def mathlibAuditPublicNote : String :=
  "Pinned mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95 exposes anchors Functor.leftDerived, Functor.rightDerived, Functor.totalLeftDerived, and Functor.totalRightDerived; the repo-local wrappers in AwesomeTheorems.Stage1.S1_M_095 check their availability without claiming terminal theorem completion."

/--
Search queries recorded for `THM-M-0006.external-audit`.

The child audit looked for non-mathlib Lean 4 primary sources that would be
stronger than the pinned mathlib derived-functor wrappers.
-/
def externalAuditSearchQueries : List String := [
  "leftDerived language:Lean",
  "Functor.leftDerived lakefile.lean",
  "totalLeftDerived language:Lean",
  "IsLeftDerivedFunctor Lean",
  "DerivedCategory leftDerived Lean"
]

/--
Non-mathlib Lean 4 repositories found with a stronger terminal
derived-functor theorem.

This list is intentionally empty: the audit found mathlib documentation and
mathlib mirrors, but no non-mathlib primary Lean 4 theorem that can be proposed
as a stronger terminal proof for this Stage1 slot.
-/
def externalAuditStrongerTerminalSources : List String := []

/-- Lake-closure decision for the external audit branch. -/
def externalAuditLakeClosureDecision : String :=
  "No non-mathlib Lean 4 external project is proposed for this Lake closure: no stronger terminal derived-functor theorem was located. The parent remains a repo-local mathlib-wrapper statement-shape artifact, not a completed terminal theorem."

/-- Public backfill note for `THM-M-0006.external-audit`. -/
def externalAuditPublicNote : String :=
  "THM-M-0006.external-audit found no non-mathlib Lean 4 primary source with a stronger terminal derived-functor existence theorem than the pinned mathlib APIs already wrapped in AwesomeTheorems.Stage1.S1_M_095. Search hits either resolved to mathlib itself or to external documentation mirrors whose source links point back to mathlib. Therefore no external project is proposed for Lake closure, no external_upstream_pinned status is claimed, and the parent integration gate remains open."

/--
Machine-readable local validation status for the terminal theorem.

The current artifact validates checked branch wrappers and statement shapes, but
it does not provide a repo-local terminal theorem for the whole derived-functor
theorem.
-/
def terminalTheoremLocalValidationPassed : Bool :=
  false

/--
Machine-readable status for a pinned external terminal proof.

The external audit did not locate a stronger non-mathlib Lean 4 terminal proof
that has been imported into this Lake closure.
-/
def pinnedExternalTerminalProofImportedAndChecked : Bool :=
  false

/-- Machine-readable gate policy: anchor-only external evidence is not enough. -/
def anchorOnlyExternalEvidenceSufficientForCompletion : Bool :=
  false

/--
Completion gate for `THM-M-0006.integration-gate`.

This gate can only be satisfied by a locally validated terminal theorem or by a
pinned external terminal proof that has been imported and checked in this Lake
closure.
-/
def IntegrationGateSatisfied : Prop :=
  terminalTheoremLocalValidationPassed = true ∨
    pinnedExternalTerminalProofImportedAndChecked = true

/-- The current Stage1 artifact does not satisfy the terminal completion gate. -/
theorem integrationGate_not_satisfied : ¬ IntegrationGateSatisfied := by
  intro h
  cases h with
  | inl hLocal => cases hLocal
  | inr hExternal => cases hExternal

/-- Checked policy fact: anchor-only external evidence is insufficient. -/
theorem anchorOnlyExternalEvidenceSufficientForCompletion_eq_false :
    anchorOnlyExternalEvidenceSufficientForCompletion = false :=
  rfl

/-- Public backfill note for `THM-M-0006.integration-gate`. -/
def integrationGatePublicNote : String :=
  "THM-M-0006.integration-gate remains open: AwesomeTheorems.Stage1.S1_M_095 validates branch wrappers and statement-shape artifacts, but no repo-local terminal theorem has passed validation and no pinned external terminal proof has been imported and checked. Anchor-only external evidence is explicitly insufficient for completion."

/-- Checked combined wrapper for the currently available mathlib-derived-functor API. -/
theorem statementShape_checked :
    StatementShape.{uC, vC, uD, vD, uH, vH} :=
  ⟨abelianResolutionStatementShape_checked, acyclicObjectsStatementShape_checked,
    zeroDegreeComparisonStatementShape_checked, totalKanStatementShape_checked,
    naturalitySquareStatementShape_checked, longExactSequenceStatementShape_checked⟩

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.CategoryTheory.Abelian.LeftDerived",
  "Mathlib.CategoryTheory.Abelian.RightDerived",
  "Mathlib.CategoryTheory.Functor.Derived.LeftDerived",
  "Mathlib.CategoryTheory.Functor.Derived.RightDerived",
  "Mathlib.CategoryTheory.Functor.Derived.PointwiseLeftDerived",
  "Mathlib.CategoryTheory.Functor.Derived.PointwiseRightDerived",
  "Mathlib.CategoryTheory.Functor.Derived.Adjunction",
  "Mathlib.Algebra.Homology.HomologySequenceLemmas",
  "Mathlib.Algebra.Homology.DerivedCategory.HomologySequence"
]

/-- Search terms and terminal gaps checked for the Stage1 audit ledger. -/
def anchorSearchTerms : List String := [
  "Functor.leftDerived",
  "Functor.rightDerived",
  "Functor.totalLeftDerived",
  "Functor.totalRightDerived",
  "Functor.leftDerivedZeroIsoSelf",
  "Functor.rightDerivedZeroIsoSelf",
  "HasLeftDerivedFunctor",
  "HasRightDerivedFunctor",
  "IsLeftDerivedFunctor",
  "IsRightDerivedFunctor",
  "Functor.leftDerivedNatTrans_app",
  "Functor.rightDerivedNatTrans_app",
  "HomologicalComplex.HomologySequence.composableArrows₂_exact",
  "HomologicalComplex.HomologySequence.composableArrows₅_exact",
  "DerivedCategory.HomologySequence.comp_δ",
  "DerivedCategory.HomologySequence.δ_comp",
  "DerivedCategory.HomologySequence.exact₁",
  "DerivedCategory.HomologySequence.exact₂",
  "DerivedCategory.HomologySequence.exact₃",
  "HasProjectiveResolutions",
  "HasInjectiveResolutions",
  "THM-M-0006.integration-gate",
  "terminal theorem local validation",
  "pinned external terminal proof imported and checked",
  "derived category total derived functor",
  "long exact sequence derived functor"
]

end S1_M_095
end Stage1
end AwesomeTheorems
