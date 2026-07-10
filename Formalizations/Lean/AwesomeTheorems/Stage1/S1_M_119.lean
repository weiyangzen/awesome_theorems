import Mathlib.Algebra.Homology.HomologySequenceLemmas
import Mathlib.AlgebraicTopology.SimplicialSet.RelativeMorphism
import Mathlib.AlgebraicTopology.SingularHomology.HomotopyInvarianceTopCat
import Mathlib.CategoryTheory.Sites.SheafCohomology.Basic
import Mathlib.Geometry.Manifold.IsManifold.InteriorBoundary
import Mathlib.LinearAlgebra.Orientation
import Mathlib.Topology.ContinuousMap.CompactlySupported

/-!
# S1-M-119 / THM-M-0547: Lefschetz duality

Repo-local Stage1 artifact: `AwesomeTheorems/Stage1/S1_M_119.lean`.

This Stage1 file records a conservative Lean 4 boundary for Lefschetz duality
for manifolds with boundary.  The pinned mathlib snapshot
`8a178386ffc0f5fef0b77738bb5449d50efeea95` has useful manifold-with-corners,
absolute singular homology, homotopy invariance, simplicial-set relative
morphism, and generic long exact homology sequence APIs, but this audit did not
find a merged concrete relative singular homology functor for a topological pair
compatible with `AlgebraicTopology.singularChainComplexFunctor`.

Upstream audit note, checked on 2026-05-01: mathlib PR
<https://github.com/leanprover-community/mathlib4/pull/37659> is titled
`feat(AlgebraicTopology): relative singular homology` and was still open with
the `awaiting-author` label in the GitHub API search result.  Until that API is
merged, pinned, and imported here, `LefschetzDualityPackage.relativeHomology`
remains an abstract field.

The declarations below therefore provide checked low-risk wrappers around the
available algebraic-topology API and a precise `StatementShape` package for the
missing duality theorem.  The checked content is limited to `StatementShape`
plus adjacent singular-homology wrappers; it does not claim the terminal
duality theorem and introduces no proof placeholders or new axioms.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits
open AlgebraicTopology
open scoped ContDiff Manifold

universe w v u

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_119

variable (C : Type u) [Category.{v} C] [HasCoproducts.{w} C]
  [Preadditive C] [CategoryWithHomology C]

/-- Local alias for mathlib's singular homology object of a topological space. -/
abbrev SingularHomology (n : ℕ) (R : C) (X : TopCat.{w}) : C :=
  (((singularHomologyFunctor C n).obj R).obj X)

/-- Local alias for mathlib's singular chain complex functor. -/
abbrev SingularChainComplexFunctor : C ⥤ TopCat.{w} ⥤ ChainComplex C ℕ :=
  singularChainComplexFunctor C

/--
Topological input data for a future Lefschetz duality statement, after the
`S1-M-119-C004` manifold-boundary API audit.

The old abstract `isManifoldWithBoundary : Prop` field has been replaced by
concrete mathlib hypotheses in the surrounding parameters:
`ModelWithCorners`, `ChartedSpace`, and `IsManifold I ∞ M`.  This is the
strongest safe local replacement found at the pinned mathlib snapshot.  The
separate `boundaryIdentifiesTopologicalBoundary` and `oriented` fields remain
propositions because this file still has no concrete API for a pair inclusion
`∂M ⟶ M`, fundamental classes, or cap products.
-/
structure LefschetzPair
    (E H M : Type w) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    (I : ModelWithCorners ℝ E H) [ChartedSpace H M] [IsManifold I ∞ M] :
    Type (w + 1) where
  boundary : TopCat.{w}
  boundaryInclusion : boundary ⟶ TopCat.of M
  dimension : ℕ
  compactOrFiniteType : Prop
  oriented : Prop
  boundaryIdentifiesTopologicalBoundary : Prop

/--
Terminal package expected from a full formalization of Lefschetz duality.

The `absoluteHomologyIso` field is tied to mathlib's current singular homology
functor.  Relative homology, compactly supported cohomology, cap products, and
fundamental classes are kept abstract here because the audited mathlib snapshot
does not expose the complete classical API needed to state them concretely.
-/
structure LefschetzDualityPackage (R : C)
    {E H M : Type w} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    {I : ModelWithCorners ℝ E H} [ChartedSpace H M] [IsManifold I ∞ M]
    (D : LefschetzPair E H M I) :
    Type (max (u + 1) (v + 1) (w + 1)) where
  compactSupportCohomology : ℕ → C
  relativeHomology : ℕ → C
  absoluteHomology : ℕ → C
  absoluteHomologyIso : ∀ n : ℕ, absoluteHomology n ≅ SingularHomology C n R (TopCat.of M)
  dualityIso : ∀ k : ℕ, compactSupportCohomology k ≅ relativeHomology (D.dimension - k)
  capProductWithFundamentalClass : Prop
  boundaryLongExactSequenceCompatibility : Prop
  naturalityForBoundaryMaps : Prop
  capProductWithFundamentalClass_holds : capProductWithFundamentalClass
  boundaryLongExactSequenceCompatibility_holds : boundaryLongExactSequenceCompatibility
  naturalityForBoundaryMaps_holds : naturalityForBoundaryMaps

/--
Stage1 normalized statement shape for THM-M-0547.

For every oriented compact or finite-type manifold-with-boundary input, there
should be a duality package identifying compactly supported cohomology with the
degree-complementary relative homology group of the pair.
-/
def StatementShape (R : C) : Prop :=
  ∀ (E H M : Type w) [NormedAddCommGroup E] [NormedSpace ℝ E]
      [TopologicalSpace H] [TopologicalSpace M]
      (I : ModelWithCorners ℝ E H) [ChartedSpace H M] [IsManifold I ∞ M],
    ∀ D : LefschetzPair E H M I,
      D.boundaryIdentifiesTopologicalBoundary →
        D.oriented →
          D.compactOrFiniteType →
            Nonempty (LefschetzDualityPackage C R D)

