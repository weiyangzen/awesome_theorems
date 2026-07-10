import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.Distribution.DerivNotation
import Mathlib.Analysis.Distribution.Distribution
import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.Analysis.InnerProductSpace.Laplacian
import Mathlib.MeasureTheory.Function.LpSpace.Basic
import Mathlib.MeasureTheory.Integral.Prod

/-!
# S1-M-157 / THM-M-1229: Serrin criterion

This Stage1 artifact records a conservative Lean 4 boundary for Serrin's
regularity criterion for weak solutions of the incompressible Navier-Stokes
equations.

The pinned mathlib snapshot has useful substrates for `MemLp`, `eLpNorm`,
Bochner integration, distributions, test functions, Laplacians, Fréchet
calculus, and Sobolev-type estimates.  It does not expose a canonical
Navier-Stokes weak-solution API or a terminal Serrin/Prodi-Serrin regularity
theorem.  The declarations below therefore freeze a statement-shape boundary
and add low-risk wrappers around available mathlib anchors.  They introduce no
proof placeholders and make no terminal PDE proof claim.
-/

noncomputable section

open MeasureTheory Set
open scoped ENNReal NNReal Distributions

namespace AwesomeTheorems
namespace Stage1
namespace S1_M_157

/-- Euclidean spatial domain for an `n`-dimensional fluid model. -/
abbrev Space (n : ℕ) : Type :=
  EuclideanSpace ℝ (Fin n)

/-- Spacetime is modeled as explicit time paired with a spatial point. -/
abbrev SpaceTime (n : ℕ) : Type :=
  ℝ × Space n

/-- Velocity fields in the spacetime model. -/
abbrev VelocityField (n : ℕ) : Type :=
  SpaceTime n → Space n

/-- Pressure fields in the spacetime model. -/
abbrev PressureField (n : ℕ) : Type :=
  SpaceTime n → ℝ

/--
The real-exponent scaling condition used by Serrin-type regularity criteria.

For the classical three-dimensional form this specializes to
`2 / q + 3 / p <= 1`, with `p > 3`; here `n` is kept explicit so the statement
shape can record the dimension parameter.
-/
def SerrinExponentCondition (n : ℕ) (p q : ℝ) : Prop :=
  0 < p ∧ 0 < q ∧ (n : ℝ) < p ∧ 2 / q + (n : ℝ) / p ≤ 1

/--
Input object for a future Lean 4 Serrin regularity theorem.

The fields using current mathlib APIs are intentionally concrete: local
measures, global `MemLp` data for velocity and pressure, and real-valued
Serrin exponents.  The weak Navier-Stokes equation, energy inequality,
boundary/initial conditions, and true mixed `L^q_t L^p_x` norm are stored as
explicit propositions because the audited local dependency closure has no
canonical Navier-Stokes weak-solution or mixed-norm API.
-/
structure SerrinWeakSolutionInput (n : ℕ)
    [MeasurableSpace (Space n)] [MeasurableSpace (SpaceTime n)] where
  timeInterval : Set ℝ
  spatialDomain : Set (Space n)
  timeInterval_isOpen : IsOpen timeInterval
  spatialDomain_isOpen : IsOpen spatialDomain
  velocity : VelocityField n
  pressure : PressureField n
  timeMeasure : Measure ℝ
  spaceMeasure : Measure (Space n)
  spaceTimeMeasure : Measure (SpaceTime n)
  globalLpExponent : ℝ≥0∞
  velocityMemLp : MemLp velocity globalLpExponent spaceTimeMeasure
  pressureMemLp : MemLp pressure globalLpExponent spaceTimeMeasure
  energyClass : Prop
  weakNavierStokesEquation : Prop
  divergenceFreeWeak : Prop
  initialConditionWeak : Prop
  boundaryCondition : Prop
  energyInequality : Prop
  serrinSpatialExponent : ℝ
  serrinTimeExponent : ℝ
  serrinExponentCondition :
    SerrinExponentCondition n serrinSpatialExponent serrinTimeExponent
  serrinMixedIntegrability : Prop

/--
Terminal conclusion package expected from Serrin's criterion.

The regularity target is expressed with `ContDiffOn` over the time-domain times
the spatial interior.  The bridge and estimate fields remain propositions: a
future terminal proof must instantiate them with a concrete weak-to-classical
Navier-Stokes bridge and the a priori estimates behind the criterion.
-/
structure SerrinRegularityConclusion {n : ℕ}
    [MeasurableSpace (Space n)] [MeasurableSpace (SpaceTime n)]
    (X : SerrinWeakSolutionInput n) : Type where
  velocityRegularOnInterior :
    ContDiffOn ℝ ⊤ X.velocity (X.timeInterval ×ˢ interior X.spatialDomain)
  pressureRegularOnInterior :
    ContDiffOn ℝ ⊤ X.pressure (X.timeInterval ×ˢ interior X.spatialDomain)
  weakToClassicalBridge : Prop
  localEnergyEstimate : Prop
  serrinBootstrapEstimate : Prop
  bridge_holds : weakToClassicalBridge
  energy_estimate_holds : localEnergyEstimate
  bootstrap_estimate_holds : serrinBootstrapEstimate

/--
Normalized Stage1 statement shape for THM-M-1229.

Given an explicitly modeled weak Navier-Stokes input satisfying the weak
equation, energy inequality, and Serrin mixed-integrability hypothesis, the
future theorem should produce an interior regularity package.
-/
def StatementShape : Prop :=
  ∀ (n : ℕ) [MeasurableSpace (Space n)] [MeasurableSpace (SpaceTime n)]
    (X : SerrinWeakSolutionInput n),
      X.weakNavierStokesEquation →
        X.divergenceFreeWeak →
          X.energyClass →
            X.energyInequality →
              X.serrinMixedIntegrability →
                Nonempty (SerrinRegularityConclusion X)

/-- Low-risk introduction wrapper for the normalized statement shape. -/
theorem StatementShape.intro
    (h : ∀ (n : ℕ) [MeasurableSpace (Space n)] [MeasurableSpace (SpaceTime n)]
      (X : SerrinWeakSolutionInput n),
        X.weakNavierStokesEquation →
          X.divergenceFreeWeak →
            X.energyClass →
              X.energyInequality →
                X.serrinMixedIntegrability →
                  Nonempty (SerrinRegularityConclusion X)) :
    StatementShape :=
  h

/-- Checked wrapper: the velocity field in the input has the stored `MemLp` property. -/
theorem velocity_memLp {n : ℕ}
    [MeasurableSpace (Space n)] [MeasurableSpace (SpaceTime n)]
    (X : SerrinWeakSolutionInput n) :
    MemLp X.velocity X.globalLpExponent X.spaceTimeMeasure :=
  X.velocityMemLp

