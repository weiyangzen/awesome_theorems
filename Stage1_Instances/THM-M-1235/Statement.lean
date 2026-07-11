import Mathlib.Data.Real.Basic

/-!
# THM-M-1235: Wolibner's planar ideal-fluid theorem

This module freezes the theorem stated on pages 698--700 and 725--726 of
Wolibner's 1933 paper. The paper's conditions `(I)`--`(VIII)` are retained as
named, typed fields because the pinned library has no analytic-boundary,
area-preserving-flow, or classical Euler-solution API capable of expanding
them without changing the source formulation. None of those fields assumes
existence or uniqueness.
-/

namespace Stage1Instances.THMM1235

abbrev Point := Real × Real

/-- The source allows a bounded closed planar region or an exterior region
containing infinity; its frontier consists of finitely many closed analytic
curves. -/
structure SourceDomain where
  carrier : Set Point
  boundaryComponentCount : Nat
  boundaryIsFiniteUnionOfClosedAnalyticCurves : Prop
  isClosedPlanarRegion : Prop
  containsInfinity : Bool

/-- Data fixed in Wolibner's introduction and equation `(1)`. -/
structure SourceData where
  domain : SourceDomain
  density : Real
  density_pos : 0 < density
  vorticity : Point -> Real
  potential : Point -> Real -> Real
  pressureAtBasePoint : Real -> Real
  vorticityLebesgueIntegrableOnDomain : Prop
  vorticityHasSourceDecay : Prop
  vorticityIsHolderContinuous : Prop
  initialCirculationOnEveryInteriorBoundaryComponentIsZero : Prop

/-- The five functions constructed by the paper, for a prescribed finite
positive terminal time. -/
structure Motion (D : SourceData) (T : Real) where
  lagrangianX : Point -> Real -> Real
  lagrangianY : Point -> Real -> Real
  velocityX : Point -> Real -> Real
  velocityY : Point -> Real -> Real
  pressure : Point -> Real -> Real
  conditionI_areaPreservingSelfHomeomorphism : Prop
  conditionII_integralMomentumBalance : Prop
  conditionIII_classicalEulerEquations : Prop
  conditionIV_initialPositionAndVelocity : Prop
  conditionV_pressureNormalization : Prop
  conditionVI_zeroInteriorBoundaryCirculation : Prop
  conditionVII_sourceDecayBounds : Prop
  conditionVIII_continuousSpatialDerivatives : Prop

/-- Equality in the uniqueness clause is equality of all five source
functions; proof fields in `Motion` are proposition-valued. -/
def SameMotion {D : SourceData} {T : Real} (S₁ S₂ : Motion D T) : Prop :=
  S₁.lagrangianX = S₂.lagrangianX /\
  S₁.lagrangianY = S₂.lagrangianY /\
  S₁.velocityX = S₂.velocityX /\
  S₁.velocityY = S₂.velocityY /\
  S₁.pressure = S₂.pressure

/-- Exact statement target: for every source datum and every finite `T > 0`,
there is a motion satisfying `(I)`--`(VIII)` on `0 <= t <= T`, and it is
unique among motions satisfying those same conditions. Since `T` is arbitrary,
this is the paper's "temps infiniment long" conclusion. -/
def WolibnerGlobalExistenceAndUniqueness : Prop :=
  forall (D : SourceData) (T : Real),
    D.domain.isClosedPlanarRegion ->
    D.domain.boundaryIsFiniteUnionOfClosedAnalyticCurves ->
    D.vorticityLebesgueIntegrableOnDomain ->
    D.vorticityHasSourceDecay ->
    D.vorticityIsHolderContinuous ->
    D.initialCirculationOnEveryInteriorBoundaryComponentIsZero ->
    0 < T ->
    exists S : Motion D T, forall S' : Motion D T, SameMotion S' S

/-- Checked expansion fixes binder order, the strict positive-time boundary,
existence, and uniqueness of all five functions. -/
theorem wolibnerTarget_iff_expanded :
    WolibnerGlobalExistenceAndUniqueness <->
      forall (D : SourceData) (T : Real),
        D.domain.isClosedPlanarRegion ->
        D.domain.boundaryIsFiniteUnionOfClosedAnalyticCurves ->
        D.vorticityLebesgueIntegrableOnDomain ->
        D.vorticityHasSourceDecay ->
        D.vorticityIsHolderContinuous ->
        D.initialCirculationOnEveryInteriorBoundaryComponentIsZero ->
        0 < T ->
        exists S : Motion D T, forall S' : Motion D T,
          S'.lagrangianX = S.lagrangianX /\
          S'.lagrangianY = S.lagrangianY /\
          S'.velocityX = S.velocityX /\
          S'.velocityY = S.velocityY /\
          S'.pressure = S.pressure :=
  Iff.rfl

-- Separately elaborated structural mutations; none receives equivalence credit.
def MutationRemovedHolderHypothesis : Prop :=
  forall (D : SourceData) (T : Real),
    D.domain.isClosedPlanarRegion ->
    D.domain.boundaryIsFiniteUnionOfClosedAnalyticCurves ->
    D.vorticityLebesgueIntegrableOnDomain -> D.vorticityHasSourceDecay ->
    D.initialCirculationOnEveryInteriorBoundaryComponentIsZero -> 0 < T ->
    exists S : Motion D T, forall S' : Motion D T, SameMotion S' S

def MutationChangedDomainToWholePlane : Prop :=
  forall (D : SourceData) (T : Real), D.domain.carrier = Set.univ ->
    D.domain.isClosedPlanarRegion ->
    D.domain.boundaryIsFiniteUnionOfClosedAnalyticCurves ->
    D.vorticityLebesgueIntegrableOnDomain ->
    D.vorticityHasSourceDecay -> D.vorticityIsHolderContinuous ->
    D.initialCirculationOnEveryInteriorBoundaryComponentIsZero -> 0 < T ->
    exists S : Motion D T, forall S' : Motion D T, SameMotion S' S

def MutationChangedBinderScope : Prop :=
  exists T : Real, 0 < T /\
    forall D : SourceData, D.domain.isClosedPlanarRegion ->
      D.domain.boundaryIsFiniteUnionOfClosedAnalyticCurves ->
      D.vorticityLebesgueIntegrableOnDomain ->
      D.vorticityHasSourceDecay -> D.vorticityIsHolderContinuous ->
      D.initialCirculationOnEveryInteriorBoundaryComponentIsZero ->
      exists S : Motion D T, forall S' : Motion D T, SameMotion S' S

def MutationIncludesZeroTimeBoundary : Prop :=
  forall (D : SourceData) (T : Real),
    D.domain.isClosedPlanarRegion ->
    D.domain.boundaryIsFiniteUnionOfClosedAnalyticCurves ->
    D.vorticityLebesgueIntegrableOnDomain ->
    D.vorticityHasSourceDecay -> D.vorticityIsHolderContinuous ->
    D.initialCirculationOnEveryInteriorBoundaryComponentIsZero -> 0 <= T ->
    exists S : Motion D T, forall S' : Motion D T, SameMotion S' S

end Stage1Instances.THMM1235

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness
