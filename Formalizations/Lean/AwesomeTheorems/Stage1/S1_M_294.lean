import Mathlib.MeasureTheory.Function.ConvergenceInDistribution
import Mathlib.Probability.Independence.Basic

/-!
# S1-M-294 / THM-M-1015: Slutsky theorem

This Stage1 artifact records a repo-local Lean wrapper around the Slutsky
theorem family already present in the pinned mathlib snapshot.

The upstream theorem
`MeasureTheory.TendstoInDistribution.prodMk_of_tendstoInMeasure_const` proves
the product-pair form: if `X n` converges in distribution to `Z` and `Y n`
converges in probability to a constant `c`, then `(X n, Y n)` converges in
distribution to `(Z, c)`.  Mathlib also exposes the continuous-map corollary
and an additive specialization.  This file checks real-valued wrappers for the
pair, addition, and multiplication forms used by the standard Slutsky theorem.

No quotient/division form is claimed here: that needs a localized continuous
mapping theorem away from the zero denominator or an explicit denominator
non-vanishing package.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory
open scoped Topology MeasureTheory ProbabilityTheory ENNReal NNReal

namespace AwesomeTheorems.Stage1.S1_M_294

universe u v w

/--
Real-valued Slutsky conclusion package for one shared source probability space
and one possible separate limit probability space.

The package includes:
* pair convergence `(X n, Y n) =>d (Z, c)`;
* additive Slutsky `X n + Y n =>d Z + c`;
* multiplicative Slutsky `X n * Y n =>d Z * c`.
-/
def SlutskyConclusion {ι : Type u} {Ω : Type v} {ΩL : Type w}
    [MeasurableSpace Ω] [MeasurableSpace ΩL]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (μL : Measure ΩL) [IsProbabilityMeasure μL]
    (l : Filter ι) (X Y : ι → Ω → ℝ) (Z : ΩL → ℝ) (c : ℝ) : Prop :=
  TendstoInDistribution (fun n ω => (X n ω, Y n ω)) l (fun ω => (Z ω, c))
      (fun _ : ι => μ) μL ∧
    TendstoInDistribution (fun n ω => X n ω + Y n ω) l (fun ω => Z ω + c)
      (fun _ : ι => μ) μL ∧
    TendstoInDistribution (fun n ω => X n ω * Y n ω) l (fun ω => Z ω * c)
      (fun _ : ι => μ) μL

/--
Stage1 normalized statement shape for the standard real-valued Slutsky package.

The source variables `X` and `Y` live on the same probability space because
pointwise combinations such as `X n + Y n` and `X n * Y n` require a common
sample point.  The limit variable `Z` may live on a separate probability space,
matching mathlib's `TendstoInDistribution` API.
-/
def StatementShape : Prop :=
  ∀ (ι : Type u) (Ω : Type v) (ΩL : Type w)
    [MeasurableSpace Ω] [MeasurableSpace ΩL]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (μL : Measure ΩL) [IsProbabilityMeasure μL]
    (l : Filter ι) [l.IsCountablyGenerated]
    (X Y : ι → Ω → ℝ) (Z : ΩL → ℝ) (c : ℝ),
      TendstoInDistribution X l Z (fun _ : ι => μ) μL →
      TendstoInMeasure μ Y l (fun _ : Ω => c) →
      (∀ i, AEMeasurable (Y i) μ) →
      SlutskyConclusion μ μL l X Y Z c

/--
Repo-local wrapper for mathlib's pair-valued Slutsky theorem.
-/
theorem slutsky_pair_real
    {ι : Type u} {Ω : Type v} {ΩL : Type w}
    [MeasurableSpace Ω] [MeasurableSpace ΩL]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (μL : Measure ΩL) [IsProbabilityMeasure μL]
    {l : Filter ι} [l.IsCountablyGenerated]
    {X Y : ι → Ω → ℝ} {Z : ΩL → ℝ} {c : ℝ}
    (hXZ : TendstoInDistribution X l Z (fun _ : ι => μ) μL)
    (hY : TendstoInMeasure μ Y l (fun _ : Ω => c))
    (hYmeas : ∀ i, AEMeasurable (Y i) μ) :
    TendstoInDistribution (fun n ω => (X n ω, Y n ω)) l (fun ω => (Z ω, c))
      (fun _ : ι => μ) μL :=
  hXZ.prodMk_of_tendstoInMeasure_const X Y Z hY hYmeas

/--
Repo-local wrapper for the additive Slutsky specialization in mathlib.
-/
theorem slutsky_add_real
    {ι : Type u} {Ω : Type v} {ΩL : Type w}
    [MeasurableSpace Ω] [MeasurableSpace ΩL]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (μL : Measure ΩL) [IsProbabilityMeasure μL]
    {l : Filter ι} [l.IsCountablyGenerated]
    {X Y : ι → Ω → ℝ} {Z : ΩL → ℝ} {c : ℝ}
    (hXZ : TendstoInDistribution X l Z (fun _ : ι => μ) μL)
    (hY : TendstoInMeasure μ Y l (fun _ : Ω => c))
    (hYmeas : ∀ i, AEMeasurable (Y i) μ) :
    TendstoInDistribution (fun n ω => X n ω + Y n ω) l (fun ω => Z ω + c)
      (fun _ : ι => μ) μL :=
  hXZ.add_of_tendstoInMeasure_const hY hYmeas

