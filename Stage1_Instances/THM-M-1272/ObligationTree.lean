import Statement

/-!
# THM-M-1272 conditional obligation composition

This module checks the final composition selected by the frozen architecture.
The symmetric minimax and compactness packages remain explicit hypotheses, so
this file does not prove the Fountain theorem.
-/

noncomputable section

open Filter Set
open scoped Topology

namespace Stage1Instances.THM_M_1272

universe u

/-- The open symmetric-minimax package: geometry produces divergent minimax
levels and a Palais-Smale sequence at every level. -/
def FountainMinimaxPackage : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
      [CompleteSpace E] (e : Nat -> E) (Phi : E -> Real),
    Orthonormal Real e ->
    (Submodule.span Real (Set.range e)).topologicalClosure = (⊤ : Submodule Real E) ->
    ContDiff Real 1 Phi ->
    (forall x, Phi (-x) = Phi x) ->
    HasFountainGeometry Phi e ->
    exists c : Nat -> Real, exists v : Nat -> Nat -> E,
      Tendsto c atTop atTop /\
      (forall k, Tendsto (fun n => Phi (v k n)) atTop (nhds (c k))) /\
      (forall k, Tendsto (fun n => norm (fderiv Real Phi (v k n))) atTop (nhds 0))

/-- The open compactness package: levelwise Palais-Smale data has critical
representatives at exactly the specified levels. -/
def FountainLimitPackage : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
      [CompleteSpace E] (Phi : E -> Real) (c : Nat -> Real)
      (v : Nat -> Nat -> E),
    ContDiff Real 1 Phi -> PalaisSmale Phi ->
    (forall k, Tendsto (fun n => Phi (v k n)) atTop (nhds (c k))) ->
    (forall k, Tendsto (fun n => norm (fderiv Real Phi (v k n))) atTop (nhds 0)) ->
    exists u : Nat -> E,
      (forall k, IsCriticalPoint Phi (u k)) /\ (forall k, Phi (u k) = c k)

/-- Kernel-checked conditional composition into the exact canonical target. -/
theorem root_of_minimax_and_limit_packages
    (minimax : FountainMinimaxPackage.{u})
    (limits : FountainLimitPackage.{u}) :
    FountainTheoremTarget.{u} := by
  intro E _group _inner _complete e Phi he htotal hC1 heven hPS hgeometry
  obtain ⟨c, v, hc, hv, hd⟩ := minimax E e Phi he htotal hC1 heven hgeometry
  obtain ⟨u, hu, hvalue⟩ := limits E Phi c v hC1 hPS hv hd
  refine ⟨u, hu, ?_⟩
  exact hc.congr' (Filter.Eventually.of_forall (fun k => (hvalue k).symm))

#print axioms root_of_minimax_and_limit_packages

end Stage1Instances.THM_M_1272