/-- The statement-shape definition unfolds to nonemptiness of the terminal package. -/
theorem statementShape_iff (R : C) :
    StatementShape C R ↔
      ∀ (E H M : Type w) [NormedAddCommGroup E] [NormedSpace ℝ E]
          [TopologicalSpace H] [TopologicalSpace M]
          (I : ModelWithCorners ℝ E H) [ChartedSpace H M] [IsManifold I ∞ M],
        ∀ D : LefschetzPair E H M I,
          D.boundaryIdentifiesTopologicalBoundary →
            D.oriented →
              D.compactOrFiniteType →
                Nonempty (LefschetzDualityPackage C R D) :=
  Iff.rfl

/-- Checked wrapper: the local singular homology alias is mathlib's functor value. -/
theorem singularHomology_eq_mathlib (n : ℕ) (R : C) (X : TopCat.{w}) :
    SingularHomology C n R X = (((singularHomologyFunctor C n).obj R).obj X) :=
  rfl

/-- Checked functoriality smoke test: the identity map induces the identity on singular homology. -/
theorem singularHomology_map_id (n : ℕ) (R : C) (X : TopCat.{w}) :
    (((singularHomologyFunctor C n).obj R).map (𝟙 X)) =
      𝟙 (SingularHomology C n R X) := by
  simp [SingularHomology]

/--
Checked mathlib wrapper: positive-degree singular homology of a totally
disconnected space vanishes.

This is only an adjacent simple-space anchor.  It is not Lefschetz duality.
-/
theorem isZero_singularHomology_of_totallyDisconnectedSpace
    (n : ℕ) (hn : n ≠ 0) (R : C) (X : TopCat.{w}) [TotallyDisconnectedSpace X] :
    IsZero (SingularHomology C n R X) := by
  exact isZero_singularHomologyFunctor_of_totallyDisconnectedSpace C n R X hn

/--
Checked mathlib wrapper: homotopic maps induce equal maps on singular homology.

This supplies a functoriality/naturality anchor needed by any later duality
formalization, but it does not construct cap products or fundamental classes.
-/
theorem homotopic_maps_induce_equal_singularHomology_maps
    (n : ℕ) (R : C) {X Y : TopCat.{w}} {f g : X ⟶ Y} (H : TopCat.Homotopy f g) :
    HomologicalComplex.homologyMap (((singularChainComplexFunctor C).obj R).map f) n =
      HomologicalComplex.homologyMap (((singularChainComplexFunctor C).obj R).map g) n := by
  exact TopCat.Homotopy.congr_homologyMap_singularChainComplexFunctor H R n

/-! ## Relative singular homology audit boundary -/

/--
Local alias for the relative-morphism API currently available for simplicial
sets.  This is an adjacent homotopy-theoretic API, not a relative singular
homology object for a topological pair.
-/
abbrev RelativeSimplicialMorphism {X Y : SSet.{w}} (A : X.Subcomplex) (B : Y.Subcomplex)
    (φ : (A : SSet.{w}) ⟶ (B : SSet.{w})) : Type w :=
  SSet.RelativeMorphism A B φ

/--
Checked wrapper for the generic long exact homology-sequence substrate.

This is the algebraic ingredient needed after a relative singular chain complex
has been constructed, but it does not by itself provide the relative singular
homology of a topological pair.
-/
theorem shortExact_chainComplex_homology_exact₂
    {A : Type u} [Category.{v} A] [Abelian A]
    {S : ShortComplex (ChainComplex A ℕ)} (hS : S.ShortExact) (i : ℕ) :
    (ShortComplex.mk (HomologicalComplex.homologyMap S.f i)
      (HomologicalComplex.homologyMap S.g i) (by
        rw [← HomologicalComplex.homologyMap_comp, S.zero,
          HomologicalComplex.homologyMap_zero])).Exact := by
  simpa using (CategoryTheory.ShortComplex.ShortExact.homology_exact₂ (S := S) hS i)

/-- Checked wrapper: exactness at the first post-boundary term of the long exact sequence. -/
theorem shortExact_chainComplex_homology_exact₁
    {A : Type u} [Category.{v} A] [Abelian A]
    {S : ShortComplex (ChainComplex A ℕ)} (hS : S.ShortExact)
    {i j : ℕ} (hij : (ComplexShape.down ℕ).Rel i j) :
    (ShortComplex.mk (hS.δ i j hij) (HomologicalComplex.homologyMap S.f j) (by
      exact CategoryTheory.ShortComplex.ShortExact.δ_comp (S := S) hS i j hij)).Exact := by
  simpa using (CategoryTheory.ShortComplex.ShortExact.homology_exact₁ (S := S) hS i j hij)

/-- Checked wrapper: exactness immediately before the connecting morphism. -/
theorem shortExact_chainComplex_homology_exact₃
    {A : Type u} [Category.{v} A] [Abelian A]
    {S : ShortComplex (ChainComplex A ℕ)} (hS : S.ShortExact)
    {i j : ℕ} (hij : (ComplexShape.down ℕ).Rel i j) :
    (ShortComplex.mk (HomologicalComplex.homologyMap S.g i) (hS.δ i j hij) (by
      exact CategoryTheory.ShortComplex.ShortExact.comp_δ (S := S) hS i j hij)).Exact := by
  simpa using (CategoryTheory.ShortComplex.ShortExact.homology_exact₃ (S := S) hS i j hij)

/-- Checked wrapper: five-term exactness for the homology sequence of a short exact complex. -/
theorem shortExact_chainComplex_homology_fiveTerm_exact
    {A : Type u} [Category.{v} A] [Abelian A]
    {S : ShortComplex (ChainComplex A ℕ)} (hS : S.ShortExact)
    {i j : ℕ} (hij : (ComplexShape.down ℕ).Rel i j) :
    (HomologicalComplex.HomologySequence.composableArrows₅ hS i j hij).Exact := by
  exact HomologicalComplex.HomologySequence.composableArrows₅_exact hS i j hij

