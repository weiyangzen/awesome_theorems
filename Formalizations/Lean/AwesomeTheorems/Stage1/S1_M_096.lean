import Mathlib.Algebra.Homology.HomologySequenceLemmas
import Mathlib.Algebra.Homology.DerivedCategory.HomologySequence
import Mathlib.Algebra.Homology.DerivedCategory.Ext.ExactSequences
import Mathlib.RepresentationTheory.Homological.GroupHomology.LongExactSequence
import Mathlib.RepresentationTheory.Homological.GroupCohomology.LongExactSequence

/-!
# S1-M-096 / THM-M-0001: long exact homology sequence

This Stage1 file records a checked mathlib wrapper for the theorem that a short
exact sequence of homological complexes in an abelian category induces the long
exact sequence on homology.

The pinned mathlib theorem family is local and machine-checked:

* `ShortComplex.ShortExact.δ`
* `ShortComplex.ShortExact.comp_δ`
* `ShortComplex.ShortExact.δ_comp`
* `ShortComplex.ShortExact.homology_exact₁`
* `ShortComplex.ShortExact.homology_exact₂`
* `ShortComplex.ShortExact.homology_exact₃`

This is not a public completion marker for the Stage1 slot.  It is a repo-local
wrapper around the pinned mathlib proof body; blueprint/todo integration remains
for a later serial integrator.
-/

universe v u w t

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_096

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Limits
open HomologicalComplex

variable {C : Type u} [Category.{v} C] [Abelian C]
variable {ι : Type w} {c : ComplexShape ι}
variable {S : ShortComplex (HomologicalComplex C c)}
variable (hS : S.ShortExact) {i j : ι} (hij : c.Rel i j)

/--
The three local exactness assertions and the connecting morphism supplied by
mathlib for a short exact sequence of homological complexes.

For adjacent degrees `i` and `j`, this packages the part of the long exact
homology sequence

`H_i(X₂) -> H_i(X₃) -> H_j(X₁) -> H_j(X₂)`

together with the preceding same-degree exactness

`H_i(X₁) -> H_i(X₂) -> H_i(X₃)`.
-/
structure LongExactHomologySequenceData where
  connecting : S.X₃.homology i ⟶ S.X₁.homology j
  connecting_eq_mathlib : connecting = hS.δ i j hij
  homologyMap_g_comp_connecting :
    HomologicalComplex.homologyMap S.g i ≫ connecting = 0
  connecting_comp_homologyMap_f :
    connecting ≫ HomologicalComplex.homologyMap S.f j = 0
  exact_at_source_degree :
    (ShortComplex.mk (HomologicalComplex.homologyMap S.f i)
      (HomologicalComplex.homologyMap S.g i)
      (by
        rw [← HomologicalComplex.homologyMap_comp, S.zero,
          HomologicalComplex.homologyMap_zero])).Exact
  exact_at_connecting_source :
    (ShortComplex.mk (HomologicalComplex.homologyMap S.g i) connecting
      homologyMap_g_comp_connecting).Exact
  exact_at_connecting_target :
    (ShortComplex.mk connecting (HomologicalComplex.homologyMap S.f j)
      connecting_comp_homologyMap_f).Exact

/--
Stage1 statement-shape candidate for the long exact sequence theorem.

It is intentionally indexed by the category, complex shape, short exact short
complex, and adjacent degrees.  The proposition asks only for the checked
category-level data that mathlib already provides locally.
-/
def StatementShape : Prop :=
  Nonempty (LongExactHomologySequenceData hS hij)

/-- The mathlib connecting morphism in the long exact homology sequence. -/
noncomputable abbrev connectingHomomorphism :
    S.X₃.homology i ⟶ S.X₁.homology j :=
  hS.δ i j hij

/-- The morphism `H_i(X_3) -> H_j(X_1)` composes to zero with `H_j(X_1) -> H_j(X_2)`. -/
theorem connecting_comp_first_homology_map :
    connectingHomomorphism hS hij ≫ HomologicalComplex.homologyMap S.f j = 0 := by
  exact hS.δ_comp i j hij

/-- The morphism `H_i(X_2) -> H_i(X_3)` composes to zero with the connecting morphism. -/
theorem third_homology_map_comp_connecting :
    HomologicalComplex.homologyMap S.g i ≫ connectingHomomorphism hS hij = 0 := by
  exact hS.comp_δ i j hij

/-- Exactness at `H_i(X_2)` in `H_i(X_1) -> H_i(X_2) -> H_i(X_3)`. -/
theorem homology_exact_at_source_degree (hS : S.ShortExact) :
    (ShortComplex.mk (HomologicalComplex.homologyMap S.f i)
      (HomologicalComplex.homologyMap S.g i)
      (by
        rw [← HomologicalComplex.homologyMap_comp, S.zero,
          HomologicalComplex.homologyMap_zero])).Exact := by
  exact CategoryTheory.ShortComplex.ShortExact.homology_exact₂ hS i

/-- Exactness at `H_i(X_3)` in `H_i(X_2) -> H_i(X_3) -> H_j(X_1)`. -/
theorem homology_exact_at_connecting_source :
    (ShortComplex.mk (HomologicalComplex.homologyMap S.g i)
      (connectingHomomorphism hS hij)
      (third_homology_map_comp_connecting hS hij)).Exact := by
  exact hS.homology_exact₃ i j hij

/-- Exactness at `H_j(X_1)` in `H_i(X_3) -> H_j(X_1) -> H_j(X_2)`. -/
theorem homology_exact_at_connecting_target :
    (ShortComplex.mk (connectingHomomorphism hS hij)
      (HomologicalComplex.homologyMap S.f j)
      (connecting_comp_first_homology_map hS hij)).Exact := by
  exact hS.homology_exact₁ i j hij

/-- Checked construction of the Stage1 statement-shape data from the pinned mathlib API. -/
noncomputable def mathlib_long_exact_homology_sequence_data :
    LongExactHomologySequenceData hS hij where
  connecting := connectingHomomorphism hS hij
  connecting_eq_mathlib := rfl
  homologyMap_g_comp_connecting := third_homology_map_comp_connecting hS hij
  connecting_comp_homologyMap_f := connecting_comp_first_homology_map hS hij
  exact_at_source_degree :=
    homology_exact_at_source_degree (i := i) hS
  exact_at_connecting_source :=
    homology_exact_at_connecting_source hS hij
  exact_at_connecting_target :=
    homology_exact_at_connecting_target hS hij

