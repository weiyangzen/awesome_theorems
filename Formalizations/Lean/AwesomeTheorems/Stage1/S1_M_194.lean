import Mathlib.LinearAlgebra.CliffordAlgebra.Basic
import Mathlib.LinearAlgebra.CliffordAlgebra.Fold
import Mathlib.LinearAlgebra.CliffordAlgebra.SpinGroup
import Mathlib.LinearAlgebra.Matrix.ToLin
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.Normed.Operator.Basic

/-!
# S1-M-194 / THM-M-1526: Dirac equation

This Stage1 artifact records a conservative Lean 4 boundary for the Dirac
equation as a relativistic quantum-mechanical first-order equation.

The pinned mathlib snapshot has Clifford algebras, complex normed vector spaces,
continuous linear operators, finite sums of bounded operators, and Hilbert-space
infrastructure.  It does not expose a terminal theorem for spinor bundles,
gamma matrices satisfying a Lorentzian Clifford relation, self-adjoint Dirac
Hamiltonians, conserved currents, Cauchy well-posedness, or the relativistic
dispersion relation.  Those mathematical-physics assumptions are therefore
kept as explicit fields.
-/

noncomputable section

open scoped BigOperators

universe uι uσ uΨ uR uM

namespace AwesomeTheorems.Stage1.S1_M_194

/-- Bounded complex-linear operators on the selected spinor-field space. -/
abbrev FieldOperator (Ψ : Type uΨ) [NormedAddCommGroup Ψ] [NormedSpace ℂ Ψ] :
    Type uΨ :=
  Ψ →L[ℂ] Ψ

/--
Abstract gamma-operator system for a Dirac model.

The `metric` field is intended to encode the inverse metric coefficients, and
`clifford_anticommutator` is the concrete finite-index Clifford relation
`γ μ γ ν + γ ν γ μ = 2 g^{μν} I` for bounded complex-linear endomorphisms.
The current mathlib snapshot has Clifford algebras but no terminal
spinor-bundle/gamma-matrix package for this theorem slot.
-/
structure GammaSystem (ι : Type uι) (Ψ : Type uΨ)
    [Fintype ι] [NormedAddCommGroup Ψ] [NormedSpace ℂ Ψ] : Type (max uι uΨ) where
  gamma : ι → FieldOperator Ψ
  metric : ι → ι → ℂ
  clifford_anticommutator : ∀ μ ν : ι,
    (gamma μ).comp (gamma ν) + (gamma ν).comp (gamma μ) =
      (2 * metric μ ν) • ContinuousLinearMap.id ℂ Ψ
  gamma_regular : Prop
  gamma_regular_holds : gamma_regular

/--
Abstract data for a Dirac equation on a spinor-field space.

`derivative μ` represents the selected first-order derivative in spacetime
direction `μ`.  `potential` allows the statement boundary to include gauge or
external-field couplings without committing to a bundle connection API yet.
-/
structure DiracModelData (ι : Type uι) (Ψ : Type uΨ)
    [Fintype ι] [NormedAddCommGroup Ψ] [NormedSpace ℂ Ψ] :
    Type (max uι uΨ) where
  derivative : ι → FieldOperator Ψ
  gammaSystem : GammaSystem ι Ψ
  mass : ℂ
  potential : FieldOperator Ψ
  admissibleSpacetimeModel : Prop
  derivative_compatibility : Prop
  hamiltonian_selfAdjoint : Prop
  conservedCurrentLaw : Prop
  cauchyWellPosed : Prop
  spectralDispersionRelation : Prop

/--
The abstract Dirac operator
`Σ_μ γ^μ ∂_μ - m I + V` on the selected spinor-field space.

This is a bounded-operator statement shape.  A terminal PDE formalization should
replace the derivative operators by concrete unbounded differential operators or
distributional/weak operators on a chosen domain.
-/
def DiracOperator {ι : Type uι} {Ψ : Type uΨ}
    [Fintype ι] [NormedAddCommGroup Ψ] [NormedSpace ℂ Ψ]
    (D : DiracModelData ι Ψ) : FieldOperator Ψ :=
  (∑ μ : ι, (D.gammaSystem.gamma μ).comp (D.derivative μ)) -
    D.mass • ContinuousLinearMap.id ℂ Ψ + D.potential

/-- A spinor field satisfies the homogeneous Dirac equation for `D`. -/
def DiracEquation {ι : Type uι} {Ψ : Type uΨ}
    [Fintype ι] [NormedAddCommGroup Ψ] [NormedSpace ℂ Ψ]
    (D : DiracModelData ι Ψ) (ψ : Ψ) : Prop :=
  DiracOperator D ψ = 0

/--
Candidate solution object for the normalized Dirac-equation boundary.

The extra proposition fields isolate the physically meaningful restrictions
that prevent the trivial zero solution from being mistaken for the intended
relativistic quantum-mechanical theorem.
-/
structure DiracSolution {ι : Type uι} {Ψ : Type uΨ}
    [Fintype ι] [NormedAddCommGroup Ψ] [NormedSpace ℂ Ψ]
    (D : DiracModelData ι Ψ) : Type uΨ where
  wavefunction : Ψ
  equation : DiracEquation D wavefunction
  regularity : Prop
  regularity_holds : regularity
  normalization : Prop
  normalization_holds : normalization
  finite_energy : Prop
  finite_energy_holds : finite_energy
  nontrivial_or_initial_data : Prop
  nontrivial_or_initial_data_holds : nontrivial_or_initial_data

/--
Normalized Stage1 statement-shape candidate for THM-M-1526.

For every finite spacetime-index type and complex spinor-field space, an
admissible Dirac model with Clifford-compatible gamma operators, compatible
first-order derivatives, a self-adjoint Hamiltonian interpretation, Cauchy
well-posedness, and the intended spectral dispersion package should produce a
physically meaningful solution object.

