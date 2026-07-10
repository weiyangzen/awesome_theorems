import Mathlib.Analysis.Distribution.Distribution
import Mathlib.Analysis.Fourier.LpSpace
import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.Analysis.InnerProductSpace.Laplacian
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic

/-!
# S1-M-153 / THM-M-1214: Cazenave-Weissler theorem

This Stage1 artifact records a conservative Lean 4 statement boundary for the
Cazenave-Weissler critical-regularity theorem for nonlinear Schrodinger
equations.

The pinned mathlib snapshot has concrete substrates for finite-dimensional
Euclidean space, `Lp`/`MemLp`, Fourier transforms on `L2`, distributions,
Laplacians, and first-order Sobolev inequalities.  It does not expose a
terminal nonlinear-Schrodinger, Strichartz-estimate, critical-Sobolev-space, or
well-posedness theorem.  The declarations below therefore normalize the
statement shape and add checked wrappers around available mathlib anchors
without introducing proof placeholders or claiming the terminal PDE result.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal NNReal FourierTransform Distributions

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_153

universe u

/-- Spatial model for the normalized NLS statement boundary. -/
abbrev Space (n : ℕ) : Type :=
  EuclideanSpace ℝ (Fin n)

/-- Space-time model for an NLS solution. -/
abbrev SpaceTime (n : ℕ) : Type :=
  ℝ × Space n

/-- Complex-valued initial data on Euclidean space. -/
abbrev InitialDatum (n : ℕ) : Type :=
  Space n → ℂ

/-- Complex-valued space-time field used for the NLS solution. -/
abbrev SolutionField (n : ℕ) : Type :=
  SpaceTime n → ℂ

/-- The sign convention for the power-type NLS nonlinearity. -/
inductive NLSSign : Type where
  | focusing
  | defocusing
  deriving DecidableEq, Repr

/-- Real coefficient attached to the selected NLS sign. -/
def nlsSignCoefficient : NLSSign → ℝ
  | .focusing => -1
  | .defocusing => 1

/--
The power nonlinearity `|z|^p z` used in the Cazenave-Weissler NLS boundary.

The exponent is kept as a real parameter because the critical relation is part
of the later scaling package.  This definition only fixes the formula-level
nonlinear term.
-/
def nlsPowerNonlinearity (p : ℝ) (z : ℂ) : ℂ :=
  (Real.rpow ‖z‖ p : ℝ) • z

/-- Signed power nonlinearity `σ |z|^p z` with `σ = ±1`. -/
def nlsSignedPowerNonlinearity (σ : NLSSign) (p : ℝ) (z : ℂ) : ℂ :=
  (nlsSignCoefficient σ : ℂ) * nlsPowerNonlinearity p z

/-- Spatial profile at a fixed time. -/
def timeSlice {n : ℕ} (u : SolutionField n) (t : ℝ) : InitialDatum n :=
  fun x => u (t, x)

/-- Time curve at a fixed spatial point. -/
def spatialPointCurve {n : ℕ} (u : SolutionField n) (x : Space n) : ℝ → ℂ :=
  fun t => u (t, x)

/-- Classical time derivative of a candidate NLS solution at `(t, x)`. -/
def nlsTimeDerivative {n : ℕ} (u : SolutionField n) (t : ℝ) (x : Space n) : ℂ :=
  deriv (spatialPointCurve u x) t

/-- Classical spatial Laplacian of a candidate NLS solution at `(t, x)`. -/
def nlsSpatialLaplacian {n : ℕ} (u : SolutionField n) (t : ℝ) : Space n → ℂ :=
  Laplacian.laplacian (timeSlice u t)

/--
Classical formula-level NLS residual
`i u_t + Δu - σ |u|^p u`.

This is a checked statement boundary for the pointwise equation.  Smoothness,
weak/distributional bridges, and estimates are separate proof packages.
-/
def classicalNLSResidual {n : ℕ} (σ : NLSSign) (p : ℝ)
    (u : SolutionField n) (t : ℝ) (x : Space n) : ℂ :=
  Complex.I * nlsTimeDerivative u t x + nlsSpatialLaplacian u t x -
    nlsSignedPowerNonlinearity σ p (u (t, x))

/--
Pointwise classical NLS equation over `Space n` with real exponent `p` and
focusing/defocusing sign `σ`.
-/
def ClassicalNLS {n : ℕ} (σ : NLSSign) (p : ℝ) (u : SolutionField n) : Prop :=
  ∀ t x, classicalNLSResidual σ p u t x = 0

/--
Operator data needed to state the mild/Duhamel NLS formula.

`propagator τ` is the linear Schrodinger evolution over elapsed time `τ`.
`duhamelIntegral t₀ t F` is the time integral of the already propagated source
term from `t₀` to `t`.  The analytic construction and estimates for these
operators are not claimed here.
-/
structure MildDuhamelOperators (n : ℕ) where
  propagator : ℝ → InitialDatum n → InitialDatum n
  duhamelIntegral : ℝ → ℝ → (ℝ → InitialDatum n) → InitialDatum n

/-- Spatial source profile `σ |u(t)|^p u(t)` for the NLS Duhamel term. -/
def nlsNonlinearSpatialProfile {n : ℕ} (σ : NLSSign) (p : ℝ)
    (u : SolutionField n) (t : ℝ) : InitialDatum n :=
  fun x => nlsSignedPowerNonlinearity σ p (u (t, x))

/--
The propagated nonlinear source appearing in the Duhamel integral at target
time `t`.
-/
def nlsDuhamelIntegrand {n : ℕ} (M : MildDuhamelOperators n)
    (σ : NLSSign) (p : ℝ) (u : SolutionField n) (t : ℝ) :
    ℝ → InitialDatum n :=
  fun τ => M.propagator (t - τ) (nlsNonlinearSpatialProfile σ p u τ)

/--
Mild/Duhamel NLS formulation
`u(t) = S(t-t₀)u₀ - i ∫ S(t-τ)(σ |u(τ)|^p u(τ)) dτ`.

The integral is represented by `M.duhamelIntegral`, so this definition fixes
the exact equation shape, exponent, and sign without pretending that the
Schrodinger propagator or Strichartz estimates are already available.
-/
def MildDuhamelNLS {n : ℕ} (M : MildDuhamelOperators n)
    (t₀ : ℝ) (u₀ : InitialDatum n) (σ : NLSSign) (p : ℝ)
    (u : SolutionField n) : Prop :=
  ∀ t : ℝ,
    timeSlice u t =
      M.propagator (t - t₀) u₀ +
        (-Complex.I) • M.duhamelIntegral t₀ t (nlsDuhamelIntegrand M σ p u t)

/-- The signed scalar coefficient is definitionally `-1` in the focusing case. -/
theorem nlsSignCoefficient_focusing :
    nlsSignCoefficient NLSSign.focusing = -1 :=
  rfl

/-- The signed scalar coefficient is definitionally `1` in the defocusing case. -/
theorem nlsSignCoefficient_defocusing :
    nlsSignCoefficient NLSSign.defocusing = 1 :=
  rfl

/-- The power nonlinearity unfolds to `|z|^p z`. -/
theorem nlsPowerNonlinearity_eq (p : ℝ) (z : ℂ) :
    nlsPowerNonlinearity p z = (Real.rpow ‖z‖ p : ℝ) • z :=
  rfl

