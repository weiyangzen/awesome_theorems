import Mathlib

namespace Arxiv.«1609.08688»

def auditLt₂ {α : Type*} [LT α] (a b : Fin 3 → α) : Prop :=
  ∃ i j : Fin 3, i ≠ j ∧ a i < b i ∧ a j < b j

example : True := by trivial

end Arxiv.«1609.08688»
