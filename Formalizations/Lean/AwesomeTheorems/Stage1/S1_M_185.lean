import Mathlib.Analysis.ODE.Gronwall
import Mathlib.Analysis.ODE.PicardLindelof
import Mathlib.LinearAlgebra.SymplecticGroup

/-!
# S1-M-185 / THM-M-1516: Hamiltonian mechanics

This Stage1 artifact records a conservative Lean boundary for the classical
Hamiltonian form of mechanics.  The physical statement "classical mechanics has
a Hamiltonian formulation" is normalized here as an abstract canonical phase
space statement: a Hamiltonian, its gradient, the canonical symplectic matrix
`J`, Hamilton's ODE, and the expected outputs of symplectic flow, energy
conservation, and Euler-Lagrange equivalence.

The file does not claim a terminal derivation of mechanics.  It provides
checked mathlib anchors for the finite-dimensional canonical symplectic matrix
and for ODE uniqueness under a Lipschitz hypothesis.
-/

noncomputable section

open Matrix

namespace AwesomeTheorems.Stage1.S1_M_185

universe u

/-- Canonical finite-dimensional phase space with coordinates `(q, p)`. -/
abbrev CanonicalPhase (Q : Type u) : Type u :=
  Q ⊕ Q → ℝ

/-- A Hamiltonian is a real-valued function on canonical phase space. -/
abbrev Hamiltonian (Q : Type u) : Type u :=
  CanonicalPhase Q → ℝ

/--
The gradient-side interface for a Hamiltonian.  This is kept as explicit data
because the terminal statement still needs a differentiability package tying it
to Frechet derivatives of `Hamiltonian Q`.
-/
abbrev HamiltonianGradient (Q : Type u) : Type u :=
  CanonicalPhase Q → CanonicalPhase Q

/-- The canonical symplectic matrix on `(q, p)` coordinates. -/
def CanonicalSymplecticMatrix (Q : Type u) [DecidableEq Q] :
    Matrix (Q ⊕ Q) (Q ⊕ Q) ℝ :=
  Matrix.J Q ℝ

/-- Hamilton's vector field in canonical coordinates, `X_H = J * grad H`. -/
def HamiltonianVectorField
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    (gradH : HamiltonianGradient Q) (x : CanonicalPhase Q) :
    CanonicalPhase Q :=
  (CanonicalSymplecticMatrix Q).mulVec (gradH x)

/-- Hamilton's ODE on a chosen time domain. -/
def HamiltonianEquationOn
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    (gradH : HamiltonianGradient Q)
    (trajectory : ℝ → CanonicalPhase Q) (timeDomain : Set ℝ) : Prop :=
  ∀ t ∈ timeDomain,
    HasDerivWithinAt trajectory
      (HamiltonianVectorField gradH (trajectory t)) timeDomain t

/--
Data for an abstract Hamiltonian-mechanics statement in canonical
finite-dimensional phase space.

Concrete mathlib data:
* phase space is `Q ⊕ Q → ℝ`;
* `CanonicalSymplecticMatrix Q` is mathlib's `Matrix.J Q ℝ`;
* `equationOn` is a checked Lean proposition using `HasDerivWithinAt`.

The derivative-to-gradient bridge, Legendre transform package, global flow, and
energy conservation theorem are left as proposition fields because they are not
closed in the repo-local dependency closure for this slot.
-/
structure HamiltonianMechanicsData
    (Q : Type u) [DecidableEq Q] [Fintype Q] : Type u where
  hamiltonian : Hamiltonian Q
  gradient : HamiltonianGradient Q
  timeDomain : Set ℝ
  trajectory : ℝ → CanonicalPhase Q
  initialTime : ℝ
  initialState : CanonicalPhase Q
  equationOn : HamiltonianEquationOn gradient trajectory timeDomain
  initialCondition : trajectory initialTime = initialState
  differentiableHamiltonianModel : Prop
  canonicalCoordinateModel : Prop
  legendreTransformAvailable : Prop
  symplecticFlowProperty : Prop
  energyConservation : Prop
  equivalentEulerLagrangeForm : Prop

