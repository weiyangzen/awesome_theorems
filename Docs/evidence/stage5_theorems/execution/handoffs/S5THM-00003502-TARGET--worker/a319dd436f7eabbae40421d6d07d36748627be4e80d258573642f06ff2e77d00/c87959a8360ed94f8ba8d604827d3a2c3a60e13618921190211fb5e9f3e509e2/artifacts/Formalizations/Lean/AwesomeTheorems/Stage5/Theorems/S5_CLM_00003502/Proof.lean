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

/-- Typed composition node for the exact expanded cancellation proposition. -/
theorem cancellation_composition {k : Type u} [Field k]
    (closure : ∀ {B : Type v} [CommRing B] [Algebra k B] [Algebra.FiniteType k B],
      Nonempty (k[X][X] ≃ₐ[k] B[X]) → Nonempty (k[X] ≃ₐ[k] B)) :
    ∀ {B : Type v} [CommRing B] [Algebra k B] [Algebra.FiniteType k B],
      Nonempty (k[X][X] ≃ₐ[k] B[X]) → Nonempty (k[X] ≃ₐ[k] B) := by
  exact closure

/-- Application node exposing all quantified hypotheses and the required output. -/
theorem cancellation_application {k : Type u} {B : Type v} [Field k] [CommRing B]
    [Algebra k B] [Algebra.FiniteType k B]
    (closure : ∀ {C : Type v} [CommRing C] [Algebra k C] [Algebra.FiniteType k C],
      Nonempty (k[X][X] ≃ₐ[k] C[X]) → Nonempty (k[X] ≃ₐ[k] C))
    (stableEquiv : Nonempty (k[X][X] ≃ₐ[k] B[X])) :
    Nonempty (k[X] ≃ₐ[k] B) := by
  exact closure stableEquiv

end AwesomeTheorems.Stage5.S5_CLM_00003502
