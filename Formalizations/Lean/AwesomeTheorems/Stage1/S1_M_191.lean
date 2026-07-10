import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.InnerProductSpace.LinearPMap
import Mathlib.Analysis.InnerProductSpace.l2Space
import Mathlib.Analysis.Normed.Operator.FredholmAlternative
import Mathlib.Algebra.Star.CHSH

/-!
# S1-M-191 / THM-M-1523: Mathematical foundations of quantum mechanics

This Stage1 artifact records a conservative Lean boundary for the Hilbert-space
formalism of quantum mechanics.  The informal source phrase is normalized as:
pure states are unit vectors in a complex Hilbert space, bounded observables are
self-adjoint continuous linear operators, transition probabilities are Born
weights, and spectral/eigenvalue facts are delegated to mathlib where available.

The file proves only low-risk substrate lemmas.  It does not claim a terminal
formalization of the full physical theory, the spectral theorem for all
self-adjoint unbounded operators, or the measurement postulates.
-/

noncomputable section

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_191

universe u v

/-- Bounded linear operators on a complex Hilbert space. -/
abbrev BoundedOperator
    (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H] : Type u :=
  H →L[ℂ] H

/-- A normalized pure state vector. -/
def StateVector (H : Type u) [NormedAddCommGroup H] : Type u :=
  {psi : H // ‖psi‖ = 1}

/-- A bounded observable is represented by a self-adjoint bounded operator. -/
structure BoundedObservable
    (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] where
  op : BoundedOperator H
  selfAdjoint : IsSelfAdjoint op

/-- The algebraic spectrum of a bounded observable/operator. -/
def OperatorSpectrum
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (T : BoundedOperator H) : Set ℂ :=
  spectrum ℂ T

/-- Transition amplitude between two vectors. -/
def ProbabilityAmplitude
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (psi phi : H) : ℂ :=
  inner ℂ phi psi

/-- Born transition weight between two vectors. -/
def BornWeight
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (psi phi : H) : ℝ :=
  ‖ProbabilityAmplitude psi phi‖ ^ 2

/-- Born weight for a projection-like bounded operator applied to a vector state. -/
def ProjectionBornWeight
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (P : BoundedOperator H) (psi : H) : ℝ :=
  ‖P psi‖ ^ 2

/-- A bounded operator is unitary when its adjoint is a two-sided inverse. -/
def IsUnitaryOperator
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (U : BoundedOperator H) : Prop :=
  ContinuousLinearMap.adjoint U ∘L U = ContinuousLinearMap.id ℂ H ∧
    U ∘L ContinuousLinearMap.adjoint U = ContinuousLinearMap.id ℂ H

/--
Data for an abstract Hilbert-space quantum model.

The first fields are concrete mathlib objects.  The final proposition fields
mark the physical/modeling postulates that are not closed by this Stage1 file.
-/
structure HilbertQuantumData
    (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] :
    Type u where
  state : StateVector H
  hamiltonian : BoundedObservable H
  timeEvolution : ℝ → BoundedOperator H
  wellFormedHilbertModel : Prop
  dynamicsGeneratedByHamiltonian : Prop
  bornRuleForProjectiveMeasurements : Prop
  spectralMeasurementPostulate : Prop
  unboundedObservableExtension : Prop
  unitaryEvolution : ∀ t : ℝ, IsUnitaryOperator (timeEvolution t)

/-- Hypotheses for the normalized Hilbert-space formalism statement. -/
def HilbertQuantumHypotheses
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (D : HilbertQuantumData H) : Prop :=
  D.wellFormedHilbertModel ∧ D.dynamicsGeneratedByHamiltonian

/-- Conclusions expected from a completed formal Hilbert-space quantum model. -/
def HilbertQuantumConclusion
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (D : HilbertQuantumData H) : Prop :=
  D.bornRuleForProjectiveMeasurements ∧
    D.spectralMeasurementPostulate ∧
      D.unboundedObservableExtension ∧
        (∀ t : ℝ, IsUnitaryOperator (D.timeEvolution t)) ∧
          IsSelfAdjoint D.hamiltonian.op

/--
Stage1 normalized statement shape.

This is a statement boundary for the Hilbert-space formalism.  A terminal proof
would need to supply the physical/modeling postulates and the unbounded
operator/spectral-theorem bridge, not merely the bounded wrappers below.
-/
def StatementShape : Prop :=
  ∀ (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H],
    ∀ D : HilbertQuantumData H,
      HilbertQuantumHypotheses D → HilbertQuantumConclusion D

/-- The statement shape unfolds to the expected quantified implication. -/
theorem statementShape_iff_forall_data :
    StatementShape.{u} ↔
      ∀ (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H],
        ∀ D : HilbertQuantumData H,
          HilbertQuantumHypotheses D → HilbertQuantumConclusion D :=
  Iff.rfl

/-- A state vector carries its unit-norm proof. -/
theorem StateVector.norm_eq_one
    {H : Type u} [NormedAddCommGroup H] (psi : StateVector H) :
    ‖psi.1‖ = 1 :=
  psi.property

/-- A bounded observable exposes its self-adjointness proof. -/
theorem BoundedObservable.isSelfAdjoint
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (A : BoundedObservable H) :
    IsSelfAdjoint A.op :=
  A.selfAdjoint

/-- Born weights are nonnegative by construction. -/
theorem BornWeight.nonneg
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (psi phi : H) :
    0 ≤ BornWeight psi phi :=
  sq_nonneg _

/-- Born weights between unit vectors are at most one by Cauchy-Schwarz. -/
theorem BornWeight.le_one_of_unit
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {psi phi : H} (hpsi : ‖psi‖ = 1) (hphi : ‖phi‖ = 1) :
    BornWeight psi phi ≤ 1 := by
  have h : ‖ProbabilityAmplitude psi phi‖ ≤ 1 := by
    simpa [ProbabilityAmplitude, hpsi, hphi] using
      norm_inner_le_norm (𝕜 := ℂ) phi psi
  have hn : 0 ≤ ‖ProbabilityAmplitude psi phi‖ := norm_nonneg _
  unfold BornWeight
  nlinarith

/-- Born weights between normalized state vectors are valid probabilities. -/
theorem StateVector.bornWeight_mem_unit_interval
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (psi phi : StateVector H) :
    0 ≤ BornWeight psi.1 phi.1 ∧
      BornWeight psi.1 phi.1 ≤ 1 :=
  ⟨BornWeight.nonneg _ _,
    BornWeight.le_one_of_unit (StateVector.norm_eq_one psi) (StateVector.norm_eq_one phi)⟩

/-- Projection-style Born weights are nonnegative. -/
theorem ProjectionBornWeight.nonneg
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (P : BoundedOperator H) (psi : H) :
    0 ≤ ProjectionBornWeight P psi :=
  sq_nonneg _

/-- The identity bounded operator is unitary. -/
theorem id_isUnitaryOperator
    (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] :
    IsUnitaryOperator (ContinuousLinearMap.id ℂ H) := by
  simp [IsUnitaryOperator]

/-- An eigenvalue of the underlying endomorphism belongs to its algebraic spectrum. -/
theorem hasEigenvalue_mem_moduleEnd_spectrum
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    {T : H →L[ℂ] H} {mu : ℂ}
    (hmu : Module.End.HasEigenvalue (T : Module.End ℂ H) mu) :
    mu ∈ spectrum ℂ (T : Module.End ℂ H) :=
  Module.End.HasEigenvalue.mem_spectrum hmu

/-- Checked wrapper: nonzero spectral points of a compact operator are eigenvalues. -/
theorem compact_operator_hasEigenvalue_iff_mem_spectrum
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    {T : H →L[ℂ] H} {mu : ℂ}
    (hT : IsCompactOperator (T : H → H)) (hmu : mu ≠ 0) :
    Module.End.HasEigenvalue (T : Module.End ℂ H) mu ↔ mu ∈ OperatorSpectrum T :=
  IsCompactOperator.hasEigenvalue_iff_mem_spectrum hT hmu

/-- A Hilbert basis supplies an orthonormal family. -/
theorem HilbertBasis.orthonormal_wrapper
    {ι : Type v}
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (b : HilbertBasis ι ℂ H) :
    Orthonormal ℂ b :=
  b.orthonormal

/-- The conclusion exposes the Born-rule postulate field. -/
theorem HilbertQuantumConclusion.bornRule
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    {D : HilbertQuantumData H}
    (h : HilbertQuantumConclusion D) :
    D.bornRuleForProjectiveMeasurements :=
  h.1

/-- The conclusion exposes unitary time evolution. -/
theorem HilbertQuantumConclusion.unitaryEvolution
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    {D : HilbertQuantumData H}
    (h : HilbertQuantumConclusion D) :
    ∀ t : ℝ, IsUnitaryOperator (D.timeEvolution t) :=
  h.2.2.2.1

/-- The conclusion exposes self-adjointness of the Hamiltonian. -/
theorem HilbertQuantumConclusion.hamiltonian_selfAdjoint
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    {D : HilbertQuantumData H}
    (h : HilbertQuantumConclusion D) :
    IsSelfAdjoint D.hamiltonian.op :=
  h.2.2.2.2

/-! ## Audit probes -/

#check StateVector
#check BoundedObservable
#check ProbabilityAmplitude
#check BornWeight
#check ProjectionBornWeight
#check IsUnitaryOperator
#check StatementShape
#check ContinuousLinearMap.adjoint
#check LinearPMap.IsFormalAdjoint
#check IsSelfAdjoint.isClosed
#check norm_inner_le_norm
#check spectrum
#check Module.End.HasEigenvalue.mem_spectrum
#check IsCompactOperator.hasEigenvalue_iff_mem_spectrum
#check HilbertBasis
#check HilbertBasis.orthonormal
#check IsCHSHTuple
#check CHSH_inequality_of_comm
#check tsirelson_inequality

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.InnerProductSpace.Basic",
  "Mathlib.Analysis.InnerProductSpace.Adjoint",
  "Mathlib.Analysis.InnerProductSpace.Symmetric",
  "Mathlib.Analysis.InnerProductSpace.Positive",
  "Mathlib.Analysis.InnerProductSpace.LinearPMap",
  "Mathlib.Analysis.InnerProductSpace.l2Space",
  "Mathlib.Analysis.InnerProductSpace.Spectrum",
  "Mathlib.Analysis.Normed.Operator.Compact",
  "Mathlib.Analysis.Normed.Operator.FredholmAlternative",
  "Mathlib.Algebra.Algebra.Spectrum.Basic",
  "Mathlib.LinearAlgebra.Eigenspace.Basic",
  "Mathlib.Algebra.Star.CHSH"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "InnerProductSpace",
  "ContinuousLinearMap.adjoint",
  "IsSelfAdjoint",
  "spectrum",
  "Module.End.HasEigenvalue.mem_spectrum",
  "IsCompactOperator.hasEigenvalue_iff_mem_spectrum",
  "HilbertBasis",
  "HilbertBasis.orthonormal",
  "norm_inner_le_norm",
  "LinearPMap.IsFormalAdjoint",
  "IsSelfAdjoint.isClosed",
  "IsCHSHTuple",
  "CHSH_inequality_of_comm",
  "tsirelson_inequality"
]

