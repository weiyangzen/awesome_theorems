import Statement

/-!
# THM-M-0600 conditional obligation composition

This module checks the final composition boundary selected by the frozen
architecture. The analytic Morse normal-form engine remains an explicit
premise; this file does not prove that engine or the Morse lemma.
-/

noncomputable section

open Set Function
open scoped Topology Manifold ContDiff

namespace Stage1Instances.THM_M_0600

universe u

/-- The output of the Euclidean reduction, splitting construction, and
manifold transport packages. It is deliberately a separate interface so the
final root composition can be checked without pretending the engine exists. -/
def MorseNormalFormEngine : Prop :=
  forall (n : Nat) (M : Type u) [TopologicalSpace M]
    (I : ModelWithCorners Real (Euclidean n) (Euclidean n))
    [ChartedSpace (Euclidean n) M] [IsManifold I ⊤ M]
    (f : M -> Real) (p : M) (base : SmoothLocalCoordinates M I p),
      ContDiffOn Real ⊤ (inCoordinates base f) base.target ->
      fderiv Real (inCoordinates base f) 0 = 0 ->
      Function.Injective (coordinateHessian base f) ->
      exists (index : Nat) (normal : SmoothLocalCoordinates M I p),
        index <= n /\ forall x, x ∈ normal.target ->
          f (normal.invFun x) = f p + morseQuadratic index x

/-- Checked conditional composition from the expanded engine interface to the
exact canonical target. -/
theorem root_of_morseNormalFormEngine
    (engine : MorseNormalFormEngine.{u}) : MorseLemmaTarget.{u} := by
  intro n M _topology I _charted _manifold f p base hsmooth hcritical hnondegenerate
  exact engine n M I f p base hsmooth hcritical hnondegenerate

#print axioms root_of_morseNormalFormEngine

end Stage1Instances.THM_M_0600
