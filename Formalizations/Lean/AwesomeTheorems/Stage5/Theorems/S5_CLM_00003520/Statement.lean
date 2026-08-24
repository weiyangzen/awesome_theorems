import Mathlib
import FormalConjectures.Arxiv.«2605.12342».Conjecture1

/-!
The provider module supplies the frozen theorem type only.  Every proof term in
this package is claim-owned and independent of the provider theorem body.
-/

#check Arxiv.«2605.12342».conjecture_1.variants.rank_3_3

namespace AwesomeTheorems.Stage5.S5_CLM_00003520

open Equiv.Perm

/-- Forward half of the active bidirectional semantic crosswalk. -/
theorem source_to_target_transport :
    type_of% Arxiv.«2605.12342».conjecture_1.variants.rank_3_3 →
    (∀ h₁ h₂ :
      ((Equiv.Perm.sign.comp
          (MonoidHom.fst (Equiv.Perm (Fin 3)) (Equiv.Perm (Fin 3)))) *
        (Equiv.Perm.sign.comp
          (MonoidHom.snd (Equiv.Perm (Fin 3)) (Equiv.Perm (Fin 3))))⁻¹).ker,
      Subgroup.closure {h₁, h₂} ≠ ⊤) := id

/-- Reverse half of the active bidirectional semantic crosswalk. -/
theorem target_to_source_transport :
    (∀ h₁ h₂ :
      ((Equiv.Perm.sign.comp
          (MonoidHom.fst (Equiv.Perm (Fin 3)) (Equiv.Perm (Fin 3)))) *
        (Equiv.Perm.sign.comp
          (MonoidHom.snd (Equiv.Perm (Fin 3)) (Equiv.Perm (Fin 3))))⁻¹).ker,
      Subgroup.closure {h₁, h₂} ≠ ⊤) →
    type_of% Arxiv.«2605.12342».conjecture_1.variants.rank_3_3 := id

end AwesomeTheorems.Stage5.S5_CLM_00003520
