import Mathlib.Geometry.Manifold.ChartedSpace
import Mathlib.Geometry.Manifold.ContMDiff.Basic
import Mathlib.Geometry.Manifold.IsManifold.Basic
import Mathlib.Geometry.Manifold.PartitionOfUnity
import Mathlib.Geometry.Manifold.PoincareConjecture
import Mathlib.Geometry.Manifold.SmoothApprox
import Mathlib.Geometry.Manifold.WhitneyEmbedding
import Mathlib.AlgebraicTopology.SimplicialComplex.Basic
import Mathlib.Analysis.Convex.SimplicialComplex.Basic

/-!
# S1-M-254 / THM-M-0607: existence of smooth structures

This Stage1 artifact records a conservative Lean statement boundary for the
existence of smooth structures on topological manifolds.

The pinned mathlib snapshot provides the general `ChartedSpace`,
`ModelWithCorners`, `IsManifold`, and `ContMDiff` framework.  This file does
not assert the false unrestricted statement that every topological manifold is
smoothable.  Instead, it separates the `C^0` manifold input, the obstruction or
low-dimensional smoothability hypothesis, and the requested smooth atlas output.

The declarations below introduce no proof placeholders and make no terminal
proof claim for the classical smoothing theorems.
-/

noncomputable section

open scoped ContDiff Manifold

universe uE uH uM

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_254

/--
Repo-local boundary for the input "topological manifold" structure.

In mathlib, `ChartedSpace H M` supplies an atlas of local homeomorphisms from
`M` to the model space `H`, while `IsManifold I 0 M` records `C^0` transition
compatibility for the chosen model-with-corners `I`.
-/
structure TopologicalManifoldPackage
    (E : Type uE) (H : Type uH) (M : Type uM)
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    (I : ModelWithCorners ℝ E H) : Type (max uH uM) where
  chartedSpace : ChartedSpace H M
  topological :
    letI : ChartedSpace H M := chartedSpace
    IsManifold I 0 M
  separationHypotheses : Prop
  separation_holds : separationHypotheses
  countabilityHypotheses : Prop
  countability_holds : countabilityHypotheses

/--
Low-dimensional positive smoothability branch for the normalized statement.

This package is an input boundary rather than a proof: the future terminal
formalization must replace `lowDimensionalSmoothingInput` by pinned Moise,
surface-classification, triangulation, or one-dimensional smoothing
infrastructure.  The branch deliberately covers only dimensions `<= 3`.
-/
structure LowDimensionalSmoothabilityHypotheses
    {E : Type uE} {H : Type uH} {M : Type uM}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    {I : ModelWithCorners ℝ E H}
    (T : TopologicalManifoldPackage E H M I) : Type (max uH uM) where
  manifoldDimension : ℕ
  dimension_le_three : manifoldDimension ≤ 3
  dimensionMatchesTopologicalAtlas : Prop
  dimension_matches_topological_atlas : dimensionMatchesTopologicalAtlas
  lowDimensionalSmoothingInput : Prop
  low_dimensional_smoothing_input : lowDimensionalSmoothingInput

/--
Dimension-specific branches for the low-dimensional smoothing audit.

This is an audit target, not a proof that the branch exists in the current
Lake closure.  The branches separate the one-dimensional route, the
surface-classification/triangulation route, and the three-dimensional
Moise-style PL/smooth route.
-/
inductive LowDimensionalSmoothingBranch : Type
  | dimensionOne
  | dimensionTwoSurface
  | dimensionThreeMoise
  deriving DecidableEq, Repr

/-- Numerical dimension associated to a low-dimensional smoothing branch. -/
def LowDimensionalSmoothingBranch.dimension :
    LowDimensionalSmoothingBranch → ℕ
  | LowDimensionalSmoothingBranch.dimensionOne => 1
  | LowDimensionalSmoothingBranch.dimensionTwoSurface => 2
  | LowDimensionalSmoothingBranch.dimensionThreeMoise => 3

/-- Every low-dimensional smoothing audit branch is bounded by dimension three. -/
theorem LowDimensionalSmoothingBranch.dimension_le_three
    (B : LowDimensionalSmoothingBranch) : B.dimension ≤ 3 := by
  cases B <;> decide

/--
Formal decomposition target for a branch of low-dimensional smoothing.

All fields are explicit inputs because the current repo-local Lean closure does
not contain terminal proofs of the corresponding classical theorems.  For
dimension one, some fields may be discharged by trivial `True` data once a
dedicated one-dimensional route is formalized; for dimensions two and three
they name the surface-classification, triangulation, and Moise-style
interfaces that must be supplied before the branch can replace the current
abstract `lowDimensionalSmoothingInput : Prop`.
-/
structure LowDimensionalSmoothingDecomposition
    {E : Type uE} {H : Type uH} {M : Type uM}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    {I : ModelWithCorners ℝ E H}
    (T : TopologicalManifoldPackage E H M I)
    (branch : LowDimensionalSmoothingBranch) : Type (max uH uM) where
  dimensionMatchesBranch : Prop
  dimension_matches_branch : dimensionMatchesBranch
  topologicalClassificationAPI : Prop
  topological_classification_api : topologicalClassificationAPI
  triangulationOrPLAPI : Prop
  triangulation_or_pl_api : triangulationOrPLAPI
  smoothAtlasConstructionAPI : Prop
  smooth_atlas_construction_api : smoothAtlasConstructionAPI
  c0CompatibilityBridgeAPI : Prop
  c0_compatibility_bridge_api : c0CompatibilityBridgeAPI

/-- A decomposition target remembers the dimension of its audited branch. -/
def LowDimensionalSmoothingDecomposition.dimension
    {E : Type uE} {H : Type uH} {M : Type uM}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    {I : ModelWithCorners ℝ E H}
    {T : TopologicalManifoldPackage E H M I}
    {branch : LowDimensionalSmoothingBranch}
    (_D : LowDimensionalSmoothingDecomposition T branch) : ℕ :=
  branch.dimension

/-- A decomposition target is still a low-dimensional target. -/
theorem LowDimensionalSmoothingDecomposition.dimension_le_three
    {E : Type uE} {H : Type uH} {M : Type uM}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    {I : ModelWithCorners ℝ E H}
    {T : TopologicalManifoldPackage E H M I}
    {branch : LowDimensionalSmoothingBranch}
    (D : LowDimensionalSmoothingDecomposition T branch) :
    D.dimension ≤ 3 :=
  LowDimensionalSmoothingBranch.dimension_le_three branch

/--
High-dimensional obstruction-vanishing branch for the normalized statement.

The package records the precise kind of side condition needed before a
high-dimensional topological manifold may be treated as smoothable in this
Stage1 boundary: a chosen dimension `>= 5`, a cohomological obstruction API,
Kirby-Siebenmann-style obstruction vanishing, and any remaining smoothing
obstructions or lift data required by the selected formal route.
-/
structure HighDimensionalObstructionVanishingHypotheses
    {E : Type uE} {H : Type uH} {M : Type uM}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    {I : ModelWithCorners ℝ E H}
    (T : TopologicalManifoldPackage E H M I) : Type (max uH uM) where
  manifoldDimension : ℕ
  dimension_at_least_five : 5 ≤ manifoldDimension
  dimensionMatchesTopologicalAtlas : Prop
  dimension_matches_topological_atlas : dimensionMatchesTopologicalAtlas
  obstructionTheoryAPI : Prop
  obstruction_theory_api : obstructionTheoryAPI
  kirbySiebenmannObstructionVanishes : Prop
  kirby_siebenmann_obstruction_vanishes :
    kirbySiebenmannObstructionVanishes
  remainingSmoothabilityObstructionsVanish : Prop
  remaining_smoothability_obstructions_vanish :
    remainingSmoothabilityObstructionsVanish

