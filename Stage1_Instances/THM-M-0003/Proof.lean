import Statement
import ObligationTree

/-!
# THM-M-0003 proof-phase closure

This module installs a wrapper at the exact frozen target and separately checks
the frozen four-segment composition. The substantive terminal proof bodies are
the declarations in the pinned mathlib snake-lemma module.
-/

universe v u

namespace Stage1Instances.THM_M_0003.Proof

open CategoryTheory
open Stage1Instances.THM_M_0003

/-- Pinned proof body for the exact kernel-row obligation. -/
theorem kernelSegment
    (C : Type u) [Category.{v} C] [Abelian C]
    (S : ShortComplex.SnakeInput C) :
    ObligationTree.KernelSegment C S :=
  S.L₀_exact

/-- Pinned proof body for exactness immediately to the left of `delta`. -/
theorem leftBridgeSegment
    (C : Type u) [Category.{v} C] [Abelian C]
    (S : ShortComplex.SnakeInput C) :
    ObligationTree.LeftBridgeSegment C S :=
  S.L₁'_exact

/-- Pinned proof body for exactness immediately to the right of `delta`. -/
theorem rightBridgeSegment
    (C : Type u) [Category.{v} C] [Abelian C]
    (S : ShortComplex.SnakeInput C) :
    ObligationTree.RightBridgeSegment C S :=
  S.L₂'_exact

/-- Pinned proof body for the exact cokernel-row obligation. -/
theorem cokernelSegment
    (C : Type u) [Category.{v} C] [Abelian C]
    (S : ShortComplex.SnakeInput C) :
    ObligationTree.CokernelSegment C S :=
  S.L₃_exact

/-- Exact canonical wrapper over the pinned mathlib snake-lemma body. -/
theorem snakeLemma : SnakeLemmaTarget.{v, u} := by
  intro C _ _ S
  exact S.snake_lemma

/-- Independent exact-type check through the frozen child-to-root composition. -/
theorem snakeLemma_via_frozen_composition : SnakeLemmaTarget.{v, u} := by
  intro C _ _ S
  exact ObligationTree.root_compose C S
    (kernelSegment C S) (leftBridgeSegment C S)
    (rightBridgeSegment C S) (cokernelSegment C S)

#print axioms kernelSegment
#print axioms leftBridgeSegment
#print axioms rightBridgeSegment
#print axioms cokernelSegment
#print axioms snakeLemma
#print axioms snakeLemma_via_frozen_composition

end Stage1Instances.THM_M_0003.Proof
