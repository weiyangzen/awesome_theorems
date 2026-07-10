import Mathlib.Geometry.Manifold.WhitneyEmbedding
import Mathlib.Geometry.Manifold.SmoothEmbedding
import Mathlib.Geometry.Manifold.SmoothApprox
import Mathlib.MeasureTheory.Function.Jacobian
import Mathlib.Topology.MetricSpace.HausdorffDimension

/-!
# S1-M-255 / THM-M-0594: Whitney embedding theorem

This Stage1 artifact records the Lean 4 boundary for the Whitney embedding
theorem.  The pinned mathlib revision contains a checked compact version:
every compact finite-dimensional real smooth manifold has a smooth closed
embedding into some finite-dimensional Euclidean space, with injective
manifold derivative at every point.

The general noncompact weak Whitney theorem is mentioned as a TODO in mathlib's
source and is not claimed here.  The declarations below therefore expose a
precise compact statement shape and a local wrapper around the checked mathlib
theorem.

Compact-anchor audit for `THM-M-0594.mathlib-compact-anchor`:
the repo-local Lake closure pins mathlib at revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, and the checked upstream theorem is
`exists_embedding_euclidean_of_compact` from
`Mathlib.Geometry.Manifold.WhitneyEmbedding`.
-/

noncomputable section

open scoped Manifold ContDiff Topology

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_255

universe uE uH uM

/-- Euclidean target space for Whitney embedding witnesses. -/
abbrev EuclideanTarget (n : ℕ) : Type :=
  EuclideanSpace ℝ (Fin n)

/--
Map-level predicate supplied by the compact Whitney embedding theorem in
mathlib: smoothness, closed topological embedding, and injective manifold
derivative at every source point.
-/
def IsWhitneySmoothClosedEmbedding
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    (n : ℕ) (e : M → EuclideanTarget n) : Prop :=
  ContMDiff I (𝓡 n) ∞ e ∧ Topology.IsClosedEmbedding e ∧
    ∀ x : M, Function.Injective (mfderiv I (𝓡 n) e x)

/--
Checked compact Whitney statement shape matching the current mathlib theorem.

This is the finite-dimensional compact real smooth-manifold version.  It does
not include the broader noncompact `σ`-compact/dimension-bound formulation.
-/
def StatementShape
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M] [IsManifold I ∞ M]
    [T2Space M] [CompactSpace M] : Prop :=
  ∃ (n : ℕ) (e : M → EuclideanTarget n), IsWhitneySmoothClosedEmbedding I n e

/-- The local statement shape unfolds to the expected Euclidean embedding witness. -/
theorem statementShape_iff_exists_smooth_closed_embedding
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M] [IsManifold I ∞ M]
    [T2Space M] [CompactSpace M] :
    StatementShape E H I M ↔
      ∃ (n : ℕ) (e : M → EuclideanTarget n), IsWhitneySmoothClosedEmbedding I n e :=
  Iff.rfl

/-- Checked wrapper around mathlib's compact Whitney embedding theorem. -/
theorem compactWhitneyEmbedding_mathlib_wrapper
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners ℝ E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M] [IsManifold I ∞ M]
    [T2Space M] [CompactSpace M] :
    StatementShape E H I M :=
  exists_embedding_euclidean_of_compact (I := I) (M := M)

/-! ## Compact mathlib anchor metadata -/

/-- Pinned mathlib revision audited for `THM-M-0594.mathlib-compact-anchor`. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- mathlib module supplying the checked compact Whitney embedding theorem. -/
def mathlibCompactAnchorModule : String :=
  "Mathlib.Geometry.Manifold.WhitneyEmbedding"

/-- Upstream theorem name used by the repo-local compact Whitney wrapper. -/
def mathlibCompactAnchorTheorem : String :=
  "exists_embedding_euclidean_of_compact"

/--
Compact anchor status: the theorem is in the repo-local Lake closure and is
used by `compactWhitneyEmbedding_mathlib_wrapper`; the broader Whitney slot
remains outside this compact anchor.
-/
def mathlibCompactAnchorStatus : List String := [
  "local_wrapper_upstream_mathlib",
  "compact finite-dimensional real smooth-manifold subtarget only",
  "full noncompact or dimension-bound Whitney target remains not_repo_local_closed"
]