This is only a statement boundary.  It is not a proof of the Dirac equation or
of any analytic well-posedness theorem.
-/
def StatementShape : Prop :=
  ∀ (ι : Type uι) (Ψ : Type uΨ)
    [Fintype ι] [NormedAddCommGroup Ψ] [NormedSpace ℂ Ψ],
      ∀ D : DiracModelData ι Ψ,
        D.gammaSystem.gamma_regular →
          D.admissibleSpacetimeModel →
            D.derivative_compatibility →
              D.hamiltonian_selfAdjoint →
                D.cauchyWellPosed →
                  D.spectralDispersionRelation →
                    Nonempty (DiracSolution D)

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (ι : Type uι) (Ψ : Type uΨ)
      [Fintype ι] [NormedAddCommGroup Ψ] [NormedSpace ℂ Ψ],
        ∀ D : DiracModelData ι Ψ,
          D.gammaSystem.gamma_regular →
            D.admissibleSpacetimeModel →
              D.derivative_compatibility →
                D.hamiltonian_selfAdjoint →
                  D.cauchyWellPosed →
                    D.spectralDispersionRelation →
                      Nonempty (DiracSolution D)) :
    StatementShape.{uι, uΨ} :=
  h

/-- Projection wrapper: the gamma system carries its Clifford anticommutator law. -/
theorem GammaSystem.clifford_anticommutator_holds {ι : Type uι} {Ψ : Type uΨ}
    [Fintype ι] [NormedAddCommGroup Ψ] [NormedSpace ℂ Ψ] (G : GammaSystem ι Ψ) (μ ν : ι) :
    (G.gamma μ).comp (G.gamma ν) + (G.gamma ν).comp (G.gamma μ) =
      (2 * G.metric μ ν) • ContinuousLinearMap.id ℂ Ψ :=
  G.clifford_anticommutator μ ν

/-- Projection wrapper: a solution satisfies the abstract Dirac equation. -/
theorem DiracSolution.satisfies_equation {ι : Type uι} {Ψ : Type uΨ}
    [Fintype ι] [NormedAddCommGroup Ψ] [NormedSpace ℂ Ψ]
    {D : DiracModelData ι Ψ} (S : DiracSolution D) :
    DiracEquation D S.wavefunction :=
  S.equation

/-- The Dirac-equation predicate unfolds to the zero equation for the Dirac operator. -/
theorem diracEquation_iff {ι : Type uι} {Ψ : Type uΨ}
    [Fintype ι] [NormedAddCommGroup Ψ] [NormedSpace ℂ Ψ]
    (D : DiracModelData ι Ψ) (ψ : Ψ) :
    DiracEquation D ψ ↔ DiracOperator D ψ = 0 :=
  Iff.rfl

/-- Pointwise form of the abstract bounded Dirac operator. -/
theorem diracOperator_apply {ι : Type uι} {Ψ : Type uΨ}
    [Fintype ι] [NormedAddCommGroup Ψ] [NormedSpace ℂ Ψ]
    (D : DiracModelData ι Ψ) (ψ : Ψ) :
    DiracOperator D ψ =
      (∑ μ : ι, D.gammaSystem.gamma μ (D.derivative μ ψ)) -
        D.mass • ψ + D.potential ψ := by
  simp [DiracOperator]

/-- Sanity check for the homogeneous bounded-operator boundary: zero is a formal solution. -/
theorem zero_satisfies_homogeneous_dirac {ι : Type uι} {Ψ : Type uΨ}
    [Fintype ι] [NormedAddCommGroup Ψ] [NormedSpace ℂ Ψ]
    (D : DiracModelData ι Ψ) :
    DiracEquation D 0 := by
  simp [DiracEquation, DiracOperator]

/-- Checked continuous-linear-map anchor: identity operators act as identity. -/
theorem continuousLinearMap_id_apply_anchor {Ψ : Type uΨ}
    [NormedAddCommGroup Ψ] [NormedSpace ℂ Ψ] (ψ : Ψ) :
    ContinuousLinearMap.id ℂ Ψ ψ = ψ :=
  ContinuousLinearMap.id_apply ψ

/-- Checked continuous-linear-map anchor: composition applies by nested application. -/
theorem continuousLinearMap_comp_apply_anchor {Ψ : Type uΨ}
    [NormedAddCommGroup Ψ] [NormedSpace ℂ Ψ]
    (A B : FieldOperator Ψ) (ψ : Ψ) :
    A.comp B ψ = A (B ψ) :=
  rfl

/-- Checked Clifford-algebra anchor: the canonical generator squares to the quadratic form. -/
theorem clifford_generator_square_anchor
    {R : Type uR} [CommRing R]
    {M : Type uM} [AddCommGroup M] [Module R M]
    (Q : QuadraticForm R M) (m : M) :
    CliffordAlgebra.ι Q m * CliffordAlgebra.ι Q m =
      algebraMap R (CliffordAlgebra Q) (Q m) :=
  CliffordAlgebra.ι_sq_scalar Q m

/-- mathlib modules checked while locating repo-local Dirac-equation anchors. -/
def mathlibAnchorModules : List String := [
  "Mathlib.LinearAlgebra.CliffordAlgebra.Basic",
  "Mathlib.LinearAlgebra.CliffordAlgebra.Fold",
  "Mathlib.LinearAlgebra.CliffordAlgebra.SpinGroup",
  "Mathlib.LinearAlgebra.CliffordAlgebra.Star",
  "Mathlib.Analysis.InnerProductSpace.Basic",
  "Mathlib.Analysis.InnerProductSpace.Spectrum",
  "Mathlib.Analysis.Normed.Operator.Basic",
  "Mathlib.Analysis.Normed.Operator.Banach",
  "Mathlib.Analysis.Normed.Operator.FredholmAlternative",
  "Mathlib.Analysis.Distribution.TemperedDistribution",
  "Mathlib.Analysis.Calculus.FDeriv.Basic",
  "Mathlib.Geometry.Manifold.VectorBundle.Basic"
]

/-- Nearby checked names used or audited for this Stage1 statement boundary. -/
def mathlibAnchorNames : List String := [
  "CliffordAlgebra",
  "CliffordAlgebra.ι",
  "CliffordAlgebra.ι_sq_scalar",
  "CliffordAlgebra.lift",
  "CliffordAlgebra.lift_ι_apply",
  "CliffordAlgebra.SpinGroup",
  "ContinuousLinearMap",
  "ContinuousLinearMap.id",
  "ContinuousLinearMap.id_apply",
  "ContinuousLinearMap.comp",
  "InnerProductSpace",
  "spectrum",
  "resolventSet",
  "TemperedDistribution",
  "fderiv"
]