/-- Exact pinned mathlib revision audited for the bounded Hilbert-space substrate. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Audit rows for the mathlib families used by the public `S1-M-191-public-002` slot. -/
def pinnedMathlibAnchorFamilies : List (String × List String) := [
  ("Hilbert-space adjoints", [
    "ContinuousLinearMap.adjoint",
    "IsSelfAdjoint",
    "IsSelfAdjoint.isClosed"
  ]),
  ("Hilbert bases", [
    "HilbertBasis",
    "HilbertBasis.orthonormal"
  ]),
  ("Algebraic spectra", [
    "spectrum",
    "Module.End.HasEigenvalue.mem_spectrum"
  ]),
  ("Compact-operator eigenvalue/spectrum wrappers", [
    "IsCompactOperator.hasEigenvalue_iff_mem_spectrum"
  ]),
  ("CHSH/Tsirelson quantum-foundation anchors", [
    "IsCHSHTuple",
    "CHSH_inequality_of_comm",
    "tsirelson_inequality"
  ])
]

/--
Search terms that did not locate a terminal Lean theorem named as the full
Hilbert-space formalism of quantum mechanics in the pinned local mathlib tree.
-/
def absentTerminalSearchTerms : List String := [
  "quantum mechanics",
  "Hilbert space formalism",
  "Born rule",
  "measurement postulate",
  "state vector",
  "wave function",
  "Schrodinger equation",
  "self-adjoint observable",
  "projection-valued measure",
  "spectral theorem quantum"
]