/-! ## Scope decision metadata -/

/--
Stage1 scope decision for `THM-M-0594.scope-decision`.

The public Stage1 target should be the compact finite-dimensional theorem
already checked through pinned mathlib and exposed by `StatementShape`.  The
weak `σ`-compact theorem and dimension-bound Whitney theorem remain broader
targets, not the current completed Stage1 boundary.
-/
def stage1ScopeDecision : String :=
  "compact finite-dimensional Whitney embedding via StatementShape"

/-- Broader Whitney variants intentionally excluded from the current closed Stage1 target. -/
def excludedTerminalScopes : List String := [
  "weak sigma-compact Whitney embedding theorem",
  "dimension-bound Whitney embedding theorem",
  "noncompact full Whitney embedding theorem"
]

/--
Reason the excluded scopes remain open: the pinned mathlib file records them as
TODO-level or broader than the compact theorem, and no repo-local Lean terminal
proof for those variants is imported, wrapped, and validated here.
-/
def excludedScopeStatus : List String := [
  "not_repo_local_closed",
  "formalization_debt",
  "requires noncompact audit before any completion claim"
]

/-! ## Noncompact audit metadata -/

/--
Audit conclusion for `THM-M-0594.noncompact-audit`.

The pinned mathlib source has a checked compact Whitney theorem but records the
weak `σ`-compact Whitney embedding theorem as TODO-level work.  This artifact
therefore does not claim the noncompact theorem as repo-local closed.
-/
def noncompactAuditConclusion : List String := [
  "weak sigma-compact Whitney embedding remains TODO in Mathlib.Geometry.Manifold.WhitneyEmbedding",
  "no repo-local Lean terminal theorem for the noncompact weak Whitney target is imported or wrapped",
  "current closed boundary remains the compact StatementShape only",
  "noncompact and dimension-bound targets remain not_repo_local_closed / formalization_debt"
]

/-- Checked mathlib APIs relevant to the noncompact Whitney route. -/
def noncompactAuditMathlibAnchors : List String := [
  "SmoothBumpCovering.exists_immersion_euclidean",
  "SmoothBumpCovering.exists_isSubordinate",
  "MeasureTheory.addHaar_image_eq_zero_of_det_fderivWithin_eq_zero",
  "dimH",
  "MeasureTheory.Measure.hausdorffMeasure",
  "LipschitzWith.dimH_image_le",
  "ContDiffOn.dimH_image_le",
  "ContDiff.dense_compl_range_of_finrank_lt_finrank",
  "SigmaCompactSpace",
  "IsSigmaCompact",
  "ChartedSpace.secondCountable_of_sigmaCompact",
  "Continuous.exists_contMDiff_approx",
  "Manifold.IsSmoothEmbedding"
]

/--
Missing bridge classes for the weak noncompact theorem.

These are not missing because the names are absent from mathlib; rather, the
currently checked APIs are not yet connected into a theorem
`σ`-compact `m`-manifold embeds in `EuclideanSpace ℝ (Fin (2*m+1))`.
-/
def noncompactAuditBlockers : List String := [
  "global weak Whitney statement over sigma-compact manifolds is absent",
  "finite-dimensional manifold dimension parameter is not connected here to a 2*m+1 target bound",
  "Hausdorff-dimension/Sard estimates are Euclidean-source APIs, not a completed manifold projection theorem here",
  "properness or closed-embedding upgrade for noncompact exhaustions is not repo-local integrated",
  "SmoothEmbedding API still has proof_wanted bridges, so this artifact keeps the explicit witness predicate"
]

/--
Repo-local integration-debt gate for the noncompact audit.

No external Lean 4 proof of the weak Whitney theorem was found and left as
anchor-only evidence.  If one is later found, it must be pinned, imported, and
checked locally, or recorded as a concrete integration blocker before any
completion claim.
-/
def noncompactAuditIntegrationDebtGate : String :=
  "passed: no anchor-only external Lean 4 completion evidence is claimed"

/-! ## Smooth-embedding API bridge decision -/

/--
Decision for `THM-M-0594.smooth-embedding-api`.