/-! ## High-dimensional obstruction branch target -/

/--
Named components required by a Kirby-Siebenmann-style smoothability
obstruction branch.

The list is deliberately API-facing.  It separates ordinary cohomology,
degree-four `ZMod 2` coefficients, functoriality/cup-product infrastructure,
characteristic-class definitions, tangent microbundle or classifying data, and
the final smoothability criterion.
-/
inductive ObstructionBranchComponent : Type
  | ordinaryCohomology
  | degreeFourZModTwoCohomology
  | cohomologyNaturality
  | cohomologyCupProduct
  | topologicalTangentMicrobundle
  | characteristicClassPackage
  | stableTopPLOrSmoothLift
  | kirbySiebenmannClass
  | smoothabilityCriterion
  deriving DecidableEq, Repr

/-- Human-readable label for an obstruction-branch component. -/
def ObstructionBranchComponent.label : ObstructionBranchComponent → String
  | ObstructionBranchComponent.ordinaryCohomology =>
      "ordinary cohomology API"
  | ObstructionBranchComponent.degreeFourZModTwoCohomology =>
      "degree-four ZMod 2 cohomology target"
  | ObstructionBranchComponent.cohomologyNaturality =>
      "cohomology pullback and naturality API"
  | ObstructionBranchComponent.cohomologyCupProduct =>
      "cohomology cup-product API"
  | ObstructionBranchComponent.topologicalTangentMicrobundle =>
      "topological tangent microbundle or stable tangent data"
  | ObstructionBranchComponent.characteristicClassPackage =>
      "characteristic-class package"
  | ObstructionBranchComponent.stableTopPLOrSmoothLift =>
      "stable TOP/PL or TOP/O lift obstruction package"
  | ObstructionBranchComponent.kirbySiebenmannClass =>
      "Kirby-Siebenmann obstruction class"
  | ObstructionBranchComponent.smoothabilityCriterion =>
      "obstruction-vanishing implies smoothability criterion"

/--
Detailed target for the high-dimensional obstruction branch.

This is the child-task replacement for the coarse
`obstructionTheoryAPI : Prop` field.  It does not define the actual
Kirby-Siebenmann class in mathlib; instead it fixes the API boundary that a
future proof or pinned upstream dependency must supply before the
high-dimensional branch can be treated as a completed smoothability theorem.
-/
structure KirbySiebenmannObstructionTarget
    {E : Type uE} {H : Type uH} {M : Type uM}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    {I : ModelWithCorners ℝ E H}
    (T : TopologicalManifoldPackage E H M I) : Type (max uH uM) where
  manifoldDimension : ℕ
  dimension_at_least_five : 5 ≤ manifoldDimension
  dimensionMatchesTopologicalAtlas : Prop
  dimension_matches_topological_atlas : dimensionMatchesTopologicalAtlas
  ordinaryCohomologyAPI : Prop
  ordinary_cohomology_api : ordinaryCohomologyAPI
  degreeFourZModTwoCohomologyAPI : Prop
  degree_four_zmod_two_cohomology_api : degreeFourZModTwoCohomologyAPI
  cohomologyPullbackNaturalityAPI : Prop
  cohomology_pullback_naturality_api : cohomologyPullbackNaturalityAPI
  cohomologyCupProductAPI : Prop
  cohomology_cup_product_api : cohomologyCupProductAPI
  topologicalTangentMicrobundleAPI : Prop
  topological_tangent_microbundle_api : topologicalTangentMicrobundleAPI
  characteristicClassAPI : Prop
  characteristic_class_api : characteristicClassAPI
  stableTopPLOrSmoothLiftAPI : Prop
  stable_top_pl_or_smooth_lift_api : stableTopPLOrSmoothLiftAPI
  kirbySiebenmannClassAPI : Prop
  kirby_siebenmann_class_api : kirbySiebenmannClassAPI
  kirbySiebenmannObstructionVanishes : Prop
  kirby_siebenmann_obstruction_vanishes :
    kirbySiebenmannObstructionVanishes
  smoothabilityCriterionAPI : Prop
  smoothability_criterion_api : smoothabilityCriterionAPI

/--
The conjunction of obstruction-theory APIs required before the detailed
Kirby-Siebenmann target can feed the coarse high-dimensional branch.
-/
def KirbySiebenmannObstructionTarget.obstructionTheoryReady
    {E : Type uE} {H : Type uH} {M : Type uM}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    {I : ModelWithCorners ℝ E H}
    {T : TopologicalManifoldPackage E H M I}
    (K : KirbySiebenmannObstructionTarget T) : Prop :=
  K.ordinaryCohomologyAPI ∧
    K.degreeFourZModTwoCohomologyAPI ∧
    K.cohomologyPullbackNaturalityAPI ∧
    K.cohomologyCupProductAPI ∧
    K.topologicalTangentMicrobundleAPI ∧
    K.characteristicClassAPI ∧
    K.stableTopPLOrSmoothLiftAPI ∧
    K.kirbySiebenmannClassAPI ∧
    K.smoothabilityCriterionAPI

/-- The detailed target supplies its bundled obstruction-theory API. -/
theorem KirbySiebenmannObstructionTarget.obstructionTheoryReady_holds
    {E : Type uE} {H : Type uH} {M : Type uM}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    {I : ModelWithCorners ℝ E H}
    {T : TopologicalManifoldPackage E H M I}
    (K : KirbySiebenmannObstructionTarget T) :
    K.obstructionTheoryReady := by
  exact ⟨K.ordinary_cohomology_api,
    K.degree_four_zmod_two_cohomology_api,
    K.cohomology_pullback_naturality_api,
    K.cohomology_cup_product_api,
    K.topological_tangent_microbundle_api,
    K.characteristic_class_api,
    K.stable_top_pl_or_smooth_lift_api,
    K.kirby_siebenmann_class_api,
    K.smoothability_criterion_api⟩

/--
The remaining branch data beyond Kirby-Siebenmann vanishing: stable lift data
and the theorem/API turning obstruction vanishing into a compatible smooth
atlas construction.
-/
def KirbySiebenmannObstructionTarget.remainingSmoothabilityReady
    {E : Type uE} {H : Type uH} {M : Type uM}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    {I : ModelWithCorners ℝ E H}
    {T : TopologicalManifoldPackage E H M I}
    (K : KirbySiebenmannObstructionTarget T) : Prop :=
  K.stableTopPLOrSmoothLiftAPI ∧ K.smoothabilityCriterionAPI

/-- The detailed target supplies the non-KS lift and criterion data. -/
theorem KirbySiebenmannObstructionTarget.remainingSmoothabilityReady_holds
    {E : Type uE} {H : Type uH} {M : Type uM}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    {I : ModelWithCorners ℝ E H}
    {T : TopologicalManifoldPackage E H M I}
    (K : KirbySiebenmannObstructionTarget T) :
    K.remainingSmoothabilityReady :=
  ⟨K.stable_top_pl_or_smooth_lift_api, K.smoothability_criterion_api⟩

