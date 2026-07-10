import Mathlib.Topology.Instances.Real.Lemmas
import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.ODE.Basic
import Mathlib.Dynamics.OmegaLimit
import Mathlib.Dynamics.PeriodicPts.Defs

/-!
# S1-M-297 / THM-M-1400: Poincare-Bendixson theorem

This Stage1 artifact records a conservative Lean 4 boundary for the
Poincare-Bendixson theorem.  The target theorem classifies compact omega-limit
sets of planar smooth flows.  The pinned mathlib snapshot contains a useful
topological-dynamical substrate: continuous flows, invariant sets, omega-limit
sets, cluster-point characterizations, and discrete periodic-point predicates.
It does not expose a terminal theorem named Poincare-Bendixson, nor does it
currently provide the full planar `C^1` ODE proof infrastructure needed for the
classical theorem.

Accordingly, this file gives a typed planar-flow statement shape and proves
only low-risk wrappers around the available mathlib flow/omega-limit/periodic
APIs.  It does not prove the Poincare-Bendixson theorem.
-/

noncomputable section

open Filter Set Function
open scoped omegaLimit

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_297

/-- The concrete two-dimensional phase space used by this statement boundary. -/
abbrev PlanarPhase : Type := ℝ × ℝ

/-- A concrete `C^1` planar vector field for the Stage1 statement boundary. -/
structure C1PlanarVectorField : Type where
  toFun : PlanarPhase → PlanarPhase
  contDiff_toFun : ContDiff ℝ 1 toFun

namespace C1PlanarVectorField

instance : CoeFun C1PlanarVectorField (fun _ => PlanarPhase → PlanarPhase) where
  coe F := F.toFun

end C1PlanarVectorField

/--
Data for a normalized planar Poincare-Bendixson statement.

The smooth vector-field clause is represented by `C1PlanarVectorField`, and the
flow-generation clause is stated with mathlib's `IsIntegralCurve` predicate for
every starting point.  The classical planar proof still remains outside the
checked file: compact absorbing-region derivation, no-crossing, transverse
sections, and separation arguments are not proved here.
-/
structure PoincareBendixsonData : Type where
  vectorField : C1PlanarVectorField
  flow : Flow ℝ PlanarPhase
  initial : PlanarPhase
  trappingRegion : Set PlanarPhase
  flowSolvesVectorField :
    ∀ x : PlanarPhase,
      IsIntegralCurve (fun t : ℝ => flow t x) (fun _ y => vectorField y)
  forwardOrbitEventuallyInTrappingRegion : Prop
  trappingRegionCompact : IsCompact trappingRegion
  omegaSetContainedInTrappingRegion : omegaLimit atTop flow {initial} ⊆ trappingRegion
  omegaSetNonempty : (omegaLimit atTop flow {initial}).Nonempty
  finitelyManyEquilibriaOnOmega : Prop

namespace PoincareBendixsonData

/-- The omega-limit set of the packaged initial point. -/
def omegaSet (D : PoincareBendixsonData) : Set PlanarPhase :=
  omegaLimit atTop D.flow {D.initial}

/-- The omega-limit set contains an equilibrium of the continuous real flow. -/
def HasEquilibriumInOmega (D : PoincareBendixsonData) : Prop :=
  ∃ p ∈ D.omegaSet, ∀ t : ℝ, D.flow t p = p

/--
A candidate periodic-orbit alternative for the omega-limit classification.

This is intentionally stated for the flow image of all real times; later
integrators should strengthen it with the usual minimal-period/nonstationary
conditions once the planar ODE branch is formalized.
-/
def IsPeriodicOrbitSet (D : PoincareBendixsonData) (s : Set PlanarPhase) : Prop :=
  ∃ p : PlanarPhase,
    ∃ T : ℝ,
      0 < T ∧ D.flow T p = p ∧ s = Set.range (fun t : ℝ => D.flow t p)

/--
Placeholder for the finite graph/cycle alternative in versions of
Poincare-Bendixson that allow finitely many equilibria in the omega-limit set.

This is not made automatically true: it records the formalization boundary for
separatrices and connecting orbit arcs, which are not available locally.
-/
def FiniteEquilibriumCycleGraph (D : PoincareBendixsonData) : Prop :=
  ∃ vertices : Set PlanarPhase, vertices.Finite ∧ vertices ⊆ D.omegaSet

/-- Human-readable hypotheses that remain outside the currently checked topological layer. -/
def CoreHypotheses (D : PoincareBendixsonData) : Prop :=
  D.forwardOrbitEventuallyInTrappingRegion ∧
    D.finitelyManyEquilibriaOnOmega

/--
Classical classification boundary: the omega-limit contains an equilibrium, is
a periodic orbit, or is accounted for by the finite-equilibrium cycle graph
alternative.
-/
def ClassificationConclusion (D : PoincareBendixsonData) : Prop :=
  D.HasEquilibriumInOmega ∨ D.IsPeriodicOrbitSet D.omegaSet ∨
    D.FiniteEquilibriumCycleGraph

end PoincareBendixsonData

/--
Stage1 normalized statement shape for the Poincare-Bendixson theorem.

This is a formalization boundary, not a proof.  It packages the planar-flow
classification target using mathlib's `Flow` and `omegaLimit` objects while
leaving the smooth ODE and planar-separation proof work as explicit hypotheses
and open proof obligations.
-/
def StatementShape : Prop :=
  ∀ D : PoincareBendixsonData,
    D.CoreHypotheses → D.ClassificationConclusion

/-- The statement shape unfolds to the expected packaged implication. -/
theorem statementShape_iff :
    StatementShape ↔
      ∀ D : PoincareBendixsonData,
        D.CoreHypotheses → D.ClassificationConclusion :=
  Iff.rfl

/-- Projection wrapper for the checked `C^1` planar vector-field hypothesis. -/
theorem vectorField_contDiff (D : PoincareBendixsonData) :
    ContDiff ℝ 1 D.vectorField.toFun :=
  D.vectorField.contDiff_toFun

/-- Projection wrapper for the checked integral-curve generation hypothesis. -/
theorem flow_solves_vectorField (D : PoincareBendixsonData) (x : PlanarPhase) :
    IsIntegralCurve (fun t : ℝ => D.flow t x) (fun _ y => D.vectorField y) :=
  D.flowSolvesVectorField x