Keep the Whitney witness predicate as the terminal local API for this artifact.
The current mathlib `Manifold.IsSmoothEmbedding` structure packages an
`IsImmersion` and an `IsEmbedding`; this file can project the topological
embedding component from the closed embedding witness, but it does not contain
a checked bridge from the pointwise injective `mfderiv` field used by
`exists_embedding_euclidean_of_compact` to `Manifold.IsImmersion`.
-/
def smoothEmbeddingApiDecision : String :=
  "do not bridge IsWhitneySmoothClosedEmbedding to Manifold.IsSmoothEmbedding in this pass"

/-- Checked and missing components for a future `Manifold.IsSmoothEmbedding` bridge. -/
def smoothEmbeddingApiBridgeAudit : List String := [
  "checked: IsWhitneySmoothClosedEmbedding projects ContMDiff",
  "checked: IsWhitneySmoothClosedEmbedding projects Topology.IsClosedEmbedding",
  "checked: Topology.IsClosedEmbedding projects Topology.IsEmbedding",
  "checked: IsWhitneySmoothClosedEmbedding projects pointwise injective mfderiv",
  "open: no repo-local theorem here converts ContMDiff plus pointwise injective mfderiv into Manifold.IsImmersion",
  "open: audited SmoothEmbedding.lean still contains proof_wanted bridge lemmas",
  "decision: keep the explicit witness predicate until the immersion/SmoothEmbedding API bridge validates locally"
]

/--
Repo-local integration-debt gate for the smooth-embedding API child.

No external Lean proof of the missing bridge is claimed.  A future completion
must add a checked local theorem, update the pinned mathlib revision to one
where the bridge exists, or record a concrete integration blocker.
-/
def smoothEmbeddingApiIntegrationDebtGate : String :=
  "passed: no anchor-only SmoothEmbedding bridge evidence is claimed"

/-! ## Theorem-tree backfill metadata -/

/--
Package-level theorem tree for `THM-M-0594.theorem-tree`.

This is a checked repo-local inventory, not a completion claim for the broad
Whitney theorem.  It records all public package ids that a later serial
integrator can merge into the blueprint while keeping the compact wrapper and
the broader noncompact/dimension-bound debts separate.
-/
def theoremTreePackages : List String := [
  "WE-P00.statement_normalization: freeze universes, model spaces, model-with-corners, charted manifold hypotheses, compact/T2 hypotheses, Euclidean target, smoothness, closed embedding, and derivative-injectivity predicates",
  "WE-P01.compact_mathlib_wrapper: expose the checked compact mathlib theorem through StatementShape and local witness projections",
  "WE-P02.bump_cover_substrate: audit SmoothBumpCovering, subordinate bump data, finite covers, and immersion construction used in the compact proof substrate",
  "WE-P03.closed_embedding_branch: separate the topological embedding and compact/T2 closed-image branch",
  "WE-P04.immersion_branch: track the mfderiv injectivity branch and future bridge to Manifold.IsImmersion",
  "WE-P05.dimension_bound_branch: decide whether the public terminal target is existence of some finite target, a 2*m+1 weak bound, or a sharper Whitney bound",
  "WE-P06.noncompact_branch: formulate or import the sigma-compact weak Whitney theorem and the Sard/Hausdorff-dimension infrastructure it needs",
  "WE-P07.smooth_embedding_api_bridge: decide whether to package witnesses using the local predicate, mathlib Manifold.IsSmoothEmbedding, or both",
  "WE-P08.repo_local_closure_gate: require local proof body, local wrapper around pinned mathlib, or pinned external dependency before any completion claim"
]

/--
Leaf-level theorem tree for `THM-M-0594.theorem-tree`.

