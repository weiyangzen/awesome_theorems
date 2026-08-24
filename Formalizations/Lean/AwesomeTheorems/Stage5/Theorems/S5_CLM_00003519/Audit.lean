import FormalConjectures.Arxiv.«2605.12342».Conjecture1

namespace AwesomeTheorems.Stage5.S5_CLM_00003519

/-
This declaration intentionally repeats the claim-owned proof in the audit
surface.  The provider-native Master compiles each owned Lean file in isolation;
the repetition prevents either the provider's placeholder body or an uncompiled
claim-local import from becoming proof authority.
-/
theorem rank_2_2_machine :
    ∃ g : Arxiv.«2605.12342».gammaSubgroup 2 2,
      Subgroup.closure {g} = ⊤ := by
  let τ : Equiv.Perm (Fin 2) := Equiv.swap 0 1
  let g : Arxiv.«2605.12342».gammaSubgroup 2 2 :=
    ⟨(τ, τ), by
      simp [Arxiv.«2605.12342».gammaSubgroup,
        Arxiv.«2605.12342».signDiffHom]⟩
  refine ⟨g, top_unique ?_⟩
  intro x _
  have hperm : ∀ σ : Equiv.Perm (Fin 2), σ = 1 ∨ σ = τ := by
    decide
  have hx : x = 1 ∨ x = g := by
    rcases x with ⟨⟨a, b⟩, hab⟩
    rcases hperm a with rfl | rfl <;> rcases hperm b with rfl | rfl
    · left
      apply Subtype.ext
      rfl
    · exfalso
      simpa [Arxiv.«2605.12342».gammaSubgroup,
        Arxiv.«2605.12342».signDiffHom, τ] using hab
    · exfalso
      simpa [Arxiv.«2605.12342».gammaSubgroup,
        Arxiv.«2605.12342».signDiffHom, τ] using hab
    · right
      apply Subtype.ext
      rfl
  rcases hx with rfl | rfl
  · exact Subgroup.one_mem _
  · exact Subgroup.subset_closure (Set.mem_singleton g)

end AwesomeTheorems.Stage5.S5_CLM_00003519

example : type_of% Arxiv.«2605.12342».conjecture_1.variants.rank_2_2 := AwesomeTheorems.Stage5.S5_CLM_00003519.rank_2_2_machine
#print axioms AwesomeTheorems.Stage5.S5_CLM_00003519.rank_2_2_machine
