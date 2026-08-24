import FormalConjectures.Arxiv.«2605.12342».Conjecture1

example :
    type_of% Arxiv.«2605.12342».conjecture_1.variants.rank_2_2 →
      type_of% Arxiv.«2605.12342».conjecture_1.variants.rank_2_2 :=
  fun h => h

namespace AwesomeTheorems.Stage5.S5_CLM_00003519

/- ANCHOR:LEAN-ROOT-BEGIN -/
theorem rank_2_2_machine :
    ∃ g : Arxiv.«2605.12342».gammaSubgroup 2 2,
      Subgroup.closure {g} = ⊤ := by
  /- ANCHOR:LEAN-GENERATOR-BEGIN -/
  let τ : Equiv.Perm (Fin 2) := Equiv.swap 0 1
  let g : Arxiv.«2605.12342».gammaSubgroup 2 2 :=
    ⟨(τ, τ), by
      simp [Arxiv.«2605.12342».gammaSubgroup,
        Arxiv.«2605.12342».signDiffHom]⟩
  /- ANCHOR:LEAN-GENERATOR-END -/
  refine ⟨g, top_unique ?_⟩
  intro x _
  /- ANCHOR:LEAN-CLASSIFICATION-BEGIN -/
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
  /- ANCHOR:LEAN-CLASSIFICATION-END -/
  rcases hx with rfl | rfl
  · exact Subgroup.one_mem _
  · exact Subgroup.subset_closure (Set.mem_singleton g)
/- ANCHOR:LEAN-ROOT-END -/

end AwesomeTheorems.Stage5.S5_CLM_00003519
