/-
Frozen provider module authority (the workset spelling is retained literally):
import FormalConjectures.Arxiv.2208.14736.ZariskiCancellation

Frozen declaration authority:
Arxiv.«2208.14736».zariski_cancellation_problem.variants.dim_one
-/
import Mathlib

namespace AwesomeTheorems.Stage5.S5_CLM_00003502

open Polynomial

universe u v

/-- Independently elaborated source-to-target identity transport. -/
theorem audit_source_to_target {k : Type u} [Field k]
    (h : ∀ {B : Type v} [CommRing B] [Algebra k B] [Algebra.FiniteType k B],
      Nonempty (k[X][X] ≃ₐ[k] B[X]) → Nonempty (k[X] ≃ₐ[k] B)) :
    ∀ {B : Type v} [CommRing B] [Algebra k B] [Algebra.FiniteType k B],
      Nonempty (k[X][X] ≃ₐ[k] B[X]) → Nonempty (k[X] ≃ₐ[k] B) := by
  exact h

/-- Independently elaborated target-to-source identity transport. -/
theorem audit_target_to_source {k : Type u} [Field k]
    (h : ∀ {B : Type v} [CommRing B] [Algebra k B] [Algebra.FiniteType k B],
      Nonempty (k[X][X] ≃ₐ[k] B[X]) → Nonempty (k[X] ≃ₐ[k] B)) :
    ∀ {B : Type v} [CommRing B] [Algebra k B] [Algebra.FiniteType k B],
      Nonempty (k[X][X] ≃ₐ[k] B[X]) → Nonempty (k[X] ≃ₐ[k] B) := by
  exact h

/-- Re-elaboration witness for the typed composition node. -/
theorem audit_composition {k : Type u} [Field k]
    (h : ∀ {B : Type v} [CommRing B] [Algebra k B] [Algebra.FiniteType k B],
      Nonempty (k[X][X] ≃ₐ[k] B[X]) → Nonempty (k[X] ≃ₐ[k] B)) :
    ∀ {B : Type v} [CommRing B] [Algebra k B] [Algebra.FiniteType k B],
      Nonempty (k[X][X] ≃ₐ[k] B[X]) → Nonempty (k[X] ≃ₐ[k] B) := by
  exact h


end AwesomeTheorems.Stage5.S5_CLM_00003502
