import Mathlib.Topology.Semicontinuity.Basic

/-!
# THM-M-1270 proof-phase admissions

This module admits the proof bodies that can be closed against the pinned
repository and mathlib snapshot.  In particular, it proves the exact transport
to the frozen statement, the positive-slope algebra, descent invariants,
localization, maximality, witness packaging, and final composition.

It deliberately does not postulate or hide the remaining complete-metric
descent construction.  `target_of_maximalPoint` exposes that frontier as an
ordinary premise.
-/

open Set

namespace Stage1Instances.THM_M_1270.Proof

universe u

/-- The frozen `Statement.lean` target, repeated transparently because dossier
files live outside the Lake library source tree. -/
def ProofTarget : Prop :=
  forall (X : Type u) [MetricSpace X] [CompleteSpace X]
    (f : X -> Real) (epsilon lambda : Real) (x0 : X),
    LowerSemicontinuous f -> BddBelow (range f) ->
      0 < epsilon -> 0 < lambda ->
        (forall x : X, f x0 <= f x + epsilon) ->
          exists v : X, f v <= f x0 /\ dist v x0 <= lambda /\
            forall y : X, y ≠ v ->
              f v < f y + (epsilon / lambda) * dist v y

def ApproximateMinimizer {X : Type u}
    (f : X -> Real) (epsilon : Real) (x0 : X) : Prop :=
  forall x : X, f x0 <= f x + epsilon

def DescentStep {X : Type u} [PseudoMetricSpace X]
    (f : X -> Real) (slope : Real) (x y : X) : Prop :=
  f y + slope * dist x y <= f x

def DescentChain {X : Type u} [PseudoMetricSpace X]
    (f : X -> Real) (slope : Real) (c : Nat -> X) : Prop :=
  forall n : Nat, DescentStep f slope (c n) (c (n + 1))

def DescentMaximalPoint {X : Type u} [PseudoMetricSpace X]
    (f : X -> Real) (epsilon lambda : Real) (x0 v : X) : Prop :=
  f v <= f x0 /\ dist v x0 <= lambda /\
    forall y : X, DescentStep f (epsilon / lambda) v y -> y = v

theorem DescentStep.penalty_le_drop {X : Type u} [PseudoMetricSpace X]
    {f : X -> Real} {slope : Real} {x y : X}
    (h : DescentStep f slope x y) :
    slope * dist x y <= f x - f y := by
  dsimp [DescentStep] at h
  linarith

/-- Positivity of the penalty coefficient used by every descent estimate. -/
theorem slope_pos {epsilon lambda : Real}
    (hepsilon : 0 < epsilon) (hlambda : 0 < lambda) :
    0 < epsilon / lambda :=
  div_pos hepsilon hlambda

/-- Descent steps compose; this is the nesting invariant for successive
descent sets. -/
theorem DescentStep.trans {X : Type u} [PseudoMetricSpace X]
    {f : X -> Real} {slope : Real} {x y z : X}
    (hxy : DescentStep f slope x y)
    (hyz : DescentStep f slope y z)
    (hslope : 0 <= slope) :
    DescentStep f slope x z := by
  dsimp [DescentStep] at hxy hyz ⊢
  have hdist : dist x z <= dist x y + dist y z := dist_triangle _ _ _
  have hmul : slope * dist x z <=
      slope * dist x y + slope * dist y z := by
    calc
      slope * dist x z <= slope * (dist x y + dist y z) :=
        mul_le_mul_of_nonneg_left hdist hslope
      _ = slope * dist x y + slope * dist y z := by ring
  linarith

/-- A finite chain's endpoint distance is controlled by its total value drop.
This is the telescoping estimate used by the Cauchy argument. -/
theorem chain_endpoint_penalty_le_drop {X : Type u} [PseudoMetricSpace X]
    {f : X -> Real} {slope : Real} {c : Nat -> X}
    (hchain : DescentChain f slope c) (hslope : 0 <= slope) :
    forall m n : Nat, m <= n ->
      slope * dist (c m) (c n) <= f (c m) - f (c n) := by
  intro m n hmn
  induction n, hmn using Nat.le_induction with
  | base => simp
  | succ n hmn ih =>
      have hstep := hchain n
      have htriangle : dist (c m) (c (n + 1)) <=
          dist (c m) (c n) + dist (c n) (c (n + 1)) :=
        dist_triangle _ _ _
      have hmul : slope * dist (c m) (c (n + 1)) <=
          slope * dist (c m) (c n) +
            slope * dist (c n) (c (n + 1)) := by
        calc
          slope * dist (c m) (c (n + 1)) <=
              slope * (dist (c m) (c n) + dist (c n) (c (n + 1))) :=
            mul_le_mul_of_nonneg_left htriangle hslope
          _ = _ := by ring
      have hdrop := DescentStep.penalty_le_drop hstep
      linarith