/--
A detailed Kirby-Siebenmann target refines the existing coarse
high-dimensional obstruction-vanishing hypothesis package.
-/
def KirbySiebenmannObstructionTarget.toHighDimensionalHypotheses
    {E : Type uE} {H : Type uH} {M : Type uM}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    {I : ModelWithCorners ℝ E H}
    {T : TopologicalManifoldPackage E H M I}
    (K : KirbySiebenmannObstructionTarget T) :
    HighDimensionalObstructionVanishingHypotheses T where
  manifoldDimension := K.manifoldDimension
  dimension_at_least_five := K.dimension_at_least_five
  dimensionMatchesTopologicalAtlas := K.dimensionMatchesTopologicalAtlas
  dimension_matches_topological_atlas :=
    K.dimension_matches_topological_atlas
  obstructionTheoryAPI := K.obstructionTheoryReady
  obstruction_theory_api := K.obstructionTheoryReady_holds
  kirbySiebenmannObstructionVanishes :=
    K.kirbySiebenmannObstructionVanishes
  kirby_siebenmann_obstruction_vanishes :=
    K.kirby_siebenmann_obstruction_vanishes
  remainingSmoothabilityObstructionsVanish :=
    K.remainingSmoothabilityReady
  remaining_smoothability_obstructions_vanish :=
    K.remainingSmoothabilityReady_holds

/--
Explicit replacement for the informal slogan "topological manifolds have smooth
structures".

The normalized scope is a disjunction of known-positive low-dimensional input
and high-dimensional obstruction-vanishing input.  Dimension four is not placed
in either branch by this Stage1 boundary.
-/
inductive SmoothabilityRoute
    {E : Type uE} {H : Type uH} {M : Type uM}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    {I : ModelWithCorners ℝ E H}
    (T : TopologicalManifoldPackage E H M I) : Type (max uH uM)
  | lowDimensional :
      LowDimensionalSmoothabilityHypotheses T → SmoothabilityRoute T
  | highDimensionalObstructionVanishing :
      HighDimensionalObstructionVanishingHypotheses T → SmoothabilityRoute T

/-- A detailed obstruction target produces the high-dimensional route. -/
def SmoothabilityRoute.highDimensionalFromKirbySiebenmannTarget
    {E : Type uE} {H : Type uH} {M : Type uM}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    {I : ModelWithCorners ℝ E H}
    {T : TopologicalManifoldPackage E H M I}
    (K : KirbySiebenmannObstructionTarget T) : SmoothabilityRoute T :=
  SmoothabilityRoute.highDimensionalObstructionVanishing
    K.toHighDimensionalHypotheses

/--
Explicit smoothability side conditions.

Classical smoothing theorems require either low-dimensional positive input or
high-dimensional obstruction-vanishing data.  The local Lean boundary keeps
that disjunction explicit until the relevant obstruction theory, triangulation,
cobordism, or low-dimensional classification package is available in the
repo-local dependency closure.
-/
structure SmoothabilityHypotheses
    {E : Type uE} {H : Type uH} {M : Type uM}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    {I : ModelWithCorners ℝ E H}
    (T : TopologicalManifoldPackage E H M I) : Type (max uH uM) where
  route : SmoothabilityRoute T
  atlasCompatibilityCondition : Prop
  atlasCompatibility_holds : atlasCompatibilityCondition

/--
Concrete C0 compatibility relation between an input topological atlas and an
output smooth maximal atlas.

The first inclusion says each input topological chart is C0-compatible with the
output charted space.  The second says each chart in the output smooth maximal
atlas is C0-compatible with the input topological charted space.  This avoids
the too-strong requirement that every original topological chart be smooth.
-/
def AtlasC0Compatibility
    {H : Type uH} {M : Type uM}
    [TopologicalSpace H] [TopologicalSpace M]
    (inputTopologicalAtlas : Set (OpenPartialHomeomorph M H))
    (outputC0MaximalAtlas : Set (OpenPartialHomeomorph M H))
    (outputSmoothMaximalAtlas : Set (OpenPartialHomeomorph M H))
    (inputC0MaximalAtlas : Set (OpenPartialHomeomorph M H)) : Prop :=
  inputTopologicalAtlas ⊆ outputC0MaximalAtlas ∧
    outputSmoothMaximalAtlas ⊆ inputC0MaximalAtlas

/--
The concrete compatibility predicate used by `SmoothStructurePackage`.

It compares the atlas from `T.chartedSpace` with the `∞` maximal atlas generated
by the candidate smooth charted space, with both sides relaxed to C0
compatibility in the opposite charted space.
-/
def CompatibleWithTopologicalAtlas
    {E : Type uE} {H : Type uH} {M : Type uM}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    (I : ModelWithCorners ℝ E H)
    (T : TopologicalManifoldPackage E H M I)
    (smoothChartedSpace : ChartedSpace H M) : Prop :=
  letI : ChartedSpace H M := T.chartedSpace
  let inputTopologicalAtlas : Set (OpenPartialHomeomorph M H) := atlas H M
  let inputC0MaximalAtlas : Set (OpenPartialHomeomorph M H) :=
    IsManifold.maximalAtlas I 0 M
  letI : ChartedSpace H M := smoothChartedSpace
  let outputC0MaximalAtlas : Set (OpenPartialHomeomorph M H) :=
    IsManifold.maximalAtlas I 0 M
  let outputSmoothMaximalAtlas : Set (OpenPartialHomeomorph M H) :=
    IsManifold.maximalAtlas I ∞ M
  AtlasC0Compatibility inputTopologicalAtlas outputC0MaximalAtlas
    outputSmoothMaximalAtlas inputC0MaximalAtlas

/-- The input atlas side of `AtlasC0Compatibility`. -/
theorem AtlasC0Compatibility.input_subset_output_c0
    {H : Type uH} {M : Type uM}
    [TopologicalSpace H] [TopologicalSpace M]
    {inputTopologicalAtlas : Set (OpenPartialHomeomorph M H)}
    {outputC0MaximalAtlas : Set (OpenPartialHomeomorph M H)}
    {outputSmoothMaximalAtlas : Set (OpenPartialHomeomorph M H)}
    {inputC0MaximalAtlas : Set (OpenPartialHomeomorph M H)}
    (h : AtlasC0Compatibility inputTopologicalAtlas outputC0MaximalAtlas
      outputSmoothMaximalAtlas inputC0MaximalAtlas) :
    inputTopologicalAtlas ⊆ outputC0MaximalAtlas :=
  h.1

/-- The output smooth maximal atlas side of `AtlasC0Compatibility`. -/
theorem AtlasC0Compatibility.output_smooth_subset_input_c0
    {H : Type uH} {M : Type uM}
    [TopologicalSpace H] [TopologicalSpace M]
    {inputTopologicalAtlas : Set (OpenPartialHomeomorph M H)}
    {outputC0MaximalAtlas : Set (OpenPartialHomeomorph M H)}
    {outputSmoothMaximalAtlas : Set (OpenPartialHomeomorph M H)}
    {inputC0MaximalAtlas : Set (OpenPartialHomeomorph M H)}
    (h : AtlasC0Compatibility inputTopologicalAtlas outputC0MaximalAtlas
      outputSmoothMaximalAtlas inputC0MaximalAtlas) :
    outputSmoothMaximalAtlas ⊆ inputC0MaximalAtlas :=
  h.2

/--
Output package for a smooth structure on the same underlying topological type.
-/
structure SmoothStructurePackage
    (E : Type uE) (H : Type uH) (M : Type uM)
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    (I : ModelWithCorners ℝ E H)
    (T : TopologicalManifoldPackage E H M I) : Type (max uH uM) where
  smoothChartedSpace : ChartedSpace H M
  smooth :
    letI : ChartedSpace H M := smoothChartedSpace
    IsManifold I ∞ M
  compatibleWithTopologicalAtlas :
    CompatibleWithTopologicalAtlas I T smoothChartedSpace

