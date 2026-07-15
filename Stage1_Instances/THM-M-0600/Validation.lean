import Statement
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0600 same-worker differential validation

This module imports only the frozen statement and independently reconstructs
the zero-dimensional branch checked during the proof phase. It also checks the
final adapter while retaining the positive-dimensional Morse normal-form
engine as an explicit premise. Neither declaration proves the general Morse
lemma.

These probes are implementation-diverse evidence from this worker, not the
distinct signed independent runner required for release.
-/

noncomputable section

open Set Function
open scoped Topology Manifold ContDiff

namespace Stage1Instances.THM_M_0600.Validation

universe u

/-- Direct reconstruction of the frozen dimension-zero branch without
importing the proof implementation or obligation-tree module. -/
theorem zeroDimensionBranchDirect
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

/-- Independently checked final adapter. The positive-dimensional engine is
deliberately visible as a premise and receives no root-closure credit. -/
theorem conditionalRootDirect
    (positive : forall (n : Nat), 0 < n -> forall (M : Type u)
      [TopologicalSpace M]
      (I : ModelWithCorners Real (Euclidean n) (Euclidean n))
      [ChartedSpace (Euclidean n) M] [IsManifold I ⊤ M]
      (f : M -> Real) (p : M) (base : SmoothLocalCoordinates M I p),
        ContDiffOn Real ⊤ (inCoordinates base f) base.target ->
        fderiv Real (inCoordinates base f) 0 = 0 ->
        Function.Injective (coordinateHessian base f) ->
        exists (index : Nat) (normal : SmoothLocalCoordinates M I p),
          index <= n /\ forall x, x ∈ normal.target ->
            f (normal.invFun x) = f p + morseQuadratic index x) :
    MorseLemmaTarget.{u} := by
  intro n M _topology I _charted _manifold f p base hsmooth hcritical hnondegenerate
  by_cases hn : n = 0
  · subst n
    exact zeroDimensionBranchDirect M I f p base hsmooth hcritical hnondegenerate
  · exact positive n (Nat.pos_of_ne_zero hn) M I f p base hsmooth hcritical hnondegenerate

assert_no_sorry zeroDimensionBranchDirect
assert_no_sorry conditionalRootDirect

#print sorries zeroDimensionBranchDirect
#print sorries conditionalRootDirect

#print axioms zeroDimensionBranchDirect
#print axioms conditionalRootDirect

end Stage1Instances.THM_M_0600.Validation
