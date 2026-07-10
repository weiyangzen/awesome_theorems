import Mathlib.Geometry.Manifold.PoincareConjecture

/-!
# S1-M-114 / THM-M-0579: Poincare conjecture statement boundary

This Stage1 artifact records a compilable Lean 4 statement shape for the
3-dimensional topological Poincare conjecture:

* the model space is `EuclideanSpace ℝ (Fin 3)`;
* the target sphere is the unit sphere in `EuclideanSpace ℝ (Fin 4)`;
* the hypotheses match mathlib's current statement file:
  `T2Space`, `ChartedSpace`, `SimplyConnectedSpace`, and `CompactSpace`.

Mathlib's `Geometry.Manifold.PoincareConjecture` contains `proof_wanted`
declarations for the topological and smooth 3-dimensional Poincare conjectures.
Those declarations are checked for well-formedness but discarded by the
`proof_wanted` elaborator, so they are not usable theorem anchors.  This file
therefore does not claim proof closure.

The audited local dependency pin is mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.
-/

noncomputable section

universe u

namespace AwesomeTheorems.Stage1.S1_M_114

/-- The 3-dimensional Euclidean model space used by the topological manifold charts. -/
abbrev ModelSpace3 : Type :=
  EuclideanSpace ℝ (Fin 3)

/-- The unit 3-sphere, represented as a subtype of 4-dimensional Euclidean space. -/
abbrev ThreeSphere : Set (EuclideanSpace ℝ (Fin 4)) :=
  Metric.sphere (0 : EuclideanSpace ℝ (Fin 4)) (1 : ℝ)

/--
The local statement shape for the topological 3-dimensional Poincare conjecture.

This proposition is intentionally not proved here.  It mirrors the source
mathematical statement and mathlib's checked `proof_wanted` signature without
turning that signature into an unsupported proof anchor or fake wrapper theorem.
-/
def StatementShape : Prop :=
  ∀ (M : Type u) [TopologicalSpace M] [T2Space M] [ChartedSpace ModelSpace3 M]
    [SimplyConnectedSpace M] [CompactSpace M], Nonempty (M ≃ₜ ThreeSphere)

/--
A named predicate wrapper for the exact topological 3-manifold hypotheses used
by `StatementShape`.  This is a documentation and API boundary only; it does
not add a proof of the Poincare conjecture.
-/
def ClosedTopologicalThreeManifold (M : Type u) [TopologicalSpace M] : Prop :=
  Nonempty (T2Space M) ∧ Nonempty (ChartedSpace ModelSpace3 M) ∧
    Nonempty (SimplyConnectedSpace M) ∧ Nonempty (CompactSpace M)

/-- The same statement shape using the named closed-topological-3-manifold wrapper. -/
def NamedStatementShape : Prop :=
  ∀ (M : Type u) [TopologicalSpace M],
    ClosedTopologicalThreeManifold M → Nonempty (M ≃ₜ ThreeSphere)

/--
The named wrapper is propositionally equivalent to the direct mathlib-style
typeclass signature.  This keeps the public statement-choice branch integration
ready without changing the proof status.
-/
theorem namedStatementShape_iff_statementShape : NamedStatementShape.{u} ↔ StatementShape.{u} := by
  constructor
  · intro h M _ _ _ _ _
    exact h M ⟨⟨inferInstance⟩, ⟨inferInstance⟩, ⟨inferInstance⟩, ⟨inferInstance⟩⟩
  · intro h M _ hM
    rcases hM with ⟨hT2, hCharted, hSimplyConnected, hCompact⟩
    letI : T2Space M := hT2.some
    letI : ChartedSpace ModelSpace3 M := hCharted.some
    letI : SimplyConnectedSpace M := hSimplyConnected.some
    letI : CompactSpace M := hCompact.some
    exact h M

/--
Public statement-boundary decision for `S1-M-114-public-004`.

The canonical public statement should keep mathlib's direct typeclass signature,
including `[ChartedSpace ModelSpace3 M]`.  The named
`ClosedTopologicalThreeManifold` predicate is retained as an integration-ready
documentation/API wrapper, with `namedStatementShape_iff_statementShape`
recording that it is propositionally equivalent to the direct signature.  This
decision does not claim proof closure for the Poincare conjecture.
-/
def publicStatementBoundaryDecision : List String := [
  "canonical public statement keeps mathlib's direct ChartedSpace ModelSpace3 M typeclass hypothesis",
  "ClosedTopologicalThreeManifold is a named documentation/API wrapper, not the canonical replacement statement",
  "namedStatementShape_iff_statementShape proves the wrapper and direct statement shapes are propositionally equivalent",
  "no proof closure or importable Poincare theorem anchor is claimed by this wrapper decision"
]

