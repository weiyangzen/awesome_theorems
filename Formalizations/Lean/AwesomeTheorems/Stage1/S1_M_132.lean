import Mathlib.Topology.MetricSpace.GromovHausdorff
import Mathlib.Geometry.Manifold.SmoothEmbedding
import Mathlib.Geometry.Manifold.WhitneyEmbedding
import Mathlib.Geometry.Manifold.Riemannian.Basic
import Mathlib.Geometry.Manifold.Riemannian.PathELength

/-!
# S1-M-132 / THM-M-0171: Gromov embedding theorem

This Stage1 file records a conservative Lean boundary for a Gromov/Kuratowski
metric embedding statement.

The pinned mathlib snapshot has a genuine theorem that every separable metric
space admits an isometric embedding into `ℓ^∞(ℕ, ℝ)`, and the Gromov-Hausdorff
space for nonempty compact metric spaces is built using this embedding
technology.  The source slot describes the theorem as a necessary-and-sufficient
condition for metric-space embedding, so the declarations below separate:

* the checkable distance-preserving iff criterion for a candidate map;
* the checked mathlib Kuratowski embedding theorem for separable metric spaces;
* the checked compact Gromov-Hausdorff wrappers available in mathlib.

No declaration here claims a terminal proof of every classical theorem that may
be called "Gromov embedding theorem".
-/

noncomputable section

open Set Metric
open scoped ENNReal

universe u v w

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_132

/-- The mathlib target space `ℓ^∞(ℕ, ℝ)` used by the Kuratowski embedding. -/
abbrev LinftyNatReal : Type :=
  lp (fun _ : ℕ => ℝ) ⊤

/--
A pointwise distance-preservation condition for a candidate embedding map.

This is the elementary necessary-and-sufficient condition for a map to be an
isometry in mathlib's metric-space API.
-/
def DistancePreservingMap
    (X : Type u) (E : Type v) [PseudoMetricSpace X] [PseudoMetricSpace E]
    (f : X → E) : Prop :=
  ∀ x y : X, dist (f x) (f y) = dist x y

/-- Existence of an isometric embedding from `X` into `E`. -/
def IsometricallyEmbedsIn
    (X : Type u) (E : Type v) [PseudoMetricSpace X] [PseudoMetricSpace E] :
    Prop :=
  ∃ f : X → E, Isometry f

/--
Candidate theorem families that the public title "Gromov embedding theorem" could
mean.  The current Stage1 child disambiguation selects only the metric
Kuratowski/`ℓ^∞` branch as repo-local Lean work; the other constructors remain
explicit non-selected variants for later source-level audit.
-/
inductive GromovEmbeddingVariant where
  | kuratowskiLinfty
  | schoenbergNegativeTypeHilbert
  | compactGromovHausdorffRealization
  | nashKuiperHPrinciple
  | riemannianIsometricEmbedding

/-- S1-M-132-C001 statement-disambiguation decision for the current Lean artifact. -/
def selectedVariantForStatementDisambiguation : GromovEmbeddingVariant :=
  GromovEmbeddingVariant.kuratowskiLinfty

/-- The child disambiguation does not select a differential-geometric variant. -/
def nonSelectedStatementVariants : List GromovEmbeddingVariant := [
  GromovEmbeddingVariant.schoenbergNegativeTypeHilbert,
  GromovEmbeddingVariant.compactGromovHausdorffRealization,
  GromovEmbeddingVariant.nashKuiperHPrinciple,
  GromovEmbeddingVariant.riemannianIsometricEmbedding
]

/-- Checked certificate for the selected Stage1 statement-disambiguation branch. -/
theorem selectedVariantForStatementDisambiguation_eq :
    selectedVariantForStatementDisambiguation = GromovEmbeddingVariant.kuratowskiLinfty :=
  rfl

/-- Repo-local metadata for a pinned upstream theorem anchor. -/
structure MathlibAnchor where
  revision : String
  moduleName : String
  theoremName : String
  target : String
  status : String