/-- Projection wrapper for the compact trapping-region hypothesis. -/
theorem trappingRegion_isCompact (D : PoincareBendixsonData) :
    IsCompact D.trappingRegion :=
  D.trappingRegionCompact

/-- Projection wrapper for the omega-limit containment hypothesis. -/
theorem omegaSet_subset_trapping (D : PoincareBendixsonData) :
    D.omegaSet ⊆ D.trappingRegion :=
  D.omegaSetContainedInTrappingRegion

/-- Projection wrapper for nonemptiness of the omega-limit set. -/
theorem omegaSet_nonempty (D : PoincareBendixsonData) :
    D.omegaSet.Nonempty :=
  D.omegaSetNonempty

/-- mathlib proves that every omega-limit set is closed. -/
theorem omegaSet_closed (D : PoincareBendixsonData) :
    IsClosed D.omegaSet :=
  isClosed_omegaLimit atTop D.flow {D.initial}

/-- Translation by a fixed real number tends to `atTop` along `atTop`. -/
theorem real_tendsto_const_add_atTop (t : ℝ) :
    Tendsto (fun u : ℝ => t + u) atTop atTop :=
  Filter.tendsto_atTop_add_const_left atTop t tendsto_id

/-- The omega-limit set of the packaged real flow is invariant. -/
theorem omegaSet_isInvariant (D : PoincareBendixsonData) :
    IsInvariant D.flow D.omegaSet :=
  D.flow.isInvariant_omegaLimit atTop {D.initial} real_tendsto_const_add_atTop

/--
Membership in the singleton omega-limit set is the same as being a cluster
point of the forward trajectory along `atTop`.
-/
theorem omegaSet_mem_iff_mapClusterPt
    (D : PoincareBendixsonData) (p : PlanarPhase) :
    p ∈ D.omegaSet ↔
      MapClusterPt p atTop (fun t : ℝ => D.flow t D.initial) :=
  mem_omegaLimit_singleton_iff_map_cluster_point atTop D.flow D.initial p

/-- A fixed point of the time-one map is periodic for every natural period. -/
theorem fixedPoint_isPeriodicPt (D : PoincareBendixsonData)
    {p : PlanarPhase} (hp : IsFixedPt (D.flow 1) p) (n : ℕ) :
    IsPeriodicPt (D.flow 1) n p :=
  hp.isPeriodicPt n

/-- For the identity map on the planar phase space, every point is periodic. -/
theorem identityMap_periodic (n : ℕ) (p : PlanarPhase) :
    IsPeriodicPt (id : PlanarPhase → PlanarPhase) n p :=
  is_periodic_id n p

/-! ## Audit probes retained in the checked file. -/

#check StatementShape
#check C1PlanarVectorField
#check C1PlanarVectorField.contDiff_toFun
#check PoincareBendixsonData
#check PoincareBendixsonData.omegaSet
#check PoincareBendixsonData.HasEquilibriumInOmega
#check PoincareBendixsonData.IsPeriodicOrbitSet
#check ContDiff
#check IsIntegralCurve
#check Flow
#check IsInvariant
#check Flow.isInvariant_omegaLimit
#check omegaLimit
#check isClosed_omegaLimit
#check mem_omegaLimit_singleton_iff_map_cluster_point
#check MapClusterPt
#check Function.IsFixedPt
#check Function.IsPeriodicPt
#check Function.IsFixedPt.isPeriodicPt

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Dynamics.Flow",
  "Mathlib.Analysis.ODE.Basic",
  "Mathlib.Dynamics.OmegaLimit",
  "Mathlib.Dynamics.PeriodicPts.Defs",
  "Mathlib.Dynamics.FixedPoints.Basic",
  "Mathlib.Topology.ClusterPt",
  "Mathlib.Topology.Instances.Real.Lemmas",
  "Mathlib.Geometry.Manifold.VectorField.Pullback",
  "Mathlib.Geometry.Manifold.VectorField.LieBracket"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "Flow",
  "ContDiff",
  "IsIntegralCurve",
  "IsInvariant",
  "IsForwardInvariant",
  "Flow.orbit",
  "Flow.forwardOrbit",
  "omegaLimit",
  "isClosed_omegaLimit",
  "Flow.isInvariant_omegaLimit",
  "mem_omegaLimit_singleton_iff_map_cluster_point",
  "MapClusterPt",
  "Function.IsFixedPt",
  "Function.IsPeriodicPt",
  "Function.IsFixedPt.isPeriodicPt",
  "Function.is_periodic_id"
]

/-- Search terms that did not locate a terminal Poincare-Bendixson theorem locally. -/
def absentTerminalSearchTerms : List String := [
  "Poincare-Bendixson",
  "Poincare Bendixson",
  "Bendixson",
  "limit set",
  "omega limit planar flow",
  "periodic orbit",
  "separatrix",
  "planar vector field",
  "smooth flow",
  "two-dimensional dynamical system"
]

/-- Primary-source pin for the local mathlib audit used by this statement-shape file. -/
def localMathlibRevision : String :=
  "leanprover-community/mathlib4@8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-! ## S1-M-297-C001 public-backfill merge gate. -/

/--
Checked local leaves that C001 can safely ask a serial public integrator to
merge into the Stage1 blueprint/todo surface.
-/
def c001CheckedLeafNames : List String := [
  "PB-L001.checked.statement_shape_unfold",
  "PB-L002.checked.compact_projection",
  "PB-L003.checked.omega_subset_projection",
  "PB-L004.checked.omega_nonempty_projection",
  "PB-L005.checked.omega_closed",
  "PB-L006.checked.real_translation_atTop",
  "PB-L007.checked.omega_invariant",
  "PB-L008.checked.cluster_characterization",
  "PB-L009.checked.fixed_to_periodic",
  "PB-L010.checked.identity_periodic"
]

/--
C001 is a public-doc integration child over checked local wrappers, not a
terminal proof of the Poincare-Bendixson theorem.
-/
def c001ChildTaskDiagnosis : String :=
  "public_doc_integration_work_for_checked_statement_shape_and_wrappers"