/-- Checked wrapper: naturality of connecting morphisms in the long exact homology sequence. -/
theorem shortExact_chainComplex_connecting_naturality
    {A : Type u} [Category.{v} A] [Abelian A]
    {S₁ S₂ : ShortComplex (ChainComplex A ℕ)}
    (φ : S₁ ⟶ S₂) (hS₁ : S₁.ShortExact) (hS₂ : S₂.ShortExact)
    {i j : ℕ} (hij : (ComplexShape.down ℕ).Rel i j) :
    hS₁.δ i j hij ≫ HomologicalComplex.homologyMap φ.τ₁ _ =
      HomologicalComplex.homologyMap φ.τ₃ _ ≫ hS₂.δ i j hij :=
  HomologicalComplex.HomologySequence.δ_naturality φ hS₁ hS₂ i j hij

/-! ## Singular cohomology and compact-support cohomology audit boundary -/

/-- Classification of the audited cohomology API surfaces for this Stage1 slot. -/
inductive CohomologyAPIAuditKind where
  | singularCohomology
  | compactSupportCohomology
  | sheafCohomologyNearMiss
  | compactSupportFunctionNearMiss
  | genericCochainSubstrate
  deriving DecidableEq, Repr

/-- One checked local record for an audited cohomology-adjacent API surface. -/
structure CohomologyAPIAuditRecord where
  kind : CohomologyAPIAuditKind
  moduleName : String
  declarationName : String
  suitabilityForPoincareLefschetz : String
  repoLocalConsequence : String

/--
Audit result for the child task `S1-M-119-C003`.

At the pinned mathlib revision, the local source search found generic cochain
complex infrastructure, sheaf cohomology, and compactly supported functions,
but did not find a topological singular cohomology functor or a compactly
supported cohomology theory suitable for the cap-product statement of
Poincare-Lefschetz duality.
-/
def cohomologyAPIAuditRecords : List CohomologyAPIAuditRecord := [
  { kind := .singularCohomology,
    moduleName := "Mathlib.AlgebraicTopology",
    declarationName := "no searched singular cohomology functor",
    suitabilityForPoincareLefschetz :=
      "missing: no local declaration matching singularCohomologyFunctor/SingularCohomology was found",
    repoLocalConsequence :=
      "LefschetzDualityPackage.compactSupportCohomology must remain abstract" },
  { kind := .compactSupportCohomology,
    moduleName := "Mathlib.AlgebraicTopology; Mathlib.Topology",
    declarationName := "no searched compact-support cohomology theory",
    suitabilityForPoincareLefschetz :=
      "missing: compact-support function APIs do not provide cohomology groups or cap products",
    repoLocalConsequence :=
      "the Poincare-Lefschetz duality isomorphism cannot be stated concretely in this file" },
  { kind := .sheafCohomologyNearMiss,
    moduleName := "Mathlib.CategoryTheory.Sites.SheafCohomology.Basic",
    declarationName := "CategoryTheory.Sheaf.cohomologyFunctor",
    suitabilityForPoincareLefschetz :=
      "near miss: sheaf cohomology for a Grothendieck topology, not topological singular or compactly supported cohomology of manifolds",
    repoLocalConsequence :=
      "usable only as evidence of general cohomology infrastructure, not as the terminal Lefschetz-duality coefficient theory" },
  { kind := .compactSupportFunctionNearMiss,
    moduleName := "Mathlib.Topology.ContinuousMap.CompactlySupported",
    declarationName := "CompactlySupportedContinuousMap; HasCompactSupport",
    suitabilityForPoincareLefschetz :=
      "near miss: compact support for functions/maps, not a cohomology functor or long exact compact-support theory",
    repoLocalConsequence :=
      "does not discharge compactSupportCohomology or capProductWithFundamentalClass" },
  { kind := .genericCochainSubstrate,
    moduleName := "Mathlib.Algebra.Homology",
    declarationName := "CochainComplex",
    suitabilityForPoincareLefschetz :=
      "substrate only: generic cochain complexes exist but are not specialized to singular cochains on TopCat",
    repoLocalConsequence :=
      "a future formalization still has to define/import singular cochains, cohomology, cup product, and cap product" }
]

/-- Machine-readable gate for the cohomology child audit: open, not completed. -/
def cohomologyAPIAuditCompletionGate : String :=
  "open_not_completed: no repo-local singular cohomology or compact-support cohomology API suitable for Poincare-Lefschetz duality was found at the pinned mathlib revision"

/-- M0387-level child leaves remaining after the cohomology API audit. -/
def cohomologyAPIAuditRemainingLeaves : List String := [
  "S1-M-119-C003-L001: define or import topological singular cochains and singular cohomology with coefficients compatible with singularHomologyFunctor",
  "S1-M-119-C003-L002: define or import compactly supported cohomology for the selected manifold category",
  "S1-M-119-C003-L003: define or import cup and cap products connecting the selected cohomology theory to singular/relative homology",
  "S1-M-119-C003-L004: prove or import the degree convention and boundary long-exact-sequence compatibility needed by Poincare-Lefschetz duality"
]

/-! ## Manifold boundary API audit boundary -/

structure ManifoldBoundaryAPIAuditRecord where
  moduleName : String
  declarationName : String
  repoLocalStatus : String
  lefschetzDualityRole : String
  blocker : String

/--
Integration-ready audit rows for the child task `S1-M-119-C004`.