/-- The mild/Duhamel predicate unfolds to the normalized equation shape. -/
theorem mildDuhamelNLS_iff {n : ℕ} (M : MildDuhamelOperators n)
    (t₀ : ℝ) (u₀ : InitialDatum n) (σ : NLSSign) (p : ℝ)
    (u : SolutionField n) :
    MildDuhamelNLS M t₀ u₀ σ p u ↔
      ∀ t : ℝ,
        timeSlice u t =
          M.propagator (t - t₀) u₀ +
            (-Complex.I) • M.duhamelIntegral t₀ t (nlsDuhamelIntegrand M σ p u t) :=
  Iff.rfl

/-- The `L^2` norm of initial data, available in the current mathlib measure API. -/
abbrev initialDatumL2Norm (n : ℕ) (u₀ : InitialDatum n) : ℝ≥0∞ :=
  eLpNorm u₀ 2 volume

/--
Fourier-side inhomogeneous Sobolev weight for `H^s(ℝ^n)`.

The weight is `(1 + ‖ξ‖^2)^(s / 2)`, so membership of the weighted Fourier
profile in `L^2` is the usual inhomogeneous `H^s` condition at the statement
boundary.
-/
def inhomogeneousSobolevWeight (n : ℕ) (s : ℝ) (ξ : Space n) : ℝ :=
  Real.rpow (1 + ‖ξ‖ ^ 2) (s / 2)

/--
Weighted Fourier profile used to express inhomogeneous critical Sobolev
membership with the pinned mathlib `L^2` Fourier transform.
-/
def weightedFourierProfile
    (n : ℕ) (s : ℝ) (u₀ : InitialDatum n)
    (hu₀ : MemLp u₀ 2 (volume : Measure (Space n))) :
    Space n → ℂ :=
  fun ξ =>
    (inhomogeneousSobolevWeight n s ξ) •
      (((𝓕 (MeasureTheory.MemLp.toLp
        (μ := (volume : Measure (Space n))) u₀ hu₀) :
          Lp ℂ 2 (volume : Measure (Space n))) : Space n → ℂ) ξ)

/--
Concrete inhomogeneous critical Sobolev membership used in the
Cazenave-Weissler statement boundary.

This is not a terminal Sobolev-space API from mathlib.  It is a repo-local
definition of the Fourier-weighted `H^s` condition over the checked Euclidean
space and `Lp` Fourier substrates available in the pinned dependency closure.
-/
def InhomogeneousCriticalSobolev (n : ℕ) (s_c : ℝ) (u₀ : InitialDatum n) : Prop :=
  ∃ hu₀ : MemLp u₀ 2 (volume : Measure (Space n)),
    MemLp (weightedFourierProfile n s_c u₀ hu₀) 2 (volume : Measure (Space n))

/--
Concrete critical Sobolev data package for the Cazenave-Weissler input datum.
-/
structure CriticalSobolevData (n : ℕ) (s_c : ℝ) (u₀ : InitialDatum n) where
  baseL2 : MemLp u₀ 2 (volume : Measure (Space n))
  weightedFourierL2 :
    MemLp (weightedFourierProfile n s_c u₀ baseL2) 2 (volume : Measure (Space n))

/-- Critical Sobolev data exposes its checked `L^2` component. -/
theorem criticalSobolevData_baseL2
    {n : ℕ} {s_c : ℝ} {u₀ : InitialDatum n}
    (h : CriticalSobolevData n s_c u₀) :
    MemLp u₀ 2 volume :=
  h.baseL2

/-- Critical Sobolev data gives the concrete inhomogeneous `H^s` membership predicate. -/
theorem criticalSobolevData_mem_inhomogeneous
    {n : ℕ} {s_c : ℝ} {u₀ : InitialDatum n}
    (h : CriticalSobolevData n s_c u₀) :
    InhomogeneousCriticalSobolev n s_c u₀ :=
  ⟨h.baseL2, h.weightedFourierL2⟩

/--
Normalized input data for a future Lean statement of the Cazenave-Weissler
critical NLS theorem.

The fields use concrete mathlib domains for initial data and solutions.  The
nonlinear equation, Strichartz admissibility, exact critical Sobolev norm, and
fixed-point hypotheses remain explicit predicates because no terminal API for
those objects was found in the pinned local dependency closure.
-/
structure CriticalNLSProblem (n : ℕ) : Type where
  criticalRegularity : ℝ
  nonlinearityPower : ℝ
  nonlinearitySign : NLSSign
  initialData : InitialDatum n
  criticalData : CriticalSobolevData n criticalRegularity initialData
  lifespan : Set ℝ
  lifespan_isOpen : IsOpen lifespan
  initialTime : ℝ
  initialTime_mem_lifespan : initialTime ∈ lifespan
  nlsEquation : SolutionField n → Prop
  initialTrace : SolutionField n → InitialDatum n → Prop
  solutionClass : SolutionField n → Prop
  strichartzAdmissiblePackage : Prop
  scalingCriticalRelation : Prop
  contractionMappingHypotheses : Prop

/--
Canonical mild/Duhamel equation attached to a normalized critical NLS problem
once a propagator/integral package has been supplied.
-/
def mildDuhamelEquationForProblem {n : ℕ} (P : CriticalNLSProblem n)
    (M : MildDuhamelOperators n) : SolutionField n → Prop :=
  MildDuhamelNLS M P.initialTime P.initialData P.nonlinearitySign P.nonlinearityPower

/-- A problem's canonical mild equation uses exactly its stored exponent and sign. -/
theorem mildDuhamelEquationForProblem_apply {n : ℕ} (P : CriticalNLSProblem n)
    (M : MildDuhamelOperators n) (u : SolutionField n) :
    mildDuhamelEquationForProblem P M u ↔
      MildDuhamelNLS M P.initialTime P.initialData P.nonlinearitySign
        P.nonlinearityPower u :=
  Iff.rfl

/-! ## Weak/classical/mild formulation bridge package -/

/--
Weak/distributional NLS formulation boundary.

The current pinned mathlib distribution API supplies distribution objects, but
not a ready-made nonlinear-Schrodinger residual operator over space-time.  This
interface therefore names the weak residual and weak trace predicates that a
future native distributional package must replace or instantiate.
-/
structure WeakNLSFormulation (n : ℕ) where
  residualVanishes : NLSSign → ℝ → SolutionField n → Prop
  weakInitialTrace : SolutionField n → InitialDatum n → Prop

/-- Weak/distributional NLS predicate supplied by a weak-formulation package. -/
def WeakNLS {n : ℕ} (W : WeakNLSFormulation n) (σ : NLSSign) (p : ℝ)
    (u : SolutionField n) : Prop :=
  W.residualVanishes σ p u

/-- The weak predicate unfolds to the residual-vanishing field. -/
theorem weakNLS_iff {n : ℕ} (W : WeakNLSFormulation n) (σ : NLSSign) (p : ℝ)
    (u : SolutionField n) :
    WeakNLS W σ p u ↔ W.residualVanishes σ p u :=
  Iff.rfl

/--
Regularity and compatibility assumptions needed by the formulation bridges.

The fields are propositions, not proofs of analytic regularity.  They isolate
the exact side conditions that later leaves must discharge: integration by
parts against test functions, Duhamel differentiation, and trace compatibility.
-/
structure FormulationBridgeRegularity {n : ℕ} (σ : NLSSign) (p : ℝ)
    (u : SolutionField n) where
  permitsIntegrationByParts : Prop
  permitsDuhamelDifferentiation : Prop
  initialTraceCompatible : Prop