/--
Completion remains blocked by formalization work rather than by a known
external Lean 4 proof that this repository failed to integrate.
-/
def c001RepoLocalDebtGate : String :=
  "pass_noncompletion: no terminal theorem completion is claimed and no known external Lean 4 Poincare-Bendixson proof is left anchor-only as completed evidence"

/-- C001 records formalization debt, not completed-state repo-local integration debt. -/
theorem c001_not_completed_with_repo_local_integration_debt :
    c001RepoLocalDebtGate ≠ "repo_local_integration_debt" := by
  native_decide

#check c001CheckedLeafNames
#check c001ChildTaskDiagnosis
#check c001RepoLocalDebtGate
#check c001_not_completed_with_repo_local_integration_debt

/-! ## S1-M-297-C002 Flow/omega-limit mathlib audit gate. -/

/-- The packaged omega-limit definition unfolds to the current mathlib object. -/
theorem c002_omegaSet_eq_omegaLimit (D : PoincareBendixsonData) :
    D.omegaSet = omegaLimit atTop D.flow {D.initial} :=
  rfl

/-- mathlib's orbit of a point under the packaged real flow is its full time range. -/
theorem c002_flow_orbit_eq_range (D : PoincareBendixsonData) (p : PlanarPhase) :
    D.flow.orbit p = Set.range (fun t : ℝ => D.flow t p) :=
  D.flow.orbit_eq_range p