/-- Well-formedness hypotheses for the normalized Hamiltonian statement. -/
def HamiltonianHypotheses
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    (D : HamiltonianMechanicsData Q) : Prop :=
  D.differentiableHamiltonianModel ∧
    D.canonicalCoordinateModel ∧
      D.legendreTransformAvailable

/-- Expected mathematical outputs of a Hamiltonian formulation. -/
def HamiltonianConclusion
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    (D : HamiltonianMechanicsData Q) : Prop :=
  D.symplecticFlowProperty ∧
    D.energyConservation ∧
      D.equivalentEulerLagrangeForm

/--
Stage1 normalized statement shape for Hamiltonian mechanics.

For every finite canonical phase coordinate type and every well-formed
Hamiltonian model satisfying Hamilton's ODE, the generated dynamics have the
expected symplectic-flow, energy-conservation, and Euler-Lagrange equivalence
properties.  This is a precise statement boundary, not a terminal proof.
-/
def StatementShape : Prop :=
  ∀ (Q : Type u) [DecidableEq Q] [Fintype Q],
    ∀ D : HamiltonianMechanicsData Q,
      HamiltonianHypotheses D → HamiltonianConclusion D

/-- The statement shape unfolds to the expected quantified implication. -/
theorem statementShape_iff_forall_data :
    StatementShape.{u} ↔
      ∀ (Q : Type u) [DecidableEq Q] [Fintype Q],
        ∀ D : HamiltonianMechanicsData Q,
          HamiltonianHypotheses D → HamiltonianConclusion D :=
  Iff.rfl

/-- The canonical symplectic matrix is skew-symmetric. -/
theorem canonicalSymplecticMatrix_transpose
    (Q : Type u) [DecidableEq Q] :
    (CanonicalSymplecticMatrix Q)ᵀ = -CanonicalSymplecticMatrix Q :=
  Matrix.J_transpose Q ℝ

/-- The square of the canonical symplectic matrix is `-1`. -/
theorem canonicalSymplecticMatrix_squared
    (Q : Type u) [DecidableEq Q] [Fintype Q] :
    CanonicalSymplecticMatrix Q * CanonicalSymplecticMatrix Q = -1 :=
  Matrix.J_squared Q ℝ

/-- The canonical symplectic matrix is an element of mathlib's symplectic group. -/
theorem canonicalSymplecticMatrix_mem_symplecticGroup
    (Q : Type u) [DecidableEq Q] [Fintype Q] :
    CanonicalSymplecticMatrix Q ∈ Matrix.symplecticGroup Q ℝ :=
  SymplecticGroup.J_mem Q ℝ

/-- A symplectic matrix has a unit determinant in mathlib's finite matrix API. -/
theorem symplecticMatrix_det_isUnit
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    {A : Matrix (Q ⊕ Q) (Q ⊕ Q) ℝ}
    (hA : A ∈ Matrix.symplecticGroup Q ℝ) :
    IsUnit (Matrix.det A) :=
  SymplecticGroup.symplectic_det hA

/-- Hamilton's vector field unfolds to multiplication by the canonical matrix. -/
theorem hamiltonianVectorField_eq_mulVec
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    (gradH : HamiltonianGradient Q) (x : CanonicalPhase Q) :
    HamiltonianVectorField gradH x =
      (CanonicalSymplecticMatrix Q).mulVec (gradH x) :=
  rfl

/-- Project the differential equation at a time inside the chosen domain. -/
theorem HamiltonianEquationOn.hasDerivWithinAt
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    {gradH : HamiltonianGradient Q}
    {trajectory : ℝ → CanonicalPhase Q} {timeDomain : Set ℝ}
    (h : HamiltonianEquationOn gradH trajectory timeDomain)
    {t : ℝ} (ht : t ∈ timeDomain) :
    HasDerivWithinAt trajectory
      (HamiltonianVectorField gradH (trajectory t)) timeDomain t :=
  h t ht

