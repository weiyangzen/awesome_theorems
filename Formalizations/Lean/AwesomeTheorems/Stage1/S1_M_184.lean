import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.FDeriv.Basic
import Mathlib.Dynamics.Flow

/-!
# S1-M-184 / THM-M-1515: Noether's theorem

This Stage1 artifact records a conservative Lean 4 statement boundary for
Noether's theorem: continuous symmetries of a variational system give conserved
quantities.

The pinned mathlib snapshot has differentiability, Frechet derivatives,
continuous linear maps, flows, and invariant sets.  It does not expose a
terminal theorem named Noether's theorem, nor a canonical Lagrangian mechanics
API with Euler-Lagrange equations and moment maps.  The declarations below
therefore normalize an abstract finite-dimensional statement shape and keep
the Euler-Lagrange/noether-current bridge as explicit proposition fields.

No terminal proof of Noether's theorem is claimed here.
-/

noncomputable section

open Set

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_184

universe u

/-- Classical velocity of a real-time trajectory. -/
def velocity
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (q : ℝ → E) : ℝ → E :=
  fun t => deriv q t

/-- A real-valued function is conserved along time when its classical derivative vanishes. -/
def ConservedAlong (J : ℝ → ℝ) : Prop :=
  ∀ t : ℝ, deriv J t = 0

/--
An abstract Lagrangian system with a one-parameter symmetry.

Concrete fields use mathlib objects where available:
* `symmetryFlow` is a bundled `Flow ℝ E`;
* `lagrangian` is a function of position and velocity;
* `momentum` is a continuous linear functional in the infinitesimal symmetry
  direction.

The separate proposition predicates below mark the formalization boundary that
a full Noether theorem must close: Euler-Lagrange equations, invariance of the
Lagrangian under the lifted symmetry, identification of the infinitesimal
generator, identification of the momentum as the velocity derivative of the
Lagrangian, and the derivative computation for the Noether current.
-/
structure NoetherSystem
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] :
    Type u where
  lagrangian : E × E → ℝ
  symmetryFlow : Flow ℝ E
  infinitesimalGenerator : E → E
  momentum : E → E → E →L[ℝ] ℝ
  eulerLagrange : (ℝ → E) → Prop

/-- The Noether charge associated to an abstract system and trajectory. -/
def NoetherCharge
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (S : NoetherSystem E) (q : ℝ → E) : ℝ → ℝ :=
  fun t => S.momentum (q t) (velocity q t) (S.infinitesimalGenerator (q t))

/--
Concrete lifted-flow invariance equation for a Lagrangian.

The velocity component is transported by the Frechet derivative of the
time-`τ` flow map.  This is the replacement for an opaque
`NoetherSystem.lagrangianInvariant` field: the invariant object is explicitly
`lagrangian : E × E → ℝ`.
-/
def LiftedFlowLagrangianInvariant
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (lagrangian : E × E → ℝ) (symmetryFlow : Flow ℝ E) : Prop :=
  ∀ (τ : ℝ) (x v : E),
    lagrangian
        (symmetryFlow τ x,
          fderiv ℝ (fun y : E => symmetryFlow τ y) x v) =
      lagrangian (x, v)

/--
System-level Lagrangian invariance is exactly the concrete lifted-flow equation
for the system's `lagrangian : E × E → ℝ` and bundled symmetry flow.
-/
def LagrangianInvariant
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (S : NoetherSystem E) : Prop :=
  LiftedFlowLagrangianInvariant S.lagrangian S.symmetryFlow

/--
The infinitesimal generator is the derivative of the symmetry flow at parameter
zero, stated as a `HasDerivAt` boundary condition.
-/
def InfinitesimalGeneratorEqDerivative
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (S : NoetherSystem E) : Prop :=
  ∀ x : E,
    HasDerivAt (fun τ : ℝ => S.symmetryFlow τ x) (S.infinitesimalGenerator x) 0

/-- The Frechet derivative of a Lagrangian in its velocity coordinate. -/
def VelocityCoordinateFDeriv
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (lagrangian : E × E → ℝ) (x v : E) : E →L[ℝ] ℝ :=
  fderiv ℝ (fun w : E => lagrangian (x, w)) v