The positive result is that the abstract `LefschetzPair.isManifoldWithBoundary`
field can be replaced by concrete mathlib manifold hypotheses:
`ModelWithCorners ℝ E H`, `ChartedSpace H M`, and `IsManifold I ∞ M`.
The remaining blocker is not the manifold substrate, but the missing concrete
identification of a chosen `boundary : TopCat` with `I.boundary M` as the pair
used by relative singular homology.
-/
def manifoldBoundaryAPIAuditRecords : List ManifoldBoundaryAPIAuditRecord := [
  {
    moduleName := "Mathlib.Geometry.Manifold.IsManifold.Basic",
    declarationName := "ModelWithCorners",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    lefschetzDualityRole :=
      "Provides the model-with-corners parameter `I : ModelWithCorners ℝ E H` for manifolds whose model range may have boundary.",
    blocker :=
      "Does not itself identify a topological pair `(M, boundary M)` or define relative homology."
  },
  {
    moduleName := "Mathlib.Geometry.Manifold.IsManifold.Basic",
    declarationName := "IsManifold",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    lefschetzDualityRole :=
      "Concrete replacement for the old abstract `isManifoldWithBoundary` proposition in `StatementShape`.",
    blocker :=
      "Smooth compatibility of charts is substrate only; orientation, fundamental class, cap product, and relative pair homology remain missing."
  },
  {
    moduleName := "Mathlib.Geometry.Manifold.IsManifold.InteriorBoundary",
    declarationName := "ModelWithCorners.interior; ModelWithCorners.boundary",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    lefschetzDualityRole :=
      "Defines the chart-independent interior and boundary subsets of a charted manifold via `extChartAt`.",
    blocker :=
      "A future pair API must still turn `I.boundary M` into the selected boundary object and inclusion used by relative homology."
  },
  {
    moduleName := "Mathlib.Geometry.Manifold.IsManifold.InteriorBoundary",
    declarationName := "BoundarylessManifold; ModelWithCorners.Boundaryless.boundary_eq_empty; ModelWithCorners.interior_eq_univ",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    lefschetzDualityRole :=
      "Audits the no-boundary specialization and distinguishes boundaryless manifolds from manifolds with boundary.",
    blocker :=
      "Lefschetz duality needs the non-boundaryless pair case, so these anchors are sanity checks rather than theorem closure."
  }
]

/-- Checked wrapper: mathlib decomposes a charted manifold into interior and boundary subsets. -/
theorem manifold_interior_union_boundary_eq_univ
    {𝕜 : Type*} [NontriviallyNormedField 𝕜]
    {E : Type*} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    {H : Type*} [TopologicalSpace H] {I : ModelWithCorners 𝕜 E H}
    {M : Type*} [TopologicalSpace M] [ChartedSpace H M] :
    (I.interior M) ∪ (I.boundary M) = Set.univ := by
  exact ModelWithCorners.interior_union_boundary_eq_univ (I := I) (M := M)

/-- Checked wrapper: the boundary is the complement of the manifold interior. -/
theorem manifold_compl_interior_eq_boundary
    {𝕜 : Type*} [NontriviallyNormedField 𝕜]
    {E : Type*} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    {H : Type*} [TopologicalSpace H] {I : ModelWithCorners 𝕜 E H}
    {M : Type*} [TopologicalSpace M] [ChartedSpace H M] :
    (I.interior M)ᶜ = I.boundary M := by
  exact ModelWithCorners.compl_interior (I := I) (M := M)

/-- Checked wrapper: a boundaryless manifold has empty manifold boundary. -/
theorem boundarylessManifold_boundary_eq_empty
    {𝕜 : Type*} [NontriviallyNormedField 𝕜]
    {E : Type*} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    {H : Type*} [TopologicalSpace H] {I : ModelWithCorners 𝕜 E H}
    {M : Type*} [TopologicalSpace M] [ChartedSpace H M]
    [BoundarylessManifold I M] :
    I.boundary M = ∅ := by
  exact ModelWithCorners.Boundaryless.boundary_eq_empty (I := I) (M := M)

/-- Checked wrapper: a boundaryless manifold has all points in the manifold interior. -/
theorem boundarylessManifold_interior_eq_univ
    {𝕜 : Type*} [NontriviallyNormedField 𝕜]
    {E : Type*} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    {H : Type*} [TopologicalSpace H] {I : ModelWithCorners 𝕜 E H}
    {M : Type*} [TopologicalSpace M] [ChartedSpace H M]
    [BoundarylessManifold I M] :
    I.interior M = Set.univ := by
  exact ModelWithCorners.interior_eq_univ (I := I) (M := M)

/-- Checked wrapper: empty manifold boundary is equivalent to `BoundarylessManifold`. -/
theorem boundarylessManifold_iff_boundary_eq_empty
    {𝕜 : Type*} [NontriviallyNormedField 𝕜]
    {E : Type*} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    {H : Type*} [TopologicalSpace H] {I : ModelWithCorners 𝕜 E H}
    {M : Type*} [TopologicalSpace M] [ChartedSpace H M] :
    I.boundary M = ∅ ↔ BoundarylessManifold I M := by
  exact ModelWithCorners.Boundaryless.iff_boundary_eq_empty (I := I) (M := M)

/-- Machine-readable gate for the manifold-boundary child audit: substrate improved, not closed. -/
def manifoldBoundaryAPIAuditCompletionGate : String :=
  "open_not_completed: LefschetzPair now uses concrete ModelWithCorners/ChartedSpace/IsManifold hypotheses, but the boundary object, relative homology of the pair, orientation fundamental class, and cap product remain abstract"

/-- M0387-level child leaves remaining after the manifold-boundary API audit. -/
def manifoldBoundaryAPIAuditRemainingLeaves : List String := [
  "S1-M-119-C004-L001: define the selected boundary object as the subtype or TopCat object attached to `I.boundary M`",
  "S1-M-119-C004-L002: prove that `boundaryInclusion` is the inclusion of `I.boundary M` into `M`",
  "S1-M-119-C004-L003: connect that boundary inclusion to the future relative singular homology pair API",
  "S1-M-119-C004-L004: add orientation and fundamental-class hypotheses using concrete mathlib APIs once available"
]

/-! ## External Lean 4 duality anchor audit boundary -/

structure ExternalLeanDualityAuditRecord where
  repository : String
  url : String
  commit : String
  sourcePath : String
  theoremNames : List String
  toolchain : String
  license : String
  classification : String
  lakeDependencyViability : String

/--
Integration-ready audit rows for the child task `S1-M-119-C005`.

