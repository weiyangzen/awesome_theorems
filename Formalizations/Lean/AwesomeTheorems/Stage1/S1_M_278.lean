import Mathlib.Probability.Moments.Variance

/-!
# S1-M-278 / THM-M-0998: Poincare inequality

This Stage1 artifact records a conservative Lean 4 boundary for the
probability-facing Poincare inequality: a variance upper bound controlled by a
Dirichlet/carre-du-champ energy.  The pinned mathlib snapshot contains strong
variance infrastructure and several checked variance upper bounds, but this
audit did not find a terminal theorem named as a Poincare inequality or a
spectral-gap/carre-du-champ package inside pinned mathlib.

The external primary-source pass did locate
`YuanheZ/lean-stat-learning-theory` theorem `gaussianPoincare` for the
standard one-dimensional Gaussian measure.  It is recorded here only as an
external anchor because that project uses a different Lean/mathlib stack and
has not been pinned, imported, or checked in this repository.

The declarations below therefore expose a precise statement-shape over an
abstract energy functional and locally wrap the checked mathlib variance
upper-bound anchors.  No full Poincare inequality is claimed here.
-/

noncomputable section

open MeasureTheory
open scoped MeasureTheory ProbabilityTheory ENNReal BigOperators

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_278

universe u

/--
Abstract Dirichlet/carre-du-champ energy for a real-valued observable.

For a concrete Poincare theorem this should later be instantiated by the
appropriate mathlib object: gradient energy, Markov-generator energy,
finite-state graph Dirichlet form, or another checked energy package.
-/
abbrev EnergyFunctional (Ω : Type u) : Type u :=
  (Ω → ℝ) → ℝ

/--
Concrete model selected for the next THM-M-0998 proof route.

The Stage1 route is the finite reversible Markov-chain Dirichlet form.  This is
deliberately narrower than manifold or Euclidean-gradient Poincare packages:
the local mathlib audit found variance infrastructure but no terminal geometric
Poincare theorem, while the finite-state model can be stated using checked
finite sums and gives the lowest-risk repo-local proof target.
-/
inductive ConcretePoincareModelChoice where
  | finiteReversibleMarkovChainDirichletForm
  deriving DecidableEq, Repr

/-- The selected concrete model for this Stage1 slot. -/
def intendedConcreteModel : ConcretePoincareModelChoice :=
  .finiteReversibleMarkovChainDirichletForm

/--
Finite reversible Markov-chain data for the selected concrete Poincare model.

The intended later specialization is the variance under the stationary
probability measure bounded by a constant times the Dirichlet form below.
This structure records only the stochastic and reversibility side conditions;
it does not assert the Poincare inequality itself.
-/
structure FiniteReversibleMarkovDirichletPackage (Ω : Type u) [Fintype Ω] where
  stationary : Ω → ℝ
  transition : Ω → Ω → ℝ
  stationary_nonneg : ∀ x, 0 ≤ stationary x
  stationary_sum_one : (∑ x : Ω, stationary x) = 1
  transition_nonneg : ∀ x y, 0 ≤ transition x y
  transition_sum_one : ∀ x, (∑ y : Ω, transition x y) = 1
  reversible :
    ∀ x y, stationary x * transition x y = stationary y * transition y x

/--
Dirichlet-form energy for a finite reversible Markov chain.

Mathematically this is `1/2 * sum_x sum_y pi x * K x y * (f y - f x)^2`.
-/
def finiteReversibleMarkovDirichletEnergy {Ω : Type u} [Fintype Ω]
    (pkg : FiniteReversibleMarkovDirichletPackage Ω) : EnergyFunctional Ω :=
  fun f => (1 / 2 : ℝ) *
    ∑ x : Ω, ∑ y : Ω,
      pkg.stationary x * pkg.transition x y * (f y - f x) ^ 2

