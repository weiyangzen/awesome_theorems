import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.Calculus.LineDeriv.Basic
import Mathlib.Analysis.Distribution.Distribution
import Mathlib.Analysis.Distribution.FourierMultiplier
import Mathlib.Analysis.Distribution.TemperedDistribution
import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.Analysis.InnerProductSpace.Laplacian
import Mathlib.MeasureTheory.Function.LpSpace.Basic

/-!
# S1-M-166 / THM-M-1307: Klainerman null-condition theorem

This Stage1 artifact records a conservative Lean 4 boundary for the
Klainerman small-data global existence theorem for nonlinear wave equations
satisfying the null condition.

The pinned mathlib snapshot has useful adjacent infrastructure: classical
derivatives, directional derivatives, the spatial Laplacian, distributions,
tempered-distribution Fourier multiplier identities, `MemLp`/`eLpNorm`, and
first-derivative Sobolev inequalities.  This audit did not find a terminal
Lean 4 theorem for nonlinear wave equations, the null condition, vector-field
commutator estimates, or global small-data existence.

The declarations below therefore normalize the formal statement shape and
provide only low-risk wrappers around available mathlib facts.  They introduce
no proof placeholders and do not claim the terminal PDE theorem.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal NNReal SchwartzMap Topology

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_166

universe u v

/-- Flat space-time model used for a finite-dimensional wave equation. -/
abbrev SpaceTime (ι : Type u) [Fintype ι] : Type u :=
  ℝ × EuclideanSpace ℝ ι

/-- Scalar space-time field used by the normalized Klainerman statement. -/
abbrev ScalarField (ι : Type u) [Fintype ι] : Type u :=
  SpaceTime ι → ℝ

/--
Formal classical wave operator `∂_t^2 u - Δ_x u`.

This is an expression-level object.  A terminal Klainerman theorem still needs
a bridge to the selected weak/classical solution predicate, initial data,
commuting vector fields, decay estimates, and continuation criterion.
-/
def waveOperatorFormal {ι : Type u} [Fintype ι] (u : ScalarField ι) :
    ScalarField ι :=
  fun z =>
    deriv (fun t : ℝ => deriv (fun τ : ℝ => u (τ, z.2)) t) z.1 -
      Laplacian.laplacian (fun x : EuclideanSpace ℝ ι => u (z.1, x)) z.2

/-- The formal wave operator unfolds to second time derivative minus spatial Laplacian. -/
theorem waveOperatorFormal_apply
    {ι : Type u} [Fintype ι] (u : ScalarField ι) (z : SpaceTime ι) :
    waveOperatorFormal u z =
      deriv (fun t : ℝ => deriv (fun τ : ℝ => u (τ, z.2)) t) z.1 -
        Laplacian.laplacian (fun x : EuclideanSpace ℝ ι => u (z.1, x)) z.2 :=
  rfl

/-- The Minkowski quadratic form used to state a finite-coordinate null cone. -/
def minkowskiQuadraticForm {ι : Type u} [Fintype ι] (v : SpaceTime ι) : ℝ :=
  v.1 ^ 2 - ‖v.2‖ ^ 2

/-- A vector is null when its Minkowski quadratic form vanishes. -/
def IsNullVector {ι : Type u} [Fintype ι] (v : SpaceTime ι) : Prop :=
  minkowskiQuadraticForm v = 0

/--
Stage1 encoding of the quadratic null condition.

`Q z ξ η` is an abstract bilinear/null-form coefficient package at the point
`z`.  The checked predicate records the required vanishing on null directions
without pretending that the full quadratic nonlinearity has already been tied
to all first derivatives of `u`.
-/
def NullConditionOnQuadratic
    {ι : Type u} [Fintype ι]
    (Q : SpaceTime ι → SpaceTime ι → SpaceTime ι → ℝ) : Prop :=
  ∀ z ξ : SpaceTime ι, IsNullVector ξ → Q z ξ ξ = 0

/-! ## Concrete null-form model -/

/-- The unit future time direction used for first-derivative components. -/
def timeDirection {ι : Type u} [Fintype ι] : SpaceTime ι :=
  (1, 0)

/-- The spatial coordinate direction `∂ᵢ` inside the finite-dimensional model. -/
def spatialCoordinateDirection {ι : Type u} [Fintype ι] (i : ι) : SpaceTime ι := by
  classical
  exact (0, EuclideanSpace.single i (1 : ℝ))

/-- First time derivative component of a scalar field. -/
def timeDerivativeComponent
    {ι : Type u} [Fintype ι] (u : ScalarField ι) (z : SpaceTime ι) : ℝ :=
  lineDeriv ℝ u z (timeDirection : SpaceTime ι)

/-- First spatial coordinate derivative component of a scalar field. -/
def spatialDerivativeComponent
    {ι : Type u} [Fintype ι] (u : ScalarField ι) (z : SpaceTime ι) (i : ι) : ℝ :=
  lineDeriv ℝ u z (spatialCoordinateDirection i)

/-- Spatial first-derivative vector, packaged as a Euclidean coordinate vector. -/
def spatialDerivativeComponents
    {ι : Type u} [Fintype ι] (u : ScalarField ι) (z : SpaceTime ι) :
    EuclideanSpace ℝ ι :=
  (EuclideanSpace.equiv ι ℝ).symm fun i => spatialDerivativeComponent u z i

/--
Full first-derivative component vector `(∂ₜu, ∇ₓu)` in the flat space-time
model.  This supplies a concrete argument type for the algebraic null forms
below without claiming a full PDE solution theory.
-/
def firstDerivativeComponents
    {ι : Type u} [Fintype ι] (u : ScalarField ι) (z : SpaceTime ι) :
    SpaceTime ι :=
  (timeDerivativeComponent u z, spatialDerivativeComponents u z)

/-- Minkowski bilinear form `m(ξ,η) = ξ₀η₀ - ξₓ · ηₓ`. -/
def minkowskiBilinearForm
    {ι : Type u} [Fintype ι] (ξ η : SpaceTime ι) : ℝ :=
  ξ.1 * η.1 - inner ℝ ξ.2 η.2

