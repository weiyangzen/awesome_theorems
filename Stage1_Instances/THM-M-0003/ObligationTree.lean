import Mathlib.Algebra.Homology.ShortComplex.SnakeLemma

/-!
# THM-M-0003 conditional obligation composition

The four exact short-complex segments are explicit premises.  This file checks
their composition into the frozen six-term target; it does not prove or credit
any premise.
-/

universe v u

namespace Stage1Instances.THM_M_0003.ObligationTree

open CategoryTheory CategoryTheory.ShortComplex
open CategoryTheory.ComposableArrows

variable (C : Type u) [Category.{v} C] [Abelian C]
variable (S : SnakeInput C)

def KernelSegment : Prop := S.L₀.Exact
def LeftBridgeSegment : Prop := S.L₁'.Exact
def RightBridgeSegment : Prop := S.L₂'.Exact
def CokernelSegment : Prop := S.L₃.Exact

/-- Exact child-to-root composition.  No snake-lemma exactness result is used. -/
theorem root_compose
    (kernel : KernelSegment C S)
    (leftBridge : LeftBridgeSegment C S)
    (rightBridge : RightBridgeSegment C S)
    (cokernel : CokernelSegment C S) : S.composableArrows.Exact :=
  exact_of_δ₀ kernel.exact_toComposableArrows
    (exact_of_δ₀ leftBridge.exact_toComposableArrows
    (exact_of_δ₀ rightBridge.exact_toComposableArrows
      cokernel.exact_toComposableArrows))

#check CategoryTheory.ShortComplex.SnakeInput.L₀_exact
#check CategoryTheory.ShortComplex.SnakeInput.L₁'_exact
#check CategoryTheory.ShortComplex.SnakeInput.L₂'_exact
#check CategoryTheory.ShortComplex.SnakeInput.L₃_exact
#print axioms root_compose

end Stage1Instances.THM_M_0003.ObligationTree