/-- Definitional equation for the selected finite-chain Dirichlet energy. -/
theorem finiteReversibleMarkovDirichletEnergy_apply {Ω : Type u} [Fintype Ω]
    (pkg : FiniteReversibleMarkovDirichletPackage Ω) (f : Ω → ℝ) :
    finiteReversibleMarkovDirichletEnergy pkg f =
      (1 / 2 : ℝ) *
        ∑ x : Ω, ∑ y : Ω,
          pkg.stationary x * pkg.transition x y * (f y - f x) ^ 2 :=
  rfl

/--
Stationary expectation for the selected finite reversible Markov-chain model.

This avoids committing to a measure-construction API while giving the
finite-state proof route a concrete variance object over finite sums.
-/
def finiteReversibleMarkovStationaryExpectation {Ω : Type u} [Fintype Ω]
    (pkg : FiniteReversibleMarkovDirichletPackage Ω) (f : Ω → ℝ) : ℝ :=
  ∑ x : Ω, pkg.stationary x * f x

/-- Stationary finite-sum variance for the selected finite-chain model. -/
def finiteReversibleMarkovStationaryVariance {Ω : Type u} [Fintype Ω]
    (pkg : FiniteReversibleMarkovDirichletPackage Ω) (f : Ω → ℝ) : ℝ :=
  ∑ x : Ω,
    pkg.stationary x *
      (f x - finiteReversibleMarkovStationaryExpectation pkg f) ^ 2

/-- Constant observables have the expected stationary expectation. -/
theorem finiteReversibleMarkovStationaryExpectation_const {Ω : Type u} [Fintype Ω]
    (pkg : FiniteReversibleMarkovDirichletPackage Ω) (c : ℝ) :
    finiteReversibleMarkovStationaryExpectation pkg (fun _ : Ω => c) = c := by
  simp [finiteReversibleMarkovStationaryExpectation, ← Finset.sum_mul,
    pkg.stationary_sum_one]

/-- The stationary finite-sum variance is nonnegative. -/
theorem finiteReversibleMarkovStationaryVariance_nonneg {Ω : Type u} [Fintype Ω]
    (pkg : FiniteReversibleMarkovDirichletPackage Ω) (f : Ω → ℝ) :
    0 ≤ finiteReversibleMarkovStationaryVariance pkg f := by
  unfold finiteReversibleMarkovStationaryVariance
  exact Finset.sum_nonneg fun x _ =>
    mul_nonneg (pkg.stationary_nonneg x) (sq_nonneg _)

/-- Constant observables have zero stationary finite-sum variance. -/
theorem finiteReversibleMarkovStationaryVariance_const {Ω : Type u} [Fintype Ω]
    (pkg : FiniteReversibleMarkovDirichletPackage Ω) (c : ℝ) :
    finiteReversibleMarkovStationaryVariance pkg (fun _ : Ω => c) = 0 := by
  simp [finiteReversibleMarkovStationaryVariance,
    finiteReversibleMarkovStationaryExpectation_const]

/-- The selected finite-chain Dirichlet energy is nonnegative. -/
theorem finiteReversibleMarkovDirichletEnergy_nonneg {Ω : Type u} [Fintype Ω]
    (pkg : FiniteReversibleMarkovDirichletPackage Ω) (f : Ω → ℝ) :
    0 ≤ finiteReversibleMarkovDirichletEnergy pkg f := by
  unfold finiteReversibleMarkovDirichletEnergy
  apply mul_nonneg
  · norm_num
  · exact Finset.sum_nonneg fun x _ =>
      Finset.sum_nonneg fun y _ =>
        mul_nonneg
          (mul_nonneg (pkg.stationary_nonneg x) (pkg.transition_nonneg x y))
          (sq_nonneg _)

/-- Constant observables have zero selected finite-chain Dirichlet energy. -/
theorem finiteReversibleMarkovDirichletEnergy_const {Ω : Type u} [Fintype Ω]
    (pkg : FiniteReversibleMarkovDirichletPackage Ω) (c : ℝ) :
    finiteReversibleMarkovDirichletEnergy pkg (fun _ : Ω => c) = 0 := by
  simp [finiteReversibleMarkovDirichletEnergy]