Leaves marked `checked` are covered by declarations or metadata in this file
and by the required local Lean validation command.  Leaves marked `unchecked`
are preserved as future M0387-level work items; they are not completed by this
metadata backfill.
-/
def theoremTreeLeaves : List String := [
  "WE-L001 [checked] WE-P00: define EuclideanTarget n as EuclideanSpace R (Fin n)",
  "WE-L002 [checked] WE-P00: define IsWhitneySmoothClosedEmbedding as smooth plus closed embedding plus injective mfderiv",
  "WE-L003 [checked] WE-P00: define compact StatementShape with finite-dimensional real model, IsManifold, T2, and CompactSpace hypotheses",
  "WE-L004 [checked] WE-P00: prove statementShape_iff_exists_smooth_closed_embedding by definitional equality",
  "WE-L005 [checked] WE-P01: wrap exists_embedding_euclidean_of_compact as compactWhitneyEmbedding_mathlib_wrapper",
  "WE-L006 [checked] WE-P01: project ContMDiff from an IsWhitneySmoothClosedEmbedding witness",
  "WE-L007 [checked] WE-P01: project Topology.IsClosedEmbedding from an IsWhitneySmoothClosedEmbedding witness",
  "WE-L008 [checked] WE-P01: project Topology.IsEmbedding from the closed-embedding witness",
  "WE-L009 [checked] WE-P01: project pointwise injective mfderiv from an IsWhitneySmoothClosedEmbedding witness",
  "WE-L010 [checked] WE-P01: retain checked metadata and #check probes for the compact mathlib anchor and adjacent APIs",
  "WE-L011 [unchecked] WE-P01: expand the upstream compact theorem proof body into a public proof tree aligned with mathlib source",
  "WE-L012 [unchecked] WE-P01: record a stable theorem-level audit table for all compact-wrapper dependencies",
  "WE-L013 [unchecked] WE-P01: decide whether the compact wrapper alone is the public terminal Stage1 target",
  "WE-L014 [unchecked] WE-P01: add a reader-facing compact-subtarget proof-flow paragraph in the public merge target",
  "WE-L015 [unchecked] WE-P01: document the proof-body boundary between local wrapper and pinned mathlib theorem",
  "WE-L016 [unchecked] WE-P01: confirm future mathlib revisions have not changed the compact theorem signature before upgrading pins",
  "WE-L017 [unchecked] WE-P01: add an import-aggregator decision outside this worker's write scope if the integrator wants public imports",
  "WE-L018 [unchecked] WE-P01: synchronize compact-wrapper status into the public checklist after serial integration",
  "WE-L019 [unchecked] WE-P01: keep the compact wrapper distinct from the broad Whitney root in public summaries",
  "WE-L020 [unchecked] WE-P02: expand the finite smooth bump-cover construction into a public proof tree aligned with mathlib source lemmas",
  "WE-L021 [unchecked] WE-P02: audit partition-of-unity prerequisites for compact real smooth manifolds",
  "WE-L022 [unchecked] WE-P02: identify the SmoothBumpCovering object and its finite index set in the compact proof",
  "WE-L023 [unchecked] WE-P02: record the subordinate bump functions and their support/local-finiteness obligations",
  "WE-L024 [unchecked] WE-P02: isolate the local chart functions used to build Euclidean coordinate components",
  "WE-L025 [unchecked] WE-P02: verify the smoothness budget for each finite component map",
  "WE-L026 [unchecked] WE-P02: connect local bump data to the global finite Euclidean target map",
  "WE-L027 [unchecked] WE-P02: record the compactness step that makes the bump cover finite",
  "WE-L028 [unchecked] WE-P02: audit the target dimension produced by the finite cover construction",
  "WE-L029 [unchecked] WE-P02: state the exact blocker for upgrading bump-cover metadata into a local proof body",
  "WE-L030 [unchecked] WE-P03: package the compact/T2 closed-embedding branch independently of the mathlib theorem body",
  "WE-L031 [unchecked] WE-P03: separate topological embedding from closed-image obligations",
  "WE-L032 [unchecked] WE-P03: audit the injectivity proof branch for the compact witness map",
  "WE-L033 [unchecked] WE-P03: audit continuity and induced-topology obligations for the embedding branch",
  "WE-L034 [unchecked] WE-P03: record the compact-domain to closed-image argument under T2 target hypotheses",
  "WE-L035 [unchecked] WE-P03: decide whether a reusable closed-embedding lemma should be added locally",
  "WE-L036 [unchecked] WE-P03: connect Topology.IsClosedEmbedding to Topology.IsEmbedding in public theorem-tree prose",
  "WE-L037 [unchecked] WE-P03: verify the target Euclidean space satisfies the required separation hypotheses",
  "WE-L038 [unchecked] WE-P03: audit whether closed embedding is stronger than the public Stage1 target needs",
  "WE-L039 [unchecked] WE-P03: preserve the closed-embedding branch as unchecked until proof-body expansion validates",
  "WE-L040 [unchecked] WE-P04: expand the mfderiv injectivity branch through chart derivatives and kernel-zero lemmas",
  "WE-L041 [unchecked] WE-P04: record the chart-level derivative statement used by the compact proof",
  "WE-L042 [unchecked] WE-P04: audit how bump-cover components separate tangent vectors",
  "WE-L043 [unchecked] WE-P04: isolate local finite-dimensional linear algebra obligations",
  "WE-L044 [unchecked] WE-P04: connect mfderiv injectivity to a future Manifold.IsImmersion bridge",
  "WE-L045 [unchecked] WE-P04: decide whether derivative injectivity is terminal API or intermediate evidence",
  "WE-L046 [unchecked] WE-P04: verify smoothness hypotheses needed for mfderiv API calls",
  "WE-L047 [unchecked] WE-P04: audit source tangent-space model assumptions",
  "WE-L048 [unchecked] WE-P04: document any universe/model-with-corners constraints that affect immersion packaging",
  "WE-L049 [unchecked] WE-P04: preserve the immersion branch as unchecked until a local bridge theorem validates",
  "WE-L050 [unchecked] WE-P05: choose the public dimension convention: existence of some finite n, 2*m+1, or sharper Whitney bound",
  "WE-L051 [unchecked] WE-P05: add a dimension-indexed statement if the Stage1 public target requires explicit source dimension",
  "WE-L052 [unchecked] WE-P05: identify the formal source-dimension parameter available for finite-dimensional manifolds",
  "WE-L053 [unchecked] WE-P05: connect manifold model-space finrank to any Euclidean target bound",
  "WE-L054 [unchecked] WE-P05: decide whether compact mathlib's unspecified finite n suffices for Stage1 closure",
  "WE-L055 [unchecked] WE-P05: audit whether mathlib has a checked 2*m+1 Whitney target theorem in a later pinned revision",
  "WE-L056 [unchecked] WE-P05: record the blocker if a dimension-bound theorem exists externally but cannot be integrated",
  "WE-L057 [unchecked] WE-P05: state how target-dimension choices affect the public theorem wording",
  "WE-L058 [unchecked] WE-P05: update the local StatementShape only after a dimension-bound statement validates",
  "WE-L059 [unchecked] WE-P05: keep dimension-bound claims out of completed status until pin/import/check closure",
  "WE-L060 [unchecked] WE-P06: formalize or import sigma-compact smooth manifold hypotheses for the weak noncompact theorem",
  "WE-L061 [unchecked] WE-P06: provide or pin Sard/Hausdorff-dimension infrastructure needed by mathlib's TODO",
  "WE-L062 [unchecked] WE-P06: connect IsSigmaCompact or SigmaCompactSpace to the needed countable exhaustion",
  "WE-L063 [unchecked] WE-P06: audit second-countability consequences for sigma-compact charted manifolds",
  "WE-L064 [unchecked] WE-P06: bridge Euclidean Hausdorff-dimension image estimates to manifold charts",
  "WE-L065 [unchecked] WE-P06: prove or import the projection-avoidance argument for generic Euclidean maps",
  "WE-L066 [unchecked] WE-P06: construct a noncompact properness or closed-embedding upgrade",
  "WE-L067 [unchecked] WE-P06: connect continuous approximation to ContMDiff approximation where needed",
  "WE-L068 [unchecked] WE-P06: search external Lean 4 sources for a terminal weak Whitney theorem at a pin",
  "WE-L069 [unchecked] WE-P06: keep the noncompact branch not_repo_local_closed until a terminal theorem validates",
  "WE-L070 [unchecked] WE-P07: bridge the local witness predicate to mathlib Manifold.IsSmoothEmbedding once immersion API blockers close",
  "WE-L071 [unchecked] WE-P07: add or import a theorem converting ContMDiff plus pointwise injective mfderiv to Manifold.IsImmersion",
  "WE-L072 [unchecked] WE-P07: package the existing Topology.IsEmbedding projection with the immersion proof",
  "WE-L073 [unchecked] WE-P07: decide whether Manifold.IsSmoothEmbedding should replace or supplement the local witness predicate",
  "WE-L074 [unchecked] WE-P07: audit SmoothEmbedding API placeholder status in the pinned mathlib revision",
  "WE-L075 [unchecked] WE-P07: update #check probes for any new bridge theorem before claiming closure",
  "WE-L076 [unchecked] WE-P07: add a local wrapper theorem for smooth-embedding packaging only after all fields validate",
  "WE-L077 [unchecked] WE-P07: record a concrete blocker if the bridge theorem exists externally but cannot be integrated",
  "WE-L078 [unchecked] WE-P07: keep the bridge branch separate from compact existence closure",
  "WE-L079 [unchecked] WE-P07: synchronize public API wording after serial integration",
  "WE-L080 [unchecked] WE-P08: replace the compact-only wrapper with a terminal root theorem or pinned external closure if available",
  "WE-L081 [unchecked] WE-P08: public blueprint/todo/README synchronization by a later integrator after closure conditions are met"
]

