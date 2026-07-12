import Statement

/-!
# THM-M-0646 proof execution

This module closes the exact frozen target through the pinned mathlib
Loewenheim-Skolem declaration. The stronger source-cardinality hypothesis is
retained at the repository boundary and is not needed by the upstream result.
-/

namespace Stage1Instances.THM_M_0646.Proof

open Cardinal FirstOrder

universe u v w w'

/-- Exact repo-local wrapper over the pinned mathlib proof body. -/
theorem loewenheimSkolem :
    LoewenheimSkolemTarget.{u, v, w, w'} := by
  intro L M _ _ kappa hInfiniteCardinal hLanguageCardinal _hSourceCardinal
  exact L.exists_elementarilyEquivalent_card_eq M kappa
    hInfiniteCardinal hLanguageCardinal

/-- Independent exact-type composition through the statement-phase adapter. -/
theorem loewenheimSkolem_via_statement_adapter :
    LoewenheimSkolemTarget.{u, v, w, w'} :=
  pinned_mathlib_implies_target

#print axioms loewenheimSkolem
#print axioms loewenheimSkolem_via_statement_adapter
#print axioms FirstOrder.Language.exists_elementarilyEquivalent_card_eq
#print axioms FirstOrder.Language.exists_elementaryEmbedding_card_eq
#print axioms FirstOrder.Language.exists_elementaryEmbedding_card_eq_of_le
#print axioms FirstOrder.Language.exists_elementaryEmbedding_card_eq_of_ge
#print axioms FirstOrder.Language.exists_elementarySubstructure_card_eq
#print axioms FirstOrder.Language.Theory.exists_large_model_of_infinite_model
#print axioms FirstOrder.Language.ElementaryEmbedding.ofModelsElementaryDiagram

end Stage1Instances.THM_M_0646.Proof