/-! ## Gamma-representation bridge API audit -/

/--
Exact `Mathlib.LinearAlgebra.CliffordAlgebra.SpinGroup` names audited for a
future gamma-representation bridge.

The installed API exposes lowercase root-level `spinGroup`, `pinGroup`, and
`lipschitzGroup` definitions, not a theorem namespace named
`CliffordAlgebra.SpinGroup`.  These names are useful for vector-range
preservation under Clifford conjugation, but they do not directly construct a
finite complex matrix gamma representation.
-/
def spinGroupBridgeAuditNames : List String := [
  "spinGroup",
  "spinGroup.mem_iff",
  "spinGroup.mem_pin",
  "spinGroup.mem_even",
  "spinGroup.involute_eq",
  "spinGroup.units_involute_act_eq_conjAct",
  "spinGroup.conjAct_smul_ι_mem_range_ι",
  "spinGroup.involute_act_ι_mem_range_ι",
  "spinGroup.conjAct_smul_range_ι",
  "spinGroup.toUnits",
  "spinGroup.toUnits_injective",
  "pinGroup",
  "pinGroup.mem_iff",
  "pinGroup.conjAct_smul_ι_mem_range_ι",
  "pinGroup.involute_act_ι_mem_range_ι",
  "lipschitzGroup",
  "lipschitzGroup.conjAct_smul_ι_mem_range_ι",
  "lipschitzGroup.involute_act_ι_mem_range_ι",
  "lipschitzGroup.conjAct_smul_range_ι"
]

/--
Exact `Mathlib.LinearAlgebra.CliffordAlgebra.Fold` names audited for extending
maps from Clifford generators to actions on a candidate spinor module.
-/
def cliffordFoldBridgeAuditNames : List String := [
  "CliffordAlgebra.foldr",
  "CliffordAlgebra.foldr_ι",
  "CliffordAlgebra.foldr_algebraMap",
  "CliffordAlgebra.foldr_one",
  "CliffordAlgebra.foldr_mul",
  "CliffordAlgebra.foldr_prod_map_ι",
  "CliffordAlgebra.foldl",
  "CliffordAlgebra.foldl_reverse",
  "CliffordAlgebra.foldr_reverse",
  "CliffordAlgebra.foldl_ι",
  "CliffordAlgebra.foldl_algebraMap",
  "CliffordAlgebra.foldl_one",
  "CliffordAlgebra.foldl_mul",
  "CliffordAlgebra.foldl_prod_map_ι",
  "CliffordAlgebra.right_induction",
  "CliffordAlgebra.left_induction",
  "CliffordAlgebra.foldr'",
  "CliffordAlgebra.foldr'_algebraMap",
  "CliffordAlgebra.foldr'_ι",
  "CliffordAlgebra.foldr'_ι_mul"
]

/--
Exact matrix API names used or audited for finite gamma-matrix anticommutators
and the selected finite constant-coefficient Dirac symbol.
-/
def matrixGammaBridgeAuditNames : List String := [
  "Matrix",
  "Matrix.ext",
  "Matrix.mul_apply",
  "Matrix.mul_apply'",
  "Matrix.mulVec",
  "Matrix.mulVec_eq_sum",
  "Matrix.mulVec_zero",
  "Matrix.sum_mulVec",
  "Matrix.mulVec_sum",
  "Matrix.smul_mul",
  "Matrix.mul_smul",
  "Matrix.one_apply",
  "Matrix.diagonal",
  "Matrix.diagonal_mul",
  "Matrix.mul_diagonal",
  "Matrix.diagonal_mul_diagonal",
  "Matrix.toLin",
  "Matrix.toLin_apply",
  "Matrix.toLin_mul",
  "Matrix.toLin_mul_apply",
  "Matrix.toLin'",
  "Matrix.toLin'_apply",
  "Matrix.toLin'_mul",
  "Matrix.toLin'_mul_apply"
]

/--
Concrete blockers found by the `S1-M-194-C004` gamma-representation bridge
audit.

This list is intentionally kept inside the owned Lean artifact so the public
blueprint can be updated later by a serial integrator without this worker
editing shared planning documents.
-/
def gammaRepresentationBridgeBlockers : List String := [
  "No terminal Dirac-equation, Dirac-operator, spinor-bundle, or gamma-matrix theorem was found in the pinned mathlib tree.",
  "`Mathlib.LinearAlgebra.CliffordAlgebra.SpinGroup` supplies `spinGroup`, `pinGroup`, and `lipschitzGroup` plus vector-range preservation under Clifford conjugation; it does not provide a matrix representation of the Clifford algebra.",
  "`CliffordAlgebra.foldr`/`foldl` can extend a generator action satisfying `f m (f m x) = Q m • x`, but the future bridge still needs a concrete linear action from generators to finite complex matrices.",
  "The matrix API is sufficient for finite anticommutator checking by `Matrix.ext`, `Matrix.mul_apply`, `Matrix.one_apply`, and `norm_num`, as demonstrated by `pauliFinTwo_clifford_anticommutator`; it does not by itself supply Lorentzian 4D gamma matrices.",
  "A completed THM-M-1526 target still needs a selected signature, a concrete representation theorem or local construction, and an integration path from the finite matrix identity to the bounded/unbounded Dirac operator semantics."
]

/--
Search terms that did not locate a terminal Dirac-equation theorem in the
local pinned mathlib tree.
-/
def absentTerminalSearchTerms : List String := [
  "DiracEquation",
  "Dirac equation",
  "Dirac operator",
  "gamma matrix",
  "GammaMatrix",
  "Pauli matrix",
  "spinor bundle",
  "Spinor",
  "Klein-Gordon",
  "relativistic wave equation",
  "self-adjoint Dirac Hamiltonian",
  "conserved current Dirac"
]