/-- The checked wrapper proves the local Stage1 statement-shape proposition. -/
theorem statementShape_from_mathlib : StatementShape hS hij :=
  ⟨mathlib_long_exact_homology_sequence_data hS hij⟩

/--
The checked six-term window used by the public `LES.1`--`LES.6` theorem-tree
backfill:

`H_i(X₁) -> H_i(X₂) -> H_i(X₃) -> H_j(X₁) -> H_j(X₂) -> H_j(X₃)`.
-/
theorem six_term_long_exact_sequence :
    (HomologicalComplex.HomologySequence.composableArrows₅ hS i j hij).Exact := by
  exact HomologicalComplex.HomologySequence.composableArrows₅_exact hS i j hij

/-- The connecting morphism is mono when the middle homology at the source degree vanishes. -/
theorem connecting_mono_of_middle_homology_source_zero
    (hi : IsZero (S.X₂.homology i)) : Mono (connectingHomomorphism hS hij) := by
  exact hS.mono_δ i j hij hi

/-- The connecting morphism is epi when the middle homology at the target degree vanishes. -/
theorem connecting_epi_of_middle_homology_target_zero
    (hj : IsZero (S.X₂.homology j)) : Epi (connectingHomomorphism hS hij) := by
  exact hS.epi_δ i j hij hj

/-- The connecting morphism is an isomorphism when both adjacent middle homology objects vanish. -/
theorem connecting_isIso_of_middle_homology_zero
    (hi : IsZero (S.X₂.homology i)) (hj : IsZero (S.X₂.homology j)) :
    IsIso (connectingHomomorphism hS hij) := by
  exact hS.isIso_δ i j hij hi hj

/-- The mathlib isomorphism consequence of the connecting morphism. -/
noncomputable abbrev connectingIsoOfMiddleHomologyZero
    (hi : IsZero (S.X₂.homology i)) (hj : IsZero (S.X₂.homology j)) :
    S.X₃.homology i ≅ S.X₁.homology j :=
  hS.δIso i j hij hi hj

/-- The opcycles/cycles form of the boundary-value computation for the connecting morphism. -/
theorem connecting_eq_from_opcycles {A : C}
    (x₃ : A ⟶ S.X₃.homology i) (x₂ : A ⟶ S.X₂.opcycles i)
    (x₁ : A ⟶ S.X₁.cycles j)
    (h₂ : x₂ ≫ HomologicalComplex.opcyclesMap S.g i = x₃ ≫ S.X₃.homologyι i)
    (h₁ : x₁ ≫ HomologicalComplex.cyclesMap S.f j = x₂ ≫ S.X₂.opcyclesToCycles i j) :
    x₃ ≫ connectingHomomorphism hS hij = x₁ ≫ S.X₁.homologyπ j := by
  exact hS.δ_eq' i j hij x₃ x₂ x₁ h₂ h₁