/-- Repo-local audit record for differential-geometric adjacent APIs. -/
structure DifferentialGeometryVariantAudit where
  revision : String
  moduleName : String
  checkedNames : List String
  boundary : String
  status : String

/-- Repo-local metadata for the C005 external Lean 4 source audit. -/
structure ExternalLeanAuditRecord where
  searchTerm : String
  source : String
  repoUrl : String
  commit : String
  theoremNames : List String
  toolchain : String
  placeholderStatus : String
  lakeDependencyFeasibility : String
  status : String

/--
S1-M-132-C002 Kuratowski anchor.

The proof-bearing declaration is `exists_isometric_embedding_linfty` below,
which directly checks `KuratowskiEmbedding.exists_isometric_embedding` in the
local Lake closure pinned to this mathlib revision.
-/
def kuratowskiEmbeddingAnchor : MathlibAnchor where
  revision := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
  moduleName := "Mathlib.Topology.MetricSpace.Kuratowski"
  theoremName := "KuratowskiEmbedding.exists_isometric_embedding"
  target := "separable metric-space embedding into lp (fun _ : Nat => Real) top"
  status := "local_wrapper_upstream_mathlib"

/-- Checked certificate for the pinned mathlib revision recorded by the Kuratowski anchor. -/
theorem kuratowskiEmbeddingAnchor_revision_eq :
    kuratowskiEmbeddingAnchor.revision = "8a178386ffc0f5fef0b77738bb5449d50efeea95" :=
  rfl

/-- Checked certificate for the upstream theorem name recorded by the Kuratowski anchor. -/
theorem kuratowskiEmbeddingAnchor_theoremName_eq :
    kuratowskiEmbeddingAnchor.theoremName = "KuratowskiEmbedding.exists_isometric_embedding" :=
  rfl

/-- Checked certificate that the Kuratowski branch is repo-local through a mathlib wrapper. -/
theorem kuratowskiEmbeddingAnchor_status_eq :
    kuratowskiEmbeddingAnchor.status = "local_wrapper_upstream_mathlib" :=
  rfl

/--
S1-M-132-C003 compact Gromov-Hausdorff anchor.

This is an adjacent compact-GH wrapper, not a terminal broad Gromov embedding
theorem.
-/
def compactGHToGHSpaceEqAnchor : MathlibAnchor where
  revision := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
  moduleName := "Mathlib.Topology.MetricSpace.GromovHausdorff"
  theoremName := "GromovHausdorff.toGHSpace_eq_toGHSpace_iff_isometryEquiv"
  target := "nonempty compact metric spaces: GH quotient equality iff isometry equivalence"
  status := "local_wrapper_upstream_mathlib"

/--
S1-M-132-C003 compact Gromov-Hausdorff anchor.

This records the upstream bound from an isometric coupling's Hausdorff distance.
-/
def compactGHGHDistLeHausdorffDistAnchor : MathlibAnchor where
  revision := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
  moduleName := "Mathlib.Topology.MetricSpace.GromovHausdorff"
  theoremName := "GromovHausdorff.ghDist_le_hausdorffDist"
  target := "GH distance bounded by Hausdorff distance in any isometric coupling"
  status := "local_wrapper_upstream_mathlib"

/--
S1-M-132-C003 compact Gromov-Hausdorff anchor.

This records the upstream optimal coupling theorem realizing the GH distance.
-/
def compactGHHausdorffDistOptimalAnchor : MathlibAnchor where
  revision := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
  moduleName := "Mathlib.Topology.MetricSpace.GromovHausdorff"
  theoremName := "GromovHausdorff.hausdorffDist_optimal"
  target := "optimal compact coupling realizes the Gromov-Hausdorff distance"
  status := "local_wrapper_upstream_mathlib"