/--
Bridge package connecting weak, classical, and mild/Duhamel NLS formulations.

Each field is a future theorem obligation, parameterized by the side condition
that makes the implication analytically valid.  This checked interface gives
the parent theorem tree stable Lean names without claiming that the PDE
analysis has already been formalized.
-/
structure FormulationBridgePackage {n : ℕ}
    (W : WeakNLSFormulation n) (M : MildDuhamelOperators n)
    (t₀ : ℝ) (u₀ : InitialDatum n) (σ : NLSSign) (p : ℝ)
    (u : SolutionField n) (R : FormulationBridgeRegularity σ p u) where
  classical_to_weak :
    R.permitsIntegrationByParts → ClassicalNLS σ p u → WeakNLS W σ p u
  mild_to_weak :
    R.permitsDuhamelDifferentiation →
      MildDuhamelNLS M t₀ u₀ σ p u → WeakNLS W σ p u
  classical_to_mild :
    R.permitsDuhamelDifferentiation →
      R.initialTraceCompatible →
        ClassicalNLS σ p u → MildDuhamelNLS M t₀ u₀ σ p u
  mild_to_classical :
    R.permitsDuhamelDifferentiation →
      MildDuhamelNLS M t₀ u₀ σ p u → ClassicalNLS σ p u
  weak_initial_trace :
    R.initialTraceCompatible → W.weakInitialTrace u u₀

/-- Projection theorem for the classical-to-weak bridge obligation. -/
theorem formulationBridge_classical_to_weak {n : ℕ}
    {W : WeakNLSFormulation n} {M : MildDuhamelOperators n}
    {t₀ : ℝ} {u₀ : InitialDatum n} {σ : NLSSign} {p : ℝ}
    {u : SolutionField n} {R : FormulationBridgeRegularity σ p u}
    (B : FormulationBridgePackage W M t₀ u₀ σ p u R)
    (hIBP : R.permitsIntegrationByParts) (hC : ClassicalNLS σ p u) :
    WeakNLS W σ p u :=
  B.classical_to_weak hIBP hC

/-- Projection theorem for the mild/Duhamel-to-weak bridge obligation. -/
theorem formulationBridge_mild_to_weak {n : ℕ}
    {W : WeakNLSFormulation n} {M : MildDuhamelOperators n}
    {t₀ : ℝ} {u₀ : InitialDatum n} {σ : NLSSign} {p : ℝ}
    {u : SolutionField n} {R : FormulationBridgeRegularity σ p u}
    (B : FormulationBridgePackage W M t₀ u₀ σ p u R)
    (hD : R.permitsDuhamelDifferentiation)
    (hMild : MildDuhamelNLS M t₀ u₀ σ p u) :
    WeakNLS W σ p u :=
  B.mild_to_weak hD hMild

/-- Projection theorem for the classical-to-mild bridge obligation. -/
theorem formulationBridge_classical_to_mild {n : ℕ}
    {W : WeakNLSFormulation n} {M : MildDuhamelOperators n}
    {t₀ : ℝ} {u₀ : InitialDatum n} {σ : NLSSign} {p : ℝ}
    {u : SolutionField n} {R : FormulationBridgeRegularity σ p u}
    (B : FormulationBridgePackage W M t₀ u₀ σ p u R)
    (hD : R.permitsDuhamelDifferentiation)
    (hTrace : R.initialTraceCompatible) (hC : ClassicalNLS σ p u) :
    MildDuhamelNLS M t₀ u₀ σ p u :=
  B.classical_to_mild hD hTrace hC

/-- Projection theorem for the mild/Duhamel-to-classical bridge obligation. -/
theorem formulationBridge_mild_to_classical {n : ℕ}
    {W : WeakNLSFormulation n} {M : MildDuhamelOperators n}
    {t₀ : ℝ} {u₀ : InitialDatum n} {σ : NLSSign} {p : ℝ}
    {u : SolutionField n} {R : FormulationBridgeRegularity σ p u}
    (B : FormulationBridgePackage W M t₀ u₀ σ p u R)
    (hD : R.permitsDuhamelDifferentiation)
    (hMild : MildDuhamelNLS M t₀ u₀ σ p u) :
    ClassicalNLS σ p u :=
  B.mild_to_classical hD hMild

/-- Projection theorem for weak initial-trace compatibility. -/
theorem formulationBridge_weak_initial_trace {n : ℕ}
    {W : WeakNLSFormulation n} {M : MildDuhamelOperators n}
    {t₀ : ℝ} {u₀ : InitialDatum n} {σ : NLSSign} {p : ℝ}
    {u : SolutionField n} {R : FormulationBridgeRegularity σ p u}
    (B : FormulationBridgePackage W M t₀ u₀ σ p u R)
    (hTrace : R.initialTraceCompatible) :
    W.weakInitialTrace u u₀ :=
  B.weak_initial_trace hTrace

/-- M0387-level leaves for the weak/classical/mild bridge package. -/
inductive FormulationBridgeLeaf : Type where
  | weakResidualModel
  | weakInitialTrace
  | classicalToWeakIBP
  | mildToWeakDuhamel
  | classicalToMildVariation
  | mildToClassicalRecovery
  | traceCompatibility
  | equivalenceAssembly
  deriving DecidableEq, Repr

/-- Stable public id for each formulation-bridge leaf. -/
def FormulationBridgeLeaf.stableId : FormulationBridgeLeaf → String
  | .weakResidualModel => "S1-M-153-C004-L01.weak_residual_model"
  | .weakInitialTrace => "S1-M-153-C004-L02.weak_initial_trace"
  | .classicalToWeakIBP => "S1-M-153-C004-L03.classical_to_weak_ibp"
  | .mildToWeakDuhamel => "S1-M-153-C004-L04.mild_to_weak_duhamel"
  | .classicalToMildVariation => "S1-M-153-C004-L05.classical_to_mild_variation"
  | .mildToClassicalRecovery => "S1-M-153-C004-L06.mild_to_classical_recovery"
  | .traceCompatibility => "S1-M-153-C004-L07.trace_compatibility"
  | .equivalenceAssembly => "S1-M-153-C004-L08.equivalence_assembly"

/-- Local proof-step budget for each bridge leaf. -/
def FormulationBridgeLeaf.proofStepBudget : FormulationBridgeLeaf → Nat
  | .weakResidualModel => 40
  | .weakInitialTrace => 35
  | .classicalToWeakIBP => 90
  | .mildToWeakDuhamel => 90
  | .classicalToMildVariation => 95
  | .mildToClassicalRecovery => 95
  | .traceCompatibility => 60
  | .equivalenceAssembly => 70

/-- Child C004 keeps every proposed formulation-bridge leaf at budget `<= 100`. -/
theorem formulationBridgeLeaf_budget_le_100 (leaf : FormulationBridgeLeaf) :
    leaf.proofStepBudget ≤ 100 := by
  cases leaf <;> decide

/-- Ordered theorem-tree leaves for the weak/classical/mild bridge package. -/
def formulationBridgeLeaves : List FormulationBridgeLeaf := [
  .weakResidualModel,
  .weakInitialTrace,
  .classicalToWeakIBP,
  .mildToWeakDuhamel,
  .classicalToMildVariation,
  .mildToClassicalRecovery,
  .traceCompatibility,
  .equivalenceAssembly
]

/-- The C004 bridge package has eight budgeted leaves. -/
theorem formulationBridgeLeaves_length :
    formulationBridgeLeaves.length = 8 :=
  rfl