/--
Checked adjacent object-model fact: the target `ThreeSphere` has the expected
charted-space instance and compact-space instance in the local mathlib closure.
-/
def ThreeSphereObjectModel : Prop :=
  Nonempty (ChartedSpace ModelSpace3 ThreeSphere) ∧ CompactSpace ThreeSphere

theorem threeSphere_object_model : ThreeSphereObjectModel := by
  constructor
  · exact ⟨inferInstance⟩
  · infer_instance

/-- The target sphere is homeomorphic to itself; this is only a sanity wrapper. -/
theorem threeSphere_self_homeomorph : Nonempty (ThreeSphere ≃ₜ ThreeSphere) :=
  ⟨Homeomorph.refl ThreeSphere⟩

/-- Mathlib's `SimplyConnectedSpace` supplies the expected path-connectedness invariant. -/
theorem simplyConnected_implies_pathConnected
    (M : Type u) [TopologicalSpace M] [SimplyConnectedSpace M] :
    PathConnectedSpace M := by
  infer_instance

/-- The fundamental-groupoid formulation exposed by mathlib's simply-connected API. -/
theorem simplyConnected_fundamentalGroupoid_equiv_unit
    (M : Type u) [TopologicalSpace M] [SimplyConnectedSpace M] :
    Nonempty (FundamentalGroupoid M ≌ CategoryTheory.Discrete Unit) :=
  SimplyConnectedSpace.equiv_unit

/-- The pinned mathlib revision audited for this Stage1 Poincare boundary. -/
def pinnedMathlibRevision : String := "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Geometry.Manifold.PoincareConjecture",
  "Mathlib.Geometry.Manifold.Instances.Sphere",
  "Mathlib.AlgebraicTopology.FundamentalGroupoid.SimplyConnected",
  "Mathlib.Topology.Homotopy.Equiv",
  "Mathlib.Topology.Category.TopCat.Sphere",
  "Mathlib.Topology.Homotopy.HomotopyGroup",
  "Mathlib.AlgebraicTopology.SingularHomology.HomotopyInvariance"
]

/--
Source-level mathlib markers audited in `Mathlib.Geometry.Manifold.PoincareConjecture`.

These names appear as `proof_wanted` declarations in the pinned mathlib source,
not as importable theorem constants in this local environment.
-/
def mathlibProofWantedMarkers : List String := [
  "ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere",
  "SimplyConnectedSpace.nonempty_homeomorph_sphere_three",
  "SimplyConnectedSpace.nonempty_diffeomorph_sphere_three",
  "exists_homeomorph_isEmpty_diffeomorph_sphere_seven",
  "exists_open_nonempty_homeomorph_isEmpty_diffeomorph_euclideanSpace_four"
]

/--
Audit note for Batteries' `proof_wanted` elaborator.

`Batteries.Util.ProofWanted.elabProofWanted` elaborates the requested theorem
signature in a temporary environment and runs it under `withoutModifyingEnv`.
Thus the signature is checked during elaboration, but the resulting helper
axiom/theorem is discarded from the final environment.  In particular,
`SimplyConnectedSpace.nonempty_homeomorph_sphere_three` is source-level
statement-shape evidence only, not an importable theorem anchor.
-/
def batteriesProofWantedAudit : List String := [
  "Batteries.Util.ProofWanted.elabProofWanted",
  "withoutModifyingEnv",
  "signature elaboration check only",
  "discarded from final environment",
  "SimplyConnectedSpace.nonempty_homeomorph_sphere_three is not an importable proof anchor"
]

/-- Search terms that did not locate a terminal retained 3D Poincare theorem in mathlib. -/
def absentTerminalSearchTerms : List String := [
  "PoincareConjecture",
  "Poincare",
  "nonempty_homeomorph_sphere",
  "SimplyConnectedSpace.nonempty_homeomorph_sphere_three",
  "SimplyConnectedSpace.nonempty_diffeomorph_sphere_three",
  "three-dimensional Poincare conjecture",
  "Perelman",
  "Ricci flow",
  "geometrization"
]

/-- External Lean 4 repository audited as primary-source evidence for this slot. -/
def leanMillenniumPrizeProblemsRepository : String :=
  "https://github.com/lean-dojo/LeanMillenniumPrizeProblems"

/-- Pinned external revision audited for `Problems/Poincare/Millennium.lean`. -/
def leanMillenniumPrizeProblemsRevision : String :=
  "540da94826f70f3edf4d4fc66ce6cda20e903f61"

/-- External source file audited for Poincare-related Lean declarations. -/
def leanMillenniumPrizeProblemsPoincareFile : String :=
  "Problems/Poincare/Millennium.lean"