/--
On a subsingleton finite state space, every observable has stationary
expectation equal to its value at the unique state.
-/
theorem finiteReversibleMarkovStationaryExpectation_eq_of_subsingleton
    {Ω : Type u} [Fintype Ω] [Subsingleton Ω]
    (pkg : FiniteReversibleMarkovDirichletPackage Ω) (f : Ω → ℝ) (x : Ω) :
    finiteReversibleMarkovStationaryExpectation pkg f = f x := by
  calc
    finiteReversibleMarkovStationaryExpectation pkg f =
        ∑ y : Ω, pkg.stationary y * f x := by
          unfold finiteReversibleMarkovStationaryExpectation
          exact Finset.sum_congr rfl fun y _ => by rw [Subsingleton.elim y x]
    _ = (∑ y : Ω, pkg.stationary y) * f x := by
          rw [Finset.sum_mul]
    _ = f x := by
          simp [pkg.stationary_sum_one]

/-- On a subsingleton finite state space, the stationary variance is zero. -/
theorem finiteReversibleMarkovStationaryVariance_eq_zero_of_subsingleton
    {Ω : Type u} [Fintype Ω] [Subsingleton Ω]
    (pkg : FiniteReversibleMarkovDirichletPackage Ω) (f : Ω → ℝ) :
    finiteReversibleMarkovStationaryVariance pkg f = 0 := by
  unfold finiteReversibleMarkovStationaryVariance
  apply Finset.sum_eq_zero
  intro x _
  rw [finiteReversibleMarkovStationaryExpectation_eq_of_subsingleton pkg f x]
  simp

/-- On a subsingleton finite state space, the Dirichlet energy is zero. -/
theorem finiteReversibleMarkovDirichletEnergy_eq_zero_of_subsingleton
    {Ω : Type u} [Fintype Ω] [Subsingleton Ω]
    (pkg : FiniteReversibleMarkovDirichletPackage Ω) (f : Ω → ℝ) :
    finiteReversibleMarkovDirichletEnergy pkg f = 0 := by
  unfold finiteReversibleMarkovDirichletEnergy
  have hsum :
      (∑ x : Ω, ∑ y : Ω,
        pkg.stationary x * pkg.transition x y * (f y - f x) ^ 2) = 0 := by
    apply Finset.sum_eq_zero
    intro x _
    apply Finset.sum_eq_zero
    intro y _
    have hxy : f y = f x := by rw [Subsingleton.elim y x]
    rw [hxy]
    simp
  simp [hsum]

/--
Pure finite-sum Poincare statement boundary for the selected model.

This is the concrete special-case target for the `S1-M-278-L020` through
`S1-M-278-L027` expansion.  It is still a predicate boundary, not a proof that
an arbitrary finite reversible chain has a particular spectral-gap constant.
-/
def FiniteReversibleMarkovChainPoincareStatement {Ω : Type u} [Fintype Ω]
    (pkg : FiniteReversibleMarkovDirichletPackage Ω) (C : ℝ) : Prop :=
  0 ≤ C ∧
    ∀ f : Ω → ℝ,
      finiteReversibleMarkovStationaryVariance pkg f ≤
        C * finiteReversibleMarkovDirichletEnergy pkg f

/-- Project the variance-energy bound from the pure finite-chain statement. -/
theorem finiteReversibleMarkovChainPoincareStatement_apply {Ω : Type u}
    [Fintype Ω] {pkg : FiniteReversibleMarkovDirichletPackage Ω} {C : ℝ}
    (h : FiniteReversibleMarkovChainPoincareStatement pkg C) (f : Ω → ℝ) :
    finiteReversibleMarkovStationaryVariance pkg f ≤
      C * finiteReversibleMarkovDirichletEnergy pkg f :=
  h.2 f

