import ObligationTree
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0600 partial proof execution

This module supplies a proof body for the zero-dimensional branch of the
frozen Morse-lemma architecture. The positive-dimensional normal-form
construction remains an explicit premise of the conditional composition
theorem.
-/

noncomputable section

open Set Function
open scoped Topology Manifold ContDiff

namespace Stage1Instances.THM_M_0600

universe u

/-- The positive-dimensional part of the frozen normal-form engine. This is
an interface for the still-open analytic construction, not a proof of it. -/
def PositiveDimensionMorseNormalFormEngine : Prop :=
  forall (n : Nat), 0 < n -> forall (M : Type u) [TopologicalSpace M]
    (I : ModelWithCorners Real (Euclidean n) (Euclidean n))
    [ChartedSpace (Euclidean n) M] [IsManifold I ⊤ M]
    (f : M -> Real) (p : M) (base : SmoothLocalCoordinates M I p),
      ContDiffOn Real ⊤ (inCoordinates base f) base.target ->
      fderiv Real (inCoordinates base f) 0 = 0 ->
      Function.Injective (coordinateHessian base f) ->
      exists (index : Nat) (normal : SmoothLocalCoordinates M I p),
        index <= n /\ forall x, x ∈ normal.target ->
          f (normal.invFun x) = f p + morseQuadratic index x

/-- In dimension zero the supplied coordinates are already Morse normal
coordinates: every vector is zero and both quadratic sums are empty. -/
theorem zeroDimensionBranch
    (M : Type u) [TopologicalSpace M]
    (I : ModelWithCorners Real (Euclidean 0) (Euclidean 0))
    [ChartedSpace (Euclidean 0) M] [IsManifold I ⊤ M]
    (f : M -> Real) (p : M) (base : SmoothLocalCoordinates M I p)
    (_hsmooth : ContDiffOn Real ⊤ (inCoordinates base f) base.target)
    (_hcritical : fderiv Real (inCoordinates base f) 0 = 0)
    (_hnondegenerate : Function.Injective (coordinateHessian base f)) :
    exists (index : Nat) (normal : SmoothLocalCoordinates M I p),
      index <= 0 /\ forall x, x ∈ normal.target ->
        f (normal.invFun x) = f p + morseQuadratic index x := by
  refine ⟨0, base, Nat.le_refl 0, ?_⟩
  intro x _hx
  have hx0 : x = 0 := Subsingleton.elim _ _
  have hinv : base.invFun 0 = p := by
    rw [← base.centered]
    exact base.left_inv base.mem_source
  rw [hx0, hinv]
  simp [morseQuadratic]

/-- Combine the checked zero-dimensional branch with an explicit
positive-dimensional engine premise. -/
theorem morseNormalFormEngine_of_positiveDimension
    (positive : PositiveDimensionMorseNormalFormEngine.{u}) :
    MorseNormalFormEngine.{u} := by
  intro n M _topology I _charted _manifold f p base hsmooth hcritical hnondegenerate
  by_cases hn : n = 0
  · subst n
    exact zeroDimensionBranch M I f p base hsmooth hcritical hnondegenerate
  · exact positive n (Nat.pos_of_ne_zero hn) M I f p base hsmooth hcritical hnondegenerate

/-- Exact-root composition after inserting the zero-dimensional body. The
sole premise is the still-open positive-dimensional construction. -/
theorem morseLemmaTarget_of_positiveDimension
    (positive : PositiveDimensionMorseNormalFormEngine.{u}) :
    MorseLemmaTarget.{u} :=
  root_of_morseNormalFormEngine
    (morseNormalFormEngine_of_positiveDimension positive)

assert_no_sorry zeroDimensionBranch
assert_no_sorry morseNormalFormEngine_of_positiveDimension
assert_no_sorry morseLemmaTarget_of_positiveDimension

#print sorries zeroDimensionBranch
#print sorries morseNormalFormEngine_of_positiveDimension
#print sorries morseLemmaTarget_of_positiveDimension

#print axioms zeroDimensionBranch
#print axioms morseNormalFormEngine_of_positiveDimension
#print axioms morseLemmaTarget_of_positiveDimension

end Stage1Instances.THM_M_0600