/-- Raw URL for the pinned external Poincare source audited in this child pass. -/
def leanMillenniumPrizeProblemsPoincareRawUrl : String :=
  "https://raw.githubusercontent.com/lean-dojo/LeanMillenniumPrizeProblems/" ++
    leanMillenniumPrizeProblemsRevision ++ "/Problems/Poincare/Millennium.lean"

/--
Retained external Lean 4 declarations found in the pinned
`LeanMillenniumPrizeProblems` Poincare source.

The proposition declarations restate Poincare-style statements.  The proof
bodies found in this file close only the dimension-0 generalized special case,
not the terminal 3-dimensional Poincare conjecture.
-/
def leanMillenniumPrizeProblemsPoincareDeclarations : List String := [
  "MillenniumPoincare.PoincareConjecture3 : Prop",
  "MillenniumPoincare.GeneralizedPoincareConjecture : Prop",
  "MillenniumPoincare.ContinuousMap.Homotopic.eq_of_discrete",
  "MillenniumPoincare.homotopyEquiv_nonempty_homeomorph_of_discrete",
  "MillenniumPoincare.generalizedPoincareConjecture_zero"
]

/-- External non-`sorry` proof bodies found during the primary-source audit. -/
def leanMillenniumPrizeProblemsNonSorryProofBodies : List String := [
  "MillenniumPoincare.ContinuousMap.Homotopic.eq_of_discrete",
  "MillenniumPoincare.homotopyEquiv_nonempty_homeomorph_of_discrete",
  "MillenniumPoincare.generalizedPoincareConjecture_zero"
]

/--
Classification of the pinned external Lean 4 Poincare source.

It contains retained statement declarations and retained non-`sorry` proof
bodies for a dimension-0 generalized special case, but no retained Lean theorem
proofing `PoincareConjecture3` or mathlib's 3-dimensional
`SimplyConnectedSpace.nonempty_homeomorph_sphere_three` statement.
-/
def leanMillenniumPrizeProblemsPoincareAuditClassification : String :=
  "retained declarations plus dimension-0 generalized special-case proof only; " ++
    "no terminal retained Lean 4 proof of the 3-dimensional Poincare conjecture"

/-- Whether the audited external source permits a theorem-completion claim here. -/
def leanMillenniumPrizeProblemsAllowsCompletionClaim : Bool := false

/--
Integration gate for `S1-M-114-public-006`.

No retained external Lean 4 proof of the terminal 3-dimensional Poincare
conjecture was found in the audited source, so there is no external theorem
body to pin/import/check and no concrete dependency/toolchain/license blocker
to record for such a body.  The only retained external proof bodies audited
close a dimension-0 generalized special case, which is outside the completion
target for this Stage1 item.
-/
def externalRetainedProofIntegrationGate : List String := [
  "no retained external Lean 4 proof of the terminal 3-dimensional Poincare conjecture was found",
  "no pin/import/check action is applicable for a terminal external proof body in this child",
  "no dependency/toolchain/license blocker is recorded because there is no terminal proof body to integrate",
  "dimension-0 generalized special-case proofs are not completion evidence for THM-M-0579",
  "no completed state may retain repo_local_integration_debt"
]

/-! ## Audit probes -/

#check StatementShape
#check ClosedTopologicalThreeManifold
#check NamedStatementShape
#check namedStatementShape_iff_statementShape
#check publicStatementBoundaryDecision
#check ThreeSphereObjectModel
#check threeSphere_object_model
#check threeSphere_self_homeomorph
#check simplyConnectedSpace_iff
#check SimplyConnectedSpace.equiv_unit
#check SimplyConnectedSpace.paths_homotopic
#check EuclideanSpace.instChartedSpaceSphere
#check EuclideanSpace.instIsManifoldSphere
#check pinnedMathlibRevision
#check mathlibAnchorModules
#check mathlibProofWantedMarkers
#check batteriesProofWantedAudit
#check absentTerminalSearchTerms
#check leanMillenniumPrizeProblemsRepository
#check leanMillenniumPrizeProblemsRevision
#check leanMillenniumPrizeProblemsPoincareFile
#check leanMillenniumPrizeProblemsPoincareRawUrl
#check leanMillenniumPrizeProblemsPoincareDeclarations
#check leanMillenniumPrizeProblemsNonSorryProofBodies
#check leanMillenniumPrizeProblemsPoincareAuditClassification
#check leanMillenniumPrizeProblemsAllowsCompletionClaim
#check externalRetainedProofIntegrationGate

end AwesomeTheorems.Stage1.S1_M_114
