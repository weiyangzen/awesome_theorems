import Mathlib.Geometry.Manifold.IsManifold.InteriorBoundary

/-!
# THM-M-0547: Lefschetz duality statement boundary

The pinned mathlib snapshot represents a manifold and its boundary, but it has no relative
singular-homology, compactly supported cohomology, cap-product, or fundamental-class API.  The
interfaces below type those missing objects without storing the duality isomorphism.  This module
freezes the target only; it contains no proof of Lefschetz duality.
-/

noncomputable section

open scoped Manifold

namespace Stage1Instances.THM_M_0547

universe uE uH uM uA

/-- Concrete pinned manifold-with-boundary data together with the coefficient and orientation
choices needed by the duality theorem.  The boundary is mathlib's actual manifold boundary. -/
structure LefschetzManifoldData
    (n : Nat)
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace Real E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners Real E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M] where
  modelDimension : Module.finrank Real E = n
  hausdorff : T2Space M
  locallyCompact : LocallyCompactSpace M
  manifold : IsManifold I top M
  compact : CompactSpace M
  orientation : Type uA
  selectedOrientation : orientation

/-- Typed realization of the missing algebraic-topology objects.  The carrier families and
cap-product map are data; `realizesClassicalObjects` identifies them with the classical integral
theories but does not assert that the cap-product map is invertible. -/
structure LefschetzHomologyData
    {n : Nat}
    {E : Type uE} [NormedAddCommGroup E] [NormedSpace Real E]
    {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners Real E H}
    {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]
    (X : LefschetzManifoldData n E H I M) where
  compactlySupportedCohomology : Nat -> Type uA
  relativeHomology : Nat -> Type uA
  [compactlySupportedCohomologyAddCommGroup :
    forall q, AddCommGroup (compactlySupportedCohomology q)]
  [relativeHomologyAddCommGroup : forall q, AddCommGroup (relativeHomology q)]
  capWithFundamentalClass : forall q,
    compactlySupportedCohomology q →+
      relativeHomology (n - q)
  realizesClassicalObjects : Prop

attribute [instance]
  LefschetzHomologyData.compactlySupportedCohomologyAddCommGroup
  LefschetzHomologyData.relativeHomologyAddCommGroup

/-- The compact Poincare-Lefschetz duality target over integral coefficients: cap product with the
selected orientation/fundamental class is an isomorphism in every natural cohomological degree. -/
def LefschetzDualityTarget : Prop :=
  forall (n : Nat)
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace Real E]
    [FiniteDimensional Real E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners Real E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    (X : LefschetzManifoldData.{uE, uH, uM, uA} n E H I M)
    (D : LefschetzHomologyData.{uE, uH, uM, uA} X),
      D.realizesClassicalObjects ->
        forall q : Nat, Function.Bijective (D.capWithFundamentalClass q)

/-- Direct expansion of the selected target, used to check the named statement encoding. -/
def ExpandedLefschetzDualityTarget : Prop :=
  forall (n : Nat)
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace Real E]
    [FiniteDimensional Real E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners Real E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    (X : LefschetzManifoldData.{uE, uH, uM, uA} n E H I M)
    (D : LefschetzHomologyData.{uE, uH, uM, uA} X),
      D.realizesClassicalObjects ->
        forall q : Nat, Function.Bijective (D.capWithFundamentalClass q)

/-- Checked identity between the named target and its direct expansion. -/
theorem lefschetzDualityTarget_iff_expanded :
    LefschetzDualityTarget.{uE, uH, uM, uA} <->
      ExpandedLefschetzDualityTarget.{uE, uH, uM, uA} :=
  Iff.rfl

/-! Structural mutations elaborate as propositions but receive no statement-identity credit. -/

def mutationRemovedOrientation : Prop :=
  forall (_n : Nat)
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace Real E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners Real E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M],
      IsManifold I ⊤ M -> True

def mutationChangedToAbsoluteHomology : Prop :=
  forall (n q : Nat) (cohomology homology : Nat -> Type uA),
    Nonempty (cohomology q -> homology (n - q))

def mutationChangedBinderScope : Prop :=
  exists n : Nat,
    forall (E : Type uE) [NormedAddCommGroup E] [NormedSpace Real E],
      Module.finrank Real E = n

def mutationBoundaryDegreeZeroOnly : Prop :=
  forall (n : Nat)
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace Real E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners Real E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    (X : LefschetzManifoldData.{uE, uH, uM, uA} n E H I M)
    (D : LefschetzHomologyData.{uE, uH, uM, uA} X),
      D.realizesClassicalObjects -> Function.Bijective (D.capWithFundamentalClass 0)

variable
  (hCanonical : LefschetzDualityTarget.{uE, uH, uM, uA})
  (hRemoved : mutationRemovedOrientation.{uE, uH, uM})
  (hDomain : mutationChangedToAbsoluteHomology.{uA})
  (hScope : mutationChangedBinderScope.{uE})
  (hBoundary : mutationBoundaryDegreeZeroOnly.{uE, uH, uM, uA})

#check_failure (show mutationRemovedOrientation.{uE, uH, uM} from hCanonical)
#check_failure (show LefschetzDualityTarget.{uE, uH, uM, uA} from hRemoved)
#check_failure (show LefschetzDualityTarget.{uE, uH, uM, uA} from hDomain)
#check_failure (show LefschetzDualityTarget.{uE, uH, uM, uA} from hScope)
#check_failure (show LefschetzDualityTarget.{uE, uH, uM, uA} from hBoundary)

#check lefschetzDualityTarget_iff_expanded
#print axioms lefschetzDualityTarget_iff_expanded

end Stage1Instances.THM_M_0547

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0547.LefschetzDualityTarget
