import Statement

/-!
# THM-M-0995 obligation-tree composition probes

This file retains the registry-v1 package types and adds the registry-v2
correction forced by the false boundary case in `OptimizeExponentPackage`.
It checks only child-to-parent composition and deliberately discharges no
analytic package.
-/

noncomputable section

namespace Stage1Instances.THM_M_0995.ObligationTree

open Stage1Instances.THM_M_0995
open MeasureTheory ProbabilityTheory

universe u

/-- The exact canonical root, without a wrapper-level change of statement. -/
abbrev Root : Prop := StatementShape.{u}

/-- Scalar exponential remainder estimate used by the individual MGF proof. -/
def ExpRemainderPackage : Prop :=
  forall x c : Real, |x| <= c -> c < 3 ->
    Real.exp x - 1 - x <= x ^ 2 / (2 * (1 - c / 3))

/-- Per-summand Bernstein MGF estimate, including its admissible tilt range. -/
def IndividualMGFPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (P : BoundedSummandProblem Omega) (i : Nat) (s : Real),
      i < P.n -> 0 <= s -> s * P.bound < 3 ->
      (∫ omega, Real.exp (s * P.X i omega) ∂P.mu) <=
        Real.exp (s ^ 2 * Var[P.X i; P.mu] /
          (2 * (1 - s * P.bound / 3)))

/-- Conditional composition interface from the scalar estimate to one summand. -/
def IndividualMGFAssemblyPackage : Prop :=
  ExpRemainderPackage ->
    forall (Omega : Type u) [MeasurableSpace Omega]
      (P : BoundedSummandProblem Omega) (i : Nat) (s : Real),
        i < P.n -> 0 <= s -> s * P.bound < 3 ->
        (∫ omega, Real.exp (s * P.X i omega) ∂P.mu) <=
          Real.exp (s ^ 2 * Var[P.X i; P.mu] /
            (2 * (1 - s * P.bound / 3)))

/-- Exact scalar-to-individual-MGF composition probe. -/
theorem individualMGF_compose
    (hExp : ExpRemainderPackage)
    (hAssembly : IndividualMGFAssemblyPackage.{u}) : IndividualMGFPackage.{u} :=
  hAssembly hExp

/-- Independent-product and variance-budget package for the finite sum MGF. -/
def SumMGFPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (P : BoundedSummandProblem Omega) (s : Real),
      0 <= s -> s * P.bound < 3 ->
      (∫ omega, Real.exp (s * partialSum P.n P.X omega) ∂P.mu) <=
        Real.exp (s ^ 2 * P.varianceBudget /
          (2 * (1 - s * P.bound / 3)))

/-- Independent finite-prefix MGF factorization before applying term bounds. -/
def PrefixMGFPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega] (mu : Measure Omega)
    (n : Nat) (X : Nat -> Omega -> Real) (s : Real),
      iIndepFun X mu ->
      (forall i, i < n -> AEMeasurable (X i) mu) ->
      (∫ omega, Real.exp (s * partialSum n X omega) ∂mu) =
        ∏ i ∈ Finset.range n, (∫ omega, Real.exp (s * X i omega) ∂mu)

/-- Conditional composition interface for the independent finite-sum MGF. -/
def SumMGFAssemblyPackage : Prop :=
  IndividualMGFPackage.{u} -> PrefixMGFPackage.{u} ->
    forall (Omega : Type u) [MeasurableSpace Omega]
      (P : BoundedSummandProblem Omega) (s : Real),
        0 <= s -> s * P.bound < 3 ->
        (∫ omega, Real.exp (s * partialSum P.n P.X omega) ∂P.mu) <=
          Real.exp (s ^ 2 * P.varianceBudget /
            (2 * (1 - s * P.bound / 3)))

/-- Exact individual/prefix-to-sum-MGF composition probe. -/
theorem sumMGF_compose
    (hIndividual : IndividualMGFPackage.{u})
    (hPrefix : PrefixMGFPackage.{u})
    (hAssembly : SumMGFAssemblyPackage.{u}) : SumMGFPackage.{u} :=
  hAssembly hIndividual hPrefix

/-- Exponential Markov specialized to the canonical sum and event. -/
def ChernoffPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (P : BoundedSummandProblem Omega) (s t : Real),
      0 <= s ->
      P.mu.real {omega | t <= partialSum P.n P.X omega} <=
        Real.exp (-s * t) *
          (∫ omega, Real.exp (s * partialSum P.n P.X omega) ∂P.mu)

/-- Registry-v1 interface, retained because its `v = 0` boundary is false. -/
def OptimizeExponentPackage : Prop :=
  forall v b t : Real, 0 <= v -> 0 <= b -> 0 <= t ->
    0 < v + b * t / 3 ->
    let s := t / (v + b * t / 3)
    0 <= s ∧ s * b < 3 ∧
      Real.exp (-s * t) * Real.exp (s ^ 2 * v / (2 * (1 - s * b / 3))) <=
        Real.exp (-(t ^ 2) / (2 * (v + b * t / 3)))

