import Statement

/-!
# THM-M-0995 obligation-tree composition probe

This file gives the frozen proof packages Lean types and checks only their
child-to-parent composition.  It deliberately does not discharge any package.
-/

noncomputable section

namespace Stage1Instances.THM_M_0995.ObligationTree

open Stage1Instances.THM_M_0995
open MeasureTheory ProbabilityTheory

universe u

/-- The exact canonical root, without a wrapper-level change of statement. -/
abbrev Root : Prop := StatementShape.{u}

/-- Per-summand Bernstein MGF estimate, including its admissible tilt range. -/
def IndividualMGFPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (P : BoundedSummandProblem Omega) (i : Nat) (s : Real),
      i < P.n -> 0 <= s -> s * P.bound < 3 ->
      (∫ omega, Real.exp (s * P.X i omega) ∂P.mu) <=
        Real.exp (s ^ 2 * Var[P.X i; P.mu] /
          (2 * (1 - s * P.bound / 3)))

/-- Independent-product and variance-budget package for the finite sum MGF. -/
def SumMGFPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (P : BoundedSummandProblem Omega) (s : Real),
      0 <= s -> s * P.bound < 3 ->
      (∫ omega, Real.exp (s * partialSum P.n P.X omega) ∂P.mu) <=
        Real.exp (s ^ 2 * P.varianceBudget /
          (2 * (1 - s * P.bound / 3)))

/-- Exponential Markov specialized to the canonical sum and event. -/
def ChernoffPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (P : BoundedSummandProblem Omega) (s t : Real),
      0 <= s ->
      P.mu.real {omega | t <= partialSum P.n P.X omega} <=
        Real.exp (-s * t) *
          (∫ omega, Real.exp (s * partialSum P.n P.X omega) ∂P.mu)

/-- Algebraic tilt choice and exponent comparison for a positive denominator. -/
def OptimizeExponentPackage : Prop :=
  forall v b t : Real, 0 <= v -> 0 <= b -> 0 <= t ->
    0 < v + b * t / 3 ->
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

/-- Exact parent interface; the proof phase must implement this implication. -/
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

end Stage1Instances.THM_M_0995.ObligationTree

#check Stage1Instances.THM_M_0995.ObligationTree.root_compose
#print axioms Stage1Instances.THM_M_0995.ObligationTree.root_compose