/-- Repo-local theorem-tree package metadata for child C004. -/
structure FormulationBridgeTheoremTree where
  root : String
  leaves : List FormulationBridgeLeaf
  allLeavesBudgeted : ∀ leaf ∈ leaves, leaf.proofStepBudget ≤ 100
  completionStatus : String

/--
The C004 theorem-tree package is checked as an interface and budget split only.
The analytic bridge leaves remain unchecked formalization debt.
-/
def c004FormulationBridgeTheoremTree : FormulationBridgeTheoremTree where
  root := "weak/classical/mild formulation bridge for the Cazenave-Weissler NLS boundary"
  leaves := formulationBridgeLeaves
  allLeavesBudgeted := by
    intro leaf _hleaf
    exact formulationBridgeLeaf_budget_le_100 leaf
  completionStatus := "unchecked_formalization_debt_no_terminal_bridge_claim"

/-- The C004 theorem-tree metadata records eight leaves. -/
theorem c004FormulationBridgeTheoremTree_leaf_count :
    c004FormulationBridgeTheoremTree.leaves.length = 8 :=
  rfl

/-- C004 does not claim a completed weak/classical/mild bridge theorem. -/
theorem c004FormulationBridgeTheoremTree_status :
    c004FormulationBridgeTheoremTree.completionStatus =
      "unchecked_formalization_debt_no_terminal_bridge_claim" :=
  rfl

/-! ## Local estimate package for the contraction argument -/

/-- Linear Schrodinger evolution field generated by a normalized problem. -/
def linearEvolutionField {n : ℕ} (P : CriticalNLSProblem n)
    (M : MildDuhamelOperators n) : SolutionField n :=
  fun tx => M.propagator (tx.1 - P.initialTime) P.initialData tx.2

/-- Duhamel nonlinear term field generated by a candidate solution. -/
def duhamelNonlinearTermField {n : ℕ} (P : CriticalNLSProblem n)
    (M : MildDuhamelOperators n) (u : SolutionField n) : SolutionField n :=
  fun tx =>
    ((-Complex.I) •
      M.duhamelIntegral P.initialTime tx.1
        (nlsDuhamelIntegrand M P.nonlinearitySign P.nonlinearityPower u tx.1)) tx.2

/--
Duhamel fixed-point map associated to the normalized NLS problem.

The map is only a checked formula boundary.  The estimates below state the
analytic obligations needed to turn it into a contraction on the critical
solution space.
-/
def mildDuhamelFixedPoint {n : ℕ} (P : CriticalNLSProblem n)
    (M : MildDuhamelOperators n) (u : SolutionField n) : SolutionField n :=
  fun tx => linearEvolutionField P M tx + duhamelNonlinearTermField P M u tx

/-- The mild equation is exactly the fixed-point equation for the Duhamel map. -/
theorem mildDuhamelNLS_iff_fixedPoint {n : ℕ} (P : CriticalNLSProblem n)
    (M : MildDuhamelOperators n) (u : SolutionField n) :
    MildDuhamelNLS M P.initialTime P.initialData P.nonlinearitySign
        P.nonlinearityPower u ↔
      u = mildDuhamelFixedPoint P M u := by
  constructor
  · intro h
    funext tx
    exact congrFun (h tx.1) tx.2
  · intro h t
    funext x
    exact congrFun h (t, x)

/--
Gauge data for the critical solution and nonlinear forcing spaces.

These are deliberately gauges rather than normed-space instances: the pinned
dependency closure has no concrete Cazenave-Weissler critical solution-space
API, but the contraction proof still needs stable names for the quantitative
objects used by the local estimates.
-/
structure CriticalEstimateGauges (n : ℕ) where
  solutionGauge : SolutionField n → ℝ
  dataGauge : InitialDatum n → ℝ
  nonlinearForcingGauge : SolutionField n → ℝ
  forcingDifferenceGauge : SolutionField n → SolutionField n → ℝ
  solutionDistance : SolutionField n → SolutionField n → ℝ

/--
Local estimate package needed before the Banach contraction theorem can be
applied in the critical solution space.

Each field is a named analytic estimate or smallness condition.  The package
does not assert that the estimates have been proved from mathlib; it is the
checked interface that future Strichartz and nonlinear-estimate leaves must
instantiate.
-/
structure CriticalLocalEstimatePackage {n : ℕ} (P : CriticalNLSProblem n)
    (M : MildDuhamelOperators n) where
  gauges : CriticalEstimateGauges n
  estimateConstant : ℝ
  ballRadius : ℝ
  contractionConstant : ℝ
  gauges_nonnegative :
    (∀ u, 0 ≤ gauges.solutionGauge u) ∧
      (∀ u₀, 0 ≤ gauges.dataGauge u₀) ∧
        (∀ u, 0 ≤ gauges.nonlinearForcingGauge u) ∧
          (∀ u v, 0 ≤ gauges.forcingDifferenceGauge u v) ∧
            (∀ u v, 0 ≤ gauges.solutionDistance u v)
  radius_positive : 0 < ballRadius
  contractionConstant_nonnegative : 0 ≤ contractionConstant
  contractionConstant_lt_one : contractionConstant < 1
  linearStrichartzEstimate :
    gauges.solutionGauge (linearEvolutionField P M) ≤
      estimateConstant * gauges.dataGauge P.initialData
  duhamelStrichartzEstimate :
    ∀ u,
      gauges.solutionGauge (duhamelNonlinearTermField P M u) ≤
        estimateConstant * gauges.nonlinearForcingGauge u
  nonlinearGrowthEstimate :
    ∀ u,
      gauges.nonlinearForcingGauge u ≤
        estimateConstant *
          Real.rpow (gauges.solutionGauge u) (P.nonlinearityPower + 1)
  nonlinearLipschitzEstimate :
    ∀ u v,
      gauges.forcingDifferenceGauge u v ≤
        estimateConstant *
          (Real.rpow (gauges.solutionGauge u) P.nonlinearityPower +
            Real.rpow (gauges.solutionGauge v) P.nonlinearityPower) *
              gauges.solutionDistance u v
  duhamelLipschitzEstimate :
    ∀ u v,
      gauges.solutionDistance (duhamelNonlinearTermField P M u)
          (duhamelNonlinearTermField P M v) ≤
        estimateConstant * gauges.forcingDifferenceGauge u v
  fixedPointSelfMapEstimate :
    ∀ u,
      gauges.solutionGauge u ≤ ballRadius →
        gauges.solutionGauge (mildDuhamelFixedPoint P M u) ≤ ballRadius
  fixedPointContractionEstimate :
    ∀ u v,
      gauges.solutionGauge u ≤ ballRadius →
        gauges.solutionGauge v ≤ ballRadius →
          gauges.solutionDistance (mildDuhamelFixedPoint P M u)
              (mildDuhamelFixedPoint P M v) ≤
            contractionConstant * gauges.solutionDistance u v

/-- C005 estimate packages are recorded as available hypotheses, not terminal proofs. -/
def CriticalContractionEstimateHypotheses {n : ℕ} (P : CriticalNLSProblem n)
    (M : MildDuhamelOperators n) : Prop :=
  Nonempty (CriticalLocalEstimatePackage P M)

/-- A local estimate package supplies the C005 contraction-estimate hypotheses. -/
theorem criticalContractionEstimateHypotheses_of_package {n : ℕ}
    {P : CriticalNLSProblem n} {M : MildDuhamelOperators n}
    (E : CriticalLocalEstimatePackage P M) :
    CriticalContractionEstimateHypotheses P M :=
  ⟨E⟩

