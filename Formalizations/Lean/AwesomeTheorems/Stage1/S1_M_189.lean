import Mathlib.LinearAlgebra.SymplecticGroup
import Mathlib.MeasureTheory.Measure.Lebesgue.EqHaar

/-!
# S1-M-189 / THM-M-1520: Liouville theorem, Stage1 statement boundary

This file records a conservative Lean 4 boundary for Liouville's theorem in
Hamiltonian mechanics: phase-space volume is preserved by Hamiltonian flow.

The pinned mathlib snapshot provides finite-dimensional real volume/Haar
measure, `MeasurePreserving`, and a linear symplectic-group API.  It does not
currently provide a terminal Hamiltonian-flow theorem proving that a smooth
Hamiltonian vector field has a globally defined volume-preserving flow.  The
declarations below therefore freeze the formalization boundary and add checked
low-risk wrappers around the measure-preserving and symplectic substrate.

No terminal Liouville theorem is claimed here.
-/

noncomputable section

open MeasureTheory

namespace AwesomeTheorems.Stage1.S1_M_189

universe u

/-- Canonical finite-dimensional phase space with position and momentum coordinates. -/
abbrev PhaseSpace (Coord : Type u) :=
  (Coord ⊕ Coord) → ℝ

/-- Phase-space volume for the finite-dimensional coordinate model. -/
abbrev PhaseVolume (Coord : Type u) [Fintype Coord] :
    Measure (PhaseSpace Coord) :=
  volume

/-- A time-dependent phase flow on the normalized phase space. -/
abbrev PhaseFlow (Coord : Type u) :=
  ℝ → PhaseSpace Coord → PhaseSpace Coord

/--
Data for an abstract Hamiltonian flow.

The fields `hamiltonian_smooth`, `solvesHamiltonEquations`, and
`symplecticFlow` are explicit proposition fields because the local mathlib
closure does not yet expose the Hamiltonian-vector-field and flow theorem
needed to prove Liouville's theorem from these hypotheses.
-/
structure HamiltonianFlowData (Coord : Type u) [Fintype Coord] where
  hamiltonian : PhaseSpace Coord → ℝ
  flow : PhaseFlow Coord
  time_zero : ∀ x : PhaseSpace Coord, flow 0 x = x
  flow_add : ∀ s t : ℝ, ∀ x : PhaseSpace Coord,
    flow (s + t) x = flow s (flow t x)
  hamiltonian_smooth : Prop
  solvesHamiltonEquations : Prop
  symplecticFlow : Prop

/-- The hypotheses expected before applying a Hamiltonian Liouville theorem. -/
def HamiltonianFlowHypotheses {Coord : Type u} [Fintype Coord]
    (D : HamiltonianFlowData Coord) : Prop :=
  D.hamiltonian_smooth ∧ D.solvesHamiltonEquations ∧ D.symplecticFlow

/-- Phase-volume preservation for all times in the normalized model. -/
def PhaseVolumePreserved {Coord : Type u} [Fintype Coord]
    (D : HamiltonianFlowData Coord) : Prop :=
  ∀ t : ℝ,
    MeasurePreserving (D.flow t) (PhaseVolume Coord) (PhaseVolume Coord)

/--
Stage1 normalized statement shape for Liouville's theorem.

For every finite-dimensional coordinate phase space and Hamiltonian-flow data,
smoothness, Hamilton equations, and symplectic-flow hypotheses imply
phase-volume preservation at every time.  This is a statement boundary, not a
repo-local proof of the Hamiltonian-flow theorem.
-/
def StatementShape : Prop :=
  ∀ (Coord : Type u) [Fintype Coord],
    ∀ D : HamiltonianFlowData Coord,
      HamiltonianFlowHypotheses D → PhaseVolumePreserved D

/-- The statement shape unfolds to the expected quantified implication. -/
theorem statementShape_iff_forall_data :
    StatementShape.{u} ↔
      ∀ (Coord : Type u) [Fintype Coord],
        ∀ D : HamiltonianFlowData Coord,
          HamiltonianFlowHypotheses D → PhaseVolumePreserved D :=
  Iff.rfl