/-- Checked certificate for the theorem names recorded by the compact GH anchors. -/
theorem compactGHAnchor_theoremNames_eq :
    [compactGHToGHSpaceEqAnchor.theoremName,
      compactGHGHDistLeHausdorffDistAnchor.theoremName,
      compactGHHausdorffDistOptimalAnchor.theoremName] =
    ["GromovHausdorff.toGHSpace_eq_toGHSpace_iff_isometryEquiv",
      "GromovHausdorff.ghDist_le_hausdorffDist",
      "GromovHausdorff.hausdorffDist_optimal"] :=
  rfl

/-- Checked certificate that all compact GH anchors are local mathlib wrappers. -/
theorem compactGHAnchor_statuses_eq :
    [compactGHToGHSpaceEqAnchor.status,
      compactGHGHDistLeHausdorffDistAnchor.status,
      compactGHHausdorffDistOptimalAnchor.status] =
    ["local_wrapper_upstream_mathlib",
      "local_wrapper_upstream_mathlib",
      "local_wrapper_upstream_mathlib"] :=
  rfl

/-- Checked certificate for the pinned revision recorded by the compact GH anchors. -/
theorem compactGHAnchor_revisions_eq :
    [compactGHToGHSpaceEqAnchor.revision,
      compactGHGHDistLeHausdorffDistAnchor.revision,
      compactGHHausdorffDistOptimalAnchor.revision] =
    ["8a178386ffc0f5fef0b77738bb5449d50efeea95",
      "8a178386ffc0f5fef0b77738bb5449d50efeea95",
      "8a178386ffc0f5fef0b77738bb5449d50efeea95"] :=
  rfl

/--
S1-M-132-C004 differential-geometric variant audit for
`Mathlib.Geometry.Manifold.SmoothEmbedding`.

This module defines smooth embeddings as smooth immersions plus topological
embeddings.  It is adjacent to a Riemannian embedding reading, but it does not
state a pullback-metric isometry or an h-principle theorem.
-/
def smoothEmbeddingVariantAudit : DifferentialGeometryVariantAudit where
  revision := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
  moduleName := "Mathlib.Geometry.Manifold.SmoothEmbedding"
  checkedNames := [
    "Manifold.IsSmoothEmbedding",
    "Manifold.IsSmoothEmbedding.id",
    "Manifold.IsSmoothEmbedding.of_opens"
  ]
  boundary := "smooth embedding = smooth immersion plus topological embedding; no pullback-metric isometry or h-principle theorem"
  status := "audited_not_terminal_gromov_embedding"

/--
S1-M-132-C004 differential-geometric variant audit for
`Mathlib.Geometry.Manifold.WhitneyEmbedding`.

The available theorem is Whitney-style smooth Euclidean embedding for compact
manifolds, with injective derivative data.  This is not a Riemannian isometric
embedding theorem and does not encode Nash-Kuiper/Gromov h-principle closure.
-/
def whitneyEmbeddingVariantAudit : DifferentialGeometryVariantAudit where
  revision := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
  moduleName := "Mathlib.Geometry.Manifold.WhitneyEmbedding"
  checkedNames := [
    "SmoothBumpCovering.exists_immersion_euclidean",
    "exists_embedding_euclidean_of_compact"
  ]
  boundary := "compact smooth manifolds have smooth Euclidean embeddings; no metric pullback equality or h-principle theorem"
  status := "audited_not_terminal_gromov_embedding"

/--
S1-M-132-C004 differential-geometric variant audit for
`Mathlib.Geometry.Manifold.Riemannian.Basic`.

The module supplies Riemannian distance infrastructure from path lengths and
Riemannian metrics, but not an embedding existence theorem into a target whose
metric pulls back to the source metric.
-/
def riemannianBasicVariantAudit : DifferentialGeometryVariantAudit where
  revision := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
  moduleName := "Mathlib.Geometry.Manifold.Riemannian.Basic"
  checkedNames := [
    "Manifold.IsRiemannianManifold",
    "Manifold.riemannianMetricVectorSpace",
    "Manifold.PseudoEMetricSpace.ofRiemannianMetric",
    "Manifold.EMetricSpace.ofRiemannianMetric"
  ]
  boundary := "Riemannian metrics and induced extended distances; no Riemannian embedding existence theorem"
  status := "audited_not_terminal_gromov_embedding"