/-- The diagonal of the Minkowski bilinear form is the stored quadratic form. -/
theorem minkowskiBilinearForm_self
    {ι : Type u} [Fintype ι] (ξ : SpaceTime ι) :
    minkowskiBilinearForm ξ ξ = minkowskiQuadraticForm ξ := by
  unfold minkowskiBilinearForm minkowskiQuadraticForm
  rw [real_inner_self_eq_norm_sq]
  ring

/-- The standard scalar null form `Q₀` vanishes when both slots are the same null vector. -/
theorem minkowskiBilinearForm_vanishes_on_null
    {ι : Type u} [Fintype ι] {ξ : SpaceTime ι}
    (hξ : IsNullVector ξ) :
    minkowskiBilinearForm ξ ξ = 0 := by
  rw [minkowskiBilinearForm_self, hξ]

/-- The standard scalar null form satisfies the abstract null-condition predicate. -/
theorem minkowskiBilinearForm_nullCondition
    {ι : Type u} [Fintype ι] :
    NullConditionOnQuadratic
      (fun _ ξ η : SpaceTime ι => minkowskiBilinearForm ξ η) := by
  intro _ ξ hξ
  exact minkowskiBilinearForm_vanishes_on_null hξ

/-- Coordinate index for time (`none`) or a spatial direction (`some i`). -/
abbrev NullFormCoordinate (ι : Type u) : Type u :=
  Option ι

/-- Extract a time/spatial coordinate from a space-time vector. -/
def spacetimeCoordinateComponent
    {ι : Type u} [Fintype ι] (a : NullFormCoordinate ι) (ξ : SpaceTime ι) : ℝ :=
  match a with
  | none => ξ.1
  | some i => ξ.2 i

/--
Coordinate antisymmetric null form `Q_{ab}(ξ,η) = ξ_a η_b - ξ_b η_a`.

These are the algebraic models for the classical Klainerman null forms
`Q_{αβ}(∂u, ∂v)`.
-/
def coordinateNullForm
    {ι : Type u} [Fintype ι] (a b : NullFormCoordinate ι)
    (ξ η : SpaceTime ι) : ℝ :=
  spacetimeCoordinateComponent a ξ * spacetimeCoordinateComponent b η -
    spacetimeCoordinateComponent b ξ * spacetimeCoordinateComponent a η

/-- Every antisymmetric coordinate null form vanishes on a repeated vector. -/
theorem coordinateNullForm_self
    {ι : Type u} [Fintype ι] (a b : NullFormCoordinate ι) (ξ : SpaceTime ι) :
    coordinateNullForm a b ξ ξ = 0 := by
  unfold coordinateNullForm
  ring

/-- Coordinate antisymmetric null forms satisfy the abstract null-condition predicate. -/
theorem coordinateNullForm_nullCondition
    {ι : Type u} [Fintype ι] (a b : NullFormCoordinate ι) :
    NullConditionOnQuadratic
      (fun _ ξ η : SpaceTime ι => coordinateNullForm a b ξ η) := by
  intro _ ξ _
  exact coordinateNullForm_self a b ξ

/-- Field-level scalar null form `Q₀(∂u,∂v)` built from first derivatives. -/
def fieldNullFormQ0
    {ι : Type u} [Fintype ι] (u v : ScalarField ι) (z : SpaceTime ι) : ℝ :=
  minkowskiBilinearForm (firstDerivativeComponents u z) (firstDerivativeComponents v z)

/-- Field-level coordinate null form `Q_{ab}(∂u,∂v)` built from first derivatives. -/
def fieldCoordinateNullForm
    {ι : Type u} [Fintype ι] (a b : NullFormCoordinate ι)
    (u v : ScalarField ι) (z : SpaceTime ι) : ℝ :=
  coordinateNullForm a b (firstDerivativeComponents u z) (firstDerivativeComponents v z)

/-! ## Vector-field method scaffold -/

/--
Classical vector-field families used by the Klainerman vector-field method.

This is a syntactic family of infinitesimal directions on the finite
Minkowski model.  It is not yet a proof of the wave-operator commutator
identities or the commuted null-form estimates.
-/
inductive KlainermanVectorFieldKind (ι : Type u) [Fintype ι] : Type u where
  | translation (direction : SpaceTime ι)
  | spatialRotation (i j : ι)
  | scaling
  | lorentzBoost (i : ι)

/-- The space-time vector field associated to a classical Klainerman generator. -/
def klainermanVectorField
    {ι : Type u} [Fintype ι] :
    KlainermanVectorFieldKind ι → SpaceTime ι → SpaceTime ι := by
  classical
  intro V z
  cases V with
  | translation direction => exact direction
  | spatialRotation i j =>
      exact
        (0,
          z.2 i • EuclideanSpace.single j (1 : ℝ) -
            z.2 j • EuclideanSpace.single i (1 : ℝ))
  | scaling => exact z
  | lorentzBoost i =>
      exact (z.2 i, z.1 • EuclideanSpace.single i (1 : ℝ))

/-- Apply a Klainerman generator to a scalar field as a directional derivative. -/
def applyKlainermanVectorField
    {ι : Type u} [Fintype ι]
    (V : KlainermanVectorFieldKind ι) (u : ScalarField ι) (z : SpaceTime ι) : ℝ :=
  lineDeriv ℝ u z (klainermanVectorField V z)

/--
Formal commutator of the wave operator with one Klainerman generator.

The identities `[□, ∂] = 0`, `[□, Ω] = 0`, `[□, L] = 0`, and `[□, S] = c□`
are left as future proof obligations; this declaration only fixes the checked
expression that those leaves should refine.
-/
def waveVectorFieldCommutatorFormal
    {ι : Type u} [Fintype ι]
    (V : KlainermanVectorFieldKind ι) (u : ScalarField ι) :
    ScalarField ι :=
  fun z =>
    waveOperatorFormal (fun y => applyKlainermanVectorField V u y) z -
      applyKlainermanVectorField V (waveOperatorFormal u) z

