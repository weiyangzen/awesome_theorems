/- Frozen workset module spelling:
import FormalConjectures.Arxiv.2605.12342.Conjecture1
-/
import Mathlib

/-!
# Trust-zero semantic audit for S5-CLM-00003519

These declarations force the exact target root to elaborate in both
directions after unfolding the frozen provider definitions. Frozen provider
declaration: Arxiv.«2605.12342».conjecture_1.variants.rank_2_2.
No local definition, notation, instance, macro, coercion, or namespace alias
is introduced.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003519

theorem audit_root_reflexive :
    (∃ g : (let φ : Equiv.Perm (Fin 2) × Equiv.Perm (Fin 2) →* ℤˣ :=
        (Equiv.Perm.sign.comp (MonoidHom.fst _ _)) *
          (Equiv.Perm.sign.comp (MonoidHom.snd _ _))⁻¹
      φ.ker),
      Subgroup.closure {g} = ⊤) ↔
    (∃ g : (let φ : Equiv.Perm (Fin 2) × Equiv.Perm (Fin 2) →* ℤˣ :=
        (Equiv.Perm.sign.comp (MonoidHom.fst _ _)) *
          (Equiv.Perm.sign.comp (MonoidHom.snd _ _))⁻¹
      φ.ker),
      Subgroup.closure {g} = ⊤) := Iff.rfl

theorem audit_source_to_target
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