/-! ## C004 full-formalism debt gate -/

/--
Machine-readable C004 boundary for the full Hilbert-space formalism of
quantum mechanics.

The checked bounded substrate above is not enough to close the physical
formalism.  These fields stay false until the corresponding packages are
supplied by local proof bodies, local wrappers over pinned dependencies, or
pinned/imported/checked external proof closures.
-/
structure FullQuantumFormalismGate : Type where
  hasUnboundedObservablePackage : Bool
  hasProjectionValuedMeasurementPackage : Bool
  hasSpectralTheoremPackage : Bool
  hasSchrodingerDynamicsPackage : Bool
  mayMarkFullFormalismComplete : Bool
  debtClass : String
  machineStatus : String

/-- C004 gate: keep the full quantum-mechanics formalism open. -/
def c004FullQuantumFormalismGate : FullQuantumFormalismGate where
  hasUnboundedObservablePackage := false
  hasProjectionValuedMeasurementPackage := false
  hasSpectralTheoremPackage := false
  hasSchrodingerDynamicsPackage := false
  mayMarkFullFormalismComplete := false
  debtClass := "formalization_debt"
  machineStatus := "not_repo_local_closed"

/--
Checked C004 boundary: the full quantum-mechanics formalism is not complete in
this artifact, and the remaining debt is formalization work rather than a
completed-state repo-local integration debt.
-/
theorem c004FullQuantumFormalismGate_blocks_completion :
    c004FullQuantumFormalismGate.mayMarkFullFormalismComplete = false ∧
    c004FullQuantumFormalismGate.debtClass = "formalization_debt" ∧
    c004FullQuantumFormalismGate.machineStatus = "not_repo_local_closed" := by
  exact ⟨rfl, rfl, rfl⟩