/-- Leaf ids whose local declarations or metadata are checked by this file. -/
def theoremTreeCheckedLeaves : List String := [
  "WE-L001",
  "WE-L002",
  "WE-L003",
  "WE-L004",
  "WE-L005",
  "WE-L006",
  "WE-L007",
  "WE-L008",
  "WE-L009",
  "WE-L010"
]

/-- Leaf ids intentionally preserved as unchecked future work. -/
def theoremTreeUncheckedLeaves : List String := [
  "WE-L011",
  "WE-L012",
  "WE-L013",
  "WE-L014",
  "WE-L015",
  "WE-L016",
  "WE-L017",
  "WE-L018",
  "WE-L019",
  "WE-L020",
  "WE-L021",
  "WE-L022",
  "WE-L023",
  "WE-L024",
  "WE-L025",
  "WE-L026",
  "WE-L027",
  "WE-L028",
  "WE-L029",
  "WE-L030",
  "WE-L031",
  "WE-L032",
  "WE-L033",
  "WE-L034",
  "WE-L035",
  "WE-L036",
  "WE-L037",
  "WE-L038",
  "WE-L039",
  "WE-L040",
  "WE-L041",
  "WE-L042",
  "WE-L043",
  "WE-L044",
  "WE-L045",
  "WE-L046",
  "WE-L047",
  "WE-L048",
  "WE-L049",
  "WE-L050",
  "WE-L051",
  "WE-L052",
  "WE-L053",
  "WE-L054",
  "WE-L055",
  "WE-L056",
  "WE-L057",
  "WE-L058",
  "WE-L059",
  "WE-L060",
  "WE-L061",
  "WE-L062",
  "WE-L063",
  "WE-L064",
  "WE-L065",
  "WE-L066",
  "WE-L067",
  "WE-L068",
  "WE-L069",
  "WE-L070",
  "WE-L071",
  "WE-L072",
  "WE-L073",
  "WE-L074",
  "WE-L075",
  "WE-L076",
  "WE-L077",
  "WE-L078",
  "WE-L079",
  "WE-L080",
  "WE-L081"
]

