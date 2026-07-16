import Mathlib.Algebra.Category.ModuleCat.Descent

/-!
# THM-M-0011 statement boundary probe

The repository source says only "descent theory under flat base change". It does not select the
objects, topology, faithful-flatness hypothesis, effectiveness condition, or conclusion of one
theorem. This module therefore checks the narrow pinned module-descent surface already identified
at intake. It intentionally declares no canonical target, transport, mutation fixture, or proof.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits ModuleCat

universe u

namespace Stage1Instances.THM_M_0011

#check ModuleCat.extendScalars
#check ModuleCat.preservesFiniteLimits_extendScalars_of_flat
#check ModuleCat.reflectsIsomorphisms_extendScalars_of_faithfullyFlat
#check comonadicExtendScalars

end Stage1Instances.THM_M_0011