/-- Checked C004 boundary: all required full-formalism packages remain absent. -/
theorem c004FullQuantumFormalismGate_missing_core_packages :
    c004FullQuantumFormalismGate.hasUnboundedObservablePackage = false ∧
    c004FullQuantumFormalismGate.hasProjectionValuedMeasurementPackage = false ∧
    c004FullQuantumFormalismGate.hasSpectralTheoremPackage = false ∧
    c004FullQuantumFormalismGate.hasSchrodingerDynamicsPackage = false := by
  exact ⟨rfl, rfl, rfl, rfl⟩

/-- Concrete unchecked leaves needed before the full formalism can close. -/
def c004QuantumFormalizationDebtLeaves : List String := [
  "supply unbounded self-adjoint observable and closed-operator packages",
  "supply projection-valued measurement and Born-rule packages",
  "supply spectral theorem and spectral-measure bridge packages",
  "supply Hamiltonian-generated unitary evolution and Schrodinger dynamics packages"
]

#check FullQuantumFormalismGate
#check c004FullQuantumFormalismGate
#check c004FullQuantumFormalismGate_blocks_completion
#check c004FullQuantumFormalismGate_missing_core_packages
#check c004QuantumFormalizationDebtLeaves

/-! ## C005 theorem-tree package split -/

/--
Machine-readable row for the C005 theorem-tree split.

`localClosure` records whether the package has a checked repo-local closure for
the package's current Stage1 scope.  Open bridge packages therefore remain
`false` even though they are named as required future proof packages.
-/
structure TheoremTreePackage : Type where
  packageName : String
  machineStatus : String
  debtClass : String
  localClosure : Bool
  checkedLeafIds : List String
  uncheckedLeafIds : List String
deriving Repr, DecidableEq

