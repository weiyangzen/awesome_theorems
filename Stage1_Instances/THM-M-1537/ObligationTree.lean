import Statement

/-!
# THM-M-1537 obligation boundary

This module checks two facts used by the frozen architecture.  First, an
explicit area-law bridge composes to the public target without changing its
binders.  Second, the current structure has a stationary semiclassical
Einstein-regime countermodel, so the bridge cannot be derived from the frozen
premises alone.  Neither fact is a proof of the canonical root.
-/

namespace Stage1Instances.THM_M_1537

/-- The substantive physics result still required by the proof tree. -/
def AreaLawBridge : Prop :=
  forall B : SemiclassicalBlackHole,
    B.stationary ->
    B.einsteinGravityRegime ->
    B.semiclassicalRegime ->
    0 <= B.horizonArea ->
    0 < B.boltzmannConstant ->
    0 < B.speedOfLight ->
    0 < B.newtonConstant ->
    0 < B.reducedPlanckConstant ->
    B.thermodynamicEntropy = entropyFromArea B

/-- Exact checked composition from the open physics bridge to the public root. -/
theorem areaLaw_of_bridge (bridge : AreaLawBridge) : BekensteinHawkingAreaLaw := by
  exact bridge

/-- The frozen data and regime markers do not constrain entropy by area. -/
def independentEntropyCountermodel : SemiclassicalBlackHole where
  horizonArea := 0
  thermodynamicEntropy := 1
  boltzmannConstant := 1
  speedOfLight := 1
  newtonConstant := 1
  reducedPlanckConstant := 1
  stationary := True
  einsteinGravityRegime := True
  semiclassicalRegime := True

/-- A kernel-checked witness that the canonical root is false for the current model. -/
theorem not_bekensteinHawkingAreaLaw : Not BekensteinHawkingAreaLaw := by
  intro law
  have h := law independentEntropyCountermodel trivial trivial trivial
    (by norm_num [independentEntropyCountermodel])
    (by norm_num [independentEntropyCountermodel])
    (by norm_num [independentEntropyCountermodel])
    (by norm_num [independentEntropyCountermodel])
    (by norm_num [independentEntropyCountermodel])
  norm_num [independentEntropyCountermodel, entropyFromArea] at h

#print axioms areaLaw_of_bridge
#print axioms not_bekensteinHawkingAreaLaw

end Stage1Instances.THM_M_1537
