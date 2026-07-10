import Mathlib.Probability.Martingale.OptionalStopping
import Mathlib.MeasureTheory.Function.LpSeminorm.Basic

/-!
# S1-M-285 / THM-M-1005: Doob inequality, Stage1 wrapper

This Stage1 artifact records the current Lean 4 boundary for Doob's
inequality.  The pinned mathlib snapshot contains the finite-horizon Doob
maximal inequality for nonnegative real-valued submartingales as
`MeasureTheory.maximal_ineq`; it does not yet close the stronger Doob Lp
moment estimate.  Accordingly, this file proves only the mathlib-backed
maximal-inequality wrapper and keeps the Lp estimate as a precise statement
shape.  It introduces no proof-placeholder declarations.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal NNReal MeasureTheory ProbabilityTheory

namespace AwesomeTheorems.Stage1.S1_M_285

universe u

/-- Running finite maximum `max_{k <= n} f k omega` in mathlib's finite-horizon form. -/
def runningMax {Omega : Type u} (f : Nat -> Omega -> Real) (n : Nat) (omega : Omega) : Real :=
  (Finset.range (n + 1)).sup' Finset.nonempty_range_add_one fun k => f k omega

/-- Running finite maximum `max_{k <= n} |f k omega|`, used for the Lp boundary. -/
def runningAbsMax {Omega : Type u} (f : Nat -> Omega -> Real) (n : Nat) (omega : Omega) :
    Real :=
  (Finset.range (n + 1)).sup' Finset.nonempty_range_add_one fun k => |f k omega|

/--
Measurability of the finite running absolute maximum.

This closes the local measurability leaf needed before the Lp/moment branch can
be attacked through layer-cake or `eLpNorm` APIs.
-/
theorem measurable_runningAbsMax {Omega : Type u} [MeasurableSpace Omega]
    {f : Nat -> Omega -> Real} {n : Nat} (hf : forall k, k <= n -> Measurable (f k)) :
    Measurable (runningAbsMax f n) := by
  simpa [runningAbsMax] using
    (Finset.measurable_range_sup'' (n := n) (f := fun k omega => |f k omega|)
      (by
        intro k hk
        simpa only [Real.norm_eq_abs] using (hf k hk).norm))

/-- A.e.-measurability corollary for the running absolute maximum. -/
theorem aemeasurable_runningAbsMax {Omega : Type u} [MeasurableSpace Omega]
    {mu : Measure Omega} {f : Nat -> Omega -> Real} {n : Nat}
    (hf : forall k, k <= n -> Measurable (f k)) :
    AEMeasurable (runningAbsMax f n) mu :=
  (measurable_runningAbsMax (n := n) hf).aemeasurable

/-- Event that the finite running maximum crosses the nonnegative threshold `epsilon`. -/
def maximalEvent {Omega : Type u} (f : Nat -> Omega -> Real) (epsilon : NNReal) (n : Nat) :
    Set Omega :=
  {omega | (epsilon : Real) <= runningMax f n omega}

/--
Mathlib-backed finite-horizon Doob maximal inequality shape.

