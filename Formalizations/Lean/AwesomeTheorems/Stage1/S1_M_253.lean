import Mathlib.Geometry.Manifold.Riemannian.Basic
import Mathlib.Geometry.Manifold.LocalDiffeomorph
import Mathlib.Geometry.Manifold.SmoothEmbedding
import Mathlib.Geometry.Manifold.VectorBundle.Tangent
import Mathlib.Analysis.Calculus.InverseFunctionTheorem.ContDiff
import Mathlib.Topology.FiberBundle.IsHomeomorphicTrivialBundle

/-!
# S1-M-253 / THM-M-0597: Tubular neighborhood theorem

This Stage1 artifact records a conservative Lean 4 boundary for the theorem
that an embedded submanifold has a tubular neighborhood modeled on its normal
bundle.

The pinned mathlib snapshot has smooth manifolds, smooth embeddings, tangent
bundles, smooth vector bundles, Riemannian bundles, local diffeomorphisms,
model-space inverse-function-theorem infrastructure, and topological
fiber-bundle infrastructure.  This audit did not locate a bundled
embedded-submanifold API, a normal-bundle construction for submanifolds, a
manifold exponential map or geodesic exponential local-diffeomorphism theorem
for Riemannian manifolds, an exponential-map tubular-neighborhood construction,
or a terminal tubular-neighborhood theorem.  Accordingly, the main theorem is
represented as a statement shape.  The checked declarations below expose nearby
mathlib anchors, replace the former unpinned embedded-submanifold proposition by
a `Manifold.IsSmoothEmbedding` carrier model, and check the degenerate
`S = univ` package.
-/

noncomputable section

open scoped Manifold Topology ContDiff

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_253

universe uE uH uM uB uF uV u𝕜

/--
Pinned mathlib carrier model for an embedded submanifold.

The current mathlib snapshot does not provide a bundled subset-level
`EmbeddedSubmanifold` structure.  The closest checked API is
`Manifold.IsSmoothEmbedding` from `Mathlib.Geometry.Manifold.SmoothEmbedding`.
This predicate records that the carrier is the range of a smooth embedding from
some source manifold using the same model-with-corners parameters as the ambient
manifold.  This is a machine-checked replacement for the former unpinned
`EmbeddedSubmanifoldInput.isEmbeddedSubmanifold : Prop` field, but it is not yet
the full normal-bundle/tubular-neighborhood input package.
-/
def HasPinnedSmoothEmbeddingCarrierModel
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M] [IsManifold I ∞ M]
    (S : Set M) : Prop :=
  ∃ (N : Type uM) (_ : TopologicalSpace N) (_ : ChartedSpace H N)
    (_ : IsManifold I ∞ N) (f : N → M),
      Manifold.IsSmoothEmbedding I I ∞ f ∧ Set.range f = S

/--
Fiberwise normal-bundle boundary over the selected carrier.

Because this mathlib snapshot has no bundled normal bundle for embedded
submanifolds, this record keeps the local linear algebra explicit: at every
carrier point it names a tangent subspace, a candidate normal fiber inside the
ambient tangent space, and the required tangent/normal direct-sum splitting.
-/
structure CarrierNormalBundleModel
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] (S : Set M) where
  tangentSubspace : (x : S) → Submodule ℝ (TangentSpace I x.1)
  normalFiber : (x : S) → Submodule ℝ (TangentSpace I x.1)
  tangent_normal_isCompl :
    ∀ x : S, IsCompl (tangentSubspace x) (normalFiber x)

/-- Total-space type of the explicit fiberwise normal-bundle boundary. -/
def CarrierNormalBundleModel.Total
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] {S : Set M}
    (N : CarrierNormalBundleModel I S) : Type _ :=
  Σ x : S, N.normalFiber x

/-- Projection from the explicit normal-bundle total space to the carrier. -/
def CarrierNormalBundleModel.proj
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] {S : Set M}
    (N : CarrierNormalBundleModel I S) :
    N.Total → S :=
  Sigma.fst

/-- Zero section of the explicit normal-bundle boundary. -/
def CarrierNormalBundleModel.zeroSection
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] {S : Set M}
    (N : CarrierNormalBundleModel I S) :
    S → N.Total :=
  fun x => ⟨x, 0⟩

/-- The explicit zero section projects back to the original carrier point. -/
theorem CarrierNormalBundleModel.proj_zeroSection
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] {S : Set M}
    (N : CarrierNormalBundleModel I S) (x : S) :
    N.proj (N.zeroSection x) = x :=
  rfl

/--
The part of the tubular-neighborhood input handled by this child task:
fiberwise tangent-space splitting along the carrier.
-/
def TangentSpaceSplittingData
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] (S : Set M) : Prop :=
  ∃ tangentSubspace normalFiber :
      (x : S) → Submodule ℝ (TangentSpace I x.1),
    ∀ x : S, IsCompl (tangentSubspace x) (normalFiber x)

/-- A pinned normal-bundle boundary supplies the tangent-space splitting data. -/
theorem CarrierNormalBundleModel.tangentSpaceSplittingData
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] {S : Set M}
    (N : CarrierNormalBundleModel I S) :
    TangentSpaceSplittingData I S :=
  ⟨N.tangentSubspace, N.normalFiber, N.tangent_normal_isCompl⟩