/-- M0387 child leaves for `THM-M-1307.vector-field-method`. -/
inductive VectorFieldMethodLeafKind where
  | translations
  | rotations
  | scaling
  | lorentzBoosts
  | commutatorIdentities
  | nullFormCommutationStability
deriving Repr

/-- Checked row format for the vector-field-method public backfill. -/
structure VectorFieldMethodLeafRow where
  leaf : VectorFieldMethodLeafKind
  publicTaskId : String
  localLeanAnchor : String
  requiredProofObject : String
  currentMachineStatus : String
  repoLocalIntegrationDebtStatus : String
deriving Repr

/--
Integration-ready task split for `THM-M-1307.vector-field-method`.

Every row is intentionally marked as an open proof obligation.  The checked
repo-local progress here is only the task split and the expression-level
scaffold for generators and commutators.
-/
def vectorFieldMethodLeafRows : List VectorFieldMethodLeafRow := [
  { leaf := .translations,
    publicTaskId := "THM-M-1307.vector-field.translations",
    localLeanAnchor :=
      "AwesomeTheorems.Stage1.S1_M_166.KlainermanVectorFieldKind.translation",
    requiredProofObject :=
      "Define all time/spatial translations and prove their wave-operator commutators.",
    currentMachineStatus :=
      "formalization_debt: generator syntax checked; commutator theorem not proved",
    repoLocalIntegrationDebtStatus := "none_detected_no_external_closure_claimed" },
  { leaf := .rotations,
    publicTaskId := "THM-M-1307.vector-field.rotations",
    localLeanAnchor :=
      "AwesomeTheorems.Stage1.S1_M_166.KlainermanVectorFieldKind.spatialRotation",
    requiredProofObject :=
      "Define spatial rotations and prove rotation commutator identities for the wave operator.",
    currentMachineStatus :=
      "formalization_debt: generator syntax checked; rotation commutator theorem not proved",
    repoLocalIntegrationDebtStatus := "none_detected_no_external_closure_claimed" },
  { leaf := .scaling,
    publicTaskId := "THM-M-1307.vector-field.scaling",
    localLeanAnchor :=
      "AwesomeTheorems.Stage1.S1_M_166.KlainermanVectorFieldKind.scaling",
    requiredProofObject :=
      "Define the scaling vector field and prove its controlled wave commutator.",
    currentMachineStatus :=
      "formalization_debt: generator syntax checked; scaling commutator theorem not proved",
    repoLocalIntegrationDebtStatus := "none_detected_no_external_closure_claimed" },
  { leaf := .lorentzBoosts,
    publicTaskId := "THM-M-1307.vector-field.lorentz-boosts",
    localLeanAnchor :=
      "AwesomeTheorems.Stage1.S1_M_166.KlainermanVectorFieldKind.lorentzBoost",
    requiredProofObject :=
      "Define Lorentz boosts and prove their wave-operator commutator identities.",
    currentMachineStatus :=
      "formalization_debt: generator syntax checked; Lorentz-boost commutator theorem not proved",
    repoLocalIntegrationDebtStatus := "none_detected_no_external_closure_claimed" },
  { leaf := .commutatorIdentities,
    publicTaskId := "THM-M-1307.vector-field.commutator-identities",
    localLeanAnchor :=
      "AwesomeTheorems.Stage1.S1_M_166.waveVectorFieldCommutatorFormal",
    requiredProofObject :=
      "Prove the full commutator table between the formal wave operator and every generator.",
    currentMachineStatus :=
      "formalization_debt: formal commutator expression checked; identity table not proved",
    repoLocalIntegrationDebtStatus := "none_detected_no_external_closure_claimed" },
  { leaf := .nullFormCommutationStability,
    publicTaskId := "THM-M-1307.vector-field.null-form-commutation-stability",
    localLeanAnchor :=
      "AwesomeTheorems.Stage1.S1_M_166.fieldNullFormQ0; " ++
        "AwesomeTheorems.Stage1.S1_M_166.fieldCoordinateNullForm",
    requiredProofObject :=
      "Prove that commuted null-form estimates remain null-form estimates for the generator algebra.",
    currentMachineStatus :=
      "formalization_debt: null-form anchors checked; stability estimate theorem not proved",
    repoLocalIntegrationDebtStatus := "none_detected_no_external_closure_claimed" }
]

/-- The vector-field-method split has exactly the six requested M0387 leaves. -/
theorem vectorFieldMethodLeafRows_length :
    vectorFieldMethodLeafRows.length = 6 :=
  rfl

/--
Completion boundary for the vector-field-method child.

This child has no external anchor-only completion claim and therefore does not
introduce repo-local integration debt.  The remaining work is formalization
debt: actual commutator identities and stability estimates still need proofs.
-/
def vectorFieldMethodCompletionGate : String :=
  "not_completed_formalization_debt: translations, rotations, scaling, Lorentz " ++
    "boosts, commutator identities, and null-form commutation stability are " ++
    "split into checked M0387 child leaves with local expression anchors; no " ++
    "external anchor-only theorem closure is claimed, and no repo_local_" ++
    "integration_debt is retained"

/-! ## Energy-decay package scaffold -/

/-- M0387 child leaves for `THM-M-1307.energy-decay`. -/
inductive EnergyDecayLeafKind where
  | weightedEnergyEstimates
  | klainermanSobolevDecay
  | nullFormImprovedEstimates
  | smallDataBootstrap
deriving Repr

/-- Checked row format for the energy-decay public backfill. -/
structure EnergyDecayLeafRow where
  leaf : EnergyDecayLeafKind
  publicTaskId : String
  localLeanAnchor : String
  requiredProofObject : String
  currentMachineStatus : String
  maxLeafProofBudget : Nat
  repoLocalIntegrationDebtStatus : String
deriving Repr

/--
Integration-ready task split for `THM-M-1307.energy-decay`.