/--
Normalized Stage1 statement shape for smooth-structure existence.

Given a `C^0` manifold package and explicit smoothability hypotheses, produce a
smooth atlas on the same underlying topological space.  This is a formalization
boundary, not a proof of a smoothing theorem.
-/
def StatementShape
    (E : Type uE) (H : Type uH) (M : Type uM)
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    (I : ModelWithCorners ℝ E H) : Prop :=
  ∀ T : TopologicalManifoldPackage E H M I,
    SmoothabilityHypotheses T →
      Nonempty (SmoothStructurePackage E H M I T)

/--
Public statement-normalization note for THM-M-0607.

`StatementShape` is the current repo-local Lean boundary for the smooth-structure
existence entry: it asks for a smooth atlas only after the `C^0` manifold input,
the dimension-or-obstruction smoothability side condition, and the atlas
compatibility side condition have been supplied.  This boundary is intentionally
not the terminal proof of smooth-structure existence.
-/
def statementNormalizationNote : List String := [
  "THM-M-0607 is normalized repo-locally by AwesomeTheorems.Stage1.S1_M_254.StatementShape.",
  "The boundary requires an explicit C^0 topological-manifold package and a SmoothabilityRoute before producing a smooth-structure package.",
  "The output package uses CompatibleWithTopologicalAtlas: input topological charts must lie in the output C^0 maximal atlas, and output smooth-maximal charts must lie in the input C^0 maximal atlas.",
  "SmoothabilityRoute is the statement-scope disjunction: low-dimensional positive input for dimensions <= 3, or high-dimensional obstruction-vanishing input for dimensions >= 5.",
  "Dimension four is not included in either branch by this Stage1 statement boundary.",
  "This checked Lean boundary is not a terminal proof of smooth-structure existence."
]

/-- The smoothability route is exactly the low-dimensional or high-dimensional branch. -/
theorem smoothabilityRoute_cases
    {E : Type uE} {H : Type uH} {M : Type uM}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    {I : ModelWithCorners ℝ E H}
    {T : TopologicalManifoldPackage E H M I}
    (S : SmoothabilityHypotheses T) :
    (∃ L : LowDimensionalSmoothabilityHypotheses T,
      S.route = SmoothabilityRoute.lowDimensional L) ∨
    (∃ O : HighDimensionalObstructionVanishingHypotheses T,
      S.route = SmoothabilityRoute.highDimensionalObstructionVanishing O) := by
  cases S.route with
  | lowDimensional L =>
      exact Or.inl ⟨L, rfl⟩
  | highDimensionalObstructionVanishing O =>
      exact Or.inr ⟨O, rfl⟩

/-- The low-dimensional branch is bounded by dimension three. -/
theorem lowDimensionalSmoothability_dimension_le_three
    {E : Type uE} {H : Type uH} {M : Type uM}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    {I : ModelWithCorners ℝ E H}
    {T : TopologicalManifoldPackage E H M I}
    (L : LowDimensionalSmoothabilityHypotheses T) :
    L.manifoldDimension ≤ 3 :=
  L.dimension_le_three

/-- The high-dimensional obstruction branch starts at dimension five. -/
theorem highDimensionalObstruction_dimension_at_least_five
    {E : Type uE} {H : Type uH} {M : Type uM}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    {I : ModelWithCorners ℝ E H}
    {T : TopologicalManifoldPackage E H M I}
    (O : HighDimensionalObstructionVanishingHypotheses T) :
    5 ≤ O.manifoldDimension :=
  O.dimension_at_least_five

/--
Public-scope summary for the `THM-M-0607.statement-scope` child task.

This is integration-ready metadata, not a public-doc edit and not a completion
claim.
-/
def statementScopeBackfillProposal : List String := [
  "Replace the slogan 'topological manifolds have smooth structures' by the checked repo-local disjunction AwesomeTheorems.Stage1.S1_M_254.SmoothabilityRoute.",
  "Low-dimensional branch: supply LowDimensionalSmoothabilityHypotheses T, including a dimension n <= 3, a proof that this dimension matches the topological atlas, and a pinned low-dimensional smoothing input such as one-dimensional smoothing, surface classification/triangulation, or Moise-style 3-manifold smoothing infrastructure.",
  "High-dimensional branch: supply HighDimensionalObstructionVanishingHypotheses T, including a dimension n >= 5, a proof that this dimension matches the topological atlas, a cohomological obstruction-theory API, Kirby-Siebenmann-style obstruction vanishing, and vanishing or lift data for any remaining smoothability obstructions required by the selected route.",
  "Dimension four is not closed by this statement scope and must remain outside the completion claim unless a separate pinned theorem or explicit hypothesis package is added.",
  "The resulting StatementShape remains conditional: TopologicalManifoldPackage plus SmoothabilityHypotheses yields Nonempty SmoothStructurePackage; it is not a terminal proof of smooth-structure existence."
]

/--
Public-scope summary for the `THM-M-0607.compatibility` child task.

This is integration-ready metadata, not a public-doc edit and not a completion
claim.
-/
def compatibilityBackfillProposal : List String := [
  "Replace the abstract output field `compatibleWithTopologicalAtlas : Prop` by the checked predicate `AwesomeTheorems.Stage1.S1_M_254.CompatibleWithTopologicalAtlas`.",
  "`CompatibleWithTopologicalAtlas I T smoothChartedSpace` binds the input charted space `T.chartedSpace`, records its atlas and C^0 maximal atlas, then binds the output `smoothChartedSpace` and records its C^0 and C^∞ maximal atlases.",
  "The concrete relation is `AtlasC0Compatibility inputTopologicalAtlas outputC0MaximalAtlas outputSmoothMaximalAtlas inputC0MaximalAtlas`, i.e. input atlas charts are contained in the output C^0 maximal atlas and output C^∞ maximal atlas charts are contained in the input C^0 maximal atlas.",
  "This is intentionally weaker than requiring every original topological chart to be smooth in the output structure; it records equivalence of the underlying C^0 atlas structures while allowing a genuinely new smooth atlas.",
  "The compatibility bridge is statement-shape progress only. It does not prove the low-dimensional smoothing branch, the high-dimensional obstruction branch, or a terminal smooth-structure existence theorem."
]

/-! ## Low-dimensional smoothing audit -/

/-- Machine-readable row for the low-dimensional smoothing component audit. -/
structure LowDimensionalSmoothingAuditRow where
  branch : LowDimensionalSmoothingBranch
  component : String
  checkedLocalLeanAnchors : List String
  repoLocalClosure : String
  integrationBlocker : String

/--
Audit rows for the `THM-M-0607.low-dimensional` child.