/-- Checked wrapper: the pressure field in the input has the stored `MemLp` property. -/
theorem pressure_memLp {n : ℕ}
    [MeasurableSpace (Space n)] [MeasurableSpace (SpaceTime n)]
    (X : SerrinWeakSolutionInput n) :
    MemLp X.pressure X.globalLpExponent X.spaceTimeMeasure :=
  X.pressureMemLp

/-- Checked mathlib anchor: `MemLp` gives almost-everywhere strong measurability. -/
theorem velocity_aestronglyMeasurable {n : ℕ}
    [MeasurableSpace (Space n)] [MeasurableSpace (SpaceTime n)]
    (X : SerrinWeakSolutionInput n) :
    AEStronglyMeasurable X.velocity X.spaceTimeMeasure :=
  X.velocityMemLp.aestronglyMeasurable

/-- Checked mathlib anchor: the velocity `eLpNorm` is finite under `MemLp`. -/
theorem velocity_eLpNorm_lt_top {n : ℕ}
    [MeasurableSpace (Space n)] [MeasurableSpace (SpaceTime n)]
    (X : SerrinWeakSolutionInput n) :
    eLpNorm X.velocity X.globalLpExponent X.spaceTimeMeasure < ∞ :=
  X.velocityMemLp.eLpNorm_lt_top

/-- Checked mathlib anchor: the pressure `eLpNorm` is finite under `MemLp`. -/
theorem pressure_eLpNorm_lt_top {n : ℕ}
    [MeasurableSpace (Space n)] [MeasurableSpace (SpaceTime n)]
    (X : SerrinWeakSolutionInput n) :
    eLpNorm X.pressure X.globalLpExponent X.spaceTimeMeasure < ∞ :=
  X.pressureMemLp.eLpNorm_lt_top

/-- Checked wrapper exposing the stored Serrin exponent inequalities. -/
theorem serrin_exponent_condition {n : ℕ}
    [MeasurableSpace (Space n)] [MeasurableSpace (SpaceTime n)]
    (X : SerrinWeakSolutionInput n) :
    SerrinExponentCondition n X.serrinSpatialExponent X.serrinTimeExponent :=
  X.serrinExponentCondition

/-- Checked wrapper extracting velocity regularity from a terminal conclusion package. -/
theorem velocity_regularOnInterior_of_conclusion {n : ℕ}
    [MeasurableSpace (Space n)] [MeasurableSpace (SpaceTime n)]
    {X : SerrinWeakSolutionInput n} (C : SerrinRegularityConclusion X) :
    ContDiffOn ℝ ⊤ X.velocity (X.timeInterval ×ˢ interior X.spatialDomain) :=
  C.velocityRegularOnInterior

/-- Checked wrapper extracting pressure regularity from a terminal conclusion package. -/
theorem pressure_regularOnInterior_of_conclusion {n : ℕ}
    [MeasurableSpace (Space n)] [MeasurableSpace (SpaceTime n)]
    {X : SerrinWeakSolutionInput n} (C : SerrinRegularityConclusion X) :
    ContDiffOn ℝ ⊤ X.pressure (X.timeInterval ×ˢ interior X.spatialDomain) :=
  C.pressureRegularOnInterior

/-- mathlib modules checked while locating repo-local anchors for this PDE slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.MeasureTheory.Function.LpSpace.Basic",
  "Mathlib.MeasureTheory.Function.LpSeminorm.Basic",
  "Mathlib.MeasureTheory.Function.Holder",
  "Mathlib.MeasureTheory.Integral.Bochner.Basic",
  "Mathlib.MeasureTheory.Integral.Prod",
  "Mathlib.Analysis.FunctionalSpaces.SobolevInequality",
  "Mathlib.Analysis.Distribution.Distribution",
  "Mathlib.Analysis.Distribution.DerivNotation",
  "Mathlib.Analysis.Distribution.TestFunction",
  "Mathlib.Analysis.InnerProductSpace.Laplacian",
  "Mathlib.Analysis.Calculus.ContDiff.Basic",
  "Mathlib.Analysis.Calculus.FDeriv.Basic"
]

/-- Pinned mathlib revision audited for this Stage1 Serrin statement-shape slot. -/
def mathlibAnchorRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Pinned theorem and definition names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.MemLp",
  "MeasureTheory.MemLp.aestronglyMeasurable",
  "MeasureTheory.MemLp.eLpNorm_lt_top",
  "MeasureTheory.eLpNorm",
  "MeasureTheory.Lp",
  "MeasureTheory.Integrable",
  "Distribution",
  "TestFunction",
  "LineDeriv.iteratedLineDerivOp",
  "Laplacian.laplacian",
  "ContDiff",
  "ContDiffOn",
  "fderiv",
  "MeasureTheory.eLpNorm_le_eLpNorm_fderiv",
  "MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq",
  "MeasureTheory.memLp_of_bilin"
]

/--
Exact child-task anchor list for `S1-M-157-C003`.

These names are source-level anchors in the pinned mathlib closure; they are
not evidence for a terminal Serrin criterion theorem.
-/
def c003RequestedAnchorNames : List String := [
  "MeasureTheory.MemLp",
  "MeasureTheory.MemLp.aestronglyMeasurable",
  "MeasureTheory.MemLp.eLpNorm_lt_top",
  "MeasureTheory.eLpNorm",
  "Distribution",
  "TestFunction",
  "LineDeriv.iteratedLineDerivOp",
  "Laplacian.laplacian",
  "ContDiffOn",
  "fderiv"
]

/-- Checked equality for downstream public backfill of the audited mathlib revision. -/
theorem mathlibAnchorRevision_eq :
    mathlibAnchorRevision = "8a178386ffc0f5fef0b77738bb5449d50efeea95" :=
  rfl

/--
Search terms that did not locate a terminal Serrin criterion theorem in pinned
mathlib.
-/
def absentTerminalSearchTerms : List String := [
  "Serrin",
  "Prodi",
  "Ladyzhenskaya",
  "Navier",
  "NavierStokes",
  "Navier-Stokes",
  "Leray-Hopf",
  "LerayHopf",
  "weak solution",
  "WeakSolution",
  "regularity criterion",
  "mixed norm",
  "Lq Lp",
  "incompressible"
]

/-! ## C004 public-blocker metadata -/

/--
Exact public blocker proposed by `S1-M-157-C004`.

This is a pass-local audit conclusion, not a universal claim about all future
Lean developments.
-/
def c004PublicBlocker : String :=
  "no pinned mathlib or external Lean 4 theorem for Serrin/Prodi-Serrin regularity of Navier-Stokes weak solutions was found in this pass"