/--
Checked mathlib anchor: uniqueness for finite-dimensional ODE solutions under a
uniform Lipschitz condition in the state variable.
-/
theorem ode_solution_unique_anchor
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {vfield : ℝ → E → E} {K : NNReal}
    {f g : ℝ → E} {a b : ℝ}
    (hv : ∀ t : ℝ, LipschitzWith K (vfield t))
    (hf : ContinuousOn f (Set.Icc a b))
    (hf' : ∀ t ∈ Set.Ico a b,
      HasDerivWithinAt f (vfield t (f t)) (Set.Ici t) t)
    (hg : ContinuousOn g (Set.Icc a b))
    (hg' : ∀ t ∈ Set.Ico a b,
      HasDerivWithinAt g (vfield t (g t)) (Set.Ici t) t)
    (ha : f a = g a) :
    Set.EqOn f g (Set.Icc a b) :=
  ODE_solution_unique hv hf hf' hg hg' ha

/--
Hamiltonian-specific ODE uniqueness wrapper: two trajectories of the same
Lipschitz canonical Hamiltonian vector field with the same initial state agree
on the closed interval.
-/
theorem hamiltonianTrajectory_unique_on_Icc
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    {gradH : HamiltonianGradient Q} {K : NNReal}
    {f g : ℝ → CanonicalPhase Q} {a b : ℝ}
    (hv : ∀ _t : ℝ,
      LipschitzWith K (fun x : CanonicalPhase Q =>
        HamiltonianVectorField gradH x))
    (hf : ContinuousOn f (Set.Icc a b))
    (hf' : ∀ t ∈ Set.Ico a b,
      HasDerivWithinAt f
        (HamiltonianVectorField gradH (f t)) (Set.Ici t) t)
    (hg : ContinuousOn g (Set.Icc a b))
    (hg' : ∀ t ∈ Set.Ico a b,
      HasDerivWithinAt g
        (HamiltonianVectorField gradH (g t)) (Set.Ici t) t)
    (ha : f a = g a) :
    Set.EqOn f g (Set.Icc a b) :=
  ODE_solution_unique
    (v := fun _ x => HamiltonianVectorField gradH x)
    hv hf hf' hg hg' ha

/-- The hypotheses expose the differentiable-Hamiltonian model field. -/
theorem HamiltonianHypotheses.differentiableHamiltonianModel
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    {D : HamiltonianMechanicsData Q}
    (h : HamiltonianHypotheses D) :
    D.differentiableHamiltonianModel :=
  h.1

/-- The hypotheses expose the canonical-coordinate model field. -/
theorem HamiltonianHypotheses.canonicalCoordinateModel
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    {D : HamiltonianMechanicsData Q}
    (h : HamiltonianHypotheses D) :
    D.canonicalCoordinateModel :=
  h.2.1

/-- The hypotheses expose the Legendre-transform availability field. -/
theorem HamiltonianHypotheses.legendreTransformAvailable
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    {D : HamiltonianMechanicsData Q}
    (h : HamiltonianHypotheses D) :
    D.legendreTransformAvailable :=
  h.2.2

/-- The conclusion exposes the symplectic-flow field. -/
theorem HamiltonianConclusion.symplecticFlowProperty
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    {D : HamiltonianMechanicsData Q}
    (h : HamiltonianConclusion D) :
    D.symplecticFlowProperty :=
  h.1

/-- The conclusion exposes the energy-conservation field. -/
theorem HamiltonianConclusion.energyConservation
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    {D : HamiltonianMechanicsData Q}
    (h : HamiltonianConclusion D) :
    D.energyConservation :=
  h.2.1

/-- The conclusion exposes the Euler-Lagrange equivalence field. -/
theorem HamiltonianConclusion.equivalentEulerLagrangeForm
    {Q : Type u} [DecidableEq Q] [Fintype Q]
    {D : HamiltonianMechanicsData Q}
    (h : HamiltonianConclusion D) :
    D.equivalentEulerLagrangeForm :=
  h.2.2

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.LinearAlgebra.SymplecticGroup",
  "Mathlib.LinearAlgebra.Matrix.NonsingularInverse",
  "Mathlib.Analysis.ODE.Basic",
  "Mathlib.Analysis.ODE.Gronwall",
  "Mathlib.Analysis.ODE.PicardLindelof",
  "Mathlib.Analysis.Calculus.FDeriv.Basic"
]