The current repo-local closure has generic manifold and simplicial-complex
objects, but not terminal Lean 4 components for one-dimensional smoothing,
surface classification, manifold triangulation, or Moise-style
three-dimensional PL/smooth compatibility.
-/
def lowDimensionalSmoothingAuditRows : List LowDimensionalSmoothingAuditRow := [
  { branch := LowDimensionalSmoothingBranch.dimensionOne
    component := "one-dimensional topological-manifold smoothing"
    checkedLocalLeanAnchors := [
      "ChartedSpace",
      "IsManifold I 0",
      "IsManifold I ∞",
      "Mathlib.Geometry.Manifold.Instances.Real" ]
    repoLocalClosure := "not_repo_local_closed"
    integrationBlocker :=
      "No checked theorem was located that classifies one-dimensional topological manifolds and constructs a compatible smooth atlas from an arbitrary C0 atlas." },
  { branch := LowDimensionalSmoothingBranch.dimensionTwoSurface
    component := "surface classification input"
    checkedLocalLeanAnchors := [
      "Mathlib.Geometry.Manifold.PoincareConjecture mentions the classical n = 2 route",
      "ChartedSpace",
      "IsManifold I 0" ]
    repoLocalClosure := "not_repo_local_closed"
    integrationBlocker :=
      "No checked Lean 4 surface-classification theorem or closed-surface normal-form API was located in the repo-local Lake closure." },
  { branch := LowDimensionalSmoothingBranch.dimensionTwoSurface
    component := "surface triangulation or PL bridge"
    checkedLocalLeanAnchors := [
      "PreAbstractSimplicialComplex",
      "AbstractSimplicialComplex",
      "Geometry.SimplicialComplex" ]
    repoLocalClosure := "generic_simplicial_complex_api_only"
    integrationBlocker :=
      "The generic simplicial-complex APIs do not provide a theorem that every topological surface has a compatible triangulation or PL structure." },
  { branch := LowDimensionalSmoothingBranch.dimensionThreeMoise
    component := "Moise-style three-dimensional triangulation and smoothing"
    checkedLocalLeanAnchors := [
      "ChartedSpace",
      "IsManifold I 0",
      "AbstractSimplicialComplex",
      "Geometry.SimplicialComplex" ]
    repoLocalClosure := "not_repo_local_closed"
    integrationBlocker :=
      "No Lean 4 theorem named or matching Moise, 3-manifold triangulation, PL uniqueness, or PL-to-smooth compatibility was located in the checked local closure." },
  { branch := LowDimensionalSmoothingBranch.dimensionThreeMoise
    component := "output atlas compatibility after low-dimensional construction"
    checkedLocalLeanAnchors := [
      "AtlasC0Compatibility",
      "CompatibleWithTopologicalAtlas",
      "IsManifold.maximalAtlas" ]
    repoLocalClosure := "statement_boundary_checked_only"
    integrationBlocker :=
      "The compatibility predicate is checked, but no low-dimensional construction currently produces the output smooth atlas and proves this predicate." }
]

/-- The low-dimensional smoothing audit has five component rows. -/
theorem lowDimensionalSmoothingAuditRows_length :
    lowDimensionalSmoothingAuditRows.length = 5 :=
  rfl

/-- Public backfill text for the low-dimensional smoothing audit child. -/
def lowDimensionalBackfillProposal : List String := [
  "THM-M-0607.low-dimensional audit: keep the branch open. The checked repo-local Lean artifact now separates low-dimensional smoothing into `LowDimensionalSmoothingBranch.dimensionOne`, `.dimensionTwoSurface`, and `.dimensionThreeMoise`, with `LowDimensionalSmoothingDecomposition` naming the required dimension match, topological-classification API, triangulation/PL API, smooth-atlas construction API, and C0 compatibility bridge.",
  "At pinned mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95, the local closure has `ChartedSpace`, `IsManifold`, maximal-atlas infrastructure, and generic `PreAbstractSimplicialComplex` / `AbstractSimplicialComplex` / `Geometry.SimplicialComplex` APIs. These are supporting objects only.",
  "No repo-local Lean theorem was located for one-dimensional topological-manifold classification plus smoothing, surface classification, triangulation of topological surfaces or 3-manifolds, Moise-style PL uniqueness/smoothing, or a construction that returns a smooth atlas satisfying `CompatibleWithTopologicalAtlas`.",
  "Machine status for this child is `not_repo_local_closed` / active `formalization_debt`, not `repo_local_integration_debt`: no terminal external Lean 4 proof was found in this child pass, and no completion claim is made.",
  "Do not close `THM-M-0607.low-dimensional` until the missing 1D/2D/3D route components are supplied by local proof bodies or pinned/imported/checked upstream Lean dependencies, followed by `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_254.lean`."
]

/-! ## Kirby-Siebenmann obstruction audit -/

/-- Machine-readable row for the high-dimensional obstruction branch audit. -/
structure ObstructionBranchAuditRow where
  component : ObstructionBranchComponent
  requiredAPI : String
  checkedLocalLeanAnchors : List String
  repoLocalClosure : String
  integrationBlocker : String

/--
Audit rows for the `THM-M-0607.obstruction` child.

The current repo-local closure contains broad manifold, vector-bundle, and
homological-algebra infrastructure, but not ordinary topological cohomology
with `ZMod 2` coefficients, characteristic classes, Kirby-Siebenmann classes,
or a smoothability criterion turning obstruction vanishing into a smooth atlas.
-/
def obstructionBranchAuditRows : List ObstructionBranchAuditRow := [
  { component := ObstructionBranchComponent.ordinaryCohomology
    requiredAPI := "ordinary cohomology H^n(X; A) for topological spaces/manifolds"
    checkedLocalLeanAnchors := [
      "CategoryTheory.Sites.SheafCohomology.Basic is adjacent but sheaf-oriented",
      "AlgebraicTopology.SingularHomology.Basic provides singular homology, not the required cohomology target" ]
    repoLocalClosure := "not_repo_local_closed"
    integrationBlocker :=
      "No checked ordinary cohomology functor for topological spaces with the required coefficient specialization was located in the local Lake closure." },
  { component := ObstructionBranchComponent.degreeFourZModTwoCohomology
    requiredAPI := "the Kirby-Siebenmann target group H^4(M; ZMod 2)"
    checkedLocalLeanAnchors := [
      "Nat degree bookkeeping",
      "ZMod exists in algebra libraries but is not connected here to topological cohomology" ]
    repoLocalClosure := "not_repo_local_closed"
    integrationBlocker :=
      "The branch still needs a concrete cohomology object in degree four with ZMod 2 coefficients and zero/equality predicates." },
  { component := ObstructionBranchComponent.cohomologyNaturality
    requiredAPI := "pullback maps and naturality for cohomology classes under maps of spaces"
    checkedLocalLeanAnchors := [
      "ContinuousMap",
      "TopCat",
      "category-theoretic functor infrastructure" ]
    repoLocalClosure := "support_only"
    integrationBlocker :=
      "Functorial cohomology pullback for the chosen ordinary cohomology model has not been instantiated." },
  { component := ObstructionBranchComponent.cohomologyCupProduct
    requiredAPI := "cup product/ring structure and coefficient-change operations as needed by characteristic-class formulas"
    checkedLocalLeanAnchors := [
      "general algebraic and homological algebra infrastructure" ]
    repoLocalClosure := "not_repo_local_closed"
    integrationBlocker :=
      "No ordinary cohomology ring or cup-product API for the target topological spaces was located." },
  { component := ObstructionBranchComponent.topologicalTangentMicrobundle
    requiredAPI := "topological tangent microbundle or stable tangent classifying data for C0 manifolds"
    checkedLocalLeanAnchors := [
      "TangentSpace and TangentBundle exist for smooth manifolds",
      "VectorBundle and FiberBundle APIs exist" ]
    repoLocalClosure := "smooth_support_only"
    integrationBlocker :=
      "The available tangent-bundle APIs are smooth-manifold APIs; no topological tangent microbundle for arbitrary C0 manifolds was located." },
  { component := ObstructionBranchComponent.characteristicClassPackage
    requiredAPI := "Stiefel-Whitney/Pontryagin-style characteristic-class package or the exact classifying substitute used by KS theory"
    checkedLocalLeanAnchors := [
      "VectorBundle",
      "ContMDiffVectorBundle" ]
    repoLocalClosure := "not_repo_local_closed"
    integrationBlocker :=
      "No characteristic-class definitions for vector bundles, microbundles, TOP/PL, or TOP/O classifying spaces were located." },
  { component := ObstructionBranchComponent.stableTopPLOrSmoothLift
    requiredAPI := "stable TOP/PL or TOP/O lift obstruction and comparison to smooth structures"
    checkedLocalLeanAnchors := [
      "ChartedSpace",
      "IsManifold",
      "AtlasC0Compatibility" ]
    repoLocalClosure := "not_repo_local_closed"
    integrationBlocker :=
      "No PL manifold category, TOP/PL comparison, or stable smoothing lift theorem is available in the repo-local dependency closure." },
  { component := ObstructionBranchComponent.kirbySiebenmannClass
    requiredAPI := "definition of ks(M) in H^4(M; ZMod 2), its zero class, and vanishing predicate"
    checkedLocalLeanAnchors := [
      "KirbySiebenmannObstructionTarget.kirbySiebenmannClassAPI",
      "KirbySiebenmannObstructionTarget.kirbySiebenmannObstructionVanishes" ]
    repoLocalClosure := "statement_boundary_checked_only"
    integrationBlocker :=
      "The local target names the KS class API, but no proof body defines the class or proves its properties." },
  { component := ObstructionBranchComponent.smoothabilityCriterion
    requiredAPI := "theorem that obstruction vanishing plus side hypotheses yields a compatible smooth atlas"
    checkedLocalLeanAnchors := [
      "KirbySiebenmannObstructionTarget.toHighDimensionalHypotheses",
      "SmoothabilityRoute.highDimensionalFromKirbySiebenmannTarget",
      "StatementShape" ]
    repoLocalClosure := "statement_boundary_checked_only"
    integrationBlocker :=
      "The checked conversion feeds the normalized statement shape, but the terminal smoothability theorem is still absent." }
]