Every row is intentionally an open proof obligation with a `<=100` local
budget.  The checked repo-local progress is the decomposition boundary and the
connection to the existing statement-shape hypotheses; it is not a weighted
energy estimate, Klainerman-Sobolev inequality, null-form decay theorem, or
bootstrap closure proof.
-/
def energyDecayLeafRows : List EnergyDecayLeafRow := [
  { leaf := .weightedEnergyEstimates,
    publicTaskId := "THM-M-1307.energy-decay.weighted-energy-estimates",
    localLeanAnchor :=
      "AwesomeTheorems.Stage1.S1_M_166.KlainermanInput.weightedEnergyEstimatePackage",
    requiredProofObject :=
      "Formalize the weighted high-order energy functional, commuted energy inequality, " ++
        "source-term estimate, and Gronwall/continuation transfer as separate leaves.",
    currentMachineStatus :=
      "formalization_debt: statement-shape hypothesis only; no weighted energy theorem proved",
    maxLeafProofBudget := 100,
    repoLocalIntegrationDebtStatus := "none_detected_no_external_closure_claimed" },
  { leaf := .klainermanSobolevDecay,
    publicTaskId := "THM-M-1307.energy-decay.klainerman-sobolev-decay",
    localLeanAnchor :=
      "AwesomeTheorems.Stage1.S1_M_166.GlobalExistencePackage.pointwiseDecay",
    requiredProofObject :=
      "Formalize the Klainerman-Sobolev inequality from commuted L2 energies to pointwise " ++
        "space-time decay, with coordinate weights and finite vector-field multiindices.",
    currentMachineStatus :=
      "formalization_debt: output field exists as a proposition; no decay theorem proved",
    maxLeafProofBudget := 100,
    repoLocalIntegrationDebtStatus := "none_detected_no_external_closure_claimed" },
  { leaf := .nullFormImprovedEstimates,
    publicTaskId := "THM-M-1307.energy-decay.null-form-improved-estimates",
    localLeanAnchor :=
      "AwesomeTheorems.Stage1.S1_M_166.fieldNullFormQ0; " ++
        "AwesomeTheorems.Stage1.S1_M_166.fieldCoordinateNullForm",
    requiredProofObject :=
      "Prove the improved bilinear estimates for Q0 and coordinate antisymmetric null forms " ++
        "using good derivatives, cone weights, and commuted first-derivative bounds.",
    currentMachineStatus :=
      "formalization_debt: algebraic null-form anchors checked; improved estimates not proved",
    maxLeafProofBudget := 100,
    repoLocalIntegrationDebtStatus := "none_detected_no_external_closure_claimed" },
  { leaf := .smallDataBootstrap,
    publicTaskId := "THM-M-1307.energy-decay.small-data-bootstrap",
    localLeanAnchor :=
      "AwesomeTheorems.Stage1.S1_M_166.KlainermanInput.decayBootstrapPackage; " ++
        "AwesomeTheorems.Stage1.S1_M_166.KlainermanInput.continuationCriterionPackage",
    requiredProofObject :=
      "Formalize the small-data bootstrap assumptions, improvement step, bootstrap closure, " ++
        "and continuation criterion that convert energy/decay bounds into global existence.",
    currentMachineStatus :=
      "formalization_debt: bootstrap and continuation are explicit hypotheses only",
    maxLeafProofBudget := 100,
    repoLocalIntegrationDebtStatus := "none_detected_no_external_closure_claimed" }
]

/-- The energy-decay split has exactly the four requested M0387 leaf packages. -/
theorem energyDecayLeafRows_length :
    energyDecayLeafRows.length = 4 :=
  rfl

/-- Every energy-decay child leaf is budgeted at the M0387 `<=100` proof-step limit. -/
theorem energyDecayLeafRows_all_budget_le_100 :
    energyDecayLeafRows.all (fun row => row.maxLeafProofBudget ≤ 100) = true :=
  rfl

/--
Completion boundary for the energy-decay child.

This child introduces no external anchor-only completion claim and therefore no
repo-local integration debt.  The remaining work is formalization debt: the
weighted energy estimates, Klainerman-Sobolev decay theorem, null-form improved
estimates, and small-data bootstrap still need proof bodies.
-/
def energyDecayCompletionGate : String :=
  "not_completed_formalization_debt: weighted energy estimates, Klainerman-" ++
    "Sobolev decay, null-form improved estimates, and small-data bootstrap are " ++
    "split into four checked M0387 leaf packages with <=100 budgets; no " ++
    "external anchor-only theorem closure is claimed, and no repo_local_" ++
    "integration_debt is retained"

/--
Concrete null-form child completion gate.

This child supplies checked algebraic null forms and first-derivative component
packaging.  It does not supply vector-field commutators, energy/decay estimates,
bootstrap, continuation, or a terminal global-existence theorem.
-/
def nullFormModelCompletionGate : String :=
  "passed_for_concrete_null_form_model_only: Q0 and coordinate antisymmetric " ++
    "null forms are defined over the finite Minkowski model, first-derivative " ++
    "components are packaged by lineDeriv, and the algebraic null-direction " ++
    "vanishing obligations are checked; parent Klainerman theorem remains open " ++
    "formalization_debt, not completed"

/--
Input data for a future formal Klainerman theorem.

The fields that currently lack mathlib-level infrastructure remain explicit
propositions: null-form representation of the nonlinearity, vector-field
commutators, weighted energy estimates, decay bootstrap, and continuation.
-/
structure KlainermanInput (ι : Type u) [Fintype ι] : Type u where
  spacetimeDomain : Set (SpaceTime ι)
  u : ScalarField ι
  nonlinearity : ScalarField ι → ScalarField ι
  quadraticForm : SpaceTime ι → SpaceTime ι → SpaceTime ι → ℝ
  smallDataNorm : ℝ≥0∞
  smallDataThreshold : ℝ≥0∞
  domainOpen : IsOpen spacetimeDomain
  initialDataSmooth : Prop
  smallData : smallDataNorm < smallDataThreshold
  classicalWaveEquation :
    ∀ z ∈ spacetimeDomain, waveOperatorFormal u z = nonlinearity u z
  nonlinearTermQuadraticNullForm : Prop
  quadraticNullCondition : NullConditionOnQuadratic quadraticForm
  vectorFieldCommutatorPackage : Prop
  weightedEnergyEstimatePackage : Prop
  decayBootstrapPackage : Prop
  continuationCriterionPackage : Prop