/-- Projection theorem for the homogeneous linear Strichartz estimate field. -/
theorem criticalLocalEstimate_linear {n : ℕ}
    {P : CriticalNLSProblem n} {M : MildDuhamelOperators n}
    (E : CriticalLocalEstimatePackage P M) :
    E.gauges.solutionGauge (linearEvolutionField P M) ≤
      E.estimateConstant * E.gauges.dataGauge P.initialData :=
  E.linearStrichartzEstimate

/-- Projection theorem for the Duhamel Strichartz estimate field. -/
theorem criticalLocalEstimate_duhamel {n : ℕ}
    {P : CriticalNLSProblem n} {M : MildDuhamelOperators n}
    (E : CriticalLocalEstimatePackage P M) (u : SolutionField n) :
    E.gauges.solutionGauge (duhamelNonlinearTermField P M u) ≤
      E.estimateConstant * E.gauges.nonlinearForcingGauge u :=
  E.duhamelStrichartzEstimate u

/-- Projection theorem for the nonlinear growth estimate field. -/
theorem criticalLocalEstimate_nonlinear_growth {n : ℕ}
    {P : CriticalNLSProblem n} {M : MildDuhamelOperators n}
    (E : CriticalLocalEstimatePackage P M) (u : SolutionField n) :
    E.gauges.nonlinearForcingGauge u ≤
      E.estimateConstant *
        Real.rpow (E.gauges.solutionGauge u) (P.nonlinearityPower + 1) :=
  E.nonlinearGrowthEstimate u

/-- Projection theorem for the nonlinear Lipschitz estimate field. -/
theorem criticalLocalEstimate_nonlinear_lipschitz {n : ℕ}
    {P : CriticalNLSProblem n} {M : MildDuhamelOperators n}
    (E : CriticalLocalEstimatePackage P M) (u v : SolutionField n) :
    E.gauges.forcingDifferenceGauge u v ≤
      E.estimateConstant *
        (Real.rpow (E.gauges.solutionGauge u) P.nonlinearityPower +
          Real.rpow (E.gauges.solutionGauge v) P.nonlinearityPower) *
            E.gauges.solutionDistance u v :=
  E.nonlinearLipschitzEstimate u v

/-- Projection theorem for the fixed-point self-map estimate. -/
theorem criticalLocalEstimate_self_map {n : ℕ}
    {P : CriticalNLSProblem n} {M : MildDuhamelOperators n}
    (E : CriticalLocalEstimatePackage P M) (u : SolutionField n)
    (hu : E.gauges.solutionGauge u ≤ E.ballRadius) :
    E.gauges.solutionGauge (mildDuhamelFixedPoint P M u) ≤ E.ballRadius :=
  E.fixedPointSelfMapEstimate u hu

/-- Projection theorem for the fixed-point contraction estimate. -/
theorem criticalLocalEstimate_contraction {n : ℕ}
    {P : CriticalNLSProblem n} {M : MildDuhamelOperators n}
    (E : CriticalLocalEstimatePackage P M) (u v : SolutionField n)
    (hu : E.gauges.solutionGauge u ≤ E.ballRadius)
    (hv : E.gauges.solutionGauge v ≤ E.ballRadius) :
    E.gauges.solutionDistance (mildDuhamelFixedPoint P M u)
        (mildDuhamelFixedPoint P M v) ≤
      E.contractionConstant * E.gauges.solutionDistance u v :=
  E.fixedPointContractionEstimate u v hu hv

/-- M0387-level leaves for the C005 local-estimate package. -/
inductive CriticalLocalEstimateLeaf : Type where
  | criticalSolutionGauge
  | homogeneousStrichartz
  | inhomogeneousDuhamelStrichartz
  | nonlinearGrowth
  | nonlinearLipschitz
  | ballSmallness
  | fixedPointSelfMap
  | fixedPointContraction
  | banachInputAssembly
  deriving DecidableEq, Repr

/-- Stable public id for each C005 local-estimate leaf. -/
def CriticalLocalEstimateLeaf.stableId : CriticalLocalEstimateLeaf → String
  | .criticalSolutionGauge => "S1-M-153-C005-L01.critical_solution_gauge"
  | .homogeneousStrichartz => "S1-M-153-C005-L02.homogeneous_strichartz"
  | .inhomogeneousDuhamelStrichartz =>
      "S1-M-153-C005-L03.inhomogeneous_duhamel_strichartz"
  | .nonlinearGrowth => "S1-M-153-C005-L04.nonlinear_growth"
  | .nonlinearLipschitz => "S1-M-153-C005-L05.nonlinear_lipschitz"
  | .ballSmallness => "S1-M-153-C005-L06.ball_smallness"
  | .fixedPointSelfMap => "S1-M-153-C005-L07.fixed_point_self_map"
  | .fixedPointContraction => "S1-M-153-C005-L08.fixed_point_contraction"
  | .banachInputAssembly => "S1-M-153-C005-L09.banach_input_assembly"

/-- Local proof-step budget for each C005 local-estimate leaf. -/
def CriticalLocalEstimateLeaf.proofStepBudget : CriticalLocalEstimateLeaf → Nat
  | .criticalSolutionGauge => 45
  | .homogeneousStrichartz => 95
  | .inhomogeneousDuhamelStrichartz => 95
  | .nonlinearGrowth => 90
  | .nonlinearLipschitz => 95
  | .ballSmallness => 70
  | .fixedPointSelfMap => 80
  | .fixedPointContraction => 80
  | .banachInputAssembly => 75

/-- Child C005 keeps every proposed local-estimate leaf at budget `<= 100`. -/
theorem criticalLocalEstimateLeaf_budget_le_100 (leaf : CriticalLocalEstimateLeaf) :
    leaf.proofStepBudget ≤ 100 := by
  cases leaf <;> decide

/-- Ordered theorem-tree leaves for the C005 local-estimate package. -/
def criticalLocalEstimateLeaves : List CriticalLocalEstimateLeaf := [
  .criticalSolutionGauge,
  .homogeneousStrichartz,
  .inhomogeneousDuhamelStrichartz,
  .nonlinearGrowth,
  .nonlinearLipschitz,
  .ballSmallness,
  .fixedPointSelfMap,
  .fixedPointContraction,
  .banachInputAssembly
]

/-- The C005 local-estimate package has nine budgeted leaves. -/
theorem criticalLocalEstimateLeaves_length :
    criticalLocalEstimateLeaves.length = 9 :=
  rfl

/-- Repo-local theorem-tree package metadata for child C005. -/
structure CriticalLocalEstimateTheoremTree where
  root : String
  leaves : List CriticalLocalEstimateLeaf
  allLeavesBudgeted : ∀ leaf ∈ leaves, leaf.proofStepBudget ≤ 100
  completionStatus : String

/--
The C005 theorem-tree metadata is checked as an interface and budget split only.
The analytic Strichartz and nonlinear estimate leaves remain formalization debt.
-/
def c005CriticalLocalEstimateTheoremTree : CriticalLocalEstimateTheoremTree where
  root := "local estimates for the critical NLS Duhamel contraction map"
  leaves := criticalLocalEstimateLeaves
  allLeavesBudgeted := by
    intro leaf _hleaf
    exact criticalLocalEstimateLeaf_budget_le_100 leaf
  completionStatus := "unchecked_formalization_debt_no_terminal_contraction_claim"

