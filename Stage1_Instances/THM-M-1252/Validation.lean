import Mathlib.Analysis.Distribution.Distribution
import Mathlib.Analysis.Distribution.Support

/-!
# THM-M-1252 independent local validation probe

This module reconstructs the frozen proposition directly from pinned mathlib without importing
the dossier's statement, obligation-tree, or proof modules. It is a same-runner differential check,
not an independent release attestation.
-/

noncomputable section

open Set TopologicalSpace
open scoped Distributions

namespace Stage1Instances.THM_M_1252.Validation

universe u

def ReconstructedTarget : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [NormedSpace Real E] [FiniteDimensional Real E]
    (Omega : Opens E) (T : Distribution Omega Real ⊤),
      (Distribution.dsupport T)ᶜ =
        ⋃₀ {U : Set E | Distribution.IsVanishingOn T U ∧ IsOpen U}

theorem independentlyReconstructedSupportLocalization :
    ReconstructedTarget.{u} := by
  intro E _ _ _ Omega T
  exact Distribution.dsupport_compl_eq

end Stage1Instances.THM_M_1252.Validation

#print axioms Distribution.dsupport_compl_eq
#print axioms Stage1Instances.THM_M_1252.Validation.independentlyReconstructedSupportLocalization
