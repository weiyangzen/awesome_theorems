import Mathlib.Topology.MetricSpace.Basic
import Mathlib.Topology.Semicontinuity.Basic

/-!
# S1-M-163 / THM-M-1270: Ekeland variational principle

This Stage1 artifact records a conservative Lean 4 statement boundary for the
real-valued complete-metric-space form of Ekeland's variational principle.

The pinned mathlib snapshot has complete metric spaces, lower semicontinuity,
bounded-below real ranges, distances, and compact lower-semicontinuous minimizer
anchors.  This audit did not find a terminal `Ekeland` or `Caristi` theorem in
the local mathlib dependency closure.

The declarations below therefore avoid proof placeholders and false completion
claims.  They normalize the expected Ekeland interface and include only small
checked wrappers around available mathlib facts.
-/

noncomputable section

open Set

namespace AwesomeTheorems.Stage1.S1_M_163

universe u

/--
`x0` is an `ε`-approximate minimizer for a real-valued function.

This formulation is equivalent to `f x0 ≤ inf f + ε` when the infimum is
available as an order-theoretic object, but it avoids committing the terminal
Ekeland statement to one particular `sInf` API shape.
-/
def ApproximateMinimizer {X : Type u} (f : X → ℝ) (ε : ℝ) (x0 : X) : Prop :=
  ∀ x : X, f x0 ≤ f x + ε

/--
Infimum-based approximate minimizer surface:
`f x0 ≤ sInf (range f) + ε`.

This is the reader-standard Ekeland hypothesis.  The public Stage1 statement
can keep the direct pointwise `ApproximateMinimizer` predicate as its canonical
Lean-facing input because the bridge below proves equivalence under the existing
`BddBelow (range f)` hypothesis.
-/
def InfimumApproximateMinimizer {X : Type u} (f : X → ℝ) (ε : ℝ) (x0 : X) :
    Prop :=
  f x0 ≤ sInf (range f) + ε

/--
Under the bounded-below hypothesis already present in `StatementShape`, the
pointwise approximate-minimizer predicate is equivalent to the conventional
`sInf (range f)` formulation.
-/
theorem approximateMinimizer_iff_infimumApproximateMinimizer
    {X : Type u} {f : X → ℝ} {ε : ℝ} {x0 : X}
    (hbdd : BddBelow (range f)) :
    ApproximateMinimizer f ε x0 ↔ InfimumApproximateMinimizer f ε x0 := by
  constructor
  · intro h
    have hlower : f x0 - ε ≤ sInf (range f) := by
      refine le_csInf ?hne ?hlb
      · exact ⟨f x0, ⟨x0, rfl⟩⟩
      · intro y hy
        rcases hy with ⟨x, rfl⟩
        linarith [h x]
    dsimp [InfimumApproximateMinimizer]
    linarith
  · intro h x
    dsimp [InfimumApproximateMinimizer] at h
    have hinf_le : sInf (range f) ≤ f x := csInf_le hbdd ⟨x, rfl⟩
    linarith

/-- Convert the conventional infimum surface to the canonical pointwise one. -/
theorem ApproximateMinimizer.of_infimum
    {X : Type u} {f : X → ℝ} {ε : ℝ} {x0 : X}
    (hbdd : BddBelow (range f))
    (h : InfimumApproximateMinimizer f ε x0) :
    ApproximateMinimizer f ε x0 :=
  (approximateMinimizer_iff_infimumApproximateMinimizer hbdd).mpr h

/-- Convert the canonical pointwise surface to the conventional infimum one. -/
theorem ApproximateMinimizer.to_infimum
    {X : Type u} {f : X → ℝ} {ε : ℝ} {x0 : X}
    (hbdd : BddBelow (range f))
    (h : ApproximateMinimizer f ε x0) :
    InfimumApproximateMinimizer f ε x0 :=
  (approximateMinimizer_iff_infimumApproximateMinimizer hbdd).mp h

/-- The penalized functional used in the strict-minimality conclusion. -/
def PerturbedFunctional {X : Type u} [PseudoMetricSpace X]
    (f : X → ℝ) (slope : ℝ) (v : X) (x : X) : ℝ :=
  f x + slope * dist v x

/--
The usual Ekeland conclusion for a chosen approximate minimizer `x0`, tolerance
`ε`, and displacement parameter `λ`.

It asserts existence of a nearby point `v` with no larger value and strict
minimality for the distance-penalized functional
`x ↦ f x + (ε / λ) * dist v x`.
-/
def EkelandConclusion {X : Type u} [PseudoMetricSpace X]
    (f : X → ℝ) (ε η : ℝ) (x0 : X) : Prop :=
  ∃ v : X,
    f v ≤ f x0 ∧
      dist v x0 ≤ η ∧
        ∀ y : X, y ≠ v → f v < f y + (ε / η) * dist v y

/--
One step in the Brøndsted/Ekeland descent preorder.

`DescentStep f slope x y` means that moving from `x` to `y` does not increase
the distance-penalized value measured from `x`.
-/
def DescentStep {X : Type u} [PseudoMetricSpace X]
    (f : X → ℝ) (slope : ℝ) (x y : X) : Prop :=
  f y + slope * dist x y ≤ f x

/-- The one-step descent preorder is reflexive. -/
theorem descentStep_self {X : Type u} [PseudoMetricSpace X]
    (f : X → ℝ) (slope : ℝ) (x : X) :
    DescentStep f slope x x := by
  simp [DescentStep]

/--
For a nonnegative slope, one descent step cannot increase the underlying
function value.
-/
theorem DescentStep.value_le {X : Type u} [PseudoMetricSpace X]
    {f : X → ℝ} {slope : ℝ} {x y : X}
    (h : DescentStep f slope x y) (hslope : 0 ≤ slope) :
    f y ≤ f x := by
  dsimp [DescentStep] at h
  have hpenalty : 0 ≤ slope * dist x y := mul_nonneg hslope dist_nonneg
  linarith [h, hpenalty]

/-- A descent step bounds the penalized distance by the value drop. -/
theorem DescentStep.penalty_le_drop {X : Type u} [PseudoMetricSpace X]
    {f : X → ℝ} {slope : ℝ} {x y : X}
    (h : DescentStep f slope x y) :
    slope * dist x y ≤ f x - f y := by
  dsimp [DescentStep] at h
  linarith [h]

/--
In a genuine metric space, a nontrivial descent step with positive slope
strictly decreases the function value.
-/
theorem DescentStep.value_lt_of_ne {X : Type u} [MetricSpace X]
    {f : X → ℝ} {slope : ℝ} {x y : X}
    (h : DescentStep f slope x y) (hslope : 0 < slope) (hyx : y ≠ x) :
    f y < f x := by
  dsimp [DescentStep] at h
  have hdist : 0 < dist x y := dist_pos.mpr (by
    intro hxy
    exact hyx hxy.symm)
  have hpenalty : 0 < slope * dist x y := mul_pos hslope hdist
  linarith [h, hpenalty]

/-- A sequence whose adjacent terms follow the descent preorder. -/
def DescentChain {X : Type u} [PseudoMetricSpace X]
    (f : X → ℝ) (slope : ℝ) (c : ℕ → X) : Prop :=
  ∀ n : ℕ, DescentStep f slope (c n) (c (n + 1))

/-- A descent chain with a specified starting point. -/
def DescentChainFrom {X : Type u} [PseudoMetricSpace X]
    (f : X → ℝ) (slope : ℝ) (x0 : X) (c : ℕ → X) : Prop :=
  c 0 = x0 ∧ DescentChain f slope c

/--
The maximal point delivered by a descent/chain construction before unwrapping
it into the usual strict Ekeland conclusion.
-/
def DescentMaximalPoint {X : Type u} [PseudoMetricSpace X]
    (f : X → ℝ) (ε η : ℝ) (x0 v : X) : Prop :=
  f v ≤ f x0 ∧
    dist v x0 ≤ η ∧
      ∀ y : X, DescentStep f (ε / η) v y → y = v

/--
Complete-metric descent/chain package expected from the hard Ekeland proof
core: a started descent chain, a Cauchy/limit witness, and a maximal descent
point.  This is an interface for the missing construction, not a proof that the
construction always exists.
-/
def CompleteMetricDescentChainPackage {X : Type u} [MetricSpace X]
    [CompleteSpace X] (f : X → ℝ) (ε η : ℝ) (x0 : X) : Prop :=
  ∃ (c : ℕ → X) (v : X),
    DescentChainFrom f (ε / η) x0 c ∧
      CauchySeq c ∧
        Filter.Tendsto c Filter.atTop (nhds v) ∧
          DescentMaximalPoint f ε η x0 v

/--
A maximal descent point is exactly the package-level object needed to recover
the strict penalized-minimality component of Ekeland's conclusion.
-/
theorem DescentMaximalPoint.to_conclusion
    {X : Type u} [PseudoMetricSpace X]
    {f : X → ℝ} {ε η : ℝ} {x0 v : X}
    (h : DescentMaximalPoint f ε η x0 v) :
    f v ≤ f x0 ∧
      dist v x0 ≤ η ∧
        ∀ y : X, y ≠ v → f v < f y + (ε / η) * dist v y := by
  rcases h with ⟨hv, hvdist, hmax⟩
  refine ⟨hv, hvdist, ?_⟩
  intro y hy
  by_contra hnot
  exact hy (hmax y (not_lt.mp hnot))

/--
The maximal-descent formulation gives the strict minimality of the named
distance-penalized functional centered at `v`.
-/
theorem DescentMaximalPoint.strict_penalizedMinimality
    {X : Type u} [PseudoMetricSpace X]
    {f : X → ℝ} {ε η : ℝ} {x0 v : X}
    (h : DescentMaximalPoint f ε η x0 v) :
    ∀ y : X, y ≠ v →
      PerturbedFunctional f (ε / η) v v <
        PerturbedFunctional f (ε / η) v y := by
  intro y hy
  simpa [PerturbedFunctional] using h.to_conclusion.2.2 y hy

/-- An existing maximal descent point produces the normalized Ekeland conclusion. -/
theorem DescentMaximalPoint.to_ekelandConclusion
    {X : Type u} [PseudoMetricSpace X]
    {f : X → ℝ} {ε η : ℝ} {x0 v : X}
    (h : DescentMaximalPoint f ε η x0 v) :
    EkelandConclusion f ε η x0 := by
  exact ⟨v, h.to_conclusion⟩

/--
If the hard complete-metric chain package has been constructed, it unwraps to
the Stage1 Ekeland conclusion.
-/
theorem CompleteMetricDescentChainPackage.to_ekelandConclusion
    {X : Type u} [MetricSpace X] [CompleteSpace X]
    {f : X → ℝ} {ε η : ℝ} {x0 : X}
    (h : CompleteMetricDescentChainPackage f ε η x0) :
    EkelandConclusion f ε η x0 := by
  rcases h with ⟨c, v, hstart, hcauchy, hlim, hmax⟩
  exact hmax.to_ekelandConclusion

/--
Normalized Stage1 statement shape for Ekeland's variational principle.

For every complete metric space and every lower-semicontinuous real-valued
bounded-below function, every positive-accuracy approximate minimizer admits an
Ekeland point.  The hard content is the final implication; no terminal Lean 4
proof of that implication was found in the local dependency closure.
-/
def StatementShape : Prop :=
  ∀ (X : Type u) [MetricSpace X] [CompleteSpace X]
    (f : X → ℝ) (ε η : ℝ) (x0 : X),
    LowerSemicontinuous f →
      BddBelow (range f) →
        0 < ε →
          0 < η →
            ApproximateMinimizer f ε x0 →
              EkelandConclusion f ε η x0

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (X : Type u) [MetricSpace X] [CompleteSpace X]
      (f : X → ℝ) (ε η : ℝ) (x0 : X),
      LowerSemicontinuous f →
        BddBelow (range f) →
          0 < ε →
            0 < η →
              ApproximateMinimizer f ε x0 →
                EkelandConclusion f ε η x0) :
    StatementShape.{u} :=
  by
    simpa [StatementShape] using h

/--
Conditional repo-local exposure wrapper for the terminal Ekeland theorem.

This theorem does not prove `StatementShape`; it only fixes the theorem-shaped
entry point that a future local proof body or pinned upstream proof can feed.
-/
theorem ekeland_variational_principle_from_statementShape
    (h : StatementShape.{u})
    (X : Type u) [MetricSpace X] [CompleteSpace X]
    (f : X → ℝ) (ε η : ℝ) (x0 : X)
    (hf : LowerSemicontinuous f)
    (hbdd : BddBelow (range f))
    (hε : 0 < ε)
    (hη : 0 < η)
    (happrox : ApproximateMinimizer f ε x0) :
    EkelandConclusion f ε η x0 := by
  exact h X f ε η x0 hf hbdd hε hη happrox

/--
If the missing complete-metric proof core is supplied, the normalized
statement shape follows by the checked descent-package bridge.
-/
theorem StatementShape.of_completeMetricDescentChainPackage
    (h : ∀ (X : Type u) [MetricSpace X] [CompleteSpace X]
      (f : X → ℝ) (ε η : ℝ) (x0 : X),
      LowerSemicontinuous f →
        BddBelow (range f) →
          0 < ε →
            0 < η →
              ApproximateMinimizer f ε x0 →
                CompleteMetricDescentChainPackage f ε η x0) :
    StatementShape.{u} := by
  refine StatementShape.intro ?_
  intro X _ _ f ε η x0 hf hbdd hε hη happrox
  exact (h X f ε η x0 hf hbdd hε hη happrox).to_ekelandConclusion

/-- The perturbation term vanishes at its center. -/
theorem perturbedFunctional_self {X : Type u} [PseudoMetricSpace X]
    (f : X → ℝ) (slope : ℝ) (v : X) :
    PerturbedFunctional f slope v v = f v := by
  simp [PerturbedFunctional]

/--
The strict Ekeland conclusion can be read as strict minimization of the
penalized functional centered at the selected point.
-/
theorem EkelandConclusion.exists_strict_minimizer
    {X : Type u} [PseudoMetricSpace X]
    {f : X → ℝ} {ε η : ℝ} {x0 : X}
    (h : EkelandConclusion f ε η x0) :
    ∃ v : X,
      f v ≤ f x0 ∧
        dist v x0 ≤ η ∧
          ∀ y : X, y ≠ v →
            PerturbedFunctional f (ε / η) v v <
              PerturbedFunctional f (ε / η) v y := by
  rcases h with ⟨v, hv, hvdist, hvstrict⟩
  refine ⟨v, hv, hvdist, ?_⟩
  intro y hy
  simpa [PerturbedFunctional] using hvstrict y hy

/-- An exact global minimizer is an approximate minimizer at any nonnegative tolerance. -/
theorem approximateMinimizer_of_global_min
    {X : Type u} {f : X → ℝ} {ε : ℝ} {x0 : X}
    (hmin : ∀ x : X, f x0 ≤ f x) (hε : 0 ≤ ε) :
    ApproximateMinimizer f ε x0 := by
  intro x
  exact (hmin x).trans (le_add_of_nonneg_right hε)

/-- Increasing the tolerance preserves the approximate-minimizer condition. -/
theorem ApproximateMinimizer.mono
    {X : Type u} {f : X → ℝ} {ε δ : ℝ} {x0 : X}
    (h : ApproximateMinimizer f ε x0) (hεδ : ε ≤ δ) :
    ApproximateMinimizer f δ x0 := by
  intro x
  exact (h x).trans (by simpa [add_comm] using add_le_add_left hεδ (f x))

/-- A continuous real-valued function is lower semicontinuous. -/
theorem continuous_lowerSemicontinuous_anchor
    {X : Type u} [TopologicalSpace X] {f : X → ℝ}
    (hf : Continuous f) :
    LowerSemicontinuous f :=
  hf.lowerSemicontinuous

/--
Checked mathlib anchor: a lower-semicontinuous function attains a minimum on a
nonempty compact set.
-/
theorem compact_lowerSemicontinuous_exists_minimizer_anchor
    {X : Type u} [TopologicalSpace X] {s : Set X} {f : X → ℝ}
    (hne : s.Nonempty) (hs : IsCompact s) (hf : LowerSemicontinuousOn f s) :
    ∃ a ∈ s, ∀ x ∈ s, f a ≤ f x := by
  rcases LowerSemicontinuousOn.exists_isMinOn hne hs hf with ⟨a, ha, hmin⟩
  exact ⟨a, ha, isMinOn_iff.mp hmin⟩

/-- mathlib modules checked while locating repo-local anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Topology.MetricSpace.Basic",
  "Mathlib.Topology.Semicontinuity.Defs",
  "Mathlib.Topology.Semicontinuity.Basic",
  "Mathlib.Order.Filter.Extr",
  "Mathlib.Data.Real.Archimedean"
]

/-- Checked local names used as anchors for the statement-shape boundary. -/
def mathlibAnchorNames : List String := [
  "MetricSpace",
  "PseudoMetricSpace",
  "CompleteSpace",
  "dist",
  "dist_self",
  "dist_nonneg",
  "LowerSemicontinuous",
  "LowerSemicontinuousOn",
  "Continuous.lowerSemicontinuous",
  "LowerSemicontinuous.lowerSemicontinuousOn",
  "LowerSemicontinuousOn.exists_isMinOn",
  "IsMinOn",
  "isMinOn_iff",
  "BddBelow",
  "Real.exists_isGLB",
  "Real.isGLB_sInf"
]

/--
Search terms that did not locate a terminal Ekeland/Caristi variational
principle theorem in pinned mathlib.
-/
def absentTerminalSearchTerms : List String := [
  "Ekeland",
  "Caristi",
  "VariationalPrinciple",
  "variational principle",
  "approximate minimizer",
  "epsilon minimizer",
  "strict perturbed minimizer"
]

/--
External Lean 4 primary-source search queries required before this Stage1 slot
can claim that no upstream Ekeland proof exists.

The child audit on 2026-05-01 found that authenticated GitHub code search was
not available in this local environment (`gh auth status` reported no login and
`GH_TOKEN`/`GITHUB_TOKEN` were unset), while unauthenticated GitHub code-search
API probes were rate-limited.  These strings are therefore a checked local audit
record, not evidence of a completed external proof search.
-/
def externalPrimarySourceSearchQueries : List String := [
  "Ekeland language:Lean",
  "Caristi language:Lean",
  "VariationalPrinciple language:Lean",
  "\"variational principle\" language:Lean",
  "\"approximate minimizer\" language:Lean",
  "\"epsilon minimizer\" language:Lean",
  "\"strict perturbed minimizer\" language:Lean"
]

/-- Concrete blockers preventing a completed authenticated external-source audit. -/
def externalPrimarySourceSearchBlockers : List String := [
  "GitHub CLI is installed but not authenticated on this machine.",
  "GH_TOKEN and GITHUB_TOKEN are unset in the validation shell.",
  "Unauthenticated GitHub code-search API requests returned rate-limit responses.",
  "grep.app API requests for the same Lean-language terms returned HTTP 503."
]

/-!
## M0387 merge/audit surface

The following string-valued declarations are deliberately non-theorem metadata.
They give the public backfill integrator a compiled, repo-local anchor for the
verified child leaves and the still-open M0387 gates without upgrading the full
Ekeland principle to a completed theorem.
-/

/--
Repo-local Lean declarations that have proof bodies in this file and passed the
Stage1 per-file validation command.
-/
def checkedLocalLeafNames : List String := [
  "S1-M-163.L001.statement_shape_def: StatementShape",
  "S1-M-163.L002.statement_shape_intro: StatementShape.intro",
  "S1-M-163.L003.infimum_bridge: approximateMinimizer_iff_infimumApproximateMinimizer",
  "S1-M-163.L004.infimum_to_pointwise: ApproximateMinimizer.of_infimum",
  "S1-M-163.L005.pointwise_to_infimum: ApproximateMinimizer.to_infimum",
  "S1-M-163.L006.descent_step_self: descentStep_self",
  "S1-M-163.L007.descent_step_value_le: DescentStep.value_le",
  "S1-M-163.L008.descent_step_penalty_le_drop: DescentStep.penalty_le_drop",
  "S1-M-163.L009.descent_step_value_lt_of_ne: DescentStep.value_lt_of_ne",
  "S1-M-163.L010.maximal_point_to_conclusion: DescentMaximalPoint.to_conclusion",
  "S1-M-163.L011.strict_penalized_minimality: DescentMaximalPoint.strict_penalizedMinimality",
  "S1-M-163.L012.maximal_point_to_ekelandConclusion: DescentMaximalPoint.to_ekelandConclusion",
  "S1-M-163.L013.chain_package_to_ekelandConclusion: CompleteMetricDescentChainPackage.to_ekelandConclusion",
  "S1-M-163.L014.statement_from_chain_package: StatementShape.of_completeMetricDescentChainPackage",
  "S1-M-163.L015.perturbed_self: perturbedFunctional_self",
  "S1-M-163.L016.ekelandConclusion_exists_strict_minimizer: EkelandConclusion.exists_strict_minimizer",
  "S1-M-163.L017.exact_global_min_to_approx: approximateMinimizer_of_global_min",
  "S1-M-163.L018.approximate_minimizer_mono: ApproximateMinimizer.mono",
  "S1-M-163.L019.continuous_lsc_anchor: continuous_lowerSemicontinuous_anchor",
  "S1-M-163.L020.compact_lsc_min_anchor: compact_lowerSemicontinuous_exists_minimizer_anchor"
]

/--
Open M0387-level child leaves for the full theorem.  These are intentionally
tasks, not completed proof leaves.
-/
def openM0387ChildLeaves : List String := [
  "S1-M-163.U001: rerun authenticated external Lean 4 primary-source search for Ekeland/Caristi and strict perturbed minimizer variants.",
  "S1-M-163.U002: prove the complete-metric descent or maximal-chain construction that produces DescentMaximalPoint.",
  "S1-M-163.U003: prove StatementShape by supplying StatementShape.of_completeMetricDescentChainPackage with a local proof body.",
  "S1-M-163.U004: if a terminal external Lean 4 proof is found, pin/import/check it or record a concrete integration blocker before any completion claim.",
  "S1-M-163.U005: serially merge the theorem-tree, machine-anchor audit, and <=100-step leaf ledger into the public Stage1 blueprint/todo surfaces."
]

/--
M0387 repo-local debt gate for this artifact: no completed state is claimed.
The remaining parent status is formalization debt, plus an authenticated-search
blocker, not a completed theorem with residual repo-local integration debt.
-/
def repoLocalIntegrationDebtGate : String :=
  "pass-for-open-state: no completed state retains repo_local_integration_debt; S1-M-163 remains not_repo_local_closed/formalization_debt until a terminal local proof body or pinned upstream dependency passes repo-local validation."

/-! ## Audit probes -/

#check ApproximateMinimizer
#check InfimumApproximateMinimizer
#check approximateMinimizer_iff_infimumApproximateMinimizer
#check ApproximateMinimizer.of_infimum
#check ApproximateMinimizer.to_infimum
#check PerturbedFunctional
#check EkelandConclusion
#check DescentStep
#check descentStep_self
#check DescentStep.value_le
#check DescentStep.penalty_le_drop
#check DescentStep.value_lt_of_ne
#check DescentChain
#check DescentChainFrom
#check DescentMaximalPoint
#check CompleteMetricDescentChainPackage
#check DescentMaximalPoint.to_conclusion
#check DescentMaximalPoint.strict_penalizedMinimality
#check DescentMaximalPoint.to_ekelandConclusion
#check CompleteMetricDescentChainPackage.to_ekelandConclusion
#check StatementShape
#check ekeland_variational_principle_from_statementShape
#check StatementShape.of_completeMetricDescentChainPackage
#check perturbedFunctional_self
#check EkelandConclusion.exists_strict_minimizer
#check approximateMinimizer_of_global_min
#check ApproximateMinimizer.mono
#check continuous_lowerSemicontinuous_anchor
#check compact_lowerSemicontinuous_exists_minimizer_anchor
#check LowerSemicontinuous
#check LowerSemicontinuousOn.exists_isMinOn
#check CompleteSpace
#check BddBelow
#check externalPrimarySourceSearchQueries
#check externalPrimarySourceSearchBlockers
#check checkedLocalLeafNames
#check openM0387ChildLeaves
#check repoLocalIntegrationDebtGate

end AwesomeTheorems.Stage1.S1_M_163
