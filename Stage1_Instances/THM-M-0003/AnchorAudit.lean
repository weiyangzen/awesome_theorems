import Mathlib.Algebra.Homology.ShortComplex.SnakeLemma

/-!
# THM-M-0003 anchor-audit probes

This file checks the exact pinned mathlib declaration against the frozen target
shape. The example is a candidate adapter, not the proof-phase root wrapper.
-/

universe v u

namespace Stage1Instances.THM_M_0003.AnchorAudit

open CategoryTheory

#check ShortComplex.SnakeInput
#check ShortComplex.SnakeInput.composableArrows
#check ShortComplex.SnakeInput.snake_lemma
#check ShortComplex.SnakeInput.L₀_exact
#check ShortComplex.SnakeInput.L₁'_exact
#check ShortComplex.SnakeInput.L₂'_exact
#check ShortComplex.SnakeInput.L₃_exact

example :
    ∀ (C : Type u) [Category.{v} C] [Abelian C]
      (S : ShortComplex.SnakeInput C),
      S.composableArrows.Exact := by
  intro C _ _ S
  exact S.snake_lemma

#print axioms ShortComplex.SnakeInput.snake_lemma

end Stage1Instances.THM_M_0003.AnchorAudit