/-- The mathlib revision pinned by the local Lake manifest for this audit. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Required upstream names supplied by the pinned mathlib revision and checked
below with repo-local wrappers or direct `#check` probes.
-/
def pinnedMathlibSuppliedNames : List String := [
  "Matrix.J",
  "Matrix.symplecticGroup",
  "SymplecticGroup.J_mem",
  "SymplecticGroup.symplectic_det",
  "ODE_solution_unique"
]

/--
Checked wrapper branches eligible for the `local_wrapper_upstream_mathlib`
machine-state label after repo-local validation.

This status applies only to the finite-dimensional symplectic matrix and ODE
uniqueness wrappers.  It does not close the terminal Hamiltonian-mechanics
statement, whose derivative-to-gradient, Legendre-transform, symplectic-flow,
energy-conservation, and Euler-Lagrange branches remain formalization debt.
-/
def localWrapperUpstreamMathlibBranches : List String := [
  "finite-dimensional symplectic matrix wrappers | wrappers: CanonicalSymplecticMatrix, canonicalSymplecticMatrix_transpose, canonicalSymplecticMatrix_squared, canonicalSymplecticMatrix_mem_symplecticGroup, symplecticMatrix_det_isUnit | upstream: Matrix.J, Matrix.J_transpose, Matrix.J_squared, Matrix.symplecticGroup, SymplecticGroup.J_mem, SymplecticGroup.symplectic_det | status: local_wrapper_upstream_mathlib",
  "ODE uniqueness wrappers | wrappers: ode_solution_unique_anchor, hamiltonianTrajectory_unique_on_Icc | upstream: ODE_solution_unique | status: local_wrapper_upstream_mathlib"
]

/--
C004 debt marker: the terminal Hamiltonian mechanics theorem remains open.

These branches are proposition fields or future bridge packages in this file,
not closed theorem bodies.  They must be formalized locally or supplied by a
pinned/imported/checked external Lean dependency before `StatementShape` can be
claimed as completed.
-/
def fullHamiltonianMechanicsFormalizationDebtBranches : List String := [
  "derivative-to-gradient bridge",
  "regular Legendre transform",
  "symplectic flow preservation",
  "Hamiltonian energy conservation",
  "Euler-Lagrange equivalence"
]

/-- C004 machine-readable status for the terminal theorem boundary. -/
def fullHamiltonianMechanicsDebtClassification : String :=
  "formalization_debt"

/-- C004 guard: the terminal statement is not a repo-local completed theorem. -/
def fullHamiltonianMechanicsMachineStatus : String :=
  "not_repo_local_closed"

/-- The C004 terminal-theorem debt classification is intentionally explicit. -/
theorem fullHamiltonianMechanicsDebtClassification_eq :
    fullHamiltonianMechanicsDebtClassification = "formalization_debt" :=
  rfl

/-! ## C005 theorem-tree split -/

/--
Metadata row for the M0387-level theorem-tree split requested by C005.

These rows are checked Lean data about the proof architecture.  A row with
`formalization_debt` or `not_repo_local_closed` is not completion evidence for
the terminal Hamiltonian-mechanics theorem.
-/
structure TheoremTreePackage where
  canonicalName : String
  role : String
  repoLocalStatus : String
  localAnchors : List String
  openLeaves : List String
deriving Repr

/--
Unchecked leaves that must be closed before the derivative data in
`HamiltonianMechanicsData.gradient` can be treated as the Frechet
derivative/gradient of `HamiltonianMechanicsData.hamiltonian`.
-/
def differentiabilityGradientBridgeLeaves : List String := [
  "choose finite-dimensional inner-product or coordinate-gradient API",
  "prove Frechet derivative of the Hamiltonian exists on the chosen domain",
  "identify the stored gradient field with the derivative/gradient object"
]

/--
Unchecked leaves for replacing the abstract Legendre-transform assumptions by a
checked regular Lagrangian-to-Hamiltonian bridge.
-/
def legendreTransformBridgeLeaves : List String := [
  "define regular Legendre transform with nondegenerate velocity Hessian data",
  "prove inverse coordinate identities between Lagrangian and Hamiltonian variables",
  "derive Euler-Lagrange equivalence from Hamilton's equations under the bridge"
]

