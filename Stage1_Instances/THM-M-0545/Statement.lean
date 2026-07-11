import Mathlib.Geometry.Manifold.Riemannian.Basic

/-!
# THM-M-0545: Hodge decomposition statement boundary

The pinned mathlib snapshot has Riemannian manifolds, but not bundled smooth
manifold differential forms, the codifferential, or the Hodge Laplacian.  This
module therefore exposes those missing objects as typed realization data.  It
states, but does not prove, the analytic Hodge decomposition.
-/

noncomputable section

open Bundle
open scoped Bundle ContDiff Manifold Topology

namespace Stage1Instances.THMM0545

universe uE uH uM uF

/-- Typed realization of complex smooth forms and the Hodge operators on a
fixed Riemannian manifold.  The two realization predicates identify this data
with the geometric notions; neither contains a decomposition assertion. -/
structure HodgeAnalyticData
    (E : Type uE) [NormedAddCommGroup E] [NormedSpace Real E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners Real E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M] where
  Form : Nat -> Type uF
  [formAddCommGroup : forall k, NormedAddCommGroup (Form k)]
  [formModule : forall k, NormedSpace Complex (Form k)]
  [formInnerProduct : forall k, InnerProductSpace Complex (Form k)]
  exteriorDerivative : forall k, Form k →L[Complex] Form (k + 1)
  codifferential : forall k, Form (k + 1) →L[Complex] Form k
  laplacian : forall k, Form k →L[Complex] Form k
  isOriented : Prop
  isBoundaryless : Prop
  realizesSmoothComplexForms : Prop
  realizesHodgeOperators : Prop

attribute [instance] HodgeAnalyticData.formAddCommGroup
  HodgeAnalyticData.formModule HodgeAnalyticData.formInnerProduct

namespace HodgeAnalyticData

variable
  {E : Type uE} [NormedAddCommGroup E] [NormedSpace Real E]
  {H : Type uH} [TopologicalSpace H] {I : ModelWithCorners Real E H}
  {M : Type uM} [TopologicalSpace M] [ChartedSpace H M]

/-- A form is harmonic exactly when its Hodge Laplacian vanishes. -/
def IsHarmonic (D : HodgeAnalyticData E H I M) (k : Nat) (h : D.Form k) : Prop :=
  D.laplacian k h = 0

/-- Degree-`k` exact forms, with the predecessor degree explicit.  This makes
degree zero a genuine boundary case rather than silently inventing degree `-1`. -/
def IsExact (D : HodgeAnalyticData E H I M) (k : Nat) (e : D.Form k) : Prop :=
  exists j : Nat, exists alpha : D.Form j, exists _hj : j + 1 = k,
    HEq (D.exteriorDerivative j alpha) e

/-- Degree-`k` coexact forms are images of the codifferential from degree
`k+1`. -/
def IsCoexact (D : HodgeAnalyticData E H I M) (k : Nat) (c : D.Form k) : Prop :=
  exists beta : D.Form (k + 1), D.codifferential k beta = c

/-- The three summands are pairwise orthogonal. -/
def PairwiseOrthogonal (D : HodgeAnalyticData E H I M) (k : Nat)
    (h e c : D.Form k) : Prop :=
  inner Complex h e = 0 /\ inner Complex h c = 0 /\ inner Complex e c = 0

/-- Existence and uniqueness of the harmonic, exact, and coexact summands of
one form. -/
def HasUniqueDecomposition (D : HodgeAnalyticData E H I M) (k : Nat)
    (omega : D.Form k) : Prop :=
  exists h e c : D.Form k,
    D.IsHarmonic k h /\ D.IsExact k e /\ D.IsCoexact k c /\
      D.PairwiseOrthogonal k h e c /\ omega = h + e + c /\
      forall h' e' c' : D.Form k,
        D.IsHarmonic k h' -> D.IsExact k e' -> D.IsCoexact k c' ->
        D.PairwiseOrthogonal k h' e' c' -> omega = h' + e' + c' ->
        h' = h /\ e' = e /\ c' = c

end HodgeAnalyticData

/-- The exact rev-5.6 target: analytic Hodge decomposition for smooth
complex-valued forms on every finite-dimensional, compact, oriented,
boundaryless smooth Riemannian manifold. -/
def HodgeDecompositionTarget : Prop :=
  forall (E : Type uE) [NormedAddCommGroup E] [NormedSpace Real E]
    [FiniteDimensional Real E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners Real E H)
    (M : Type uM) [TopologicalSpace M] [EMetricSpace M] [ChartedSpace H M]
    [CompactSpace M] [T2Space M] [IsManifold I ∞ M]
    [RiemannianBundle (fun x : M => TangentSpace I x)]
    [IsContMDiffRiemannianBundle I ∞ E (fun x : M => TangentSpace I x)]
    [IsRiemannianManifold I M]
    (D : HodgeAnalyticData.{uE, uH, uM, uF} E H I M),
      D.isOriented -> D.isBoundaryless -> D.realizesSmoothComplexForms ->
        D.realizesHodgeOperators ->
          forall k : Nat, forall omega : D.Form k, D.HasUniqueDecomposition k omega

/-- Checked direct expansion of the canonical target. -/
theorem hodgeDecompositionTarget_iff_expanded :
    HodgeDecompositionTarget.{uE, uH, uM, uF} <->
      forall (E : Type uE) [NormedAddCommGroup E] [NormedSpace Real E]
        [FiniteDimensional Real E]
        (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners Real E H)
        (M : Type uM) [TopologicalSpace M] [EMetricSpace M] [ChartedSpace H M]
        [CompactSpace M] [T2Space M] [IsManifold I ∞ M]
        [RiemannianBundle (fun x : M => TangentSpace I x)]
        [IsContMDiffRiemannianBundle I ∞ E (fun x : M => TangentSpace I x)]
        [IsRiemannianManifold I M]
        (D : HodgeAnalyticData.{uE, uH, uM, uF} E H I M),
          D.isOriented -> D.isBoundaryless -> D.realizesSmoothComplexForms ->
            D.realizesHodgeOperators ->
              forall k : Nat, forall omega : D.Form k,
                D.HasUniqueDecomposition k omega :=
  Iff.rfl

-- Separately elaborated structural mutations; none receives equivalence credit.
def MutationRemovedCompactness : Prop :=
  forall (E : Type uE) [NormedAddCommGroup E] [NormedSpace Real E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners Real E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    (D : HodgeAnalyticData.{uE, uH, uM, uF} E H I M),
      forall k : Nat, forall _omega : D.Form k, True

def MutationChangedCoefficientDomain : Prop :=
  forall _k : Nat, forall V : Type uF, [AddCommGroup V] → Nonempty V

def MutationChangedBinderScope : Prop :=
  forall (E : Type uE) [NormedAddCommGroup E] [NormedSpace Real E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners Real E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    (D : HodgeAnalyticData.{uE, uH, uM, uF} E H I M),
      exists k : Nat, forall omega : D.Form k, D.HasUniqueDecomposition k omega

def MutationDegreeZeroOnly : Prop :=
  forall (E : Type uE) [NormedAddCommGroup E] [NormedSpace Real E]
    (H : Type uH) [TopologicalSpace H] (I : ModelWithCorners Real E H)
    (M : Type uM) [TopologicalSpace M] [ChartedSpace H M]
    (D : HodgeAnalyticData.{uE, uH, uM, uF} E H I M),
      forall omega : D.Form 0, D.HasUniqueDecomposition 0 omega

end Stage1Instances.THMM0545

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THMM0545.HodgeDecompositionTarget
