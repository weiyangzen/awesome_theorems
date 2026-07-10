import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.Topology.MetricSpace.Bounded

/-!
# S1-M-176 / THM-M-1238: Rellich-Kondrachov theorem

This Stage1 artifact records a conservative Lean 4 boundary for the
Rellich-Kondrachov compact embedding theorem.

The pinned repo-local mathlib snapshot
`8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies topology, bornology,
`L^p` objects, Fréchet derivatives, and first-order Sobolev inequalities.  It
does not expose a canonical Sobolev-space API or a terminal
Rellich-Kondrachov theorem in the local Lake closure.  A current external Lean 4 repository was found
(`abenenson/rellich-kondrachov`), but it is not pinned/imported here and cannot
be treated as repo-local completion from this worker scope.

The declarations below therefore avoid proof placeholders and false completion
claims: they normalize compact embedding as a bounded-set-to-relatively-compact
image property, package the future theorem statement, and provide small checked
wrappers around local mathlib compactness and Sobolev anchors.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal NNReal

universe u v w

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_176

variable {W : Type u} [NormedAddCommGroup W] [NormedSpace ℝ W]
variable {L : Type v} [NormedAddCommGroup L] [NormedSpace ℝ L]

/--
Compact embedding, stated in the bornological form used by analysis:
bounded source sets have relatively compact image in the target topology.

For a normed linear inclusion this is the usual compactness of the inclusion
operator, phrased without requiring a dedicated Sobolev-space API.
-/
def CompactEmbeddingByBoundedSets (incl : W →L[ℝ] L) : Prop :=
  ∀ s : Set W, Bornology.IsBounded s → IsCompact (closure (incl '' s))

/-- The compact-embedding boundary unfolds to the bounded-set compactness condition. -/
theorem compactEmbeddingByBoundedSets_iff (incl : W →L[ℝ] L) :
    CompactEmbeddingByBoundedSets incl ↔
      ∀ s : Set W, Bornology.IsBounded s → IsCompact (closure (incl '' s)) :=
  Iff.rfl

/-- A compact embedding gives compact closure of the image of any bounded source family. -/
theorem compact_closure_image_of_bounded {incl : W →L[ℝ] L}
    (h : CompactEmbeddingByBoundedSets incl) {s : Set W} (hs : Bornology.IsBounded s) :
    IsCompact (closure (incl '' s)) :=
  h s hs

/--
Statement-shape data for a Rellich-Kondrachov theorem.

`sourceSobolevModel`, `targetLpModel`, `domainRegularity`, and
`exponentHypotheses` are explicit propositions because the pinned repo-local
mathlib snapshot does not yet provide a canonical `W^{k,p}` object model with
weak derivatives and domain regularity.  A terminal theorem must replace those
fields by concrete APIs or import a checked upstream proof.
-/
structure RellichKondrachovData (W : Type u) (L : Type v)
    [NormedAddCommGroup W] [NormedSpace ℝ W]
    [NormedAddCommGroup L] [NormedSpace ℝ L] : Type (max u v) where
  inclusion : W →L[ℝ] L
  sourceSobolevModel : Prop
  targetLpModel : Prop
  domainRegularity : Prop
  exponentHypotheses : Prop
  compactEmbedding : CompactEmbeddingByBoundedSets inclusion

/--
Normalized Stage1 statement shape for Rellich-Kondrachov.

For explicit source and target normed spaces, there should be a continuous
linear inclusion satisfying the compact-embedding property once the Sobolev,
`L^p`, domain-regularity, and exponent hypotheses are instantiated.
-/
def StatementShape (W : Type u) (L : Type v)
    [NormedAddCommGroup W] [NormedSpace ℝ W]
    [NormedAddCommGroup L] [NormedSpace ℝ L] : Prop :=
  Nonempty (RellichKondrachovData W L)

/-- The statement-shape definition is exactly nonemptiness of the normalized data package. -/
theorem statementShape_iff_nonempty :
    StatementShape W L ↔ Nonempty (RellichKondrachovData W L) :=
  Iff.rfl

/-- A data package exposes the compactness of the normalized inclusion. -/
theorem compactEmbedding_of_data (d : RellichKondrachovData W L) :
    CompactEmbeddingByBoundedSets d.inclusion :=
  d.compactEmbedding

/-- Checked general topology anchor: continuous images of compact sets are compact. -/
theorem isCompact_image_of_continuous
    {X : Type u} {Y : Type v} [TopologicalSpace X] [TopologicalSpace Y]
    {s : Set X} {f : X → Y} (hs : IsCompact s) (hf : Continuous f) :
    IsCompact (f '' s) :=
  hs.image hf

variable {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
variable {F : Type w} [NormedAddCommGroup F] [NormedSpace ℝ F]

/--
Checked wrapper around mathlib's Gagliardo-Nirenberg-Sobolev estimate.

This is first-order Sobolev infrastructure, not the Rellich-Kondrachov compact
embedding theorem.
-/
theorem gns_firstDerivative_eLpNorm_bound
    [MeasurableSpace E] [BorelSpace E] [FiniteDimensional ℝ E]
    (μ : Measure E) [μ.IsAddHaarMeasure] [FiniteDimensional ℝ F]
    {u : E → F} {s : Set E} (hu : ContDiff ℝ 1 u)
    (h2u : Function.support u ⊆ s) {p : ℝ≥0}
    (hp : 1 ≤ p) (h2p : p < Module.finrank ℝ E)
    (hs : Bornology.IsBounded s) :
    eLpNorm u p μ ≤
      eLpNormLESNormFDerivOfLeConst F μ s p p * eLpNorm (fderiv ℝ u) p μ := by
  exact MeasureTheory.eLpNorm_le_eLpNorm_fderiv μ hu h2u hp h2p hs

/--
Checked wrapper around the equal-exponent Gagliardo-Nirenberg-Sobolev API.

The target exponent `p'` is related to `p` by the usual Sobolev conjugacy
formula.  This remains a first-derivative estimate rather than compactness.
-/
theorem gns_firstDerivative_conjugate_eLpNorm_bound
    [MeasurableSpace E] [BorelSpace E] [FiniteDimensional ℝ E]
    (μ : Measure E) [μ.IsAddHaarMeasure] [FiniteDimensional ℝ F]
    {u : E → F} (hu : ContDiff ℝ 1 u) (h2u : HasCompactSupport u)
    {p p' : ℝ≥0} (hp : 1 ≤ p) (hn : 0 < Module.finrank ℝ E)
    (hp' : (p' : ℝ)⁻¹ = (p : ℝ)⁻¹ - (Module.finrank ℝ E : ℝ)⁻¹) :
    eLpNorm u p' μ ≤
      SNormLESNormFDerivOfEqConst F μ p * eLpNorm (fderiv ℝ u) p μ := by
  exact MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq μ hu h2u hp hn hp'