/--
Integration-debt gate for the theorem-tree backfill.

The tree inventory is locally checked as metadata, but the broad Whitney root
remains `not_repo_local_closed` / `formalization_debt`; no completed state is
claimed from anchor-only external evidence.
-/
def theoremTreeIntegrationDebtGate : String :=
  "passed for metadata backfill; broad root remains not_repo_local_closed / formalization_debt"

/-! ## Full-root formalization-debt gate -/

/--
Debt gate for `THM-M-0594.debt`.

The compact wrapper is locally checked, but it is not a closure claim for every
standard Whitney embedding formulation.  Until a chosen terminal root statement
for the public theorem is present in this repo and validates with the local
Lean command, the full root remains explicitly open as formalization debt.
-/
def fullRootFormalizationDebtGate : List String := [
  "full root status: not_repo_local_closed",
  "full root debt type: formalization_debt",
  "closed subtarget: compact StatementShape via compactWhitneyEmbedding_mathlib_wrapper",
  "not closed here: weak sigma-compact Whitney embedding theorem",
  "not closed here: dimension-bound Whitney embedding theorem",
  "completion gate: chosen terminal statement must validate repo-locally before public completion",
  "integration gate: no repo_local_integration_debt is carried as completed evidence"
]

/-! ## Future external-proof integration gate -/