/-- No pinned mathlib terminal Serrin theorem was found in this pass. -/
def pinnedMathlibTerminalSerrinTheoremFoundInThisPass : Bool :=
  false

/-- No external Lean 4 terminal Serrin theorem was found in this pass. -/
def externalLeanTerminalSerrinTheoremFoundInThisPass : Bool :=
  false

/-- Checked equality for the C004 public blocker text. -/
theorem c004PublicBlocker_eq :
    c004PublicBlocker =
      "no pinned mathlib or external Lean 4 theorem for Serrin/Prodi-Serrin regularity of Navier-Stokes weak solutions was found in this pass" :=
  rfl

/-- Checked non-discovery gate for pinned mathlib terminal theorem evidence. -/
theorem pinnedMathlibTerminalSerrinTheoremFoundInThisPass_eq_false :
    pinnedMathlibTerminalSerrinTheoremFoundInThisPass = false :=
  rfl

/-- Checked non-discovery gate for external Lean 4 terminal theorem evidence. -/
theorem externalLeanTerminalSerrinTheoremFoundInThisPass_eq_false :
    externalLeanTerminalSerrinTheoremFoundInThisPass = false :=
  rfl

/-! ## C005 theorem-tree leaf inventory -/

/--
Compact theorem-tree leaf record for the C005 public backfill proposal.

The `status` field is deliberately string-valued because these records are
planning metadata, not proof-state objects.
-/
structure C005TheoremTreeLeaf where
  id : String
  status : String
  description : String
  localStepBudget : ℕ
deriving Repr, DecidableEq

/--
The theorem-tree leaves requested by `S1-M-157-C005`.

Leaves `M1229-L001` through `M1229-L012` correspond to checked local
statement-shape or validation work.  Terminal PDE, external-audit, integration,
and public-surface leaves `M1229-L013` through `M1229-L021` are intentionally
left `unchecked`.
-/
def c005TheoremTreeLeaves : List C005TheoremTreeLeaf := [
  { id := "M1229-L001", status := "checked",
    description := "Define Space n, SpaceTime n, VelocityField n, and PressureField n",
    localStepBudget := 8 },
  { id := "M1229-L002", status := "checked",
    description := "Define SerrinExponentCondition n p q",
    localStepBudget := 6 },
  { id := "M1229-L003", status := "checked",
    description := "Define SerrinWeakSolutionInput n",
    localStepBudget := 18 },
  { id := "M1229-L004", status := "checked",
    description := "Define SerrinRegularityConclusion X",
    localStepBudget := 12 },
  { id := "M1229-L005", status := "checked",
    description := "Define StatementShape",
    localStepBudget := 8 },
  { id := "M1229-L006", status := "checked",
    description := "Add StatementShape.intro",
    localStepBudget := 5 },
  { id := "M1229-L007", status := "checked",
    description := "Wrap velocity and pressure MemLp fields",
    localStepBudget := 5 },
  { id := "M1229-L008", status := "checked",
    description := "Wrap MemLp.aestronglyMeasurable",
    localStepBudget := 4 },
  { id := "M1229-L009", status := "checked",
    description := "Wrap MemLp.eLpNorm_lt_top for velocity and pressure",
    localStepBudget := 5 },
  { id := "M1229-L010", status := "checked",
    description := "Wrap stored Serrin exponent condition",
    localStepBudget := 3 },
  { id := "M1229-L011", status := "checked",
    description := "Wrap regularity conclusions from terminal package fields",
    localStepBudget := 5 },
  { id := "M1229-L012", status := "checked",
    description := "Validate direct Lean command",
    localStepBudget := 4 },
  { id := "M1229-L013", status := "unchecked",
    description := "Authenticated external Lean 4 source search for terminal Serrin criterion proof",
    localStepBudget := 25 },
  { id := "M1229-L014", status := "unchecked",
    description := "Define true mixed L^q_t L^p_x object, including measurability of the spatial Lp norm",
    localStepBudget := 90 },
  { id := "M1229-L015", status := "unchecked",
    description := "Define weak incompressible Navier-Stokes equation over distributions or test functions",
    localStepBudget := 95 },
  { id := "M1229-L016", status := "unchecked",
    description := "Define Leray-Hopf energy class and local/global energy inequality",
    localStepBudget := 90 },
  { id := "M1229-L017", status := "unchecked",
    description := "Prove nonlinear convection estimate under Serrin exponents",
    localStepBudget := 95 },
  { id := "M1229-L018", status := "unchecked",
    description := "Prove parabolic/Stokes bootstrap regularity branch",
    localStepBudget := 95 },
  { id := "M1229-L019", status := "unchecked",
    description := "Prove terminal weak-to-classical regularity wrapper",
    localStepBudget := 80 },
  { id := "M1229-L020", status := "unchecked",
    description := "Pin/import/check any future external Lean proof or record concrete blocker",
    localStepBudget := 40 },
  { id := "M1229-L021", status := "unchecked",
    description := "Public blueprint/todo/README synchronization by later integrator",
    localStepBudget := 30 }
]

/-- Terminal leaves that must remain unchecked in the public C005 backfill. -/
def c005UncheckedTerminalLeaves : List String := [
  "M1229-L013",
  "M1229-L014",
  "M1229-L015",
  "M1229-L016",
  "M1229-L017",
  "M1229-L018",
  "M1229-L019",
  "M1229-L020",
  "M1229-L021"
]

/-- Checked leaf count for the C005 theorem-tree inventory. -/
theorem c005TheoremTreeLeaves_length :
    c005TheoremTreeLeaves.length = 21 :=
  rfl

/-- Checked terminal-unchecked list for downstream public backfill. -/
theorem c005UncheckedTerminalLeaves_eq :
    c005UncheckedTerminalLeaves = [
      "M1229-L013",
      "M1229-L014",
      "M1229-L015",
      "M1229-L016",
      "M1229-L017",
      "M1229-L018",
      "M1229-L019",
      "M1229-L020",
      "M1229-L021"
    ] :=
  rfl

/-- Checked budget gate: every listed local leaf estimate is at most 100 steps. -/
theorem c005EveryLeafWithinBudget :
    c005TheoremTreeLeaves.all (fun leaf => leaf.localStepBudget ≤ 100) = true :=
  rfl

/--
C005 does not claim terminal Serrin criterion completion.

It only records a theorem-tree backfill inventory for later serialized public
planning integration.
-/
def c005TerminalTheoremCompleted : Bool :=
  false

/-- Checked non-completion gate for C005. -/
theorem c005TerminalTheoremCompleted_eq_false :
    c005TerminalTheoremCompleted = false :=
  rfl

