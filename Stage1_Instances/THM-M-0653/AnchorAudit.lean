import Mathlib.ModelTheory.Definability
import Mathlib.ModelTheory.Satisfiability

/-!
# THM-M-0653 pinned anchor probes

These declarations are usable model-theory infrastructure. None states Beth
definability or proves `Stage1.THM_M_0653.BethDefinabilityTarget`.
-/

#check Set.Definable
#check Set.empty_definable_iff
#check Set.Definable.map_expansion
#check FirstOrder.Language.LHom.reduct
#check FirstOrder.Language.LHom.onTheory_model
#check FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable
#check FirstOrder.Language.Theory.models_iff_finset_models