/--
Integration gate for `THM-M-0594.integration-gate`.

Any future external Lean 4 proof of a broader Whitney embedding target must
enter the repo-local validation closure before it can support a completion
claim.  Anchor-only evidence is not enough: the proof must be pinned, imported,
and checked locally, or its failure to integrate must be recorded as a concrete
blocker while the corresponding target remains open.
-/
def futureExternalProofIntegrationGate : List String := [
  "future external Lean 4 proof requirement: pin/import/check in this repo before completion",
  "accepted completed states: local_proof_body, local_wrapper_upstream_mathlib, external_upstream_pinned",
  "rejected completed evidence: external_upstream_anchor_only",
  "if pin/import/check fails: record the exact dependency, toolchain, license, API, or theorem-shape blocker",
  "until integration validates locally or a blocker is recorded, the affected Whitney target remains not_repo_local_closed",
  "no completed state may retain repo_local_integration_debt"
]

/-! ## Shared import-aggregator decision -/

/--
Machine-readable decision for `THM-M-0594.import-aggregator`.

The serialized integrator, not this child worker, owns any actual edit to a
shared import aggregator.
-/
inductive SharedImportAggregatorDecision where
  /-- Add the validated Stage1 module to the shared aggregator in a serialized patch. -/
  | addStage1Module
  /-- Keep the file as a directly validated standalone Stage1 artifact. -/
  | keepStandalone
deriving DecidableEq, Repr

/-- Integration-ready status for child `S1-M-255-C011`. -/
structure SharedImportAggregatorDecisionStatus where
  modulePath : String
  candidateImportLine : String
  targetAggregator : String
  moduleValidatedLocally : Bool
  sharedAggregatorEditedInChild : Bool
  recommendedDecision : SharedImportAggregatorDecision
  terminalTheoremCompletedByImport : Bool
  reason : String
deriving DecidableEq, Repr

/--
Current child recommendation: keep this Whitney Stage1 module as a directly
validated standalone artifact unless and until a serialized project policy adds
Stage1 files to the default Lean import surface.

The candidate import exposes the compact mathlib wrapper and audit metadata;
it does not close the weak noncompact or dimension-bound Whitney theorem.
-/
def sharedImportAggregatorDecisionStatus :
    SharedImportAggregatorDecisionStatus where
  modulePath := "AwesomeTheorems/Stage1/S1_M_255.lean"
  candidateImportLine := "import AwesomeTheorems.Stage1.S1_M_255"
  targetAggregator := "Formalizations/Lean/AwesomeTheorems.lean"
  moduleValidatedLocally := true
  sharedAggregatorEditedInChild := false
  recommendedDecision := .keepStandalone
  terminalTheoremCompletedByImport := false
  reason :=
    "Keep the validated Whitney Stage1 artifact standalone for now; add the " ++
    "candidate import only in a later serialized Stage1 import-policy patch, " ++
    "and do not treat the import as completion of the noncompact or " ++
    "dimension-bound Whitney theorem."

/--
Checked local status: the import-aggregator decision is recorded for a later
serialized integration patch, while the shared aggregator remains untouched in
this pass.
-/
theorem shared_import_aggregator_decision_local_checked :
    sharedImportAggregatorDecisionStatus.modulePath =
        "AwesomeTheorems/Stage1/S1_M_255.lean" ∧
      sharedImportAggregatorDecisionStatus.candidateImportLine =
        "import AwesomeTheorems.Stage1.S1_M_255" ∧
      sharedImportAggregatorDecisionStatus.targetAggregator =
        "Formalizations/Lean/AwesomeTheorems.lean" ∧
      sharedImportAggregatorDecisionStatus.moduleValidatedLocally = true ∧
      sharedImportAggregatorDecisionStatus.sharedAggregatorEditedInChild = false ∧
      sharedImportAggregatorDecisionStatus.recommendedDecision =
        SharedImportAggregatorDecision.keepStandalone ∧
      sharedImportAggregatorDecisionStatus.terminalTheoremCompletedByImport = false :=
  by
    simp [sharedImportAggregatorDecisionStatus]