/-- The momentum is the Frechet derivative of the Lagrangian in the velocity coordinate. -/
def MomentumIsVelocityDerivative
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (S : NoetherSystem E) : Prop :=
  ∀ x v : E, VelocityCoordinateFDeriv S.lagrangian x v = S.momentum x v

/-- The Euler-Lagrange and symmetry bridge proves the Noether-current derivative vanishes. -/
def NoetherCurrentDerivativeFormula
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (S : NoetherSystem E) : Prop :=
  ∀ q : ℝ → E, S.eulerLagrange q → ∀ t : ℝ, deriv (NoetherCharge S q) t = 0

/-- The hypotheses needed to apply the normalized Noether statement for one system. -/
def NoetherHypotheses
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (S : NoetherSystem E) : Prop :=
  LagrangianInvariant S ∧
    InfinitesimalGeneratorEqDerivative S ∧
      MomentumIsVelocityDerivative S ∧
        NoetherCurrentDerivativeFormula S

/-- The conclusion for one trajectory: its Noether charge is conserved. -/
def NoetherConclusion
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (S : NoetherSystem E) (q : ℝ → E) : Prop :=
  ConservedAlong (NoetherCharge S q)

/--
Normalized Stage1 statement shape for Noether's theorem.

For every normed real phase/configuration space and every abstract
Lagrangian system, if the symmetry, infinitesimal-generator, momentum, and
current-derivative packages are supplied, every Euler-Lagrange trajectory has a
conserved Noether charge.
-/
def StatementShape
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] :
    Prop :=
  ∀ S : NoetherSystem E,
    NoetherHypotheses S →
      ∀ q : ℝ → E, S.eulerLagrange q → NoetherConclusion S q

/-- The normalized statement shape unfolds to the expected implication. -/
theorem statementShape_iff_forall_system
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] :
    StatementShape E ↔
      ∀ S : NoetherSystem E,
        NoetherHypotheses S →
          ∀ q : ℝ → E, S.eulerLagrange q → NoetherConclusion S q :=
  Iff.rfl

/--
A local proof package for a single abstract system.

This is ordinary data.  A terminal formalization should
replace this package by proofs from concrete Euler-Lagrange and symmetry APIs,
or by a pinned upstream theorem wrapper if such a theorem exists.
-/
structure NoetherProofPackage
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (S : NoetherSystem E) : Type u where
  conservation_from_hypotheses :
    NoetherHypotheses S →
      ∀ q : ℝ → E, S.eulerLagrange q → NoetherConclusion S q

/-- A supplied proof package closes the normalized statement for its system. -/
theorem NoetherProofPackage.statement_for_system
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {S : NoetherSystem E} (P : NoetherProofPackage S) :
    NoetherHypotheses S →
      ∀ q : ℝ → E, S.eulerLagrange q → NoetherConclusion S q :=
  P.conservation_from_hypotheses

/--
The normalized abstract statement is closed once the explicit
Noether-current derivative bridge is available for the system.
-/
theorem noetherConclusion_of_hypotheses
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {S : NoetherSystem E} (h : NoetherHypotheses S) :
    ∀ q : ℝ → E, S.eulerLagrange q → NoetherConclusion S q := by
  intro q hq t
  exact h.2.2.2 q hq t

/--
With the current-derivative bridge recorded as an explicit hypothesis field,
the Stage1 statement shape is a theorem for the abstract boundary object.
-/
theorem statementShape_of_current_derivative_bridge
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] :
    StatementShape E := by
  intro S hS q hq
  exact noetherConclusion_of_hypotheses hS q hq

/-- The system-level predicate is definitionally the concrete lifted-flow equation. -/
theorem lagrangianInvariant_iff_liftedFlow
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (S : NoetherSystem E) :
    LagrangianInvariant S ↔
      LiftedFlowLagrangianInvariant S.lagrangian S.symmetryFlow :=
  Iff.rfl

/-- Apply the concrete lifted-flow Lagrangian invariance equation. -/
theorem LagrangianInvariant.apply
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {S : NoetherSystem E} (h : LagrangianInvariant S) (τ : ℝ) (x v : E) :
    S.lagrangian
        (S.symmetryFlow τ x,
          fderiv ℝ (fun y : E => S.symmetryFlow τ y) x v) =
      S.lagrangian (x, v) :=
  h τ x v