/-! ## External Lean 4 anchor audit -/

/--
External GitHub code-search terms for child `S1-M-194-C005`.

The authenticated GitHub code-search route was unavailable in this worker
process because `gh auth status` reported no logged-in GitHub host.  These
terms therefore remain an integration-ready audit checklist rather than a
completion certificate.
-/
def externalDiracLeanSearchTerms : List String := [
  "DiracEquation language:Lean",
  "\"Dirac equation\" language:Lean",
  "\"Dirac operator\" language:Lean",
  "\"gamma matrix\" language:Lean",
  "GammaMatrix language:Lean",
  "Pauli CliffordAlgebra language:Lean",
  "Spinor CliffordAlgebra language:Lean",
  "\"spinor bundle\" language:Lean",
  "\"Klein-Gordon\" language:Lean",
  "\"Dirac Hamiltonian\" language:Lean",
  "\"conserved current\" Dirac language:Lean"
]

/--
External Lean 4 candidate located during the child `S1-M-194-C005` audit.

`HEPLean/PhysLean` contains adjacent Dirac-representation gamma matrices,
Clifford-algebra maps, Pauli-matrix Clifford infrastructure, and bispinor
definitions.  It does not expose a terminal Dirac-equation theorem, Dirac PDE
operator theorem, self-adjoint Dirac Hamiltonian theorem, conserved-current
theorem, or Klein-Gordon bridge theorem in the audited modules.
-/
def externalDiracLeanCandidates : List String := [
  "https://github.com/HEPLean/PhysLean @ cd22b0c28882412447d12d5cfde677c4ad999994; module Physlib.Relativity.CliffordAlgebra; declarations spaceTime.γ.γ0_mul_γ0, spaceTime.γ.γ1_mul_γ1, spaceTime.γ.γ2_mul_γ2, spaceTime.γ.γ3_mul_γ3, spaceTime.γ.ofCliffordAlgebra_ι_single, spaceTime.γ.ofCliffordAlgebra_surjective; placeholder status: no kernel-placeholder token in this module but TODO records missing injectivity/isomorphism; Lake compatibility: external project uses Lean 4.29.1 and mathlib v4.29.1, while this repo pins Lean 4.29.0 and mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95, so not pinned/import-checked here.",
  "https://github.com/HEPLean/PhysLean @ cd22b0c28882412447d12d5cfde677c4ad999994; module Physlib.Relativity.PauliMatrices.CliffordAlgebra; declarations PauliMatrix.form, PauliMatrix.ofCliffordAlgebra, PauliMatrix.ofCliffordAlgebra_ι_single; placeholder status: no kernel-placeholder token in this module; Lake compatibility: same Lean/mathlib revision mismatch as Physlib.Relativity.CliffordAlgebra.",
  "https://github.com/HEPLean/PhysLean @ cd22b0c28882412447d12d5cfde677c4ad999994; module Physlib.Relativity.Bispinors.Basic; declarations complexLorentzTensor.contrBispinorUp, complexLorentzTensor.contrBispinorDown, complexLorentzTensor.coBispinorUp, complexLorentzTensor.coBispinorDown; placeholder status: contains informal_lemma placeholders for metric-contraction equalities; Lake compatibility: same Lean/mathlib revision mismatch as Physlib.Relativity.CliffordAlgebra."
]

/--
Repo-local integration conclusion for the external audit.

The audit found adjacent external Lean 4 infrastructure but no terminal
placeholder-free Dirac-equation proof body.  Because no such proof body was
found, there is no completed-state `repo_local_integration_debt` for this
child; the theorem remains `formalization_debt` until a precise target is
proved locally or a terminal external proof is pinned/imported/checked.
-/
def externalDiracAuditBlockers : List String := [
  "Authenticated GitHub code search was blocked in this worker: `gh auth status` reported no logged-in GitHub host and unauthenticated GitHub code search required sign-in or hit the REST API rate limit.",
  "`HEPLean/PhysLean` is an adjacent Lean 4 physics source, not a terminal THM-M-1526 closure: it supplies gamma matrices, Clifford-algebra maps, Pauli Clifford infrastructure, and bispinor definitions, but no Dirac-equation theorem.",
  "The relevant PhysLean revision uses Lean 4.29.1 and mathlib v4.29.1; this repo pins Lean 4.29.0 and mathlib commit 8a178386ffc0f5fef0b77738bb5449d50efeea95, so importing it would require an explicit dependency/toolchain compatibility pass.",
  "No external theorem was found that can be marked completed from URL-only evidence; any future external closure must be pinned/imported/checked or listed with a concrete integration blocker before public completion."
]

/-! ## External closure integration gate -/

/--
Repo-local integration status for child `S1-M-194-C006`.

This gate separates a real external closure from adjacent formal infrastructure.
The current status is `noTerminalClosureFound`: no pinned dependency or vendored
proof body was added, because the prior external audit found no terminal
placeholder-free Lean 4 theorem for the Dirac equation.
-/
inductive ExternalDiracClosureIntegrationStatus : Type
  | noTerminalClosureFound
  | blockedExternalClosure
  | pinnedDependencyValidated
  | vendoredProofValidated
  deriving DecidableEq, Repr

/-- Current C006 integration-gate status for THM-M-1526. -/
def externalDiracClosureIntegrationStatus : ExternalDiracClosureIntegrationStatus :=
  .noTerminalClosureFound

/--
Checked witness that C006 did not claim `external_upstream_pinned` closure.

If a future audit finds a terminal external Lean 4 Dirac-equation proof, this
constant should change only after a Lake pin/import/check or a vendored proof
body validates locally, or after an exact integration blocker is recorded.
-/
theorem externalDiracClosureIntegrationStatus_eq :
    externalDiracClosureIntegrationStatus =
      ExternalDiracClosureIntegrationStatus.noTerminalClosureFound :=
  rfl

/--
Integration actions considered for C006.