/-! ## C006 mixed `L^q_t L^p_x` follow-up task -/

/--
Spatial `eLpNorm` profile for a spacetime velocity field.

For each time `t`, this records the spatial `L^p` seminorm of the slice
`x ↦ u (t, x)`.  The C006 follow-up task is to prove the required measurability
of this profile from product-measurability hypotheses, rather than storing it
as an opaque Serrin-side proposition.
-/
def spatialELpNormProfile {n : ℕ} [MeasurableSpace (Space n)]
    (u : VelocityField n) (spaceMeasure : Measure (Space n)) (p : ℝ≥0∞) :
    ℝ → ℝ≥0∞ :=
  fun t => eLpNorm (fun x : Space n => u (t, x)) p spaceMeasure

/--
Integration-ready target shape for true mixed `L^q_t L^p_x` hypotheses.

This is deliberately not a proof that Serrin's criterion holds.  It isolates
the missing mixed-norm API over the product measure `timeMeasure.prod
spaceMeasure`, including the measurability of
`t ↦ ||u(t, .)||_{L^p_x}` and the outer `L^q_t` membership.
-/
structure MixedLqLpFollowUpSpec (n : ℕ) [MeasurableSpace (Space n)] where
  velocity : VelocityField n
  timeMeasure : Measure ℝ
  spaceMeasure : Measure (Space n)
  productMeasure : Measure (ℝ × Space n)
  spatialExponent : ℝ≥0∞
  timeExponent : ℝ≥0∞
  productMeasure_eq : productMeasure = timeMeasure.prod spaceMeasure
  spatialSliceMemLp :
    ∀ᵐ t ∂timeMeasure,
      MemLp (fun x : Space n => velocity (t, x)) spatialExponent spaceMeasure
  spatialProfileAEMeasurable :
    AEMeasurable
      (spatialELpNormProfile velocity spaceMeasure spatialExponent) timeMeasure
  mixedTimeMemLp :
    MemLp (spatialELpNormProfile velocity spaceMeasure spatialExponent)
      timeExponent timeMeasure

/-- C006 wrapper: the mixed-norm package uses the product time-space measure. -/
theorem c006_productMeasure_eq {n : ℕ}
    [MeasurableSpace (Space n)]
    (M : MixedLqLpFollowUpSpec n) :
    M.productMeasure = M.timeMeasure.prod M.spaceMeasure :=
  M.productMeasure_eq

/-- C006 wrapper: almost every spatial slice belongs to the inner `L^p_x`. -/
theorem c006_spatialSliceMemLp {n : ℕ}
    [MeasurableSpace (Space n)]
    (M : MixedLqLpFollowUpSpec n) :
    ∀ᵐ t ∂M.timeMeasure,
      MemLp (fun x : Space n => M.velocity (t, x)) M.spatialExponent M.spaceMeasure :=
  M.spatialSliceMemLp

/-- C006 wrapper: the spatial `Lp` norm profile is measurable in time. -/
theorem c006_spatialProfileAEMeasurable {n : ℕ}
    [MeasurableSpace (Space n)]
    (M : MixedLqLpFollowUpSpec n) :
    AEMeasurable
      (spatialELpNormProfile M.velocity M.spaceMeasure M.spatialExponent)
      M.timeMeasure :=
  M.spatialProfileAEMeasurable

/-- C006 wrapper: the spatial `Lp` norm profile belongs to the outer `L^q_t`. -/
theorem c006_mixedTimeMemLp {n : ℕ}
    [MeasurableSpace (Space n)]
    (M : MixedLqLpFollowUpSpec n) :
    MemLp (spatialELpNormProfile M.velocity M.spaceMeasure M.spatialExponent)
      M.timeExponent M.timeMeasure :=
  M.mixedTimeMemLp

/-- C006 wrapper: the mixed `L^q_t L^p_x` `eLpNorm` is finite. -/
theorem c006_mixedTimeELpNorm_lt_top {n : ℕ}
    [MeasurableSpace (Space n)]
    (M : MixedLqLpFollowUpSpec n) :
    eLpNorm (spatialELpNormProfile M.velocity M.spaceMeasure M.spatialExponent)
      M.timeExponent M.timeMeasure < ∞ :=
  M.mixedTimeMemLp.eLpNorm_lt_top

/--
Compact local leaf record for the C006 mixed-norm follow-up task.

The task leaves are planning metadata for later public integration.  Checked
leaves correspond only to declarations and wrappers in this file; unchecked
leaves are the genuine future proofs needed to remove the opaque
`serrinMixedIntegrability` field from the parent statement shape.
-/
structure C006MixedNormFollowUpLeaf where
  id : String
  status : String
  description : String
  localStepBudget : ℕ
deriving Repr, DecidableEq

/-- Follow-up task leaves for true mixed `L^q_t L^p_x` formalization. -/
def c006MixedNormFollowUpLeaves : List C006MixedNormFollowUpLeaf := [
  { id := "M1229-C006-L001", status := "checked",
    description := "Define spatialELpNormProfile t = eLpNorm (fun x => u (t, x)) p spaceMeasure",
    localStepBudget := 12 },
  { id := "M1229-C006-L002", status := "checked",
    description := "Define MixedLqLpFollowUpSpec with productMeasure = timeMeasure.prod spaceMeasure",
    localStepBudget := 18 },
  { id := "M1229-C006-L003", status := "checked",
    description := "Expose the spatial-slice MemLp and spatial-profile AEMeasurable fields",
    localStepBudget := 10 },
  { id := "M1229-C006-L004", status := "checked",
    description := "Expose the outer mixedTimeMemLp field and finite mixed eLpNorm wrapper",
    localStepBudget := 10 },
  { id := "M1229-C006-L005", status := "unchecked",
    description := "Prove spatial-profile AEMeasurable from product-measurability and Fubini/Tonelli infrastructure",
    localStepBudget := 90 },
  { id := "M1229-C006-L006", status := "unchecked",
    description := "Replace SerrinWeakSolutionInput.serrinMixedIntegrability with the true mixed-norm package",
    localStepBudget := 65 }
]

/-- C006 leaves that remain genuine mixed-norm formalization debt. -/
def c006UncheckedMixedNormLeaves : List String := [
  "M1229-C006-L005",
  "M1229-C006-L006"
]

/-- The C006 follow-up task has a repo-local checked Lean target shape. -/
def c006MixedNormFollowUpTaskCreated : Bool :=
  true

/-- C006 does not complete the full mixed-norm proof branch. -/
def c006TrueMixedNormProofCompleted : Bool :=
  false