This is the checked part of the Stage1 artifact.  It is the theorem currently
named `MeasureTheory.maximal_ineq` in pinned mathlib, rewritten through local
notation.
-/
def FiniteHorizonMaximalInequalityStatement : Prop :=
  forall (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
    [IsFiniteMeasure mu] (G : Filtration Nat mOmega) (f : Nat -> Omega -> Real),
      Submartingale f G mu ->
        0 <= f ->
          forall {epsilon : NNReal} (n : Nat),
            epsilon * mu (maximalEvent f epsilon n) <=
              ENNReal.ofReal (∫ omega in maximalEvent f epsilon n, f n omega ∂mu)

/--
Stage1 boundary for the stronger Doob Lp estimate.

The intended analytic content is the usual finite-horizon bound
`||max_{k <= n} |M_k|||_p <= (p / (p - 1)) ||M_n||_p` for `1 < p < infinity`.
The statement is retained as a candidate target because the audited mathlib
file says the Lp inequality is future work rather than a current theorem.
-/
def DoobLpMomentEstimateStatement : Prop :=
  forall (Omega : Type u) [mOmega : MeasurableSpace Omega] (mu : Measure Omega)
    [IsFiniteMeasure mu] (G : Filtration Nat mOmega) (f : Nat -> Omega -> Real),
      Martingale f G mu ->
        forall (p : ENNReal), 1 < p -> p < (⊤ : ENNReal) -> forall n : Nat,
          eLpNorm (runningAbsMax f n) p mu <=
            ENNReal.ofReal (p.toReal / (p.toReal - 1)) * eLpNorm (f n) p mu

/--
Combined Stage1 statement shape for THM-M-1005.

The first conjunct is closed locally by `finiteHorizonMaximalInequality_mathlib`.
The second conjunct is the intended Lp/moment estimate boundary and is not
proved in this file.
-/
def StatementShape : Prop :=
  FiniteHorizonMaximalInequalityStatement.{u} ∧ DoobLpMomentEstimateStatement.{u}

/-- Checked wrapper around mathlib's finite-horizon Doob maximal inequality. -/
theorem finiteHorizonMaximalInequality_mathlib {Omega : Type u} [mOmega : MeasurableSpace Omega]
    {mu : Measure Omega} [IsFiniteMeasure mu] {G : Filtration Nat mOmega}
    {f : Nat -> Omega -> Real} (hsub : Submartingale f G mu) (hnonneg : 0 <= f)
    {epsilon : NNReal} (n : Nat) :
    epsilon * mu (maximalEvent f epsilon n) <=
      ENNReal.ofReal (∫ omega in maximalEvent f epsilon n, f n omega ∂mu) := by
  simpa [maximalEvent, runningMax] using
    (MeasureTheory.maximal_ineq (𝒢 := G) (f := f) hsub hnonneg (ε := epsilon) n)

/-- The checked mathlib wrapper closes the finite-horizon part of the Stage1 statement. -/
theorem finiteHorizonMaximalInequalityStatement_mathlib :
    FiniteHorizonMaximalInequalityStatement := by
  intro Omega mOmega mu hmu G f hsub hnonneg epsilon n
  exact finiteHorizonMaximalInequality_mathlib (mu := mu) (G := G) (f := f) hsub hnonneg n

/--
Checked martingale-specialized finite-horizon maximal inequality.

This does not close the Lp/moment branch; it only records that the already
checked nonnegative-submartingale wrapper is immediately available for
nonnegative martingales through mathlib's `Martingale.submartingale` API.
-/
theorem finiteHorizonMaximalInequality_martingale_mathlib {Omega : Type u}
    [mOmega : MeasurableSpace Omega] {mu : Measure Omega} [IsFiniteMeasure mu]
    {G : Filtration Nat mOmega} {f : Nat -> Omega -> Real} (hf : Martingale f G mu)
    (hnonneg : 0 <= f) {epsilon : NNReal} (n : Nat) :
    epsilon * mu (maximalEvent f epsilon n) <=
      ENNReal.ofReal (∫ omega in maximalEvent f epsilon n, f n omega ∂mu) :=
  finiteHorizonMaximalInequality_mathlib (mu := mu) (G := G) (f := f)
    hf.submartingale hnonneg n

/--
If a later package supplies the Lp estimate, this wrapper combines it with the
already checked mathlib maximal-inequality branch.
-/
theorem statementShape_from_lp_boundary (hLp : DoobLpMomentEstimateStatement.{u}) :
    StatementShape.{u} :=
  ⟨finiteHorizonMaximalInequalityStatement_mathlib, hLp⟩

/--
Completion gate for the current Stage1 target: a proof of the combined Doob
statement necessarily includes the stronger Lp/moment boundary.
-/
theorem statementShape_requires_lp_boundary (h : StatementShape.{u}) :
    DoobLpMomentEstimateStatement.{u} :=
  h.2

/--
Exact completion gate for the current combined Stage1 target.

Because the finite maximal inequality branch is already closed by the checked
mathlib wrapper, proving the combined `StatementShape` is now equivalent to
proving the stronger Lp/moment boundary.  Thus `MeasureTheory.maximal_ineq`
alone can justify only a narrowed finite-maximal public target, not completion
of the current Doob Lp/moment wording.
-/
theorem statementShape_iff_lp_boundary :
    StatementShape.{u} ↔ DoobLpMomentEstimateStatement.{u} := by
  constructor
  · exact statementShape_requires_lp_boundary
  · exact statementShape_from_lp_boundary

/-- A martingale is a submartingale in mathlib's process API. -/
theorem martingale_submartingale_wrapper {Omega : Type u} [mOmega : MeasurableSpace Omega]
    {mu : Measure Omega} {G : Filtration Nat mOmega} {f : Nat -> Omega -> Real}
    (hf : Martingale f G mu) :
    Submartingale f G mu :=
  hf.submartingale

/-- Checked declaration and search-name anchors retained for the Stage1 audit ledger. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.maximal_ineq",
  "MeasureTheory.smul_le_stoppedValue_hittingBtwn",
  "MeasureTheory.Submartingale.expected_stoppedValue_mono",
  "MeasureTheory.submartingale_iff_expected_stoppedValue_mono",
  "MeasureTheory.Submartingale.stoppedProcess",
  "MeasureTheory.hittingBtwn",
  "MeasureTheory.stoppedValue",
  "MeasureTheory.Martingale.submartingale",
  "AwesomeTheorems.Stage1.S1_M_285.finiteHorizonMaximalInequality_martingale_mathlib",
  "AwesomeTheorems.Stage1.S1_M_285.measurable_runningAbsMax",
  "AwesomeTheorems.Stage1.S1_M_285.aemeasurable_runningAbsMax",
  "AwesomeTheorems.Stage1.S1_M_285.statementShape_requires_lp_boundary",
  "AwesomeTheorems.Stage1.S1_M_285.statementShape_iff_lp_boundary",
  "MeasureTheory.eLpNorm"
]