/-- Mathlib revision pinned by the repo-local Lake configuration for this audit. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Exact local modules requested by `THM-M-1238.mathlib-audit`. -/
def mathlibAuditAvailableLocalModules : List String := [
  "Topology.Compactness.Compact",
  "Topology.MetricSpace.Bounded",
  "Topology.Bornology.Basic",
  "MeasureTheory.Function.LpSpace.Basic",
  "Analysis.FunctionalSpaces.SobolevInequality"
]

/-- Repo-local mathlib modules checked while locating anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Topology.Compactness.Compact",
  "Mathlib.Topology.MetricSpace.Bounded",
  "Mathlib.Topology.Bornology.Basic",
  "Mathlib.MeasureTheory.Function.LpSpace.Basic",
  "Mathlib.MeasureTheory.Function.LpSeminorm.Basic",
  "Mathlib.Analysis.Calculus.FDeriv.Basic",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "Mathlib.Analysis.Distribution.Distribution",
  "Mathlib.Analysis.Distribution.DerivNotation"
]

/-- Pinned theorem and definition names audited for the repo-local Stage1 boundary. -/
def mathlibAnchorNames : List String := [
  "IsCompact",
  "IsCompact.image",
  "Bornology.IsBounded",
  "Bornology.IsBounded.isCompact_closure",
  "TotallyBounded",
  "MeasureTheory.Lp",
  "MeasureTheory.MemLp",
  "MeasureTheory.eLpNorm",
  "fderiv",
  "ContDiff",
  "MeasureTheory.eLpNorm_le_eLpNorm_fderiv",
  "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq"
]