/-- The obstruction branch audit has one row for each required component. -/
theorem obstructionBranchAuditRows_length :
    obstructionBranchAuditRows.length = 9 :=
  rfl

/-- Public backfill text for the obstruction-branch child. -/
def obstructionBackfillProposal : List String := [
  "THM-M-0607.obstruction: keep the branch open, but replace the coarse obstruction placeholder by the checked target `AwesomeTheorems.Stage1.S1_M_254.KirbySiebenmannObstructionTarget`.",
  "`KirbySiebenmannObstructionTarget` requires dimension n >= 5, a dimension/topological-atlas match, ordinary cohomology, the degree-four `ZMod 2` cohomology target, cohomology pullback naturality, cup product, topological tangent microbundle or stable tangent data, characteristic-class APIs, stable TOP/PL or TOP/O lift data, a Kirby-Siebenmann class API, vanishing of that obstruction, and the smoothability criterion.",
  "The checked conversion `KirbySiebenmannObstructionTarget.toHighDimensionalHypotheses` refines the existing `HighDimensionalObstructionVanishingHypotheses`; `SmoothabilityRoute.highDimensionalFromKirbySiebenmannTarget` feeds it into the normalized statement route.",
  "At pinned mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95, the repo-local closure has manifold, smooth tangent/vector-bundle, generic homological-algebra, sheaf-cohomology, and singular-homology support, but no ordinary topological cohomology H^4(M; ZMod 2), no characteristic classes, no Kirby-Siebenmann class, no PL/TOP comparison package, and no obstruction-vanishing smoothability theorem.",
  "Machine status is `not_repo_local_closed` with active `formalization_debt`; this child introduces no completion claim and no `repo_local_integration_debt` completion state."
]

/-! ## External smoothability audit -/

/-- Machine-readable row for the external Lean 4 smoothability audit. -/
structure ExternalSmoothabilityAuditRow where
  searchTerms : List String
  source : String
  terminalLeanProofFound : Bool
  repoLocalAction : String
  integrationBlocker : String

/--
Rows for the `THM-M-0607.external-audit` child.

The pass searched GitHub-facing Lean 4 sources for Moise, Kirby-Siebenmann,
smoothability, PL-manifold, triangulation, and topological-manifold smooth
structure terminology.  No terminal upstream Lean 4 theorem was located, so
there is no external proof to pin/import/check in this child pass.
-/
def externalSmoothabilityAuditRows : List ExternalSmoothabilityAuditRow := [
  { searchTerms := [
      "Moise",
      "topological manifold smooth structure",
      "Lean 4" ]
    source := "GitHub web search"
    terminalLeanProofFound := false
    repoLocalAction := "no pin/import/check target available"
    integrationBlocker :=
      "No GitHub-hosted Lean 4 theorem for Moise-style 3-manifold triangulation, PL uniqueness, or PL-to-smooth compatibility was found." },
  { searchTerms := [
      "KirbySiebenmann",
      "Kirby-Siebenmann",
      "smoothable",
      "Lean 4" ]
    source := "GitHub web search"
    terminalLeanProofFound := false
    repoLocalAction := "no pin/import/check target available"
    integrationBlocker :=
      "No GitHub-hosted Lean 4 definition of a Kirby-Siebenmann class, obstruction-vanishing predicate, or smoothability theorem was found." },
  { searchTerms := [
      "PL manifold",
      "triangulation",
      "topological manifold",
      "Lean" ]
    source := "GitHub web search"
    terminalLeanProofFound := false
    repoLocalAction := "no pin/import/check target available"
    integrationBlocker :=
      "No GitHub-hosted Lean theorem for topological-manifold triangulation, PL-manifold structure, or PL-to-smooth comparison was found." },
  { searchTerms := [
      "Lean4 Moise topological manifold smooth structure",
      "Lean4 Kirby Siebenmann smoothable PL manifold",
      "Lean4 smoothable topological manifold triangulation" ]
    source := "GitHub repository search API"
    terminalLeanProofFound := false
    repoLocalAction := "no repository dependency to add"
    integrationBlocker :=
      "Repository search returned no candidate Lean/Lean4 upstream project for the requested smoothability routes; unauthenticated GitHub code search requires authentication and could not be used as a pin source." }
]

/-- The external smoothability audit has four source/query rows. -/
theorem externalSmoothabilityAuditRows_length :
    externalSmoothabilityAuditRows.length = 4 :=
  rfl

/-- Public backfill text for the external Lean 4 smoothability audit child. -/
def externalSmoothabilityBackfillProposal : List String := [
  "THM-M-0607.external-audit: keep the branch open. A 2026-05-01 primary-source GitHub-facing Lean 4 audit for `Moise`, `KirbySiebenmann`, `Kirby-Siebenmann`, `smoothable`, `PL manifold`, `triangulation`, and `topological manifold smooth structure` did not locate a terminal Lean 4 proof of smooth-structure existence or smoothability for the required low-dimensional or obstruction-vanishing branches.",
  "Checked local artifact: `AwesomeTheorems.Stage1.S1_M_254.externalSmoothabilityAuditRows` records the external search rows and integration blockers. Validation must remain `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_254.lean`.",
  "No external proof is available to pin/import/check from this pass. The status is active `formalization_debt`, not completed `external_upstream_anchor_only`; therefore no completed-state `repo_local_integration_debt` is retained.",
  "If a later audit finds an upstream Lean 4 theorem, the next integrator must record the repository, commit SHA, module, theorem names, license/import compatibility, and either add a pinned dependency or document the concrete blocker before any completion checkbox is changed."
]