/-- C005 theorem-tree split requested by the public Stage1 backfill line. -/
def c005TheoremTreeSplit : List TheoremTreePackage := [
  {
    packageName := "statement_normalization",
    machineStatus := "local_proof_body",
    debtClass := "no_debt",
    localClosure := true,
    checkedLeafIds := [
      "S1-M-191.L001",
      "S1-M-191.L002",
      "S1-M-191.L003"
    ],
    uncheckedLeafIds := []
  },
  {
    packageName := "mathlib_object_model",
    machineStatus := "local_wrapper_upstream_mathlib",
    debtClass := "no_debt",
    localClosure := true,
    checkedLeafIds := [
      "S1-M-191.L004",
      "S1-M-191.L017",
      "S1-M-191.L018"
    ],
    uncheckedLeafIds := []
  },
  {
    packageName := "state_probability_substrate",
    machineStatus := "local_proof_body",
    debtClass := "no_debt",
    localClosure := true,
    checkedLeafIds := [
      "S1-M-191.L005",
      "S1-M-191.L006",
      "S1-M-191.L007",
      "S1-M-191.L008",
      "S1-M-191.L009"
    ],
    uncheckedLeafIds := []
  },
  {
    packageName := "operator_substrate",
    machineStatus := "local_wrapper_upstream_mathlib",
    debtClass := "no_debt",
    localClosure := true,
    checkedLeafIds := [
      "S1-M-191.L010",
      "S1-M-191.L011",
      "S1-M-191.L012",
      "S1-M-191.L013",
      "S1-M-191.L014",
      "S1-M-191.L015"
    ],
    uncheckedLeafIds := []
  },
  {
    packageName := "quantum_foundation_adjacent_anchor",
    machineStatus := "local_wrapper_upstream_mathlib",
    debtClass := "no_debt",
    localClosure := true,
    checkedLeafIds := [
      "S1-M-191.L016"
    ],
    uncheckedLeafIds := []
  },
  {
    packageName := "unbounded_and_measurement_bridge",
    machineStatus := "not_repo_local_closed",
    debtClass := "formalization_debt",
    localClosure := false,
    checkedLeafIds := [],
    uncheckedLeafIds := [
      "S1-M-191.L019",
      "S1-M-191.L020",
      "S1-M-191.L021"
    ]
  },
  {
    packageName := "dynamics_bridge",
    machineStatus := "not_repo_local_closed",
    debtClass := "formalization_debt",
    localClosure := false,
    checkedLeafIds := [],
    uncheckedLeafIds := [
      "S1-M-191.L022",
      "S1-M-191.L023"
    ]
  }
]

/-- C005 package names, in the public theorem-tree order. -/
theorem c005TheoremTreeSplit_packageNames :
    c005TheoremTreeSplit.map TheoremTreePackage.packageName = [
      "statement_normalization",
      "mathlib_object_model",
      "state_probability_substrate",
      "operator_substrate",
      "quantum_foundation_adjacent_anchor",
      "unbounded_and_measurement_bridge",
      "dynamics_bridge"
    ] :=
  rfl

/-- C005 gate: no package row is closed by retaining repo-local integration debt. -/
theorem c005TheoremTreeSplit_no_repoLocalIntegrationDebt :
    ¬ "repo_local_integration_debt" ∈
      c005TheoremTreeSplit.map TheoremTreePackage.debtClass := by
  simp [c005TheoremTreeSplit]

/-- C005 gate: the two bridge packages remain open formalization debt. -/
theorem c005TheoremTreeSplit_openBridgePackages :
    c005TheoremTreeSplit.map
        (fun P => (P.packageName, P.machineStatus, P.debtClass, P.localClosure)) = [
      ("statement_normalization", "local_proof_body", "no_debt", true),
      ("mathlib_object_model", "local_wrapper_upstream_mathlib", "no_debt", true),
      ("state_probability_substrate", "local_proof_body", "no_debt", true),
      ("operator_substrate", "local_wrapper_upstream_mathlib", "no_debt", true),
      ("quantum_foundation_adjacent_anchor", "local_wrapper_upstream_mathlib", "no_debt", true),
      ("unbounded_and_measurement_bridge", "not_repo_local_closed", "formalization_debt", false),
      ("dynamics_bridge", "not_repo_local_closed", "formalization_debt", false)
    ] :=
  rfl