/-- Local search terms that did not locate a terminal mathlib Rellich-Kondrachov theorem. -/
def absentTerminalMathlibSearchTerms : List String := [
  "Rellich",
  "Kondrachov",
  "RellichKondrachov",
  "CompactEmbedding",
  "compact embedding",
  "Sobolev space",
  "WeakDerivative",
  "weak derivative"
]

/-- Primary external Lean 4 source found during the Stage1 audit. -/
def externalLean4AnchorRepository : String :=
  "https://github.com/abenenson/rellich-kondrachov"

/-- External repository revision observed by `git ls-remote` on 2026-04-30. -/
def externalLean4AnchorRevision : String :=
  "85f2c2e943404e5ba92911346874d8961e137b60"

/-- Main theorem name advertised by the external primary source. -/
def externalLean4AdvertisedMainTheorem : String :=
  "RellichKondrachov.Geometry.Manifold.Sobolev.RiemannianFiniteChartData.isCompactOperator_h1ToL2_riemannianVolume"

/-- External module containing the advertised main theorem at the audited revision. -/
def externalLean4AdvertisedMainModule : String :=
  "RellichKondrachov.Geometry.Manifold.Sobolev.RellichKondrachovRiemannian.Global"

/-- External source file containing the advertised main theorem at the audited revision. -/
def externalLean4AdvertisedMainSourceFile : String :=
  "RellichKondrachov/Geometry/Manifold/Sobolev/RellichKondrachovRiemannian/Global.lean"

/-- Toolchain declared by the external source at the audited revision. -/
def externalLean4AnchorToolchain : String :=
  "leanprover/lean4:v4.29.0-rc7"

/-- Mathlib dependency tag declared by the external source at the audited revision. -/
def externalLean4AnchorMathlibRequirement : String :=
  "v4.29.0-rc7"

/-- Repo-local Lean toolchain declared by `Formalizations/Lean/lean-toolchain`. -/
def repoLocalLeanToolchain : String :=
  "leanprover/lean4:v4.29.0"

/-- Repo-local mathlib revision declared by `Formalizations/Lean/lake-manifest.json`. -/
def repoLocalMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Mathlib revision resolved by the external source's `lake-manifest.json`. -/
def externalLean4AnchorMathlibRevision : String :=
  "c5edb8d3738a5abd7da7f34d5bcb27f632a1ecca"

/-- Exact repo-local blockers found before a direct import/check can be claimed. -/
def externalLean4IntegrationBlockers : List String := [
  "Repo-local Lean toolchain is leanprover/lean4:v4.29.0, but the external project declares leanprover/lean4:v4.29.0-rc7.",
  "Repo-local mathlib is pinned to 8a178386ffc0f5fef0b77738bb5449d50efeea95, but the external project resolves mathlib v4.29.0-rc7 to c5edb8d3738a5abd7da7f34d5bcb27f632a1ecca.",
  "This worker does not own Lake dependency or import-aggregator edits, so it cannot add the external project to the repo-local dependency closure."
]

/-- M0387 machine-status classification for the external source from this repo's viewpoint. -/
def externalLean4AnchorStatus : String :=
  "external_upstream_anchor_only"

/-- M0387 debt classification that blocks any local completion claim for this slot. -/
def externalLean4AnchorDebtClass : String :=
  "repo_local_integration_debt"

/--
Why this file does not close the theorem: the external proof is not currently
inside this repository's Lake dependency closure.
-/
def repoLocalIntegrationBlocker : String :=
  "External Lean 4 proof source found, but direct repo-local closure is blocked by Lean toolchain and mathlib revision mismatch plus lack of worker-owned Lake dependency scope; pin/import/check or a compatibility branch is required before any completion claim."

end S1_M_176
end Stage1
end AwesomeTheorems