/-- The boundary-value computation for the connecting morphism, as supplied by mathlib. -/
theorem connecting_eq_boundary_formula {A : C}
    (x₃ : A ⟶ S.X₃.X i) (hx₃ : x₃ ≫ S.X₃.d i j = 0)
    (x₂ : A ⟶ S.X₂.X i) (hx₂ : x₂ ≫ S.g.f i = x₃)
    (x₁ : A ⟶ S.X₁.X j) (hx₁ : x₁ ≫ S.f.f j = x₂ ≫ S.X₂.d i j)
    (k : ι) (hk : c.next j = k) :
    S.X₃.liftCycles x₃ j (c.next_eq' hij) hx₃ ≫ S.X₃.homologyπ i ≫
        connectingHomomorphism hS hij =
      S.X₁.liftCycles x₁ k hk (by
        have := hS.mono_f
        rw [← cancel_mono (S.f.f k), assoc, ← S.f.comm, reassoc_of% hx₁,
          d_comp_d, comp_zero, zero_comp]) ≫ S.X₁.homologyπ j := by
  exact hS.δ_eq i j hij x₃ hx₃ x₂ hx₂ x₁ hx₁ k hk

/--
Primary machine anchor requested by the Stage1 public backfill task for the long
exact homology sequence.
-/
def primaryMachineAnchorModule : String :=
  "Mathlib.Algebra.Homology.HomologySequence"

/-- Canonical mathlib theorem names for the primary long exact sequence anchor. -/
def primaryMachineAnchorTheorems : List String := [
  "ShortComplex.ShortExact.δ",
  "ShortComplex.ShortExact.comp_δ",
  "ShortComplex.ShortExact.δ_comp",
  "ShortComplex.ShortExact.homology_exact₁",
  "ShortComplex.ShortExact.homology_exact₂",
  "ShortComplex.ShortExact.homology_exact₃"
]

/-- Integration-ready public theorem-tree package metadata for `LES.1` through `LES.8`. -/
structure PublicTheoremTreePackage where
  packageId : String
  status : String
  canonicalMathlibNames : List String
  repoLocalWitnesses : List String
  m0387Boundary : String
deriving Repr

/--
Public theorem-tree backfill data for a serial integrator.

The first six packages are backed by checked declarations in this file and by
`HomologicalComplex.HomologySequence.composableArrows₅_exact`. `LES.7` is backed
by checked local wrappers for the boundary formula and isomorphism consequences.
`LES.8` is deliberately marked as a follow-up package because derived-category
triangle integration is a separate public child task.
-/
def publicTheoremTreePackages : List PublicTheoremTreePackage := [
  {
    packageId := "LES.1",
    status := "checked-local-wrapper",
    canonicalMathlibNames := [
      "HomologicalComplex.HomologySequence.composableArrows₅",
      "HomologicalComplex.HomologySequence.composableArrows₅_exact"
    ],
    repoLocalWitnesses := [
      "AwesomeTheorems.Stage1.S1_M_096.LongExactHomologySequenceData",
      "AwesomeTheorems.Stage1.S1_M_096.StatementShape",
      "AwesomeTheorems.Stage1.S1_M_096.six_term_long_exact_sequence"
    ],
    m0387Boundary :=
      "Object model and hypotheses: abelian category, complex shape, short exact short complex, and adjacent degrees."
  },
  {
    packageId := "LES.2",
    status := "checked-local-wrapper",
    canonicalMathlibNames := [
      "ShortComplex.ShortExact.δ",
      "CategoryTheory.ShortComplex.ShortExact.δ"
    ],
    repoLocalWitnesses := [
      "AwesomeTheorems.Stage1.S1_M_096.connectingHomomorphism",
      "AwesomeTheorems.Stage1.S1_M_096.mathlib_long_exact_homology_sequence_data"
    ],
    m0387Boundary :=
      "Connecting morphism package for H_i(X3) -> H_j(X1)."
  },
  {
    packageId := "LES.3",
    status := "checked-local-wrapper",
    canonicalMathlibNames := [
      "ShortComplex.ShortExact.comp_δ",
      "ShortComplex.ShortExact.δ_comp",
      "CategoryTheory.ShortComplex.ShortExact.comp_δ",
      "CategoryTheory.ShortComplex.ShortExact.δ_comp"
    ],
    repoLocalWitnesses := [
      "AwesomeTheorems.Stage1.S1_M_096.third_homology_map_comp_connecting",
      "AwesomeTheorems.Stage1.S1_M_096.connecting_comp_first_homology_map"
    ],
    m0387Boundary :=
      "Zero-composition gates around the connecting morphism."
  },
  {
    packageId := "LES.4",
    status := "checked-local-wrapper",
    canonicalMathlibNames := [
      "ShortComplex.ShortExact.homology_exact₂",
      "CategoryTheory.ShortComplex.ShortExact.homology_exact₂"
    ],
    repoLocalWitnesses := [
      "AwesomeTheorems.Stage1.S1_M_096.homology_exact_at_source_degree",
      "AwesomeTheorems.Stage1.S1_M_096.six_term_long_exact_sequence"
    ],
    m0387Boundary :=
      "Exactness at H_i(X2) in H_i(X1) -> H_i(X2) -> H_i(X3)."
  },
  {
    packageId := "LES.5",
    status := "checked-local-wrapper",
    canonicalMathlibNames := [
      "ShortComplex.ShortExact.homology_exact₃",
      "CategoryTheory.ShortComplex.ShortExact.homology_exact₃"
    ],
    repoLocalWitnesses := [
      "AwesomeTheorems.Stage1.S1_M_096.homology_exact_at_connecting_source",
      "AwesomeTheorems.Stage1.S1_M_096.six_term_long_exact_sequence"
    ],
    m0387Boundary :=
      "Exactness at H_i(X3) in H_i(X2) -> H_i(X3) -> H_j(X1)."
  },
  {
    packageId := "LES.6",
    status := "checked-local-wrapper",
    canonicalMathlibNames := [
      "ShortComplex.ShortExact.homology_exact₁",
      "CategoryTheory.ShortComplex.ShortExact.homology_exact₁"
    ],
    repoLocalWitnesses := [
      "AwesomeTheorems.Stage1.S1_M_096.homology_exact_at_connecting_target",
      "AwesomeTheorems.Stage1.S1_M_096.six_term_long_exact_sequence"
    ],
    m0387Boundary :=
      "Exactness at H_j(X1) in H_i(X3) -> H_j(X1) -> H_j(X2)."
  },
  {
    packageId := "LES.7",
    status := "checked-local-wrapper",
    canonicalMathlibNames := [
      "ShortComplex.ShortExact.δ_eq",
      "ShortComplex.ShortExact.δ_eq'",
      "ShortComplex.ShortExact.mono_δ",
      "ShortComplex.ShortExact.epi_δ",
      "ShortComplex.ShortExact.isIso_δ",
      "ShortComplex.ShortExact.δIso",
      "CategoryTheory.ShortComplex.ShortExact.δ_eq",
      "CategoryTheory.ShortComplex.ShortExact.δIso"
    ],
    repoLocalWitnesses := [
      "AwesomeTheorems.Stage1.S1_M_096.connecting_eq_from_opcycles",
      "AwesomeTheorems.Stage1.S1_M_096.connecting_eq_boundary_formula",
      "AwesomeTheorems.Stage1.S1_M_096.connecting_mono_of_middle_homology_source_zero",
      "AwesomeTheorems.Stage1.S1_M_096.connecting_epi_of_middle_homology_target_zero",
      "AwesomeTheorems.Stage1.S1_M_096.connecting_isIso_of_middle_homology_zero",
      "AwesomeTheorems.Stage1.S1_M_096.connectingIsoOfMiddleHomologyZero"
    ],
    m0387Boundary :=
      "Boundary computation and isomorphism consequences; upstream snakeInput proof internals remain unchecked for sub-100-step decomposition."
  },
  {
    packageId := "LES.8",
    status := "checked-local-wrapper-public-backfill-pending",
    canonicalMathlibNames := [
      "DerivedCategory.HomologySequence.δ",
      "DerivedCategory.HomologySequence.comp_δ",
      "DerivedCategory.HomologySequence.δ_comp",
      "DerivedCategory.HomologySequence.exact₁",
      "DerivedCategory.HomologySequence.exact₂",
      "DerivedCategory.HomologySequence.exact₃"
    ],
    repoLocalWitnesses := [
      "AwesomeTheorems.Stage1.S1_M_096.derivedTriangleConnectingHomomorphism",
      "AwesomeTheorems.Stage1.S1_M_096.derived_triangle_second_homology_map_comp_connecting",
      "AwesomeTheorems.Stage1.S1_M_096.derived_triangle_connecting_comp_first_homology_map",
      "AwesomeTheorems.Stage1.S1_M_096.derived_triangle_exact_at_middle_object",
      "AwesomeTheorems.Stage1.S1_M_096.derived_triangle_exact_at_connecting_source",
      "AwesomeTheorems.Stage1.S1_M_096.derived_triangle_exact_at_connecting_target",
      "AwesomeTheorems.Stage1.S1_M_096.derivedTriangleFollowUpStatus_eq_checked"
    ],
    m0387Boundary :=
      "Derived-category triangle long exact sequence branch has repo-local wrappers over pinned mathlib; public blueprint/todo merge remains for the serialized integrator."
  }
]

/-- Pinned mathlib modules checked for this Stage1 slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Algebra.Homology.HomologySequence",
  "Mathlib.Algebra.Homology.HomologySequenceLemmas",
  "Mathlib.Algebra.Homology.ShortComplex.SnakeLemma",
  "Mathlib.Algebra.Homology.ShortComplex.ShortExact",
  "Mathlib.Algebra.Homology.ExactSequence",
  "Mathlib.Algebra.Homology.DerivedCategory.HomologySequence",
  "Mathlib.Algebra.Homology.DerivedCategory.Ext.ExactSequences",
  "Mathlib.RepresentationTheory.Homological.GroupHomology.LongExactSequence",
  "Mathlib.RepresentationTheory.Homological.GroupCohomology.LongExactSequence"
]