#check TheoremTreePackage
#check c005TheoremTreeSplit
#check c005TheoremTreeSplit_packageNames
#check c005TheoremTreeSplit_no_repoLocalIntegrationDebt
#check c005TheoremTreeSplit_openBridgePackages

/-! ## C006 unchecked public leaves -/

/--
An unbounded self-adjoint operator wrapper using mathlib's `LinearPMap` API.

This is a generic object-model anchor only.  It does not construct the
quantum-mechanical Hamiltonians, projection-valued measures, spectral measures,
Stone-theorem unitary group, or Schrodinger-equation solution package needed
for the terminal Hilbert-space formalism.
-/
structure UnboundedSelfAdjointOperator
    (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] where
  op : H →ₗ.[ℂ] H
  selfAdjoint : IsSelfAdjoint op

/-- Checked generic bridge: a self-adjoint `LinearPMap` is closed. -/
theorem UnboundedSelfAdjointOperator.isClosed
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (A : UnboundedSelfAdjointOperator H) :
    A.op.IsClosed :=
  A.selfAdjoint.isClosed

/--
Unchecked public leaf metadata for the C006 public backfill.

Each row is intentionally `unchecked_formalization_debt`: it is an
integration-ready theorem-tree leaf, not a completed theorem.  `machineStatus`
therefore stays `not_repo_local_closed` until a local proof body, a local
wrapper over pinned mathlib, or a pinned/imported/checked external dependency
closes the row.
-/
structure QuantumUncheckedPublicLeaf where
  leafId : String
  packageName : String
  title : String
  status : String
  debtClass : String
  machineStatus : String
  localBudgetStepLimit : Nat
  closureRequirement : String
deriving Repr, DecidableEq

/--
C006 unchecked public leaves for the quantum-mechanics formalism frontier.

These five leaves are the public descendants requested by
`S1-M-191-public-006`.  The Lean file checks the metadata and the generic
`LinearPMap` closed-operator anchor, while leaving the mathematical packages
open as formalization debt.
-/
def c006UncheckedPublicLeaves : List QuantumUncheckedPublicLeaf := [
  {
    leafId := "S1-M-191.L019",
    packageName := "unbounded_and_measurement_bridge",
    title := "projection-valued measures",
    status := "unchecked_formalization_debt",
    debtClass := "formalization_debt",
    machineStatus := "not_repo_local_closed",
    localBudgetStepLimit := 100,
    closureRequirement :=
      "define projection-valued measures over a measurable outcome space, " ++
      "prove orthogonal-projection/idempotence and countable-additivity " ++
      "interfaces, and connect the resulting measure to Born probabilities"
  },
  {
    leafId := "S1-M-191.L020",
    packageName := "unbounded_and_measurement_bridge",
    title := "unbounded self-adjoint operators",
    status := "unchecked_formalization_debt",
    debtClass := "formalization_debt",
    machineStatus := "not_repo_local_closed",
    localBudgetStepLimit := 100,
    closureRequirement :=
      "upgrade the generic `LinearPMap` self-adjoint/closed anchor to the " ++
      "specific dense-domain observable and Hamiltonian operators required " ++
      "by the selected quantum model"
  },
  {
    leafId := "S1-M-191.L021",
    packageName := "unbounded_and_measurement_bridge",
    title := "LinearPMap closed-operator bridge",
    status := "unchecked_formalization_debt",
    debtClass := "formalization_debt",
    machineStatus := "not_repo_local_closed",
    localBudgetStepLimit := 100,
    closureRequirement :=
      "prove that the domain, adjoint, formal-adjoint, closure, and spectral " ++
      "interfaces for the selected unbounded operators are compatible with " ++
      "mathlib's `LinearPMap` API"
  },
  {
    leafId := "S1-M-191.L022",
    packageName := "dynamics_bridge",
    title := "Hamiltonian-generated unitary evolution",
    status := "unchecked_formalization_debt",
    debtClass := "formalization_debt",
    machineStatus := "not_repo_local_closed",
    localBudgetStepLimit := 100,
    closureRequirement :=
      "construct or import the Stone-theorem bridge assigning a strongly " ++
      "continuous one-parameter unitary group to the chosen self-adjoint " ++
      "Hamiltonian and prove that it agrees with the model's time evolution"
  },
  {
    leafId := "S1-M-191.L023",
    packageName := "dynamics_bridge",
    title := "Schrodinger equation closure",
    status := "unchecked_formalization_debt",
    debtClass := "formalization_debt",
    machineStatus := "not_repo_local_closed",
    localBudgetStepLimit := 100,
    closureRequirement :=
      "prove domain invariance, differentiability of the unitary orbit, the " ++
      "Schrodinger differential equation, and the initial-value closure for " ++
      "the selected Hamiltonian"
  }
]

