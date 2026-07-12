import Mathlib.Probability.IdentDistrib

/-!
# THM-M-1122 anchor-audit elaboration probe

This file checks the only exact pinned-mathlib anchor used by the frozen target.
It deliberately does not define Brownian motion, Loewner evolution, LERW, or a
proof of the target.
-/

open MeasureTheory ProbabilityTheory

#check ProbabilityTheory.IdentDistrib
#check ProbabilityTheory.IdentDistrib.refl
#check ProbabilityTheory.IdentDistrib.trans
#check ProbabilityTheory.HasLaw.identDistrib

example {OmegaLERW OmegaBrownian Curve : Type*}
    [MeasurableSpace OmegaLERW] [MeasurableSpace OmegaBrownian]
    [MeasurableSpace Curve]
    (sigma : OmegaBrownian → Curve) (lerwScalingLimit : OmegaLERW → Curve)
    (muBrownian : Measure OmegaBrownian) (muLERW : Measure OmegaLERW) : Prop :=
  IdentDistrib sigma lerwScalingLimit muBrownian muLERW