/--
S1-M-132-C004 differential-geometric variant audit for
`Mathlib.Geometry.Manifold.Riemannian.PathELength`.

The module gives path length and Riemannian extended-distance API.  It is a
metric substrate, not a pullback-metric embedding or h-principle statement.
-/
def riemannianPathELengthVariantAudit : DifferentialGeometryVariantAudit where
  revision := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
  moduleName := "Mathlib.Geometry.Manifold.Riemannian.PathELength"
  checkedNames := [
    "Manifold.pathELength",
    "Manifold.riemannianEDist",
    "Manifold.riemannianEDist_le_pathELength",
    "Manifold.riemannianEDist_triangle"
  ]
  boundary := "path length and Riemannian extended-distance calculus; no embedding existence theorem"
  status := "audited_not_terminal_gromov_embedding"

/-- The differential-geometric audit records all four modules requested by S1-M-132-C004. -/
theorem differentialGeometryVariantAudit_moduleNames_eq :
    [smoothEmbeddingVariantAudit.moduleName,
      whitneyEmbeddingVariantAudit.moduleName,
      riemannianBasicVariantAudit.moduleName,
      riemannianPathELengthVariantAudit.moduleName] =
    ["Mathlib.Geometry.Manifold.SmoothEmbedding",
      "Mathlib.Geometry.Manifold.WhitneyEmbedding",
      "Mathlib.Geometry.Manifold.Riemannian.Basic",
      "Mathlib.Geometry.Manifold.Riemannian.PathELength"] :=
  rfl

/--
The audited differential-geometric APIs are explicitly non-terminal for this
public title until a precise pullback-metric or h-principle statement is chosen
and separately formalized.
-/
theorem differentialGeometryVariantAudit_statuses_eq :
    [smoothEmbeddingVariantAudit.status,
      whitneyEmbeddingVariantAudit.status,
      riemannianBasicVariantAudit.status,
      riemannianPathELengthVariantAudit.status] =
    ["audited_not_terminal_gromov_embedding",
      "audited_not_terminal_gromov_embedding",
      "audited_not_terminal_gromov_embedding",
      "audited_not_terminal_gromov_embedding"] :=
  rfl

/-- Checked certificate for the pinned revision recorded by all differential-geometry audits. -/
theorem differentialGeometryVariantAudit_revisions_eq :
    [smoothEmbeddingVariantAudit.revision,
      whitneyEmbeddingVariantAudit.revision,
      riemannianBasicVariantAudit.revision,
      riemannianPathELengthVariantAudit.revision] =
    ["8a178386ffc0f5fef0b77738bb5449d50efeea95",
      "8a178386ffc0f5fef0b77738bb5449d50efeea95",
      "8a178386ffc0f5fef0b77738bb5449d50efeea95",
      "8a178386ffc0f5fef0b77738bb5449d50efeea95"] :=
  rfl

/--
The distance-preserving criterion is equivalent to existence of an isometry.

This is a low-risk checked wrapper around `Isometry.of_dist_eq` and
`Isometry.dist_eq`, not a global Gromov theorem.
-/
theorem isometricallyEmbedsIn_iff_exists_distancePreserving
    (X : Type u) (E : Type v) [PseudoMetricSpace X] [PseudoMetricSpace E] :
    IsometricallyEmbedsIn X E ↔ ∃ f : X → E, DistancePreservingMap X E f := by
  constructor
  · rintro ⟨f, hf⟩
    exact ⟨f, hf.dist_eq⟩
  · rintro ⟨f, hf⟩
    exact ⟨f, Isometry.of_dist_eq hf⟩

/--
Data package for the checked separable metric-space embedding substrate.