/--
Riemannian orthogonal-complement specialization of the explicit normal-bundle
boundary.  This is still a boundary record: the smooth vector-bundle structure
of these fibers is a later child task.
-/
structure RiemannianOrthogonalNormalBundleModel
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    [(x : M) → NormedAddCommGroup (TangentSpace I x)]
    [(x : M) → InnerProductSpace ℝ (TangentSpace I x)]
    (S : Set M) extends CarrierNormalBundleModel I S where
  normalFiber_mem_iff_inner_eq_zero :
    ∀ x : S, ∀ v : TangentSpace I x.1,
      v ∈ normalFiber x ↔
        ∀ w : TangentSpace I x.1, w ∈ tangentSubspace x → inner ℝ v w = 0

/-- The orthogonal-complement package still exposes the same splitting gate. -/
theorem RiemannianOrthogonalNormalBundleModel.tangentSpaceSplittingData
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    [(x : M) → NormedAddCommGroup (TangentSpace I x)]
    [(x : M) → InnerProductSpace ℝ (TangentSpace I x)]
    {S : Set M} (N : RiemannianOrthogonalNormalBundleModel I S) :
    TangentSpaceSplittingData I S :=
  N.toCarrierNormalBundleModel.tangentSpaceSplittingData

/--
Checked smooth-vector-bundle wrapper for a candidate normal bundle over the
carrier subtype.

The wrapper deliberately separates two facts.  The typeclass parameters are
machine-checked mathlib structure: a topological total space
`Bundle.TotalSpace F ν`, a topological fiber bundle, a real vector bundle, and
a `C^∞` vector bundle over the carrier manifold.  The final proposition records
the still-missing mathematical identification of these fibers with the normal
subspaces coming from `CarrierNormalBundleModel`; this cannot be discharged
until a pinned submanifold normal-bundle construction is available.
-/
structure SmoothNormalBundleVectorBundleWrapper
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] (S : Set M)
    [TopologicalSpace S] [ChartedSpace H S] [IsManifold I ∞ S]
    (F : Type uF) [NormedAddCommGroup F] [NormedSpace ℝ F]
    (ν : S → Type uV) [TopologicalSpace (Bundle.TotalSpace F ν)]
    [∀ x : S, TopologicalSpace (ν x)] [FiberBundle F ν]
    [∀ x : S, AddCommGroup (ν x)] [∀ x : S, Module ℝ (ν x)]
    [VectorBundle ℝ F ν] [ContMDiffVectorBundle ∞ F ν I] where
  identifiesCarrierNormalFibers : Prop
  identifiesCarrierNormalFibers_holds : identifiesCarrierNormalFibers

namespace SmoothNormalBundleVectorBundleWrapper

/-- Total-space type supplied by mathlib's vector-bundle hierarchy. -/
abbrev Total
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] {S : Set M}
    [TopologicalSpace S] [ChartedSpace H S] [IsManifold I ∞ S]
    {F : Type uF} [NormedAddCommGroup F] [NormedSpace ℝ F]
    {ν : S → Type uV} [TopologicalSpace (Bundle.TotalSpace F ν)]
    [∀ x : S, TopologicalSpace (ν x)] [FiberBundle F ν]
    [∀ x : S, AddCommGroup (ν x)] [∀ x : S, Module ℝ (ν x)]
    [VectorBundle ℝ F ν] [ContMDiffVectorBundle ∞ F ν I]
    (_N : SmoothNormalBundleVectorBundleWrapper I S F ν) : Type _ :=
  Bundle.TotalSpace F ν

/-- Projection from the checked normal-bundle total space to the carrier. -/
def proj
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] {S : Set M}
    [TopologicalSpace S] [ChartedSpace H S] [IsManifold I ∞ S]
    {F : Type uF} [NormedAddCommGroup F] [NormedSpace ℝ F]
    {ν : S → Type uV} [TopologicalSpace (Bundle.TotalSpace F ν)]
    [∀ x : S, TopologicalSpace (ν x)] [FiberBundle F ν]
    [∀ x : S, AddCommGroup (ν x)] [∀ x : S, Module ℝ (ν x)]
    [VectorBundle ℝ F ν] [ContMDiffVectorBundle ∞ F ν I]
    (N : SmoothNormalBundleVectorBundleWrapper I S F ν) :
    N.Total → S :=
  Bundle.TotalSpace.proj

/-- Zero section of the checked smooth normal-bundle wrapper. -/
def zeroSection
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] {S : Set M}
    [TopologicalSpace S] [ChartedSpace H S] [IsManifold I ∞ S]
    {F : Type uF} [NormedAddCommGroup F] [NormedSpace ℝ F]
    {ν : S → Type uV} [TopologicalSpace (Bundle.TotalSpace F ν)]
    [∀ x : S, TopologicalSpace (ν x)] [FiberBundle F ν]
    [∀ x : S, AddCommGroup (ν x)] [∀ x : S, Module ℝ (ν x)]
    [VectorBundle ℝ F ν] [ContMDiffVectorBundle ∞ F ν I]
    (N : SmoothNormalBundleVectorBundleWrapper I S F ν) :
    S → N.Total :=
  Bundle.zeroSection F ν

/-- The checked wrapper carries an explicit topological total space. -/
theorem total_topologicalSpace
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] {S : Set M}
    [TopologicalSpace S] [ChartedSpace H S] [IsManifold I ∞ S]
    {F : Type uF} [NormedAddCommGroup F] [NormedSpace ℝ F]
    {ν : S → Type uV} [TopologicalSpace (Bundle.TotalSpace F ν)]
    [∀ x : S, TopologicalSpace (ν x)] [FiberBundle F ν]
    [∀ x : S, AddCommGroup (ν x)] [∀ x : S, Module ℝ (ν x)]
    [VectorBundle ℝ F ν] [ContMDiffVectorBundle ∞ F ν I]
    (N : SmoothNormalBundleVectorBundleWrapper I S F ν) :
    Nonempty (TopologicalSpace N.Total) :=
  ⟨inferInstance⟩