/-- The C005 theorem-tree metadata records nine leaves. -/
theorem c005CriticalLocalEstimateTheoremTree_leaf_count :
    c005CriticalLocalEstimateTheoremTree.leaves.length = 9 :=
  rfl

/-- C005 does not claim a completed contraction mapping theorem. -/
theorem c005CriticalLocalEstimateTheoremTree_status :
    c005CriticalLocalEstimateTheoremTree.completionStatus =
      "unchecked_formalization_debt_no_terminal_contraction_claim" :=
  rfl

/--
Conclusion package expected from the terminal Cazenave-Weissler theorem.

This records local existence, uniqueness in the critical solution class, and
continuous dependence as a formal boundary.  It is not a proof of those facts.
-/
structure CriticalNLSConclusion {n : ℕ} (P : CriticalNLSProblem n) : Type where
  solution : SolutionField n
  solvesNLS : P.nlsEquation solution
  hasInitialTrace : P.initialTrace solution P.initialData
  solution_mem_class : P.solutionClass solution
  uniqueness :
    ∀ v : SolutionField n,
      P.nlsEquation v →
        P.initialTrace v P.initialData →
          P.solutionClass v →
            v = solution
  continuousDependenceAtInitialData : Prop
  continuousDependenceAtInitialData_holds : continuousDependenceAtInitialData

/-! ## Uniqueness and continuous-dependence package -/

/--
Existence data for a candidate critical-class NLS solution.

This is separated from uniqueness and continuous dependence so child C006 can
state exactly what remains after the C004/C005 formulation and estimate leaves:
given a candidate solution and the fixed-point/metric closure package, assemble
the terminal conclusion without asserting that the analytic estimates already
exist.
-/
structure CriticalExistenceSeed {n : ℕ} (P : CriticalNLSProblem n) where
  solution : SolutionField n
  solvesNLS : P.nlsEquation solution
  hasInitialTrace : P.initialTrace solution P.initialData
  solution_mem_class : P.solutionClass solution

/--
Uniqueness and continuous-dependence package for the normalized critical NLS
problem.

The package is parameterized by a C005 local estimate package.  Its fields are
the remaining proof obligations after Strichartz and nonlinear estimates are
available: critical-class solutions lie in the contraction ball, satisfy the
Duhamel fixed-point equation, fixed points in that ball are unique, and the
solution map is continuous at the initial datum.  These are hypotheses here,
not terminal Cazenave-Weissler proof claims.
-/
structure CriticalUniquenessContinuousDependencePackage {n : ℕ}
    (P : CriticalNLSProblem n) (M : MildDuhamelOperators n)
    (E : CriticalLocalEstimatePackage P M) where
  solutionClassWithinBall :
    ∀ u : SolutionField n,
      P.solutionClass u → E.gauges.solutionGauge u ≤ E.ballRadius
  solutionClassSatisfiesFixedPoint :
    ∀ u : SolutionField n,
      P.nlsEquation u →
        P.initialTrace u P.initialData →
          P.solutionClass u →
            u = mildDuhamelFixedPoint P M u
  fixedPointUniquenessInBall :
    ∀ u v : SolutionField n,
      u = mildDuhamelFixedPoint P M u →
        v = mildDuhamelFixedPoint P M v →
          E.gauges.solutionGauge u ≤ E.ballRadius →
            E.gauges.solutionGauge v ≤ E.ballRadius →
              u = v
  continuousDependenceAtInitialData : Prop
  continuousDependenceAtInitialData_holds : continuousDependenceAtInitialData

/-- Projection theorem for the C006 solution-class ball inclusion obligation. -/
theorem criticalUniqueness_solutionClassWithinBall {n : ℕ}
    {P : CriticalNLSProblem n} {M : MildDuhamelOperators n}
    {E : CriticalLocalEstimatePackage P M}
    (U : CriticalUniquenessContinuousDependencePackage P M E)
    (u : SolutionField n) (hu : P.solutionClass u) :
    E.gauges.solutionGauge u ≤ E.ballRadius :=
  U.solutionClassWithinBall u hu

/-- Projection theorem from the solution class to the Duhamel fixed-point equation. -/
theorem criticalUniqueness_solutionClassSatisfiesFixedPoint {n : ℕ}
    {P : CriticalNLSProblem n} {M : MildDuhamelOperators n}
    {E : CriticalLocalEstimatePackage P M}
    (U : CriticalUniquenessContinuousDependencePackage P M E)
    (u : SolutionField n) (hEq : P.nlsEquation u)
    (hTrace : P.initialTrace u P.initialData) (hClass : P.solutionClass u) :
    u = mildDuhamelFixedPoint P M u :=
  U.solutionClassSatisfiesFixedPoint u hEq hTrace hClass

/--
C006 assembly theorem: the package gives uniqueness in the critical solution
class once both compared solutions solve the normalized equation, have the
same initial trace, and belong to the solution class.
-/
theorem criticalUniqueness_unique_in_solutionClass {n : ℕ}
    {P : CriticalNLSProblem n} {M : MildDuhamelOperators n}
    {E : CriticalLocalEstimatePackage P M}
    (U : CriticalUniquenessContinuousDependencePackage P M E)
    (u v : SolutionField n)
    (huEq : P.nlsEquation u) (huTrace : P.initialTrace u P.initialData)
    (huClass : P.solutionClass u)
    (hvEq : P.nlsEquation v) (hvTrace : P.initialTrace v P.initialData)
    (hvClass : P.solutionClass v) :
    u = v :=
  U.fixedPointUniquenessInBall u v
    (U.solutionClassSatisfiesFixedPoint u huEq huTrace huClass)
    (U.solutionClassSatisfiesFixedPoint v hvEq hvTrace hvClass)
    (U.solutionClassWithinBall u huClass)
    (U.solutionClassWithinBall v hvClass)

/-- Projection theorem for the C006 continuous-dependence proposition. -/
theorem criticalUniqueness_continuousDependence {n : ℕ}
    {P : CriticalNLSProblem n} {M : MildDuhamelOperators n}
    {E : CriticalLocalEstimatePackage P M}
    (U : CriticalUniquenessContinuousDependencePackage P M E) :
    U.continuousDependenceAtInitialData :=
  U.continuousDependenceAtInitialData_holds

/--
Assemble the terminal conclusion object from an existence seed and a C006
uniqueness/continuous-dependence package.

This is a checked packaging theorem only.  It does not produce the existence
seed, Strichartz estimates, nonlinear estimates, or fixed-point uniqueness
package.
-/
def criticalNLSConclusion_of_existence_and_c006_package {n : ℕ}
    {P : CriticalNLSProblem n} {M : MildDuhamelOperators n}
    {E : CriticalLocalEstimatePackage P M}
    (S : CriticalExistenceSeed P)
    (U : CriticalUniquenessContinuousDependencePackage P M E) :
    CriticalNLSConclusion P where
  solution := S.solution
  solvesNLS := S.solvesNLS
  hasInitialTrace := S.hasInitialTrace
  solution_mem_class := S.solution_mem_class
  uniqueness := by
    intro v hvEq hvTrace hvClass
    exact criticalUniqueness_unique_in_solutionClass U v S.solution
      hvEq hvTrace hvClass S.solvesNLS S.hasInitialTrace S.solution_mem_class
  continuousDependenceAtInitialData := U.continuousDependenceAtInitialData
  continuousDependenceAtInitialData_holds :=
    U.continuousDependenceAtInitialData_holds