The search found no completed Lean 4 formalization of classical Lefschetz
duality, Poincare-Lefschetz duality, or manifold Poincare duality that can be
pin/import/checked here as a terminal proof.  The `gift-framework/core` hit is
recorded because it contains theorem names with `poincare_duality`, but those
theorems are finite Betti-number equalities over project constants, not a
cap-product/fundamental-class theorem and not Lefschetz duality.
-/
def externalLeanDualityAuditRecords : List ExternalLeanDualityAuditRecord := [
  {
    repository := "leanprover-community/mathlib4",
    url :=
      "https://github.com/leanprover-community/mathlib4/tree/8a178386ffc0f5fef0b77738bb5449d50efeea95",
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    sourcePath := "Mathlib",
    theoremNames := [],
    toolchain := "leanprover/lean4:v4.29.0",
    license := "Apache-2.0",
    classification :=
      "no completed theorem found under LefschetzDuality, PoincareLefschetz, PoincareDuality, or nearby cap-product/fundamental-class search terms",
    lakeDependencyViability :=
      "already pinned locally, but no terminal theorem exists to import or wrap for this Stage1 target"
  },
  {
    repository := "gift-framework/core",
    url :=
      "https://github.com/gift-framework/core/tree/fc5ed2c2c3a660d73acf7772f7705d216131a969",
    commit := "fc5ed2c2c3a660d73acf7772f7705d216131a969",
    sourcePath := "GIFT/Foundations/PoincareDuality.lean; GIFT/DifferentialForms.lean; GIFT/Relations/V33Additions.lean",
    theoremNames := [
      "GIFT.Foundations.PoincareDuality.total_betti_eq_two_H_star",
      "GIFT.Foundations.PoincareDuality.H_star_structural",
      "GIFT.Foundations.PoincareDuality.betti_pair_eq_two_K7_sq",
      "GIFT.Foundations.PoincareDuality.poincare_duality_certificate",
      "GIFT.DifferentialForms.poincare_duality",
      "GIFT.Relations.V33Additions.poincare_duality_K7"
    ],
    toolchain := "leanprover/lean4:v4.29.0",
    license := "MIT",
    classification :=
      "near_miss_not_terminal: arithmetic Betti-number equalities/certificates over project constants, not classical Poincare duality and not Poincare-Lefschetz/Lefschetz duality",
    lakeDependencyViability :=
      "toolchain and mathlib revision match this repo, but adding the dependency would not close THM-M-0547 because the named theorems do not provide relative homology, compact-support cohomology, cap products, orientation fundamental classes, or boundary long-exact-sequence compatibility"
  }
]

/-- Machine-readable gate for the external Lean duality search: no repo-local closure. -/
def externalLeanDualityAuditCompletionGate : String :=
  "open_not_completed: no completed external Lean 4 LefschetzDuality, PoincareLefschetz, or classical PoincareDuality formalization was found that can be pin/import/checked for THM-M-0547"

/-- M0387-level child leaves remaining after the external Lean 4 duality search. -/
def externalLeanDualityAuditRemainingLeaves : List String := [
  "S1-M-119-C005-L001: if a future external Lean 4 terminal duality proof is found, record repository URL, exact commit, module, theorem names, toolchain, license, placeholder inventory, and dependency graph",
  "S1-M-119-C005-L002: either pin/import/check the future terminal proof locally or record a concrete blocker such as license, Lean version mismatch, dependency conflict, or incompatible statement shape",
  "S1-M-119-C005-L003: reject arithmetic or statement-only near misses unless they expose compact-support cohomology, relative homology of a pair, cap product, orientation fundamental class, and the pair long-exact-sequence compatibility"
]

/-! ## Cap product and orientation fundamental-class API audit boundary -/

/--
Checked orientation anchor: mathlib has linear/module orientations, but this is
not a manifold local-orientation system and does not construct a singular
homology fundamental class for an oriented manifold with boundary.
-/
def modulePositiveOrientationAnchor
    (R : Type u) [CommSemiring R] [PartialOrder R] [IsStrictOrderedRing R]
    (V : Type w) [AddCommMonoid V] [Module R V] (ι : Type v)
    [Module.Oriented R V ι] :
    Orientation R V ι :=
  positiveOrientation

/--
API boundary for the cap product and relative orientation fundamental class
needed to make `LefschetzDualityPackage.dualityIso` concrete.

The fields intentionally separate the future concrete objects from the checked
mathlib substrate currently available here.  In a terminal formalization, the
`capProductWithFundamentalClass` isomorphism should be induced by capping a
compactly supported cohomology class with the relative fundamental class
`[M, ∂M]`.  This structure is only an integration target: it records exactly
what is missing without manufacturing a theorem from abstract placeholders.
-/
structure LefschetzCapFundamentalClassAPIBoundary (R : C)
    {E H M : Type w} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    {I : ModelWithCorners ℝ E H} [ChartedSpace H M] [IsManifold I ∞ M]
    (D : LefschetzPair E H M I)
    (CompactSupportCohomology RelativeHomology AbsoluteHomology : ℕ → C) :
    Type (max (u + 1) (v + 1) (w + 1)) where
  absoluteHomologyIso : ∀ n : ℕ, AbsoluteHomology n ≅ SingularHomology C n R (TopCat.of M)
  cochainComplex : Type (max u v w)
  compactSupportCondition : Type (max u v w)
  pairRelativeChainComplex : Type (max u v w)
  localOrientationSystem : Type (max u v w)
  relativeFundamentalClassCarrier : Type (max u v w)
  relativeFundamentalClass : relativeFundamentalClassCarrier
  capProduct : (p q : ℕ) → CompactSupportCohomology p ⟶ RelativeHomology (p + q)
  capProductWithFundamentalClass : ∀ k : ℕ,
    CompactSupportCohomology k ≅ RelativeHomology (D.dimension - k)
  orientationDeterminesRelativeFundamentalClass : Prop
  relativeFundamentalClassIsCycle : Prop
  capProductDegreeConvention : Prop
  capProductBoundaryCompatibility : Prop
  compatibleWithBoundaryInclusion : Prop
  apiConventionSatisfied :
    orientationDeterminesRelativeFundamentalClass ∧
      relativeFundamentalClassIsCycle ∧
      capProductDegreeConvention ∧
      capProductBoundaryCompatibility ∧
      compatibleWithBoundaryInclusion