/-- The checked wrapper is a real vector bundle in mathlib's topology hierarchy. -/
theorem vectorBundle
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] {S : Set M}
    [TopologicalSpace S] [ChartedSpace H S] [IsManifold I ∞ S]
    {F : Type uF} [NormedAddCommGroup F] [NormedSpace ℝ F]
    {ν : S → Type uV} [TopologicalSpace (Bundle.TotalSpace F ν)]
    [∀ x : S, TopologicalSpace (ν x)] [FiberBundle F ν]
    [∀ x : S, AddCommGroup (ν x)] [∀ x : S, Module ℝ (ν x)]
    [VectorBundle ℝ F ν] [ContMDiffVectorBundle ∞ F ν I]
    (_N : SmoothNormalBundleVectorBundleWrapper I S F ν) :
    VectorBundle ℝ F ν :=
  inferInstance

/-- The checked wrapper is a `C^∞` vector bundle over the carrier manifold. -/
theorem contMDiffVectorBundle
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] {S : Set M}
    [TopologicalSpace S] [ChartedSpace H S] [IsManifold I ∞ S]
    {F : Type uF} [NormedAddCommGroup F] [NormedSpace ℝ F]
    {ν : S → Type uV} [TopologicalSpace (Bundle.TotalSpace F ν)]
    [∀ x : S, TopologicalSpace (ν x)] [FiberBundle F ν]
    [∀ x : S, AddCommGroup (ν x)] [∀ x : S, Module ℝ (ν x)]
    [VectorBundle ℝ F ν] [ContMDiffVectorBundle ∞ F ν I]
    (_N : SmoothNormalBundleVectorBundleWrapper I S F ν) :
    ContMDiffVectorBundle ∞ F ν I :=
  inferInstance

/-- The zero section projects back to the carrier point. -/
theorem proj_zeroSection
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] {S : Set M}
    [TopologicalSpace S] [ChartedSpace H S] [IsManifold I ∞ S]
    {F : Type uF} [NormedAddCommGroup F] [NormedSpace ℝ F]
    {ν : S → Type uV} [TopologicalSpace (Bundle.TotalSpace F ν)]
    [∀ x : S, TopologicalSpace (ν x)] [FiberBundle F ν]
    [∀ x : S, AddCommGroup (ν x)] [∀ x : S, Module ℝ (ν x)]
    [VectorBundle ℝ F ν] [ContMDiffVectorBundle ∞ F ν I]
    (N : SmoothNormalBundleVectorBundleWrapper I S F ν) (x : S) :
    N.proj (N.zeroSection x) = x :=
  rfl

/-- The normal-bundle projection is continuous by mathlib's fiber-bundle API. -/
theorem continuous_proj
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] {S : Set M}
    [TopologicalSpace S] [ChartedSpace H S] [IsManifold I ∞ S]
    {F : Type uF} [NormedAddCommGroup F] [NormedSpace ℝ F]
    {ν : S → Type uV} [TopologicalSpace (Bundle.TotalSpace F ν)]
    [∀ x : S, TopologicalSpace (ν x)] [FiberBundle F ν]
    [∀ x : S, AddCommGroup (ν x)] [∀ x : S, Module ℝ (ν x)]
    [VectorBundle ℝ F ν] [ContMDiffVectorBundle ∞ F ν I]
    (N : SmoothNormalBundleVectorBundleWrapper I S F ν) :
    Continuous N.proj :=
  FiberBundle.continuous_proj F ν

/-- The zero section is smooth in the checked smooth-vector-bundle wrapper. -/
theorem contMDiff_zeroSection
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] {S : Set M}
    [TopologicalSpace S] [ChartedSpace H S] [IsManifold I ∞ S]
    {F : Type uF} [NormedAddCommGroup F] [NormedSpace ℝ F]
    {ν : S → Type uV} [TopologicalSpace (Bundle.TotalSpace F ν)]
    [∀ x : S, TopologicalSpace (ν x)] [FiberBundle F ν]
    [∀ x : S, AddCommGroup (ν x)] [∀ x : S, Module ℝ (ν x)]
    [VectorBundle ℝ F ν] [ContMDiffVectorBundle ∞ F ν I]
    (N : SmoothNormalBundleVectorBundleWrapper I S F ν) :
    ContMDiff I (I.prod 𝓘(ℝ, F)) ∞ N.zeroSection :=
  Bundle.contMDiff_zeroSection ℝ ν

/-- The total space is a smooth manifold modeled on base charts times the fiber. -/
theorem total_isManifold
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] {S : Set M}
    [TopologicalSpace S] [ChartedSpace H S] [IsManifold I ∞ S]
    {F : Type uF} [NormedAddCommGroup F] [NormedSpace ℝ F]
    {ν : S → Type uV} [TopologicalSpace (Bundle.TotalSpace F ν)]
    [∀ x : S, TopologicalSpace (ν x)] [FiberBundle F ν]
    [∀ x : S, AddCommGroup (ν x)] [∀ x : S, Module ℝ (ν x)]
    [VectorBundle ℝ F ν] [ContMDiffVectorBundle ∞ F ν I]
    (N : SmoothNormalBundleVectorBundleWrapper I S F ν) :
    IsManifold (I.prod 𝓘(ℝ, F)) ∞ N.Total :=
  inferInstance

end SmoothNormalBundleVectorBundleWrapper

/-- Degenerate carrier model: for `S = univ`, the normal fiber is `⊥`. -/
def univCarrierNormalBundleModel
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M] :
    CarrierNormalBundleModel I (Set.univ : Set M) where
  tangentSubspace := fun _ => ⊤
  normalFiber := fun _ => ⊥
  tangent_normal_isCompl := by
    intro x
    exact isCompl_top_bot