/-- Checked leaf count for the C006 mixed-norm follow-up inventory. -/
theorem c006MixedNormFollowUpLeaves_length :
    c006MixedNormFollowUpLeaves.length = 6 :=
  rfl

/-- Checked unchecked-leaf list for the C006 mixed-norm follow-up inventory. -/
theorem c006UncheckedMixedNormLeaves_eq :
    c006UncheckedMixedNormLeaves = [
      "M1229-C006-L005",
      "M1229-C006-L006"
    ] :=
  rfl

/-- Checked budget gate: every listed C006 leaf estimate is at most 100 steps. -/
theorem c006EveryMixedNormLeafWithinBudget :
    c006MixedNormFollowUpLeaves.all (fun leaf => leaf.localStepBudget ≤ 100) = true :=
  rfl

/-- Checked task-creation gate for C006. -/
theorem c006MixedNormFollowUpTaskCreated_eq_true :
    c006MixedNormFollowUpTaskCreated = true :=
  rfl

/-- Checked non-completion gate for the future mixed-norm proof branch. -/
theorem c006TrueMixedNormProofCompleted_eq_false :
    c006TrueMixedNormProofCompleted = false :=
  rfl

/-! ## C007 weak incompressible Navier-Stokes follow-up task -/

/--
Concrete data shape for the Leray-Hopf energy inequality branch.

This does not prove the analytic energy inequality.  It fixes the fields that a
future weak Navier-Stokes API must expose: kinetic energy, viscous
dissipation, their measurability and finiteness gates, and the proposition
that will eventually encode the Leray-Hopf inequality itself.
-/
structure LerayHopfEnergyInequalityFields (n : ℕ)
    [MeasurableSpace (Space n)] where
  timeMeasure : Measure ℝ
  spaceMeasure : Measure (Space n)
  velocity : VelocityField n
  initialVelocity : Space n → Space n
  kineticEnergy : ℝ → ℝ≥0∞
  viscousDissipation : ℝ → ℝ≥0∞
  kineticEnergyAEMeasurable : AEMeasurable kineticEnergy timeMeasure
  viscousDissipationAEMeasurable :
    AEMeasurable viscousDissipation timeMeasure
  kineticEnergyFiniteAE : ∀ᵐ t ∂timeMeasure, kineticEnergy t < ∞
  viscousDissipationFiniteAE :
    ∀ᵐ t ∂timeMeasure, viscousDissipation t < ∞
  initialEnergy : ℝ≥0∞
  energyInequality : Prop

/--
Integration-ready object shape for a weak incompressible Navier-Stokes
solution candidate.

The test-function carriers and residual predicates are explicit fields so a
later PDE API can replace them with distributional or test-function
definitions.  The divergence-free condition and Leray-Hopf energy inequality
are proof-carrying fields on this object, while the terminal Serrin
regularity theorem remains unproved.
-/
structure WeakIncompressibleNavierStokesFollowUpSpec (n : ℕ)
    [MeasurableSpace (Space n)] where
  timeInterval : Set ℝ
  spatialDomain : Set (Space n)
  timeInterval_isOpen : IsOpen timeInterval
  spatialDomain_isOpen : IsOpen spatialDomain
  velocity : VelocityField n
  pressure : PressureField n
  externalForce : VelocityField n
  viscosity : ℝ
  viscosity_pos : 0 < viscosity
  timeMeasure : Measure ℝ
  spaceMeasure : Measure (Space n)
  spaceTimeMeasure : Measure (ℝ × Space n)
  spaceTimeMeasure_eq_prod : spaceTimeMeasure = timeMeasure.prod spaceMeasure
  finiteEnergyExponent : ℝ≥0∞
  velocityFiniteEnergyMemLp : MemLp velocity finiteEnergyExponent spaceTimeMeasure
  pressureMemLpExponent : ℝ≥0∞
  pressureMemLp : MemLp pressure pressureMemLpExponent spaceTimeMeasure
  momentumTestFunction : Type
  divergenceTestFunction : Type
  weakMomentumResidual : momentumTestFunction → Prop
  weakMomentumEquation : ∀ φ : momentumTestFunction, weakMomentumResidual φ
  weakDivergenceResidual : divergenceTestFunction → Prop
  divergenceFreeWeak :
    ∀ ψ : divergenceTestFunction, weakDivergenceResidual ψ
  initialTraceWeak : Prop
  boundaryConditionWeak : Prop
  lerayHopfEnergy : LerayHopfEnergyInequalityFields n
  lerayHopfVelocity_eq : lerayHopfEnergy.velocity = velocity
  lerayHopfTimeMeasure_eq : lerayHopfEnergy.timeMeasure = timeMeasure
  lerayHopfSpaceMeasure_eq : lerayHopfEnergy.spaceMeasure = spaceMeasure
  lerayHopfEnergyInequality : lerayHopfEnergy.energyInequality

/-- C007 wrapper: the weak Navier-Stokes object uses the product spacetime measure. -/
theorem c007_spaceTimeMeasure_eq_prod {n : ℕ}
    [MeasurableSpace (Space n)]
    (W : WeakIncompressibleNavierStokesFollowUpSpec n) :
    W.spaceTimeMeasure = W.timeMeasure.prod W.spaceMeasure :=
  W.spaceTimeMeasure_eq_prod

/-- C007 wrapper: the stored weak momentum residual vanishes on all tests. -/
theorem c007_weakMomentumEquation {n : ℕ}
    [MeasurableSpace (Space n)]
    (W : WeakIncompressibleNavierStokesFollowUpSpec n)
    (φ : W.momentumTestFunction) :
    W.weakMomentumResidual φ :=
  W.weakMomentumEquation φ

/-- C007 wrapper: the stored incompressibility residual vanishes on all tests. -/
theorem c007_divergenceFreeWeak {n : ℕ}
    [MeasurableSpace (Space n)]
    (W : WeakIncompressibleNavierStokesFollowUpSpec n)
    (ψ : W.divergenceTestFunction) :
    W.weakDivergenceResidual ψ :=
  W.divergenceFreeWeak ψ

/-- C007 wrapper: the Leray-Hopf energy package is attached to the same velocity. -/
theorem c007_lerayHopfVelocity_eq {n : ℕ}
    [MeasurableSpace (Space n)]
    (W : WeakIncompressibleNavierStokesFollowUpSpec n) :
    W.lerayHopfEnergy.velocity = W.velocity :=
  W.lerayHopfVelocity_eq

/-- C007 wrapper: the Leray-Hopf kinetic-energy profile is measurable in time. -/
theorem c007_kineticEnergyAEMeasurable {n : ℕ}
    [MeasurableSpace (Space n)]
    (E : LerayHopfEnergyInequalityFields n) :
    AEMeasurable E.kineticEnergy E.timeMeasure :=
  E.kineticEnergyAEMeasurable