The first two actions were deliberately not performed because no terminal
external proof body was found.  The third item is the active gate for any future
external closure.
-/
def externalDiracClosureIntegrationActions : List String := [
  "No Lake dependency was added for THM-M-1526 in C006 because no terminal external Lean 4 Dirac-equation proof was found.",
  "No proof body was vendored in C006 because the audited PhysLean modules are adjacent gamma/spinor infrastructure, not a closed Dirac-equation theorem.",
  "If a terminal external proof is later found, it must be pinned/imported/checked or vendored and locally validated before any completed-state claim."
]

/-! ## First concrete target decision -/

/--
Candidate theorem families considered for the first concrete THM-M-1526 target.

The selected first target below is intentionally finite-dimensional and
constant-coefficient.  It is a matrix/symbol problem, so later workers can
replace the abstract Clifford proposition by an explicit finite anticommutator
identity before taking on unbounded PDE domains, conserved currents, or
self-adjointness.
-/
inductive FirstConcreteDiracTarget : Type
  | freeFlatSpaceEquation
  | finiteDimensionalConstantCoefficientMatrixModel
  | conservedCurrent
  | selfAdjointHamiltonian
  | squaredOperatorKleinGordonBridge
  deriving DecidableEq, Repr

/-- The first concrete closure target selected by child `S1-M-194-C001`. -/
def selectedFirstConcreteTarget : FirstConcreteDiracTarget :=
  .finiteDimensionalConstantCoefficientMatrixModel

/-- Checked witness for the selected first concrete target. -/
theorem selectedFirstConcreteTarget_eq :
    selectedFirstConcreteTarget =
      FirstConcreteDiracTarget.finiteDimensionalConstantCoefficientMatrixModel :=
  rfl

/--
Finite-dimensional constant-coefficient Dirac symbol data.

Here `σ` indexes spinor components, `ι` indexes spacetime directions, `gamma`
is a concrete matrix family, and `momentum` is the constant-coefficient Fourier
or algebraic replacement for the derivative variables.  The Clifford relation
is already a finite matrix anticommutator identity, making this the next
machine-checkable refinement target.
-/
structure FiniteConstantCoefficientDiracData
    (ι : Type uι) (σ : Type uσ) [Fintype ι] [Fintype σ] [DecidableEq σ] :
    Type (max uι uσ) where
  gamma : ι → Matrix σ σ ℂ
  metric : ι → ι → ℂ
  momentum : ι → ℂ
  mass : ℂ
  potential : Matrix σ σ ℂ
  clifford_anticommutator : ∀ μ ν : ι,
    gamma μ * gamma ν + gamma ν * gamma μ =
      (2 * metric μ ν) • (1 : Matrix σ σ ℂ)

/--
The finite constant-coefficient Dirac matrix symbol
`Σ_μ p_μ γ^μ - m I + V`.
-/
def finiteConstantCoefficientDiracSymbol
    {ι : Type uι} {σ : Type uσ} [Fintype ι] [Fintype σ] [DecidableEq σ]
    (D : FiniteConstantCoefficientDiracData ι σ) : Matrix σ σ ℂ :=
  (∑ μ : ι, D.momentum μ • D.gamma μ) -
    D.mass • (1 : Matrix σ σ ℂ) + D.potential

/-- Algebraic finite-dimensional Dirac equation for the selected first target. -/
def finiteConstantCoefficientDiracEquation
    {ι : Type uι} {σ : Type uσ} [Fintype ι] [Fintype σ] [DecidableEq σ]
    (D : FiniteConstantCoefficientDiracData ι σ) (ψ : σ → ℂ) : Prop :=
  Matrix.mulVec (finiteConstantCoefficientDiracSymbol D) ψ = 0

/-- The finite-dimensional selected target unfolds to its matrix-vector equation. -/
theorem finiteConstantCoefficientDiracEquation_iff
    {ι : Type uι} {σ : Type uσ} [Fintype ι] [Fintype σ] [DecidableEq σ]
    (D : FiniteConstantCoefficientDiracData ι σ) (ψ : σ → ℂ) :
    finiteConstantCoefficientDiracEquation D ψ ↔
      Matrix.mulVec (finiteConstantCoefficientDiracSymbol D) ψ = 0 :=
  Iff.rfl

/--
Sanity check for the selected finite-dimensional homogeneous equation: the zero
spinor is a formal algebraic solution.  Nonzero kernel, dispersion, and
spectral claims remain separate future leaves.
-/
theorem finiteConstantCoefficientDirac_zero_solution
    {ι : Type uι} {σ : Type uσ} [Fintype ι] [Fintype σ] [DecidableEq σ]
    (D : FiniteConstantCoefficientDiracData ι σ) :
    finiteConstantCoefficientDiracEquation D 0 := by
  simp [finiteConstantCoefficientDiracEquation]

/-! ## Concrete finite gamma representation -/

/-- First Pauli generator used as a concrete two-component gamma matrix. -/
def pauliGammaX : Matrix (Fin 2) (Fin 2) ℂ :=
  ![![0, 1], ![1, 0]]

/-- Second Pauli generator used as a concrete two-component gamma matrix. -/
def pauliGammaZ : Matrix (Fin 2) (Fin 2) ℂ :=
  ![![1, 0], ![0, -1]]

/-- Selected `Fin 2` gamma-matrix representation for the first finite Clifford leaf. -/
def pauliFinTwoGamma : Fin 2 → Matrix (Fin 2) (Fin 2) ℂ
  | 0 => pauliGammaX
  | 1 => pauliGammaZ

/-- Euclidean two-generator metric for the selected Pauli gamma representation. -/
def pauliFinTwoMetric (μ ν : Fin 2) : ℂ :=
  if μ = ν then 1 else 0

/--
Concrete finite-index anticommutator identity for the selected Pauli
representation:
`γ μ γ ν + γ ν γ μ = 2 δ μν I`.

This closes only the finite gamma-algebra child leaf; it is not a Lorentzian
four-dimensional Dirac-equation theorem.
-/
theorem pauliFinTwo_clifford_anticommutator (μ ν : Fin 2) :
    pauliFinTwoGamma μ * pauliFinTwoGamma ν +
        pauliFinTwoGamma ν * pauliFinTwoGamma μ =
      (2 * pauliFinTwoMetric μ ν) • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  fin_cases μ <;> fin_cases ν <;>
    ext i j <;> fin_cases i <;> fin_cases j <;>
      norm_num [pauliFinTwoGamma, pauliGammaX, pauliGammaZ,
        pauliFinTwoMetric, Matrix.mul_apply, Fin.sum_univ_two]