/--
Unchecked leaves for replacing the abstract flow and energy conclusion fields by
checked flow-preservation and conservation theorems.
-/
def symplecticFlowEnergyLeaves : List String := [
  "construct or import the local/global Hamiltonian flow object",
  "prove the flow maps preserve the canonical symplectic form",
  "prove Hamiltonian energy is constant along Hamiltonian trajectories"
]

/--
Repo-local closure leaves for the C005 gate.  The current artifact closes only
the statement-shape, symplectic-object, ODE-model, and ODE-uniqueness wrapper
packages; the terminal Hamiltonian theorem remains open.
-/
def repoLocalClosureGateLeaves : List String := [
  "no completed full-theorem claim until all bridge packages are proved or imported",
  "if an external Lean 4 terminal proof is found, pin/import/check it or record a concrete blocker",
  "keep public blueprint and todo states unchecked until serial integration records the local validation result"
]

/-! ## C006 unchecked public leaves -/

/--
Unchecked public leaf metadata for the C006 public backfill.

Each row is deliberately marked `unchecked` because it names a future
formalization obligation, not a completed local theorem.  The rows are
integration-ready public leaves for the M0387-style theorem tree.
-/
structure PublicUncheckedLeaf where
  leafId : String
  packageName : String
  title : String
  status : String
  closureRequirement : String
deriving Repr

/--
C006 unchecked public leaves for the Hamiltonian mechanics frontier.

These are the five public leaves requested by `S1-M-185-public-006`.  They are
checked as Lean metadata so the boundary is repo-local, while the mathematical
content remains `formalization_debt` until proved locally or supplied by a
pinned/imported/checked external Lean dependency.
-/
def c006UncheckedPublicLeaves : List PublicUncheckedLeaf := [
  {
    leafId := "S1-M-185.L017",
    packageName := "differentiability_gradient_bridge",
    title := "Frechet derivative/gradient bridge",
    status := "unchecked_formalization_debt",
    closureRequirement :=
      "prove that the stored Hamiltonian gradient is induced by the " ++
      "Frechet derivative of the Hamiltonian in the chosen finite-dimensional " ++
      "coordinate or inner-product model"
  },
  {
    leafId := "S1-M-185.L018",
    packageName := "legendre_transform_bridge",
    title := "regular Legendre transform",
    status := "unchecked_formalization_debt",
    closureRequirement :=
      "define the regular Legendre transform with nondegenerate velocity " ++
      "Hessian or equivalent invertibility data and prove the coordinate " ++
      "inverse identities used by the Hamiltonian model"
  },
  {
    leafId := "S1-M-185.L019",
    packageName := "legendre_transform_bridge",
    title := "Euler-Lagrange equivalence",
    status := "unchecked_formalization_debt",
    closureRequirement :=
      "prove that Euler-Lagrange trajectories correspond to Hamiltonian " ++
      "trajectories under the checked regular Legendre-transform bridge"
  },
  {
    leafId := "S1-M-185.L020",
    packageName := "symplectic_flow_energy",
    title := "symplectic flow preservation",
    status := "unchecked_formalization_debt",
    closureRequirement :=
      "construct or import the Hamiltonian flow object and prove its time " ++
      "maps preserve the canonical symplectic structure"
  },
  {
    leafId := "S1-M-185.L021",
    packageName := "symplectic_flow_energy",
    title := "Hamiltonian energy conservation",
    status := "unchecked_formalization_debt",
    closureRequirement :=
      "prove that the Hamiltonian value is constant along trajectories " ++
      "satisfying Hamilton's equation under the selected differentiability " ++
      "and flow hypotheses"
  }
]

/-- C006 has exactly the five requested unchecked public leaf titles. -/
theorem c006UncheckedPublicLeaves_titles :
    c006UncheckedPublicLeaves.map PublicUncheckedLeaf.title = [
      "Frechet derivative/gradient bridge",
      "regular Legendre transform",
      "Euler-Lagrange equivalence",
      "symplectic flow preservation",
      "Hamiltonian energy conservation"
    ] :=
  rfl