/-- C007 wrapper: the Leray-Hopf viscous-dissipation profile is measurable in time. -/
theorem c007_viscousDissipationAEMeasurable {n : ℕ}
    [MeasurableSpace (Space n)]
    (E : LerayHopfEnergyInequalityFields n) :
    AEMeasurable E.viscousDissipation E.timeMeasure :=
  E.viscousDissipationAEMeasurable

/-- C007 wrapper: the attached Leray-Hopf energy inequality proposition holds. -/
theorem c007_lerayHopfEnergyInequality {n : ℕ}
    [MeasurableSpace (Space n)]
    (W : WeakIncompressibleNavierStokesFollowUpSpec n) :
    W.lerayHopfEnergy.energyInequality :=
  W.lerayHopfEnergyInequality

/--
Compact local leaf record for the C007 weak Navier-Stokes follow-up task.

Checked leaves correspond to declarations and wrappers in this file.  Unchecked
leaves are the genuine future PDE API, distributional residual, and
Leray-Hopf inequality proofs needed before the parent Serrin statement can stop
using opaque weak-solution propositions.
-/
structure C007WeakNavierStokesFollowUpLeaf where
  id : String
  status : String
  description : String
  localStepBudget : ℕ
deriving Repr, DecidableEq

/-- Follow-up task leaves for a concrete weak incompressible Navier-Stokes object. -/
def c007WeakNavierStokesFollowUpLeaves :
    List C007WeakNavierStokesFollowUpLeaf := [
  { id := "M1229-C007-L001", status := "checked",
    description := "Define LerayHopfEnergyInequalityFields with kinetic energy, dissipation, measurability, finiteness, and energy-inequality fields",
    localStepBudget := 20 },
  { id := "M1229-C007-L002", status := "checked",
    description := "Define WeakIncompressibleNavierStokesFollowUpSpec with velocity, pressure, force, viscosity, product measure, weak momentum residual, weak divergence residual, and Leray-Hopf package",
    localStepBudget := 30 },
  { id := "M1229-C007-L003", status := "checked",
    description := "Expose wrappers for product spacetime measure, weak momentum equation, and divergence-free condition",
    localStepBudget := 12 },
  { id := "M1229-C007-L004", status := "checked",
    description := "Expose wrappers for Leray-Hopf velocity alignment, energy-profile measurability, dissipation-profile measurability, and the attached energy inequality",
    localStepBudget := 14 },
  { id := "M1229-C007-L005", status := "unchecked",
    description := "Replace the abstract weakMomentumResidual field with a distributional or test-function formula for the incompressible Navier-Stokes momentum equation",
    localStepBudget := 95 },
  { id := "M1229-C007-L006", status := "unchecked",
    description := "Replace weakDivergenceResidual with a mathlib-native weak divergence-free definition and prove equivalence to the selected PDE API",
    localStepBudget := 90 },
  { id := "M1229-C007-L007", status := "unchecked",
    description := "Define the Leray-Hopf kinetic-energy and viscous-dissipation profiles from spatial integrals of velocity and gradient fields",
    localStepBudget := 95 },
  { id := "M1229-C007-L008", status := "unchecked",
    description := "Prove or import the Leray-Hopf energy inequality for the selected weak-solution object and bridge it into SerrinWeakSolutionInput.energyInequality",
    localStepBudget := 95 }
]

/-- C007 leaves that remain genuine weak Navier-Stokes formalization debt. -/
def c007UncheckedWeakNavierStokesLeaves : List String := [
  "M1229-C007-L005",
  "M1229-C007-L006",
  "M1229-C007-L007",
  "M1229-C007-L008"
]

/-- The C007 follow-up task has a repo-local checked Lean target shape. -/
def c007WeakNavierStokesFollowUpTaskCreated : Bool :=
  true

/-- C007 does not complete the weak Navier-Stokes PDE API or proof branch. -/
def c007WeakNavierStokesProofCompleted : Bool :=
  false

/-- C007 does not complete the Leray-Hopf energy inequality proof branch. -/
def c007LerayHopfEnergyInequalityProofCompleted : Bool :=
  false

/-- Checked leaf count for the C007 weak Navier-Stokes follow-up inventory. -/
theorem c007WeakNavierStokesFollowUpLeaves_length :
    c007WeakNavierStokesFollowUpLeaves.length = 8 :=
  rfl

/-- Checked unchecked-leaf list for the C007 weak Navier-Stokes inventory. -/
theorem c007UncheckedWeakNavierStokesLeaves_eq :
    c007UncheckedWeakNavierStokesLeaves = [
      "M1229-C007-L005",
      "M1229-C007-L006",
      "M1229-C007-L007",
      "M1229-C007-L008"
    ] :=
  rfl

/-- Checked budget gate: every listed C007 leaf estimate is at most 100 steps. -/
theorem c007EveryWeakNavierStokesLeafWithinBudget :
    c007WeakNavierStokesFollowUpLeaves.all
      (fun leaf => leaf.localStepBudget ≤ 100) = true :=
  rfl

/-- Checked task-creation gate for C007. -/
theorem c007WeakNavierStokesFollowUpTaskCreated_eq_true :
    c007WeakNavierStokesFollowUpTaskCreated = true :=
  rfl

/-- Checked non-completion gate for the future weak Navier-Stokes proof branch. -/
theorem c007WeakNavierStokesProofCompleted_eq_false :
    c007WeakNavierStokesProofCompleted = false :=
  rfl

/-- Checked non-completion gate for the future Leray-Hopf proof branch. -/
theorem c007LerayHopfEnergyInequalityProofCompleted_eq_false :
    c007LerayHopfEnergyInequalityProofCompleted = false :=
  rfl

/-! ## C008 external primary-source Lean 4 audit -/

/--
Primary-source repository record for the C008 external Lean 4 audit.

The `acceptedAsTerminalProof` flag is deliberately strict: a source with
placeholder definitions, `sorry`, new axioms, or only statement scaffolding is
not accepted as a completed Serrin/Prodi-Serrin regularity proof.
-/
structure C008ExternalLeanAuditRecord where
  repository : String
  revision : String
  leanToolchain : String
  sourcePath : String
  declarationsOrHits : List String
  diagnosis : String
  acceptedAsTerminalProof : Bool
deriving Repr, DecidableEq

/-- Search terms requested by the C008 authenticated-primary-source audit leaf. -/
def c008RequestedSearchTerms : List String := [
  "Serrin",
  "Prodi",
  "Ladyzhenskaya",
  "NavierStokes",
  "Navier-Stokes",
  "LerayHopf",
  "WeakSolution",
  "regularity criterion",
  "mixed norm",
  "Lq Lp"
]