/-- The approximate-minimizer premise turns a descent step from `x0` into the
required radius bound. -/
theorem localization_of_descent {X : Type u} [MetricSpace X]
    {f : X -> Real} {epsilon lambda : Real} {x0 v : X}
    (hepsilon : 0 < epsilon) (hlambda : 0 < lambda)
    (happrox : ApproximateMinimizer f epsilon x0)
    (hdescent : DescentStep f (epsilon / lambda) x0 v) :
    dist v x0 <= lambda := by
  have hslope : 0 < epsilon / lambda := slope_pos hepsilon hlambda
  have hpenalty := DescentStep.penalty_le_drop hdescent
  have happ := happrox v
  have hdist : dist x0 v <= lambda := by
    have hratio : (epsilon / lambda) * lambda = epsilon := by
      field_simp
    have hmul : (epsilon / lambda) * dist x0 v <=
        (epsilon / lambda) * lambda := by
      rw [hratio]
      linarith
    exact le_of_mul_le_mul_left hmul hslope
  simpa [dist_comm] using hdist

/-- A maximal point for the descent relation has the strict penalized
minimality demanded by the frozen conclusion. -/
theorem strict_of_maximal {X : Type u} [PseudoMetricSpace X]
    {f : X -> Real} {epsilon lambda : Real} {x0 v : X}
    (hmax : DescentMaximalPoint f epsilon lambda x0 v) :
    forall y : X, y ≠ v ->
      f v < f y + (epsilon / lambda) * dist v y := by
  intro y hy
  rcases hmax with ⟨_, _, hmax⟩
  by_contra hnot
  exact hy (hmax y (not_lt.mp hnot))

/-- Package a maximal descent point as the exact existential witness used by
the rev-5.6 target. -/
theorem witness_of_maximal {X : Type u} [MetricSpace X]
    {f : X -> Real} {epsilon lambda : Real} {x0 v : X}
    (hmax : DescentMaximalPoint f epsilon lambda x0 v) :
    exists w : X,
      f w <= f x0 /\ dist w x0 <= lambda /\
        forall y : X, y ≠ w ->
          f w < f y + (epsilon / lambda) * dist w y := by
  exact ⟨v, hmax.1, hmax.2.1, strict_of_maximal hmax⟩

/-- Exact root composition from the remaining hard frontier: construction of
a maximal descent point from the canonical hypotheses. -/
theorem target_of_maximalPoint
    (hardCore : forall (X : Type u) [MetricSpace X] [CompleteSpace X]
      (f : X -> Real) (epsilon lambda : Real) (x0 : X),
      LowerSemicontinuous f -> BddBelow (range f) ->
        0 < epsilon -> 0 < lambda -> ApproximateMinimizer f epsilon x0 ->
          exists v : X, DescentMaximalPoint f epsilon lambda x0 v) :
    ProofTarget.{u} := by
  intro X _ _ f epsilon lambda x0 hlsc hbdd hepsilon hlambda happrox
  obtain ⟨v, hv⟩ :=
    hardCore X f epsilon lambda x0 hlsc hbdd hepsilon hlambda happrox
  exact witness_of_maximal hv

end Stage1Instances.THM_M_1270.Proof

#print axioms Stage1Instances.THM_M_1270.Proof.slope_pos
#print axioms Stage1Instances.THM_M_1270.Proof.DescentStep.trans
#print axioms Stage1Instances.THM_M_1270.Proof.chain_endpoint_penalty_le_drop
#print axioms Stage1Instances.THM_M_1270.Proof.localization_of_descent
#print axioms Stage1Instances.THM_M_1270.Proof.strict_of_maximal
#print axioms Stage1Instances.THM_M_1270.Proof.witness_of_maximal
#print axioms Stage1Instances.THM_M_1270.Proof.target_of_maximalPoint
