import Mathlib.Topology.Semicontinuity.Basic

/-!
# THM-M-1270: Ekeland variational principle statement boundary

This module freezes the real-valued, two-parameter complete-metric-space form
selected from the intake. It elaborates the proposition but does not prove it.
-/

open Set

namespace Stage1Instances.THM_M_1270

universe u

/-- A point whose value is within `epsilon` of every value of `f`. -/
def ApproximateMinimizer {X : Type u} (f : X -> Real) (epsilon : Real) (x0 : X) : Prop :=
  forall x : X, f x0 <= f x + epsilon

/-- The infimum presentation of the same approximate-minimizer premise. -/
def InfimumApproximateMinimizer {X : Type u}
    (f : X -> Real) (epsilon : Real) (x0 : X) : Prop :=
  f x0 <= sInf (range f) + epsilon

/-- The exact real-valued two-parameter Ekeland target selected at statement phase. -/
def EkelandVariationalPrincipleTarget : Prop :=
  forall (X : Type u) [MetricSpace X] [CompleteSpace X]
    (f : X -> Real) (epsilon lambda : Real) (x0 : X),
    LowerSemicontinuous f ->
      BddBelow (range f) ->
        0 < epsilon ->
          0 < lambda ->
            ApproximateMinimizer f epsilon x0 ->
              exists v : X,
                f v <= f x0 /\
                  dist v x0 <= lambda /\
                    forall y : X, y ≠ v ->
                      f v < f y + (epsilon / lambda) * dist v y

/-- Alternate root using the reader-standard infimum premise. -/
def InfimumEkelandVariationalPrincipleTarget : Prop :=
  forall (X : Type u) [MetricSpace X] [CompleteSpace X]
    (f : X -> Real) (epsilon lambda : Real) (x0 : X),
    LowerSemicontinuous f ->
      BddBelow (range f) ->
        0 < epsilon ->
          0 < lambda ->
            InfimumApproximateMinimizer f epsilon x0 ->
              exists v : X,
                f v <= f x0 /\
                  dist v x0 <= lambda /\
                    forall y : X, y ≠ v ->
                      f v < f y + (epsilon / lambda) * dist v y

/-- Under boundedness below, the pointwise and infimum premises agree. -/
theorem approximateMinimizer_iff_infimum
    {X : Type u} {f : X -> Real} {epsilon : Real} {x0 : X}
    (hbdd : BddBelow (range f)) :
    ApproximateMinimizer f epsilon x0 <->
      InfimumApproximateMinimizer f epsilon x0 := by
  constructor
  · intro h
    have hlower : f x0 - epsilon <= sInf (range f) := by
      refine le_csInf ?_ ?_
      · exact ⟨f x0, ⟨x0, rfl⟩⟩
      · intro y hy
        rcases hy with ⟨x, rfl⟩
        linarith [h x]
    dsimp [InfimumApproximateMinimizer]
    linarith
  · intro h x
    dsimp [InfimumApproximateMinimizer] at h
    have hinf : sInf (range f) <= f x := csInf_le hbdd ⟨x, rfl⟩
    linarith

/-- Checked equivalence between the two accepted premise encodings. -/
theorem target_iff_infimum_target :
    EkelandVariationalPrincipleTarget.{u} <->
      InfimumEkelandVariationalPrincipleTarget.{u} := by
  constructor
  · intro h X _ _ f epsilon lambda x0 hlsc hbdd hepsilon hlambda happrox
    exact h X f epsilon lambda x0 hlsc hbdd hepsilon hlambda
      ((approximateMinimizer_iff_infimum hbdd).mpr happrox)
  · intro h X _ _ f epsilon lambda x0 hlsc hbdd hepsilon hlambda happrox
    exact h X f epsilon lambda x0 hlsc hbdd hepsilon hlambda
      ((approximateMinimizer_iff_infimum hbdd).mp happrox)

-- Independently elaborated structural mutations for statement review.
def mutationRemovedCompleteness : Prop :=
  forall (X : Type u) [MetricSpace X] (f : X -> Real) (epsilon lambda : Real) (x0 : X),
    LowerSemicontinuous f -> BddBelow (range f) -> 0 < epsilon -> 0 < lambda ->
      ApproximateMinimizer f epsilon x0 ->
        exists v : X, f v <= f x0 /\ dist v x0 <= lambda /\
          forall y : X, y ≠ v -> f v < f y + (epsilon / lambda) * dist v y

def mutationRemovedLowerSemicontinuity : Prop :=
  forall (X : Type u) [MetricSpace X] [CompleteSpace X]
    (f : X -> Real) (epsilon lambda : Real) (x0 : X),
    BddBelow (range f) -> 0 < epsilon -> 0 < lambda -> ApproximateMinimizer f epsilon x0 ->
      exists v : X, f v <= f x0 /\ dist v x0 <= lambda /\
        forall y : X, y ≠ v -> f v < f y + (epsilon / lambda) * dist v y

def mutationNonStrictConclusion : Prop :=
  forall (X : Type u) [MetricSpace X] [CompleteSpace X]
    (f : X -> Real) (epsilon lambda : Real) (x0 : X),
    LowerSemicontinuous f -> BddBelow (range f) -> 0 < epsilon -> 0 < lambda ->
      ApproximateMinimizer f epsilon x0 ->
        exists v : X, f v <= f x0 /\ dist v x0 <= lambda /\
          forall y : X, y ≠ v -> f v <= f y + (epsilon / lambda) * dist v y

end Stage1Instances.THM_M_1270

set_option pp.explicit true in
#print Stage1Instances.THM_M_1270.EkelandVariationalPrincipleTarget

set_option pp.explicit true in
#print Stage1Instances.THM_M_1270.mutationRemovedCompleteness

set_option pp.explicit true in
#print Stage1Instances.THM_M_1270.mutationRemovedLowerSemicontinuity

set_option pp.explicit true in
#print Stage1Instances.THM_M_1270.mutationNonStrictConclusion