/--
Input data for a future formal tubular-neighborhood theorem.

The `carrier` is the subset of the ambient manifold intended to be the embedded
submanifold.  The embedded-carrier field is pinned to mathlib's
`Manifold.IsSmoothEmbedding` API.  The normal-bundle predicates remain explicit
proposition fields because this mathlib snapshot does not expose a canonical
bundled normal-bundle API for the theorem.
-/
structure EmbeddedSubmanifoldInput
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M] [IsManifold I ∞ M] where
  carrier : Set M
  smoothEmbeddingCarrierModel : HasPinnedSmoothEmbeddingCarrierModel E H I M carrier
  normalBundleModel : Nonempty (CarrierNormalBundleModel I carrier)
  hasSmoothNormalBundleModel : Prop
  normalBundleSplittingData : Prop
  normalBundleSplittingWitness : TangentSpaceSplittingData I carrier

/--
Candidate output object for a tubular neighborhood.

`NormalTotal` stands for the total space of the normal bundle restricted to the
submanifold.  The fields assert that a domain around the zero section is mapped
onto a neighborhood of the submanifold and that the zero section is the original
inclusion.  Smoothness/diffeomorphism requirements remain proposition fields
until the missing submanifold and normal-bundle APIs are pinned.
-/
structure TubularNeighborhoodPackage
    (M : Type uM) [TopologicalSpace M] (S : Set M) where
  NormalTotal : Type uM
  normalTopologicalSpace : TopologicalSpace NormalTotal
  zeroSection : S → NormalTotal
  baseProjection : NormalTotal → S
  tubularMap : NormalTotal → M
  domain : Set NormalTotal
  imageNeighborhood : Set M
  imageNeighborhood_mem_nhdsSet : imageNeighborhood ∈ 𝓝ˢ S
  mapsTo_imageNeighborhood : Set.MapsTo tubularMap domain imageNeighborhood
  zeroSection_landsInDomain : ∀ x : S, zeroSection x ∈ domain
  tubularMap_zeroSection : ∀ x : S, tubularMap (zeroSection x) = x.1
  normalBundleModel : Prop
  smoothOnDomain : Prop
  diffeomorphsDomainOntoNeighborhood : Prop

/--
Terminal conclusion expected from a completed tubular-neighborhood
formalization.
-/
def TubularNeighborhoodConclusion
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] [IsManifold I ∞ M]
    (D : EmbeddedSubmanifoldInput E H I M) : Prop :=
  Nonempty (TubularNeighborhoodPackage M D.carrier)

/--
Stage1 normalized statement shape for the tubular-neighborhood theorem.

This is intentionally a boundary statement, not a proof.  A full proof must
replace the proposition fields in `EmbeddedSubmanifoldInput` and
`TubularNeighborhoodPackage` with pinned mathlib or external Lean definitions
for embedded submanifolds, normal bundles, exponential maps, and local
diffeomorphism data.
-/
def StatementShape
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    [FiniteDimensional ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
  (M : Type uM) [TopologicalSpace M] [ChartedSpace H M] [IsManifold I ∞ M] :
    Prop :=
  ∀ D : EmbeddedSubmanifoldInput E H I M,
    D.hasSmoothNormalBundleModel →
      D.normalBundleSplittingData →
        TubularNeighborhoodConclusion D

/-- The normalized statement shape unfolds to the explicit input/conclusion form. -/
theorem statementShape_iff
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]
    [FiniteDimensional ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M] [IsManifold I ∞ M] :
    StatementShape E H I M ↔
      ∀ D : EmbeddedSubmanifoldInput E H I M,
        D.hasSmoothNormalBundleModel →
          D.normalBundleSplittingData →
            TubularNeighborhoodConclusion D :=
  Iff.rfl

/--
The whole ambient manifold is the range of the identity smooth embedding.

This is the checked low-risk carrier witness used by the degenerate
`S = univ` tubular-neighborhood package.
-/
theorem univ_hasPinnedSmoothEmbeddingCarrierModel
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M] [IsManifold I ∞ M] :
    HasPinnedSmoothEmbeddingCarrierModel E H I M (Set.univ : Set M) := by
  refine ⟨M, inferInstance, inferInstance, inferInstance, id, ?_, ?_⟩
  · exact Manifold.IsSmoothEmbedding.id
  · ext x
    simp

/--
Degenerate checked package: the whole ambient space has a tautological
"tubular neighborhood" given by the identity map on `M`.

This is not the submanifold theorem.  It verifies that the package type itself
has a nonempty, locally checkable instance in the easiest boundary case.
-/
def univTubularNeighborhoodPackage
    (M : Type uM) [TopologicalSpace M] :
    TubularNeighborhoodPackage M (Set.univ : Set M) where
  NormalTotal := M
  normalTopologicalSpace := inferInstance
  zeroSection := fun x => x.1
  baseProjection := fun x => ⟨x, trivial⟩
  tubularMap := id
  domain := Set.univ
  imageNeighborhood := Set.univ
  imageNeighborhood_mem_nhdsSet := Filter.univ_mem
  mapsTo_imageNeighborhood := by
    intro x hx
    trivial
  zeroSection_landsInDomain := by
    intro x
    trivial
  tubularMap_zeroSection := by
    intro x
    rfl
  normalBundleModel := True
  smoothOnDomain := True
  diffeomorphsDomainOntoNeighborhood := True