/--
C008 audit records for primary-source Lean 4 material inspected in this pass.

The mathlib check is represented by the existing pinned local source closure.
The two external cloned primary sources below contain either statement
scaffolding or placeholder routes, not an importable proof of the Serrin
regularity criterion.
-/
def c008ExternalLeanAuditRecords : List C008ExternalLeanAuditRecord := [
  {
    repository := "https://github.com/lean-dojo/LeanMillenniumPrizeProblems.git",
    revision := "540da94826f70f3edf4d4fc66ce6cda20e903f61",
    leanToolchain := "leanprover/lean4:v4.26.0",
    sourcePath := "Problems/NavierStokes/Navierstokes.lean; Problems/NavierStokes/Millennium.lean",
    declarationsOrHits := [
      "NavierStokes.NavierStokesEquations",
      "NavierStokes.Solution",
      "NavierStokes.WeakSolution",
      "NavierStokes.LerayHopfSolution",
      "MillenniumNavierStokes.NavierStokesMillenniumProblem"
    ],
    diagnosis := "Navier-Stokes statement/scaffold material only; no Serrin, Prodi, Ladyzhenskaya, mixed-norm, or regularity-criterion theorem found.",
    acceptedAsTerminalProof := false
  },
  {
    repository := "https://github.com/motanova84/3D-Navier-Stokes.git",
    revision := "7fbbcb26c1557ef2f048f7e21a40caf1107e5995",
    leanToolchain := "Lean4-Formalization/lean-toolchain: leanprover/lean4:v4.25.0-rc2",
    sourcePath := "Lean4-Formalization/SerrinEndpoint.lean; formal_verification/lean4/PsiNSE/SerrinEndpoint.lean",
    declarationsOrHits := [
      "NavierStokes.serrin_criterion",
      "NavierStokes.serrin_endpoint",
      "NavierStokes.global_regularity_via_serrin",
      "Lean4-Formalization/SerrinEndpoint.lean defines CInfinity as True",
      "Lean4-Formalization/SerrinEndpoint.lean defines IsSolution as True",
      "formal_verification/lean4/PsiNSE/SerrinEndpoint.lean contains sorry"
    ],
    diagnosis := "Not accepted as a terminal Serrin proof: one route trivializes the target through True-valued placeholder definitions, and the parallel route contains sorry; nearby Navier-Stokes modules also contain axioms/placeholders.",
    acceptedAsTerminalProof := false
  }
]

/-- GitHub CLI authentication was unavailable for the C008 code-search portion. -/
def c008GitHubCliAuthenticated : Bool :=
  false

/--
No accepted external Lean 4 terminal Serrin proof was found by C008.

This is not a claim that no such proof can exist; it records the result of the
local pinned mathlib search plus the cloned primary-source repositories audited
in this child pass.
-/
def c008AcceptedExternalTerminalProofFound : Bool :=
  false

/--
C008 does not create a dependency-integration task because no acceptable
external terminal proof was found.

If a later authenticated search finds a real proof, M0387 requires a serialized
pin/import/check task or a concrete integration blocker before any completion
claim.
-/
def c008DependencyIntegrationTaskRequiredNow : Bool :=
  false

/-- C008 leaves that remain open after the unauthenticated code-search blocker. -/
def c008RemainingAuditLeaves : List String := [
  "M1229-C008-L001: rerun GitHub code search with an authenticated token for the requested terms",
  "M1229-C008-L002: if a real external Lean 4 Serrin proof is found, create a serialized pin/import/check task or record a concrete integration blocker"
]

/-- Checked search-term list for C008. -/
theorem c008RequestedSearchTerms_length :
    c008RequestedSearchTerms.length = 10 :=
  rfl

/-- Checked primary-source record count for C008. -/
theorem c008ExternalLeanAuditRecords_length :
    c008ExternalLeanAuditRecords.length = 2 :=
  rfl

/-- Checked non-authentication gate for the GitHub CLI code-search channel. -/
theorem c008GitHubCliAuthenticated_eq_false :
    c008GitHubCliAuthenticated = false :=
  rfl

/-- Checked negative terminal-proof discovery result for C008. -/
theorem c008AcceptedExternalTerminalProofFound_eq_false :
    c008AcceptedExternalTerminalProofFound = false :=
  rfl

/-- Checked integration-task gate for C008. -/
theorem c008DependencyIntegrationTaskRequiredNow_eq_false :
    c008DependencyIntegrationTaskRequiredNow = false :=
  rfl

/-- Checked remaining-leaf count for C008. -/
theorem c008RemainingAuditLeaves_length :
    c008RemainingAuditLeaves.length = 2 :=
  rfl

/-! ## C009 shared import aggregator decision task -/

/--
Serialized choices for the later shared-import decision.

This child pass is not allowed to edit shared Lean import aggregators directly,
so the datatype records an integration-ready decision without changing
`AwesomeTheorems.lean` or Lake configuration.
-/
inductive SharedImportAggregatorDecision where
  /-- Add the validated Stage1 module to the shared aggregator in a serialized patch. -/
  | addStage1Module
  /-- Keep the file as a directly validated standalone Stage1 artifact. -/
  | keepStandalone
deriving DecidableEq, Repr

/--
Machine-readable status for deciding whether this Stage1 artifact should be
added to a shared Lean import aggregator.

The local recommendation is to add the module in a later serialized patch
because the file is a validated Stage1 statement-shape artifact with explicit
nonterminal Serrin status tags.  That import must not be described as
completing the Serrin/Prodi-Serrin regularity theorem.
-/
structure SharedImportAggregatorDecisionStatus where
  childId : String
  modulePath : String
  candidateImportLine : String
  targetAggregator : String
  moduleValidatedLocally : Bool
  sharedAggregatorEditedInChild : Bool
  recommendedDecision : SharedImportAggregatorDecision
  terminalTheoremCompletedByImport : Bool
  repoLocalIntegrationDebtRetainedInCompletedState : Bool
  reason : String
deriving DecidableEq, Repr

/-- Integration-ready shared-import decision for child `S1-M-157-C009`. -/
def c009SharedImportAggregatorDecisionStatus :
    SharedImportAggregatorDecisionStatus where
  childId := "S1-M-157-C009"
  modulePath := "AwesomeTheorems/Stage1/S1_M_157.lean"
  candidateImportLine := "import AwesomeTheorems.Stage1.S1_M_157"
  targetAggregator := "Formalizations/Lean/AwesomeTheorems.lean"
  moduleValidatedLocally := true
  sharedAggregatorEditedInChild := false
  recommendedDecision := .addStage1Module
  terminalTheoremCompletedByImport := false
  repoLocalIntegrationDebtRetainedInCompletedState := false
  reason :=
    "Add the validated Stage1 module in a later serialized aggregator patch; " ++
    "the import exposes statement-shape, audit, and follow-up metadata only, " ++
    "not a terminal Serrin/Prodi-Serrin regularity theorem."