/-! ## Completion gate audit -/

/-- M0387-level machine-status labels for the THM-M-0607 completion gate. -/
inductive RepoLocalMachineStatus : Type
  | localProofBody
  | localWrapperUpstreamMathlib
  | externalUpstreamPinned
  | externalUpstreamAnchorOnly
  | notRepoLocalClosed
  deriving DecidableEq, Repr

/--
Machine-readable audit row for the `THM-M-0607.completion-gate` child.

This is a local ledger surface inside the owned Lean artifact.  It does not
mark the theorem complete; it records the exact blockers that prevent a public
completion checkbox from being changed by this child task.
-/
structure CompletionGateAudit where
  validationCommand : String
  terminalTheoremOrPinnedWrapperPresent : Bool
  publicBlueprintTodoReadmeMerged : Bool
  completionClaimed : Bool
  machineStatus : RepoLocalMachineStatus
  completedStateRetainsRepoLocalIntegrationDebt : Bool
  blocker : String

/--
Current completion-gate state for THM-M-0607.

The Lean file itself can be validated, but the validated declarations are
statement-shape, audit, and wrapper metadata only.  They are not a terminal
smooth-structure existence theorem and are not a pinned upstream wrapper.
-/
def completionGateAudit : CompletionGateAudit where
  validationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_254.lean"
  terminalTheoremOrPinnedWrapperPresent := false
  publicBlueprintTodoReadmeMerged := false
  completionClaimed := false
  machineStatus := RepoLocalMachineStatus.notRepoLocalClosed
  completedStateRetainsRepoLocalIntegrationDebt := false
  blocker :=
    "No terminal smoothability theorem or pinned upstream wrapper is present; public blueprint/todo/README surfaces still require a serial integrator merge before any completion state can be claimed."

/-- The current completion-gate audit makes no completion claim. -/
theorem completionGateAudit_no_completion_claim :
    completionGateAudit.completionClaimed = false :=
  rfl

/-- The current gate has no terminal local theorem or pinned upstream wrapper. -/
theorem completionGateAudit_no_terminal_theorem_or_pinned_wrapper :
    completionGateAudit.terminalTheoremOrPinnedWrapperPresent = false :=
  rfl

/-- The shared public status surfaces have not been serially merged by this child. -/
theorem completionGateAudit_public_surfaces_not_merged :
    completionGateAudit.publicBlueprintTodoReadmeMerged = false :=
  rfl

/-- The current machine status remains open under repo-local closure rules. -/
theorem completionGateAudit_machine_status :
    completionGateAudit.machineStatus = RepoLocalMachineStatus.notRepoLocalClosed :=
  rfl

/-- The current non-completed state does not retain completed repo-local integration debt. -/
theorem completionGateAudit_no_completed_repo_local_integration_debt :
    completionGateAudit.completedStateRetainsRepoLocalIntegrationDebt = false :=
  rfl

/-- Public backfill text for the completion-gate child. -/
def completionGateBackfillProposal : List String := [
  "THM-M-0607.completion-gate: keep the item open. The checked Lean artifact `AwesomeTheorems.Stage1.S1_M_254.completionGateAudit` records `machineStatus = not_repo_local_closed`, `terminalTheoremOrPinnedWrapperPresent = false`, and `completionClaimed = false`.",
  "The local validation command is `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_254.lean`; a passing run validates the statement-shape, audit metadata, and wrapper declarations only, not a terminal smooth-structure existence theorem.",
  "Do not mark THM-M-0607 complete until either a local proof body, a local wrapper over pinned mathlib, or a pinned/imported/checked external upstream theorem supplies the terminal smoothability theorem and passes the same local Lean gate.",
  "Do not mark THM-M-0607 complete until the public blueprint, todo, and README status surfaces are merged consistently by a serial integrator patch.",
  "No completed state currently retains `repo_local_integration_debt`: no terminal external Lean 4 proof was found, no anchor-only proof is being counted as complete, and this child makes no completion claim."
]

/-- The statement-shape definition unfolds to the explicit smoothability package. -/
theorem statementShape_iff
    (E : Type uE) (H : Type uH) (M : Type uM)
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    (I : ModelWithCorners ℝ E H) :
    StatementShape E H M I ↔
      (∀ T : TopologicalManifoldPackage E H M I,
        SmoothabilityHypotheses T →
          Nonempty (SmoothStructurePackage E H M I T)) :=
  Iff.rfl

/-- A supplied smooth-structure package gives the requested statement output. -/
theorem statementShape_from_smoothing_constructor
    {E : Type uE} {H : Type uH} {M : Type uM}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    {I : ModelWithCorners ℝ E H}
    (h : ∀ T : TopologicalManifoldPackage E H M I,
      SmoothabilityHypotheses T →
        Nonempty (SmoothStructurePackage E H M I T)) :
    StatementShape E H M I :=
  h

/--
Checked mathlib wrapper: every smooth manifold package is a `C^0` manifold for
its chosen smooth atlas.
-/
theorem smoothPackage_to_c0
    {E : Type uE} {H : Type uH} {M : Type uM}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    {I : ModelWithCorners ℝ E H}
    {T : TopologicalManifoldPackage E H M I}
    (S : SmoothStructurePackage E H M I T) :
    letI : ChartedSpace H M := S.smoothChartedSpace
    IsManifold I 0 M := by
  letI : ChartedSpace H M := S.smoothChartedSpace
  letI : IsManifold I ∞ M := S.smooth
  infer_instance

/-- Checked mathlib wrapper: the identity map on a smooth manifold is smooth. -/
theorem smoothPackage_id_contMDiff
    {E : Type uE} {H : Type uH} {M : Type uM}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [TopologicalSpace H] [TopologicalSpace M]
    {I : ModelWithCorners ℝ E H}
    {T : TopologicalManifoldPackage E H M I}
    (S : SmoothStructurePackage E H M I T) :
    letI : ChartedSpace H M := S.smoothChartedSpace
    ContMDiff I I ∞ (fun x : M => x) := by
  letI : ChartedSpace H M := S.smoothChartedSpace
  letI : IsManifold I ∞ M := S.smooth
  exact contMDiff_id

/--
Checked low-risk special package: a normed real vector space has its standard
smooth self-charted structure.  This is only an API sanity check, not a
topological-manifold smoothing theorem.
-/
def euclideanSelfSmoothPackage
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (T : TopologicalManifoldPackage E E E 𝓘(ℝ, E))
    (compat :
      CompatibleWithTopologicalAtlas 𝓘(ℝ, E) T
        (inferInstance : ChartedSpace E E)) :
    SmoothStructurePackage E E E 𝓘(ℝ, E) T where
  smoothChartedSpace := inferInstance
  smooth := by infer_instance
  compatibleWithTopologicalAtlas := compat

/-- Standard topological-manifold package for a normed real vector space. -/
def euclideanSelfTopologicalPackage
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E] :
    TopologicalManifoldPackage E E E 𝓘(ℝ, E) where
  chartedSpace := inferInstance
  topological := by infer_instance
  separationHypotheses := True
  separation_holds := trivial
  countabilityHypotheses := True
  countability_holds := trivial

/-- The standard Euclidean self atlas satisfies the concrete compatibility relation. -/
theorem euclideanSelf_compatibleWithTopologicalAtlas
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E] :
    CompatibleWithTopologicalAtlas 𝓘(ℝ, E)
      (euclideanSelfTopologicalPackage E)
      (inferInstance : ChartedSpace E E) := by
  constructor
  · exact IsManifold.subset_maximalAtlas
  · exact IsManifold.maximalAtlas_subset_of_le (I := 𝓘(ℝ, E)) (M := E) (by simp)