/--
Finite constant-coefficient Dirac data built from the selected checked Pauli
gamma representation.
-/
def pauliFiniteConstantCoefficientDiracData
    (momentum : Fin 2 → ℂ) (mass : ℂ) (potential : Matrix (Fin 2) (Fin 2) ℂ) :
    FiniteConstantCoefficientDiracData (Fin 2) (Fin 2) where
  gamma := pauliFinTwoGamma
  metric := pauliFinTwoMetric
  momentum := momentum
  mass := mass
  potential := potential
  clifford_anticommutator := pauliFinTwo_clifford_anticommutator

/-- Projection wrapper for the checked Pauli finite-data anticommutator field. -/
theorem pauliFiniteConstantCoefficientDiracData_clifford_anticommutator
    (momentum : Fin 2 → ℂ) (mass : ℂ) (potential : Matrix (Fin 2) (Fin 2) ℂ)
    (μ ν : Fin 2) :
    (pauliFiniteConstantCoefficientDiracData momentum mass potential).gamma μ *
        (pauliFiniteConstantCoefficientDiracData momentum mass potential).gamma ν +
      (pauliFiniteConstantCoefficientDiracData momentum mass potential).gamma ν *
        (pauliFiniteConstantCoefficientDiracData momentum mass potential).gamma μ =
      (2 * (pauliFiniteConstantCoefficientDiracData momentum mass potential).metric μ ν) •
        (1 : Matrix (Fin 2) (Fin 2) ℂ) :=
  (pauliFiniteConstantCoefficientDiracData momentum mass potential).clifford_anticommutator μ ν

/-! ## Derivative/operator semantics -/

/--
Possible meanings of the spacetime derivative symbol `∂_μ` for the first
Dirac-equation closure target.

The current selected target is the finite-dimensional constant-coefficient
matrix model, so derivative variables are represented by bounded algebraic
operators or Fourier-symbol scalars instead of unbounded PDE operators on a
domain.
-/
inductive DerivativeOperatorSemantics : Type
  | boundedOperator
  | unboundedOperator
  | smoothFunction
  | schwartzDistributional
  | sobolevSpace
  deriving DecidableEq, Repr

/--
Selected semantics for `∂_μ` in the first THM-M-1526 closure target.

This is a bounded-operator/algebraic-symbol boundary.  The unbounded-operator,
smooth-function, Schwartz/distributional, and Sobolev-space interpretations
remain later formalization leaves.
-/
def selectedDerivativeOperatorSemantics : DerivativeOperatorSemantics :=
  .boundedOperator

/-- Checked witness for the selected `∂_μ` semantics. -/
theorem selectedDerivativeOperatorSemantics_eq :
    selectedDerivativeOperatorSemantics =
      DerivativeOperatorSemantics.boundedOperator :=
  rfl

/--
The first concrete finite-dimensional target and the selected derivative
semantics are aligned: `∂_μ` is closed as a bounded algebraic operator/symbol,
not yet as an unbounded PDE derivative.
-/
theorem selectedTarget_uses_bounded_derivative_semantics :
    selectedFirstConcreteTarget =
        FirstConcreteDiracTarget.finiteDimensionalConstantCoefficientMatrixModel ∧
      selectedDerivativeOperatorSemantics =
        DerivativeOperatorSemantics.boundedOperator :=
  ⟨selectedFirstConcreteTarget_eq, selectedDerivativeOperatorSemantics_eq⟩

/-! ## C007 theorem-tree split and leaf-budget ledger -/

/--
The seven proof packages requested for the THM-M-1526 theorem-tree split.

Only the `gammaAlgebra` package has a repo-local checked proof leaf in the
current artifact, namely `pauliFinTwo_clifford_anticommutator`.  The remaining
packages are explicit formalization-debt boundaries rather than completed
analytic Dirac-equation theorems.
-/
inductive DiracTheoremPackage : Type
  | gammaAlgebra
  | operatorDomain
  | selfAdjointness
  | spectralRelation
  | cauchyWellPosedness
  | conservedCurrent
  | finalWrapper
  deriving DecidableEq, Repr

/-- Current repo-local closure status for each C007 theorem-tree package. -/
inductive DiracLeafClosureStatus : Type
  | localProofBody
  | checkedStatementBoundary
  | formalizationDebt
  deriving DecidableEq, Repr

/--
A compact checked budget record for one theorem-tree package.

`stepBudget` is the local proof-process budget assigned to this leaf.  A status
of `formalizationDebt` means the package is deliberately not claimed as proved.
-/
structure DiracProofLeafBudget : Type where
  package : DiracTheoremPackage
  stepBudget : Nat
  status : DiracLeafClosureStatus
  deriving DecidableEq, Repr

/--
C007 theorem-tree split into `<= 100`-step package leaves.

The split is intentionally conservative: it records exactly the seven requested
packages and assigns each a local budget below the M0387 threshold.  It does not
turn the open analytic packages into completed theorems.
-/
def diracTheoremLeafBudgetPlan : List DiracProofLeafBudget := [
  { package := .gammaAlgebra, stepBudget := 24, status := .localProofBody },
  { package := .operatorDomain, stepBudget := 32, status := .checkedStatementBoundary },
  { package := .selfAdjointness, stepBudget := 36, status := .formalizationDebt },
  { package := .spectralRelation, stepBudget := 40, status := .formalizationDebt },
  { package := .cauchyWellPosedness, stepBudget := 44, status := .formalizationDebt },
  { package := .conservedCurrent, stepBudget := 36, status := .formalizationDebt },
  { package := .finalWrapper, stepBudget := 28, status := .formalizationDebt }
]

/-- Machine-checked C007 budget gate: every current package leaf is `<= 100` steps. -/
theorem diracTheoremLeafBudgetPlan_all_le_100 :
    diracTheoremLeafBudgetPlan.all (fun leaf => leaf.stepBudget <= 100) = true := by
  decide

