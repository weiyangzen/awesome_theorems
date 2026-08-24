import FormalConjectures.Arxiv.«2605.12342».Conjecture1

/-!
Exact statement transport for `S5-CLM-00003519`.

The two directions below mention the provider declaration through `type_of%`.
They therefore compare elaborated types in the provider environment instead of
copying a theorem header as text.
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003519

theorem source_to_target
    (h : type_of% Arxiv.«2605.12342».conjecture_1.variants.rank_2_2) :
    ∃ g : Arxiv.«2605.12342».gammaSubgroup 2 2,
      Subgroup.closure {g} = ⊤ :=
  h

theorem target_to_source
    (h : ∃ g : Arxiv.«2605.12342».gammaSubgroup 2 2,
      Subgroup.closure {g} = ⊤) :
    type_of% Arxiv.«2605.12342».conjecture_1.variants.rank_2_2 :=
  h

end AwesomeTheorems.Stage5.S5_CLM_00003519