/-- Project Lagrangian invariance from the normalized hypothesis package. -/
theorem NoetherHypotheses.lagrangianInvariant
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {S : NoetherSystem E} (h : NoetherHypotheses S) :
    LagrangianInvariant S :=
  h.1

/-- Project the infinitesimal-generator bridge from the normalized hypothesis package. -/
theorem NoetherHypotheses.infinitesimalGenerator_eq_derivative
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {S : NoetherSystem E} (h : NoetherHypotheses S) :
    InfinitesimalGeneratorEqDerivative S :=
  h.2.1

/-- Apply the infinitesimal-generator `HasDerivAt` bridge at a point. -/
theorem InfinitesimalGeneratorEqDerivative.hasDerivAt
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {S : NoetherSystem E} (h : InfinitesimalGeneratorEqDerivative S) (x : E) :
    HasDerivAt (fun τ : ℝ => S.symmetryFlow τ x) (S.infinitesimalGenerator x) 0 :=
  h x

/-- Recover the classical `deriv` equality from the `HasDerivAt` bridge. -/
theorem InfinitesimalGeneratorEqDerivative.deriv
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {S : NoetherSystem E} (h : InfinitesimalGeneratorEqDerivative S) (x : E) :
    deriv (fun τ : ℝ => S.symmetryFlow τ x) 0 = S.infinitesimalGenerator x :=
  (h.hasDerivAt x).deriv

/-- Project the pointwise `HasDerivAt` bridge from the normalized hypotheses. -/
theorem NoetherHypotheses.infinitesimalGenerator_hasDerivAt
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {S : NoetherSystem E} (h : NoetherHypotheses S) (x : E) :
    HasDerivAt (fun τ : ℝ => S.symmetryFlow τ x) (S.infinitesimalGenerator x) 0 :=
  h.infinitesimalGenerator_eq_derivative.hasDerivAt x

/-- Project the classical `deriv` equation from the normalized hypotheses. -/
theorem NoetherHypotheses.infinitesimalGenerator_deriv
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {S : NoetherSystem E} (h : NoetherHypotheses S) (x : E) :
    deriv (fun τ : ℝ => S.symmetryFlow τ x) 0 = S.infinitesimalGenerator x :=
  h.infinitesimalGenerator_eq_derivative.deriv x

/-- Project the momentum bridge from the normalized hypothesis package. -/
theorem NoetherHypotheses.momentum_is_velocity_derivative
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {S : NoetherSystem E} (h : NoetherHypotheses S) :
    MomentumIsVelocityDerivative S :=
  h.2.2.1

/-- Apply the velocity-coordinate Frechet derivative bridge at a position and velocity. -/
theorem MomentumIsVelocityDerivative.fderiv_eq_momentum
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {S : NoetherSystem E} (h : MomentumIsVelocityDerivative S) (x v : E) :
    fderiv ℝ (fun w : E => S.lagrangian (x, w)) v = S.momentum x v :=
  h x v

/--
The velocity-coordinate Frechet derivative, applied to a velocity variation,
is the system momentum applied to that variation.
-/
theorem MomentumIsVelocityDerivative.apply
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {S : NoetherSystem E} (h : MomentumIsVelocityDerivative S) (x v δv : E) :
    fderiv ℝ (fun w : E => S.lagrangian (x, w)) v δv = S.momentum x v δv := by
  rw [h.fderiv_eq_momentum x v]

/-- Project the concrete velocity-coordinate `fderiv` equation from the normalized hypotheses. -/
theorem NoetherHypotheses.velocity_fderiv_eq_momentum
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {S : NoetherSystem E} (h : NoetherHypotheses S) (x v : E) :
    fderiv ℝ (fun w : E => S.lagrangian (x, w)) v = S.momentum x v :=
  h.momentum_is_velocity_derivative.fderiv_eq_momentum x v

/--
Project the pointwise velocity-variation form of the momentum bridge from the
normalized hypotheses.
-/
theorem NoetherHypotheses.velocity_fderiv_apply
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {S : NoetherSystem E} (h : NoetherHypotheses S) (x v δv : E) :
    fderiv ℝ (fun w : E => S.lagrangian (x, w)) v δv = S.momentum x v δv :=
  h.momentum_is_velocity_derivative.apply x v δv