The target is fixed to mathlib's `ℓ^∞(ℕ, ℝ)` target for the Kuratowski embedding.
-/
structure LinftyEmbeddingData (X : Type u) [MetricSpace X] where
  map : X → LinftyNatReal
  isometry_map : Isometry map

/--
Stage1 statement-shape candidate.

For a metric space `X`, separability is sufficient for the checked
Kuratowski/Gromov-style isometric embedding into `ℓ^∞(ℕ, ℝ)`.
-/
def StatementShape (X : Type u) [MetricSpace X] : Prop :=
  TopologicalSpace.SeparableSpace X → Nonempty (LinftyEmbeddingData X)

/-- The Kuratowski embedding as a normalized data package. -/
def kuratowskiEmbeddingData (X : Type u) [MetricSpace X] [TopologicalSpace.SeparableSpace X] :
    LinftyEmbeddingData X where
  map := kuratowskiEmbedding X
  isometry_map := kuratowskiEmbedding.isometry X

/-- mathlib proves that every separable metric space embeds isometrically into `ℓ^∞(ℕ, ℝ)`. -/
theorem statementShape_of_separable
    (X : Type u) [MetricSpace X] [TopologicalSpace.SeparableSpace X] :
    StatementShape X := by
  intro _hsep
  exact ⟨kuratowskiEmbeddingData X⟩

/-- Direct wrapper around `KuratowskiEmbedding.exists_isometric_embedding`. -/
theorem exists_isometric_embedding_linfty
    (X : Type u) [MetricSpace X] [TopologicalSpace.SeparableSpace X] :
    IsometricallyEmbedsIn X LinftyNatReal := by
  exact KuratowskiEmbedding.exists_isometric_embedding X

/-- The canonical Kuratowski embedding is an isometry. -/
theorem kuratowskiEmbedding_isometry
    (X : Type u) [MetricSpace X] [TopologicalSpace.SeparableSpace X] :
    Isometry (kuratowskiEmbedding X) :=
  kuratowskiEmbedding.isometry X

/-- A checked topological consequence: an isometry is a topological embedding. -/
theorem kuratowskiEmbedding_isEmbedding
    (X : Type u) [MetricSpace X] [TopologicalSpace.SeparableSpace X] :
    Topology.IsEmbedding (kuratowskiEmbedding X) :=
  (kuratowskiEmbedding.isometry X).isEmbedding

/--
For nonempty compact metric spaces, equality in the Gromov-Hausdorff quotient is
equivalent to isometry equivalence.
-/
theorem toGHSpace_eq_toGHSpace_iff_isometryEquiv
    {X : Type u} [MetricSpace X] [CompactSpace X] [Nonempty X]
    {Y : Type v} [MetricSpace Y] [CompactSpace Y] [Nonempty Y] :
    GromovHausdorff.toGHSpace X = GromovHausdorff.toGHSpace Y ↔ Nonempty (X ≃ᵢ Y) :=
  GromovHausdorff.toGHSpace_eq_toGHSpace_iff_isometryEquiv

/-- The Gromov-Hausdorff distance is bounded by any isometric coupling's Hausdorff distance. -/
theorem ghDist_le_hausdorffDist_of_isometric_coupling
    {X : Type u} [MetricSpace X] [CompactSpace X] [Nonempty X]
    {Y : Type v} [MetricSpace Y] [CompactSpace Y] [Nonempty Y]
    {Z : Type w} [MetricSpace Z] {Φ : X → Z} {Ψ : Y → Z}
    (hΦ : Isometry Φ) (hΨ : Isometry Ψ) :
    GromovHausdorff.ghDist X Y ≤ hausdorffDist (range Φ) (range Ψ) :=
  GromovHausdorff.ghDist_le_hausdorffDist hΦ hΨ