/--
Output package expected from Klainerman's small-data global existence theorem.

Because Lean functions are total, global existence is represented by explicit
coverage of every time slice by the modeled space-time domain.
-/
structure GlobalExistencePackage
    {ι : Type u} [Fintype ι] (X : KlainermanInput ι) : Type u where
  solutionRegularity : ContDiffOn ℝ 2 X.u X.spacetimeDomain
  globalTimeCoverage :
    ∀ t : ℝ, ∃ x : EuclideanSpace ℝ ι, (t, x) ∈ X.spacetimeDomain
  solvesEquation :
    ∀ z ∈ X.spacetimeDomain, waveOperatorFormal X.u z = X.nonlinearity X.u z
  energyBound : Prop
  energyBound_holds : energyBound
  pointwiseDecay : Prop
  pointwiseDecay_holds : pointwiseDecay
  continuationCriterion : Prop
  continuationCriterion_holds : continuationCriterion

/--
Normalized Stage1 statement shape for THM-M-1307.

For every finite-dimensional space-time model and audited nonlinear wave input,
smooth small initial data, null-form structure, vector-field commutators,
weighted energy estimates, decay bootstrap, and continuation data should
produce a global classical solution package.  The high-risk PDE content remains
as explicit hypotheses because no terminal Lean 4 proof was found locally.
-/
def StatementShape : Prop :=
  ∀ (ι : Type u) [Fintype ι] (X : KlainermanInput ι),
    X.initialDataSmooth →
      X.nonlinearTermQuadraticNullForm →
        X.vectorFieldCommutatorPackage →
          X.weightedEnergyEstimatePackage →
            X.decayBootstrapPackage →
              X.continuationCriterionPackage →
                Nonempty (GlobalExistencePackage X)

/--
Public Stage1 boundary alias for the Klainerman null-condition slot.

This is definitionally just `StatementShape`.  It is intentionally a
statement-normalization boundary, not a proof of global small-data existence.
-/
def Stage1StatementBoundary : Prop :=
  StatementShape.{u}

/--
The public Stage1 boundary is exactly the normalized `StatementShape`.

This wrapper lets documentation cite a checked declaration while keeping the
terminal theorem status open until the null-form model, vector-field method,
energy-decay package, bootstrap, and continuation proof are actually supplied.
-/
theorem stage1StatementBoundary_iff :
    Stage1StatementBoundary.{u} ↔ StatementShape.{u} :=
  Iff.rfl

/--
Machine-readable integration note for the public blueprint backfill.

The checked boundary is useful for public statement normalization only; it does
not complete Klainerman's null-condition global-existence theorem.
-/
def statementShapeBoundaryNote : String :=
  "AwesomeTheorems.Stage1.S1_M_166.StatementShape is the checked Stage1 Lean " ++
    "statement boundary for THM-M-1307 / Klainerman's null-condition theorem; " ++
    "it is not a terminal global-existence proof."

/-- Checked declaration names for the statement-boundary backfill. -/
def statementShapeBoundaryDeclarations : List String := [
  "AwesomeTheorems.Stage1.S1_M_166.StatementShape",
  "AwesomeTheorems.Stage1.S1_M_166.Stage1StatementBoundary",
  "AwesomeTheorems.Stage1.S1_M_166.stage1StatementBoundary_iff",
  "AwesomeTheorems.Stage1.S1_M_166.statementShapeBoundaryNote"
]

/-- Pinned mathlib revision audited for the THM-M-1307 Stage1 module row. -/
def pinnedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- One requested mathlib module-availability row for the Klainerman audit. -/
structure MathlibModuleAuditRow where
  publicModuleLabel : String
  importPath : String
  pinnedRevision : String
  availabilityStatus : String
deriving Repr

/--
Requested pinned-mathlib module audit for `THM-M-1307.mathlib-audit`.

Every row is availability evidence only.  These modules provide adjacent
calculus, distribution, Fourier-multiplier, Sobolev, and `Lp` infrastructure;
they do not contain a terminal Klainerman null-condition global-existence
theorem.
-/
def mathlibModuleAuditRows : List MathlibModuleAuditRow := [
  { publicModuleLabel := "ContDiff.Basic",
    importPath := "Mathlib.Analysis.Calculus.ContDiff.Basic",
    pinnedRevision := pinnedMathlibRevision,
    availabilityStatus := "available_imported_and_checked" },
  { publicModuleLabel := "LineDeriv.Basic",
    importPath := "Mathlib.Analysis.Calculus.LineDeriv.Basic",
    pinnedRevision := pinnedMathlibRevision,
    availabilityStatus := "available_imported_and_checked" },
  { publicModuleLabel := "InnerProductSpace.Laplacian",
    importPath := "Mathlib.Analysis.InnerProductSpace.Laplacian",
    pinnedRevision := pinnedMathlibRevision,
    availabilityStatus := "available_imported_and_checked" },
  { publicModuleLabel := "Distribution",
    importPath := "Mathlib.Analysis.Distribution.Distribution",
    pinnedRevision := pinnedMathlibRevision,
    availabilityStatus := "available_imported_and_checked" },
  { publicModuleLabel := "TemperedDistribution",
    importPath := "Mathlib.Analysis.Distribution.TemperedDistribution",
    pinnedRevision := pinnedMathlibRevision,
    availabilityStatus := "available_imported_and_checked" },
  { publicModuleLabel := "FourierMultiplier",
    importPath := "Mathlib.Analysis.Distribution.FourierMultiplier",
    pinnedRevision := pinnedMathlibRevision,
    availabilityStatus := "available_imported_and_checked" },
  { publicModuleLabel := "FunctionalSpaces.SobolevInequality",
    importPath := "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
    pinnedRevision := pinnedMathlibRevision,
    availabilityStatus := "available_imported_and_checked" },
  { publicModuleLabel := "LpSpace.Basic",
    importPath := "Mathlib.MeasureTheory.Function.LpSpace.Basic",
    pinnedRevision := pinnedMathlibRevision,
    availabilityStatus := "available_imported_and_checked" }
]