/-- C007 includes the requested gamma-algebra package. -/
theorem diracTheoremLeafBudgetPlan_has_gammaAlgebra :
    { package := DiracTheoremPackage.gammaAlgebra,
      stepBudget := 24,
      status := DiracLeafClosureStatus.localProofBody } ∈
      diracTheoremLeafBudgetPlan := by
  simp [diracTheoremLeafBudgetPlan]

/-- C007 includes the requested operator-domain package. -/
theorem diracTheoremLeafBudgetPlan_has_operatorDomain :
    { package := DiracTheoremPackage.operatorDomain,
      stepBudget := 32,
      status := DiracLeafClosureStatus.checkedStatementBoundary } ∈
      diracTheoremLeafBudgetPlan := by
  simp [diracTheoremLeafBudgetPlan]

/-- C007 includes the requested self-adjointness package. -/
theorem diracTheoremLeafBudgetPlan_has_selfAdjointness :
    { package := DiracTheoremPackage.selfAdjointness,
      stepBudget := 36,
      status := DiracLeafClosureStatus.formalizationDebt } ∈
      diracTheoremLeafBudgetPlan := by
  simp [diracTheoremLeafBudgetPlan]

/-- C007 includes the requested spectral-relation package. -/
theorem diracTheoremLeafBudgetPlan_has_spectralRelation :
    { package := DiracTheoremPackage.spectralRelation,
      stepBudget := 40,
      status := DiracLeafClosureStatus.formalizationDebt } ∈
      diracTheoremLeafBudgetPlan := by
  simp [diracTheoremLeafBudgetPlan]

/-- C007 includes the requested Cauchy/well-posedness package. -/
theorem diracTheoremLeafBudgetPlan_has_cauchyWellPosedness :
    { package := DiracTheoremPackage.cauchyWellPosedness,
      stepBudget := 44,
      status := DiracLeafClosureStatus.formalizationDebt } ∈
      diracTheoremLeafBudgetPlan := by
  simp [diracTheoremLeafBudgetPlan]

/-- C007 includes the requested conserved-current package. -/
theorem diracTheoremLeafBudgetPlan_has_conservedCurrent :
    { package := DiracTheoremPackage.conservedCurrent,
      stepBudget := 36,
      status := DiracLeafClosureStatus.formalizationDebt } ∈
      diracTheoremLeafBudgetPlan := by
  simp [diracTheoremLeafBudgetPlan]

/-- C007 includes the requested final-wrapper package. -/
theorem diracTheoremLeafBudgetPlan_has_finalWrapper :
    { package := DiracTheoremPackage.finalWrapper,
      stepBudget := 28,
      status := DiracLeafClosureStatus.formalizationDebt } ∈
      diracTheoremLeafBudgetPlan := by
  simp [diracTheoremLeafBudgetPlan]

/--
C007 repo-local integration-debt gate.

The split records a local proof body only for finite Pauli gamma algebra and
does not use URL-only external evidence as completion evidence.  Hence this
child leaves formalization debt, not completed-state repo-local integration
debt.
-/
def diracTheoremLeafBudgetRepoLocalIntegrationDebtRetained : Bool := false

/-- Checked witness that C007 retains no completed-state repo-local integration debt. -/
theorem diracTheoremLeafBudgetRepoLocalIntegrationDebtRetained_eq :
    diracTheoremLeafBudgetRepoLocalIntegrationDebtRetained = false :=
  rfl

/-! ## C008 public-surface backfill gate -/

/--
Public Stage1 backfill status for child `S1-M-194-C008`.

This child is a serial public-document integration task by request, but this
worker is not allowed to edit shared public planning documents directly.  The
Lean artifact therefore records an integration-ready status instead of changing
`Docs/Stage1_Blueprint.md` or shared import aggregators.
-/
inductive DiracPublicBackfillStatus : Type
  | readyForSerialIntegrator
  | blockedByUnstableMachineAnchors
  | publicDocsSynchronized
  deriving DecidableEq, Repr

/-- Current C008 status: public backfill is ready for a serial integrator. -/
def diracPublicBackfillStatus : DiracPublicBackfillStatus :=
  .readyForSerialIntegrator

/-- Checked witness for the current public-backfill status. -/
theorem diracPublicBackfillStatus_eq :
    diracPublicBackfillStatus =
      DiracPublicBackfillStatus.readyForSerialIntegrator :=
  rfl

/--
C008 public synchronization facts that an integrator can merge into the public
Stage1 surface.
-/
def diracPublicBackfillFacts : List String := [
  "Machine artifact: Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_194.lean.",
  "Current repo-local status: not_repo_local_closed; the artifact is a statement-shape and finite gamma-algebra boundary, not a terminal Dirac-equation proof.",
  "Checked local proof body: pauliFinTwo_clifford_anticommutator for a Fin 2 Pauli gamma anticommutator identity.",
  "Selected first target: finiteDimensionalConstantCoefficientMatrixModel.",
  "Selected derivative semantics: boundedOperator/algebraic-symbol boundary.",
  "External closure gate: noTerminalClosureFound; no external Lean 4 Dirac-equation proof was pinned, vendored, or checked.",
  "Theorem-tree packages: gammaAlgebra has localProofBody; operatorDomain is checkedStatementBoundary; selfAdjointness, spectralRelation, cauchyWellPosedness, conservedCurrent, and finalWrapper remain formalizationDebt.",
  "Repo-local integration-debt gate: no completed-state repo_local_integration_debt is retained."
]

/--
C008 records that public documents were not edited by this worker.

The value is deliberately `false`: public synchronization must be done by the
serial integrator that owns shared planning documents.
-/
def diracPublicDocsEditedByC008 : Bool := false

/-- Checked witness that C008 did not edit public shared planning docs. -/
theorem diracPublicDocsEditedByC008_eq :
    diracPublicDocsEditedByC008 = false :=
  rfl

/-- C008 repo-local integration-debt gate for the public backfill child. -/
def diracPublicBackfillRepoLocalIntegrationDebtRetained : Bool := false