/-- Project smoothness out of a Whitney witness. -/
theorem whitneyWitness_contMDiff
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {n : ℕ} {e : M → EuclideanTarget n} (he : IsWhitneySmoothClosedEmbedding I n e) :
    ContMDiff I (𝓡 n) ∞ e :=
  he.1

/-- Project the closed topological embedding data out of a Whitney witness. -/
theorem whitneyWitness_isClosedEmbedding
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {n : ℕ} {e : M → EuclideanTarget n} (he : IsWhitneySmoothClosedEmbedding I n e) :
    Topology.IsClosedEmbedding e :=
  he.2.1

/-- Project the underlying topological embedding out of a Whitney witness. -/
theorem whitneyWitness_isEmbedding
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {n : ℕ} {e : M → EuclideanTarget n} (he : IsWhitneySmoothClosedEmbedding I n e) :
    Topology.IsEmbedding e :=
  (whitneyWitness_isClosedEmbedding he).isEmbedding

/-- Project the injective manifold-derivative data out of a Whitney witness. -/
theorem whitneyWitness_injective_mfderiv
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners ℝ E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    {n : ℕ} {e : M → EuclideanTarget n} (he : IsWhitneySmoothClosedEmbedding I n e)
    (x : M) :
    Function.Injective (mfderiv I (𝓡 n) e x) :=
  he.2.2 x

/-! ## Audit probes retained in the checked file. -/

#check StatementShape
#check IsWhitneySmoothClosedEmbedding
#check statementShape_iff_exists_smooth_closed_embedding
#check compactWhitneyEmbedding_mathlib_wrapper
#check pinnedMathlibRevision
#check mathlibCompactAnchorModule
#check mathlibCompactAnchorTheorem
#check mathlibCompactAnchorStatus
#check stage1ScopeDecision
#check excludedTerminalScopes
#check excludedScopeStatus
#check noncompactAuditConclusion
#check noncompactAuditMathlibAnchors
#check noncompactAuditBlockers
#check noncompactAuditIntegrationDebtGate
#check smoothEmbeddingApiDecision
#check smoothEmbeddingApiBridgeAudit
#check smoothEmbeddingApiIntegrationDebtGate
#check theoremTreePackages
#check theoremTreeLeaves
#check theoremTreeCheckedLeaves
#check theoremTreeUncheckedLeaves
#check theoremTreeIntegrationDebtGate
#check fullRootFormalizationDebtGate
#check futureExternalProofIntegrationGate
#check SharedImportAggregatorDecision
#check SharedImportAggregatorDecisionStatus
#check sharedImportAggregatorDecisionStatus
#check shared_import_aggregator_decision_local_checked
#check whitneyWitness_contMDiff
#check whitneyWitness_isClosedEmbedding
#check whitneyWitness_isEmbedding
#check whitneyWitness_injective_mfderiv
#check exists_embedding_euclidean_of_compact
#check SmoothBumpCovering.exists_immersion_euclidean
#check SmoothBumpCovering.exists_isSubordinate
#check MeasureTheory.addHaar_image_eq_zero_of_det_fderivWithin_eq_zero
#check dimH
#check MeasureTheory.Measure.hausdorffMeasure
#check LipschitzWith.dimH_image_le
#check ContDiffOn.dimH_image_le
#check ContDiff.dense_compl_range_of_finrank_lt_finrank
#check SigmaCompactSpace
#check IsSigmaCompact
#check ChartedSpace.secondCountable_of_sigmaCompact
#check Continuous.exists_contMDiff_approx
#check Manifold.IsSmoothEmbedding
#check Manifold.IsImmersion
#check Topology.IsClosedEmbedding
#check Topology.IsEmbedding
#check mfderiv

end S1_M_255
end Stage1
end AwesomeTheorems
