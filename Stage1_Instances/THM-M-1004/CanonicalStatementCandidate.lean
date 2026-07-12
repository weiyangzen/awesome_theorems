import Mathlib.Probability.Martingale.OptionalStopping

/-!
# THM-M-1004 statement candidate

This file elaborates the bounded discrete-time formulation selected at intake. It is a candidate,
not the accepted canonical target: the repository source record does not specify the hypotheses
needed to distinguish this formulation from the other optional-stopping variants.
-/

noncomputable section

open MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_1004

universe uOmega

/--
Candidate bounded discrete-time optional-stopping equality. The later stopping time has a
deterministic finite bound; pointwise ordering then bounds the earlier stopping time as well.
-/
def CanonicalTargetCandidate : Prop :=
  forall (Omega : Type uOmega) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (filtration : Filtration Nat (inferInstance : MeasurableSpace Omega))
    [SigmaFiniteFiltration mu filtration]
    (process : Nat -> Omega -> Real) (tau pi : Omega -> WithTop Nat),
      Martingale process filtration mu ->
        IsStoppingTime filtration tau ->
          IsStoppingTime filtration pi ->
            tau <= pi ->
              (Exists fun N : Nat => forall omega, pi omega <= N) ->
                mu[stoppedValue process tau] = mu[stoppedValue process pi]

#check CanonicalTargetCandidate

end Stage1Instances.THM_M_1004