/--
The measured-set consequence of phase-volume preservation: null-measurable
sets have equal volume after taking preimage under the flow.
-/
theorem PhaseVolumePreserved.measure_preimage
    {Coord : Type u} [Fintype Coord]
    {D : HamiltonianFlowData Coord}
    (hD : PhaseVolumePreserved D) (t : ℝ)
    {s : Set (PhaseSpace Coord)}
    (hs : NullMeasurableSet s (PhaseVolume Coord)) :
    PhaseVolume Coord ((D.flow t) ⁻¹' s) = PhaseVolume Coord s :=
  (hD t).measure_preimage hs

/-- A volume-preserving phase flow is quasi-measure-preserving at every time. -/
theorem PhaseVolumePreserved.quasiMeasurePreserving
    {Coord : Type u} [Fintype Coord]
    {D : HamiltonianFlowData Coord}
    (hD : PhaseVolumePreserved D) (t : ℝ) :
    Measure.QuasiMeasurePreserving
      (D.flow t) (PhaseVolume Coord) (PhaseVolume Coord) :=
  (hD t).quasiMeasurePreserving

/-- Identity flow as a checked toy model for the statement interface. -/
def identityHamiltonianData (Coord : Type u) [Fintype Coord] :
    HamiltonianFlowData Coord where
  hamiltonian := fun _ => 0
  flow := fun _ x => x
  time_zero := by
    intro x
    rfl
  flow_add := by
    intro s t x
    rfl
  hamiltonian_smooth := True
  solvesHamiltonEquations := True
  symplecticFlow := True

/-- The identity flow satisfies the normalized hypotheses. -/
theorem identityHamiltonianData_hypotheses
    (Coord : Type u) [Fintype Coord] :
    HamiltonianFlowHypotheses (identityHamiltonianData Coord) :=
  ⟨trivial, trivial, trivial⟩

/-- The identity flow preserves phase volume, checked through mathlib. -/
theorem identityPhaseVolumePreserved
    (Coord : Type u) [Fintype Coord] :
    PhaseVolumePreserved (identityHamiltonianData Coord) := by
  intro t
  exact MeasurePreserving.id (PhaseVolume Coord)

/-- mathlib proves that a symplectic matrix has a unit determinant. -/
theorem symplecticMatrix_det_isUnit
    {Coord : Type u} [DecidableEq Coord] [Fintype Coord]
    {A : Matrix (Coord ⊕ Coord) (Coord ⊕ Coord) ℝ}
    (hA : A ∈ Matrix.symplecticGroup Coord ℝ) :
    IsUnit A.det :=
  SymplecticGroup.symplectic_det hA

/--
The determinant of a real symplectic matrix is nonzero.

This is the strongest determinant consequence available from the current
pinned mathlib symplectic API without proving the upstream TODO that the
determinant is exactly one.
-/
theorem symplecticMatrix_det_ne_zero
    {Coord : Type u} [DecidableEq Coord] [Fintype Coord]
    {A : Matrix (Coord ⊕ Coord) (Coord ⊕ Coord) ℝ}
    (hA : A ∈ Matrix.symplecticGroup Coord ℝ) :
    A.det ≠ 0 :=
  (symplecticMatrix_det_isUnit hA).ne_zero

/--
The canonical symplectic matrix belongs to mathlib's symplectic group.

This is a linear-algebra anchor only; the current mathlib file explicitly
leaves determinant-one for symplectic matrices as a TODO.
-/
theorem canonicalSymplecticMatrix_mem
    (Coord : Type u) [DecidableEq Coord] [Fintype Coord] :
    Matrix.J Coord ℝ ∈ Matrix.symplecticGroup Coord ℝ :=
  SymplecticGroup.J_mem Coord ℝ

/-- The determinant-unit anchor applied to the canonical symplectic matrix. -/
theorem canonicalSymplecticMatrix_det_isUnit
    (Coord : Type u) [DecidableEq Coord] [Fintype Coord] :
    IsUnit (Matrix.J Coord ℝ).det :=
  symplecticMatrix_det_isUnit (canonicalSymplecticMatrix_mem Coord)

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.LinearAlgebra.SymplecticGroup",
  "Mathlib.MeasureTheory.Measure.Lebesgue.EqHaar",
  "Mathlib.MeasureTheory.Measure.QuasiMeasurePreserving",
  "Mathlib.MeasureTheory.Measure.Haar.Basic",
  "Mathlib.MeasureTheory.Measure.Lebesgue.Basic"
]

/-- Pinned mathlib revision recorded for the public C002 anchor audit. -/
def c002PinnedMathlibRevision : String :=
  "dc7664a302ed42b3acb861ceeacdb5e866358313"

/-- Exact public C002 anchors requested for the Liouville Stage1 slot. -/
def c002PublicAnchorNames : List String := [
  "MeasureTheory.MeasurePreserving",
  "MeasureTheory.MeasurePreserving.measure_preimage",
  "Matrix.symplecticGroup",
  "SymplecticGroup.J_mem",
  "SymplecticGroup.symplectic_det"
]

/--
Public C002 anchor table as `(mathlib revision, module, declaration)`.

The declarations are substrate anchors only.  They do not close the terminal
Hamiltonian-flow Liouville theorem.
-/
def c002PublicAnchorTable : List (String × String × String) := [
  (c002PinnedMathlibRevision,
    "Mathlib.Dynamics.Ergodic.MeasurePreserving",
    "MeasureTheory.MeasurePreserving"),
  (c002PinnedMathlibRevision,
    "Mathlib.Dynamics.Ergodic.MeasurePreserving",
    "MeasureTheory.MeasurePreserving.measure_preimage"),
  (c002PinnedMathlibRevision,
    "Mathlib.LinearAlgebra.SymplecticGroup",
    "Matrix.symplecticGroup"),
  (c002PinnedMathlibRevision,
    "Mathlib.LinearAlgebra.SymplecticGroup",
    "SymplecticGroup.J_mem"),
  (c002PinnedMathlibRevision,
    "Mathlib.LinearAlgebra.SymplecticGroup",
    "SymplecticGroup.symplectic_det")
]