/-- The degenerate `S = univ` package is a checked nonempty conclusion. -/
theorem univ_tubularNeighborhoodConclusion
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M] [IsManifold I ∞ M] :
    TubularNeighborhoodConclusion
      ({ carrier := Set.univ
         smoothEmbeddingCarrierModel := univ_hasPinnedSmoothEmbeddingCarrierModel E H I M
         normalBundleModel := ⟨univCarrierNormalBundleModel E H I M⟩
         hasSmoothNormalBundleModel := True
         normalBundleSplittingData := True
         normalBundleSplittingWitness :=
           (univCarrierNormalBundleModel E H I M).tangentSpaceSplittingData } :
        EmbeddedSubmanifoldInput E H I M) :=
  ⟨univTubularNeighborhoodPackage M⟩

/-- Carrier of the zero-section/trivial-product submanifold `B × {0}` in `B × F`. -/
def productZeroSectionCarrier (B : Type uB) (F : Type uF) [Zero F] : Set (B × F) :=
  Set.range fun b : B => (b, 0)

/-- Membership in the product zero-section carrier is exactly vanishing of the fiber coordinate. -/
theorem mem_productZeroSectionCarrier_iff
    (B : Type uB) (F : Type uF) [Zero F] (x : B × F) :
    x ∈ productZeroSectionCarrier B F ↔ x.2 = 0 := by
  constructor
  · rintro ⟨b, rfl⟩
    rfl
  · intro hx
    refine ⟨x.1, ?_⟩
    ext <;> simp [hx]

/--
Checked product/trivial-submanifold package for the zero section `B × {0}`.

This is the low-risk trivial case where the normal total space is modeled by
the ambient product itself, the base projection forgets the fiber coordinate,
and the tubular map is the identity on `B × F`.
-/
def productTrivialSubmanifoldTubularNeighborhoodPackage
    (B : Type uB) (F : Type uF) [TopologicalSpace B] [TopologicalSpace F] [Zero F] :
    TubularNeighborhoodPackage (B × F) (productZeroSectionCarrier B F) where
  NormalTotal := B × F
  normalTopologicalSpace := inferInstance
  zeroSection := fun x => x.1
  baseProjection := fun p => ⟨(p.1, 0), ⟨p.1, rfl⟩⟩
  tubularMap := id
  domain := Set.univ
  imageNeighborhood := Set.univ
  imageNeighborhood_mem_nhdsSet := Filter.univ_mem
  mapsTo_imageNeighborhood := by
    intro x hx
    trivial
  zeroSection_landsInDomain := by
    intro x
    trivial
  tubularMap_zeroSection := by
    intro x
    rfl
  normalBundleModel := True
  smoothOnDomain := True
  diffeomorphsDomainOntoNeighborhood := True

/-- The product/trivial-submanifold carrier has a checked tubular-neighborhood package. -/
theorem productTrivialSubmanifold_tubularNeighborhoodPackage_nonempty
    (B : Type uB) (F : Type uF) [TopologicalSpace B] [TopologicalSpace F] [Zero F] :
    Nonempty (TubularNeighborhoodPackage (B × F) (productZeroSectionCarrier B F)) :=
  ⟨productTrivialSubmanifoldTubularNeighborhoodPackage B F⟩

/-- The product/trivial-submanifold package projects `(b, v)` to `(b, 0)`. -/
theorem productTrivialSubmanifold_baseProjection_coe
    (B : Type uB) (F : Type uF) [TopologicalSpace B] [TopologicalSpace F] [Zero F]
    (p : B × F) :
    ((productTrivialSubmanifoldTubularNeighborhoodPackage B F).baseProjection p).1 =
      (p.1, 0) :=
  rfl

/-- The product/trivial-submanifold tubular map is the identity on the ambient product. -/
theorem productTrivialSubmanifold_tubularMap_apply
    (B : Type uB) (F : Type uF) [TopologicalSpace B] [TopologicalSpace F] [Zero F]
    (p : B × F) :
    (productTrivialSubmanifoldTubularNeighborhoodPackage B F).tubularMap p = p :=
  rfl

/-- Checked wrapper: the identity map on a charted manifold is smooth to any order. -/
theorem contMDiff_id_mathlib_wrapper
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners 𝕜 E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {n : WithTop ℕ∞} :
    ContMDiff I I n (id : M → M) :=
  contMDiff_id

/-- Checked wrapper: the tangent map of the identity is the identity. -/
theorem tangentMap_id_mathlib_wrapper
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners 𝕜 E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] :
    tangentMap I I (id : M → M) = id :=
  tangentMap_id

/-- Checked wrapper: the manifold derivative of the identity is the identity on tangent spaces. -/
theorem mfderiv_id_mathlib_wrapper
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners 𝕜 E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M] (x : M) :
    mfderiv I I (id : M → M) x = ContinuousLinearMap.id 𝕜 (TangentSpace I x) :=
  mfderiv_id

/-- Checked wrapper: the product projection is mathlib's trivial fiber bundle model. -/
theorem productProjection_trivialFiberBundle_mathlib_wrapper
    (B : Type uB) (F : Type uF) [TopologicalSpace B] [TopologicalSpace F] :
    IsHomeomorphicTrivialFiberBundle F (Prod.fst : B × F → B) :=
  isHomeomorphicTrivialFiberBundle_fst F

/-- Checked wrapper: the product projection is continuous. -/
theorem productProjection_continuous_mathlib_wrapper
    (B : Type uB) (F : Type uF) [TopologicalSpace B] [TopologicalSpace F] :
    Continuous (Prod.fst : B × F → B) :=
  (productProjection_trivialFiberBundle_mathlib_wrapper B F).continuous_proj

/--
Checked wrapper: mathlib has a generic smooth local-diffeomorphism predicate
for manifolds.