/-- The child mathlib-module audit has exactly the eight requested rows. -/
theorem mathlibModuleAuditRows_length :
    mathlibModuleAuditRows.length = 8 :=
  rfl

/--
Completion boundary for the mathlib-audit child.

The requested modules are locally checked at the pinned revision, but this row
is not a terminal theorem closure for Klainerman's theorem.
-/
def mathlibAuditCompletionNote : String :=
  "At mathlib revision " ++ pinnedMathlibRevision ++
    ", the requested ContDiff, LineDeriv, Laplacian, Distribution, " ++
    "TemperedDistribution, FourierMultiplier, SobolevInequality, and LpSpace " ++
    "modules are available in the local Lake closure; this is infrastructure " ++
    "evidence only, not a Klainerman global-existence proof."

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (ι : Type u) [Fintype ι] (X : KlainermanInput ι),
      X.initialDataSmooth →
        X.nonlinearTermQuadraticNullForm →
          X.vectorFieldCommutatorPackage →
            X.weightedEnergyEstimatePackage →
              X.decayBootstrapPackage →
                X.continuationCriterionPackage →
                  Nonempty (GlobalExistencePackage X)) :
    StatementShape.{u} :=
  h

/-- Checked wrapper exposing the stored null-condition predicate. -/
theorem quadratic_null_condition
    {ι : Type u} [Fintype ι] (X : KlainermanInput ι) :
    NullConditionOnQuadratic X.quadraticForm :=
  X.quadraticNullCondition

/-- Checked wrapper exposing the formal classical wave-equation residual. -/
theorem waveEquation_holds
    {ι : Type u} [Fintype ι] (X : KlainermanInput ι) :
    ∀ z ∈ X.spacetimeDomain, waveOperatorFormal X.u z = X.nonlinearity X.u z :=
  X.classicalWaveEquation

/-- Extract the global time-coverage conclusion from a solution package. -/
theorem global_time_coverage
    {ι : Type u} [Fintype ι] {X : KlainermanInput ι}
    (G : GlobalExistencePackage X) :
    ∀ t : ℝ, ∃ x : EuclideanSpace ℝ ι, (t, x) ∈ X.spacetimeDomain :=
  G.globalTimeCoverage

/-- Extract the equation component from a global-existence package. -/
theorem GlobalExistencePackage.solves_equation
    {ι : Type u} [Fintype ι] {X : KlainermanInput ι}
    (G : GlobalExistencePackage X) :
    ∀ z ∈ X.spacetimeDomain, waveOperatorFormal X.u z = X.nonlinearity X.u z :=
  G.solvesEquation

/-- Checked mathlib anchor: the Laplacian is additive for `C^2` functions at a point. -/
theorem laplacian_add_anchor
    {ι : Type u} [Fintype ι] {f g : EuclideanSpace ℝ ι → ℝ}
    {x : EuclideanSpace ℝ ι}
    (hf : ContDiffAt ℝ 2 f x) (hg : ContDiffAt ℝ 2 g x) :
    Laplacian.laplacian (fun y => f y + g y) x =
      Laplacian.laplacian f x + Laplacian.laplacian g x := by
  simpa [Pi.add_apply] using hf.laplacian_add hg

/-- Checked mathlib anchor: directional derivatives scale in their direction argument. -/
theorem lineDeriv_smul_anchor
    {ι : Type u} [Fintype ι] (u : ScalarField ι)
    (z v : SpaceTime ι) (c : ℝ) :
    lineDeriv ℝ u z (c • v) = c * lineDeriv ℝ u z v := by
  simpa using (lineDeriv_smul (𝕜 := ℝ) (f := u) (x := z) (v := v) (c := c))

/-- Checked mathlib anchor: the distributional Laplacian is a Fourier multiplier. -/
theorem tempered_laplacian_fourierMultiplier_anchor
    {E F : Type v} [NormedAddCommGroup E] [NormedAddCommGroup F]
    [InnerProductSpace ℝ E] [NormedSpace ℂ F] [FiniteDimensional ℝ E]
    [MeasurableSpace E] [BorelSpace E]
    (f : TemperedDistribution E F) :
    Laplacian.laplacian f =
      -((2 * Real.pi : ℝ) ^ 2) •
        (TemperedDistribution.fourierMultiplierCLM F fun x => ((‖x‖ ^ 2 : ℝ) : ℂ)) f :=
  TemperedDistribution.laplacian_eq_fourierMultiplierCLM f

/-- Checked mathlib anchor: distributional directional derivative as a Fourier multiplier. -/
theorem tempered_lineDeriv_fourierMultiplier_anchor
    {E F : Type v} [NormedAddCommGroup E] [NormedAddCommGroup F]
    [InnerProductSpace ℝ E] [NormedSpace ℂ F] [FiniteDimensional ℝ E]
    [MeasurableSpace E] [BorelSpace E]
    (m : E) (f : TemperedDistribution E F) :
    LineDeriv.lineDerivOp m f =
      (2 * (Real.pi : ℂ) * Complex.I) •
        (TemperedDistribution.fourierMultiplierCLM F fun x => (inner ℝ x m : ℂ)) f :=
  TemperedDistribution.lineDeriv_eq_fourierMultiplierCLM m f

/-- Audit row for available wrappers that are infrastructure anchors only. -/
structure AvailableWrapperAnchorRow where
  localWrapper : String
  upstreamDeclaration : String
  repoLocalStatus : String
  theoremClosureStatus : String
  publicUse : String
deriving Repr

/--
Checked wrapper inventory for `THM-M-1307.available-wrapper`.