/-- The public C002 audit records exactly the five requested anchors. -/
theorem c002PublicAnchorNames_length :
    c002PublicAnchorNames.length = 5 :=
  rfl

/-! ## C003 formalization-debt boundary -/

/--
Public C003 debt classification for the terminal Hamiltonian Liouville theorem.

This records that the full Hamiltonian-flow theorem is mathematical knowledge
whose repo-local Lean proof is not yet closed.
-/
def c003FullLiouvilleDebtClass : String :=
  "formalization_debt"

/--
Public C003 completion flag for the terminal Hamiltonian Liouville theorem.

The checked statement boundary and substrate wrappers below are local progress,
but they are not a proof of volume preservation for every Hamiltonian flow.
-/
def c003FullLiouvilleCompleted : Bool :=
  false

/-- The C003 terminal theorem completion flag is intentionally false. -/
theorem c003FullLiouville_not_completed :
    c003FullLiouvilleCompleted = false :=
  rfl

/-- Repo-local declarations that form the checked C003 statement boundary. -/
def c003CompiledStatementBoundary : List String := [
  "PhaseSpace",
  "PhaseVolume",
  "PhaseFlow",
  "HamiltonianFlowData",
  "HamiltonianFlowHypotheses",
  "PhaseVolumePreserved",
  "StatementShape",
  "statementShape_iff_forall_data"
]

/-- Repo-local substrate wrappers that compile, without closing the full theorem. -/
def c003CompiledSubstrateWrappers : List String := [
  "PhaseVolumePreserved.measure_preimage",
  "PhaseVolumePreserved.quasiMeasurePreserving",
  "identityHamiltonianData_hypotheses",
  "identityPhaseVolumePreserved",
  "symplecticMatrix_det_isUnit",
  "canonicalSymplecticMatrix_mem",
  "canonicalSymplecticMatrix_det_isUnit"
]

/-- Concrete theorem/API families still blocking a terminal repo-local proof. -/
def c003FormalizationBlockers : List String := [
  "Hamiltonian vector field API",
  "global Hamiltonian flow existence and group law",
  "Hamilton equation encoding",
  "proof that Hamiltonian flow is symplectic or divergence-free",
  "bridge from the flow theorem to MeasurePreserving phase volume"
]

/-! ## C004 theorem-tree split -/

/--
Package-level theorem-tree metadata for the public Liouville Stage1 split.

Rows in this structure are audit metadata.  They record checked local anchors
and remaining leaves, but they do not assert the terminal Hamiltonian-flow
Liouville theorem.
-/
structure C004TheoremTreePackage where
  canonicalName : String
  role : String
  repoLocalStatus : String
  localAnchors : List String
  remainingLeaves : List String

/--
M0387-style theorem-tree split for the Hamiltonian Liouville Stage1 artifact.