/-- mathlib modules audited for this Stage1 slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.Probability.Martingale.OptionalStopping",
  "Mathlib.Probability.Martingale.Basic",
  "Mathlib.Probability.Process.Filtration",
  "Mathlib.Probability.Process.Stopping",
  "Mathlib.Probability.Process.HittingTime",
  "Mathlib.Probability.Martingale.Upcrossing",
  "Mathlib.Probability.Martingale.Convergence",
  "Mathlib.MeasureTheory.Function.LpSeminorm.Basic"
]

/-- Search terms used in the pinned local mathlib tree for the anchor audit. -/
def mathlibAuditSearchTerms : List String := [
  "Doob",
  "maximal_ineq",
  "Doob's Lp inequality",
  "martingale maximal inequality",
  "Submartingale.expected_stoppedValue_mono",
  "Submartingale.eLpNorm",
  "Finset.measurable_range_sup''",
  "MeasureTheory.lintegral_layercake",
  "upcrossing",
  "stoppedValue",
  "hittingBtwn"
]

/-- Primary-source pin for the checked mathlib proof body used by this wrapper. -/
def mathlibPrimarySource : String :=
  "https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/Probability/Martingale/OptionalStopping.lean"

/--
Pinned local mathlib revision audited for the Doob Lp/moment branch during
the Stage1 child pass.  This records the exact dependency snapshot for the
negative audit result and is not a theorem-completion claim.
-/
def mathlibAuditRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/--
Concrete integration blocker for the stronger Doob Lp/moment estimate at the
audited mathlib revision.

`MeasureTheory.maximal_ineq` is checked above and closes only the finite
nonnegative-submartingale maximal inequality branch.  The upstream source
comments identify the Lp inequality as a corollary planned for a future PR, so
there is currently no theorem in the pinned local mathlib tree that can be
imported as a proof of `DoobLpMomentEstimateStatement`.
-/
def doobLpMomentIntegrationBlocker : String :=
  "No pinned local mathlib theorem matching DoobLpMomentEstimateStatement was found at revision 8a178386ffc0f5fef0b77738bb5449d50efeea95; OptionalStopping.maximal_ineq is only the finite nonnegative-submartingale maximal inequality, and the source comment says the Doob Lp inequality remains future work."

/-! ## Audit probes retained in the checked file. -/

#check runningMax
#check runningAbsMax
#check measurable_runningAbsMax
#check aemeasurable_runningAbsMax
#check maximalEvent
#check FiniteHorizonMaximalInequalityStatement
#check DoobLpMomentEstimateStatement
#check StatementShape
#check finiteHorizonMaximalInequality_mathlib
#check finiteHorizonMaximalInequalityStatement_mathlib
#check finiteHorizonMaximalInequality_martingale_mathlib
#check statementShape_from_lp_boundary
#check statementShape_requires_lp_boundary
#check statementShape_iff_lp_boundary
#check MeasureTheory.maximal_ineq
#check MeasureTheory.smul_le_stoppedValue_hittingBtwn
#check MeasureTheory.Submartingale.expected_stoppedValue_mono
#check MeasureTheory.submartingale_iff_expected_stoppedValue_mono
#check MeasureTheory.Submartingale.stoppedProcess
#check MeasureTheory.hittingBtwn
#check MeasureTheory.stoppedValue
#check MeasureTheory.Martingale.submartingale
#check MeasureTheory.eLpNorm
#check mathlibAuditRevision
#check doobLpMomentIntegrationBlocker

end AwesomeTheorems.Stage1.S1_M_285