/-- Project the Noether-current derivative computation from the hypothesis package. -/
theorem NoetherHypotheses.noether_current_derivative_formula
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {S : NoetherSystem E} (h : NoetherHypotheses S) :
    NoetherCurrentDerivativeFormula S :=
  h.2.2.2

/-- The formal velocity is definitionally the classical derivative. -/
theorem velocity_eq_deriv
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (q : ℝ → E) :
    velocity q = fun t => deriv q t :=
  rfl

/-- The Noether charge unfolds to momentum applied to the infinitesimal generator. -/
theorem noetherCharge_eq_momentum_generator
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (S : NoetherSystem E) (q : ℝ → E) :
    NoetherCharge S q =
      fun t => S.momentum (q t) (velocity q t) (S.infinitesimalGenerator (q t)) :=
  rfl

/-- A constant real-valued current is conserved in the normalized sense. -/
theorem conservedAlong_const (c : ℝ) :
    ConservedAlong (fun _ : ℝ => c) := by
  intro t
  simp

/-! ## One-dimensional zero-Lagrangian special case -/

/-- The zero Lagrangian on the one-dimensional real configuration space. -/
def realZeroLagrangian : ℝ × ℝ → ℝ :=
  fun _ => 0

/-- The identity real-line flow used as a concrete one-parameter symmetry. -/
def realIdentityFlow : Flow ℝ ℝ :=
  default

/--
A concrete one-dimensional Euler-Lagrange residual.

For `L : ℝ × ℝ → ℝ`, the coordinate velocity derivative is evaluated on the
real basis vector `1`, and the coordinate position derivative is evaluated on
the same vector.  The residual is
`d/dt (partial L / partial v) - partial L / partial x`.
-/
def RealEulerLagrangeResidual (L : ℝ × ℝ → ℝ) (q : ℝ → ℝ) (t : ℝ) : ℝ :=
  deriv (fun τ : ℝ => VelocityCoordinateFDeriv L (q τ) (velocity q τ) 1) t -
    fderiv ℝ (fun x : ℝ => L (x, velocity q t)) (q t) 1

/-- A concrete Euler-Lagrange predicate for real-line trajectories. -/
def RealEulerLagrange (L : ℝ × ℝ → ℝ) (q : ℝ → ℝ) : Prop :=
  ∀ t : ℝ, RealEulerLagrangeResidual L q t = 0

/-- Every real-line trajectory satisfies the zero-Lagrangian Euler-Lagrange equation. -/
theorem realEulerLagrange_zeroLagrangian (q : ℝ → ℝ) :
    RealEulerLagrange realZeroLagrangian q := by
  intro t
  simp [RealEulerLagrangeResidual, VelocityCoordinateFDeriv, realZeroLagrangian]

/-- The concrete zero-Lagrangian real-line Noether system. -/
def realZeroLagrangianSystem : NoetherSystem ℝ where
  lagrangian := realZeroLagrangian
  symmetryFlow := realIdentityFlow
  infinitesimalGenerator := fun _ => 0
  momentum := fun _ _ => 0
  eulerLagrange := RealEulerLagrange realZeroLagrangian

/-- The zero Lagrangian is invariant under the identity lifted flow. -/
theorem realZeroLagrangianSystem_lagrangianInvariant :
    LagrangianInvariant realZeroLagrangianSystem := by
  intro τ x v
  simp [realZeroLagrangianSystem, realZeroLagrangian]

/-- The infinitesimal generator of the identity real-line flow is zero. -/
theorem realZeroLagrangianSystem_infinitesimalGenerator :
    InfinitesimalGeneratorEqDerivative realZeroLagrangianSystem := by
  intro x
  simpa [realZeroLagrangianSystem, realIdentityFlow] using
    (hasDerivAt_const (0 : ℝ) x)

/-- The zero momentum is the velocity derivative of the zero Lagrangian. -/
theorem realZeroLagrangianSystem_momentum :
    MomentumIsVelocityDerivative realZeroLagrangianSystem := by
  intro x v
  ext
  simp [VelocityCoordinateFDeriv, realZeroLagrangianSystem, realZeroLagrangian]