/--
Checked local status for C009: the shared-import decision is ready for a
serialized integrator patch, while the shared aggregator remains untouched in
this child pass.
-/
theorem c009_shared_import_aggregator_decision_local_checked :
    c009SharedImportAggregatorDecisionStatus.childId = "S1-M-157-C009" ∧
      c009SharedImportAggregatorDecisionStatus.modulePath =
        "AwesomeTheorems/Stage1/S1_M_157.lean" ∧
      c009SharedImportAggregatorDecisionStatus.candidateImportLine =
        "import AwesomeTheorems.Stage1.S1_M_157" ∧
      c009SharedImportAggregatorDecisionStatus.targetAggregator =
        "Formalizations/Lean/AwesomeTheorems.lean" ∧
      c009SharedImportAggregatorDecisionStatus.moduleValidatedLocally = true ∧
      c009SharedImportAggregatorDecisionStatus.sharedAggregatorEditedInChild =
        false ∧
      c009SharedImportAggregatorDecisionStatus.recommendedDecision =
        SharedImportAggregatorDecision.addStage1Module ∧
      c009SharedImportAggregatorDecisionStatus.terminalTheoremCompletedByImport =
        false ∧
      c009SharedImportAggregatorDecisionStatus.repoLocalIntegrationDebtRetainedInCompletedState =
        false :=
  by
    simp [c009SharedImportAggregatorDecisionStatus]

/-! ## Machine-status gate -/

/--
Machine status for this Stage1 artifact.

This is intentionally weaker than terminal theorem completion: the local Lean
file checks a normalized statement shape and adjacent mathlib anchors, but it
does not prove Serrin's regularity criterion.
-/
def machineStatus : String :=
  "statement_shape_local_checked"

/-- The terminal Serrin regularity theorem is not completed by this artifact. -/
def terminalSerrinCriterionCompleted : Bool :=
  false

/--
No completed state in this artifact retains `repo_local_integration_debt`.

The current pass records no external Lean 4 Serrin proof as anchor-only
completion evidence; the terminal theorem remains formalization debt.
-/
def completedStateRetainsRepoLocalIntegrationDebt : Bool :=
  false

/-- Checked status equality for downstream public backfill. -/
theorem machineStatus_eq_statement_shape_local_checked :
    machineStatus = "statement_shape_local_checked" :=
  rfl

/-- Checked non-completion equality for downstream public backfill. -/
theorem terminalSerrinCriterionCompleted_eq_false :
    terminalSerrinCriterionCompleted = false :=
  rfl

/-- Checked no-residual-integration-debt gate for downstream public backfill. -/
theorem completedStateRetainsRepoLocalIntegrationDebt_eq_false :
    completedStateRetainsRepoLocalIntegrationDebt = false :=
  rfl

/-! ## Audit probes -/

#check MeasureTheory.MemLp
#check MeasureTheory.MemLp.aestronglyMeasurable
#check MeasureTheory.MemLp.eLpNorm_lt_top
#check MeasureTheory.eLpNorm
#check MeasureTheory.Measure.prod
#check AEMeasurable
#check Distribution
#check TestFunction
#check LineDeriv.iteratedLineDerivOp
#check Laplacian.laplacian
#check ContDiff
#check ContDiffOn
#check fderiv
#check mathlibAnchorRevision
#check c003RequestedAnchorNames
#check mathlibAnchorRevision_eq
#check c004PublicBlocker
#check c004PublicBlocker_eq
#check pinnedMathlibTerminalSerrinTheoremFoundInThisPass_eq_false
#check externalLeanTerminalSerrinTheoremFoundInThisPass_eq_false
#check c005TheoremTreeLeaves
#check c005TheoremTreeLeaves_length
#check c005UncheckedTerminalLeaves
#check c005UncheckedTerminalLeaves_eq
#check c005EveryLeafWithinBudget
#check c005TerminalTheoremCompleted_eq_false
#check spatialELpNormProfile
#check MixedLqLpFollowUpSpec
#check c006_productMeasure_eq
#check c006_spatialSliceMemLp
#check c006_spatialProfileAEMeasurable
#check c006_mixedTimeMemLp
#check c006_mixedTimeELpNorm_lt_top
#check c006MixedNormFollowUpLeaves
#check c006MixedNormFollowUpLeaves_length
#check c006UncheckedMixedNormLeaves
#check c006UncheckedMixedNormLeaves_eq
#check c006EveryMixedNormLeafWithinBudget
#check c006MixedNormFollowUpTaskCreated_eq_true
#check c006TrueMixedNormProofCompleted_eq_false
#check LerayHopfEnergyInequalityFields
#check WeakIncompressibleNavierStokesFollowUpSpec
#check c007_spaceTimeMeasure_eq_prod
#check c007_weakMomentumEquation
#check c007_divergenceFreeWeak
#check c007_lerayHopfVelocity_eq
#check c007_kineticEnergyAEMeasurable
#check c007_viscousDissipationAEMeasurable
#check c007_lerayHopfEnergyInequality
#check c007WeakNavierStokesFollowUpLeaves
#check c007WeakNavierStokesFollowUpLeaves_length
#check c007UncheckedWeakNavierStokesLeaves
#check c007UncheckedWeakNavierStokesLeaves_eq
#check c007EveryWeakNavierStokesLeafWithinBudget
#check c007WeakNavierStokesFollowUpTaskCreated_eq_true
#check c007WeakNavierStokesProofCompleted_eq_false
#check c007LerayHopfEnergyInequalityProofCompleted_eq_false
#check C008ExternalLeanAuditRecord
#check c008RequestedSearchTerms
#check c008RequestedSearchTerms_length
#check c008ExternalLeanAuditRecords
#check c008ExternalLeanAuditRecords_length
#check c008GitHubCliAuthenticated_eq_false
#check c008AcceptedExternalTerminalProofFound_eq_false
#check c008DependencyIntegrationTaskRequiredNow_eq_false
#check c008RemainingAuditLeaves
#check c008RemainingAuditLeaves_length
#check SharedImportAggregatorDecision
#check SharedImportAggregatorDecisionStatus
#check c009SharedImportAggregatorDecisionStatus
#check c009_shared_import_aggregator_decision_local_checked

end S1_M_157
end Stage1
end AwesomeTheorems
