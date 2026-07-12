import Statement

/-!
# THM-M-1177 conditional obligation composition

This module checks only the final case-split interface of the frozen ABP
architecture.  The degenerate and positive-maximum packages remain explicit
premises; no ABP estimate is proved here.
-/

noncomputable section

open MeasureTheory

namespace Stage1Instances.THM_M_1177

/-- The hypotheses of the canonical target, factored without changing their
order or strength. -/
def ABPHypotheses {n : Nat} (Omega : Set (Euclidean n))
    (u f : Euclidean n -> Real)
    (A : Euclidean n -> Matrix (Fin n) (Fin n) Real) : Prop :=
  IsOpen Omega ∧ IsPreconnected Omega ∧ Bornology.IsBounded Omega ∧
  ContinuousOn u (closure Omega) ∧ ContDiffOn Real 2 u Omega ∧
  Measurable f ∧ (∀ i j, Measurable fun x => A x i j) ∧
  (∀ x ∈ Omega, IsSymmetricPositiveDefinite (A x)) ∧
  (∀ x ∈ Omega, Matrix.trace (A x * hessian u x) ≥ f x) ∧
  (∀ x ∈ frontier Omega, u x ≤ 0) ∧
  IntegrableOn (fun x => (max (-f x) 0) ^ n / Matrix.det (A x))
    (upperContactSet Omega u)

/-- The exact conclusion with a fixed dimensional constant. -/
def ABPBound {n : Nat} (Cn : Real) (Omega : Set (Euclidean n))
    (u f : Euclidean n -> Real)
    (A : Euclidean n -> Matrix (Fin n) (Fin n) Real) : Prop :=
  sSup (u '' Omega) ≤
    Cn * Metric.diam Omega * weightedNegativeNorm Omega u f A

/-- The branch in which the positive maximum is already nonpositive. -/
def DegenerateMaximumPackage (n : Nat) (Cn : Real) : Prop :=
  ∀ (Omega : Set (Euclidean n))
    (u f : Euclidean n -> Real)
    (A : Euclidean n -> Matrix (Fin n) (Fin n) Real),
    ABPHypotheses Omega u f A -> sSup (u '' Omega) ≤ 0 ->
    ABPBound Cn Omega u f A

/-- The substantive contact-set/area-formula branch. -/
def PositiveMaximumPackage (n : Nat) (Cn : Real) : Prop :=
  ∀ (Omega : Set (Euclidean n))
    (u f : Euclidean n -> Real)
    (A : Euclidean n -> Matrix (Fin n) (Fin n) Real),
    ABPHypotheses Omega u f A -> 0 < sSup (u '' Omega) ->
    ABPBound Cn Omega u f A

/-- A uniform interface supplying one constant to both exhaustive branches. -/
def ABPArchitecturePackage : Prop :=
  ∀ n : Nat, 1 ≤ n -> ∃ Cn : Real, 0 ≤ Cn ∧
    DegenerateMaximumPackage n Cn ∧ PositiveMaximumPackage n Cn

/-- Checked conditional composition into the exact canonical root. -/
theorem root_of_architecture (architecture : ABPArchitecturePackage) :
    AlexandrovBakelmanPucciTarget := by
  intro n hn
  obtain ⟨Cn, hCn, hdegenerate, hpositive⟩ := architecture n hn
  refine ⟨Cn, hCn, ?_⟩
  intro Omega u f A hopen hconnected hbounded hcontinuous hsmooth hf hAmeas
    hApos hop hboundary hintegrable
  have hypotheses : ABPHypotheses Omega u f A :=
    ⟨hopen, hconnected, hbounded, hcontinuous, hsmooth, hf, hAmeas,
      hApos, hop, hboundary, hintegrable⟩
  by_cases hmax : sSup (u '' Omega) ≤ 0
  · exact hdegenerate Omega u f A hypotheses hmax
  · exact hpositive Omega u f A hypotheses (lt_of_not_ge hmax)

#print axioms root_of_architecture

end Stage1Instances.THM_M_1177