/-- Pinned theorem names used or audited for this Stage1 slot. -/
def mathlibAnchorTheorems : List String := [
  "CategoryTheory.ShortComplex.ShortExact.δ",
  "CategoryTheory.ShortComplex.ShortExact.comp_δ",
  "CategoryTheory.ShortComplex.ShortExact.δ_comp",
  "CategoryTheory.ShortComplex.ShortExact.homology_exact₁",
  "CategoryTheory.ShortComplex.ShortExact.homology_exact₂",
  "CategoryTheory.ShortComplex.ShortExact.homology_exact₃",
  "CategoryTheory.ShortComplex.ShortExact.δ_eq",
  "CategoryTheory.ShortComplex.ShortExact.δIso",
  "HomologicalComplex.HomologySequence.mapSnakeInput",
  "HomologicalComplex.HomologySequence.δ_naturality",
  "HomologicalComplex.HomologySequence.mapComposableArrows₂",
  "HomologicalComplex.HomologySequence.mapComposableArrows₅",
  "HomologicalComplex.HomologySequence.mono_homologyMap_τ₃",
  "HomologicalComplex.HomologySequence.epi_homologyMap_τ₃",
  "HomologicalComplex.HomologySequence.isIso_homologyMap_τ₃",
  "HomologicalComplex.HomologySequence.quasiIso_τ₃",
  "DerivedCategory.HomologySequence.δ",
  "DerivedCategory.HomologySequence.exact₁",
  "DerivedCategory.HomologySequence.exact₂",
  "DerivedCategory.HomologySequence.exact₃",
  "Abelian.Ext.covariantSequence",
  "Abelian.Ext.covariantSequence_exact",
  "Abelian.Ext.covariant_sequence_exact₁",
  "Abelian.Ext.covariant_sequence_exact₂",
  "Abelian.Ext.covariant_sequence_exact₃",
  "Abelian.Ext.contravariantSequence",
  "Abelian.Ext.contravariantSequence_exact",
  "Abelian.Ext.contravariant_sequence_exact₁",
  "Abelian.Ext.contravariant_sequence_exact₂",
  "Abelian.Ext.contravariant_sequence_exact₃",
  "groupHomology.map_chainsFunctor_shortExact",
  "groupHomology.mapShortComplex₁_exact",
  "groupHomology.mapShortComplex₂_exact",
  "groupHomology.mapShortComplex₃_exact",
  "groupHomology.δ",
  "groupHomology.epi_δ_of_isZero",
  "groupHomology.mono_δ_of_isZero",
  "groupHomology.isIso_δ_of_isZero",
  "groupCohomology.map_cochainsFunctor_shortExact",
  "groupCohomology.mapShortComplex₁_exact",
  "groupCohomology.mapShortComplex₂_exact",
  "groupCohomology.mapShortComplex₃_exact",
  "groupCohomology.δ",
  "groupCohomology.epi_δ_of_isZero",
  "groupCohomology.mono_δ_of_isZero",
  "groupCohomology.isIso_δ_of_isZero"
]

section NaturalitySquareFollowUp

variable {S₁ S₂ : ShortComplex (HomologicalComplex C c)}
variable (φ : S₁ ⟶ S₂) (hS₁ : S₁.ShortExact) (hS₂ : S₂.ShortExact)

/--
Naturality of the connecting morphism for a morphism of short exact sequences
of homological complexes.

This is the checked Stage1 child wrapper for the naturality-square follow-up
anchored at `Mathlib.Algebra.Homology.HomologySequenceLemmas`.
-/
theorem connecting_homomorphism_naturality_square :
    hS₁.δ i j hij ≫ HomologicalComplex.homologyMap φ.τ₁ j =
      HomologicalComplex.homologyMap φ.τ₃ i ≫ hS₂.δ i j hij := by
  exact HomologicalComplex.HomologySequence.δ_naturality φ hS₁ hS₂ i j hij

/--
The mathlib morphism between the two same-degree three-term homology sequences
induced by a morphism of short exact sequences.
-/
noncomputable abbrev naturalityMapComposableArrows₂ :
    HomologicalComplex.HomologySequence.composableArrows₂ S₁ i ⟶
      HomologicalComplex.HomologySequence.composableArrows₂ S₂ i :=
  HomologicalComplex.HomologySequence.mapComposableArrows₂ φ i

/--
The mathlib morphism between the two six-term long exact sequence windows
induced by a morphism of short exact sequences.
-/
noncomputable abbrev naturalityMapComposableArrows₅ :
    HomologicalComplex.HomologySequence.composableArrows₅ hS₁ i j hij ⟶
      HomologicalComplex.HomologySequence.composableArrows₅ hS₂ i j hij :=
  HomologicalComplex.HomologySequence.mapComposableArrows₅ φ hS₁ hS₂ i j hij

/-- Machine-readable child status for the naturality-square follow-up. -/
def naturalitySquareFollowUpStatus : String :=
  "checked-local-wrapper-upstream-mathlib"

/-- Checked marker that the naturality-square child has a repo-local wrapper. -/
theorem naturalitySquareFollowUpStatus_eq_checked :
    naturalitySquareFollowUpStatus = "checked-local-wrapper-upstream-mathlib" := rfl

