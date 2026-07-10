import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.MeasureTheory.Integral.IntervalIntegral.IntegrationByParts
import Mathlib.MeasureTheory.Function.AEEqOfIntegral
import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.Calculus.FDeriv.Basic
import Mathlib.Analysis.Calculus.LocalExtr.Basic

/-!
# S1-M-187 / THM-M-1518: Principle of least action

This Stage1 artifact records a conservative Lean 4 statement boundary for the
principle of least action / stationary action.

The physical phrase "a physical system follows a path of least action" is
normalized here as a calculus-of-variations statement over a real normed
configuration space: a Lagrangian `L(q, v)`, an action integral on a finite time
interval, fixed-endpoint variations, a first-variation predicate, and an
Euler-Lagrange predicate.  The pinned mathlib snapshot supplies the interval
integral and derivative infrastructure, but this audit did not locate a
terminal least-action or Euler-Lagrange theorem.  The declarations below are
therefore statement-shape and checked wrapper artifacts only.
-/

noncomputable section

open Filter Set MeasureTheory
open scoped Topology

set_option linter.unusedSectionVars false

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_187

universe u

/-- Curves in a configuration space, parametrized by real time. -/
abbrev Curve (E : Type u) := ℝ → E

variable {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]

/-- The velocity curve associated to a time-parametrized curve. -/
def Velocity (q : Curve E) : Curve E :=
  fun t => deriv q t

/--
Partial derivative of a Lagrangian with respect to the position coordinate,
viewed as a continuous linear functional on the configuration space.
-/
def PositionDerivative (L : E × E → ℝ) (x v : E) : E →L[ℝ] ℝ :=
  (fderiv ℝ L (x, v)).comp (ContinuousLinearMap.inl ℝ E E)

/--
Partial derivative of a Lagrangian with respect to the velocity coordinate,
viewed as a continuous linear functional on the configuration space.
-/
def VelocityDerivative (L : E × E → ℝ) (x v : E) : E →L[ℝ] ℝ :=
  (fderiv ℝ L (x, v)).comp (ContinuousLinearMap.inr ℝ E E)

/-- Boundary data for a fixed-endpoint variational problem. -/
structure BoundaryData (E : Type u) where
  t₀ : ℝ
  t₁ : ℝ
  q₀ : E
  q₁ : E
  time_order : t₀ < t₁

/-- The action integral associated to a Lagrangian and a curve. -/
def Action (L : E × E → ℝ) (B : BoundaryData E) (q : Curve E) : ℝ :=
  ∫ t in B.t₀..B.t₁, L (q t, Velocity q t)

/-- The pointwise integrand of the action functional. -/
def ActionIntegrand (L : E × E → ℝ) (q : Curve E) : ℝ → ℝ :=
  fun t => L (q t, Velocity q t)

/-- A curve satisfies the fixed endpoint conditions in the variational problem. -/
def FixedEndpoints (B : BoundaryData E) (q : Curve E) : Prop :=
  q B.t₀ = B.q₀ ∧ q B.t₁ = B.q₁

/-- A variation vanishes at both fixed endpoints. -/
def VariationVanishesAtEndpoints (B : BoundaryData E) (η : Curve E) : Prop :=
  η B.t₀ = 0 ∧ η B.t₁ = 0

/-- Exact Stage1 admissible curve class selected before proof work starts. -/
def AdmissibleCurve (B : BoundaryData E) (q : Curve E) : Prop :=
  ContDiff ℝ 2 q ∧ FixedEndpoints B q

/-- Exact Stage1 admissible variation class selected before proof work starts. -/
def AdmissibleVariation (B : BoundaryData E) (η : Curve E) : Prop :=
  ContDiff ℝ 1 η ∧ VariationVanishesAtEndpoints B η

/-- The one-parameter variation `q + ε η`. -/
def VariedCurve (q η : Curve E) (ε : ℝ) : Curve E :=
  fun t => q t + ε • η t

/-- The first variation of the action in the direction `η`. -/
def FirstVariation (L : E × E → ℝ) (B : BoundaryData E) (q η : Curve E) : ℝ :=
  deriv (fun ε : ℝ => Action L B (VariedCurve q η ε)) 0

/--
The formal first-variation density expected after differentiating the action
integral under the variation parameter.
-/
def FirstVariationDensity (L : E × E → ℝ) (q η : Curve E) : ℝ → ℝ :=
  fun t =>
    PositionDerivative L (q t) (Velocity q t) (η t) +
      VelocityDerivative L (q t) (Velocity q t) (Velocity η t)

/--
Repo-local predicate isolating the differentiation-under-the-integral leaf.

This is deliberately a hypothesis package, not a terminal proof: future work
must discharge it from regularity and dominated-convergence hypotheses.
-/
def DifferentiatesUnderActionIntegral
    (L : E × E → ℝ) (B : BoundaryData E) (q η : Curve E) : Prop :=
  HasDerivAt
    (fun ε : ℝ => Action L B (VariedCurve q η ε))
    (∫ t in B.t₀..B.t₁, FirstVariationDensity L q η t)
    0

/-- Pairing between a time-dependent velocity derivative and a variation velocity. -/
def VelocityPairingIntegrand (P : ℝ → E →L[ℝ] ℝ) (η : Curve E) : ℝ → ℝ :=
  fun t => P t (Velocity η t)