For the tubular-neighborhood theorem this is only the target API for the future
tubular map; this child did not locate a Riemannian exponential-map theorem
which proves that the normal exponential map satisfies this predicate.
-/
theorem isLocalDiffeomorph_contMDiff_mathlib_wrapper
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    {F : Type uF} [NormedAddCommGroup F] [NormedSpace 𝕜 F]
    {H : Type uH} [TopologicalSpace H] {G : Type uB} [TopologicalSpace G]
    {I : ModelWithCorners 𝕜 E H} {J : ModelWithCorners 𝕜 F G}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {N : Type uV} [TopologicalSpace N] [ChartedSpace G N]
    {n : WithTop ℕ∞} {f : M → N} (hf : IsLocalDiffeomorph I J n f) :
    ContMDiff I J n f :=
  hf.contMDiff

/-- Checked wrapper: a mathlib local diffeomorphism has open range. -/
theorem isLocalDiffeomorph_openRange_mathlib_wrapper
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    {F : Type uF} [NormedAddCommGroup F] [NormedSpace 𝕜 F]
    {H : Type uH} [TopologicalSpace H] {G : Type uB} [TopologicalSpace G]
    {I : ModelWithCorners 𝕜 E H} {J : ModelWithCorners 𝕜 F G}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {N : Type uV} [TopologicalSpace N] [ChartedSpace G N]
    {n : WithTop ℕ∞} {f : M → N} (hf : IsLocalDiffeomorph I J n f) :
    IsOpen (Set.range f) :=
  hf.isOpen_range

/-- Checked wrapper: local-diffeomorphism hypotheses give fiberwise tangent equivalences. -/
noncomputable def isLocalDiffeomorphAt_mfderivEquiv_mathlib_wrapper
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
    {F : Type uF} [NormedAddCommGroup F] [NormedSpace 𝕜 F]
    {H : Type uH} [TopologicalSpace H] {G : Type uB} [TopologicalSpace G]
    {I : ModelWithCorners 𝕜 E H} {J : ModelWithCorners 𝕜 F G}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {N : Type uV} [TopologicalSpace N] [ChartedSpace G N]
    {n : WithTop ℕ∞} {f : M → N} {x : M}
    (hf : IsLocalDiffeomorphAt I J n f x) (hn : n ≠ 0) :
    TangentSpace I x ≃L[𝕜] TangentSpace J (f x) :=
  hf.mfderivToContinuousLinearEquiv hn