The statement, measure-object, identity-model, and symplectic-linear substrate
rows have repo-local checked anchors.  The nonlinear Hamiltonian-flow bridge
rows remain formalization debt until mathlib or this repository supplies the
Hamiltonian vector field, global flow, Hamilton-equation, symplectic-flow or
divergence-free, and `MeasurePreserving` bridge APIs.
-/
def c004TheoremTreeSplit : List C004TheoremTreePackage := [
  {
    canonicalName := "statement_normalization",
    role :=
      "Normalize Liouville's theorem as phase-volume preservation for " ++
      "finite-dimensional Hamiltonian-flow data.",
    repoLocalStatus := "checked_statement_boundary_not_terminal",
    localAnchors := [
      "PhaseSpace",
      "PhaseVolume",
      "PhaseFlow",
      "HamiltonianFlowData",
      "HamiltonianFlowHypotheses",
      "PhaseVolumePreserved",
      "StatementShape",
      "statementShape_iff_forall_data"
    ],
    remainingLeaves := [
      "choose a concrete smooth Hamiltonian API",
      "replace proposition fields by checked analytic hypotheses"
    ]
  },
  {
    canonicalName := "measure_object_model",
    role :=
      "Fix the phase-space measure target as mathlib volume on the " ++
      "finite-dimensional coordinate model and expose its " ++
      "MeasurePreserving consequences.",
    repoLocalStatus := "checked_statement_boundary_not_terminal",
    localAnchors := [
      "PhaseVolume",
      "PhaseVolumePreserved",
      "PhaseVolumePreserved.measure_preimage",
      "PhaseVolumePreserved.quasiMeasurePreserving",
      "MeasureTheory.MeasurePreserving"
    ],
    remainingLeaves := [
      "prove the nonlinear Hamiltonian flow is MeasurePreserving",
      "connect any Liouville-measure variant to the selected phase volume"
    ]
  },
  {
    canonicalName := "symplectic_linear_substrate",
    role :=
      "Record the checked linear symplectic-group substrate available from " ++
      "pinned mathlib.",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    localAnchors := [
      "Matrix.symplecticGroup",
      "SymplecticGroup.J_mem",
      "SymplecticGroup.symplectic_det",
      "symplecticMatrix_det_isUnit",
      "canonicalSymplecticMatrix_mem",
      "canonicalSymplecticMatrix_det_isUnit"
    ],
    remainingLeaves := [
      "upgrade determinant-unit substrate to the exact real volume determinant condition if required",
      "lift linear symplectic anchors to nonlinear flow differentials"
    ]
  },
  {
    canonicalName := "flow_to_measure_bridge",
    role :=
      "Turn a checked global Hamiltonian flow theorem into phase-volume " ++
      "preservation for each time.",
    repoLocalStatus := "formalization_debt",
    localAnchors := [
      "HamiltonianFlowData",
      "HamiltonianFlowHypotheses",
      "PhaseVolumePreserved"
    ],
    remainingLeaves := [
      "define Hamiltonian vector fields",
      "prove global flow existence and group law",
      "encode Hamilton equations",
      "prove the resulting flow preserves the chosen phase measure"
    ]
  },
  {
    canonicalName := "jacobian_or_symplectic_volume_bridge",
    role :=
      "Close the analytic bridge from symplectic or divergence-free flow " ++
      "data to volume preservation.",
    repoLocalStatus := "formalization_debt",
    localAnchors := [
      "SymplecticGroup.symplectic_det",
      "MeasureTheory.MeasurePreserving",
      "MeasureTheory.MeasurePreserving.measure_preimage"
    ],
    remainingLeaves := [
      "prove determinant-one or Jacobian-volume bridge for the selected finite-dimensional model",
      "prove symplectic-flow or divergence-free property for Hamiltonian flow",
      "package the bridge as a repo-local MeasurePreserving theorem"
    ]
  },
  {
    canonicalName := "special_models",
    role :=
      "Keep checked toy or special models separate from the terminal theorem.",
    repoLocalStatus := "local_proof_body_for_identity_model_only",
    localAnchors := [
      "identityHamiltonianData",
      "identityHamiltonianData_hypotheses",
      "identityPhaseVolumePreserved"
    ],
    remainingLeaves := [
      "add nontrivial Hamiltonian examples only after their flow and measure bridge validate locally",
      "do not promote identity-flow sanity checks to the full Liouville theorem"
    ]
  },
  {
    canonicalName := "repo_local_closure_gate",
    role :=
      "Prevent any completed public state unless the terminal theorem is " ++
      "proved locally or a pinned external proof is imported and checked.",
    repoLocalStatus := "open_not_completed",
    localAnchors := [
      "c003FullLiouvilleDebtClass",
      "c003FullLiouvilleCompleted",
      "c003FullLiouville_not_completed",
      "c003FormalizationBlockers"
    ],
    remainingLeaves := [
      "run repo-local Lean validation after any terminal theorem or wrapper is added",
      "pin/import/check any external Lean proof before it can count as completed",
      "leave external anchor-only evidence open with a concrete integration blocker"
    ]
  }
]

/-- The C004 theorem-tree split has exactly the requested seven packages. -/
theorem c004TheoremTreeSplit_names :
    c004TheoremTreeSplit.map C004TheoremTreePackage.canonicalName = [
      "statement_normalization",
      "measure_object_model",
      "symplectic_linear_substrate",
      "flow_to_measure_bridge",
      "jacobian_or_symplectic_volume_bridge",
      "special_models",
      "repo_local_closure_gate"
    ] :=
  rfl

/-- The C004 theorem-tree split records seven public packages. -/
theorem c004TheoremTreeSplit_length :
    c004TheoremTreeSplit.length = 7 :=
  rfl

/-! ## C005 unchecked public leaves -/

/--
Unchecked public leaf metadata for the Hamiltonian Liouville theorem.

Each row is a future proof/API leaf required before the terminal theorem can
be claimed.  The rows are intentionally metadata: they do not assert existence
of the missing Hamiltonian-flow APIs or the final `MeasurePreserving` theorem.
-/
structure C005UncheckedPublicLeaf where
  canonicalName : String
  packageName : String
  requiredApiOrTheorem : String
  currentRepoLocalStatus : String
  debtClass : String
  completionGate : String
  localBudgetStatus : String

/--
Public C005 leaves requested for the Hamiltonian Liouville Stage1 split.