/-- C006 rows are metadata only; every row remains unchecked. -/
theorem c006UncheckedPublicLeaves_statuses :
    c006UncheckedPublicLeaves.map PublicUncheckedLeaf.status = [
      "unchecked_formalization_debt",
      "unchecked_formalization_debt",
      "unchecked_formalization_debt",
      "unchecked_formalization_debt",
      "unchecked_formalization_debt"
    ] :=
  rfl

/-! ## C007 external upstream integration gate -/

/--
External Lean 4 Hamiltonian-mechanics candidate row for the C007 audit.

The row is metadata only.  It records a concrete upstream candidate and the
repo-local blocker preventing this child from treating it as checked closure.
-/
structure ExternalHamiltonianProofCandidate where
  project : String
  source : String
  moduleName : String
  theoremNames : List String
  statementCoverage : String
  observedToolchain : String
  observedMathlibRequirement : String
  repoLocalStatus : String
  integrationBlocker : String
deriving Repr

/--
C007 upstream candidate found outside mathlib.

Physlib currently has a Lean 4 module for Hamilton's equations and a variational
gradient theorem.  This is useful external evidence, but it is not a repo-local
completed state for this slot until a serialized dependency change pins Physlib
at a concrete revision, imports the module, and checks wrappers in this Lake
project.
-/
def c007ExternalHamiltonianProofCandidate : ExternalHamiltonianProofCandidate := {
  project := "leanprover-community/physlib",
  source :=
    "https://raw.githubusercontent.com/leanprover-community/physlib/master/" ++
    "Physlib/ClassicalMechanics/HamiltonsEquations.lean",
  moduleName := "Physlib.ClassicalMechanics.HamiltonsEquations",
  theoremNames := [
    "ClassicalMechanics.hamiltonEqOp",
    "ClassicalMechanics.hamiltonEqOp_eq",
    "ClassicalMechanics.hamiltonEqOp_eq_zero_iff_hamiltons_equations",
    "ClassicalMechanics.hamiltons_equations_varGradient"
  ],
  statementCoverage :=
    "partial Hamilton-equations and variational-gradient coverage; not a " ++
    "repo-local proof of symplectic flow preservation, Hamiltonian energy " ++
    "conservation, and Euler-Lagrange equivalence for StatementShape",
  observedToolchain := "leanprover/lean4:v4.29.1",
  observedMathlibRequirement :=
    "mathlib from git https://github.com/leanprover-community/mathlib4.git @ v4.29.1",
  repoLocalStatus := "external_upstream_anchor_only_not_completed",
  integrationBlocker :=
    "This child owns only S1_M_185.lean and its private ledger, so it cannot " ++
    "edit lakefile.lean, lake-manifest.json, or shared import aggregators to " ++
    "pin Physlib.  The current repo toolchain is leanprover/lean4:v4.29.0 " ++
    "with pinned mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95, while " ++
    "the observed Physlib master requires leanprover/lean4:v4.29.1 and " ++
    "mathlib @ v4.29.1.  A serialized integrator must choose and pin a " ++
    "concrete Physlib revision, reconcile the toolchain/mathlib dependency, " ++
    "import this module, and run repo-local wrappers before any completion claim."
}

/-- C007 gate status: the external candidate is not repo-local closure. -/
def c007RepoLocalIntegrationDebtGate : String :=
  "blocked_not_completed_no_completed_repo_local_integration_debt"

/-- C007 records anchor-only external evidence as non-completion. -/
theorem c007ExternalHamiltonianProofCandidate_status :
    c007ExternalHamiltonianProofCandidate.repoLocalStatus =
      "external_upstream_anchor_only_not_completed" :=
  rfl

/-- C007 leaves no completed state with repo-local integration debt. -/
theorem c007RepoLocalIntegrationDebtGate_eq :
    c007RepoLocalIntegrationDebtGate =
      "blocked_not_completed_no_completed_repo_local_integration_debt" :=
  rfl

/--
C005 theorem-tree package split for THM-M-1516 Hamiltonian mechanics.