/-- C006 has exactly the five requested unchecked public leaf titles. -/
theorem c006UncheckedPublicLeaves_titles :
    c006UncheckedPublicLeaves.map QuantumUncheckedPublicLeaf.title = [
      "projection-valued measures",
      "unbounded self-adjoint operators",
      "LinearPMap closed-operator bridge",
      "Hamiltonian-generated unitary evolution",
      "Schrodinger equation closure"
    ] :=
  rfl

/-- C006 rows are metadata only; every row remains unchecked formalization debt. -/
theorem c006UncheckedPublicLeaves_statuses :
    c006UncheckedPublicLeaves.map QuantumUncheckedPublicLeaf.status = [
      "unchecked_formalization_debt",
      "unchecked_formalization_debt",
      "unchecked_formalization_debt",
      "unchecked_formalization_debt",
      "unchecked_formalization_debt"
    ] :=
  rfl

/-- C006 rows do not retain repo-local integration debt as a completed state. -/
theorem c006UncheckedPublicLeaves_no_repoLocalIntegrationDebt :
    ¬ "repo_local_integration_debt" ∈
      c006UncheckedPublicLeaves.map QuantumUncheckedPublicLeaf.debtClass := by
  simp [c006UncheckedPublicLeaves]

/-- C006 rows are all bounded by the M0387 local leaf budget threshold. -/
theorem c006UncheckedPublicLeaves_budgetCaps :
    c006UncheckedPublicLeaves.map QuantumUncheckedPublicLeaf.localBudgetStepLimit =
      [100, 100, 100, 100, 100] :=
  rfl

#check UnboundedSelfAdjointOperator
#check UnboundedSelfAdjointOperator.isClosed
#check QuantumUncheckedPublicLeaf
#check c006UncheckedPublicLeaves
#check c006UncheckedPublicLeaves_titles
#check c006UncheckedPublicLeaves_statuses
#check c006UncheckedPublicLeaves_no_repoLocalIntegrationDebt
#check c006UncheckedPublicLeaves_budgetCaps

/-! ## C007 external terminal-proof integration gate -/

/--
External Lean 4 candidate status for the full quantum-mechanics formalism.

The `terminalFullFormalismProof` flag is deliberately stricter than
quantum-adjacent Hilbert-space or quantum-computing development: it requires a
proof of the selected terminal Hilbert-space formalism, including the unbounded
observable, projection-valued measurement, spectral theorem, and Schrodinger
dynamics bridges tracked above.
-/
structure ExternalQuantumFormalismCandidate where
  repo : String
  revision : String
  evidenceScope : String
  terminalFullFormalismProof : Bool
  pinnedImportedCheckedHere : Bool
  integrationBlocker : String
deriving Repr, DecidableEq

/--
C007 candidate anchors found by the 2026-05-01 public-source pass.