All five leaves remain unchecked formalization debt.  A future public
completion claim must replace these metadata rows by repo-local checked
theorems, local wrappers over pinned mathlib, or pinned/vendored external
proofs that validate in this repository.
-/
def c005UncheckedPublicLeaves : List C005UncheckedPublicLeaf := [
  {
    canonicalName := "hamiltonian_vector_field_api",
    packageName := "flow_to_measure_bridge",
    requiredApiOrTheorem :=
      "Define the Hamiltonian vector field on the selected finite-dimensional phase space.",
    currentRepoLocalStatus := "unchecked_formalization_debt",
    debtClass := "formalization_debt",
    completionGate :=
      "replace proposition fields by a concrete checked vector-field API",
    localBudgetStatus := "unchecked_leaf_requires_future_<=100_step_ledger"
  },
  {
    canonicalName := "global_flow_existence_group_law",
    packageName := "flow_to_measure_bridge",
    requiredApiOrTheorem :=
      "Prove or import global flow existence, time-zero identity, and flow-add group law.",
    currentRepoLocalStatus := "unchecked_formalization_debt",
    debtClass := "formalization_debt",
    completionGate :=
      "validate global flow theorem locally or record a concrete integration blocker",
    localBudgetStatus := "unchecked_leaf_requires_future_<=100_step_ledger"
  },
  {
    canonicalName := "hamilton_equation_encoding",
    packageName := "flow_to_measure_bridge",
    requiredApiOrTheorem :=
      "Encode Hamilton equations for the chosen coordinate and differentiability model.",
    currentRepoLocalStatus := "unchecked_formalization_debt",
    debtClass := "formalization_debt",
    completionGate :=
      "connect the flow derivative to the Hamiltonian vector field in checked Lean",
    localBudgetStatus := "unchecked_leaf_requires_future_<=100_step_ledger"
  },
  {
    canonicalName := "divergence_free_or_symplectic_flow_proof",
    packageName := "jacobian_or_symplectic_volume_bridge",
    requiredApiOrTheorem :=
      "Prove Hamiltonian flow is divergence-free or symplectic in the selected model.",
    currentRepoLocalStatus := "unchecked_formalization_debt",
    debtClass := "formalization_debt",
    completionGate :=
      "supply a checked divergence-free/Jacobian or symplectic-flow proof",
    localBudgetStatus := "unchecked_leaf_requires_future_<=100_step_ledger"
  },
  {
    canonicalName := "measure_preserving_bridge",
    packageName := "jacobian_or_symplectic_volume_bridge",
    requiredApiOrTheorem :=
      "Bridge the checked flow theorem to `MeasurePreserving` for phase volume at every time.",
    currentRepoLocalStatus := "unchecked_formalization_debt",
    debtClass := "formalization_debt",
    completionGate :=
      "prove `PhaseVolumePreserved` from the selected analytic bridge and validate locally",
    localBudgetStatus := "unchecked_leaf_requires_future_<=100_step_ledger"
  }
]

/-- The C005 unchecked public leaves are exactly the requested five leaves. -/
theorem c005UncheckedPublicLeaves_names :
    c005UncheckedPublicLeaves.map C005UncheckedPublicLeaf.canonicalName = [
      "hamiltonian_vector_field_api",
      "global_flow_existence_group_law",
      "hamilton_equation_encoding",
      "divergence_free_or_symplectic_flow_proof",
      "measure_preserving_bridge"
    ] :=
  rfl

/-- The C005 unchecked public leaf table records five leaves. -/
theorem c005UncheckedPublicLeaves_length :
    c005UncheckedPublicLeaves.length = 5 :=
  rfl

/--
C005 does not claim terminal completion of Hamiltonian Liouville.

This checked flag prevents the metadata-only leaf table from being read as a
repo-local proof of the terminal theorem.
-/
def c005ClaimsTerminalCompletion : Bool :=
  false

/-- C005 terminal completion is intentionally false. -/
theorem c005ClaimsTerminalCompletion_eq_false :
    c005ClaimsTerminalCompletion = false :=
  rfl

/--
C005 repo-local integration-debt gate.

The current state has no completed external-anchor-only claim.  The public
leaves above remain unchecked `formalization_debt` until a local proof body,
pinned mathlib wrapper, or pinned/vendored external proof validates here.
-/
def c005RepoLocalIntegrationDebtGate : String :=
  "no_completed_state_retains_repo_local_integration_debt"

/-! ## C006 future-mathlib symplectic-volume audit -/

/--
C006 audit row for possible future mathlib upgrades relevant to the
Hamiltonian Liouville bridge.

Rows are evidence metadata.  They separate checked local wrappers from symbols
that were searched for but are absent in the current pinned mathlib snapshot.
-/
structure C006MathlibUpgradeAuditRow where
  canonicalName : String
  searchedFor : String
  currentPinnedResult : String
  repoLocalAction : String
  completionStatus : String

/--
Current C006 audit result.