/--
Checked model-space inverse-function-theorem anchor.  It constructs a local
homeomorphism from an invertible strict derivative in normed vector spaces, but
it is not a Riemannian exponential-map theorem and it is not a manifold tubular
construction.
-/
noncomputable def hasStrictFDerivAt_toOpenPartialHomeomorph_mathlib_wrapper
    {𝕜 : Type u𝕜} [NontriviallyNormedField 𝕜]
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace 𝕜 E] [CompleteSpace E]
    {F : Type uF} [NormedAddCommGroup F] [NormedSpace 𝕜 F]
    {f : E → F} {f' : E ≃L[𝕜] F} {a : E}
    (hf : HasStrictFDerivAt f (f' : E →L[𝕜] F) a) :
    OpenPartialHomeomorph E F :=
  hf.toOpenPartialHomeomorph f

/-! ## Audit probes retained in the checked file. -/

#check ModelWithCorners
#check IsManifold
#check ContMDiff
#check ContMDiffOn
#check Manifold.IsSmoothEmbedding
#check Manifold.IsSmoothEmbedding.id
#check Manifold.IsSmoothEmbedding.of_opens
#check TangentSpace
#check TangentBundle.contMDiffVectorBundle
#check Bundle.TotalSpace
#check Bundle.zeroSection
#check Bundle.zeroSection_proj
#check Bundle.contMDiff_zeroSection
#check Bundle.TotalSpace.isManifold
#check VectorBundle
#check ContMDiffVectorBundle
#check Bundle.RiemannianBundle
#check IsContMDiffRiemannianBundle
#check IsRiemannianManifold
#check IsCompl
#check inner
#check FiberBundle
#check FiberBundle.continuous_proj
#check IsHomeomorphicTrivialFiberBundle
#check isHomeomorphicTrivialFiberBundle_fst
#check tangentMap
#check tangentMap_id
#check mfderiv
#check mfderiv_id
#check IsLocalDiffeomorph
#check IsLocalDiffeomorphAt
#check IsLocalDiffeomorphOn
#check IsLocalDiffeomorph.contMDiff
#check IsLocalDiffeomorph.isOpen_range
#check IsLocalDiffeomorphAt.mfderivToContinuousLinearEquiv
#check IsLocalDiffeomorph.diffeomorphOfBijective
#check HasStrictFDerivAt.toOpenPartialHomeomorph
#check HasStrictFDerivAt.localInverse
#check ContDiffAt.to_localInverse

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Geometry.Manifold.Riemannian.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.Tangent",
  "Mathlib.Geometry.Manifold.VectorBundle.Riemannian",
  "Mathlib.Geometry.Manifold.SmoothEmbedding",
  "Mathlib.Geometry.Manifold.Immersion",
  "Mathlib.Geometry.Manifold.LocalDiffeomorph",
  "Mathlib.Geometry.Manifold.MFDeriv.Defs",
  "Mathlib.Analysis.Calculus.InverseFunctionTheorem.FDeriv",
  "Mathlib.Analysis.Calculus.InverseFunctionTheorem.ContDiff",
  "Mathlib.Topology.FiberBundle.Basic",
  "Mathlib.Topology.FiberBundle.IsHomeomorphicTrivialBundle"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ModelWithCorners",
  "IsManifold",
  "ContMDiff",
  "ContMDiffOn",
  "Manifold.IsSmoothEmbedding",
  "Manifold.IsSmoothEmbedding.id",
  "Manifold.IsSmoothEmbedding.of_opens",
  "TangentSpace",
  "TangentBundle.contMDiffVectorBundle",
  "Bundle.TotalSpace",
  "Bundle.zeroSection",
  "Bundle.zeroSection_proj",
  "Bundle.contMDiff_zeroSection",
  "Bundle.TotalSpace.isManifold",
  "VectorBundle",
  "ContMDiffVectorBundle",
  "RiemannianBundle",
  "IsContMDiffRiemannianBundle",
  "IsRiemannianManifold",
  "IsCompl",
  "inner",
  "FiberBundle",
  "FiberBundle.continuous_proj",
  "IsHomeomorphicTrivialFiberBundle",
  "isHomeomorphicTrivialFiberBundle_fst",
  "tangentMap",
  "tangentMap_id",
  "mfderiv",
  "mfderiv_id",
  "IsLocalDiffeomorph",
  "IsLocalDiffeomorphAt",
  "IsLocalDiffeomorphOn",
  "IsLocalDiffeomorph.contMDiff",
  "IsLocalDiffeomorph.isOpen_range",
  "IsLocalDiffeomorphAt.mfderivToContinuousLinearEquiv",
  "IsLocalDiffeomorph.diffeomorphOfBijective",
  "HasStrictFDerivAt.toOpenPartialHomeomorph",
  "HasStrictFDerivAt.localInverse",
  "ContDiffAt.to_localInverse"
]

/--
Search terms that did not locate a terminal tubular-neighborhood theorem or
bundled submanifold normal-bundle API in local mathlib.
-/
def absentTerminalSearchTerms : List String := [
  "Tubular",
  "tubular",
  "tubular neighborhood",
  "tubular neighbourhood",
  "Submanifold",
  "EmbeddedSubmanifold",
  "normal bundle",
  "normalBundle",
  "NormalBundle",
  "exponential tubular",
  "expMap",
  "exponential map",
  "manifold exponential map",
  "geodesic exponential",
  "Geodesic"
]

/-- One row in the external Lean 4 tubular-neighborhood anchor audit. -/
structure ExternalAnchorAuditRow where
  source : String
  checkedOn : String
  outcome : String
  repoLocalAction : String

/--
External-source audit rows for the terminal tubular-neighborhood theorem.

These rows are intentionally data, not theorem evidence.  They record that this
Stage1 pass did not find an external Lean 4 theorem that can be pinned,
imported, and checked.  If a future audit finds a real terminal theorem, the
repo-local completion gate must switch to a pinned Lake dependency, vendored
proof body, or explicit Lake/toolchain/license blocker before any completion
claim.
-/
def externalTubularNeighborhoodAnchorAudit : List ExternalAnchorAuditRow := [
  { source :=
      "local mathlib4 dependency https://github.com/leanprover-community/mathlib4 at rev 8a178386ffc0f5fef0b77738bb5449d50efeea95"
    checkedOn := "2026-05-01"
    outcome :=
      "no terminal tubular-neighborhood theorem, bundled embedded-submanifold normal bundle, normal exponential map, or manifold exponential-map local-diffeomorphism theorem located by local source search"
    repoLocalAction :=
      "no external import target; keep parent as formalization_debt rather than repo_local_integration_debt" },
  { source :=
      "web search queries: \"tubular neighborhood theorem\" \"Lean 4\"; \"tubular neighbourhood theorem\" \"Lean 4\"; \"TubularNeighborhood\" Lean theorem; site:github.com \"tubular neighborhood theorem\" \"Lean\""
    checkedOn := "2026-05-01"
    outcome :=
      "no primary Lean 4 project exposing a terminal tubular-neighborhood theorem was found; broad results were unrelated pages or non-Lean mathematical references"
    repoLocalAction :=
      "no pin/import/check candidate; do not claim external_upstream_anchor_only completion" },
  { source :=
      "GitHub REST code-search API probes for Lean files containing TubularNeighborhood or tubular-neighborhood theorem terms"
    checkedOn := "2026-05-01"
    outcome :=
      "code search returned HTTP 401 Requires authentication in this environment, so it did not provide a primary-source candidate"
    repoLocalAction :=
      "concrete audit blocker for this probe only: authenticated GitHub code search is required before treating GitHub-wide absence as exhaustive" }
]

/-- This child found no external terminal theorem that is ready for repo-local import. -/
def externalTubularNeighborhoodImportCandidateFound : Bool := false

/-- One unchecked M0387 theorem-tree leaf for the future tubular-neighborhood proof. -/
structure TubularNeighborhoodLeafSplitRow where
  leafId : String
  parentPackage : String
  independentObligation : String
  localBudgetBound : Nat
  machineAnchorStatus : String
  integrationBlocker : String

/--
Machine-readable split of `TN-L101` through `TN-L112` into independent
`<= 100`-step leaves.

These rows are proof-tree planning data, not completed theorem evidence.  Every
row is deliberately marked `unchecked` because the current repo-local artifact
still lacks the terminal embedded-submanifold normal-bundle and
normal-exponential-map APIs needed to discharge the general theorem.
-/
def tubularNeighborhoodUncheckedLeafSplit : List TubularNeighborhoodLeafSplitRow := [
  { leafId := "TN-L101"
    parentPackage := "TN-P2-mathlib-object-model"
    independentObligation :=
      "pin or define the canonical embedded-submanifold object model and replace proposition-only carrier fields"
    localBudgetBound := 100
    machineAnchorStatus := "unchecked"
    integrationBlocker :=
      "no bundled subset-level EmbeddedSubmanifold API was located in the pinned mathlib snapshot" },
  { leafId := "TN-L102"
    parentPackage := "TN-P2-mathlib-object-model"
    independentObligation :=
      "define tangent restriction and normal quotient or Riemannian orthogonal-complement fibers over the carrier"
    localBudgetBound := 100
    machineAnchorStatus := "unchecked"
    integrationBlocker :=
      "the current file has CarrierNormalBundleModel boundaries but no canonical submanifold normal-bundle construction" },
  { leafId := "TN-L103"
    parentPackage := "TN-P3-local-trivial-vector-bundle"
    independentObligation :=
      "prove or import that the normal object is a smooth vector bundle over the carrier subtype"
    localBudgetBound := 100
    machineAnchorStatus := "unchecked"
    integrationBlocker :=
      "SmoothNormalBundleVectorBundleWrapper checks generic vector-bundle structure only; fiber identification remains propositional" },
  { leafId := "TN-L104"
    parentPackage := "TN-P3-local-trivial-vector-bundle"
    independentObligation :=
      "construct the normal-bundle zero section and prove its smoothness in the strengthened normal-bundle API"
    localBudgetBound := 100
    machineAnchorStatus := "unchecked"
    integrationBlocker :=
      "Bundle.zeroSection and Bundle.contMDiff_zeroSection are checked, but not yet tied to a canonical submanifold normal bundle" },
  { leafId := "TN-L105"
    parentPackage := "TN-P4-Riemannian-or-splitting-construction"
    independentObligation :=
      "construct the candidate tubular map from the normal exponential map or from split-submanifold charts"
    localBudgetBound := 100
    machineAnchorStatus := "unchecked"
    integrationBlocker :=
      "local search found no manifold exponential map, normal exponential map, or split-chart tubular construction theorem" },
  { leafId := "TN-L106"
    parentPackage := "TN-P4-Riemannian-or-splitting-construction"
    independentObligation :=
      "prove the candidate tubular map restricts to the original inclusion on the zero section"
    localBudgetBound := 100
    machineAnchorStatus := "unchecked"
    integrationBlocker :=
      "requires the missing candidate tubular map from TN-L105" },
  { leafId := "TN-L107"
    parentPackage := "TN-P5-local-diffeomorphism-branch"
    independentObligation :=
      "prove local diffeomorphism of the tubular map near each zero-section point"
    localBudgetBound := 100
    machineAnchorStatus := "unchecked"
    integrationBlocker :=
      "generic IsLocalDiffeomorph anchors are checked, but no exponential-map local-diffeomorphism theorem is available" },
  { leafId := "TN-L108"
    parentPackage := "TN-P6-neighborhood-shrink-branch"
    independentObligation :=
      "produce an open domain around the zero section inside the normal total space"
    localBudgetBound := 100
    machineAnchorStatus := "unchecked"
    integrationBlocker :=
      "depends on the local diffeomorphism neighborhoods from TN-L107 and a concrete normal-total-space topology" },
  { leafId := "TN-L109"
    parentPackage := "TN-P6-neighborhood-shrink-branch"
    independentObligation :=
      "prove injectivity of the tubular map on the shrunk normal-bundle domain"
    localBudgetBound := 100
    machineAnchorStatus := "unchecked"
    integrationBlocker :=
      "requires a completed shrink argument and concrete tubular map; no terminal theorem is pinned" },
  { leafId := "TN-L110"
    parentPackage := "TN-P6-neighborhood-shrink-branch"
    independentObligation :=
      "prove that the image of the shrunk domain is a neighborhood of the submanifold in the nhdsSet sense"
    localBudgetBound := 100
    machineAnchorStatus := "unchecked"
    integrationBlocker :=
      "requires TN-L108 and TN-L109 plus the strengthened image-neighborhood theorem" },
  { leafId := "TN-L111"
    parentPackage := "TN-P7-functoriality-and-special-cases"
    independentObligation :=
      "prove base-projection or retraction compatibility for the final tubular-neighborhood package"
    localBudgetBound := 100
    machineAnchorStatus := "unchecked"
    integrationBlocker :=
      "current degenerate and product packages check special cases only, not the final general package" },
  { leafId := "TN-L112"
    parentPackage := "TN-P8-repo-local-closure-gate"
    independentObligation :=
      "package the result as a repo-local theorem or pinned wrapper with no proposition placeholders"
    localBudgetBound := 100
    machineAnchorStatus := "unchecked"
    integrationBlocker :=
      "blocked until TN-L101 through TN-L111 are discharged and public status is serially merged by an integrator" }
]

/-- The unchecked future-proof split covers exactly `TN-L101` through `TN-L112`. -/
theorem tubularNeighborhoodUncheckedLeafSplit_length :
    tubularNeighborhoodUncheckedLeafSplit.length = 12 :=
  rfl

/-- Every row in the future-proof split is budgeted as a `<= 100`-step leaf. -/
theorem tubularNeighborhoodUncheckedLeafSplit_budgetBound :
    ∀ row ∈ tubularNeighborhoodUncheckedLeafSplit, row.localBudgetBound ≤ 100 := by
  intro row hrow
  fin_cases hrow <;> decide

/--
The TN-L101..TN-L112 split is not a repo-local completion claim; no external
terminal theorem was found for import in this pass.
-/
theorem tubularNeighborhoodLeafSplit_noExternalCompletionClaim :
    externalTubularNeighborhoodImportCandidateFound = false :=
  rfl

end S1_M_253
end Stage1
end AwesomeTheorems