/-- The standard self-charted normed vector space inhabits the output package. -/
theorem euclideanSelf_has_smooth_package
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E] :
    Nonempty (SmoothStructurePackage E E E 𝓘(ℝ, E)
      (euclideanSelfTopologicalPackage E)) :=
  ⟨euclideanSelfSmoothPackage E (euclideanSelfTopologicalPackage E)
    (euclideanSelf_compatibleWithTopologicalAtlas E)⟩

/-! ## Audit metadata -/

/-- Pinned mathlib revision audited for the THM-M-0607 mathlib-anchor pass. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- mathlib modules checked while locating smooth-structure anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Geometry.Manifold.ChartedSpace",
  "Mathlib.Geometry.Manifold.IsManifold.Basic",
  "Mathlib.Geometry.Manifold.ContMDiff.Basic",
  "Mathlib.Geometry.Manifold.PoincareConjecture",
  "Mathlib.Geometry.Manifold.SmoothApprox",
  "Mathlib.Geometry.Manifold.PartitionOfUnity",
  "Mathlib.Geometry.Manifold.WhitneyEmbedding",
  "Mathlib.AlgebraicTopology.SimplicialComplex.Basic",
  "Mathlib.Analysis.Convex.SimplicialComplex.Basic"
]

/-- Public-facing short module labels for the `THM-M-0607.mathlib-audit` child task. -/
def mathlibAuditShortModuleLabels : List String := [
  "ChartedSpace",
  "IsManifold.Basic",
  "ContMDiff.Basic",
  "PoincareConjecture",
  "SmoothApprox",
  "PartitionOfUnity",
  "WhitneyEmbedding",
  "AlgebraicTopology.SimplicialComplex.Basic",
  "Analysis.Convex.SimplicialComplex.Basic"
]

/--
Audit conclusion for the checked mathlib modules.

The pinned modules provide the manifold framework and adjacent smooth tools, but
not a terminal theorem asserting smoothability of arbitrary topological
manifolds.  In particular, the Poincare module records `proof_wanted` statement
surfaces, and the smooth approximation, partition of unity, and Whitney
embedding files are downstream smooth-manifold tools.
-/
def mathlibAuditConclusion : List String := [
  "The repo-local Lake closure pins mathlib at 8a178386ffc0f5fef0b77738bb5449d50efeea95.",
  "The checked modules provide ChartedSpace, IsManifold, ContMDiff, smooth approximation, partition-of-unity, Poincare statement, and Whitney embedding anchors.",
  "No checked module supplies a terminal smoothability theorem for arbitrary topological manifolds."
]

/-- Pinned names checked or used by this Stage1 artifact. -/
def mathlibAnchorNames : List String := [
  "ChartedSpace",
  "ModelWithCorners",
  "IsManifold",
  "IsManifold.maximalAtlas",
  "IsManifold.chart_mem_maximalAtlas",
  "IsManifold.compatible_of_mem_maximalAtlas",
  "ContMDiff",
  "contMDiff_id",
  "modelWithCornersSelf",
  "ContinuousMap.HomotopyEquiv.NonemptyDiffeomorphSphere",
  "Continuous.exists_contMDiff_approx",
  "exists_contMDiffMap_forall_mem_convex_of_local",
  "exists_embedding_euclidean_of_compact",
  "PreAbstractSimplicialComplex",
  "AbstractSimplicialComplex",
  "Geometry.SimplicialComplex"
]

/--
Search terms that did not locate a terminal smoothability theorem in the pinned
repo-local mathlib closure.
-/
def absentTerminalSearchTerms : List String := [
  "Smoothable",
  "smoothable",
  "smooth structure",
  "smoothing theorem",
  "Moise",
  "Kirby",
  "Siebenmann",
  "triangulation",
  "topological manifold smooth structure",
  "obstruction",
  "ordinary cohomology",
  "Stiefel-Whitney",
  "Pontryagin class",
  "characteristic class",
  "TOP/PL",
  "TOP/O",
  "surface classification",
  "one-dimensional topological manifold",
  "3-manifold triangulation",
  "PL smooth"
]

/-! ## Audit probes -/

#check ChartedSpace
#check ModelWithCorners
#check IsManifold
#check ContMDiff
#check contMDiff_id
#check IsManifold.chart_mem_maximalAtlas
#check IsManifold.compatible_of_mem_maximalAtlas
#check PreAbstractSimplicialComplex
#check AbstractSimplicialComplex
#check Geometry.SimplicialComplex
#check TopologicalManifoldPackage
#check LowDimensionalSmoothabilityHypotheses
#check LowDimensionalSmoothingBranch
#check LowDimensionalSmoothingDecomposition
#check lowDimensionalSmoothingAuditRows
#check HighDimensionalObstructionVanishingHypotheses
#check ObstructionBranchComponent
#check ObstructionBranchComponent.label
#check KirbySiebenmannObstructionTarget
#check KirbySiebenmannObstructionTarget.obstructionTheoryReady
#check KirbySiebenmannObstructionTarget.obstructionTheoryReady_holds
#check KirbySiebenmannObstructionTarget.remainingSmoothabilityReady
#check KirbySiebenmannObstructionTarget.remainingSmoothabilityReady_holds
#check KirbySiebenmannObstructionTarget.toHighDimensionalHypotheses
#check SmoothabilityRoute
#check SmoothabilityRoute.highDimensionalFromKirbySiebenmannTarget
#check SmoothabilityHypotheses
#check AtlasC0Compatibility
#check CompatibleWithTopologicalAtlas
#check AtlasC0Compatibility.input_subset_output_c0
#check AtlasC0Compatibility.output_smooth_subset_input_c0
#check SmoothStructurePackage
#check StatementShape
#check statementNormalizationNote
#check smoothabilityRoute_cases
#check lowDimensionalSmoothability_dimension_le_three
#check highDimensionalObstruction_dimension_at_least_five
#check statementScopeBackfillProposal
#check compatibilityBackfillProposal
#check obstructionBranchAuditRows
#check obstructionBranchAuditRows_length
#check obstructionBackfillProposal
#check ExternalSmoothabilityAuditRow
#check externalSmoothabilityAuditRows
#check externalSmoothabilityAuditRows_length
#check externalSmoothabilityBackfillProposal
#check RepoLocalMachineStatus
#check CompletionGateAudit
#check completionGateAudit
#check completionGateAudit_no_completion_claim
#check completionGateAudit_no_terminal_theorem_or_pinned_wrapper
#check completionGateAudit_public_surfaces_not_merged
#check completionGateAudit_machine_status
#check completionGateAudit_no_completed_repo_local_integration_debt
#check completionGateBackfillProposal
#check smoothPackage_to_c0
#check smoothPackage_id_contMDiff
#check euclideanSelfTopologicalPackage
#check euclideanSelf_compatibleWithTopologicalAtlas
#check euclideanSelf_has_smooth_package
#check pinnedMathlibRevision
#check mathlibAnchorModules
#check mathlibAuditShortModuleLabels
#check mathlibAuditConclusion
#check ContinuousMap.HomotopyEquiv.NonemptyDiffeomorphSphere
#check Continuous.exists_contMDiff_approx
#check exists_contMDiffMap_forall_mem_convex_of_local
#check exists_embedding_euclidean_of_compact

end S1_M_254
end Stage1
end AwesomeTheorems