The pinned mathlib snapshot still exports `SymplecticGroup.symplectic_det` as
an `IsUnit` determinant theorem and the source file still records
determinant-one as a TODO.  General Haar/Jacobian scaling APIs exist, but this
snapshot does not expose a symplectic-specific determinant-one theorem or a
volume-preserving linear symplectic map theorem that can be wrapped as the
Hamiltonian Liouville volume bridge.
-/
def c006MathlibUpgradeAudit : List C006MathlibUpgradeAuditRow := [
  {
    canonicalName := "symplectic_det_determinant_one_upgrade",
    searchedFor :=
      "SymplecticGroup.symplectic_det_eq_one / SymplecticGroup.det_eq_one / Matrix.symplecticGroup.det_eq_one",
    currentPinnedResult :=
      "absent; `SymplecticGroup.symplectic_det` has type `IsUnit A.det`",
    repoLocalAction :=
      "kept `symplecticMatrix_det_isUnit` and added `symplecticMatrix_det_ne_zero`",
    completionStatus :=
      "audited_no_upgrade_available"
  },
  {
    canonicalName := "linear_symplectic_volume_preserving_api",
    searchedFor :=
      "symplectic-specific MeasurePreserving or volume-preserving linear map theorem",
    currentPinnedResult :=
      "absent; only general Haar/Jacobian scaling APIs such as `MeasureTheory.Measure.map_linearMap_addHaar_eq_smul_addHaar` are available",
    repoLocalAction :=
      "did not assert MeasurePreserving for symplectic matrices without a checked determinant-one bridge",
    completionStatus :=
      "audited_no_upgrade_available"
  }
]

/-- C006 records exactly the two requested upgrade-audit branches. -/
theorem c006MathlibUpgradeAudit_names :
    c006MathlibUpgradeAudit.map C006MathlibUpgradeAuditRow.canonicalName = [
      "symplectic_det_determinant_one_upgrade",
      "linear_symplectic_volume_preserving_api"
    ] :=
  rfl

/-- C006 records two audit rows. -/
theorem c006MathlibUpgradeAudit_length :
    c006MathlibUpgradeAudit.length = 2 :=
  rfl

/-- C006 did not find a determinant-one symplectic theorem in the pinned snapshot. -/
def c006DeterminantOneUpgradeFound : Bool :=
  false

/-- C006 did not find a symplectic-specific volume-preserving linear map theorem. -/
def c006LinearSymplecticMeasurePreservingFound : Bool :=
  false

/-- C006 terminal theorem completion remains false. -/
def c006ClaimsTerminalCompletion : Bool :=
  false

/-- The determinant-one upgrade flag is intentionally false for this snapshot. -/
theorem c006DeterminantOneUpgradeFound_eq_false :
    c006DeterminantOneUpgradeFound = false :=
  rfl

/-- The linear symplectic measure-preserving upgrade flag is intentionally false. -/
theorem c006LinearSymplecticMeasurePreservingFound_eq_false :
    c006LinearSymplecticMeasurePreservingFound = false :=
  rfl

/-- C006 does not claim terminal Hamiltonian Liouville completion. -/
theorem c006ClaimsTerminalCompletion_eq_false :
    c006ClaimsTerminalCompletion = false :=
  rfl

/--
C006 repo-local integration-debt gate.

No external anchor-only proof or unwrapped future-mathlib theorem is being
claimed as completed.  The remaining bridge from symplectic data to phase
volume preservation is still `formalization_debt`.
-/
def c006RepoLocalIntegrationDebtGate : String :=
  "no_completed_state_retains_repo_local_integration_debt"

/-- The C003 statement-boundary list records exactly eight checked declarations. -/
theorem c003CompiledStatementBoundary_length :
    c003CompiledStatementBoundary.length = 8 :=
  rfl

/-- The C003 substrate-wrapper list records exactly seven checked declarations. -/
theorem c003CompiledSubstrateWrappers_length :
    c003CompiledSubstrateWrappers.length = 7 :=
  rfl

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.MeasurePreserving",
  "MeasureTheory.MeasurePreserving.measure_preimage",
  "MeasureTheory.MeasurePreserving.quasiMeasurePreserving",
  "MeasureTheory.volume",
  "Matrix.symplecticGroup",
  "Matrix.J",
  "SymplecticGroup.J_mem",
  "SymplecticGroup.symplectic_det",
  "MeasureTheory.addHaar_image_linearMap",
  "MeasureTheory.LinearMap.quasiMeasurePreserving"
]

/--
Search terms used to distinguish the checked substrate from a missing terminal
Hamiltonian Liouville theorem.
-/
def absentTerminalSearchTerms : List String := [
  "Liouville theorem",
  "Liouville measure",
  "phase-space volume",
  "Hamiltonian flow",
  "Hamiltonian vector field",
  "symplectic flow",
  "volume preserving flow",
  "divergence-free Hamiltonian vector field"
]

/-! ## C007 external terminal-proof audit -/

/--
C007 external Lean 4 audit row for a terminal Hamiltonian-flow Liouville
proof search.