/--
Concrete Noether-current derivative cancellation for the zero-Lagrangian
real-line special case.
-/
theorem realZeroLagrangianSystem_currentDerivative :
    NoetherCurrentDerivativeFormula realZeroLagrangianSystem := by
  intro q _hq t
  change deriv (fun _ : ℝ => (0 : ℝ)) t = 0
  simp

/--
The one-dimensional zero-Lagrangian system satisfies the normalized Noether
hypothesis package by local proof bodies.
-/
theorem realZeroLagrangianSystem_noetherHypotheses :
    NoetherHypotheses realZeroLagrangianSystem :=
  ⟨realZeroLagrangianSystem_lagrangianInvariant,
    realZeroLagrangianSystem_infinitesimalGenerator,
    realZeroLagrangianSystem_momentum,
    realZeroLagrangianSystem_currentDerivative⟩

/-- The Noether charge of the zero-Lagrangian real-line system is conserved. -/
theorem realZeroLagrangianSystem_conserved
    (q : ℝ → ℝ) (hq : RealEulerLagrange realZeroLagrangian q) :
    NoetherConclusion realZeroLagrangianSystem q :=
  noetherConclusion_of_hypotheses realZeroLagrangianSystem_noetherHypotheses q hq

/-- mathlib flow anchor: time zero acts as the identity. -/
theorem symmetryFlow_zero_apply
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (S : NoetherSystem E) (x : E) :
    S.symmetryFlow 0 x = x :=
  Flow.map_zero_apply S.symmetryFlow x

/-- mathlib flow anchor: a flow composes by adding times. -/
theorem symmetryFlow_map_add
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (S : NoetherSystem E) (t₁ t₂ : ℝ) (x : E) :
    S.symmetryFlow (t₁ + t₂) x = S.symmetryFlow t₁ (S.symmetryFlow t₂ x) :=
  Flow.map_add S.symmetryFlow t₁ t₂ x

/-- mathlib invariant-set anchor for the orbit of a point under the symmetry flow. -/
theorem orbit_isInvariant
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (S : NoetherSystem E) (x : E) :
    IsInvariant S.symmetryFlow (Flow.orbit S.symmetryFlow x) :=
  Flow.isInvariant_orbit S.symmetryFlow x

/-- mathlib differentiability anchor: differentiability gives a Frechet derivative witness. -/
theorem differentiableAt_hasFDerivAt
    {E F : Type u}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    [NormedAddCommGroup F] [NormedSpace ℝ F]
    {f : E → F} {x : E} (hf : DifferentiableAt ℝ f x) :
    HasFDerivAt f (fderiv ℝ f x) x :=
  hf.hasFDerivAt

/-- mathlib differentiability anchor: the identity has the identity Frechet derivative. -/
theorem fderiv_id_anchor
    {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E] :
    fderiv ℝ (id : E → E) = fun _ => ContinuousLinearMap.id ℝ E := by
  funext x
  exact fderiv_id

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Analysis.Calculus.Deriv.Basic",
  "Mathlib.Analysis.Calculus.FDeriv.Basic",
  "Mathlib.Analysis.Calculus.FDeriv.Comp",
  "Mathlib.Analysis.Calculus.FDeriv.Const",
  "Mathlib.Analysis.Calculus.LineDeriv.Basic",
  "Mathlib.Dynamics.Flow",
  "Mathlib.Analysis.ODE.Basic",
  "Mathlib.Analysis.ODE.PicardLindelof",
  "Mathlib.Geometry.Manifold.Algebra.LeftInvariantDerivation"
]

/-- Pinned mathlib revision used for the Stage1 Noether audit. -/
def mathlibPinnedRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Checked or audited local names used as anchors for the statement boundary. -/
def mathlibAnchorNames : List String := [
  "deriv",
  "HasDerivAt",
  "fderiv",
  "HasFDerivAt",
  "DifferentiableAt.hasFDerivAt",
  "ContinuousLinearMap",
  "Flow",
  "Flow.map_zero_apply",
  "Flow.map_add",
  "Flow.orbit",
  "Flow.isInvariant_orbit",
  "IsInvariant",
  "HasDerivAt.const"
]

/--
Search terms that did not locate a terminal Noether theorem in the pinned
mathlib snapshot during this Stage1 audit.
-/
def absentTerminalSearchTerms : List String := [
  "Noether",
  "Noether theorem",
  "Lagrangian",
  "Euler-Lagrange",
  "EulerLagrange",
  "conserved quantity",
  "conservation law",
  "momentum map",
  "Hamiltonian symmetry",
  "variational symmetry"
]