/-- Project nonnegativity of the constant from the pure finite-chain statement. -/
theorem finiteReversibleMarkovChainPoincareStatement_constant_nonneg {Ω : Type u}
    [Fintype Ω] {pkg : FiniteReversibleMarkovDirichletPackage Ω} {C : ℝ}
    (h : FiniteReversibleMarkovChainPoincareStatement pkg C) :
    0 ≤ C :=
  h.1

/--
Repo-local finite-state Poincare special case.

For a subsingleton state space every observable is constant, so both the
finite-sum stationary variance and the reversible-chain Dirichlet energy are
zero.  Hence the pure finite-chain Poincare statement holds for any
nonnegative constant `C`.
-/
theorem finiteReversibleMarkovChainPoincareStatement_of_subsingleton
    {Ω : Type u} [Fintype Ω] [Subsingleton Ω]
    (pkg : FiniteReversibleMarkovDirichletPackage Ω) {C : ℝ} (hC : 0 ≤ C) :
    FiniteReversibleMarkovChainPoincareStatement pkg C := by
  refine ⟨hC, ?_⟩
  intro f
  rw [finiteReversibleMarkovStationaryVariance_eq_zero_of_subsingleton pkg f,
    finiteReversibleMarkovDirichletEnergy_eq_zero_of_subsingleton pkg f]
  simp

/--
Predicate form of a probability Poincare inequality.

It states that every square-integrable real observable has variance bounded by
`C` times the chosen energy.  This is intentionally abstract: the present
mathlib audit did not locate a terminal theorem providing a canonical energy
object for this Stage1 slot.
-/
def PoincareInequality (Ω : Type u) [MeasurableSpace Ω]
    (μ : Measure Ω) (energy : EnergyFunctional Ω) (C : ℝ) : Prop :=
  IsProbabilityMeasure μ ∧ 0 ≤ C ∧
    ∀ X : Ω → ℝ, AEStronglyMeasurable X μ → MemLp X 2 μ →
      Var[X; μ] ≤ C * energy X

/--
Normalized Stage1 statement-shape candidate for the Poincare variance bound.

This is a `Prop` boundary, not a proof that an arbitrary measure and energy
satisfy the inequality.
-/
def StatementShape (Ω : Type u) [MeasurableSpace Ω]
    (μ : Measure Ω) (energy : EnergyFunctional Ω) (C : ℝ) : Prop :=
  PoincareInequality Ω μ energy C

/--
Selected concrete THM-M-0998 statement boundary.

This specializes the abstract statement shape to the finite reversible
Markov-chain Dirichlet energy.  It remains a predicate boundary: a future proof
must still connect `μ` to the stationary weights and prove the variance-energy
bound for a concrete spectral-gap/Poincare constant.
-/
def FiniteReversibleMarkovPoincareInequality (Ω : Type u) [Fintype Ω]
    [MeasurableSpace Ω] (μ : Measure Ω)
    (pkg : FiniteReversibleMarkovDirichletPackage Ω) (C : ℝ) : Prop :=
  PoincareInequality Ω μ (finiteReversibleMarkovDirichletEnergy pkg) C

/-- The statement-shape definition unfolds to the abstract variance-energy inequality. -/
theorem statementShape_iff (Ω : Type u) [MeasurableSpace Ω]
    (μ : Measure Ω) (energy : EnergyFunctional Ω) (C : ℝ) :
    StatementShape Ω μ energy C ↔
      IsProbabilityMeasure μ ∧ 0 ≤ C ∧
        ∀ X : Ω → ℝ, AEStronglyMeasurable X μ → MemLp X 2 μ →
          Var[X; μ] ≤ C * energy X :=
  Iff.rfl