Rows are repository-level evidence metadata.  They do not import an external
proof and do not assert terminal theorem completion.
-/
structure C007ExternalLeanAuditRow where
  sourceName : String
  sourceKind : String
  revisionOrAccessResult : String
  searchedFor : List String
  terminalProofResult : String
  repoLocalAction : String
  integrationDebtStatus : String

/--
C007 primary-source audit result for the Hamiltonian Liouville terminal proof.

The audit checked the local vendored mathlib snapshot, the active local Lake
mathlib dependency, upstream mathlib HEAD, and the SciLean Lean 4 source tree.
No terminal theorem proving that Hamiltonian flow preserves phase-space volume
was located, so there is no external Lean proof to pin/import/check in this
child pass.  Search-service failures are recorded as non-evidence and are not
counted as proof anchors.
-/
def c007ExternalLeanAudit : List C007ExternalLeanAuditRow := [
  {
    sourceName := "local vendored mathlib4",
    sourceKind := "primary Lean 4 source dependency",
    revisionOrAccessResult := "dc7664a302ed42b3acb861ceeacdb5e866358313",
    searchedFor := absentTerminalSearchTerms,
    terminalProofResult :=
      "not found; matches are other Liouville theorems or substrate APIs, not Hamiltonian-flow volume preservation",
    repoLocalAction :=
      "no import added; kept terminal theorem under formalization_debt",
    integrationDebtStatus :=
      "no_external_upstream_anchor_only_claim"
  },
  {
    sourceName := "local Lake mathlib package",
    sourceKind := "primary Lean 4 source dependency",
    revisionOrAccessResult := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    searchedFor := absentTerminalSearchTerms,
    terminalProofResult :=
      "not found; no Hamiltonian-flow Liouville theorem was located in the local package tree",
    repoLocalAction :=
      "no import added; no completed claim made",
    integrationDebtStatus :=
      "no_external_upstream_anchor_only_claim"
  },
  {
    sourceName := "upstream mathlib4",
    sourceKind := "primary Lean 4 source repository",
    revisionOrAccessResult := "5198248eff75ab2950d71ba7a777c8789a9aac2e",
    searchedFor := absentTerminalSearchTerms,
    terminalProofResult :=
      "not found; search hits are complex-analysis, differential-field, and number-theory Liouville files",
    repoLocalAction :=
      "no pin/import/check action available because no terminal proof candidate was found",
    integrationDebtStatus :=
      "no_external_upstream_anchor_only_claim"
  },
  {
    sourceName := "SciLean",
    sourceKind := "primary Lean 4 scientific-computing source repository",
    revisionOrAccessResult := "95f8119a2884e9c41f82136523bd5568ea7075c5",
    searchedFor := absentTerminalSearchTerms,
    terminalProofResult :=
      "not found; the only symplectic match in the audited tree is an ODE solver comment",
    repoLocalAction :=
      "no pin/import/check action available because no terminal proof candidate was found",
    integrationDebtStatus :=
      "no_external_upstream_anchor_only_claim"
  },
  {
    sourceName := "GitHub code search API",
    sourceKind := "search service, not proof source",
    revisionOrAccessResult := "rate_limited_for_unauthenticated_request",
    searchedFor := absentTerminalSearchTerms,
    terminalProofResult :=
      "no usable primary theorem evidence obtained from this service during the child pass",
    repoLocalAction :=
      "did not treat search-service output as an external proof anchor",
    integrationDebtStatus :=
      "not_evidence_for_completion"
  }
]

/-- C007 records five audit rows. -/
theorem c007ExternalLeanAudit_length :
    c007ExternalLeanAudit.length = 5 :=
  rfl

/-- C007 found no terminal external Hamiltonian-flow Liouville proof. -/
def c007TerminalExternalProofFound : Bool :=
  false

/-- C007 does not claim terminal Hamiltonian Liouville completion. -/
def c007ClaimsTerminalCompletion : Bool :=
  false

/-- The C007 external terminal-proof flag is intentionally false. -/
theorem c007TerminalExternalProofFound_eq_false :
    c007TerminalExternalProofFound = false :=
  rfl

/-- C007 terminal completion remains intentionally false. -/
theorem c007ClaimsTerminalCompletion_eq_false :
    c007ClaimsTerminalCompletion = false :=
  rfl

/--
C007 repo-local integration-debt gate.

No external proof was found and left as a completed anchor-only claim.  If a
future terminal Lean proof is found, this gate requires pin/import/check or a
concrete integration blocker before any completion claim.
-/
def c007RepoLocalIntegrationDebtGate : String :=
  "no_completed_state_retains_repo_local_integration_debt"

/-! ## C008 name-collision notes -/

/--
C008 name-collision note for Liouville/Hamiltonian search hits.

Rows in this structure are public-surface disambiguation metadata.  They keep
nearby mathlib theorem families from being mistaken for the Hamiltonian
phase-space volume theorem tracked by this Stage1 slot.
-/
structure C008NameCollisionNote where
  collisionFamily : String
  primaryModuleOrApi : String
  whyNotTarget : String
  publicSurfaceAction : String