/-- mathlib's optimal compact coupling realizes the Gromov-Hausdorff distance. -/
theorem hausdorffDist_optimal_eq_ghDist
    {X : Type u} [MetricSpace X] [CompactSpace X] [Nonempty X]
    {Y : Type v} [MetricSpace Y] [CompactSpace Y] [Nonempty Y] :
    hausdorffDist (range (GromovHausdorff.optimalGHInjl X Y))
        (range (GromovHausdorff.optimalGHInjr X Y)) =
      GromovHausdorff.ghDist X Y :=
  GromovHausdorff.hausdorffDist_optimal

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Topology.MetricSpace.Kuratowski",
  "Mathlib.Topology.MetricSpace.GromovHausdorffRealized",
  "Mathlib.Topology.MetricSpace.GromovHausdorff",
  "Mathlib.Topology.MetricSpace.Isometry",
  "Mathlib.Geometry.Manifold.SmoothEmbedding",
  "Mathlib.Geometry.Manifold.WhitneyEmbedding",
  "Mathlib.Geometry.Manifold.Riemannian.Basic",
  "Mathlib.Geometry.Manifold.Riemannian.PathELength"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "KuratowskiEmbedding.exists_isometric_embedding",
  "kuratowskiEmbedding",
  "kuratowskiEmbedding.isometry",
  "Isometry.of_dist_eq",
  "Isometry.dist_eq",
  "Isometry.isEmbedding",
  "GromovHausdorff.toGHSpace_eq_toGHSpace_iff_isometryEquiv",
  "GromovHausdorff.ghDist_le_hausdorffDist",
  "GromovHausdorff.hausdorffDist_optimal",
  "Manifold.IsSmoothEmbedding",
  "SmoothBumpCovering.exists_immersion_euclidean",
  "exists_embedding_euclidean_of_compact",
  "Manifold.IsRiemannianManifold",
  "Manifold.riemannianMetricVectorSpace",
  "Manifold.PseudoEMetricSpace.ofRiemannianMetric",
  "Manifold.EMetricSpace.ofRiemannianMetric",
  "Manifold.pathELength",
  "Manifold.riemannianEDist",
  "Manifold.riemannianEDist_le_pathELength",
  "Manifold.riemannianEDist_triangle"
]

/-- Search terms that did not locate a broader terminal Gromov embedding theorem in local mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Gromov embedding theorem",
  "GromovEmbedding",
  "gromov embedding",
  "Schoenberg",
  "negative type",
  "conditionally negative definite",
  "Nash-Kuiper",
  "Gromov h-principle",
  "isometric immersion h-principle",
  "pullback metric embedding theorem"
]

/-- C005 requested external-audit search terms. -/
def externalAuditSearchTerms : List String := [
  "GromovEmbedding",
  "Gromov embedding",
  "KuratowskiEmbedding",
  "exists_isometric_embedding",
  "Schoenberg",
  "negative type",
  "conditionally negative",
  "NashKuiper",
  "Nash-Kuiper",
  "h-principle",
  "isometric immersion"
]

/-- Authentication status for the C005 GitHub primary-source code search attempt. -/
def externalAuditGithubAuthStatus : String :=
  "blocked: gh auth status reports no logged-in GitHub host and no GH_TOKEN/GITHUB_TOKEN env var was present"

/--
C005 positive and negative external Lean 4 audit records.