/-- M0387-level leaves for the C006 uniqueness/dependence package. -/
inductive CriticalUniquenessDependenceLeaf : Type where
  | criticalMetricClosure
  | solutionClassBallEmbedding
  | equationToFixedPoint
  | fixedPointUniqueness
  | uniquenessInClassAssembly
  | solutionMapModel
  | dataPerturbationEstimate
  | continuousDependenceAssembly
  | conclusionPackaging
  deriving DecidableEq, Repr

/-- Stable public id for each C006 uniqueness/dependence leaf. -/
def CriticalUniquenessDependenceLeaf.stableId :
    CriticalUniquenessDependenceLeaf → String
  | .criticalMetricClosure => "S1-M-153-C006-L01.critical_metric_closure"
  | .solutionClassBallEmbedding => "S1-M-153-C006-L02.solution_class_ball_embedding"
  | .equationToFixedPoint => "S1-M-153-C006-L03.equation_to_fixed_point"
  | .fixedPointUniqueness => "S1-M-153-C006-L04.fixed_point_uniqueness"
  | .uniquenessInClassAssembly => "S1-M-153-C006-L05.uniqueness_in_class_assembly"
  | .solutionMapModel => "S1-M-153-C006-L06.solution_map_model"
  | .dataPerturbationEstimate => "S1-M-153-C006-L07.data_perturbation_estimate"
  | .continuousDependenceAssembly =>
      "S1-M-153-C006-L08.continuous_dependence_assembly"
  | .conclusionPackaging => "S1-M-153-C006-L09.conclusion_packaging"

/-- Local proof-step budget for each C006 uniqueness/dependence leaf. -/
def CriticalUniquenessDependenceLeaf.proofStepBudget :
    CriticalUniquenessDependenceLeaf → Nat
  | .criticalMetricClosure => 70
  | .solutionClassBallEmbedding => 65
  | .equationToFixedPoint => 85
  | .fixedPointUniqueness => 95
  | .uniquenessInClassAssembly => 60
  | .solutionMapModel => 70
  | .dataPerturbationEstimate => 95
  | .continuousDependenceAssembly => 85
  | .conclusionPackaging => 55

/-- Child C006 keeps every proposed uniqueness/dependence leaf at budget `<= 100`. -/
theorem criticalUniquenessDependenceLeaf_budget_le_100
    (leaf : CriticalUniquenessDependenceLeaf) :
    leaf.proofStepBudget ≤ 100 := by
  cases leaf <;> decide

/-- Ordered theorem-tree leaves for the C006 uniqueness/dependence package. -/
def criticalUniquenessDependenceLeaves :
    List CriticalUniquenessDependenceLeaf := [
  .criticalMetricClosure,
  .solutionClassBallEmbedding,
  .equationToFixedPoint,
  .fixedPointUniqueness,
  .uniquenessInClassAssembly,
  .solutionMapModel,
  .dataPerturbationEstimate,
  .continuousDependenceAssembly,
  .conclusionPackaging
]

/-- The C006 uniqueness/dependence package has nine budgeted leaves. -/
theorem criticalUniquenessDependenceLeaves_length :
    criticalUniquenessDependenceLeaves.length = 9 :=
  rfl

/-- Repo-local theorem-tree package metadata for child C006. -/
structure CriticalUniquenessDependenceTheoremTree where
  root : String
  leaves : List CriticalUniquenessDependenceLeaf
  allLeavesBudgeted :
    ∀ leaf ∈ leaves, leaf.proofStepBudget ≤ 100
  completionStatus : String

/--
The C006 theorem-tree metadata is checked as an interface and budget split only.
The fixed-point uniqueness and solution-map continuity leaves remain blocked
until the C002/C005 Strichartz and nonlinear-estimate packages are available.
-/
def c006CriticalUniquenessDependenceTheoremTree :
    CriticalUniquenessDependenceTheoremTree where
  root := "uniqueness and continuous dependence for the critical NLS solution map"
  leaves := criticalUniquenessDependenceLeaves
  allLeavesBudgeted := by
    intro leaf _hleaf
    exact criticalUniquenessDependenceLeaf_budget_le_100 leaf
  completionStatus :=
    "blocked_formalization_debt_waiting_on_c002_c005_no_terminal_uniqueness_claim"

/-- The C006 theorem-tree metadata records nine leaves. -/
theorem c006CriticalUniquenessDependenceTheoremTree_leaf_count :
    c006CriticalUniquenessDependenceTheoremTree.leaves.length = 9 :=
  rfl

/-- C006 does not claim completed uniqueness or continuous dependence. -/
theorem c006CriticalUniquenessDependenceTheoremTree_status :
    c006CriticalUniquenessDependenceTheoremTree.completionStatus =
      "blocked_formalization_debt_waiting_on_c002_c005_no_terminal_uniqueness_claim" :=
  rfl

/--
Stage1 statement-shape candidate for the Cazenave-Weissler critical NLS
regularity theorem.

For each normalized NLS problem satisfying the audited Strichartz, scaling, and
fixed-point hypotheses, the expected conclusion is a local critical-class
solution package.  Future work must replace the abstract predicate fields by a
concrete Lean 4 PDE/Strichartz/Sobolev API or by a pinned external dependency.
-/
def StatementShape : Prop :=
  ∀ (n : ℕ) (P : CriticalNLSProblem n),
    P.strichartzAdmissiblePackage →
      P.scalingCriticalRelation →
        P.contractionMappingHypotheses →
          Nonempty (CriticalNLSConclusion P)

/-- The statement-shape definition unfolds to the normalized problem/conclusion form. -/
theorem statementShape_iff :
    StatementShape ↔
      ∀ (n : ℕ) (P : CriticalNLSProblem n),
        P.strichartzAdmissiblePackage →
          P.scalingCriticalRelation →
            P.contractionMappingHypotheses →
              Nonempty (CriticalNLSConclusion P) :=
  Iff.rfl

/-- A conclusion package exposes the solution's critical-class membership. -/
theorem solution_mem_class_of_conclusion
    {n : ℕ} {P : CriticalNLSProblem n} (C : CriticalNLSConclusion P) :
    P.solutionClass C.solution :=
  C.solution_mem_class

/-- Scalar distributions on an open spatial domain, using mathlib's current distribution object. -/
abbrev ScalarDistributionOn {n : ℕ} (Ω : TopologicalSpace.Opens (Space n)) : Type :=
  Distribution Ω ℂ ⊤

/-- Checked distribution API: continuous linear maps act on scalar distributions by postcomposition. -/
def distributionMapCLM {n : ℕ} (Ω : TopologicalSpace.Opens (Space n))
    (A : ℂ →L[ℝ] ℂ) :
    ScalarDistributionOn Ω →L[ℝ] ScalarDistributionOn Ω :=
  Distribution.mapCLM A

/-- Checked mathlib anchor: Plancherel for `L^2` functions on the spatial model. -/
theorem l2_fourier_norm_eq (n : ℕ) (f : Lp (α := Space n) ℂ 2) :
    ‖𝓕 f‖ = ‖f‖ :=
  MeasureTheory.Lp.norm_fourier_eq f

/-- Checked mathlib anchor: the Laplacian of a constant complex field is zero. -/
theorem laplacian_const_complex (n : ℕ) (c : ℂ) :
    Laplacian.laplacian (fun _ : Space n => c) = 0 :=
  InnerProductSpace.laplacian_const

/--
Checked wrapper for mathlib's first-order Sobolev inequality.