/--
Public C008 name-collision exclusions for the Hamiltonian Liouville slot.

These rows are intentionally negative metadata.  They do not supply a terminal
Hamiltonian-flow proof, and they must not be counted as external anchors for
phase-space volume preservation.
-/
def c008NameCollisionNotes : List C008NameCollisionNote := [
  {
    collisionFamily := "complex_analysis_liouville",
    primaryModuleOrApi := "Mathlib.Analysis.Complex.Liouville",
    whyNotTarget :=
      "bounded entire complex-differentiable functions are constant; this is not a Hamiltonian flow or phase-volume theorem",
    publicSurfaceAction :=
      "record as a non-target Liouville theorem when auditing Lean search hits"
  },
  {
    collisionFamily := "differential_field_liouville",
    primaryModuleOrApi := "Mathlib.FieldTheory.Differential.Liouville / IsLiouville",
    whyNotTarget :=
      "differential-field antiderivative structure theorem; this is not a measure-preserving phase-space flow theorem",
    publicSurfaceAction :=
      "record as a non-target Liouville theorem when auditing algebra/differential-field hits"
  },
  {
    collisionFamily := "graph_theory_hamiltonian",
    primaryModuleOrApi :=
      "Mathlib.Combinatorics.SimpleGraph.Hamiltonian / SimpleGraph.IsHamiltonian",
    whyNotTarget :=
      "Hamiltonian paths, cycles, and graphs are named after Hamiltonian graph theory; they are not Hamiltonian mechanics APIs",
    publicSurfaceAction :=
      "record as a non-target Hamiltonian API when auditing search hits"
  }
]

/-- C008 records exactly the three requested name-collision families. -/
theorem c008NameCollisionNotes_families :
    c008NameCollisionNotes.map C008NameCollisionNote.collisionFamily = [
      "complex_analysis_liouville",
      "differential_field_liouville",
      "graph_theory_hamiltonian"
    ] :=
  rfl

/-- C008 records three name-collision notes. -/
theorem c008NameCollisionNotes_length :
    c008NameCollisionNotes.length = 3 :=
  rfl

/-- C008 name-collision metadata does not claim terminal Liouville completion. -/
def c008ClaimsTerminalCompletion : Bool :=
  false

/-- C008 terminal completion remains intentionally false. -/
theorem c008ClaimsTerminalCompletion_eq_false :
    c008ClaimsTerminalCompletion = false :=
  rfl

/--
C008 repo-local integration-debt gate.

The collision notes are negative disambiguation metadata, not proof anchors.
No completed state is inferred from complex-analysis Liouville, differential
field Liouville, or graph-theory Hamiltonian APIs.
-/
def c008RepoLocalIntegrationDebtGate : String :=
  "no_completed_state_retains_repo_local_integration_debt"

/-! ## Audit probes -/

#check StatementShape
#check PhaseVolumePreserved
#check PhaseVolumePreserved.measure_preimage
#check identityPhaseVolumePreserved
#check Matrix.symplecticGroup
#check SymplecticGroup.symplectic_det
#check symplecticMatrix_det_ne_zero
#check c002PinnedMathlibRevision
#check c002PublicAnchorTable
#check c003FullLiouvilleDebtClass
#check c003FullLiouville_not_completed
#check c003CompiledStatementBoundary
#check c003CompiledSubstrateWrappers
#check c003FormalizationBlockers
#check C004TheoremTreePackage
#check c004TheoremTreeSplit
#check c004TheoremTreeSplit_names
#check c004TheoremTreeSplit_length
#check C005UncheckedPublicLeaf
#check c005UncheckedPublicLeaves
#check c005UncheckedPublicLeaves_names
#check c005UncheckedPublicLeaves_length
#check c005ClaimsTerminalCompletion_eq_false
#check c005RepoLocalIntegrationDebtGate
#check C006MathlibUpgradeAuditRow
#check c006MathlibUpgradeAudit
#check c006MathlibUpgradeAudit_names
#check c006MathlibUpgradeAudit_length
#check c006DeterminantOneUpgradeFound_eq_false
#check c006LinearSymplecticMeasurePreservingFound_eq_false
#check c006ClaimsTerminalCompletion_eq_false
#check c006RepoLocalIntegrationDebtGate
#check C007ExternalLeanAuditRow
#check c007ExternalLeanAudit
#check c007ExternalLeanAudit_length
#check c007TerminalExternalProofFound_eq_false
#check c007ClaimsTerminalCompletion_eq_false
#check c007RepoLocalIntegrationDebtGate
#check C008NameCollisionNote
#check c008NameCollisionNotes
#check c008NameCollisionNotes_families
#check c008NameCollisionNotes_length
#check c008ClaimsTerminalCompletion_eq_false
#check c008RepoLocalIntegrationDebtGate

end AwesomeTheorems.Stage1.S1_M_189