/-- M0387 boundary note for naturality consequences not yet present upstream. -/
def naturalitySquareRemainingBoundary : String :=
  "Mathlib currently supplies δ_naturality, mapComposableArrows₂, mapComposableArrows₅, and τ₃ mono/epi/isIso/quasiIso consequences; upstream notes that analogous τ₁/τ₂ consequence lemmas remain TODO."

end NaturalitySquareFollowUp

section DerivedCategoryTriangleFollowUp

open Pretriangulated

variable [HasDerivedCategory.{t} C]
variable (T : Triangle (DerivedCategory C)) (hT : T ∈ distTriang (DerivedCategory C))
variable (n₀ n₁ : ℤ) (hn : n₀ + 1 = n₁)

include hT

/--
The derived-category connecting morphism attached to a distinguished triangle.

This is the checked Stage1 child wrapper for the follow-up anchored at
`Mathlib.Algebra.Homology.DerivedCategory.HomologySequence`.
-/
noncomputable abbrev derivedTriangleConnectingHomomorphism :
    (DerivedCategory.homologyFunctor C n₀).obj T.obj₃ ⟶
      (DerivedCategory.homologyFunctor C n₁).obj T.obj₁ :=
  DerivedCategory.HomologySequence.δ T n₀ n₁ hn

/--
In the derived-category long exact homology sequence, the map
`H_n(T₂) -> H_n(T₃)` composes to zero with the connecting morphism.
-/
theorem derived_triangle_second_homology_map_comp_connecting :
    (DerivedCategory.homologyFunctor C n₀).map T.mor₂ ≫
      derivedTriangleConnectingHomomorphism T n₀ n₁ hn = 0 := by
  exact DerivedCategory.HomologySequence.comp_δ T hT n₀ n₁ hn

/--
In the derived-category long exact homology sequence, the connecting morphism
composes to zero with `H_{n+1}(T₁) -> H_{n+1}(T₂)`.
-/
theorem derived_triangle_connecting_comp_first_homology_map :
    derivedTriangleConnectingHomomorphism T n₀ n₁ hn ≫
      (DerivedCategory.homologyFunctor C n₁).map T.mor₁ = 0 := by
  exact DerivedCategory.HomologySequence.δ_comp T hT n₀ n₁ hn

/--
Exactness at the middle object in the same-degree part
`H_n(T₁) -> H_n(T₂) -> H_n(T₃)` of the derived-category homology sequence.
-/
theorem derived_triangle_exact_at_middle_object :
    (ShortComplex.mk ((DerivedCategory.homologyFunctor C n₀).map T.mor₁)
      ((DerivedCategory.homologyFunctor C n₀).map T.mor₂)
      (by
        simp only [← Functor.map_comp, comp_distTriang_mor_zero₁₂ _ hT,
          Functor.map_zero])).Exact := by
  exact DerivedCategory.HomologySequence.exact₂ T hT n₀

/--
Exactness at `H_n(T₃)` in
`H_n(T₂) -> H_n(T₃) -> H_{n+1}(T₁)`.
-/
theorem derived_triangle_exact_at_connecting_source :
    (ShortComplex.mk ((DerivedCategory.homologyFunctor C n₀).map T.mor₂)
      (derivedTriangleConnectingHomomorphism T n₀ n₁ hn)
      (derived_triangle_second_homology_map_comp_connecting T hT n₀ n₁ hn)).Exact := by
  exact DerivedCategory.HomologySequence.exact₃ T hT n₀ n₁ hn

/--
Exactness at `H_{n+1}(T₁)` in
`H_n(T₃) -> H_{n+1}(T₁) -> H_{n+1}(T₂)`.
-/
theorem derived_triangle_exact_at_connecting_target :
    (ShortComplex.mk (derivedTriangleConnectingHomomorphism T n₀ n₁ hn)
      ((DerivedCategory.homologyFunctor C n₁).map T.mor₁)
      (derived_triangle_connecting_comp_first_homology_map T hT n₀ n₁ hn)).Exact := by
  exact DerivedCategory.HomologySequence.exact₁ T hT n₀ n₁ hn

end DerivedCategoryTriangleFollowUp

/-- Machine-readable child status for the derived-category triangle follow-up. -/
def derivedTriangleFollowUpStatus : String :=
  "checked-local-wrapper-upstream-mathlib-public-backfill-pending"

/-- Checked marker that the derived-category triangle child has repo-local wrappers. -/
theorem derivedTriangleFollowUpStatus_eq_checked :
    derivedTriangleFollowUpStatus =
      "checked-local-wrapper-upstream-mathlib-public-backfill-pending" := rfl

/--
M0387 boundary for the derived-category triangle follow-up: the mathlib anchors
are imported and wrapped locally, while public blueprint/todo integration must
still happen in a serialized merge-back pass.
-/
def derivedTrianglePublicBackfillBoundary : String :=
  "local_wrapper_upstream_mathlib; no repo_local_integration_debt; public Stage1/todo backfill pending"

section GroupHomologyCohomologySpecializationFollowUp

variable {k G : Type u} [CommRing k] [Group G]
variable {X : ShortComplex (Rep k G)} (hX : X.ShortExact)

include hX

section GroupHomologySpecialization

variable {i j : ℕ} (hij : j + 1 = i)

/--
The group-homology connecting morphism attached to a short exact sequence of
`k`-linear `G`-representations.

This is the checked Stage1 child wrapper for the group-homology specialization
anchored at
`Mathlib.RepresentationTheory.Homological.GroupHomology.LongExactSequence`.
-/
noncomputable abbrev groupHomologyConnectingHomomorphism :
    groupHomology (k := k) (G := G) X.X₃ i ⟶ groupHomology (k := k) (G := G) X.X₁ j :=
  groupHomology.δ hX i j hij

/-- The local wrapper uses mathlib's canonical group-homology connecting morphism. -/
theorem groupHomologyConnectingHomomorphism_eq_mathlib :
    groupHomologyConnectingHomomorphism hX hij = groupHomology.δ hX i j hij := rfl

/-- Exactness of `H_i(G, X_3) -> H_j(G, X_1) -> H_j(G, X_2)`. -/
theorem groupHomology_exact_at_connecting_target :
    (groupHomology.mapShortComplex₁ hX hij).Exact := by
  exact groupHomology.mapShortComplex₁_exact hX hij

