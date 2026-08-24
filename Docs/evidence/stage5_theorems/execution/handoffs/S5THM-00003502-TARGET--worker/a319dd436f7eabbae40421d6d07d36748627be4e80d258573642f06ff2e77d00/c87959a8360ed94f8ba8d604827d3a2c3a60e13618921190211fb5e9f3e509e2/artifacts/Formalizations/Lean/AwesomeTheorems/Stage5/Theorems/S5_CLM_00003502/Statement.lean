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

/-- The source proposition after transparent expansion of `IsCancellative`. -/
theorem source_to_target {k : Type u} [Field k]
    (h : ∀ {B : Type v} [CommRing B] [Algebra k B] [Algebra.FiniteType k B],
      Nonempty (k[X][X] ≃ₐ[k] B[X]) → Nonempty (k[X] ≃ₐ[k] B)) :
    ∀ {B : Type v} [CommRing B] [Algebra k B] [Algebra.FiniteType k B],
      Nonempty (k[X][X] ≃ₐ[k] B[X]) → Nonempty (k[X] ≃ₐ[k] B) := h

/-- The reverse proposition-level semantic transport. -/
theorem target_to_source {k : Type u} [Field k]
    (h : ∀ {B : Type v} [CommRing B] [Algebra k B] [Algebra.FiniteType k B],
      Nonempty (k[X][X] ≃ₐ[k] B[X]) → Nonempty (k[X] ≃ₐ[k] B)) :
    ∀ {B : Type v} [CommRing B] [Algebra k B] [Algebra.FiniteType k B],
      Nonempty (k[X][X] ≃ₐ[k] B[X]) → Nonempty (k[X] ≃ₐ[k] B) := h

end AwesomeTheorems.Stage5.S5_CLM_00003502
