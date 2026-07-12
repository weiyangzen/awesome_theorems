import Statement

/-!
# THM-M-1122 conditional obligation composition

This module checks only the final composition boundary of the frozen proof
architecture.  The substantive Schramm identification remains an explicit
premise; no proof of it is asserted here.
-/

namespace Stage1Instances.THM_M_1122

open MeasureTheory ProbabilityTheory

universe u v w

/-- The substantive conditional identification package, deliberately stated
with exactly the binders and conclusion of the canonical target. -/
def ConditionalIdentification
    {OmegaLERW : Type u} {OmegaBrownian : Type v} {Curve Driver : Type w}
    [MeasurableSpace OmegaLERW] [MeasurableSpace OmegaBrownian]
    [MeasurableSpace Curve]
    (muLERW : Measure OmegaLERW) (muBrownian : Measure OmegaBrownian)
    (conjecture1_2 : Prop)
    (lerwScalingLimit : OmegaLERW -> Curve)
    (isUniformCircleBrownian : (OmegaBrownian -> Real -> Driver) -> Prop)
    (loewnerSolution : (NegativeTime -> Driver) -> Curve -> Prop) : Prop :=
  conjecture1_2 ->
    forall B : OmegaBrownian -> Real -> Driver,
      isUniformCircleBrownian B ->
      forall sigma : OmegaBrownian -> Curve,
        (forall omega,
          loewnerSolution (fun t => B omega (-2 * (t : Real))) (sigma omega)) ->
        IdentDistrib sigma lerwScalingLimit muBrownian muLERW

/-- Checked composition from the substantive package to the exact root. -/
theorem root_of_conditionalIdentification
    {OmegaLERW : Type u} {OmegaBrownian : Type v} {Curve Driver : Type w}
    [MeasurableSpace OmegaLERW] [MeasurableSpace OmegaBrownian]
    [MeasurableSpace Curve]
    (muLERW : Measure OmegaLERW) (muBrownian : Measure OmegaBrownian)
    (conjecture1_2 : Prop)
    (lerwScalingLimit : OmegaLERW -> Curve)
    (isUniformCircleBrownian : (OmegaBrownian -> Real -> Driver) -> Prop)
    (loewnerSolution : (NegativeTime -> Driver) -> Curve -> Prop)
    (identification : ConditionalIdentification muLERW muBrownian conjecture1_2
      lerwScalingLimit isUniformCircleBrownian loewnerSolution) :
    SchrammLoewnerEvolutionTarget muLERW muBrownian conjecture1_2
      lerwScalingLimit isUniformCircleBrownian loewnerSolution :=
  identification

#print axioms root_of_conditionalIdentification

end Stage1Instances.THM_M_1122