Every listed declaration validates repo-locally as adjacent PDE infrastructure.
None is a terminal Klainerman null-condition theorem, and none discharges the
remaining null-form, vector-field, energy-decay, bootstrap, or continuation
packages.
-/
def availableWrapperAnchorRows : List AvailableWrapperAnchorRow := [
  { localWrapper := "AwesomeTheorems.Stage1.S1_M_166.laplacian_add_anchor",
    upstreamDeclaration := "ContDiffAt.laplacian_add",
    repoLocalStatus := "local_wrapper_upstream_mathlib_infrastructure_anchor",
    theoremClosureStatus := "not_klainerman_theorem_closure",
    publicUse := "spatial Laplacian additivity anchor only" },
  { localWrapper := "AwesomeTheorems.Stage1.S1_M_166.lineDeriv_smul_anchor",
    upstreamDeclaration := "lineDeriv_smul",
    repoLocalStatus := "local_wrapper_upstream_mathlib_infrastructure_anchor",
    theoremClosureStatus := "not_klainerman_theorem_closure",
    publicUse := "directional-derivative homogeneity anchor only" },
  { localWrapper :=
      "AwesomeTheorems.Stage1.S1_M_166.tempered_laplacian_fourierMultiplier_anchor",
    upstreamDeclaration := "TemperedDistribution.laplacian_eq_fourierMultiplierCLM",
    repoLocalStatus := "local_wrapper_upstream_mathlib_infrastructure_anchor",
    theoremClosureStatus := "not_klainerman_theorem_closure",
    publicUse := "distributional Laplacian Fourier-multiplier anchor only" },
  { localWrapper :=
      "AwesomeTheorems.Stage1.S1_M_166.tempered_lineDeriv_fourierMultiplier_anchor",
    upstreamDeclaration := "TemperedDistribution.lineDeriv_eq_fourierMultiplierCLM",
    repoLocalStatus := "local_wrapper_upstream_mathlib_infrastructure_anchor",
    theoremClosureStatus := "not_klainerman_theorem_closure",
    publicUse := "distributional directional-derivative Fourier-multiplier anchor only" }
]

/-- The available-wrapper child has exactly the four requested infrastructure anchors. -/
theorem availableWrapperAnchorRows_length :
    availableWrapperAnchorRows.length = 4 :=
  rfl

/--
M0387 gate note for the available-wrapper child.

The local wrappers are checked mathlib infrastructure anchors, so there is no
external anchor-only integration debt for this child.  The parent Klainerman
theorem remains open as formalization debt until a terminal proof body or
pinned dependency validates repo-locally.
-/
def availableWrapperInfrastructureOnlyGate : String :=
  "passed_for_infrastructure_anchors_only: the four available wrappers validate " ++
    "repo-locally as pinned mathlib infrastructure anchors, but they are not a " ++
    "Klainerman null-condition global-existence closure; parent terminal theorem " ++
    "status remains open formalization_debt, not completed"

/-- mathlib modules checked while locating repo-local anchors for this PDE slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Calculus.ContDiff.Basic",
  "Mathlib.Analysis.Calculus.LineDeriv.Basic",
  "Mathlib.Analysis.InnerProductSpace.Laplacian",
  "Mathlib.Analysis.Distribution.Distribution",
  "Mathlib.Analysis.Distribution.TemperedDistribution",
  "Mathlib.Analysis.Distribution.FourierMultiplier",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "Mathlib.Analysis.Fourier.LpSpace",
  "Mathlib.MeasureTheory.Function.LpSpace.Basic"
]

/-- Checked declaration names used as Stage1 anchors. -/
def mathlibAnchorNames : List String := [
  "deriv",
  "fderiv",
  "lineDeriv",
  "lineDeriv_smul",
  "Laplacian.laplacian",
  "ContDiffOn",
  "ContDiffAt.laplacian_add",
  "MeasureTheory.MemLp",
  "MeasureTheory.eLpNorm",
  "MeasureTheory.eLpNorm_le_eLpNorm_fderiv",
  "Distribution",
  "TemperedDistribution",
  "TemperedDistribution.lineDeriv_eq_fourierMultiplierCLM",
  "TemperedDistribution.laplacian_eq_fourierMultiplierCLM"
]

/-- Search terms requested for the THM-M-1307 external Lean 4 audit. -/
def externalLeanAuditSearchTerms : List String := [
  "Klainerman",
  "null condition",
  "null form",
  "wave equation",
  "dAlembertian",
  "D'Alembert",
  "dAlembert",
  "Minkowski space",
  "nonlinear wave",
  "small data global existence",
  "vector field method",
  "Lorentz boost",
  "Klainerman-Sobolev"
]

/--
Search terms that did not locate a terminal Klainerman/null-condition theorem
in the pinned local Lean source closure.
-/
def absentTerminalSearchTerms : List String :=
  externalLeanAuditSearchTerms

/-- One source surface checked for terminal external Lean 4 evidence. -/
structure ExternalLeanAuditSurfaceRow where
  sourceName : String
  repoUrl : String
  commit : String
  toolchain : String
  searchedTerms : List String
  terminalTheoremNames : List String
  placeholderStatus : String
  lakeDependencyFeasibility : String
  completionStatus : String
deriving Repr

/--
Primary-source Lean 4 surfaces checked for `THM-M-1307.external-audit`.

The checked rows are negative terminal-theorem evidence only: no row contains a
Klainerman null-condition global-existence proof, and no external anchor-only
completion claim is made.
-/
def externalLeanAuditSurfaceRows : List ExternalLeanAuditSurfaceRow := [
  { sourceName := "mathlib4 pinned Lake dependency",
    repoUrl := "https://github.com/leanprover-community/mathlib4.git",
    commit := pinnedMathlibRevision,
    toolchain := "leanprover/lean4:v4.29.0",
    searchedTerms := externalLeanAuditSearchTerms,
    terminalTheoremNames := [],
    placeholderStatus :=
      "no terminal Klainerman/null-condition source hit in Mathlib or docs-only wave-equation note",
    lakeDependencyFeasibility :=
      "already pinned/imported as mathlib infrastructure; no terminal theorem to import",
    completionStatus := "not_repo_local_closed_formalization_debt" },
  { sourceName := "flt-regular pinned Lake dependency",
    repoUrl := "https://github.com/leanprover-community/flt-regular.git",
    commit := "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27",
    toolchain := "leanprover/lean4:v4.29.0",
    searchedTerms := externalLeanAuditSearchTerms,
    terminalTheoremNames := [],
    placeholderStatus := "no requested-term source hits",
    lakeDependencyFeasibility :=
      "already pinned for unrelated number-theory work; no Klainerman theorem to import",
    completionStatus := "not_repo_local_closed_formalization_debt" }
]

