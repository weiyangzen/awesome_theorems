import Mathlib.MeasureTheory.Function.ConvergenceInDistribution
import Mathlib.MeasureTheory.Measure.LevyConvergence
import Mathlib.Analysis.InnerProductSpace.PiL2

/-!
# S1-M-292 / THM-M-1013: Cramer-Wold theorem

This Stage1 file records a Lean 4 statement boundary for the Cramer-Wold theorem:
weak convergence of finite-dimensional laws is characterized by weak convergence of
all one-dimensional linear projections.

The hard converse is intentionally represented as a `Prop` statement shape.  The
locally checked wrappers
`projection_tendsto_of_probabilityMeasure_tendsto` and
`projection_tendstoInDistribution_of_vector` cover the easy direction supplied
by mathlib's continuous mapping theorem for convergence in distribution and
probability measures.  The local bridge
`charFun_tendsto_of_projection_tendsto` converts convergence of every scalar
projection into pointwise convergence of finite-dimensional characteristic
functions, and `measureStatementShape_of_projection_tendsto` closes the
measure-level hard direction by Lévy's convergence theorem.  The theorem
`statementShape_of_projection_tendstoInDistribution` then closes the normalized
finite-dimensional random-variable statement used by this Stage1 slot.  This is
still not a public completion claim for every Cramer-Wold formulation until the
Stage1 public surfaces, theorem-tree leaves, and integration gates are synced.

Local mathlib audit at revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:
`TendstoInDistribution`, `ProbabilityMeasure`,
`ProbabilityMeasure.tendsto_map_of_tendsto_of_continuous`,
`ProbabilityMeasure.tendsto_iff_tendsto_charFun`, `charFun`,
`Measure.ext_of_charFun`, and `Measure.ext_of_charFunDual` are present.  A
local search for `CramerWold`, `cramer_wold`, `CramérWold`, and `Cramer-Wold`
found no direct Cramer-Wold theorem in mathlib.
-/

open Filter MeasureTheory
open scoped Topology

namespace AwesomeTheorems.Stage1.S1_M_292

noncomputable section

universe u v

/-- The finite-dimensional real state space used for this Stage1 normalization. -/
abbrev Vector (d : ℕ) := EuclideanSpace ℝ (Fin d)

/-- One-dimensional linear projection along `t`. -/
def projection {d : ℕ} (t : Vector d) (x : Vector d) : ℝ :=
  inner ℝ x t

/-- The Cramer-Wold test functions are continuous. -/
lemma continuous_projection {d : ℕ} (t : Vector d) : Continuous (projection t) := by
  unfold projection
  exact continuous_id.inner continuous_const

/-- The Cramer-Wold projection along the `i`-th standard vector is the `i`-th coordinate. -/
lemma projection_single_one {d : ℕ} (i : Fin d) (x : Vector d) :
    projection (EuclideanSpace.single i (1 : ℝ)) x = x i := by
  unfold projection
  simpa using (EuclideanSpace.inner_single_right (𝕜 := ℝ) i (1 : ℝ) x)

/--
If all Cramer-Wold scalar projections of a vector-valued random variable are
almost everywhere measurable, then the vector-valued random variable itself is
almost everywhere measurable.
-/
lemma aemeasurable_vector_of_projection {d : ℕ} {Ω : Type u} [MeasurableSpace Ω]
    {μ : Measure Ω} {X : Ω → Vector d}
    (h : ∀ t : Vector d, AEMeasurable (fun ω ↦ projection t (X ω)) μ) :
    AEMeasurable X μ := by
  let Y : Ω → (Fin d → ℝ) := fun ω i ↦ X ω i
  have hY : AEMeasurable Y μ := by
    refine aemeasurable_pi_lambda Y fun i ↦ ?_
    simpa [Y, projection_single_one] using h (EuclideanSpace.single i (1 : ℝ))
  have hY' :
      AEMeasurable
        (fun ω ↦ (PiLp.continuousLinearEquiv 2 ℝ (fun _ : Fin d ↦ ℝ)).symm (Y ω))
        μ :=
    (PiLp.continuousLinearEquiv 2 ℝ (fun _ : Fin d ↦ ℝ)).symm.continuous.measurable
      |>.comp_aemeasurable hY
  simpa [Y, PiLp.coe_symm_continuousLinearEquiv] using hY'

/--
Measure-level Cramer-Wold statement shape.

If every one-dimensional projection of `μ n` converges weakly to the corresponding
projection of `μ0`, then the finite-dimensional probability measures themselves
converge weakly.  The checked theorem
`measureStatementShape_of_projection_tendsto` proves this measure-level hard
direction in this Stage1 artifact.
-/
def MeasureStatementShape (d : ℕ) (μ : ℕ → ProbabilityMeasure (Vector d))
    (μ0 : ProbabilityMeasure (Vector d)) : Prop :=
  (∀ t : Vector d,
      Tendsto
        (fun n ↦ (μ n).map ((continuous_projection t).measurable.aemeasurable))
        atTop
        (𝓝 (μ0.map ((continuous_projection t).measurable.aemeasurable)))) →
    Tendsto μ atTop (𝓝 μ0)

/--
Random-variable Cramer-Wold statement shape using mathlib's
`TendstoInDistribution`.

This version keeps the probability spaces explicit and states that convergence in
distribution of all scalar projections implies convergence in distribution of the
vector-valued random variables.
-/
def StatementShape (d : ℕ) {Ω : ℕ → Type u} {Ω0 : Type v}
    [∀ n, MeasurableSpace (Ω n)] [MeasurableSpace Ω0]
    (μ : ∀ n, Measure (Ω n)) (μ0 : Measure Ω0)
    [∀ n, IsProbabilityMeasure (μ n)] [IsProbabilityMeasure μ0]
    (X : ∀ n, Ω n → Vector d) (X0 : Ω0 → Vector d) : Prop :=
  (∀ t : Vector d,
      TendstoInDistribution
        (fun n ω ↦ projection t (X n ω))
        atTop
        (fun ω ↦ projection t (X0 ω))
        μ
        μ0) →
    TendstoInDistribution X atTop X0 μ μ0

/--
Checked easy direction at the measure level: weak convergence of vector laws implies
weak convergence of each Cramer-Wold projection.
-/
theorem projection_tendsto_of_probabilityMeasure_tendsto {d : ℕ}
    {μ : ℕ → ProbabilityMeasure (Vector d)} {μ0 : ProbabilityMeasure (Vector d)}
    (h : Tendsto μ atTop (𝓝 μ0)) (t : Vector d) :
    Tendsto
      (fun n ↦ (μ n).map ((continuous_projection t).measurable.aemeasurable))
      atTop
      (𝓝 (μ0.map ((continuous_projection t).measurable.aemeasurable))) :=
  ProbabilityMeasure.tendsto_map_of_tendsto_of_continuous μ μ0 h (continuous_projection t)

/--
Characteristic-function identity for Cramer-Wold projections, stated for raw
measures.  The scalar push-forward along `x ↦ ⟪x, t⟫` has at frequency `1` the
same characteristic function as the original finite-dimensional law at `t`.
-/
lemma projection_charFun_one_measure {d : ℕ} (μ : Measure (Vector d)) (t : Vector d) :
    charFun (μ.map (projection t)) 1 = charFun μ t := by
  rw [charFun_apply_real, charFun_apply]
  rw [integral_map ((continuous_projection t).aemeasurable) (by fun_prop)]
  simp [projection]

/--
Probability-measure version of `projection_charFun_one_measure`, matching the
push-forwards used by the Stage1 Cramer-Wold statement shape.
-/
lemma projection_charFun_one {d : ℕ} (μ : ProbabilityMeasure (Vector d)) (t : Vector d) :
    charFun (μ.map ((continuous_projection t).measurable.aemeasurable) : Measure ℝ) 1 =
      charFun (μ : Measure (Vector d)) t := by
  simpa only [ProbabilityMeasure.toMeasure_map] using
    projection_charFun_one_measure (μ : Measure (Vector d)) t

/--
P3 bridge for the hard Cramer-Wold direction: scalar weak convergence of every
projection implies pointwise convergence of the finite-dimensional
characteristic functions.
-/
theorem charFun_tendsto_of_projection_tendsto {d : ℕ}
    {μ : ℕ → ProbabilityMeasure (Vector d)} {μ0 : ProbabilityMeasure (Vector d)}
    (h : ∀ t : Vector d,
      Tendsto
        (fun n ↦ (μ n).map ((continuous_projection t).measurable.aemeasurable))
        atTop
        (𝓝 (μ0.map ((continuous_projection t).measurable.aemeasurable)))) :
    ∀ t : Vector d,
      Tendsto (fun n ↦ charFun (μ n : Measure (Vector d)) t)
        atTop
        (𝓝 (charFun (μ0 : Measure (Vector d)) t)) := by
  intro t
  have hchar := (ProbabilityMeasure.tendsto_iff_tendsto_charFun.mp (h t)) 1
  simpa only [ProbabilityMeasure.toMeasure_map, projection_charFun_one_measure] using hchar

/--
P4 closure for the measure-level Cramer-Wold statement shape.  The P3
characteristic-function bridge supplies exactly the right-hand side of mathlib's
Lévy convergence theorem for `ProbabilityMeasure`.
-/
theorem measureStatementShape_of_projection_tendsto {d : ℕ}
    {μ : ℕ → ProbabilityMeasure (Vector d)} {μ0 : ProbabilityMeasure (Vector d)} :
    MeasureStatementShape d μ μ0 := by
  intro h
  exact ProbabilityMeasure.tendsto_iff_tendsto_charFun.mpr
    (charFun_tendsto_of_projection_tendsto h)

/--
Random-variable bridge for the hard Cramer-Wold direction.

This theorem unfolds `TendstoInDistribution` to laws, applies the checked
measure-level Cramer-Wold closure to those laws as `ProbabilityMeasure` values,
and folds the result back into `TendstoInDistribution`.
-/
theorem tendstoInDistribution_of_projection_tendstoInDistribution {d : ℕ}
    {Ω : ℕ → Type u} {Ω0 : Type v}
    [∀ n, MeasurableSpace (Ω n)] [MeasurableSpace Ω0]
    {μ : ∀ n, Measure (Ω n)} {μ0 : Measure Ω0}
    [∀ n, IsProbabilityMeasure (μ n)] [IsProbabilityMeasure μ0]
    {X : ∀ n, Ω n → Vector d} {X0 : Ω0 → Vector d}
    (h : ∀ t : Vector d,
      TendstoInDistribution
        (fun n ω ↦ projection t (X n ω))
        atTop
        (fun ω ↦ projection t (X0 ω))
        μ
        μ0) :
    TendstoInDistribution X atTop X0 μ μ0 := by
  have hX : ∀ n, AEMeasurable (X n) (μ n) := fun n ↦
    aemeasurable_vector_of_projection fun t ↦ (h t).forall_aemeasurable n
  have hX0 : AEMeasurable X0 μ0 :=
    aemeasurable_vector_of_projection fun t ↦ (h t).aemeasurable_limit
  let ν : ℕ → ProbabilityMeasure (Vector d) := fun n ↦
    ⟨(μ n).map (X n), Measure.isProbabilityMeasure_map (hX n)⟩
  let ν0 : ProbabilityMeasure (Vector d) :=
    ⟨μ0.map X0, Measure.isProbabilityMeasure_map hX0⟩
  have hproj :
      ∀ t : Vector d,
        Tendsto
          (fun n ↦ (ν n).map ((continuous_projection t).measurable.aemeasurable))
          atTop
          (𝓝 (ν0.map ((continuous_projection t).measurable.aemeasurable))) := by
    intro t
    convert (h t).tendsto using 2 with n
    · ext s hs
      simp only [ν, ProbabilityMeasure.toMeasure_map, ProbabilityMeasure.coe_mk]
      rw [AEMeasurable.map_map_of_aemeasurable
        ((continuous_projection t).measurable.aemeasurable) (hX n)]
      rfl
    · ext s hs
      simp only [ν0, ProbabilityMeasure.toMeasure_map, ProbabilityMeasure.coe_mk]
      rw [AEMeasurable.map_map_of_aemeasurable
        ((continuous_projection t).measurable.aemeasurable) hX0]
      rfl
  refine
    { forall_aemeasurable := hX
      aemeasurable_limit := hX0
      tendsto := ?_ }
  simpa [ν, ν0] using measureStatementShape_of_projection_tendsto (μ := ν) (μ0 := ν0) hproj

/-- Checked closure of the random-variable `StatementShape`. -/
theorem statementShape_of_projection_tendstoInDistribution {d : ℕ}
    {Ω : ℕ → Type u} {Ω0 : Type v}
    [∀ n, MeasurableSpace (Ω n)] [MeasurableSpace Ω0]
    {μ : ∀ n, Measure (Ω n)} {μ0 : Measure Ω0}
    [∀ n, IsProbabilityMeasure (μ n)] [IsProbabilityMeasure μ0]
    {X : ∀ n, Ω n → Vector d} {X0 : Ω0 → Vector d} :
    StatementShape d μ μ0 X X0 := by
  intro h
  exact tendstoInDistribution_of_projection_tendstoInDistribution h

/--
Checked easy direction for random variables: vector convergence in distribution
implies convergence in distribution after every one-dimensional projection.
-/
theorem projection_tendstoInDistribution_of_vector {d : ℕ}
    {Ω : ℕ → Type u} {Ω0 : Type v}
    [∀ n, MeasurableSpace (Ω n)] [MeasurableSpace Ω0]
    {μ : ∀ n, Measure (Ω n)} {μ0 : Measure Ω0}
    [∀ n, IsProbabilityMeasure (μ n)] [IsProbabilityMeasure μ0]
    {X : ∀ n, Ω n → Vector d} {X0 : Ω0 → Vector d}
    (h : TendstoInDistribution X atTop X0 μ μ0) (t : Vector d) :
    TendstoInDistribution
      (fun n ω ↦ projection t (X n ω))
      atTop
      (fun ω ↦ projection t (X0 ω))
      μ
      μ0 :=
  TendstoInDistribution.continuous_comp
    (X := X) (Z := X0) (μ := μ) (μ' := μ0) (g := projection t)
    (continuous_projection t) h

/-! ## External Lean 4 audit metadata -/

/-- Exact search terms required by `S1-M-292.external-audit`. -/
def externalAuditSearchTerms : List String := [
  "CramerWold",
  "cramer_wold",
  "CramérWold",
  "Cramer-Wold",
  "TendstoInDistribution"
]

/-- A structured row for the Cramer-Wold external Lean 4 source audit. -/
structure ExternalLeanAuditRow where
  searchSurface : String
  url : String
  commit : String
  moduleName : String
  theoremName : String
  placeholders : String
  license : String
  toolchain : String
  lakeIntegrationFeasibility : String
deriving Repr

/--
Primary Lean 4 source audit rows for `S1-M-292.external-audit`.

Rows are audit data only.  The checked local artifact above proves the normalized
finite-dimensional Cramer-Wold statement shape in this repository, but this table
does not claim that a separate external terminal proof has been imported.
-/
def externalLeanPrimarySourceAuditRows : List ExternalLeanAuditRow := [
  {
    searchSurface := "pinned local mathlib source search for Cramer-Wold spellings",
    url := "https://github.com/leanprover-community/mathlib4/tree/8a178386ffc0f5fef0b77738bb5449d50efeea95",
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    moduleName := "Mathlib.MeasureTheory.Function.ConvergenceInDistribution; Mathlib.MeasureTheory.Measure.LevyConvergence; Mathlib.MeasureTheory.Measure.CharacteristicFunction.Basic",
    theoremName := "no direct Cramer-Wold declaration found for CramerWold, cramer_wold, CramérWold, or Cramer-Wold",
    placeholders := "none found in the audited mathlib source files by local placeholder scan",
    license := "Apache-2.0",
    toolchain := "leanprover/lean4:v4.29.0",
    lakeIntegrationFeasibility := "already pinned as this repository's mathlib dependency; no external Cramer-Wold theorem to import from these search terms"
  },
  {
    searchSurface := "pinned local mathlib source search for TendstoInDistribution",
    url := "https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/MeasureTheory/Function/ConvergenceInDistribution.lean",
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    moduleName := "Mathlib.MeasureTheory.Function.ConvergenceInDistribution",
    theoremName := "MeasureTheory.TendstoInDistribution; MeasureTheory.TendstoInDistribution.continuous_comp",
    placeholders := "none found in this source file by local placeholder scan",
    license := "Apache-2.0",
    toolchain := "leanprover/lean4:v4.29.0",
    lakeIntegrationFeasibility := "already available through the pinned mathlib import used by this file"
  },
  {
    searchSurface := "pinned local mathlib source search for characteristic-function convergence bridge",
    url := "https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/MeasureTheory/Measure/LevyConvergence.lean",
    commit := "8a178386ffc0f5fef0b77738bb5449d50efeea95",
    moduleName := "Mathlib.MeasureTheory.Measure.LevyConvergence",
    theoremName := "MeasureTheory.ProbabilityMeasure.tendsto_iff_tendsto_charFun",
    placeholders := "none found in this source file by local placeholder scan",
    license := "Apache-2.0",
    toolchain := "leanprover/lean4:v4.29.0",
    lakeIntegrationFeasibility := "already available through the pinned mathlib import used by this file"
  },
  {
    searchSurface := "Loogle public declaration index on 2026-05-01",
    url := "https://loogle.lean-lang.org/json",
    commit := "index query, no source commit exposed",
    moduleName := "Mathlib.MeasureTheory.Function.ConvergenceInDistribution; Mathlib.MeasureTheory.Measure.LevyConvergence",
    theoremName := "0 declaration-name hits for CramerWold, cramer_wold, CramérWold, Cramer-Wold, or Cramér-Wold; TendstoInDistribution and ProbabilityMeasure.tendsto_iff_tendsto_charFun resolved to mathlib declarations",
    placeholders := "not a source checkout; placeholder status taken from the pinned mathlib files above",
    license := "not a proof source license; resolved declarations are in mathlib under Apache-2.0",
    toolchain := "public index over mathlib; local checked toolchain is leanprover/lean4:v4.29.0",
    lakeIntegrationFeasibility := "no additional external dependency identified; resolved declarations are already in the current Lake closure"
  },
  {
    searchSurface := "unauthenticated GitHub code-search fallback",
    url := "https://api.github.com/search/code",
    commit := "not available: unauthenticated search was rate-limited",
    moduleName := "not available",
    theoremName := "not available",
    placeholders := "not available",
    license := "not available",
    toolchain := "not available",
    lakeIntegrationFeasibility := "audit blocker for global GitHub coverage only; it is not evidence for an external theorem and creates no repo-local integration debt"
  }
]

/-- Checked row count for the C007 external Lean 4 source-audit table. -/
theorem externalLeanPrimarySourceAuditRows_length :
    externalLeanPrimarySourceAuditRows.length = 5 := by
  native_decide

/--
Repo-local integration-debt gate result for the C007 external audit.

No separate external Lean 4 terminal Cramer-Wold theorem was found by the
audited sources, so this child does not create an anchor-only external proof.
The current repo-local closure comes from the checked proof body in this file,
not from an unintegrated external dependency.
-/
def externalAuditRepoLocalIntegrationDebtGate : String :=
  "pass: no external_upstream_anchor_only terminal Cramer-Wold proof was found; no completed state relies on repo_local_integration_debt"

/--
C008 integration-gate result.

The retained external audit rows do not discover a separate terminal Lean 4
Cramer-Wold proof.  Therefore there is no external proof to pin/import/check and
no concrete external-integration blocker to record for this child.  Future
external-proof claims must be treated as incomplete until they are either
checked in this repository's Lake closure or blocked with a specific
toolchain/license/dependency reason.
-/
def childC008ExternalIntegrationGate : String :=
  "pass: no external Lean 4 terminal Cramer-Wold proof was discovered; no anchor-only external proof is used as completion evidence"

/--
C009 public-sync gate result.

This is a machine-visible marker for the serial public-document integration
boundary.  The checked local proof body may be used as evidence by a later
integrator, but public Stage1 completion must stay open until the authoritative
blueprint, todo, and README surfaces are updated together.
-/
def childC009PublicSyncGate : String :=
  "open: public Stage1 surfaces must stay unsynchronized-completion-open until an integrator merges the validated local result into blueprint/todo/README together"

/-! ## Audit probes retained in the checked file. -/

#check MeasureTheory.TendstoInDistribution
#check MeasureTheory.TendstoInDistribution.continuous_comp
#check MeasureTheory.ProbabilityMeasure.tendsto_iff_tendsto_charFun
#check StatementShape
#check statementShape_of_projection_tendstoInDistribution
#check externalAuditSearchTerms
#check externalLeanPrimarySourceAuditRows
#check externalLeanPrimarySourceAuditRows_length
#check externalAuditRepoLocalIntegrationDebtGate
#check childC008ExternalIntegrationGate
#check childC009PublicSyncGate

end

end AwesomeTheorems.Stage1.S1_M_292
