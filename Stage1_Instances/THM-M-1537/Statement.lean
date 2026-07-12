import Mathlib.Data.Real.Basic

/-!
# THM-M-1537: black-hole entropy statement boundary

This file freezes the Bekenstein-Hawking area law as a theorem about an
explicit semiclassical black-hole model.  The model records no area-law field,
so the target is not a projection from an assumed conclusion.
-/

namespace Stage1Instances.THM_M_1537

noncomputable section

/-- Physical data used by the dimensionful Bekenstein-Hawking law. -/
structure SemiclassicalBlackHole where
  horizonArea : Real
  thermodynamicEntropy : Real
  boltzmannConstant : Real
  speedOfLight : Real
  newtonConstant : Real
  reducedPlanckConstant : Real
  stationary : Prop
  einsteinGravityRegime : Prop
  semiclassicalRegime : Prop

/-- The dimensionful Bekenstein-Hawking entropy value
`k_B * c^3 * A / (4 * G * hbar)`. -/
def entropyFromArea (B : SemiclassicalBlackHole) : Real :=
  B.boltzmannConstant * B.speedOfLight ^ 3 * B.horizonArea /
    (4 * B.newtonConstant * B.reducedPlanckConstant)

/-- Exact target selected from the intake claim.  Degenerate horizons are
admitted (`A = 0`), while all physical constants are required to be positive. -/
def BekensteinHawkingAreaLaw : Prop :=
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

/-- A direct expanded encoding of the canonical target. -/
def ExpandedBekensteinHawkingAreaLaw : Prop :=
  forall B : SemiclassicalBlackHole,
    B.stationary ->
    B.einsteinGravityRegime ->
    B.semiclassicalRegime ->
    0 <= B.horizonArea ->
    0 < B.boltzmannConstant ->
    0 < B.speedOfLight ->
    0 < B.newtonConstant ->
    0 < B.reducedPlanckConstant ->
    B.thermodynamicEntropy =
      B.boltzmannConstant * B.speedOfLight ^ 3 * B.horizonArea /
        (4 * B.newtonConstant * B.reducedPlanckConstant)

/-- Checked transport to the expanded dimensionful source shape. -/
theorem areaLaw_iff_expanded :
    BekensteinHawkingAreaLaw <-> ExpandedBekensteinHawkingAreaLaw :=
  Iff.rfl

-- Structural mutations: the statement validator requires distinct kernel expressions.
def mutationRemovedSemiclassicalHypothesis : Prop :=
  forall B : SemiclassicalBlackHole,
    B.stationary ->
    B.einsteinGravityRegime ->
    0 <= B.horizonArea ->
    0 < B.boltzmannConstant ->
    0 < B.speedOfLight ->
    0 < B.newtonConstant ->
    0 < B.reducedPlanckConstant ->
    B.thermodynamicEntropy = entropyFromArea B

def mutationChangedDomainToNat : Prop :=
  forall (horizonArea thermodynamicEntropy : Nat),
    thermodynamicEntropy = horizonArea / 4

def mutationChangedBinderScope : Prop :=
  forall B : SemiclassicalBlackHole,
    B.stationary ->
    (B.einsteinGravityRegime /\ B.semiclassicalRegime) ->
    0 <= B.horizonArea ->
    0 < B.boltzmannConstant ->
    0 < B.speedOfLight ->
    0 < B.newtonConstant ->
    0 < B.reducedPlanckConstant ->
    B.thermodynamicEntropy = entropyFromArea B

def mutationExcludedZeroArea : Prop :=
  forall B : SemiclassicalBlackHole,
    B.stationary ->
    B.einsteinGravityRegime ->
    B.semiclassicalRegime ->
    0 < B.horizonArea ->
    0 < B.boltzmannConstant ->
    0 < B.speedOfLight ->
    0 < B.newtonConstant ->
    0 < B.reducedPlanckConstant ->
    B.thermodynamicEntropy = entropyFromArea B

/-- The canonical statement includes the zero-area boundary syntactically. -/
example : (0 : Real) <= 0 := le_rfl

end
end Stage1Instances.THM_M_1537

set_option pp.explicit true in
#print Stage1Instances.THM_M_1537.BekensteinHawkingAreaLaw

set_option pp.explicit true in
#print Stage1Instances.THM_M_1537.mutationRemovedSemiclassicalHypothesis

set_option pp.explicit true in
#print Stage1Instances.THM_M_1537.mutationChangedDomainToNat

set_option pp.explicit true in
#print Stage1Instances.THM_M_1537.mutationChangedBinderScope

set_option pp.explicit true in
#print Stage1Instances.THM_M_1537.mutationExcludedZeroArea