This is useful analytic infrastructure for a future NLS proof package, but it
is not a Strichartz estimate or a Cazenave-Weissler well-posedness theorem.
-/
theorem sobolev_eLpNorm_le_fderiv_one_mathlib_wrapper
    (n : ℕ) (μ : Measure (Space n)) [μ.IsAddHaarMeasure]
    {u : Space n → ℂ} (hu : ContDiff ℝ 1 u) (hcu : HasCompactSupport u)
    {p : ℝ≥0}
    (hp : NNReal.HolderConjugate (Module.finrank ℝ (Space n)) p) :
    eLpNorm u (↑p) μ ≤
      ↑(eLpNormLESNormFDerivOneConst μ p) * eLpNorm (fderiv ℝ u) 1 μ :=
  MeasureTheory.eLpNorm_le_eLpNorm_fderiv_one μ hu hcu hp

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Fourier.LpSpace",
  "Mathlib.Analysis.Fourier.FourierTransform",
  "Mathlib.Analysis.Distribution.Distribution",
  "Mathlib.Analysis.Distribution.TemperedDistribution",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "Mathlib.Analysis.InnerProductSpace.Laplacian",
  "Mathlib.MeasureTheory.Function.LpSpace.Basic",
  "Mathlib.MeasureTheory.Function.LpSeminorm.Basic",
  "Mathlib.MeasureTheory.Measure.Lebesgue.Basic"
]

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.MemLp",
  "MeasureTheory.eLpNorm",
  "MeasureTheory.Lp",
  "MeasureTheory.Lp.fourierTransformₗᵢ",
  "MeasureTheory.Lp.norm_fourier_eq",
  "Distribution",
  "Distribution.mapCLM",
  "Laplacian.laplacian",
  "InnerProductSpace.laplacian_const",
  "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_one"
]

/-- Search terms that did not locate a terminal Cazenave-Weissler theorem in local mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Cazenave",
  "Weissler",
  "Cazenave-Weissler",
  "nonlinear Schrodinger",
  "nonlinear Schrödinger",
  "NLS",
  "Strichartz",
  "critical regularity",
  "critical Sobolev",
  "local well-posedness"
]

/-- Child C002 primary-source surfaces audited for Strichartz/NLS anchors. -/
def c002PrimarySourceSurfaces : List String := [
  "pinned mathlib4 dependency: leanprover-community/mathlib4 at 8a178386ffc0f5fef0b77738bb5449d50efeea95",
  "local mathlib tree: Formalizations/Lean/.lake/packages/mathlib/Mathlib",
  "local dependency trees: flt-regular, batteries, aesop, LeanSearchClient",
  "GitHub repository search: \"Strichartz\" Lean",
  "GitHub repository search: \"nonlinear Schrodinger\" Lean",
  "GitHub repository search: \"Cazenave\" \"Weissler\" Lean",
  "web search for primary Lean 4/GitHub anchors matching Strichartz, Cazenave-Weissler, and nonlinear Schrödinger"
]

/--
Theorem families still missing after the C002 Strichartz audit.

This is deliberately metadata, not a theorem-completion claim.  No external
Lean 4 Strichartz or Cazenave-Weissler proof was found and no anchor-only
evidence is counted as repo-local closure.
-/
def c002MissingStrichartzTheoremFamilies : List String := [
  "Strichartz admissible exponent-pair definitions for the Schrodinger propagator",
  "homogeneous linear Schrodinger Strichartz estimates",
  "inhomogeneous/Duhamel Strichartz estimates",
  "nonlinear estimates in the critical Cazenave-Weissler solution space",
  "critical NLS local well-posedness via contraction mapping"
]

/-- C002 machine-debt classification for the missing Strichartz theorem family. -/
def c002MachineDebtClassification : String :=
  "formalization_debt"

/--
C002 repo-local integration-debt gate.

The gate is passed only as a non-completion audit result: no external Lean 4
closure was found, no pinned/imported external theorem is available, and the
terminal Cazenave-Weissler theorem is not claimed complete.
-/
def c002RepoLocalIntegrationDebtGate : String :=
  "passed_noncompletion_no_external_lean4_strichartz_closure_found"

/-- The C002 audit currently records five missing theorem-family branches. -/
theorem c002MissingStrichartzTheoremFamilies_length :
    c002MissingStrichartzTheoremFamilies.length = 5 :=
  rfl

/-- The C002 debt classification is explicitly formalization debt. -/
theorem c002MachineDebtClassification_eq :
    c002MachineDebtClassification = "formalization_debt" :=
  rfl

/-! ## Public Stage1 backfill metadata -/

/--
Public surfaces that must be updated by a serial integrator.

This child records the integration target set only.  Parallel workers must not
edit these shared documents directly.
-/
def c007PublicBackfillTargets : List String := [
  "Docs/Stage1_Blueprint.md",
  "Docs/todos_20260430.md",
  "README.md"
]

/-- Checked repo-local statement-shape names ready for public backfill. -/
def c007CheckedStatementShapeSurface : List String := [
  "StatementShape",
  "statementShape_iff",
  "CriticalNLSProblem",
  "CriticalNLSConclusion",
  "InhomogeneousCriticalSobolev",
  "CriticalSobolevData",
  "ClassicalNLS",
  "MildDuhamelNLS",
  "mildDuhamelEquationForProblem"
]

/-- Checked repo-local audit/status names ready for public backfill. -/
def c007CheckedAuditStatusSurface : List String := [
  "mathlibAnchorModules",
  "mathlibAnchorNames",
  "absentTerminalSearchTerms",
  "c002PrimarySourceSurfaces",
  "c002MissingStrichartzTheoremFamilies",
  "c002MachineDebtClassification",
  "c002RepoLocalIntegrationDebtGate",
  "c004FormulationBridgeTheoremTree",
  "c005CriticalLocalEstimateTheoremTree",
  "c006CriticalUniquenessDependenceTheoremTree"
]

/--
Child C007 non-completion gate.

The checked statement-shape and audit metadata are ready for serial public
backfill, but the terminal Cazenave-Weissler theorem remains open
formalization debt.
-/
structure PublicStage1BackfillGate where
  publicDocsRequireSerialIntegrator : Bool
  theoremCompletionClaim : Bool
  repoLocalIntegrationDebt : Bool
  machineDebtClassification : String
  requiredValidationCommand : String

/-- C007 gate value for public backfill without theorem completion. -/
def c007PublicStage1BackfillGate : PublicStage1BackfillGate where
  publicDocsRequireSerialIntegrator := true
  theoremCompletionClaim := false
  repoLocalIntegrationDebt := false
  machineDebtClassification := "formalization_debt"
  requiredValidationCommand :=
    "cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_153.lean"

/-- The C007 public backfill target set has three shared surfaces. -/
theorem c007PublicBackfillTargets_length :
    c007PublicBackfillTargets.length = 3 :=
  rfl

/-- C007 explicitly does not claim terminal theorem completion. -/
theorem c007PublicStage1BackfillGate_no_completion :
    c007PublicStage1BackfillGate.theoremCompletionClaim = false :=
  rfl

/-- C007 records formalization debt, not repo-local integration debt. -/
theorem c007PublicStage1BackfillGate_debt :
    c007PublicStage1BackfillGate.machineDebtClassification = "formalization_debt" ∧
      c007PublicStage1BackfillGate.repoLocalIntegrationDebt = false :=
  ⟨rfl, rfl⟩

end S1_M_153
end Stage1
end AwesomeTheorems