The only selected-branch positive result is already in the repo-local Lake
closure through pinned mathlib.  The sphere-eversion project is an external
Lean 4 h-principle/Gromov-flexibility anchor, but it is not imported here and is
not a terminal Gromov metric embedding theorem for the selected branch.
-/
def externalLeanAuditRecords : List ExternalLeanAuditRecord := [
  {
    searchTerm := "KuratowskiEmbedding"
    source := "repo-local pinned mathlib primary source"
    repoUrl := "https://github.com/leanprover-community/mathlib4"
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
    theoremNames := [
      "KuratowskiEmbedding.exists_isometric_embedding",
      "kuratowskiEmbedding",
      "kuratowskiEmbedding.isometry"
    ]
    toolchain := "leanprover/lean4:v4.29.0"
    placeholderStatus := "repo-local Stage1 wrapper has no forbidden proof placeholders; mathlib theorem is in pinned Lake closure"
    lakeDependencyFeasibility := "already feasible: mathlib is pinned in this repo's lakefile and checked by exists_isometric_embedding_linfty"
    status := "local_wrapper_upstream_mathlib"
  },
  {
    searchTerm := "exists_isometric_embedding"
    source := "repo-local pinned mathlib primary source"
    repoUrl := "https://github.com/leanprover-community/mathlib4"
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
    theoremNames := ["KuratowskiEmbedding.exists_isometric_embedding"]
    toolchain := "leanprover/lean4:v4.29.0"
    placeholderStatus := "repo-local Stage1 wrapper has no forbidden proof placeholders; mathlib theorem is in pinned Lake closure"
    lakeDependencyFeasibility := "already feasible: mathlib is pinned in this repo's lakefile and checked by exists_isometric_embedding_linfty"
    status := "local_wrapper_upstream_mathlib"
  },
  {
    searchTerm := "h-principle"
    source := "external Lean 4 primary source: sphere-eversion"
    repoUrl := "https://github.com/leanprover-community/sphere-eversion"
    commit := "5b63797f94521b1d61586060455754d9740b109e"
    theoremNames := [
      "RelMfld.Ample.satisfiesHPrinciple",
      "RelMfld.Ample.satisfiesHPrincipleWith",
      "RelMfld.Ample.satisfiesHPrincipleWith'",
      "immersionRel_satisfiesHPrincipleWith",
      "Gromov",
      "Smale",
      "sphere_eversion"
    ]
    toolchain := "leanprover/lean4:v4.28.0"
    placeholderStatus := "Global/Local/Main h-principle files scanned clean for forbidden proof placeholders; project-level scan found placeholder proof terms in ToMathlib support files"
    lakeDependencyFeasibility := "blocked for current repo-local completion: external project uses Lean v4.28.0 and mathlib 8f9d9cff..., while this repo uses Lean v4.29.0 and mathlib 8a178386...; also not pinned/imported here"
    status := "external_adjacent_hprinciple_anchor_only_with_integration_blocker"
  },
  {
    searchTerm := "isometric immersion"
    source := "repo-local pinned mathlib primary source"
    repoUrl := "https://github.com/leanprover-community/mathlib4"
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
    theoremNames := ["controlled_closure_range_of_complete"]
    toolchain := "leanprover/lean4:v4.29.0"
    placeholderStatus := "phrase occurs in explanatory text for a normed-group theorem, not as a terminal isometric-immersion embedding theorem"
    lakeDependencyFeasibility := "already in pinned mathlib, but mathematically irrelevant to THM-M-0171 completion"
    status := "negative_for_terminal_gromov_embedding"
  },
  {
    searchTerm := "GromovEmbedding / Gromov embedding / Schoenberg / negative type / conditionally negative / NashKuiper / Nash-Kuiper"
    source := "repo-local pinned mathlib plus shallow external sphere-eversion source audit"
    repoUrl := "https://github.com/leanprover-community/mathlib4 ; https://github.com/leanprover-community/sphere-eversion"
    commit := "mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95 ; sphere-eversion 5b63797f94521b1d61586060455754d9740b109e"
    theoremNames := []
    toolchain := "mathlib Lean v4.29.0 ; sphere-eversion Lean v4.28.0"
    placeholderStatus := "no terminal Lean 4 theorem located for these exact names/phrases in the audited primary sources"
    lakeDependencyFeasibility := "not applicable unless a later authenticated global GitHub code search locates a concrete proof-bearing project"
    status := "not_found_in_audited_primary_sources_auth_global_search_blocked"
  }
]

/-- Checked certificate for the C005 GitHub authentication blocker. -/
theorem externalAuditGithubAuthStatus_eq :
    externalAuditGithubAuthStatus =
      "blocked: gh auth status reports no logged-in GitHub host and no GH_TOKEN/GITHUB_TOKEN env var was present" :=
  rfl