/-- Exactness of `H_i(G, X_2) -> H_i(G, X_3) -> H_j(G, X_1)`. -/
theorem groupHomology_exact_at_connecting_source :
    (groupHomology.mapShortComplex₃ hX hij).Exact := by
  exact groupHomology.mapShortComplex₃_exact hX hij

/-- Exactness of `H_i(G, X_1) -> H_i(G, X_2) -> H_i(G, X_3)`. -/
theorem groupHomology_exact_at_source_degree (i : ℕ) :
    (groupHomology.mapShortComplex₂ X i).Exact := by
  exact groupHomology.mapShortComplex₂_exact hX i

/-- The group-homology connecting morphism is epi when the middle target degree vanishes. -/
theorem groupHomology_connecting_epi_of_middle_homology_target_zero
    (n : ℕ) (h : IsZero (groupHomology (k := k) (G := G) X.X₂ n)) :
    Epi (groupHomology.δ hX (n + 1) n rfl) := by
  exact groupHomology.epi_δ_of_isZero hX n h

/-- The group-homology connecting morphism is mono when the middle source degree vanishes. -/
theorem groupHomology_connecting_mono_of_middle_homology_source_zero
    (n : ℕ) (h : IsZero (groupHomology (k := k) (G := G) X.X₂ (n + 1))) :
    Mono (groupHomology.δ hX (n + 1) n rfl) := by
  exact groupHomology.mono_δ_of_isZero hX n h

/-- The group-homology connecting morphism is an isomorphism when both adjacent middle terms vanish. -/
theorem groupHomology_connecting_isIso_of_middle_homology_zero
    (n : ℕ) (hs : IsZero (groupHomology (k := k) (G := G) X.X₂ (n + 1)))
    (h : IsZero (groupHomology (k := k) (G := G) X.X₂ n)) :
    IsIso (groupHomology.δ hX (n + 1) n rfl) := by
  exact groupHomology.isIso_δ_of_isZero hX n hs h

end GroupHomologySpecialization

section GroupCohomologySpecialization

variable {i j : ℕ} (hij : i + 1 = j)

/--
The group-cohomology connecting morphism attached to a short exact sequence of
`k`-linear `G`-representations.

This is the checked Stage1 child wrapper for the group-cohomology specialization
anchored at
`Mathlib.RepresentationTheory.Homological.GroupCohomology.LongExactSequence`.
-/
noncomputable abbrev groupCohomologyConnectingHomomorphism :
    groupCohomology (k := k) (G := G) X.X₃ i ⟶
      groupCohomology (k := k) (G := G) X.X₁ j :=
  groupCohomology.δ hX i j hij

/-- The local wrapper uses mathlib's canonical group-cohomology connecting morphism. -/
theorem groupCohomologyConnectingHomomorphism_eq_mathlib :
    groupCohomologyConnectingHomomorphism hX hij = groupCohomology.δ hX i j hij := rfl

/-- Exactness of `H^i(G, X_3) -> H^j(G, X_1) -> H^j(G, X_2)`. -/
theorem groupCohomology_exact_at_connecting_target :
    (groupCohomology.mapShortComplex₁ hX hij).Exact := by
  exact groupCohomology.mapShortComplex₁_exact hX hij

/-- Exactness of `H^i(G, X_2) -> H^i(G, X_3) -> H^j(G, X_1)`. -/
theorem groupCohomology_exact_at_connecting_source :
    (groupCohomology.mapShortComplex₃ hX hij).Exact := by
  exact groupCohomology.mapShortComplex₃_exact hX hij

/-- Exactness of `H^i(G, X_1) -> H^i(G, X_2) -> H^i(G, X_3)`. -/
theorem groupCohomology_exact_at_source_degree (i : ℕ) :
    (groupCohomology.mapShortComplex₂ X i).Exact := by
  exact groupCohomology.mapShortComplex₂_exact hX i

/-- The group-cohomology connecting morphism is epi when the middle target degree vanishes. -/
theorem groupCohomology_connecting_epi_of_middle_cohomology_target_zero
    (n : ℕ) (h : IsZero (groupCohomology (k := k) (G := G) X.X₂ (n + 1))) :
    Epi (groupCohomology.δ hX n (n + 1) rfl) := by
  exact groupCohomology.epi_δ_of_isZero hX n h

/-- The group-cohomology connecting morphism is mono when the middle source degree vanishes. -/
theorem groupCohomology_connecting_mono_of_middle_cohomology_source_zero
    (n : ℕ) (h : IsZero (groupCohomology (k := k) (G := G) X.X₂ n)) :
    Mono (groupCohomology.δ hX n (n + 1) rfl) := by
  exact groupCohomology.mono_δ_of_isZero hX n h

/-- The group-cohomology connecting morphism is an isomorphism when both adjacent middle terms vanish. -/
theorem groupCohomology_connecting_isIso_of_middle_cohomology_zero
    (n : ℕ) (h : IsZero (groupCohomology (k := k) (G := G) X.X₂ n))
    (hs : IsZero (groupCohomology (k := k) (G := G) X.X₂ (n + 1))) :
    IsIso (groupCohomology.δ hX n (n + 1) rfl) := by
  exact groupCohomology.isIso_δ_of_isZero hX n h hs

end GroupCohomologySpecialization

end GroupHomologyCohomologySpecializationFollowUp

/-- Machine-readable child status for the group homology/cohomology specialization follow-up. -/
def groupHomologyCohomologyFollowUpStatus : String :=
  "checked-local-wrapper-upstream-mathlib-public-backfill-pending"

/-- Checked marker that the group homology/cohomology specialization child has repo-local wrappers. -/
theorem groupHomologyCohomologyFollowUpStatus_eq_checked :
    groupHomologyCohomologyFollowUpStatus =
      "checked-local-wrapper-upstream-mathlib-public-backfill-pending" := rfl

/--
M0387 boundary for the group homology/cohomology specialization follow-up: the
mathlib anchors are imported and wrapped locally, while public blueprint/todo
integration must still happen in a serialized merge-back pass.
-/
def groupHomologyCohomologyPublicBackfillBoundary : String :=
  "local_wrapper_upstream_mathlib; no repo_local_integration_debt; public Stage1/todo backfill pending"