/-- Pairing between a time-dependent derivative term and a variation. -/
def VariationPairingIntegrand (P' : ℝ → E →L[ℝ] ℝ) (η : Curve E) : ℝ → ℝ :=
  fun t => P' t (η t)

/--
Repo-local statement package for the vector/dual integration-by-parts leaf.

Mathlib supplies scalar and scalar-vector interval integration by parts.  The
dual-pairing version needed for Euler-Lagrange remains isolated here as a
concrete bridge target.
-/
def VelocityPairingIntegrationByParts
    (B : BoundaryData E) (P P' : ℝ → E →L[ℝ] ℝ) (η : Curve E) : Prop :=
  (∫ t in B.t₀..B.t₁, VelocityPairingIntegrand P η t) =
    P B.t₁ (η B.t₁) - P B.t₀ (η B.t₀) -
      ∫ t in B.t₀..B.t₁, VariationPairingIntegrand P' η t

/--
Euler-Lagrange residual after the integration-by-parts step.

The residual is zero exactly when the derivative of the velocity partial
derivative agrees with the position partial derivative.
-/
def EulerLagrangeResidual (L : E × E → ℝ) (q : Curve E) :
    ℝ → E →L[ℝ] ℝ :=
  fun t =>
    PositionDerivative L (q t) (Velocity q t) -
      deriv (fun τ : ℝ => VelocityDerivative L (q τ) (Velocity q τ)) t

/-- Pairing between an Euler-Lagrange residual and an admissible variation. -/
def ResidualPairingIntegrand (R : ℝ → E →L[ℝ] ℝ) (η : Curve E) : ℝ → ℝ :=
  fun t => R t (η t)

/--
Selected smooth-variation form of the fundamental lemma of the calculus of
variations for this Stage1 slot.

This is intentionally a bridge target.  Mathlib's current local dependency
provides measure-theoretic almost-everywhere integral-determination lemmas,
but not the full smooth compactly supported variation-to-pointwise residual
lemma needed by the Euler-Lagrange proof.
-/
def FundamentalLemmaForVariations
    (B : BoundaryData E) (R : ℝ → E →L[ℝ] ℝ) : Prop :=
  (∀ η : Curve E,
      AdmissibleVariation B η →
        (∫ t in B.t₀..B.t₁, ResidualPairingIntegrand R η t) = 0) →
    ∀ t ∈ Ioo B.t₀ B.t₁, R t = 0

/-- Measure used for the open-time-interval version of the fundamental lemma. -/
def InteriorTimeMeasure (B : BoundaryData E) : Measure ℝ :=
  volume.restrict (Ioo B.t₀ B.t₁)

/--
Set-integral hypothesis used by the checked measure-theoretic fundamental
lemma wrapper.
-/
def SetIntegralZeroOnInterior {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F]
    (B : BoundaryData E) (r : ℝ → F) : Prop :=
  ∀ s : Set ℝ,
    MeasurableSet s →
      InteriorTimeMeasure B s < ⊤ →
        (∫ t in s, r t ∂(InteriorTimeMeasure B)) = 0

/-- Almost-everywhere conclusion for the selected measure-theoretic bridge. -/
def FundamentalLemmaAEConclusion {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F]
    (B : BoundaryData E) (r : ℝ → F) : Prop :=
  r =ᵐ[InteriorTimeMeasure B] 0

/--
Stationarity of the action under smooth fixed-endpoint variations.

This is the conservative Stage1 reading of the "least action" phrase: the
formal target is stationarity under admissible variations, not an unqualified
global minimum over all physically meaningful paths.
-/
def StationaryAction (L : E × E → ℝ) (B : BoundaryData E) (q : Curve E) : Prop :=
  ∀ η : Curve E,
    ContDiff ℝ 1 η →
      VariationVanishesAtEndpoints B η →
        FirstVariation L B q η = 0

/--
Local least-action predicate on the fixed-endpoint class.

This records the literal minimization reading separately from the stationary
Euler-Lagrange reading.  It is not used as a completed theorem in this file.
-/
def LocallyMinimizesAction
    (L : E × E → ℝ) (B : BoundaryData E) (q : Curve E) (hq : FixedEndpoints B q) : Prop :=
  IsLocalMin
    (fun r : {r : Curve E // FixedEndpoints B r} => Action L B r.1)
    ⟨q, hq⟩

/--
Euler-Lagrange equation in weak statement-shape form.

At each interior time, the derivative of the velocity partial derivative along
the curve equals the position partial derivative.
-/
def EulerLagrangeEquation (L : E × E → ℝ) (B : BoundaryData E) (q : Curve E) : Prop :=
  ∀ t ∈ Ioo B.t₀ B.t₁,
    HasDerivAt (fun τ : ℝ => VelocityDerivative L (q τ) (Velocity q τ))
      (PositionDerivative L (q t) (Velocity q t)) t

/--
The selected public theorem target for this Stage1 slot.

The primary target is stationary action.  The literal local-minimum reading is
kept as `LocallyMinimizesAction` for a later Fermat-style bridge, but is not the
terminal target claimed by the normalized statement shape.
-/
def SelectedPublicTarget (L : E × E → ℝ) (B : BoundaryData E) (q : Curve E) : Prop :=
  StationaryAction L B q

/-- Exact regularity and boundary hypotheses for the selected stationary target. -/
structure StationaryTargetHypotheses (L : E × E → ℝ) (B : BoundaryData E) (q : Curve E) :
    Prop where
  lagrangian_contDiff_two : ContDiff ℝ 2 L
  curve_admissible : AdmissibleCurve B q
  euler_lagrange : EulerLagrangeEquation L B q

/--
Normalized Stage1 statement shape for the stationary-action theorem.

For a twice differentiable Lagrangian and twice differentiable fixed-endpoint
curve, the Euler-Lagrange equation should imply vanishing first variation.
This file states the target shape; it does not provide a terminal proof.
-/
def StatementShape : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (L : E × E → ℝ) (B : BoundaryData E) (q : Curve E),
      ContDiff ℝ 2 L →
        ContDiff ℝ 2 q →
          FixedEndpoints B q →
            EulerLagrangeEquation L B q →
              StationaryAction L B q

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
      (L : E × E → ℝ) (B : BoundaryData E) (q : Curve E),
        ContDiff ℝ 2 L →
          ContDiff ℝ 2 q →
            FixedEndpoints B q →
              EulerLagrangeEquation L B q →
                StationaryAction L B q) :
    StatementShape.{u} :=
  h

/-- Extract the left fixed-endpoint equality. -/
theorem fixedEndpoint_left
    {B : BoundaryData E} {q : Curve E} (h : FixedEndpoints B q) :
    q B.t₀ = B.q₀ :=
  h.1

/-- Extract the right fixed-endpoint equality. -/
theorem fixedEndpoint_right
    {B : BoundaryData E} {q : Curve E} (h : FixedEndpoints B q) :
    q B.t₁ = B.q₁ :=
  h.2

/-- Extract the left vanishing condition for an endpoint-fixed variation. -/
theorem variation_left_zero
    {B : BoundaryData E} {η : Curve E} (h : VariationVanishesAtEndpoints B η) :
    η B.t₀ = 0 :=
  h.1

/-- Extract the right vanishing condition for an endpoint-fixed variation. -/
theorem variation_right_zero
    {B : BoundaryData E} {η : Curve E} (h : VariationVanishesAtEndpoints B η) :
    η B.t₁ = 0 :=
  h.2

/-- Extract smoothness from the selected admissible-curve class. -/
theorem admissibleCurve_contDiff
    {B : BoundaryData E} {q : Curve E} (h : AdmissibleCurve B q) :
    ContDiff ℝ 2 q :=
  h.1

/-- Extract endpoint constraints from the selected admissible-curve class. -/
theorem admissibleCurve_fixedEndpoints
    {B : BoundaryData E} {q : Curve E} (h : AdmissibleCurve B q) :
    FixedEndpoints B q :=
  h.2

/-- Extract smoothness from the selected admissible-variation class. -/
theorem admissibleVariation_contDiff
    {B : BoundaryData E} {η : Curve E} (h : AdmissibleVariation B η) :
    ContDiff ℝ 1 η :=
  h.1

/-- Extract endpoint vanishing from the selected admissible-variation class. -/
theorem admissibleVariation_vanishes
    {B : BoundaryData E} {η : Curve E} (h : AdmissibleVariation B η) :
    VariationVanishesAtEndpoints B η :=
  h.2

/-- The zero variation is endpoint-fixed. -/
theorem zero_variation_vanishes (B : BoundaryData E) :
    VariationVanishesAtEndpoints B (fun _ : ℝ => (0 : E)) :=
  ⟨rfl, rfl⟩

/-- At variation parameter zero, `q + ε η` is the original curve. -/
theorem variedCurve_zero (q η : Curve E) :
    VariedCurve q η 0 = q := by
  funext t
  simp [VariedCurve]

/-- Checked wrapper exposing the position partial derivative definition. -/
theorem positionDerivative_eq (L : E × E → ℝ) (x v : E) :
    PositionDerivative L x v =
      (fderiv ℝ L (x, v)).comp (ContinuousLinearMap.inl ℝ E E) :=
  rfl

/-- Checked wrapper exposing the velocity partial derivative definition. -/
theorem velocityDerivative_eq (L : E × E → ℝ) (x v : E) :
    VelocityDerivative L x v =
      (fderiv ℝ L (x, v)).comp (ContinuousLinearMap.inr ℝ E E) :=
  rfl

/-- The selected public target is definitionally the stationary-action target. -/
theorem selectedPublicTarget_eq_stationaryAction
    (L : E × E → ℝ) (B : BoundaryData E) (q : Curve E) :
    SelectedPublicTarget L B q = StationaryAction L B q :=
  rfl

/-- The action is definitionally the interval integral of `ActionIntegrand`. -/
theorem action_eq_integral_actionIntegrand
    (L : E × E → ℝ) (B : BoundaryData E) (q : Curve E) :
    Action L B q = ∫ t in B.t₀..B.t₁, ActionIntegrand L q t :=
  rfl

/--
Continuity on the closed time interval is enough for action-integrand
interval integrability.
-/
theorem actionIntegrand_intervalIntegrable_of_continuousOn
    {L : E × E → ℝ} {B : BoundaryData E} {q : Curve E}
    (h : ContinuousOn (ActionIntegrand L q) (uIcc B.t₀ B.t₁)) :
    IntervalIntegrable (ActionIntegrand L q) volume B.t₀ B.t₁ :=
  h.intervalIntegrable

/-- Extract the first-variation integral identity from the D-U-I hypothesis. -/
theorem firstVariation_eq_integral_of_differentiatesUnderActionIntegral
    {L : E × E → ℝ} {B : BoundaryData E} {q η : Curve E}
    (h : DifferentiatesUnderActionIntegral L B q η) :
    FirstVariation L B q η =
      ∫ t in B.t₀..B.t₁, FirstVariationDensity L q η t := by
  simpa [FirstVariation, DifferentiatesUnderActionIntegral] using h.deriv

/--
Endpoint-fixed variations remove the boundary terms from the dual-pairing
integration-by-parts statement.
-/
theorem velocityPairing_integral_eq_neg_integral_of_vanishing_endpoints
    {B : BoundaryData E} {P P' : ℝ → E →L[ℝ] ℝ} {η : Curve E}
    (hibp : VelocityPairingIntegrationByParts B P P' η)
    (hη : VariationVanishesAtEndpoints B η) :
    (∫ t in B.t₀..B.t₁, VelocityPairingIntegrand P η t) =
      -∫ t in B.t₀..B.t₁, VariationPairingIntegrand P' η t := by
  rw [hibp, hη.2, hη.1]
  simp

/--
Checked mathlib wrapper for the measure-theoretic fundamental lemma used as
the safe repo-local anchor for the calculus-of-variations fundamental lemma.
-/
theorem measureTheory_ae_eq_zero_of_forall_setIntegral_eq_zero
    {α F : Type*} [MeasurableSpace α] {μ : Measure α}
    [NormedAddCommGroup F] [NormedSpace ℝ F] [CompleteSpace F]
    {f : α → F} (hf : Integrable f μ)
    (hzero : ∀ s : Set α,
      MeasurableSet s → μ s < ⊤ → (∫ x in s, f x ∂μ) = 0) :
    f =ᵐ[μ] 0 :=
  hf.ae_eq_zero_of_forall_setIntegral_eq_zero hzero

/--
Open-interval specialization of the checked measure-theoretic fundamental
lemma anchor.
-/
theorem fundamentalLemmaAE_of_integrable_setIntegral_zero
    {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F] [CompleteSpace F]
    {B : BoundaryData E} {r : ℝ → F}
    (hint : Integrable r (InteriorTimeMeasure B))
    (hzero : SetIntegralZeroOnInterior B r) :
    FundamentalLemmaAEConclusion B r :=
  measureTheory_ae_eq_zero_of_forall_setIntegral_eq_zero hint hzero

/--
Use the selected smooth-variation fundamental lemma bridge once a future proof
or pinned dependency supplies it.
-/
theorem residual_eq_zero_of_fundamentalLemmaForVariations
    {B : BoundaryData E} {R : ℝ → E →L[ℝ] ℝ}
    (hFL : FundamentalLemmaForVariations B R)
    (hweak : ∀ η : Curve E,
      AdmissibleVariation B η →
        (∫ t in B.t₀..B.t₁, ResidualPairingIntegrand R η t) = 0) :
    ∀ t ∈ Ioo B.t₀ B.t₁, R t = 0 :=
  hFL hweak

/-- Pack the exact hypotheses used by the normalized stationary target. -/
theorem stationaryTargetHypotheses_intro
    {L : E × E → ℝ} {B : BoundaryData E} {q : Curve E}
    (hL : ContDiff ℝ 2 L) (hq : ContDiff ℝ 2 q) (hfix : FixedEndpoints B q)
    (hEL : EulerLagrangeEquation L B q) :
    StationaryTargetHypotheses L B q :=
  ⟨hL, ⟨hq, hfix⟩, hEL⟩

/-- Unpack the exact hypotheses used by the normalized stationary target. -/
theorem stationaryTargetHypotheses_elim
    {L : E × E → ℝ} {B : BoundaryData E} {q : Curve E}
    (h : StationaryTargetHypotheses L B q) :
    ContDiff ℝ 2 L ∧ ContDiff ℝ 2 q ∧ FixedEndpoints B q ∧
      EulerLagrangeEquation L B q :=
  ⟨h.lagrangian_contDiff_two, h.curve_admissible.1, h.curve_admissible.2,
    h.euler_lagrange⟩

/-- Checked mathlib anchor: Fermat's theorem for a local minimum. -/
theorem localMin_fderiv_eq_zero
    {X : Type u} [NormedAddCommGroup X] [NormedSpace ℝ X]
    {A : X → ℝ} {x : X} (h : IsLocalMin A x) :
    fderiv ℝ A x = 0 :=
  h.fderiv_eq_zero

/-- Checked mathlib anchor: Fermat's theorem for a local extremum. -/
theorem localExtr_fderiv_eq_zero
    {X : Type u} [NormedAddCommGroup X] [NormedSpace ℝ X]
    {A : X → ℝ} {x : X} (h : IsLocalExtr A x) :
    fderiv ℝ A x = 0 :=
  h.fderiv_eq_zero

/-- Checked interval-integral anchor used by the action functional. -/
theorem action_integral_const
    (B : BoundaryData E) [CompleteSpace E] (c : ℝ) :
    (∫ _t in B.t₀..B.t₁, c) = (B.t₁ - B.t₀) • c :=
  intervalIntegral.integral_const c

/--
Checked anchor for the interval-integral fundamental theorem of calculus.

This wrapper is intentionally no stronger than the pinned mathlib theorem; it
records the exact API surface needed before a future first-variation proof can
replace formalization debt with a local proof body.
-/
theorem intervalIntegral_integral_eq_sub_of_hasDerivAt
    [CompleteSpace E] {a b : ℝ} {f f' : ℝ → E}
    (hderiv : ∀ x ∈ uIcc a b, HasDerivAt f (f' x) x)
    (hint : IntervalIntegrable f' volume a b) :
    (∫ y in a..b, f' y) = f b - f a :=
  intervalIntegral.integral_eq_sub_of_hasDerivAt hderiv hint

/-- Checked anchor for the derivative-form fundamental theorem of calculus. -/
theorem intervalIntegral_integral_deriv_eq_sub
    [CompleteSpace E] {a b : ℝ} {f : ℝ → E}
    (hderiv : ∀ x ∈ uIcc a b, DifferentiableAt ℝ f x)
    (hint : IntervalIntegrable (deriv f) volume a b) :
    (∫ y in a..b, deriv f y) = f b - f a :=
  intervalIntegral.integral_deriv_eq_sub hderiv hint

/--
Checked anchor for scalar-valued interval integration by parts.

The calculus-of-variations bridge will need a vector-valued version for pairing
the velocity derivative with a variation; this scalar theorem is the basic
mathlib endpoint identity.
-/
theorem intervalIntegral_integral_mul_deriv_eq_deriv_mul
    {a b : ℝ} {u v u' v' : ℝ → ℝ}
    (hu : ∀ x ∈ uIcc a b, HasDerivAt u (u' x) x)
    (hv : ∀ x ∈ uIcc a b, HasDerivAt v (v' x) x)
    (hu' : IntervalIntegrable u' volume a b)
    (hv' : IntervalIntegrable v' volume a b) :
    (∫ x in a..b, u x * v' x) =
      u b * v b - u a * v a - ∫ x in a..b, u' x * v x :=
  intervalIntegral.integral_mul_deriv_eq_deriv_mul hu hv hu' hv'

/-- Checked anchor for vector-valued scalar integration by parts. -/
theorem intervalIntegral_integral_smul_deriv_eq_deriv_smul
    [CompleteSpace E] {a b : ℝ} {u u' : ℝ → ℝ} {v v' : ℝ → E}
    (hu : ∀ x ∈ uIcc a b, HasDerivAt u (u' x) x)
    (hv : ∀ x ∈ uIcc a b, HasDerivAt v (v' x) x)
    (hu' : IntervalIntegrable u' volume a b)
    (hv' : IntervalIntegrable v' volume a b) :
    (∫ x in a..b, u x • v' x) =
      u b • v b - u a • v a - ∫ x in a..b, u' x • v x :=
  intervalIntegral.integral_smul_deriv_eq_deriv_smul hu hv hu' hv'

/-- Pinned mathlib revision used for this Stage1 anchor audit. -/
def mathlibAnchorRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- One row in the repo-local mathlib anchor audit table. -/
structure MathlibAnchor where
  moduleName : String
  checkedNames : List String
  role : String
  status : String
deriving Repr

/-- Machine-readable status row for the requested S187-L020 through S187-L023 backfill. -/
structure FirstVariationLeafBackfill where
  leafId : String
  target : String
  checkedDeclarations : List String
  status : String
  remainingGate : String
deriving Repr

/-- Machine-readable status row for the requested S187-L030 and S187-L031 backfill. -/
structure FundamentalLemmaLeafBackfill where
  leafId : String
  target : String
  selectedLemma : String
  checkedDeclarations : List String
  status : String
  remainingGate : String
deriving Repr

/-- One row in the C006 external Lean 4 primary-source audit. -/
structure ExternalLeanAnchorAudit where
  source : String
  revision : String
  moduleName : String
  checkedNames : List String
  matchedSearchTerms : List String
  status : String
  integrationBlocker : String
deriving Repr

/-- One row in the C007 completion-gate audit. -/
structure CompletionGateAudit where
  gate : String
  localEvidence : String
  status : String
  publicStatusConsequence : String
deriving Repr

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic",
  "Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus",
  "Mathlib.MeasureTheory.Integral.IntervalIntegral.IntegrationByParts",
  "Mathlib.Analysis.Calculus.ContDiff.Basic",
  "Mathlib.Analysis.Calculus.FDeriv.Basic",
  "Mathlib.Analysis.Calculus.LocalExtr.Basic"
]

/-- Integration-ready anchor table for the public Stage1 surface. -/
def mathlibAnchorTable : List MathlibAnchor := [
  {
    moduleName := "Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic"
    checkedNames := [
      "intervalIntegral.integral_const",
      "IntervalIntegrable"
    ]
    role := "action integral over a finite time interval"
    status := "repo-local checked wrapper: action_integral_const"
  },
  {
    moduleName := "Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus"
    checkedNames := [
      "intervalIntegral.integral_eq_sub_of_hasDerivAt",
      "intervalIntegral.integral_deriv_eq_sub"
    ]
    role := "fundamental-theorem bridge for endpoint terms"
    status := "repo-local checked wrappers: intervalIntegral_integral_eq_sub_of_hasDerivAt, intervalIntegral_integral_deriv_eq_sub"
  },
  {
    moduleName := "Mathlib.MeasureTheory.Integral.IntervalIntegral.IntegrationByParts"
    checkedNames := [
      "intervalIntegral.integral_mul_deriv_eq_deriv_mul",
      "intervalIntegral.integral_smul_deriv_eq_deriv_smul"
    ]
    role := "integration-by-parts bridge for first-variation leaves"
    status := "repo-local checked wrappers: intervalIntegral_integral_mul_deriv_eq_deriv_mul, intervalIntegral_integral_smul_deriv_eq_deriv_smul"
  },
  {
    moduleName := "Mathlib.Analysis.Calculus.FDeriv.Basic"
    checkedNames := [
      "fderiv",
      "HasFDerivAt",
      "ContinuousLinearMap.inl",
      "ContinuousLinearMap.inr"
    ]
    role := "position and velocity partial derivatives of the Lagrangian"
    status := "repo-local checked wrappers: positionDerivative_eq, velocityDerivative_eq"
  },
  {
    moduleName := "Mathlib.Analysis.Calculus.ContDiff.Basic"
    checkedNames := [
      "ContDiff",
      "ContDiffOn"
    ]
    role := "regularity hypotheses for curves, variations, and Lagrangian"
    status := "repo-local checked by declarations using ContDiff"
  },
  {
    moduleName := "Mathlib.Analysis.Calculus.LocalExtr.Basic"
    checkedNames := [
      "IsLocalMin.fderiv_eq_zero",
      "IsLocalExtr.fderiv_eq_zero"
    ]
    role := "Fermat local-extremum bridge from local least action to stationarity"
    status := "repo-local checked wrappers: localMin_fderiv_eq_zero, localExtr_fderiv_eq_zero"
  }
]

/-- Checked declaration names used as Stage1 anchors. -/
def mathlibAnchorNames : List String := [
  "deriv",
  "HasDerivAt",
  "HasFDerivAt",
  "fderiv",
  "ContDiff",
  "ContDiffOn",
  "intervalIntegral.integral_const",
  "intervalIntegral.integral_eq_sub_of_hasDerivAt",
  "intervalIntegral.integral_deriv_eq_sub",
  "intervalIntegral.integral_mul_deriv_eq_deriv_mul",
  "intervalIntegral.integral_smul_deriv_eq_deriv_smul",
  "IsLocalMin.fderiv_eq_zero",
  "IsLocalExtr.fderiv_eq_zero",
  "Integrable.ae_eq_zero_of_forall_setIntegral_eq_zero",
  "ContinuousLinearMap.inl",
  "ContinuousLinearMap.inr",
  "IntervalIntegrable"
]

/-- Repo-local checked backfill status for leaves S187-L020 through S187-L023. -/
def firstVariationLeafBackfillTable : List FirstVariationLeafBackfill := [
  {
    leafId := "S187-L020"
    target := "action-integrand integrability"
    checkedDeclarations := [
      "ActionIntegrand",
      "action_eq_integral_actionIntegrand",
      "actionIntegrand_intervalIntegrable_of_continuousOn"
    ]
    status := "checked local wrapper under ContinuousOn hypothesis"
    remainingGate := "derive the ContinuousOn/IntervalIntegrable hypothesis from the final selected Lagrangian and curve regularity assumptions"
  },
  {
    leafId := "S187-L021"
    target := "first-variation density and differentiation under the action integral"
    checkedDeclarations := [
      "FirstVariationDensity",
      "DifferentiatesUnderActionIntegral",
      "firstVariation_eq_integral_of_differentiatesUnderActionIntegral"
    ]
    status := "checked local bridge predicate and extraction theorem"
    remainingGate := "prove DifferentiatesUnderActionIntegral from regularity plus domination or a pinned mathlib differentiation-under-integral theorem"
  },
  {
    leafId := "S187-L022"
    target := "integration-by-parts anchors"
    checkedDeclarations := [
      "intervalIntegral_integral_mul_deriv_eq_deriv_mul",
      "intervalIntegral_integral_smul_deriv_eq_deriv_smul",
      "VelocityPairingIntegrationByParts"
    ]
    status := "checked mathlib wrappers plus concrete dual-pairing bridge target"
    remainingGate := "derive VelocityPairingIntegrationByParts for continuous-linear-functional pairings"
  },
  {
    leafId := "S187-L023"
    target := "endpoint-vanishing integration-by-parts consequence"
    checkedDeclarations := [
      "VelocityPairingIntegrand",
      "VariationPairingIntegrand",
      "velocityPairing_integral_eq_neg_integral_of_vanishing_endpoints"
    ]
    status := "checked endpoint-cancellation consequence under the dual-pairing IBP hypothesis"
    remainingGate := "combine the proved dual-pairing IBP with Euler-Lagrange equality and first-variation density integrability"
  }
]

/-- Repo-local checked backfill status for leaves S187-L030 and S187-L031. -/
def fundamentalLemmaLeafBackfillTable : List FundamentalLemmaLeafBackfill := [
  {
    leafId := "S187-L030"
    target := "measure-theoretic fundamental lemma on the open time interval"
    selectedLemma := "Integrable.ae_eq_zero_of_forall_setIntegral_eq_zero specialized to InteriorTimeMeasure"
    checkedDeclarations := [
      "InteriorTimeMeasure",
      "SetIntegralZeroOnInterior",
      "FundamentalLemmaAEConclusion",
      "measureTheory_ae_eq_zero_of_forall_setIntegral_eq_zero",
      "fundamentalLemmaAE_of_integrable_setIntegral_zero"
    ]
    status := "checked local wrapper over pinned mathlib; proves an almost-everywhere zero conclusion from zero set integrals"
    remainingGate := "connect smooth fixed-endpoint variation test functions to the all finite-measure set-integral hypothesis, or replace this bridge with a pinned smooth-test-function theorem"
  },
  {
    leafId := "S187-L031"
    target := "smooth-variation fundamental lemma converting weak residual vanishing to pointwise Euler-Lagrange residual vanishing"
    selectedLemma := "FundamentalLemmaForVariations"
    checkedDeclarations := [
      "EulerLagrangeResidual",
      "ResidualPairingIntegrand",
      "FundamentalLemmaForVariations",
      "residual_eq_zero_of_fundamentalLemmaForVariations"
    ]
    status := "checked bridge target and elimination wrapper; not a completed proof of the smooth fundamental lemma"
    remainingGate := "prove FundamentalLemmaForVariations from bump functions/test-function density and residual regularity, or pin/import/check an external Lean 4 proof; until then the parent theorem remains formalization_debt"
  }
]

/-- Search terms that did not locate a terminal least-action theorem in pinned mathlib. -/
def absentTerminalSearchTerms : List String := [
  "least action",
  "stationary action",
  "principle of least action",
  "Euler-Lagrange",
  "EulerLagrange",
  "Lagrangian",
  "calculus of variations",
  "first variation",
  "Hamilton principle",
  "Hamilton's principle"
]

/-- Exact C006 search terms requested for external Lean 4 primary-source audit. -/
def c006ExternalSearchTerms : List String := [
  "EulerLagrange",
  "least_action",
  "stationary_action",
  "Hamilton_principle",
  "first_variation"
]

/-- Current Physlib revision inspected for C006 external-anchor audit. -/
def c006PhyslibCurrentRevision : String :=
  "cd22b0c28882412447d12d5cfde677c4ad999994"

/-- Current Physlib Lean toolchain observed during C006 audit. -/
def c006PhyslibCurrentLeanToolchain : String :=
  "leanprover/lean4:v4.29.1"

/-- Current Physlib mathlib revision observed during C006 audit. -/
def c006PhyslibCurrentMathlibRevision : String :=
  "5e932f97dd25535344f80f9dd8da3aab83df0fe6"

/-- Earlier PhysLean/physlib revision inspected by sibling Stage1 audits. -/
def c006PhyslibLegacyRevision : String :=
  "f4f09f50fd292e69301ae6f12ab12358df2112f6"

/-- Legacy PhysLean/physlib Lean toolchain at the pinned sibling-audit revision. -/
def c006PhyslibLegacyLeanToolchain : String :=
  "leanprover/lean4:v4.28.0"

/-- Legacy PhysLean/physlib mathlib revision at the pinned sibling-audit revision. -/
def c006PhyslibLegacyMathlibRevision : String :=
  "8f9d9cff6bd728b17a24e163c9402775d9e6a365"

/-- Current SciLean revision inspected for C006 negative-search audit. -/
def c006SciLeanCurrentRevision : String :=
  "95f8119a2884e9c41f82136523bd5568ea7075c5"

/--
C006 external Lean 4 primary-source audit table.

Rows are anchors or exclusions only.  None is imported into this repository's
Lake dependency closure in this child pass, so no row is counted as terminal
completion of the least-action theorem.
-/
def c006ExternalLeanAnchorAuditTable : List ExternalLeanAnchorAudit := [
  {
    source := "https://github.com/leanprover-community/physlib"
    revision := c006PhyslibCurrentRevision
    moduleName := "Physlib.ClassicalMechanics.EulerLagrange"
    checkedNames := [
      "ClassicalMechanics.eulerLagrangeOp",
      "ClassicalMechanics.eulerLagrangeOp_eq",
      "ClassicalMechanics.eulerLagrangeOp_zero",
      "ClassicalMechanics.euler_lagrange_varGradient"
    ]
    matchedSearchTerms := [
      "EulerLagrange",
      "first_variation"
    ]
    status := "external_upstream_anchor_only; proves a variational-gradient-to-Euler-Lagrange identity in Physlib's Time/varGradient framework, not this repo's fixed-endpoint StationaryAction theorem"
    integrationBlocker := "not pin/import/check in this child: current Physlib requires Lean v4.29.1 and mathlib 5e932f97dd25535344f80f9dd8da3aab83df0fe6, while this repo uses Lean v4.29.0 and mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95; importing also needs an API bridge from Physlib Time/inner-product varGradient to BoundaryData/FirstVariation/StationaryAction"
  },
  {
    source := "https://github.com/leanprover-community/physlib"
    revision := c006PhyslibCurrentRevision
    moduleName := "Physlib.Mathematics.VariationalCalculus.Basic"
    checkedNames := [
      "fundamental_theorem_of_variational_calculus'",
      "fundamental_theorem_of_variational_calculus"
    ]
    matchedSearchTerms := [
      "first_variation"
    ]
    status := "external_upstream_anchor_only; supplies a test-function fundamental lemma in Physlib's variational-calculus API, useful for S187-L031 but not imported or adapted"
    integrationBlocker := "same Lean/mathlib dependency mismatch as Physlib EulerLagrange; after pinning, a bridge is still needed from Physlib IsTestFunction/inner-product hypotheses to smooth fixed-endpoint variations on Ioo B.t₀ B.t₁"
  },
  {
    source := "https://github.com/leanprover-community/physlib"
    revision := c006PhyslibCurrentRevision
    moduleName := "Physlib.ClassicalMechanics.HarmonicOscillator.Basic"
    checkedNames := [
      "ClassicalMechanics.HarmonicOscillator.equationOfMotion_tfae"
    ]
    matchedSearchTerms := [
      "least_action",
      "stationary_action",
      "Hamilton_principle"
    ]
    status := "external_upstream_anchor_only; model-specific harmonic-oscillator equivalence includes a variational-principle formulation but is not the general least-action theorem"
    integrationBlocker := "same Physlib dependency mismatch; even after import this would be a special-case anchor and would not close the general Stage1 statement"
  },
  {
    source := "https://github.com/lecopivo/SciLean"
    revision := c006SciLeanCurrentRevision
    moduleName := "doc/literate/literate_lean_test.lean"
    checkedNames := [
      "section EulerLagrange"
    ]
    matchedSearchTerms := [
      "EulerLagrange"
    ]
    status := "excluded; literate/demo material only, includes unclosed placeholder proofs, and no checked least-action or stationary-action theorem was found in SciLean source search"
    integrationBlocker := "no integration target identified"
  },
  {
    source := "pinned local mathlib dependency"
    revision := mathlibAnchorRevision
    moduleName := "Mathlib"
    checkedNames := []
    matchedSearchTerms := c006ExternalSearchTerms
    status := "negative terminal search; pinned mathlib has calculus, interval-integral, local-extremum, and measure-theoretic anchors but no terminal theorem named or documented as EulerLagrange, least_action, stationary_action, Hamilton_principle, or first_variation"
    integrationBlocker := "none for mathlib anchors already imported; terminal theorem remains formalization_debt rather than repo_local_integration_debt"
  }
]

/-- C006 found external anchors but no repo-local terminal closure. -/
def c006TerminalExternalClosureImported : Bool :=
  false

/--
C006 repo-local integration-debt gate.

This is `true` only because no completed theorem state is claimed by C006.
The Physlib rows remain external anchors with concrete blockers, not completed
repo-local closures.
-/
def c006NoCompletedRepoLocalIntegrationDebt : Bool :=
  true

/--
C007 gate: no local proof body for the terminal stationary-action theorem has
validated in this repository.
-/
def c007LocalProofBodyValidated : Bool :=
  false

/--
C007 gate: no terminal mathlib wrapper closes the selected stationary-action
target in this repository.
-/
def c007TerminalMathlibWrapperValidated : Bool :=
  false

/--
C007 gate: no external least-action dependency is pinned, imported, and checked
inside this repository's Lake closure.
-/
def c007PinnedExternalDependencyValidated : Bool :=
  false

/--
C007 public-status gate.

The parent must stay open because none of the three completion paths has
validated repo-locally.
-/
def c007PublicStatusMustRemainOpen : Bool :=
  true

/-- C007 integration-ready completion-gate audit table. -/
def c007CompletionGateAuditTable : List CompletionGateAudit := [
  {
    gate := "local_proof_body"
    localEvidence := "StatementShape is a checked Prop and local wrappers validate only statement-shape, integrability, endpoint-cancellation, and anchor APIs; no theorem proves StatementShape or StationaryAction from EulerLagrangeEquation."
    status := "not_repo_local_closed"
    publicStatusConsequence := "keep S1-M-187 open / not completed"
  },
  {
    gate := "local_wrapper_upstream_mathlib"
    localEvidence := "Pinned mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95 supplies interval-integral, calculus, local-extremum, and measure-theoretic wrappers recorded in mathlibAnchorTable, but no terminal least-action or Euler-Lagrange theorem wrapper."
    status := "not_repo_local_closed"
    publicStatusConsequence := "keep S1-M-187 open / not completed"
  },
  {
    gate := "external_upstream_pinned"
    localEvidence := "c006ExternalLeanAnchorAuditTable records Physlib anchors as external_upstream_anchor_only with Lean/mathlib mismatch and API-bridge blockers; no dependency was added to this repository."
    status := "external_upstream_anchor_only_with_blocker"
    publicStatusConsequence := "keep S1-M-187 open / not completed"
  },
  {
    gate := "repo_local_integration_debt"
    localEvidence := "No completed theorem state is claimed by this file, so external anchor-only evidence is not counted as completion."
    status := "no_completed_state_retains_repo_local_integration_debt"
    publicStatusConsequence := "public backfill may record progress, but must not mark the theorem complete"
  }
]

/-- Checked C007 summary: the public parent status must remain open. -/
theorem c007_publicStatusMustRemainOpen_eq_true :
    c007PublicStatusMustRemainOpen = true :=
  rfl

/-! ## Audit probes -/

#check Curve
#check Velocity
#check Action
#check ActionIntegrand
#check FirstVariation
#check FirstVariationDensity
#check DifferentiatesUnderActionIntegral
#check VelocityPairingIntegrationByParts
#check EulerLagrangeResidual
#check ResidualPairingIntegrand
#check FundamentalLemmaForVariations
#check InteriorTimeMeasure
#check SetIntegralZeroOnInterior
#check FundamentalLemmaAEConclusion
#check AdmissibleCurve
#check AdmissibleVariation
#check StationaryAction
#check LocallyMinimizesAction
#check EulerLagrangeEquation
#check SelectedPublicTarget
#check StationaryTargetHypotheses
#check StatementShape
#check action_eq_integral_actionIntegrand
#check actionIntegrand_intervalIntegrable_of_continuousOn
#check firstVariation_eq_integral_of_differentiatesUnderActionIntegral
#check velocityPairing_integral_eq_neg_integral_of_vanishing_endpoints
#check measureTheory_ae_eq_zero_of_forall_setIntegral_eq_zero
#check fundamentalLemmaAE_of_integrable_setIntegral_zero
#check residual_eq_zero_of_fundamentalLemmaForVariations
#check deriv
#check HasDerivAt
#check HasFDerivAt
#check fderiv
#check ContDiff
#check ContDiffOn
#check intervalIntegral.integral_const
#check intervalIntegral.integral_eq_sub_of_hasDerivAt
#check intervalIntegral.integral_deriv_eq_sub
#check intervalIntegral.integral_mul_deriv_eq_deriv_mul
#check intervalIntegral.integral_smul_deriv_eq_deriv_smul
#check IsLocalMin.fderiv_eq_zero
#check IsLocalExtr.fderiv_eq_zero
#check Integrable.ae_eq_zero_of_forall_setIntegral_eq_zero
#check mathlibAnchorRevision
#check mathlibAnchorTable
#check firstVariationLeafBackfillTable
#check fundamentalLemmaLeafBackfillTable
#check c006ExternalSearchTerms
#check c006PhyslibCurrentRevision
#check c006PhyslibCurrentLeanToolchain
#check c006PhyslibCurrentMathlibRevision
#check c006PhyslibLegacyRevision
#check c006PhyslibLegacyLeanToolchain
#check c006PhyslibLegacyMathlibRevision
#check c006SciLeanCurrentRevision
#check c006ExternalLeanAnchorAuditTable
#check c006TerminalExternalClosureImported
#check c006NoCompletedRepoLocalIntegrationDebt
#check c007LocalProofBodyValidated
#check c007TerminalMathlibWrapperValidated
#check c007PinnedExternalDependencyValidated
#check c007PublicStatusMustRemainOpen
#check c007CompletionGateAuditTable
#check c007_publicStatusMustRemainOpen_eq_true

end S1_M_187
end Stage1
end AwesomeTheorems