/--
Multiplicative Slutsky wrapper, obtained from mathlib's continuous-function
Slutsky theorem with the globally continuous multiplication map on `R x R`.
-/
theorem slutsky_mul_real
    {ι : Type u} {Ω : Type v} {ΩL : Type w}
    [MeasurableSpace Ω] [MeasurableSpace ΩL]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (μL : Measure ΩL) [IsProbabilityMeasure μL]
    {l : Filter ι} [l.IsCountablyGenerated]
    {X Y : ι → Ω → ℝ} {Z : ΩL → ℝ} {c : ℝ}
    (hXZ : TendstoInDistribution X l Z (fun _ : ι => μ) μL)
    (hY : TendstoInMeasure μ Y l (fun _ : Ω => c))
    (hYmeas : ∀ i, AEMeasurable (Y i) μ) :
    TendstoInDistribution (fun n ω => X n ω * Y n ω) l (fun ω => Z ω * c)
      (fun _ : ι => μ) μL := by
  simpa using hXZ.continuous_comp_prodMk_of_tendstoInMeasure_const
    (g := fun p : ℝ × ℝ => p.1 * p.2) (by fun_prop) hY hYmeas

/--
The normalized Stage1 statement is locally closed by wrappers over the pinned
mathlib Slutsky theorem family.
-/
theorem statementShape_local_wrapper : StatementShape.{u, v, w} := by
  intro ι Ω ΩL _ _ μ _ μL _ l _ X Y Z c hXZ hY hYmeas
  exact ⟨slutsky_pair_real μ μL hXZ hY hYmeas,
    slutsky_add_real μ μL hXZ hY hYmeas,
    slutsky_mul_real μ μL hXZ hY hYmeas⟩

/-- mathlib modules checked while locating anchors for this slot. -/
def mathlibAnchorModules : List String := [
  "Mathlib.MeasureTheory.Function.ConvergenceInMeasure",
  "Mathlib.MeasureTheory.Function.ConvergenceInDistribution",
  "Mathlib.MeasureTheory.Measure.Portmanteau",
  "Mathlib.MeasureTheory.Measure.ProbabilityMeasure",
  "Mathlib.Probability.IdentDistrib",
  "Mathlib.Probability.Independence.Basic"
]

/-- Checked declaration names used or audited for this Stage1 slot. -/
def mathlibAnchorNames : List String := [
  "MeasureTheory.TendstoInMeasure",
  "MeasureTheory.TendstoInDistribution",
  "MeasureTheory.tendstoInDistribution_of_tendstoInMeasure_sub",
  "MeasureTheory.TendstoInMeasure.tendstoInDistribution",
  "MeasureTheory.TendstoInDistribution.prodMk_of_tendstoInMeasure_const",
  "MeasureTheory.TendstoInDistribution.continuous_comp_prodMk_of_tendstoInMeasure_const",
  "MeasureTheory.TendstoInDistribution.add_of_tendstoInMeasure_const",
  "MeasureTheory.TendstoInDistribution.continuous_comp",
  "ProbabilityTheory.IdentDistrib",
  "ProbabilityTheory.IndepFun",
  "ProbabilityTheory.iIndepFun"
]

/--
Pinned primary-source URLs for the upstream Lean 4 anchors.  These URLs point at
the mathlib commit pinned by `Formalizations/Lean/lakefile.lean`.
-/
def primarySourceUrls : List String := [
  "https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/MeasureTheory/Function/ConvergenceInDistribution.lean",
  "https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/MeasureTheory/Function/ConvergenceInMeasure.lean",
  "https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/Probability/IdentDistrib.lean",
  "https://github.com/leanprover-community/mathlib4/blob/8a178386ffc0f5fef0b77738bb5449d50efeea95/Mathlib/Probability/Independence/Basic.lean"
]

/--
Search terms checked in the pinned local mathlib snapshot before selecting the
repo-local wrapper boundary.
-/
def auditSearchTerms : List String := [
  "Slutsky",
  "slutsky",
  "TendstoInMeasure",
  "TendstoInDistribution",
  "prodMk_of_tendstoInMeasure_const",
  "continuous_comp_prodMk_of_tendstoInMeasure_const",
  "add_of_tendstoInMeasure_const",
  "convergence in probability",
  "IdentDistrib",
  "IndepFun",
  "iIndepFun"
]

/-! ## Audit probes retained in the checked file. -/

#check SlutskyConclusion
#check StatementShape
#check statementShape_local_wrapper
#check slutsky_pair_real
#check slutsky_add_real
#check slutsky_mul_real
#check MeasureTheory.TendstoInMeasure
#check MeasureTheory.TendstoInDistribution
#check MeasureTheory.tendstoInDistribution_of_tendstoInMeasure_sub
#check MeasureTheory.TendstoInMeasure.tendstoInDistribution
#check MeasureTheory.TendstoInDistribution.prodMk_of_tendstoInMeasure_const
#check MeasureTheory.TendstoInDistribution.continuous_comp_prodMk_of_tendstoInMeasure_const
#check MeasureTheory.TendstoInDistribution.add_of_tendstoInMeasure_const
#check MeasureTheory.TendstoInDistribution.continuous_comp
#check ProbabilityTheory.IdentDistrib
#check ProbabilityTheory.IndepFun
#check ProbabilityTheory.iIndepFun

end AwesomeTheorems.Stage1.S1_M_294
