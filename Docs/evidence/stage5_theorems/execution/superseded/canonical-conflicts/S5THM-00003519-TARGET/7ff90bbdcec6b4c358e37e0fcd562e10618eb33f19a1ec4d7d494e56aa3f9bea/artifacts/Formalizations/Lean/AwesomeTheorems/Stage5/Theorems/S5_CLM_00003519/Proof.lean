/- Frozen workset module spelling:
import FormalConjectures.Arxiv.2605.12342.Conjecture1
-/
import Mathlib

/-!
# A generator for Γ_(2 ⊕ 2)

Every permutation of `Fin 2` is either the identity or the transposition.
The exact unfolded kernel condition defining `gammaSubgroup` rules out the two mixed pairs,
so the diagonal transposition generates the whole subgroup.
Frozen source declaration:
Arxiv.«2605.12342».conjecture_1.variants.rank_2_2
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003519

open Equiv.Perm

theorem rank_2_2 :
    ∃ g : (let φ : Equiv.Perm (Fin 2) × Equiv.Perm (Fin 2) →* ℤˣ :=
        (sign.comp (MonoidHom.fst _ _)) * (sign.comp (MonoidHom.snd _ _))⁻¹
      φ.ker),
      Subgroup.closure {g} = ⊤ := by
  classical
  let φ : Equiv.Perm (Fin 2) × Equiv.Perm (Fin 2) →* ℤˣ :=
    (sign.comp (MonoidHom.fst _ _)) * (sign.comp (MonoidHom.snd _ _))⁻¹
  change ∃ g : φ.ker, Subgroup.closure {g} = ⊤
  let τ : Equiv.Perm (Fin 2) := Equiv.swap 0 1
  have permutation_cases : ∀ p : Equiv.Perm (Fin 2), p = 1 ∨ p = τ := by
    decide
  let g : φ.ker :=
    ⟨(τ, τ), by
      simp [φ]⟩
  refine ⟨g, top_unique ?_⟩
  intro x hx
  rcases permutation_cases x.1.1 with hp | hp <;>
    rcases permutation_cases x.1.2 with hq | hq
  · have hx_one : x = 1 := by
      apply Subtype.ext
      exact Prod.ext hp hq
    rw [hx_one]
    exact Subgroup.one_mem _
  · have hkernel := x.2
    have hpair : x.1 = (1, τ) := Prod.ext hp hq
    change φ x.1 = 1 at hkernel
    rw [hpair] at hkernel
    simp [φ, τ] at hkernel
  · have hkernel := x.2
    have hpair : x.1 = (τ, 1) := Prod.ext hp hq
    change φ x.1 = 1 at hkernel
    rw [hpair] at hkernel
    simp [φ, τ] at hkernel
  · have hx_generator : x = g := by
      apply Subtype.ext
      exact Prod.ext hp hq
    rw [hx_generator]
    exact Subgroup.subset_closure (by simp)

end AwesomeTheorems.Stage5.S5_CLM_00003519