/-- Checked certificate for the C005 search-term list. -/
theorem externalAuditSearchTerms_eq :
    externalAuditSearchTerms =
      ["GromovEmbedding",
        "Gromov embedding",
        "KuratowskiEmbedding",
        "exists_isometric_embedding",
        "Schoenberg",
        "negative type",
        "conditionally negative",
        "NashKuiper",
        "Nash-Kuiper",
        "h-principle",
        "isometric immersion"] :=
  rfl

/-- Checked certificate for the status summary of C005 external audit records. -/
theorem externalLeanAuditRecord_statuses_eq :
    externalLeanAuditRecords.map (fun r => r.status) =
      ["local_wrapper_upstream_mathlib",
        "local_wrapper_upstream_mathlib",
        "external_adjacent_hprinciple_anchor_only_with_integration_blocker",
        "negative_for_terminal_gromov_embedding",
        "not_found_in_audited_primary_sources_auth_global_search_blocked"] :=
  rfl

/-- Repo-local integration-gate decision record for C006. -/
structure IntegrationGateRecord where
  branch : String
  evidence : String
  gateResult : String
  blocker : String

/--
S1-M-132-C006 integration gate.

The selected metric branch is already in the local Lake closure through pinned
mathlib.  The external `sphere-eversion` h-principle project is recorded only
as adjacent evidence with a concrete integration blocker, not as completed
anchor-only evidence for this theorem.
-/
def integrationGateRecords : List IntegrationGateRecord := [
  {
    branch := "selected Kuratowski/Linfty metric branch"
    evidence := "KuratowskiEmbedding.exists_isometric_embedding checked by exists_isometric_embedding_linfty"
    gateResult := "repo_local_closed_by_local_wrapper_upstream_mathlib"
    blocker := "none"
  },
  {
    branch := "external sphere-eversion h-principle adjacent branch"
    evidence := "RelMfld.Ample.satisfiesHPrincipleWith, Gromov, and sphere_eversion at commit 5b63797f94521b1d61586060455754d9740b109e"
    gateResult := "not_completed_external_anchor_only_with_concrete_blocker"
    blocker := "not a terminal metric Gromov embedding theorem; not selected for this Stage1 statement; Lean v4.28.0/mathlib 8f9d9cff mismatch; ToMathlib support files contain placeholder proof terms"
  },
  {
    branch := "authenticated global external search"
    evidence := externalAuditGithubAuthStatus
    gateResult := "not_completed_authentication_blocker"
    blocker := "rerun requested GitHub code-search terms under gh auth or GH_TOKEN before public external-audit completion"
  }
]

/-- C006 repo-local integration-debt gate result. -/
def integrationGateRepoLocalDebtResult : String :=
  "pass: no completed state retains repo_local_integration_debt; adjacent external anchor has a concrete blocker and is not a completion claim"

/-- Checked certificate for the C006 integration-gate branches. -/
theorem integrationGateRecord_branches_eq :
    integrationGateRecords.map (fun r => r.branch) =
      ["selected Kuratowski/Linfty metric branch",
        "external sphere-eversion h-principle adjacent branch",
        "authenticated global external search"] :=
  rfl

/-- Checked certificate for the C006 integration-gate decisions. -/
theorem integrationGateRecord_gateResults_eq :
    integrationGateRecords.map (fun r => r.gateResult) =
      ["repo_local_closed_by_local_wrapper_upstream_mathlib",
        "not_completed_external_anchor_only_with_concrete_blocker",
        "not_completed_authentication_blocker"] :=
  rfl

/-- Checked certificate that C006 does not mark anchor-only evidence as completed. -/
theorem integrationGateRepoLocalDebtResult_eq :
    integrationGateRepoLocalDebtResult =
      "pass: no completed state retains repo_local_integration_debt; adjacent external anchor has a concrete blocker and is not a completion claim" :=
  rfl

end S1_M_132
end Stage1
end AwesomeTheorems