section ExtLongExactSequenceFollowUp

variable [HasExt.{w} C]
variable {E : ShortComplex C} (hE : E.ShortExact)
variable (X Y : C) (n₀ n₁ : ℕ)

/--
The covariant long exact sequence of Ext groups attached to a short exact
sequence `E`:

`Ext X E.X₁ n₀ -> Ext X E.X₂ n₀ -> Ext X E.X₃ n₀ ->
 Ext X E.X₁ n₁ -> Ext X E.X₂ n₁ -> Ext X E.X₃ n₁`.

This is the checked Stage1 child wrapper for the follow-up anchored at
`Mathlib.Algebra.Homology.DerivedCategory.Ext.ExactSequences`.
-/
noncomputable abbrev extCovariantLongExactSequence (hn : n₀ + 1 = n₁) :
    ComposableArrows AddCommGrpCat.{w} 5 :=
  Abelian.Ext.covariantSequence X hE n₀ n₁ hn

/-- Exactness of the covariant Ext long exact sequence supplied by mathlib. -/
theorem ext_covariant_long_exact_sequence (hn : n₀ + 1 = n₁) :
    (extCovariantLongExactSequence hE X n₀ n₁ hn).Exact := by
  exact Abelian.Ext.covariantSequence_exact X hE n₀ n₁ hn

/--
The contravariant long exact sequence of Ext groups attached to a short exact
sequence `E`:

`Ext E.X₃ Y n₀ -> Ext E.X₂ Y n₀ -> Ext E.X₁ Y n₀ ->
 Ext E.X₃ Y n₁ -> Ext E.X₂ Y n₁ -> Ext E.X₁ Y n₁`.
-/
noncomputable abbrev extContravariantLongExactSequence (hn : 1 + n₀ = n₁) :
    ComposableArrows AddCommGrpCat.{w} 5 :=
  Abelian.Ext.contravariantSequence hE Y n₀ n₁ hn

/-- Exactness of the contravariant Ext long exact sequence supplied by mathlib. -/
theorem ext_contravariant_long_exact_sequence (hn : 1 + n₀ = n₁) :
    (extContravariantLongExactSequence hE Y n₀ n₁ hn).Exact := by
  exact Abelian.Ext.contravariantSequence_exact hE Y n₀ n₁ hn

variable {X Y}

/-- Pointwise exactness at `Ext X E.X₁ n₁` in the covariant Ext sequence. -/
theorem ext_covariant_exact_at_target {n₁ : ℕ} (x₁ : Abelian.Ext X E.X₁ n₁)
    (hx₁ : x₁.comp (Abelian.Ext.mk₀ E.f) (add_zero n₁) = 0) {n₀ : ℕ}
    (hn₀ : n₀ + 1 = n₁) :
    ∃ (x₃ : Abelian.Ext X E.X₃ n₀), x₃.comp hE.extClass hn₀ = x₁ := by
  exact Abelian.Ext.covariant_sequence_exact₁ X hE x₁ hx₁ hn₀

/-- Pointwise exactness at `Ext X E.X₂ n` in the covariant Ext sequence. -/
theorem ext_covariant_exact_at_middle (hE : E.ShortExact) {n : ℕ}
    (x₂ : Abelian.Ext X E.X₂ n)
    (hx₂ : x₂.comp (Abelian.Ext.mk₀ E.g) (add_zero n) = 0) :
    ∃ (x₁ : Abelian.Ext X E.X₁ n),
      x₁.comp (Abelian.Ext.mk₀ E.f) (add_zero n) = x₂ := by
  exact Abelian.Ext.covariant_sequence_exact₂ X hE x₂ hx₂

/-- Pointwise exactness at `Ext X E.X₃ n₀` in the covariant Ext sequence. -/
theorem ext_covariant_exact_at_source {n₀ : ℕ} (x₃ : Abelian.Ext X E.X₃ n₀)
    {n₁ : ℕ} (hn₁ : n₀ + 1 = n₁) (hx₃ : x₃.comp hE.extClass hn₁ = 0) :
    ∃ (x₂ : Abelian.Ext X E.X₂ n₀),
      x₂.comp (Abelian.Ext.mk₀ E.g) (add_zero n₀) = x₃ := by
  exact Abelian.Ext.covariant_sequence_exact₃ X hE x₃ hn₁ hx₃

/-- Pointwise exactness at `Ext E.X₁ Y n₀` in the contravariant Ext sequence. -/
theorem ext_contravariant_exact_at_source {n₀ : ℕ} (x₁ : Abelian.Ext E.X₁ Y n₀)
    {n₁ : ℕ} (hn₁ : 1 + n₀ = n₁) (hx₁ : hE.extClass.comp x₁ hn₁ = 0) :
    ∃ (x₂ : Abelian.Ext E.X₂ Y n₀),
      (Abelian.Ext.mk₀ E.f).comp x₂ (zero_add n₀) = x₁ := by
  exact Abelian.Ext.contravariant_sequence_exact₁ hE Y x₁ hn₁ hx₁

/-- Pointwise exactness at `Ext E.X₂ Y n` in the contravariant Ext sequence. -/
theorem ext_contravariant_exact_at_middle (hE : E.ShortExact) {n : ℕ}
    (x₂ : Abelian.Ext E.X₂ Y n)
    (hx₂ : (Abelian.Ext.mk₀ E.f).comp x₂ (zero_add n) = 0) :
    ∃ (x₁ : Abelian.Ext E.X₃ Y n),
      (Abelian.Ext.mk₀ E.g).comp x₁ (zero_add n) = x₂ := by
  exact Abelian.Ext.contravariant_sequence_exact₂ hE Y x₂ hx₂

/-- Pointwise exactness at `Ext E.X₃ Y n₁` in the contravariant Ext sequence. -/
theorem ext_contravariant_exact_at_target {n₁ : ℕ} (x₃ : Abelian.Ext E.X₃ Y n₁)
    (hx₃ : (Abelian.Ext.mk₀ E.g).comp x₃ (zero_add n₁) = 0) {n₀ : ℕ}
    (hn₀ : 1 + n₀ = n₁) :
    ∃ (x₁ : Abelian.Ext E.X₁ Y n₀), hE.extClass.comp x₁ hn₀ = x₃ := by
  exact Abelian.Ext.contravariant_sequence_exact₃ hE Y x₃ hx₃ hn₀