/-- The external-audit search-term list records the thirteen checked terms. -/
theorem externalLeanAuditSearchTerms_length :
    externalLeanAuditSearchTerms.length = 13 :=
  rfl

/-- The repo-local external-audit table records the two pinned Lean source surfaces. -/
theorem externalLeanAuditSurfaceRows_length :
    externalLeanAuditSurfaceRows.length = 2 :=
  rfl

/--
M0387 external-audit gate for this Stage1 artifact.

No external Lean 4 terminal proof has been found, pinned, imported, or checked.
Therefore the parent theorem remains open formalization debt rather than a
completed state with repo-local integration debt.
-/
def externalLeanAuditCompletionGate : String :=
  "not_completed_formalization_debt: authenticated GitHub code search was " ++
    "unavailable in this environment, and pinned local Lean source searches " ++
    "found no terminal Klainerman/null-condition theorem; no external " ++
    "anchor-only completion is claimed, and no repo_local_integration_debt " ++
    "is retained as completed"

/-- One integration-gate decision row for external Lean 4 theorem closures. -/
structure IntegrationGateDecisionRow where
  publicTaskId : String
  checkedLocalSurfaces : List String
  externalClosureFound : Bool
  repoLocalActionRequiredBeforeCompletion : String
  currentGateStatus : String
deriving Repr

/--
Integration-gate surface for `THM-M-1307.integration-gate`.

This row records the repo-local decision boundary: the current Lake closure has
no terminal Klainerman theorem to pin/import/check.  If a future authenticated
external audit locates such a Lean 4 closure, the public task must remain open
until that proof is either included in the repo-local validation closure or a
specific blocker is recorded.
-/
def integrationGateDecisionRows : List IntegrationGateDecisionRow := [
  { publicTaskId := "THM-M-1307.integration-gate",
    checkedLocalSurfaces := [
      "mathlib4@8a178386ffc0f5fef0b77738bb5449d50efeea95",
      "flt-regular@56161b6eb5281fbfe9c38f2bcec0f429ebc11a27",
      "AwesomeTheorems.Stage1.S1_M_166.externalLeanAuditSurfaceRows"
    ],
    externalClosureFound := false,
    repoLocalActionRequiredBeforeCompletion :=
      "No completion claim is permitted from anchor-only evidence.  If an external " ++
        "Lean 4 Klainerman/null-condition global-existence proof is later found, " ++
        "pin/import/check it in the Lake closure or record a concrete blocker " ++
        "such as incompatible Lean toolchain, dependency conflict, license barrier, " ++
        "or proof placeholders in the relevant path.",
    currentGateStatus :=
      "open_not_completed: no external Lean 4 closure was found in the current " ++
        "repo-local Lake closure, and no external_upstream_anchor_only state is " ++
        "being counted as completed" }
]

/-- The integration-gate child contributes exactly one decision row. -/
theorem integrationGateDecisionRows_length :
    integrationGateDecisionRows.length = 1 :=
  rfl

/--
M0387 completion gate for the integration-gate child.

There is no completed-state repo-local integration debt because this artifact
does not count any external anchor-only evidence as a theorem closure.  The
parent theorem remains open until a terminal local proof body, mathlib wrapper,
or pinned external dependency is validated.
-/
def integrationGateCompletionGate : String :=
  "open_not_completed_no_repo_local_integration_debt: no external Lean 4 " ++
    "Klainerman/null-condition global-existence closure is present in the " ++
    "current Lake validation closure; any future external closure must be " ++
    "pinned/imported/checked or blocked concretely before public completion"

/-! ## Audit probes -/

#check deriv
#check fderiv
#check lineDeriv
#check Laplacian.laplacian
#check ContDiffAt.laplacian_add
#check lineDeriv_smul
#check MeasureTheory.MemLp
#check MeasureTheory.eLpNorm
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv
#check Distribution
#check TemperedDistribution.lineDeriv_eq_fourierMultiplierCLM
#check TemperedDistribution.laplacian_eq_fourierMultiplierCLM
#check pinnedMathlibRevision
#check mathlibModuleAuditRows
#check mathlibModuleAuditRows_length
#check mathlibAuditCompletionNote
#check availableWrapperAnchorRows
#check availableWrapperAnchorRows_length
#check availableWrapperInfrastructureOnlyGate
#check timeDirection
#check spatialCoordinateDirection
#check firstDerivativeComponents
#check minkowskiBilinearForm
#check minkowskiBilinearForm_self
#check minkowskiBilinearForm_nullCondition
#check coordinateNullForm
#check coordinateNullForm_self
#check coordinateNullForm_nullCondition
#check fieldNullFormQ0
#check fieldCoordinateNullForm
#check nullFormModelCompletionGate
#check KlainermanVectorFieldKind
#check klainermanVectorField
#check applyKlainermanVectorField
#check waveVectorFieldCommutatorFormal
#check vectorFieldMethodLeafRows
#check vectorFieldMethodLeafRows_length
#check vectorFieldMethodCompletionGate
#check externalLeanAuditSearchTerms
#check externalLeanAuditSearchTerms_length
#check externalLeanAuditSurfaceRows
#check externalLeanAuditSurfaceRows_length
#check externalLeanAuditCompletionGate
#check integrationGateDecisionRows
#check integrationGateDecisionRows_length
#check integrationGateCompletionGate

end S1_M_166
end Stage1
end AwesomeTheorems