The first four packages are repo-local checked statement/wrapper metadata.  The
last four packages are explicit formalization or closure gates.  This is a
checked package ledger, not a proof of `StatementShape`.
-/
def theoremTreeSplit : List TheoremTreePackage := [
  {
    canonicalName := "statement_normalization",
    role :=
      "Normalize the public Hamiltonian-mechanics wording to a finite " ++
      "canonical phase-space statement with a Hamiltonian, gradient, " ++
      "trajectory, time domain, hypotheses, and expected conclusions.",
    repoLocalStatus := "checked_statement_shape_not_terminal_proof",
    localAnchors := [
      "CanonicalPhase",
      "Hamiltonian",
      "HamiltonianGradient",
      "HamiltonianMechanicsData",
      "HamiltonianHypotheses",
      "HamiltonianConclusion",
      "StatementShape",
      "statementShape_iff_forall_data"
    ],
    openLeaves := []
  },
  {
    canonicalName := "symplectic_object_model",
    role :=
      "Model the canonical symplectic matrix with mathlib's `Matrix.J Q ℝ` " ++
      "and checked symplectic-group wrappers.",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    localAnchors := [
      "CanonicalSymplecticMatrix",
      "canonicalSymplecticMatrix_transpose",
      "canonicalSymplecticMatrix_squared",
      "canonicalSymplecticMatrix_mem_symplecticGroup",
      "symplecticMatrix_det_isUnit",
      "Matrix.J",
      "Matrix.symplecticGroup",
      "SymplecticGroup.J_mem",
      "SymplecticGroup.symplectic_det"
    ],
    openLeaves := []
  },
  {
    canonicalName := "hamiltonian_ode_model",
    role :=
      "Express Hamilton's equation as the canonical vector field `J * grad H` " ++
      "and a `HasDerivWithinAt` ODE on the selected time domain.",
    repoLocalStatus := "checked_statement_shape_not_terminal_proof",
    localAnchors := [
      "HamiltonianVectorField",
      "HamiltonianEquationOn",
      "hamiltonianVectorField_eq_mulVec",
      "HamiltonianEquationOn.hasDerivWithinAt"
    ],
    openLeaves := []
  },
  {
    canonicalName := "ode_wellposedness_anchor",
    role :=
      "Wrap mathlib ODE uniqueness and specialize it to Lipschitz canonical " ++
      "Hamiltonian vector fields.",
    repoLocalStatus := "local_wrapper_upstream_mathlib",
    localAnchors := [
      "ode_solution_unique_anchor",
      "hamiltonianTrajectory_unique_on_Icc",
      "ODE_solution_unique"
    ],
    openLeaves := []
  },
  {
    canonicalName := "differentiability_gradient_bridge",
    role :=
      "Replace the abstract gradient-side interface with a checked bridge " ++
      "from Frechet differentiability of the Hamiltonian to the stored gradient.",
    repoLocalStatus := "formalization_debt",
    localAnchors := [
      "HamiltonianMechanicsData.differentiableHamiltonianModel",
      "HamiltonianHypotheses.differentiableHamiltonianModel",
      "differentiabilityGradientBridgeLeaves"
    ],
    openLeaves := differentiabilityGradientBridgeLeaves
  },
  {
    canonicalName := "legendre_transform_bridge",
    role :=
      "Build the regular Legendre transform and Euler-Lagrange equivalence " ++
      "package needed to connect Lagrangian and Hamiltonian formulations.",
    repoLocalStatus := "formalization_debt",
    localAnchors := [
      "HamiltonianMechanicsData.legendreTransformAvailable",
      "HamiltonianMechanicsData.equivalentEulerLagrangeForm",
      "HamiltonianHypotheses.legendreTransformAvailable",
      "HamiltonianConclusion.equivalentEulerLagrangeForm",
      "legendreTransformBridgeLeaves"
    ],
    openLeaves := legendreTransformBridgeLeaves
  },
  {
    canonicalName := "symplectic_flow_energy",
    role :=
      "Prove flow preservation of the canonical symplectic structure and " ++
      "Hamiltonian energy conservation for the selected flow object.",
    repoLocalStatus := "formalization_debt",
    localAnchors := [
      "HamiltonianMechanicsData.symplecticFlowProperty",
      "HamiltonianMechanicsData.energyConservation",
      "HamiltonianConclusion.symplecticFlowProperty",
      "HamiltonianConclusion.energyConservation",
      "symplecticFlowEnergyLeaves"
    ],
    openLeaves := symplecticFlowEnergyLeaves
  },
  {
    canonicalName := "repo_local_closure_gate",
    role :=
      "Prevent a completed-state claim until the terminal theorem is proved " ++
      "locally, wrapped over pinned mathlib, or supplied by a pinned and " ++
      "checked external Lean dependency.",
    repoLocalStatus := "not_repo_local_closed",
    localAnchors := [
      "fullHamiltonianMechanicsFormalizationDebtBranches",
      "fullHamiltonianMechanicsDebtClassification",
      "fullHamiltonianMechanicsMachineStatus",
      "repoLocalClosureGateLeaves"
    ],
    openLeaves := repoLocalClosureGateLeaves
  }
]