end ExtLongExactSequenceFollowUp

/-- Machine-readable child status for the Ext long exact sequence follow-up. -/
def extLongExactSequenceFollowUpStatus : String :=
  "checked-local-wrapper-upstream-mathlib-public-backfill-pending"

/-- Checked marker that the Ext long exact sequence child has repo-local wrappers. -/
theorem extLongExactSequenceFollowUpStatus_eq_checked :
    extLongExactSequenceFollowUpStatus =
      "checked-local-wrapper-upstream-mathlib-public-backfill-pending" := rfl

/--
M0387 boundary for the Ext long exact sequence follow-up: the mathlib anchor is
imported and wrapped locally, while public blueprint/todo integration must still
happen in a serialized merge-back pass.
-/
def extLongExactSequencePublicBackfillBoundary : String :=
  "local_wrapper_upstream_mathlib; no repo_local_integration_debt; public Stage1/todo backfill pending"

/--
M0387 audit metadata for upstream proof segments feeding
`HomologicalComplex.HomologySequence.snakeInput`.

These rows are deliberately not completion evidence.  They make the current
repo-local boundary checkable in Lean: every proof-internal upstream segment is
named and remains `unchecked` until a later audit decomposes it into independent
sub-100-step leaves.
-/
structure UpstreamSnakeInputProofSegment where
  segmentId : String
  upstreamModule : String
  upstreamDeclaration : String
  status : String
  m0387BudgetBoundary : String
deriving Repr

/-- Upstream `snakeInput` proof path segments that still need sub-100-step audit. -/
def snakeInputProofPathSegments : List UpstreamSnakeInputProofSegment := [
  {
    segmentId := "SNAKE-L01",
    upstreamModule := "Mathlib.Algebra.Homology.HomologySequence",
    upstreamDeclaration := "HomologicalComplex.HomologySequence.snakeInput.h₀",
    status := "unchecked",
    m0387BudgetBoundary :=
      "Kernel witness for the homology/opcycles/cycles/homology four-term diagram; depends on composableArrows₃_exact and has not been locally split into sub-100-step leaves."
  },
  {
    segmentId := "SNAKE-L02",
    upstreamModule := "Mathlib.Algebra.Homology.HomologySequence",
    upstreamDeclaration := "HomologicalComplex.HomologySequence.snakeInput.h₃",
    status := "unchecked",
    m0387BudgetBoundary :=
      "Cokernel witness for the same four-term diagram; depends on composableArrows₃_exact and has not been locally split into sub-100-step leaves."
  },
  {
    segmentId := "SNAKE-L03",
    upstreamModule := "Mathlib.Algebra.Homology.HomologySequence",
    upstreamDeclaration := "HomologicalComplex.HomologySequence.opcycles_right_exact",
    status := "unchecked",
    m0387BudgetBoundary :=
      "Exactness of opcycles under the right-exact half of a short exact complex sequence; proof body has not been audited into sub-100-step local leaves."
  },
  {
    segmentId := "SNAKE-L04",
    upstreamModule := "Mathlib.Algebra.Homology.HomologySequence",
    upstreamDeclaration := "HomologicalComplex.HomologySequence.cycles_left_exact",
    status := "unchecked",
    m0387BudgetBoundary :=
      "Exactness of cycles under the left-exact half of a short exact complex sequence; proof body has not been audited into sub-100-step local leaves."
  },
  {
    segmentId := "SNAKE-L05",
    upstreamModule := "Mathlib.Algebra.Homology.ShortComplex.SnakeLemma",
    upstreamDeclaration := "ShortComplex.SnakeInput.L₁'_exact",
    status := "unchecked",
    m0387BudgetBoundary :=
      "First auxiliary exactness segment used by the snake lemma; upstream proof internals remain outside the local leaf-budget ledger."
  },
  {
    segmentId := "SNAKE-L06",
    upstreamModule := "Mathlib.Algebra.Homology.ShortComplex.SnakeLemma",
    upstreamDeclaration := "ShortComplex.SnakeInput.L₂'_exact",
    status := "unchecked",
    m0387BudgetBoundary :=
      "Dual auxiliary exactness segment used by the snake lemma; upstream proof internals remain outside the local leaf-budget ledger."
  },
  {
    segmentId := "SNAKE-L07",
    upstreamModule := "Mathlib.Algebra.Homology.ShortComplex.SnakeLemma",
    upstreamDeclaration := "ShortComplex.SnakeInput.snake_lemma",
    status := "unchecked",
    m0387BudgetBoundary :=
      "Assembly of the six-term exact composable-arrows sequence; not yet decomposed into independent local proof leaves."
  },
  {
    segmentId := "SNAKE-L08",
    upstreamModule := "Mathlib.Algebra.Homology.ShortComplex.SnakeLemma",
    upstreamDeclaration := "ShortComplex.SnakeInput.δ_eq",
    status := "unchecked",
    m0387BudgetBoundary :=
      "Boundary-value computation for the connecting morphism; proof internals have not been audited into sub-100-step leaves."
  },
  {
    segmentId := "SNAKE-L09",
    upstreamModule := "Mathlib.Algebra.Homology.ShortComplex.SnakeLemma",
    upstreamDeclaration := "ShortComplex.SnakeInput.mono_δ / epi_δ / isIso_δ / δIso",
    status := "unchecked",
    m0387BudgetBoundary :=
      "Isomorphism consequences for the connecting morphism; grouped here as consequences to audit after the exactness segments."
  }
]

/-- Child `S1-M-096-C004` keeps the upstream `snakeInput` proof-path budget open. -/
def snakeInputProofPathAuditStatus : String :=
  "unchecked"

/-- Checked marker that this file does not claim `snakeInput` proof-path completion. -/
theorem snakeInputProofPathAuditStatus_eq_unchecked :
    snakeInputProofPathAuditStatus = "unchecked" := rfl

end S1_M_096
end Stage1
end AwesomeTheorems
