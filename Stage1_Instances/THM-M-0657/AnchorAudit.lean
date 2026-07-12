import Mathlib.ModelTheory.Algebra.Field.IsAlgClosed
import Mathlib.ModelTheory.Order

/-!
# THM-M-0657 anchor audit probes

These checks identify usable pinned mathlib infrastructure and nearby examples.
They do not prove or postulate Morley's categoricity transfer theorem.
-/

#check Cardinal.Categorical
#check Cardinal.Categorical.isComplete
#check FirstOrder.Field.ACF_categorical
#check FirstOrder.Language.aleph0_categorical_dlo

#print axioms Cardinal.Categorical.isComplete
#print axioms FirstOrder.Field.ACF_categorical
#print axioms FirstOrder.Language.aleph0_categorical_dlo