/-- Checked witness that C008 retains no completed-state repo-local integration debt. -/
theorem diracPublicBackfillRepoLocalIntegrationDebtRetained_eq :
    diracPublicBackfillRepoLocalIntegrationDebtRetained = false :=
  rfl

/-! ## Audit probes -/

#check FieldOperator
#check GammaSystem
#check DiracModelData
#check DiracOperator
#check DiracEquation
#check DiracSolution
#check StatementShape
#check StatementShape.intro
#check GammaSystem.clifford_anticommutator_holds
#check diracOperator_apply
#check zero_satisfies_homogeneous_dirac
#check continuousLinearMap_id_apply_anchor
#check continuousLinearMap_comp_apply_anchor
#check CliffordAlgebra
#check CliffordAlgebra.ι_sq_scalar
#check clifford_generator_square_anchor
#check spinGroup
#check spinGroup.mem_iff
#check spinGroup.mem_pin
#check spinGroup.mem_even
#check spinGroup.involute_eq
#check spinGroup.units_involute_act_eq_conjAct
#check spinGroup.conjAct_smul_ι_mem_range_ι
#check spinGroup.involute_act_ι_mem_range_ι
#check spinGroup.conjAct_smul_range_ι
#check spinGroup.toUnits
#check spinGroup.toUnits_injective
#check pinGroup
#check pinGroup.mem_iff
#check pinGroup.conjAct_smul_ι_mem_range_ι
#check pinGroup.involute_act_ι_mem_range_ι
#check lipschitzGroup
#check lipschitzGroup.conjAct_smul_ι_mem_range_ι
#check lipschitzGroup.involute_act_ι_mem_range_ι
#check lipschitzGroup.conjAct_smul_range_ι
#check CliffordAlgebra.foldr
#check CliffordAlgebra.foldr_ι
#check CliffordAlgebra.foldr_algebraMap
#check CliffordAlgebra.foldr_one
#check CliffordAlgebra.foldr_mul
#check CliffordAlgebra.foldr_prod_map_ι
#check CliffordAlgebra.foldl
#check CliffordAlgebra.foldl_reverse
#check CliffordAlgebra.foldr_reverse
#check CliffordAlgebra.foldl_ι
#check CliffordAlgebra.foldl_algebraMap
#check CliffordAlgebra.foldl_one
#check CliffordAlgebra.foldl_mul
#check CliffordAlgebra.foldl_prod_map_ι
#check CliffordAlgebra.right_induction
#check CliffordAlgebra.left_induction
#check CliffordAlgebra.foldr'
#check CliffordAlgebra.foldr'_algebraMap
#check CliffordAlgebra.foldr'_ι
#check CliffordAlgebra.foldr'_ι_mul
#check Matrix.ext
#check Matrix.mul_apply
#check Matrix.mul_apply'
#check Matrix.mulVec
#check Matrix.mulVec_eq_sum
#check Matrix.mulVec_zero
#check Matrix.sum_mulVec
#check Matrix.mulVec_sum
#check Matrix.smul_mul
#check Matrix.mul_smul
#check Matrix.one_apply
#check Matrix.diagonal
#check Matrix.diagonal_mul
#check Matrix.mul_diagonal
#check Matrix.diagonal_mul_diagonal
#check Matrix.toLin
#check Matrix.toLin_apply
#check Matrix.toLin_mul
#check Matrix.toLin_mul_apply
#check Matrix.toLin'
#check Matrix.toLin'_apply
#check Matrix.toLin'_mul
#check Matrix.toLin'_mul_apply
#check FirstConcreteDiracTarget
#check selectedFirstConcreteTarget
#check selectedFirstConcreteTarget_eq
#check FiniteConstantCoefficientDiracData
#check finiteConstantCoefficientDiracSymbol
#check finiteConstantCoefficientDiracEquation
#check finiteConstantCoefficientDiracEquation_iff
#check finiteConstantCoefficientDirac_zero_solution
#check pauliGammaX
#check pauliGammaZ
#check pauliFinTwoGamma
#check pauliFinTwoMetric
#check pauliFinTwo_clifford_anticommutator
#check pauliFiniteConstantCoefficientDiracData
#check pauliFiniteConstantCoefficientDiracData_clifford_anticommutator
#check externalDiracLeanSearchTerms
#check externalDiracLeanCandidates
#check externalDiracAuditBlockers
#check ExternalDiracClosureIntegrationStatus
#check externalDiracClosureIntegrationStatus
#check externalDiracClosureIntegrationStatus_eq
#check externalDiracClosureIntegrationActions
#check DerivativeOperatorSemantics
#check selectedDerivativeOperatorSemantics
#check selectedDerivativeOperatorSemantics_eq
#check selectedTarget_uses_bounded_derivative_semantics
#check DiracTheoremPackage
#check DiracLeafClosureStatus
#check DiracProofLeafBudget
#check diracTheoremLeafBudgetPlan
#check diracTheoremLeafBudgetPlan_all_le_100
#check diracTheoremLeafBudgetPlan_has_gammaAlgebra
#check diracTheoremLeafBudgetPlan_has_operatorDomain
#check diracTheoremLeafBudgetPlan_has_selfAdjointness
#check diracTheoremLeafBudgetPlan_has_spectralRelation
#check diracTheoremLeafBudgetPlan_has_cauchyWellPosedness
#check diracTheoremLeafBudgetPlan_has_conservedCurrent
#check diracTheoremLeafBudgetPlan_has_finalWrapper
#check diracTheoremLeafBudgetRepoLocalIntegrationDebtRetained
#check diracTheoremLeafBudgetRepoLocalIntegrationDebtRetained_eq
#check DiracPublicBackfillStatus
#check diracPublicBackfillStatus
#check diracPublicBackfillStatus_eq
#check diracPublicBackfillFacts
#check diracPublicDocsEditedByC008
#check diracPublicDocsEditedByC008_eq
#check diracPublicBackfillRepoLocalIntegrationDebtRetained
#check diracPublicBackfillRepoLocalIntegrationDebtRetained_eq

end AwesomeTheorems.Stage1.S1_M_194