/--
Constructor for the future cap-product/fundamental-class API package.

This is useful to downstream integration because it fixes the exact data that a
pinned mathlib import, external dependency, or local proof body must supply
before `LefschetzDualityPackage.dualityIso` can be replaced by capping with
`[M, ∂M]`.
-/
def LefschetzCapFundamentalClassAPIBoundary.fromData (R : C)
    {E H M : Type w} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    {I : ModelWithCorners ℝ E H} [ChartedSpace H M] [IsManifold I ∞ M]
    (D : LefschetzPair E H M I)
    (CompactSupportCohomology RelativeHomology AbsoluteHomology : ℕ → C)
    (absoluteHomologyIso :
      ∀ n : ℕ, AbsoluteHomology n ≅ SingularHomology C n R (TopCat.of M))
    (cochainComplex compactSupportCondition pairRelativeChainComplex
      localOrientationSystem relativeFundamentalClassCarrier : Type (max u v w))
    (relativeFundamentalClass : relativeFundamentalClassCarrier)
    (capProduct : (p q : ℕ) → CompactSupportCohomology p ⟶ RelativeHomology (p + q))
    (capProductWithFundamentalClass : ∀ k : ℕ,
      CompactSupportCohomology k ≅ RelativeHomology (D.dimension - k))
    (orientationDeterminesRelativeFundamentalClass relativeFundamentalClassIsCycle
      capProductDegreeConvention capProductBoundaryCompatibility
      compatibleWithBoundaryInclusion : Prop)
    (apiConventionSatisfied :
      orientationDeterminesRelativeFundamentalClass ∧
        relativeFundamentalClassIsCycle ∧
        capProductDegreeConvention ∧
        capProductBoundaryCompatibility ∧
        compatibleWithBoundaryInclusion) :
    LefschetzCapFundamentalClassAPIBoundary C R D
      CompactSupportCohomology RelativeHomology AbsoluteHomology where
  absoluteHomologyIso := absoluteHomologyIso
  cochainComplex := cochainComplex
  compactSupportCondition := compactSupportCondition
  pairRelativeChainComplex := pairRelativeChainComplex
  localOrientationSystem := localOrientationSystem
  relativeFundamentalClassCarrier := relativeFundamentalClassCarrier
  relativeFundamentalClass := relativeFundamentalClass
  capProduct := capProduct
  capProductWithFundamentalClass := capProductWithFundamentalClass
  orientationDeterminesRelativeFundamentalClass :=
    orientationDeterminesRelativeFundamentalClass
  relativeFundamentalClassIsCycle := relativeFundamentalClassIsCycle
  capProductDegreeConvention := capProductDegreeConvention
  capProductBoundaryCompatibility := capProductBoundaryCompatibility
  compatibleWithBoundaryInclusion := compatibleWithBoundaryInclusion
  apiConventionSatisfied := apiConventionSatisfied

structure CapFundamentalClassAPIAuditRecord where
  moduleName : String
  declarationName : String
  repoLocalStatus : String
  lefschetzDualityRole : String
  blocker : String

/--
Integration-ready audit rows for the child task `S1-M-119-C006`.

At the pinned mathlib revision, the local repository can check linear
orientation anchors and absolute singular homology, but it does not expose the
concrete cap product, compactly supported cohomology, relative singular
homology of `(M, ∂M)`, or relative orientation fundamental class needed for the
terminal Lefschetz-duality isomorphism.
-/
def capFundamentalClassAPIAuditRecords : List CapFundamentalClassAPIAuditRecord := [
  {
    moduleName := "Mathlib.LinearAlgebra.Orientation",
    declarationName := "Orientation; Module.Oriented; positiveOrientation",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    lefschetzDualityRole :=
      "Provides checked linear orientation data for model modules.",
    blocker :=
      "This is not a manifold local-orientation system and does not construct the relative fundamental class `[M, boundary M]`."
  },
  {
    moduleName := "Mathlib.AlgebraicTopology.SingularHomology.Basic",
    declarationName := "singularHomologyFunctor",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    lefschetzDualityRole :=
      "Provides the absolute singular-homology convention used by `LefschetzDualityPackage.absoluteHomologyIso`.",
    blocker :=
      "No concrete relative singular homology of a topological pair is available in the pinned local closure."
  },
  {
    moduleName := "Mathlib.AlgebraicTopology; Mathlib.Algebra.Homology",
    declarationName := "no searched singular cohomology cup/cap-product API",
    repoLocalStatus := "not_repo_local_closed",
    lefschetzDualityRole :=
      "Would define the cap product pairing compactly supported cohomology against relative homology.",
    blocker :=
      "No local declaration matching a topological singular cohomology functor plus cap product was found."
  },
  {
    moduleName := "Mathlib.Geometry.Manifold.IsManifold.InteriorBoundary",
    declarationName := "ModelWithCorners.boundary",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    lefschetzDualityRole :=
      "Provides the manifold-boundary subset that a future pair API must identify with `D.boundary`.",
    blocker :=
      "The subset API alone does not provide a relative fundamental class or compatibility with the pair long exact sequence."
  }
]

/-- Machine-readable gate for C006: open, not completed. -/
def capFundamentalClassAPIAuditCompletionGate : String :=
  "open_not_completed: only linear orientation and absolute singular-homology anchors are repo-local checked; no concrete cap product, compactly supported cohomology, relative pair homology, or relative fundamental class is available to instantiate LefschetzDualityPackage.dualityIso"

/-- M0387-level child leaves remaining after the C006 cap/fundamental-class audit. -/
def capFundamentalClassAPIAuditRemainingLeaves : List String := [
  "S1-M-119-C006-L001: define or import topological singular cochains and compactly supported cohomology for the selected manifold category",
  "S1-M-119-C006-L002: define or import relative singular homology of the pair `(M, boundary M)` compatible with `singularChainComplexFunctor`",
  "S1-M-119-C006-L003: define or import a manifold local-orientation system whose orientation determines the relative fundamental class `[M, boundary M]`",
  "S1-M-119-C006-L004: define or import the cap product pairing compactly supported cohomology with the relative fundamental class",
  "S1-M-119-C006-L005: prove or import the degree convention identifying capping with `[M, boundary M]` as `H_c^k(M; R) ≅ H_{n-k}(M, boundary M; R)`"
]