Both projects are quantum-adjacent Lean 4 developments, not terminal closures
for the full Hilbert-space quantum-mechanics formalism selected by this slot.
Therefore neither can be used as `external_upstream_pinned` evidence here.
-/
def c007ExternalQuantumCandidates : List ExternalQuantumFormalismCandidate := [
  {
    repo := "https://github.com/Timeroot/Lean-QuantumInfo",
    revision := "9b74fd907c9774ac092d5a6b4caa892edaf8a8e9",
    evidenceScope :=
      "finite-dimensional quantum information theory; README scope excludes " ++
      "general infinite-dimensional quantum theory and does not claim the " ++
      "terminal Hilbert-space formalism",
    terminalFullFormalismProof := false,
    pinnedImportedCheckedHere := false,
    integrationBlocker :=
      "scope mismatch: no identified theorem proving the selected terminal " ++
      "full quantum-mechanics formalism with unbounded observables, PVMs, " ++
      "spectral-measure bridge, and Schrodinger dynamics"
  },
  {
    repo := "https://github.com/Maokami/vqc_in_lean",
    revision := "00b7e012c2c867535f2f4561e5d931a336b5fc5d",
    evidenceScope :=
      "work-in-progress Lean 4 port of Verified Quantum Computing for " ++
      "quantum-program verification",
    terminalFullFormalismProof := false,
    pinnedImportedCheckedHere := false,
    integrationBlocker :=
      "scope mismatch: quantum-computing/program-verification foundation, " ++
      "not a terminal proof of the Hilbert-space quantum-mechanics formalism"
  }
]

/-- C007 searched terms for future authenticated external Lean 4 audits. -/
def c007ExternalAuditSearchTerms : List String := [
  "quantum mechanics",
  "Hilbert-space formalism",
  "Born rule",
  "projection-valued measure",
  "PVM",
  "self-adjoint observable",
  "unbounded operator",
  "spectral theorem quantum",
  "Schrodinger equation",
  "Hamiltonian-generated unitary evolution",
  "Stone theorem quantum"
]

/-- C007 records that authenticated GitHub code search was unavailable in this pass. -/
def c007AuthenticatedGitHubCodeSearchAvailable : Bool := false

/-- C007 records that this pass verified no terminal external closure to import. -/
def c007ExternalTerminalClosureVerifiedThisPass : Bool := false

/-- C007 records that no completed state retains repo-local integration debt. -/
def c007CompletedStateRetainsRepoLocalIntegrationDebt : Bool := false

/-- C007 candidate repositories inspected in this pass. -/
theorem c007ExternalQuantumCandidates_repos :
    c007ExternalQuantumCandidates.map ExternalQuantumFormalismCandidate.repo = [
      "https://github.com/Timeroot/Lean-QuantumInfo",
      "https://github.com/Maokami/vqc_in_lean"
    ] :=
  rfl

/-- C007 candidate revisions inspected in this pass. -/
theorem c007ExternalQuantumCandidates_revisions :
    c007ExternalQuantumCandidates.map ExternalQuantumFormalismCandidate.revision = [
      "9b74fd907c9774ac092d5a6b4caa892edaf8a8e9",
      "00b7e012c2c867535f2f4561e5d931a336b5fc5d"
    ] :=
  rfl

/-- C007 gate: no inspected candidate is a terminal full-formalism proof. -/
theorem c007ExternalQuantumCandidates_noTerminalClosure :
    c007ExternalQuantumCandidates.map
        ExternalQuantumFormalismCandidate.terminalFullFormalismProof =
      [false, false] :=
  rfl

/-- C007 gate: no inspected candidate is pinned/imported/checked in this repository. -/
theorem c007ExternalQuantumCandidates_notPinnedHere :
    c007ExternalQuantumCandidates.map
        ExternalQuantumFormalismCandidate.pinnedImportedCheckedHere =
      [false, false] :=
  rfl

/--
C007 gate: this child does not leave a completed state carrying repo-local
integration debt or anchor-only evidence.
-/
theorem c007IntegrationDebtGate :
    c007ExternalTerminalClosureVerifiedThisPass = false ∧
    c007CompletedStateRetainsRepoLocalIntegrationDebt = false :=
  ⟨rfl, rfl⟩

#check ExternalQuantumFormalismCandidate
#check c007ExternalQuantumCandidates
#check c007ExternalAuditSearchTerms
#check c007AuthenticatedGitHubCodeSearchAvailable
#check c007ExternalTerminalClosureVerifiedThisPass
#check c007CompletedStateRetainsRepoLocalIntegrationDebt
#check c007ExternalQuantumCandidates_repos
#check c007ExternalQuantumCandidates_revisions
#check c007ExternalQuantumCandidates_noTerminalClosure
#check c007ExternalQuantumCandidates_notPinnedHere
#check c007IntegrationDebtGate

end S1_M_191
end Stage1
end AwesomeTheorems
