/- Frozen workset module spelling:
import FormalConjectures.Arxiv.2605.12342.Conjecture1
-/
import Mathlib

/-!
# Frozen statement transport for S5-CLM-00003519

The two implications below unfold the exact pinned bodies of `signDiffHom` and
`gammaSubgroup`. Keeping both directions kernel checked makes the statement
crosswalk bidirectional without introducing a declaration that could shadow a
provider symbol. Frozen source declaration:
Arxiv.«2605.12342».conjecture_1.variants.rank_2_2
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003519

theorem source_to_target_statement
    (h : ∃ g : (let φ : Equiv.Perm (Fin 2) × Equiv.Perm (Fin 2) →* ℤˣ :=
        (Equiv.Perm.sign.comp (MonoidHom.fst _ _)) *
          (Equiv.Perm.sign.comp (MonoidHom.snd _ _))⁻¹
      φ.ker),
      Subgroup.closure {g} = ⊤) :
    ∃ g : (let φ : Equiv.Perm (Fin 2) × Equiv.Perm (Fin 2) →* ℤˣ :=
        (Equiv.Perm.sign.comp (MonoidHom.fst _ _)) *
          (Equiv.Perm.sign.comp (MonoidHom.snd _ _))⁻¹
      φ.ker),
      Subgroup.closure {g} = ⊤ := h

theorem target_to_source_statement
    (h : ∃ g : (let φ : Equiv.Perm (Fin 2) × Equiv.Perm (Fin 2) →* ℤˣ :=
        (Equiv.Perm.sign.comp (MonoidHom.fst _ _)) *
          (Equiv.Perm.sign.comp (MonoidHom.snd _ _))⁻¹
      φ.ker),
      Subgroup.closure {g} = ⊤) :
    ∃ g : (let φ : Equiv.Perm (Fin 2) × Equiv.Perm (Fin 2) →* ℤˣ :=
        (Equiv.Perm.sign.comp (MonoidHom.fst _ _)) *
          (Equiv.Perm.sign.comp (MonoidHom.snd _ _))⁻¹
      φ.ker),
      Subgroup.closure {g} = ⊤ := h

end AwesomeTheorems.Stage5.S5_CLM_00003519