/-! ## Cap product and pair long-exact-sequence compatibility audit boundary -/

/--
API boundary for compatibility between cap product and the long exact sequence
of the pair `(M, boundary M)`.

The checked substrate in this file is the generic mathlib long exact homology
sequence for a short exact complex.  The topological pair sequence and the cap
product remain abstract because the pinned local closure has no concrete
relative singular homology object for `(M, boundary M)` and no singular
cohomology cap-product API.  A terminal formalization must replace these fields
by the actual pair sequence and prove the chain-level boundary/cap identity
with the correct sign convention.
-/
structure LefschetzCapLongExactCompatibilityBoundary (R : C)
    {E H M : Type w} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    {I : ModelWithCorners ℝ E H} [ChartedSpace H M] [IsManifold I ∞ M]
    (D : LefschetzPair E H M I)
    (CompactSupportCohomology RelativeHomology AbsoluteHomology BoundaryHomology : ℕ → C) :
    Type (max (u + 1) (v + 1) (w + 1)) where
  pairShortExactChainComplex : Type (max u v w)
  pairLongExactSequence : Type (max u v w)
  capProduct : (p q : ℕ) → (CompactSupportCohomology p ⟶ RelativeHomology (p + q))
  boundaryCapProduct : (p q : ℕ) → (CompactSupportCohomology p ⟶ BoundaryHomology (p + q))
  absoluteToRelativeMap : ∀ n : ℕ, (AbsoluteHomology n ⟶ RelativeHomology n)
  boundaryToAbsoluteMap : ∀ n : ℕ, (BoundaryHomology n ⟶ AbsoluteHomology n)
  relativeConnectingMap : ∀ i j : ℕ, (ComplexShape.down ℕ).Rel i j →
    (RelativeHomology i ⟶ BoundaryHomology j)
  capCommutesWithConnectingMorphisms : Prop
  capCommutesWithBoundaryInclusion : Prop
  capCommutesWithAbsoluteToRelativeMap : Prop
  capProductBoundarySignConvention : Prop
  naturalityForPairBoundaryMaps : Prop
  compatibilitySatisfied :
    capCommutesWithConnectingMorphisms ∧
      capCommutesWithBoundaryInclusion ∧
      capCommutesWithAbsoluteToRelativeMap ∧
      capProductBoundarySignConvention ∧
      naturalityForPairBoundaryMaps

structure CapLongExactCompatibilityAuditRecord where
  moduleName : String
  declarationName : String
  repoLocalStatus : String
  lefschetzDualityRole : String
  blocker : String

/--
Integration-ready audit rows for the child task `S1-M-119-C007`.

The local repository can check generic long-exact homology-sequence exactness
and connecting-map naturality.  It still cannot prove the pair-level
compatibility with cap products because the cap product, compactly supported
cohomology, and relative singular homology of `(M, boundary M)` are not present
as concrete repo-local APIs.
-/
def capLongExactCompatibilityAuditRecords : List CapLongExactCompatibilityAuditRecord := [
  {
    moduleName := "Mathlib.Algebra.Homology.HomologySequenceLemmas",
    declarationName :=
      "HomologicalComplex.HomologySequence.composableArrows₅_exact; HomologicalComplex.HomologySequence.δ_naturality",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    lefschetzDualityRole :=
      "Provides checked generic exactness and connecting-map naturality for the homology sequence of a short exact complex.",
    blocker :=
      "This is algebraic substrate only; it is not yet the long exact sequence of the topological pair `(M, boundary M)`."
  },
  {
    moduleName := "Mathlib.AlgebraicTopology.SingularHomology.Basic",
    declarationName := "singularChainComplexFunctor; singularHomologyFunctor",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    lefschetzDualityRole :=
      "Provides absolute singular chains and homology that the future pair sequence must extend.",
    blocker :=
      "The pinned local closure does not expose the relative singular chain quotient for `(M, boundary M)`."
  },
  {
    moduleName := "Mathlib.AlgebraicTopology; Mathlib.Algebra.Homology",
    declarationName := "no searched topological singular cohomology cap-product compatibility theorem",
    repoLocalStatus := "not_repo_local_closed",
    lefschetzDualityRole :=
      "Would prove that capping with `[M, boundary M]` intertwines cohomology boundary maps with the pair long exact sequence.",
    blocker :=
      "No concrete cap product or chain-level boundary/cap identity is available locally."
  }
]

/-- Machine-readable gate for C007: open, not completed. -/
def capLongExactCompatibilityCompletionGate : String :=
  "open_not_completed: generic long-exact homology sequence exactness and connecting-map naturality are repo-local checked, but there is no concrete cap product, compact-support cohomology, or relative singular homology pair sequence for `(M, boundary M)` to prove the compatibility theorem"

/-- M0387-level child leaves remaining after the C007 compatibility audit. -/
def capLongExactCompatibilityRemainingLeaves : List String := [
  "S1-M-119-C007-L001: define or import the short exact singular-chain sequence whose quotient computes `H_*(M, boundary M)`",
  "S1-M-119-C007-L002: instantiate the resulting long exact sequence for the pair `(M, boundary M)` and identify its boundary maps",
  "S1-M-119-C007-L003: define or import the singular cochain cap product with relative chains and compact-support restrictions",
  "S1-M-119-C007-L004: prove or import the chain-level boundary formula for cap product, including the sign convention used by mathlib's connecting morphism",
  "S1-M-119-C007-L005: prove or import the commutative diagram showing cap product with `[M, boundary M]` is compatible with the pair long exact sequence"
]

/-! ## Completion gate audit boundary -/

structure LefschetzCompletionGateAuditRecord where
  gateName : String
  repoLocalStatus : String
  evidence : String
  requiredForCompletion : String