/--
Public audit note for serialized Stage1 backfill: pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` provides `deriv`, `fderiv`,
`HasFDerivAt`, `ContinuousLinearMap`, `Flow`, and `IsInvariant`; no terminal
variational Noether theorem was found in that pinned snapshot.
-/
def mathlibNoetherAuditNote : String :=
  "Pinned mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95 provides \
  deriv, fderiv, HasFDerivAt, ContinuousLinearMap, Flow, and IsInvariant; \
  no terminal variational Noether theorem was found in that pinned snapshot."

/-! ## M0387 completion gate record -/

/--
Current repo-local closure status for the terminal variational Noether theorem.

The finite-dimensional zero-Lagrangian special case above has local proof
bodies, but the general Noether theorem is not repo-locally closed by this
Stage1 artifact.
-/
def terminalNoetherRepoLocalStatus : String :=
  "not_repo_local_closed"

/--
M0387-level completion gates that must be reflected on the serialized public
surface before the parent theorem can be marked complete.
-/
def m0387CompletionGateLeaves : List String := [
  "public_surface_records_local_validation",
  "public_surface_records_leq_100_leaf_ledger",
  "terminal_local_proof_body_or_pinned_imported_checked_upstream_closure",
  "no_residual_repo_local_integration_debt"
]

/--
Public backfill note for the completion gate: do not close THM-M-1515 from
anchor-only evidence or from the abstract statement boundary.
-/
def m0387CompletionGateNote : String :=
  "Keep THM-M-1515 open until the public surface records local validation, a \
  <=100 leaf ledger, and either a terminal local proof body or a pinned, \
  imported, checked upstream closure, with no residual repo_local_integration_debt."

/-! ## Audit probes -/

#check velocity
#check ConservedAlong
#check NoetherSystem
#check NoetherCharge
#check LiftedFlowLagrangianInvariant
#check LagrangianInvariant
#check lagrangianInvariant_iff_liftedFlow
#check LagrangianInvariant.apply
#check InfinitesimalGeneratorEqDerivative
#check InfinitesimalGeneratorEqDerivative.hasDerivAt
#check InfinitesimalGeneratorEqDerivative.deriv
#check NoetherHypotheses.infinitesimalGenerator_hasDerivAt
#check NoetherHypotheses.infinitesimalGenerator_deriv
#check VelocityCoordinateFDeriv
#check MomentumIsVelocityDerivative
#check MomentumIsVelocityDerivative.fderiv_eq_momentum
#check MomentumIsVelocityDerivative.apply
#check NoetherHypotheses.velocity_fderiv_eq_momentum
#check NoetherHypotheses.velocity_fderiv_apply
#check NoetherCurrentDerivativeFormula
#check NoetherHypotheses
#check NoetherConclusion
#check StatementShape
#check NoetherProofPackage.statement_for_system
#check noetherConclusion_of_hypotheses
#check statementShape_of_current_derivative_bridge
#check conservedAlong_const
#check realZeroLagrangian
#check realIdentityFlow
#check RealEulerLagrangeResidual
#check RealEulerLagrange
#check realEulerLagrange_zeroLagrangian
#check realZeroLagrangianSystem
#check realZeroLagrangianSystem_lagrangianInvariant
#check realZeroLagrangianSystem_infinitesimalGenerator
#check realZeroLagrangianSystem_momentum
#check realZeroLagrangianSystem_currentDerivative
#check realZeroLagrangianSystem_noetherHypotheses
#check realZeroLagrangianSystem_conserved
#check symmetryFlow_zero_apply
#check symmetryFlow_map_add
#check orbit_isInvariant
#check differentiableAt_hasFDerivAt
#check fderiv_id_anchor
#check mathlibPinnedRevision
#check mathlibNoetherAuditNote
#check terminalNoetherRepoLocalStatus
#check m0387CompletionGateLeaves
#check m0387CompletionGateNote
#check deriv
#check HasDerivAt
#check fderiv
#check Flow
#check Flow.isInvariant_orbit

end S1_M_184
end Stage1
end AwesomeTheorems