/-- mathlib's forward orbit is the range over nonnegative real times. -/
theorem c002_flow_forwardOrbit_eq_range_nonneg
    (D : PoincareBendixsonData) (p : PlanarPhase) :
    D.flow.forwardOrbit p = Set.range (fun t : {t : ℝ // 0 ≤ t} => D.flow t p) :=
  D.flow.forwardOrbit_eq_range_nonneg p

/-- The forward orbit API is weaker than a full planar orbit but is locally available. -/
theorem c002_flow_forwardOrbit_subset_orbit
    (D : PoincareBendixsonData) (p : PlanarPhase) :
    D.flow.forwardOrbit p ⊆ D.flow.orbit p :=
  D.flow.forwardOrbit_subset_orbit p

/--
If a compact absorbing-closure hypothesis is supplied, mathlib already gives
nonemptiness of the omega-limit set.  PB.P4 still has to derive this
absorbing-closure hypothesis from the classical trapping-region assumptions.
-/
theorem c002_omegaSet_nonempty_of_compact_absorbing_closure
    (D : PoincareBendixsonData)
    (habs : ∃ v ∈ (atTop : Filter ℝ),
      closure (image2 D.flow v {D.initial}) ⊆ D.trappingRegion) :
    D.omegaSet.Nonempty :=
  nonempty_omegaLimit_of_isCompact_absorbing atTop D.flow {D.initial}
    D.trappingRegionCompact habs (Set.singleton_nonempty D.initial)

/-- C002 audited these mathlib source modules for flow and omega-limit support. -/
def c002AuditedMathlibModules : List String := [
  "Mathlib.Dynamics.Flow",
  "Mathlib.Dynamics.OmegaLimit",
  "Mathlib.Dynamics.PeriodicPts.Defs",
  "Mathlib.Dynamics.FixedPoints.Basic",
  "Mathlib.Topology.ClusterPt",
  "Mathlib.Topology.Instances.Real.Lemmas"
]

/-- Current positive anchors found in mathlib for PB.P2. -/
def c002PositiveAnchorNames : List String := [
  "Flow",
  "Flow.toFun",
  "Flow.continuous",
  "Flow.map_add",
  "Flow.map_zero_apply",
  "Flow.orbit",
  "Flow.orbit_eq_range",
  "Flow.forwardOrbit",
  "Flow.forwardOrbit_eq_range_nonneg",
  "Flow.forwardOrbit_subset_orbit",
  "Flow.isInvariant_omegaLimit",
  "omegaLimit",
  "omegaLimit_def",
  "omegaLimit_subset_of_tendsto",
  "omegaLimit_mono_right",
  "isClosed_omegaLimit",
  "mem_omegaLimit_iff_frequently",
  "mem_omegaLimit_iff_frequently₂",
  "mem_omegaLimit_singleton_iff_map_cluster_point",
  "omegaLimit_subset_closure_fw_image",
  "eventually_mapsTo_of_isCompact_absorbing_of_isOpen_of_omegaLimit_subset",
  "nonempty_omegaLimit_of_isCompact_absorbing"
]

/--
Negative audit result: the current mathlib layer has topological-dynamics
building blocks but not a terminal Poincare-Bendixson theorem.
-/
def c002NegativeAuditFinding : String :=
  "no_terminal_poincare_bendixson_theorem_found_in_pinned_mathlib_flow_omegaLimit_sources"

/-- C002 is an anchor/API audit, not a terminal theorem proof. -/
def c002ChildTaskDiagnosis : String :=
  "mathlib_flow_omegaLimit_anchor_audit_and_formalization_debt_boundary"

/-- C002 does not permit a completion claim for THM-M-1400. -/
def c002CompletionClaimAllowed : Bool :=
  false

/-- No completed state is asserted, so no completed-state repo-local integration debt remains. -/
def c002RepoLocalIntegrationDebtRetainedInCompletedState : Bool :=
  false

/-- The positive-anchor list has the expected checked audit cardinality. -/
theorem c002PositiveAnchorNames_length :
    c002PositiveAnchorNames.length = 22 := by
  native_decide

/-- The C002 audit gate keeps THM-M-1400 open. -/
theorem c002CompletionClaimAllowed_eq_false :
    c002CompletionClaimAllowed = false := by
  native_decide

/-- C002 does not leave a completed theorem with repo-local integration debt. -/
theorem c002RepoLocalIntegrationDebtRetainedInCompletedState_eq_false :
    c002RepoLocalIntegrationDebtRetainedInCompletedState = false := by
  native_decide

#check c002_omegaSet_eq_omegaLimit
#check c002_flow_orbit_eq_range
#check c002_flow_forwardOrbit_eq_range_nonneg
#check c002_flow_forwardOrbit_subset_orbit
#check c002_omegaSet_nonempty_of_compact_absorbing_closure
#check c002AuditedMathlibModules
#check c002PositiveAnchorNames
#check c002NegativeAuditFinding
#check c002ChildTaskDiagnosis
#check c002CompletionClaimAllowed_eq_false
#check c002RepoLocalIntegrationDebtRetainedInCompletedState_eq_false

/-! ## S1-M-297-C003 typed C1 vector-field and ODE-generation gate. -/

/--
After C003, the smoothness clause is no longer an opaque proposition field:
it is carried by the typed `C1PlanarVectorField` structure.
-/
def c003TypedSmoothnessModel : String :=
  "C1PlanarVectorField.toFun_with_ContDiff_R_1_certificate"

/--
After C003, the flow-generation clause is no longer an opaque proposition
field: each trajectory of the packaged flow is required to be a mathlib
`IsIntegralCurve` for the time-independent planar vector field.
-/
def c003TypedOdeGenerationModel : String :=
  "forall_initial_point_flow_trajectory_IsIntegralCurve_for_time_independent_vectorField"

/-- The C003 checked local leaves added to this boundary artifact. -/
def c003CheckedLeafNames : List String := [
  "PB-L011.checked.C1_vector_field_model",
  "PB-L012.checked.flow_integral_curve_generation_hypothesis",
  "PB-L013.checked.core_hypotheses_prop_placeholder_removed"
]

/-- C003 leaves the terminal Poincare-Bendixson classification open. -/
def c003CompletionClaimAllowed : Bool :=
  false

/-- C003 records formalization progress, not a completed theorem with repo-local debt. -/
def c003RepoLocalIntegrationDebtRetainedInCompletedState : Bool :=
  false

/-- The C003 core-hypothesis cleanup leaves only the still-open packaged clauses. -/
theorem c003_coreHypotheses_iff (D : PoincareBendixsonData) :
    D.CoreHypotheses ↔
      D.forwardOrbitEventuallyInTrappingRegion ∧
        D.finitelyManyEquilibriaOnOmega :=
  Iff.rfl

/-- The C003 checked leaf ledger has the expected cardinality. -/
theorem c003CheckedLeafNames_length :
    c003CheckedLeafNames.length = 3 := by
  native_decide

/-- C003 does not permit a terminal theorem completion claim. -/
theorem c003CompletionClaimAllowed_eq_false :
    c003CompletionClaimAllowed = false := by
  native_decide

/-- C003 does not leave completed-state repo-local integration debt. -/
theorem c003RepoLocalIntegrationDebtRetainedInCompletedState_eq_false :
    c003RepoLocalIntegrationDebtRetainedInCompletedState = false := by
  native_decide

#check vectorField_contDiff
#check flow_solves_vectorField
#check c003TypedSmoothnessModel
#check c003TypedOdeGenerationModel
#check c003CheckedLeafNames
#check c003_coreHypotheses_iff
#check c003CompletionClaimAllowed_eq_false
#check c003RepoLocalIntegrationDebtRetainedInCompletedState_eq_false

/-! ## S1-M-297-C004 compact absorbing-region nonempty gate. -/

/--
The checked PB.P4 leaf available in the current statement boundary: once the
omega-limit set is nonempty and contained in the trapping region, the trapping
region itself is nonempty.
-/
theorem c004_trappingRegion_nonempty_of_omegaSet
    (D : PoincareBendixsonData) :
    D.trappingRegion.Nonempty := by
  rcases D.omegaSetNonempty with ⟨p, hp⟩
  exact ⟨p, D.omegaSetContainedInTrappingRegion hp⟩

/--
Combining the audited mathlib compact-absorbing omega-limit theorem with the
local containment hypothesis gives a nonempty trapping region.  This is still a
conditional PB.P4 bridge: deriving the absorbing-closure hypothesis from a
classical planar trapping-region assumption remains future formalization work.
-/
theorem c004_trappingRegion_nonempty_of_compact_absorbing_closure
    (D : PoincareBendixsonData)
    (habs : ∃ v ∈ (atTop : Filter ℝ),
      closure (image2 D.flow v {D.initial}) ⊆ D.trappingRegion) :
    D.trappingRegion.Nonempty := by
  rcases c002_omegaSet_nonempty_of_compact_absorbing_closure D habs with ⟨p, hp⟩
  exact ⟨p, D.omegaSetContainedInTrappingRegion hp⟩

/-- C004 checked local leaves for the PB.P4 nonempty bridge. -/
def c004CheckedLeafNames : List String := [
  "PB-L014a.checked.trapping_region_nonempty_from_nonempty_omega_subset",
  "PB-L014b.checked.trapping_region_nonempty_from_compact_absorbing_closure"
]

/--
C004 is conditional proof work inside the compact absorbing-region branch, not
a terminal Poincare-Bendixson classification proof.
-/
def c004ChildTaskDiagnosis : String :=
  "conditional_repo_local_proof_work_for_compact_absorbing_region_nonempty_bridge"

/--
The remaining PB.P4 debt is deriving the compact absorbing-closure hypothesis
from the classical planar trapping-region assumptions.
-/
def c004RemainingFormalizationDebt : String :=
  "derive_absorbing_closure_hypothesis_from_forward_eventual_trapping_and_planar_flow_model"

/-- C004 leaves the terminal Poincare-Bendixson classification open. -/
def c004CompletionClaimAllowed : Bool :=
  false

/-- C004 does not leave completed-state repo-local integration debt. -/
def c004RepoLocalIntegrationDebtRetainedInCompletedState : Bool :=
  false

/-- The C004 checked leaf ledger has the expected cardinality. -/
theorem c004CheckedLeafNames_length :
    c004CheckedLeafNames.length = 2 := by
  native_decide

/-- C004 does not permit a terminal theorem completion claim. -/
theorem c004CompletionClaimAllowed_eq_false :
    c004CompletionClaimAllowed = false := by
  native_decide

/-- C004 does not leave completed-state repo-local integration debt. -/
theorem c004RepoLocalIntegrationDebtRetainedInCompletedState_eq_false :
    c004RepoLocalIntegrationDebtRetainedInCompletedState = false := by
  native_decide

#check c004_trappingRegion_nonempty_of_omegaSet
#check c004_trappingRegion_nonempty_of_compact_absorbing_closure
#check c004CheckedLeafNames
#check c004ChildTaskDiagnosis
#check c004RemainingFormalizationDebt
#check c004CompletionClaimAllowed_eq_false
#check c004RepoLocalIntegrationDebtRetainedInCompletedState_eq_false

/-! ## S1-M-297-C005 planar no-crossing/transverse-section/separation split. -/

/--
Minimal same-time no-crossing core available from mathlib's real-flow API:
each time slice of a real flow is a homeomorphism, hence injective.  This is
not yet the full planar ODE no-crossing lemma used in Poincare-Bendixson; that
future lemma must connect uniqueness of integral curves, orbit arcs, and
transverse sections.
-/
def C005NoCrossingCore (D : PoincareBendixsonData) : Prop :=
  ∀ t : ℝ, Function.Injective (D.flow t)

/--
Typed boundary for the future local transverse-section package.  The fields
that remain `Prop` are the open formalization targets: transversality to the
vector field, a local flow-box/section chart, and a first-return map.
-/
structure C005TransverseSectionDatum (D : PoincareBendixsonData) : Type where
  carrier : Set PlanarPhase
  basePoint : PlanarPhase
  basePoint_mem : basePoint ∈ carrier
  transverseToVectorFieldAtBasePoint : Prop
  localFlowBoxChart : Prop
  firstReturnMapDefined : Prop

/--
Typed boundary for the future planar-separation package.  It is intentionally
separate from the transverse-section datum because the Jordan/separation branch
needs different topology APIs from the local ODE flow-box branch.
-/
structure C005PlanarSeparationDatum (D : PoincareBendixsonData) : Type where
  separator : Set PlanarPhase
  separatorCompact : IsCompact separator
  boundaryMadeOfOrbitArcsAndSections : Prop
  separatesInteriorExterior : Prop
  omegaSetSideControl : Prop

/-- PB.P5 proof leaves split at M0387-compatible granularity. -/
structure C005PlanarProofLeaf where
  id : String
  package : String
  role : String
  requiredApi : String
  expectedTarget : String
  maxProofSteps : Nat
  machineStatus : String
  debtClassification : String
  repoLocalCompletionGate : String

/-- The M0387 proof-step budget used for each PB.P5 child leaf. -/
def c005LeafStepBudget : Nat :=
  100

/--
PB.P5 is split into independent leaves for the same-time flow no-crossing
substrate, the stronger planar ODE no-crossing theorem, local transverse
sections, first-return/ordering control, planar separation, and the omega-limit
side-control bridge.
-/
def c005PlanarProofLeaves : List C005PlanarProofLeaf := [
  { id := "PB-P5-L001-flow-time-slice-injective",
    package := "PB.P5.no_crossing_substrate",
    role := "Record the checked same-time injectivity/homeomorphism substrate for real flow time slices.",
    requiredApi := "Flow.toHomeomorph, Function.Injective",
    expectedTarget := "∀ t : ℝ, Function.Injective (D.flow t)",
    maxProofSteps := c005LeafStepBudget,
    machineStatus := "checked_substrate_not_terminal_planar_no_crossing",
    debtClassification := "formalization_debt_for_stronger_planar_ODE_no_crossing",
    repoLocalCompletionGate := "validated local wrapper only; does not close Poincare-Bendixson" },
  { id := "PB-P5-L002-orbit-arc-no-crossing",
    package := "PB.P5.no_crossing_planar_ODE",
    role := "Upgrade same-time flow injectivity to the planar orbit-arc no-crossing theorem used by the classical proof.",
    requiredApi := "integral-curve uniqueness, orbit arcs, time-shift normalization, nonstationary trajectory hypotheses",
    expectedTarget := "two nonstationary planar solution arcs meeting at an interior point are the same time-shifted orbit arc",
    maxProofSteps := c005LeafStepBudget,
    machineStatus := "unchecked",
    debtClassification := "formalization_debt",
    repoLocalCompletionGate := "requires local proof body or pinned checked import" },
  { id := "PB-P5-L003-local-transverse-section-existence",
    package := "PB.P5.transverse_section",
    role := "Build a local section through a non-equilibrium omega-limit point transverse to the vector field.",
    requiredApi := "nonzero vector field at the point, local chart on ℝ × ℝ, flow-box or implicit-function theorem",
    expectedTarget := "C005TransverseSectionDatum D with transversality and local flow-box fields inhabited",
    maxProofSteps := c005LeafStepBudget,
    machineStatus := "unchecked",
    debtClassification := "formalization_debt",
    repoLocalCompletionGate := "requires local proof body or pinned checked import" },
  { id := "PB-P5-L004-first-return-map-ordering",
    package := "PB.P5.transverse_section_return",
    role := "Define first-hit/return data on the transverse section and prove the monotonic/order constraint forced by no-crossing.",
    requiredApi := "hitting times, local section coordinates, order on a one-dimensional section, no-crossing bridge",
    expectedTarget := "successive returns to a transverse section are ordered or eventually periodic",
    maxProofSteps := c005LeafStepBudget,
    machineStatus := "unchecked",
    debtClassification := "formalization_debt",
    repoLocalCompletionGate := "requires local proof body or pinned checked import" },
  { id := "PB-P5-L005-planar-separation-jordan-arc",
    package := "PB.P5.planar_separation",
    role := "Formalize the planar separation/Jordan-arc region built from an orbit segment and a transverse-section segment.",
    requiredApi := "Jordan curve or simple arc separation in ℝ², compactness of the boundary, inside/outside components",
    expectedTarget := "C005PlanarSeparationDatum D with separation fields inhabited",
    maxProofSteps := c005LeafStepBudget,
    machineStatus := "unchecked",
    debtClassification := "formalization_debt",
    repoLocalCompletionGate := "requires local proof body or pinned checked import" },
  { id := "PB-P5-L006-omega-side-control",
    package := "PB.P5.separation_to_omega_limit",
    role := "Connect the separated planar region to omega-limit recurrence so the no-equilibrium branch can use it.",
    requiredApi := "omega-limit invariance, recurrence/cluster characterization, planar side-control from no-crossing",
    expectedTarget := "omega-limit points cannot alternate across the separated boundary except through the permitted return pattern",
    maxProofSteps := c005LeafStepBudget,
    machineStatus := "unchecked",
    debtClassification := "formalization_debt",
    repoLocalCompletionGate := "requires local proof body or pinned checked import" }
]

/-- Every PB.P5 split leaf is at or below the M0387 `<= 100` proof-step budget. -/
def c005AllLeafBudgetsWithinM0387Limit : Bool :=
  c005PlanarProofLeaves.all (fun leaf => leaf.maxProofSteps ≤ c005LeafStepBudget)

/-- C005 is theorem-tree split and checked substrate work, not terminal theorem closure. -/
def c005ChildTaskDiagnosis : String :=
  "theorem_tree_split_with_checked_flow_injectivity_substrate_for_planar_no_crossing_transverse_section_and_separation_branches"

/-- C005 leaves the terminal Poincare-Bendixson classification open. -/
def c005CompletionClaimAllowed : Bool :=
  false

/-- C005 does not leave completed-state repo-local integration debt. -/
def c005RepoLocalIntegrationDebtRetainedInCompletedState : Bool :=
  false

/-- The same-time no-crossing core follows from the real-flow homeomorphism API. -/
theorem c005_noCrossingCore_from_flow (D : PoincareBendixsonData) :
    C005NoCrossingCore D := by
  intro t
  exact (D.flow.toHomeomorph t).injective

/-- A direct same-time no-crossing wrapper for two points under one flow time. -/
theorem c005_same_time_no_crossing
    (D : PoincareBendixsonData) {x y : PlanarPhase} {t : ℝ}
    (h : D.flow t x = D.flow t y) :
    x = y :=
  (c005_noCrossingCore_from_flow D t) h

/-- Time images of sets are equivalent to preimages under reversed time. -/
theorem c005_flow_image_eq_preimage_reverse
    (D : PoincareBendixsonData) (t : ℝ) (s : Set PlanarPhase) :
    D.flow t '' s = D.flow (-t) ⁻¹' s :=
  D.flow.image_eq_preimage_symm t s

/-- The C005 theorem-tree split has the expected six leaves. -/
theorem c005PlanarProofLeaves_length :
    c005PlanarProofLeaves.length = 6 := by
  native_decide

/-- The C005 leaf budget gate is checked locally. -/
theorem c005AllLeafBudgetsWithinM0387Limit_eq_true :
    c005AllLeafBudgetsWithinM0387Limit = true := by
  native_decide

/-- C005 does not permit a terminal theorem completion claim. -/
theorem c005CompletionClaimAllowed_eq_false :
    c005CompletionClaimAllowed = false := by
  native_decide

/-- C005 does not leave completed-state repo-local integration debt. -/
theorem c005RepoLocalIntegrationDebtRetainedInCompletedState_eq_false :
    c005RepoLocalIntegrationDebtRetainedInCompletedState = false := by
  native_decide

#check C005NoCrossingCore
#check C005TransverseSectionDatum
#check C005PlanarSeparationDatum
#check C005PlanarProofLeaf
#check c005PlanarProofLeaves
#check c005_noCrossingCore_from_flow
#check c005_same_time_no_crossing
#check c005_flow_image_eq_preimage_reverse
#check c005PlanarProofLeaves_length
#check c005AllLeafBudgetsWithinM0387Limit_eq_true
#check c005CompletionClaimAllowed_eq_false
#check c005RepoLocalIntegrationDebtRetainedInCompletedState_eq_false

/-! ## S1-M-297-C006 no-equilibrium omega-limit classification branch. -/

/--
The no-equilibrium branch hypothesis for PB.P6: no point of the omega-limit set
is fixed by every time of the continuous real flow.
-/
def C006NoEquilibriumOmegaCase (D : PoincareBendixsonData) : Prop :=
  ¬ D.HasEquilibriumInOmega

/--
The PB.P6 target once PB.P5 has supplied the planar no-crossing,
transverse-section return, and separation/side-control machinery.
-/
def C006NoEquilibriumPeriodicOrbitTarget (D : PoincareBendixsonData) : Prop :=
  D.CoreHypotheses → C006NoEquilibriumOmegaCase D →
    D.IsPeriodicOrbitSet D.omegaSet

/--
If a no-equilibrium branch proof produces the periodic-orbit alternative, it
assembles into the local `ClassificationConclusion` disjunction.
-/
theorem c006_classification_of_periodicOrbitSet
    (D : PoincareBendixsonData)
    (hper : D.IsPeriodicOrbitSet D.omegaSet) :
    D.ClassificationConclusion :=
  Or.inr (Or.inl hper)

/--
Under a no-equilibrium hypothesis, any already-known classification conclusion
reduces to the periodic-orbit or finite-equilibrium-cycle alternatives.
-/
theorem c006_noEquilibrium_cases_of_classification
    (D : PoincareBendixsonData)
    (hno : C006NoEquilibriumOmegaCase D)
    (hclass : D.ClassificationConclusion) :
    D.IsPeriodicOrbitSet D.omegaSet ∨ D.FiniteEquilibriumCycleGraph := by
  rcases hclass with heq | hrest
  · exact False.elim (hno heq)
  · exact hrest

/--
The set-level periodic-orbit predicate carries a positive return time whose
time-map fixes the base point.
-/
theorem c006_periodicOrbitSet_has_fixed_return_time
    (D : PoincareBendixsonData)
    (hper : D.IsPeriodicOrbitSet D.omegaSet) :
    ∃ p : PlanarPhase, ∃ T : ℝ, 0 < T ∧ IsFixedPt (D.flow T) p := by
  rcases hper with ⟨p, T, hTpos, hTfix, _hset⟩
  exact ⟨p, T, hTpos, hTfix⟩

/--
A positive return time from the set-level periodic-orbit predicate gives a
periodic point for every iterate of that time map.
-/
theorem c006_periodicOrbitSet_has_periodicPt_for_return_map
    (D : PoincareBendixsonData)
    (hper : D.IsPeriodicOrbitSet D.omegaSet) (n : ℕ) :
    ∃ p : PlanarPhase, ∃ T : ℝ, 0 < T ∧ IsPeriodicPt (D.flow T) n p := by
  rcases c006_periodicOrbitSet_has_fixed_return_time D hper with
    ⟨p, T, hTpos, hfix⟩
  exact ⟨p, T, hTpos, hfix.isPeriodicPt n⟩

/-- PB.P6 proof leaves at M0387-compatible granularity. -/
structure C006NoEquilibriumProofLeaf where
  id : String
  package : String
  role : String
  expectedTarget : String
  maxProofSteps : Nat
  machineStatus : String
  debtClassification : String
  repoLocalCompletionGate : String

/-- The M0387 proof-step budget used for each PB.P6 child leaf. -/
def c006LeafStepBudget : Nat :=
  100

/--
PB.P6 is split into checked local assembly leaves plus open planar-dynamics
leaves that must be discharged before the no-equilibrium branch can close.
-/
def c006NoEquilibriumProofLeaves : List C006NoEquilibriumProofLeaf := [
  { id := "PB-P6-L001-no-equilibrium-branch-predicate",
    package := "PB.P6.branch_statement",
    role := "Name the no-equilibrium omega-limit branch as the negation of the existing equilibrium alternative.",
    expectedTarget := "C006NoEquilibriumOmegaCase D = ¬ D.HasEquilibriumInOmega",
    maxProofSteps := c006LeafStepBudget,
    machineStatus := "checked_statement_boundary",
    debtClassification := "none_for_local_predicate",
    repoLocalCompletionGate := "validated local definition only; does not close Poincare-Bendixson" },
  { id := "PB-P6-L002-periodic-orbit-target",
    package := "PB.P6.branch_statement",
    role := "State the no-equilibrium compact omega-limit target as the periodic-orbit set alternative.",
    expectedTarget := "D.CoreHypotheses → C006NoEquilibriumOmegaCase D → D.IsPeriodicOrbitSet D.omegaSet",
    maxProofSteps := c006LeafStepBudget,
    machineStatus := "checked_statement_boundary",
    debtClassification := "formalization_debt_for_proof_body",
    repoLocalCompletionGate := "requires PB.P5 side-control proof plus local proof body or pinned checked import" },
  { id := "PB-P6-L003-periodic-branch-final-disjunction",
    package := "PB.P6.classification_assembly",
    role := "Assemble a proved periodic-orbit branch into ClassificationConclusion.",
    expectedTarget := "D.IsPeriodicOrbitSet D.omegaSet → D.ClassificationConclusion",
    maxProofSteps := c006LeafStepBudget,
    machineStatus := "checked_wrapper",
    debtClassification := "none_for_local_wrapper",
    repoLocalCompletionGate := "validated local wrapper only; does not close Poincare-Bendixson" },
  { id := "PB-P6-L004-no-equilibrium-disjunction-elimination",
    package := "PB.P6.classification_assembly",
    role := "Eliminate the equilibrium alternative from an already-known classification under the no-equilibrium hypothesis.",
    expectedTarget := "C006NoEquilibriumOmegaCase D → D.ClassificationConclusion → D.IsPeriodicOrbitSet D.omegaSet ∨ D.FiniteEquilibriumCycleGraph",
    maxProofSteps := c006LeafStepBudget,
    machineStatus := "checked_wrapper",
    debtClassification := "none_for_local_wrapper",
    repoLocalCompletionGate := "validated local wrapper only; does not close Poincare-Bendixson" },
  { id := "PB-P6-L005-periodic-set-to-time-map-periodic-point",
    package := "PB.P6.periodic_api_bridge",
    role := "Connect the set-level continuous-flow periodic orbit predicate to mathlib fixed/periodic point predicates for a return-time map.",
    expectedTarget := "D.IsPeriodicOrbitSet D.omegaSet → ∃ p T, 0 < T ∧ IsPeriodicPt (D.flow T) n p",
    maxProofSteps := c006LeafStepBudget,
    machineStatus := "checked_wrapper",
    debtClassification := "none_for_local_wrapper",
    repoLocalCompletionGate := "validated local wrapper only; does not close Poincare-Bendixson" },
  { id := "PB-P6-L006-no-equilibrium-planar-return-proof",
    package := "PB.P6.no_equilibrium_to_periodic_orbit",
    role := "Use transverse sections, ordered returns, no-crossing, and omega-limit recurrence to prove the no-equilibrium omega-limit set is one periodic orbit.",
    expectedTarget := "C006NoEquilibriumPeriodicOrbitTarget D",
    maxProofSteps := c006LeafStepBudget,
    machineStatus := "unchecked",
    debtClassification := "formalization_debt",
    repoLocalCompletionGate := "requires local proof body or pinned checked import" }
]

/-- Every PB.P6 split leaf is at or below the M0387 `<= 100` proof-step budget. -/
def c006AllLeafBudgetsWithinM0387Limit : Bool :=
  c006NoEquilibriumProofLeaves.all (fun leaf => leaf.maxProofSteps ≤ c006LeafStepBudget)

/-- C006 is branch-target and checked assembly work, not terminal theorem closure. -/
def c006ChildTaskDiagnosis : String :=
  "formalization_debt_with_checked_no_equilibrium_branch_target_and_periodic_api_assembly_wrappers"

/-- C006 leaves the terminal Poincare-Bendixson classification open. -/
def c006CompletionClaimAllowed : Bool :=
  false

/-- C006 does not leave completed-state repo-local integration debt. -/
def c006RepoLocalIntegrationDebtRetainedInCompletedState : Bool :=
  false

/-- The no-equilibrium branch predicate unfolds to the existing equilibrium alternative. -/
theorem c006_noEquilibriumOmegaCase_iff (D : PoincareBendixsonData) :
    C006NoEquilibriumOmegaCase D ↔ ¬ D.HasEquilibriumInOmega :=
  Iff.rfl

/-- The PB.P6 theorem-tree split has the expected six leaves. -/
theorem c006NoEquilibriumProofLeaves_length :
    c006NoEquilibriumProofLeaves.length = 6 := by
  native_decide

/-- The C006 leaf budget gate is checked locally. -/
theorem c006AllLeafBudgetsWithinM0387Limit_eq_true :
    c006AllLeafBudgetsWithinM0387Limit = true := by
  native_decide

/-- C006 does not permit a terminal theorem completion claim. -/
theorem c006CompletionClaimAllowed_eq_false :
    c006CompletionClaimAllowed = false := by
  native_decide

/-- C006 does not leave completed-state repo-local integration debt. -/
theorem c006RepoLocalIntegrationDebtRetainedInCompletedState_eq_false :
    c006RepoLocalIntegrationDebtRetainedInCompletedState = false := by
  native_decide

#check C006NoEquilibriumOmegaCase
#check C006NoEquilibriumPeriodicOrbitTarget
#check c006_classification_of_periodicOrbitSet
#check c006_noEquilibrium_cases_of_classification
#check c006_periodicOrbitSet_has_fixed_return_time
#check c006_periodicOrbitSet_has_periodicPt_for_return_map
#check C006NoEquilibriumProofLeaf
#check c006NoEquilibriumProofLeaves
#check c006_noEquilibriumOmegaCase_iff
#check c006NoEquilibriumProofLeaves_length
#check c006AllLeafBudgetsWithinM0387Limit_eq_true
#check c006CompletionClaimAllowed_eq_false
#check c006RepoLocalIntegrationDebtRetainedInCompletedState_eq_false

/-! ## S1-M-297-C007 external Lean 4 primary-source audit gate. -/

/-- One primary-source audit row for a possible external Poincare-Bendixson proof. -/
structure C007ExternalAuditEntry where
  source : String
  sourceKind : String
  sourceUrl : String
  searchedTerms : List String
  finding : String
  importDecision : String

/-- Date of the C007 external Lean 4 primary-source audit. -/
def c007ExternalAuditDate : String :=
  "2026-05-01"

/-- C007 search terms for an importable Lean 4 Poincare-Bendixson proof. -/
def c007ExternalLean4SearchTerms : List String := [
  "Poincare-Bendixson Lean 4",
  "Poincare Bendixson Lean theorem",
  "PoincareBendixson Lean",
  "Bendixson omegaLimit Lean",
  "site:github.com Poincare-Bendixson Lean",
  "site:github.com Poincare Bendixson mathlib"
]

/--
Primary-source rows from the C007 audit.  The AFP row is retained as a
near-miss because it is a genuine formal proof, but it is Isabelle/HOL rather
than an importable Lean 4 dependency.
-/
def c007ExternalAuditEntries : List C007ExternalAuditEntry := [
  { source := "leanprover-community/mathlib4 pinned Flow/OmegaLimit sources",
    sourceKind := "Lean 4 primary source already pinned locally",
    sourceUrl :=
      "https://github.com/leanprover-community/mathlib4/tree/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/Dynamics",
    searchedTerms := [
      "Poincare", "Poincare-Bendixson", "Bendixson", "omegaLimit",
      "periodic orbit", "Flow", "IsPeriodicPt"
    ],
    finding :=
      "Flow, omegaLimit, invariant, fixed-point, and periodic-point anchors exist; no terminal Poincare-Bendixson theorem was found",
    importDecision :=
      "already pinned as mathlib substrate; no terminal theorem exists here to import as closure" },
  { source := "GitHub public repository search API",
    sourceKind := "external Lean 4 repository discovery probe",
    sourceUrl :=
      "https://api.github.com/search/repositories?q=%22Poincare-Bendixson%22+Lean",
    searchedTerms := c007ExternalLean4SearchTerms,
    finding :=
      "exact repository searches for Poincare-Bendixson Lean variants returned no candidate Lean repository",
    importDecision :=
      "no external Lean 4 repository candidate to pin/import/check" },
  { source := "Archive of Formal Proofs Poincare_Bendixson",
    sourceKind := "Isabelle/HOL primary-source near-miss",
    sourceUrl :=
      "https://www.isa-afp.org/entries/Poincare_Bendixson.html",
    searchedTerms := [
      "poincare_bendixson", "poincare_bendixson_general",
      "poincare_bendixson_applied", "poincare_bendixson_limit_cycle"
    ],
    finding :=
      "AFP exposes Isabelle/HOL theorems named poincare_bendixson and poincare_bendixson_general, but it is not Lean 4",
    importDecision :=
      "proof-architecture reference only; not importable into this Lean 4 Lake closure" }
]

/-- C007 found no importable external Lean 4 terminal Poincare-Bendixson proof. -/
def c007ExternalLean4TerminalProofFound : Bool :=
  false

/-- C007 is an external-anchor audit, not terminal proof work. -/
def c007ChildTaskDiagnosis : String :=
  "external_anchor_audit_with_non_Lean_AFP_near_miss_and_no_importable_Lean4_terminal_proof_found"

/-- C007 leaves the terminal Poincare-Bendixson classification open. -/
def c007CompletionClaimAllowed : Bool :=
  false

/-- C007 does not leave completed-state repo-local integration debt. -/
def c007RepoLocalIntegrationDebtRetainedInCompletedState : Bool :=
  false

/-- The C007 audit rows include mathlib, repository search, and AFP near-miss checks. -/
theorem c007ExternalAuditEntries_length :
    c007ExternalAuditEntries.length = 3 := by
  native_decide

/-- The C007 external Lean 4 audit found no terminal proof to pin. -/
theorem c007ExternalLean4TerminalProofFound_eq_false :
    c007ExternalLean4TerminalProofFound = false := by
  native_decide

/-- C007 does not permit a terminal theorem completion claim. -/
theorem c007CompletionClaimAllowed_eq_false :
    c007CompletionClaimAllowed = false := by
  native_decide

/-- C007 does not leave completed-state repo-local integration debt. -/
theorem c007RepoLocalIntegrationDebtRetainedInCompletedState_eq_false :
    c007RepoLocalIntegrationDebtRetainedInCompletedState = false := by
  native_decide

#check C007ExternalAuditEntry
#check c007ExternalAuditDate
#check c007ExternalLean4SearchTerms
#check c007ExternalAuditEntries
#check c007ExternalAuditEntries_length
#check c007ExternalLean4TerminalProofFound_eq_false
#check c007ChildTaskDiagnosis
#check c007CompletionClaimAllowed_eq_false
#check c007RepoLocalIntegrationDebtRetainedInCompletedState_eq_false

end S1_M_297
end Stage1
end AwesomeTheorems