/-- Project the variance bound from an abstract Poincare inequality certificate. -/
theorem poincareInequality_apply {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {energy : EnergyFunctional Ω} {C : ℝ}
    (h : PoincareInequality Ω μ energy C) (X : Ω → ℝ)
    (hX_meas : AEStronglyMeasurable X μ) (hX_l2 : MemLp X 2 μ) :
    Var[X; μ] ≤ C * energy X :=
  h.2.2 X hX_meas hX_l2

/--
Project the variance bound from the selected finite reversible Markov-chain
Poincare predicate.
-/
theorem finiteReversibleMarkovPoincareInequality_apply {Ω : Type u}
    [Fintype Ω] [MeasurableSpace Ω] {μ : Measure Ω}
    {pkg : FiniteReversibleMarkovDirichletPackage Ω} {C : ℝ}
    (h : FiniteReversibleMarkovPoincareInequality Ω μ pkg C) (X : Ω → ℝ)
    (hX_meas : AEStronglyMeasurable X μ) (hX_l2 : MemLp X 2 μ) :
    Var[X; μ] ≤ C * finiteReversibleMarkovDirichletEnergy pkg X :=
  poincareInequality_apply h X hX_meas hX_l2

/-- Project the probability-measure condition from an abstract Poincare certificate. -/
theorem poincareInequality_isProbability {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {energy : EnergyFunctional Ω} {C : ℝ}
    (h : PoincareInequality Ω μ energy C) :
    IsProbabilityMeasure μ :=
  h.1

/-- Project nonnegativity of the Poincare constant from the abstract certificate. -/
theorem poincareInequality_constant_nonneg {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {energy : EnergyFunctional Ω} {C : ℝ}
    (h : PoincareInequality Ω μ energy C) :
    0 ≤ C :=
  h.2.1

/-- Checked mathlib anchor: variance is bounded by the second moment. -/
theorem variance_le_expectation_sq_mathlib_wrapper {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} [IsProbabilityMeasure μ] {X : Ω → ℝ}
    (hX : AEStronglyMeasurable X μ) :
    Var[X; μ] ≤ μ[X ^ 2] :=
  ProbabilityTheory.variance_le_expectation_sq hX

/--
Checked mathlib anchor: Popoviciu's bounded-variable variance inequality.

This is a variance upper bound, but it is not the full Poincare
variance-energy theorem.
-/
theorem variance_le_sq_of_bounded_mathlib_wrapper {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} [IsProbabilityMeasure μ] {a b : ℝ} {X : Ω → ℝ}
    (hbound : ∀ᵐ ω ∂μ, X ω ∈ Set.Icc a b) (hX : AEMeasurable X μ) :
    Var[X; μ] ≤ ((b - a) / 2) ^ 2 :=
  ProbabilityTheory.variance_le_sq_of_bounded hbound hX

/-- Checked mathlib anchor: Bhatia-Davis variance inequality. -/
theorem variance_le_sub_mul_sub_mathlib_wrapper {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} [IsProbabilityMeasure μ] {a b : ℝ} {X : Ω → ℝ}
    (hbound : ∀ᵐ ω ∂μ, X ω ∈ Set.Icc a b) (hX : AEMeasurable X μ) :
    Var[X; μ] ≤ (b - μ[X]) * (μ[X] - a) :=
  ProbabilityTheory.variance_le_sub_mul_sub hbound hX

/-- Checked mathlib anchor: Chebyshev's inequality from variance. -/
theorem chebyshev_variance_mathlib_wrapper {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} [IsFiniteMeasure μ] {X : Ω → ℝ}
    (hX : MemLp X 2 μ) {c : ℝ} (hc : 0 < c) :
    μ {ω | c ≤ |X ω - μ[X]|} ≤ ENNReal.ofReal (Var[X; μ] / c ^ 2) :=
  ProbabilityTheory.meas_ge_le_variance_div_sq hX hc

/-- mathlib modules checked for this Stage1 slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.Moments.Variance",
  "Mathlib.Probability.Moments.Covariance",
  "Mathlib.Probability.StrongLaw",
  "Mathlib.Analysis.Calculus.Gradient.Basic",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality"
]

/-- Pinned declarations used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "ProbabilityTheory.variance",
  "ProbabilityTheory.evariance",
  "ProbabilityTheory.variance_le_expectation_sq",
  "ProbabilityTheory.variance_le_sq_of_bounded",
  "ProbabilityTheory.variance_le_sub_mul_sub",
  "ProbabilityTheory.meas_ge_le_variance_div_sq",
  "gradient",
  "MeasureTheory.MemLp"
]

/-- Repo-local declarations recording the concrete model decision. -/
def concreteModelDecisionNames : List String := [
  "ConcretePoincareModelChoice.finiteReversibleMarkovChainDirichletForm",
  "intendedConcreteModel",
  "FiniteReversibleMarkovDirichletPackage",
  "finiteReversibleMarkovDirichletEnergy",
  "finiteReversibleMarkovDirichletEnergy_apply",
  "finiteReversibleMarkovStationaryExpectation",
  "finiteReversibleMarkovStationaryVariance",
  "finiteReversibleMarkovStationaryExpectation_const",
  "finiteReversibleMarkovStationaryVariance_nonneg",
  "finiteReversibleMarkovStationaryVariance_const",
  "finiteReversibleMarkovDirichletEnergy_nonneg",
  "finiteReversibleMarkovDirichletEnergy_const",
  "finiteReversibleMarkovStationaryExpectation_eq_of_subsingleton",
  "finiteReversibleMarkovStationaryVariance_eq_zero_of_subsingleton",
  "finiteReversibleMarkovDirichletEnergy_eq_zero_of_subsingleton",
  "finiteReversibleMarkovChainPoincareStatement_of_subsingleton",
  "FiniteReversibleMarkovChainPoincareStatement",
  "finiteReversibleMarkovChainPoincareStatement_apply",
  "finiteReversibleMarkovChainPoincareStatement_constant_nonneg",
  "FiniteReversibleMarkovPoincareInequality",
  "finiteReversibleMarkovPoincareInequality_apply"
]

/--
Expanded `S1-M-278-L020` through `S1-M-278-L027` finite-chain leaf plan.

Each line is intended to be an independent `<=100` proof leaf or integration
leaf for the selected finite reversible Markov-chain Dirichlet-form route.
The terminal spectral-gap theorem remains open until a local proof body or a
repo-local pinned/imported dependency checks in this Lake closure.
-/
def finiteReversibleMarkovLeafPlan_L020_L027 : List String := [
  "S1-M-278-L020a: selected model is finite reversible Markov-chain Dirichlet form; checked by intendedConcreteModel",
  "S1-M-278-L020b: keep Euclidean-gradient and manifold Poincare branches out of the terminal route unless separately pinned",
  "S1-M-278-L021a: no Euclidean-gradient energy leaf is needed for this selected finite-chain branch",
  "S1-M-278-L021b: if a Gaussian or gradient proof is imported later, record it as a separate special-case branch with its own integration gate",
  "S1-M-278-L022a: checked finite package fields for stationary weights, transition rows, nonnegativity, row sums, and reversibility",
  "S1-M-278-L022b: checked finite Dirichlet energy definition and definitional apply lemma",
  "S1-M-278-L022c: checked stationary expectation and finite-sum variance definitions",
  "S1-M-278-L022d: checked constant-observable expectation, variance, and Dirichlet-energy sanity lemmas",
  "S1-M-278-L022e: checked nonnegativity leaves for finite-sum stationary variance and Dirichlet energy",
  "S1-M-278-L023a: define spectral-gap constant or Rayleigh quotient over nonconstant observables",
  "S1-M-278-L023b: prove the bridge from the chosen spectral-gap definition to stationary variance <= C times Dirichlet energy",
  "S1-M-278-L024a: prove/import terminal finite-chain Poincare theorem for the selected constant",
  "S1-M-278-L024b: verify terminal theorem locally with lake env lean before any completion claim",
  "S1-M-278-L025a: discharge nonnegativity and zero-energy constant-function side conditions",
  "S1-M-278-L025b: connect the pure finite-sum statement to the measure-based PoincareInequality boundary if needed",
  "S1-M-278-L026a: checked pure finite-chain Poincare statement boundary over finite sums",
  "S1-M-278-L026b: checked projections from the pure finite-chain Poincare statement",
  "S1-M-278-L027a0: checked subsingleton finite-state Poincare special case; every observable has zero stationary variance and zero Dirichlet energy",
  "S1-M-278-L027a: prove the finite-state special case from a checked spectral-gap/eigenvalue assumption or pin/import a compatible external proof",
  "S1-M-278-L027b: keep THM-M-0998 open if the only evidence is external_upstream_anchor_only or an unchecked spectral-gap argument"
]

/-- Search terms that did not locate a terminal Poincare inequality in local mathlib. -/
def absentTerminalSearchTerms : List String := [
  "Poincare inequality",
  "Poincare",
  "poincare",
  "spectral gap",
  "Dirichlet form variance",
  "carre du champ",
  "variance gradient",
  "Var energy"
]

/--
Primary external Lean 4 candidate found for a terminal Poincare inequality.

This is anchor metadata only.  The theorem has not been brought into the
repo-local Lake dependency closure, so it is not a completion witness for this
Stage1 slot.
-/
def externalTerminalCandidate : List String := [
  "repository=https://github.com/YuanheZ/lean-stat-learning-theory",
  "commit=4aaea15591360ccfffa1befdf0e7162f5af17f60",
  "lake_package=SLT",
  "module=SLT.GaussianPoincare.Limit",
  "theorem=gaussianPoincare",
  "statement=variance (fun x => f x) stdGaussianMeasure <= integral of (deriv f)^2 against stdGaussianMeasure",
  "placeholder_status=GaussianPoincare source subtree has no proof-placeholder or extra-trust hits in the audited commit",
  "lean_toolchain=leanprover/lean4:v4.27.0-rc1",
  "mathlib_dependency=d68c4dc09f5e000d3c968adae8def120a0758729",
  "license=not declared by GitHub license API and no root LICENSE file found",
  "import_feasibility=blocked until license is clarified and the Lean v4.27.0-rc1/mathlib stack is ported or isolated from this repo's v4.29.0/mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95 stack"
]

/--
Repo-local integration gate for the external terminal candidate.

This records the PUB-06 decision boundary: `gaussianPoincare` is a relevant
external Lean 4 theorem, but it has not been pinned, imported, or checked by
this repository.  The anchor is therefore not a completion witness.
-/
def externalTerminalIntegrationGate : List String := [
  "status=external_upstream_anchor_only",
  "repo_local_completion=no",
  "candidate=YuanheZ/lean-stat-learning-theory@4aaea15591360ccfffa1befdf0e7162f5af17f60:SLT.GaussianPoincare.Limit.gaussianPoincare",
  "blocker.lean_toolchain=this repo uses leanprover/lean4:v4.29.0 but upstream uses leanprover/lean4:v4.27.0-rc1",
  "blocker.mathlib=this repo pins mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95 but upstream pins d68c4dc09f5e000d3c968adae8def120a0758729",
  "blocker.license=GitHub reports no detected license and no root LICENSE file was found at the audited commit",
  "blocker.model=the external theorem is a one-dimensional Gaussian Poincare inequality, while the selected local route is finite reversible Markov-chain Dirichlet form",
  "required_for_completion=pin/import/check the external proof in this Lake closure, vendor a license-compatible proof body and check it locally, or prove the selected local theorem directly",
  "completion_claim=forbidden until a repo-local lake env lean validation passes for the terminal theorem or a concrete successor artifact"
]

/--
PUB-09 status gate for this Stage1 slot.

The public item must remain open until all four gates below are closed in the
same serialized integration pass.  This declaration is checked metadata, not a
proof of the terminal Poincare inequality.
-/
def publicStage1OpenGate_PUB09 : List String := [
  "terminal_theorem_gate=open: no repo-local terminal proof of PoincareInequality or the selected finite-chain spectral-gap theorem has been checked",
  "public_merge_back_gate=open: Docs/Stage1_Blueprint.md, Docs/todos_20260430.md, and README.md are reserved for a later serialized integrator pass",
  "local_validation_gate=required: rerun cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_278.lean after every Lean edit",
  "status_synchronization_gate=open: public checklist, todo, and README status must not be upgraded before terminal validation and merge-back",
  "public_stage1_item_status=keep_open"
]

/--
PUB-10 public synchronization plan for the serialized integrator pass.

This records the child-task boundary in the checked Lean artifact: parallel
workers may prepare evidence and private ledgers, but public planning surfaces
must be synchronized only by a later serialized integrator after the completion
gates are actually satisfied.
-/
def publicBackfillPlan_PUB10 : List String := [
  "scope=public-doc integration plan only",
  "do_not_edit=Docs/Stage1_Blueprint.md, Docs/todos_20260430.md, README.md during parallel child worker pass",
  "integrator_trigger=after terminal theorem, public merge-back, local validation, and status synchronization gates are satisfied",
  "required_command=cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_278.lean",
  "current_action=keep S1-M-278-PUB-10 open and provide exact backfill text in the private child ledger",
  "completion_claim=forbidden while the terminal theorem remains not_repo_local_closed or only external_upstream_anchor_only"
]

/-! ## Audit probes retained in the checked file. -/

#check StatementShape
#check PoincareInequality
#check poincareInequality_apply
#check intendedConcreteModel
#check FiniteReversibleMarkovDirichletPackage
#check finiteReversibleMarkovDirichletEnergy
#check finiteReversibleMarkovDirichletEnergy_apply
#check finiteReversibleMarkovStationaryExpectation
#check finiteReversibleMarkovStationaryVariance
#check finiteReversibleMarkovStationaryExpectation_const
#check finiteReversibleMarkovStationaryVariance_nonneg
#check finiteReversibleMarkovStationaryVariance_const
#check finiteReversibleMarkovDirichletEnergy_nonneg
#check finiteReversibleMarkovDirichletEnergy_const
#check finiteReversibleMarkovStationaryExpectation_eq_of_subsingleton
#check finiteReversibleMarkovStationaryVariance_eq_zero_of_subsingleton
#check finiteReversibleMarkovDirichletEnergy_eq_zero_of_subsingleton
#check finiteReversibleMarkovChainPoincareStatement_of_subsingleton
#check FiniteReversibleMarkovChainPoincareStatement
#check finiteReversibleMarkovChainPoincareStatement_apply
#check finiteReversibleMarkovChainPoincareStatement_constant_nonneg
#check FiniteReversibleMarkovPoincareInequality
#check finiteReversibleMarkovPoincareInequality_apply
#check variance_le_expectation_sq_mathlib_wrapper
#check variance_le_sq_of_bounded_mathlib_wrapper
#check variance_le_sub_mul_sub_mathlib_wrapper
#check chebyshev_variance_mathlib_wrapper
#check ProbabilityTheory.variance_le_expectation_sq
#check ProbabilityTheory.variance_le_sq_of_bounded
#check ProbabilityTheory.variance_le_sub_mul_sub
#check ProbabilityTheory.meas_ge_le_variance_div_sq
#check externalTerminalCandidate
#check externalTerminalIntegrationGate
#check finiteReversibleMarkovLeafPlan_L020_L027
#check publicStage1OpenGate_PUB09
#check publicBackfillPlan_PUB10

end S1_M_278
end Stage1
end AwesomeTheorems