/-- Corrected optimizer interface on the positive-variance branch. -/
def PositiveVarianceOptimizePackage : Prop :=
  forall v b t : Real, 0 < v -> 0 <= b -> 0 <= t ->
    let s := t / (v + b * t / 3)
    0 <= s ∧ s * b < 3 ∧
      Real.exp (-s * t) * Real.exp (s ^ 2 * v / (2 * (1 - s * b / 3))) <=
        Real.exp (-(t ^ 2) / (2 * (v + b * t / 3)))

/-- The totalized zero-denominator boundary, where the usual tilt is unavailable. -/
def ZeroDenominatorPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (P : BoundedSummandProblem Omega) (t : Real),
      0 <= t -> P.varianceBudget + P.bound * t / 3 = 0 ->
      P.mu.real {omega | t <= partialSum P.n P.X omega} <=
        Real.exp (-(t ^ 2) /
          (2 * (P.varianceBudget + P.bound * t / 3)))

/-- Zero variance forces the canonical partial sum to vanish almost everywhere. -/
def VarianceZeroAEPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (P : BoundedSummandProblem Omega),
      P.varianceBudget = 0 ->
      ∀ᵐ omega ∂P.mu, partialSum P.n P.X omega = 0

/-- Exact root conclusion restricted to the zero-variance branch. -/
def ZeroVariancePackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (P : BoundedSummandProblem Omega) (t : Real),
      0 <= t -> P.varianceBudget = 0 ->
      P.mu.real {omega | t <= partialSum P.n P.X omega} <=
        Real.exp (-(t ^ 2) /
          (2 * (P.varianceBudget + P.bound * t / 3)))

/-- Conditional composition interface for the complete zero-variance branch. -/
def ZeroVarianceAssemblyPackage : Prop :=
  ZeroDenominatorPackage.{u} -> VarianceZeroAEPackage.{u} ->
    forall (Omega : Type u) [MeasurableSpace Omega]
      (P : BoundedSummandProblem Omega) (t : Real),
        0 <= t -> P.varianceBudget = 0 ->
        P.mu.real {omega | t <= partialSum P.n P.X omega} <=
          Real.exp (-(t ^ 2) /
            (2 * (P.varianceBudget + P.bound * t / 3)))

/-- Exact zero-denominator/variance-zero composition probe. -/
theorem zeroVariance_compose
    (hZeroDenominator : ZeroDenominatorPackage.{u})
    (hVarianceZero : VarianceZeroAEPackage.{u})
    (hAssembly : ZeroVarianceAssemblyPackage.{u}) : ZeroVariancePackage.{u} :=
  hAssembly hZeroDenominator hVarianceZero

/-- Registry-v1 parent interface, retained as the historical failed route. -/
def AssemblyPackage : Prop :=
  IndividualMGFPackage.{u} -> SumMGFPackage.{u} -> ChernoffPackage.{u} ->
    OptimizeExponentPackage -> ZeroDenominatorPackage.{u} -> Root.{u}

/-- Kernel-checked child-to-parent composition, conditional on every open package. -/
theorem root_compose
    (hIndividual : IndividualMGFPackage.{u})
    (hSum : SumMGFPackage.{u})
    (hChernoff : ChernoffPackage.{u})
    (hOptimize : OptimizeExponentPackage)
    (hZero : ZeroDenominatorPackage.{u})
    (hAssembly : AssemblyPackage.{u}) : Root.{u} :=
  hAssembly hIndividual hSum hChernoff hOptimize hZero

/-- Registry-v2 parent interface with the exhaustive variance split. -/
def AssemblyPackageV2 : Prop :=
  SumMGFPackage.{u} -> ChernoffPackage.{u} -> PositiveVarianceOptimizePackage ->
    ZeroVariancePackage.{u} ->
    forall (Omega : Type u) [MeasurableSpace Omega]
      (P : BoundedSummandProblem Omega) (t : Real),
        0 <= t ->
        P.mu.real {omega | t <= partialSum P.n P.X omega} <=
          Real.exp (-(t ^ 2) /
            (2 * (P.varianceBudget + P.bound * t / 3)))

/-- Corrected child-to-parent composition for the exact canonical root. -/
theorem root_compose_v2
    (hSum : SumMGFPackage.{u})
    (hChernoff : ChernoffPackage.{u})
    (hOptimize : PositiveVarianceOptimizePackage)
    (hZeroVariance : ZeroVariancePackage.{u})
    (hAssembly : AssemblyPackageV2.{u}) : Root.{u} :=
  hAssembly hSum hChernoff hOptimize hZeroVariance

end Stage1Instances.THM_M_0995.ObligationTree

#check Stage1Instances.THM_M_0995.ObligationTree.root_compose
#check Stage1Instances.THM_M_0995.ObligationTree.individualMGF_compose
#check Stage1Instances.THM_M_0995.ObligationTree.sumMGF_compose
#check Stage1Instances.THM_M_0995.ObligationTree.zeroVariance_compose
#check Stage1Instances.THM_M_0995.ObligationTree.root_compose_v2
#print axioms Stage1Instances.THM_M_0995.ObligationTree.root_compose
#print axioms Stage1Instances.THM_M_0995.ObligationTree.individualMGF_compose
#print axioms Stage1Instances.THM_M_0995.ObligationTree.sumMGF_compose
#print axioms Stage1Instances.THM_M_0995.ObligationTree.zeroVariance_compose
#print axioms Stage1Instances.THM_M_0995.ObligationTree.root_compose_v2