/-- The C005 package ledger contains exactly the eight requested package names. -/
theorem theoremTreeSplit_names :
    theoremTreeSplit.map TheoremTreePackage.canonicalName = [
      "statement_normalization",
      "symplectic_object_model",
      "hamiltonian_ode_model",
      "ode_wellposedness_anchor",
      "differentiability_gradient_bridge",
      "legendre_transform_bridge",
      "symplectic_flow_energy",
      "repo_local_closure_gate"
    ] :=
  rfl

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "Matrix.J",
  "Matrix.J_transpose",
  "Matrix.J_squared",
  "Matrix.symplecticGroup",
  "SymplecticGroup.J_mem",
  "SymplecticGroup.mem_iff",
  "SymplecticGroup.symplectic_det",
  "ODE_solution_unique",
  "IsPicardLindelof.exists_eq_forall_mem_Icc_hasDerivWithinAt",
  "IsPicardLindelof.exists_forall_mem_closedBall_eq_hasDerivWithinAt_lipschitzOnWith"
]

/--
Search terms used to distinguish checked mathlib anchors from a terminal
Hamiltonian-mechanics formalization not present in the local dependency closure.
-/
def boundarySearchTerms : List String := [
  "Hamiltonian mechanics",
  "Hamiltonian flow",
  "Hamilton's equations",
  "symplecticGroup",
  "Matrix.J",
  "Poisson bracket",
  "Legendre transform",
  "Euler Lagrange Hamiltonian",
  "Liouville theorem"
]

/-! ## Audit probes -/

#check StatementShape
#check canonicalSymplecticMatrix_transpose
#check canonicalSymplecticMatrix_squared
#check canonicalSymplecticMatrix_mem_symplecticGroup
#check symplecticMatrix_det_isUnit
#check hamiltonianTrajectory_unique_on_Icc
#check Matrix.J
#check Matrix.J_transpose
#check Matrix.J_squared
#check Matrix.symplecticGroup
#check SymplecticGroup.J_mem
#check SymplecticGroup.symplectic_det
#check ODE_solution_unique
#check localWrapperUpstreamMathlibBranches
#check fullHamiltonianMechanicsFormalizationDebtBranches
#check fullHamiltonianMechanicsDebtClassification_eq
#check TheoremTreePackage
#check theoremTreeSplit
#check theoremTreeSplit_names
#check PublicUncheckedLeaf
#check c006UncheckedPublicLeaves
#check c006UncheckedPublicLeaves_titles
#check c006UncheckedPublicLeaves_statuses
#check ExternalHamiltonianProofCandidate
#check c007ExternalHamiltonianProofCandidate
#check c007ExternalHamiltonianProofCandidate_status
#check c007RepoLocalIntegrationDebtGate
#check c007RepoLocalIntegrationDebtGate_eq
#check differentiabilityGradientBridgeLeaves
#check legendreTransformBridgeLeaves
#check symplecticFlowEnergyLeaves
#check repoLocalClosureGateLeaves

end AwesomeTheorems.Stage1.S1_M_185
