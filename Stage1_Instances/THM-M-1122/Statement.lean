import Mathlib.Probability.IdentDistrib

/-!
# THM-M-1122: Schramm-Loewner evolution statement

This module freezes Theorem 1.3 of Schramm's 2000 paper at its exact
probabilistic interface. The analytic Loewner and LERW objects remain explicit
parameters because pinned mathlib does not provide their domain-specific APIs.
It contains the target proposition, not a proof of it.
-/

namespace Stage1Instances.THM_M_1122

open MeasureTheory ProbabilityTheory

universe u v w

/-- Time domain used by Schramm's radial, capacity-parametrized equation. -/
abbrev NegativeTime := {t : ℝ // t ≤ 0}

/-- Exact proposition corresponding to Schramm (2000), Theorem 1.3.

`loewnerSolution driver trace` exposes equations (1.1)--(1.3), including the
normalization and the operation of adjoining the terminal point `0`. The
conclusion is equality in distribution with the LERW scaling-limit random
curve. The implication is conditional on Conjecture 1.2, as in the source.
-/
def SchrammLoewnerEvolutionTarget
    {OmegaLERW : Type u} {OmegaBrownian : Type v} {Curve Driver : Type w}
    [MeasurableSpace OmegaLERW] [MeasurableSpace OmegaBrownian]
    [MeasurableSpace Curve]
    (muLERW : Measure OmegaLERW) (muBrownian : Measure OmegaBrownian)
    (conjecture1_2 : Prop)
    (lerwScalingLimit : OmegaLERW → Curve)
    (isUniformCircleBrownian : (OmegaBrownian → ℝ → Driver) → Prop)
    (loewnerSolution : (NegativeTime → Driver) → Curve → Prop) : Prop :=
  conjecture1_2 →
    ∀ B : OmegaBrownian → ℝ → Driver,
      isUniformCircleBrownian B →
      ∀ sigma : OmegaBrownian → Curve,
        (∀ omega, loewnerSolution (fun t ↦ B omega (-2 * (t : ℝ))) (sigma omega)) →
        IdentDistrib sigma lerwScalingLimit muBrownian muLERW

/-- Expanded spelling used to check binder order and the time scaling `-2t`. -/
def ExpandedTarget
    {OmegaLERW : Type u} {OmegaBrownian : Type v} {Curve Driver : Type w}
    [MeasurableSpace OmegaLERW] [MeasurableSpace OmegaBrownian]
    [MeasurableSpace Curve]
    (muLERW : Measure OmegaLERW) (muBrownian : Measure OmegaBrownian)
    (conjecture1_2 : Prop)
    (lerwScalingLimit : OmegaLERW → Curve)
    (isUniformCircleBrownian : (OmegaBrownian → ℝ → Driver) → Prop)
    (loewnerSolution : (NegativeTime → Driver) → Curve → Prop) : Prop :=
  conjecture1_2 →
    ∀ B : OmegaBrownian → ℝ → Driver,
      isUniformCircleBrownian B →
      ∀ sigma : OmegaBrownian → Curve,
        (∀ omega, loewnerSolution (fun t ↦ B omega (-2 * (t : ℝ))) (sigma omega)) →
        IdentDistrib sigma lerwScalingLimit muBrownian muLERW

/-- Checked definitional transport to the expanded encoding. -/
theorem target_iff_expanded
    {OmegaLERW : Type u} {OmegaBrownian : Type v} {Curve Driver : Type w}
    [MeasurableSpace OmegaLERW] [MeasurableSpace OmegaBrownian]
    [MeasurableSpace Curve]
    (muLERW : Measure OmegaLERW) (muBrownian : Measure OmegaBrownian)
    (conjecture1_2 : Prop)
    (lerwScalingLimit : OmegaLERW → Curve)
    (isUniformCircleBrownian : (OmegaBrownian → ℝ → Driver) → Prop)
    (loewnerSolution : (NegativeTime → Driver) → Curve → Prop) :
    SchrammLoewnerEvolutionTarget muLERW muBrownian conjecture1_2
        lerwScalingLimit isUniformCircleBrownian loewnerSolution ↔
      ExpandedTarget muLERW muBrownian conjecture1_2
        lerwScalingLimit isUniformCircleBrownian loewnerSolution :=
  Iff.rfl

-- Proposition-changing mutations retained for the statement validator.
def mutationDropsConjecture
    {OmegaLERW : Type u} {OmegaBrownian : Type v} {Curve Driver : Type w}
    [MeasurableSpace OmegaLERW] [MeasurableSpace OmegaBrownian]
    [MeasurableSpace Curve]
    (muLERW : Measure OmegaLERW) (muBrownian : Measure OmegaBrownian)
    (lerwScalingLimit : OmegaLERW → Curve)
    (isUniformCircleBrownian : (OmegaBrownian → ℝ → Driver) → Prop)
    (loewnerSolution : (NegativeTime → Driver) → Curve → Prop) : Prop :=
  ∀ B : OmegaBrownian → ℝ → Driver, isUniformCircleBrownian B →
  ∀ sigma : OmegaBrownian → Curve,
    (∀ omega, loewnerSolution
      (fun t ↦ B omega (-2 * (t : ℝ))) (sigma omega)) →
    IdentDistrib sigma lerwScalingLimit muBrownian muLERW

def mutationChangesTimeScale
    {OmegaLERW : Type u} {OmegaBrownian : Type v} {Curve Driver : Type w}
    [MeasurableSpace OmegaLERW] [MeasurableSpace OmegaBrownian]
    [MeasurableSpace Curve]
    (muLERW : Measure OmegaLERW) (muBrownian : Measure OmegaBrownian)
    (conjecture1_2 : Prop) (lerwScalingLimit : OmegaLERW → Curve)
    (isUniformCircleBrownian : (OmegaBrownian → ℝ → Driver) → Prop)
    (loewnerSolution : (NegativeTime → Driver) → Curve → Prop) : Prop :=
  conjecture1_2 →
  ∀ B : OmegaBrownian → ℝ → Driver, isUniformCircleBrownian B →
  ∀ sigma : OmegaBrownian → Curve,
    (∀ omega, loewnerSolution
      (fun t ↦ B omega (-(t : ℝ))) (sigma omega)) →
    IdentDistrib sigma lerwScalingLimit muBrownian muLERW

end Stage1Instances.THM_M_1122

set_option pp.explicit true in
#print Stage1Instances.THM_M_1122.SchrammLoewnerEvolutionTarget