/--
Integration-ready audit rows for the child task `S1-M-119-C008`.

This is the explicit Stage1 hold gate: THM-M-0547 must remain unchecked until
local Lean validation, machine-anchor audit, M0387 leaf ledger, and public
merge-back are all closed.  The current repo-local file validates only the
statement boundary and adjacent wrappers/audits, so this gate is intentionally
open and cannot be used as terminal theorem evidence.
-/
def lefschetzCompletionGateAuditRecords : List LefschetzCompletionGateAuditRecord := [
  {
    gateName := "local Lean validation",
    repoLocalStatus := "local_statement_boundary_validates",
    evidence :=
      "This file is validated by `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_119.lean`.",
    requiredForCompletion :=
      "A terminal `StatementShape` theorem or imported/wrapped duality theorem must validate in the repo-local Lake closure."
  },
  {
    gateName := "machine anchor audit",
    repoLocalStatus := "open_not_completed",
    evidence :=
      "Audits record mathlib singular-homology/manifold/homology-sequence anchors and no terminal Lefschetz/Poincare-Lefschetz proof body.",
    requiredForCompletion :=
      "If a completed external Lean 4 proof is found, it must be pinned/imported/checked or blocked by a concrete integration reason."
  },
  {
    gateName := "M0387 leaf ledger",
    repoLocalStatus := "open_not_completed",
    evidence :=
      "Remaining leaf lists identify missing relative homology, compact-support cohomology, cap product, fundamental class, pair sequence, and compatibility leaves.",
    requiredForCompletion :=
      "All terminal proof leaves must have checked local proof bodies or checked pinned wrappers and `<=100` step ledger entries."
  },
  {
    gateName := "public merge-back",
    repoLocalStatus := "open_not_completed",
    evidence :=
      "Private runtime ledgers may propose public text, but public Stage1 blueprint/todo completion is a serial integrator action.",
    requiredForCompletion :=
      "The authoritative public checklist must record the exact repo-local validation boundary without marking the theorem completed prematurely."
  }
]

/-- Machine-readable C008 gate: THM-M-0547 remains open, not completed. -/
def lefschetzCompletionGate : String :=
  "open_not_completed: keep THM-M-0547 unchecked until a terminal repo-local Lean theorem or pinned external dependency validates, machine anchors are audited, all M0387 leaves are closed, and public merge-back is complete"

/-- M0387-level child leaves that remain after the C008 completion-gate audit. -/
def lefschetzCompletionGateRemainingLeaves : List String := [
  "S1-M-119-C008-L001: validate any future terminal Lefschetz/Poincare-Lefschetz theorem in the repo-local Lake closure",
  "S1-M-119-C008-L002: keep external proof evidence out of completed state until it is pinned/imported/checked locally or has a concrete integration blocker",
  "S1-M-119-C008-L003: close the remaining relative homology, compact-support cohomology, cap-product, fundamental-class, pair exact-sequence, and compatibility leaves",
  "S1-M-119-C008-L004: serially merge the checked boundary and remaining leaves back to the public Stage1/todo surfaces without editing shared docs from this child worker"
]

/-! ## Audit probes -/

#check ModelWithCorners
#check IsManifold
#check ModelWithCorners.Boundaryless
#check BoundarylessManifold
#check ModelWithCorners.interior
#check ModelWithCorners.boundary
#check ModelWithCorners.interior_union_boundary_eq_univ
#check ModelWithCorners.compl_interior
#check ModelWithCorners.Boundaryless.boundary_eq_empty
#check ModelWithCorners.Boundaryless.iff_boundary_eq_empty
#check ModelWithCorners.interior_eq_univ
#check singularChainComplexFunctor
#check singularHomologyFunctor
#check SSet.RelativeMorphism
#check RelativeSimplicialMorphism
#check CochainComplex
#check CategoryTheory.Sheaf.cohomologyFunctor
#check HasCompactSupport
#check CompactlySupportedContinuousMap
#check CohomologyAPIAuditRecord
#check cohomologyAPIAuditRecords
#check cohomologyAPIAuditCompletionGate
#check ManifoldBoundaryAPIAuditRecord
#check manifoldBoundaryAPIAuditRecords
#check manifold_interior_union_boundary_eq_univ
#check manifold_compl_interior_eq_boundary
#check boundarylessManifold_boundary_eq_empty
#check boundarylessManifold_interior_eq_univ
#check boundarylessManifold_iff_boundary_eq_empty
#check manifoldBoundaryAPIAuditCompletionGate
#check ExternalLeanDualityAuditRecord
#check externalLeanDualityAuditRecords
#check externalLeanDualityAuditCompletionGate
#check modulePositiveOrientationAnchor
#check LefschetzCapFundamentalClassAPIBoundary
#check LefschetzCapFundamentalClassAPIBoundary.fromData
#check CapFundamentalClassAPIAuditRecord
#check capFundamentalClassAPIAuditRecords
#check capFundamentalClassAPIAuditCompletionGate
#check LefschetzCapLongExactCompatibilityBoundary
#check CapLongExactCompatibilityAuditRecord
#check capLongExactCompatibilityAuditRecords
#check capLongExactCompatibilityCompletionGate
#check capLongExactCompatibilityRemainingLeaves
#check LefschetzCompletionGateAuditRecord
#check lefschetzCompletionGateAuditRecords
#check lefschetzCompletionGate
#check lefschetzCompletionGateRemainingLeaves
#check Orientation
#check positiveOrientation
#check isZero_singularHomologyFunctor_of_totallyDisconnectedSpace
#check TopCat.Homotopy.congr_homologyMap_singularChainComplexFunctor
#check ShortComplex.ShortExact.δ
#check ShortComplex.ShortExact.homology_exact₁
#check ShortComplex.ShortExact.homology_exact₂
#check ShortComplex.ShortExact.homology_exact₃
#check HomologicalComplex.HomologySequence.composableArrows₅_exact
#check HomologicalComplex.HomologySequence.δ_naturality

end S1_M_119
end Stage1
end AwesomeTheorems
