import ObligationTree

/-!
# THM-M-0984 proof bodies

This module closes the frozen machine proof cut set with the pinned mathlib
strong law and then applies the obligation tree's checked composition map.
The distinct historical-source identification obligation is not discharged by
this machine proof.
-/

noncomputable section

open Filter Finset Function MeasureTheory
open scoped MeasureTheory ProbabilityTheory Topology

namespace Stage1Instances.THM_M_0984

universe u v

/-- The terminal proof body for the exact Banach-valued strong-law obligation. -/
theorem terminalStrongLaw : ObligationTree.TerminalStrongLaw.{u, v} := by
  intro Omega _ E _ _ _ _ _ mu X h_integrable h_independent h_identical
  exact ProbabilityTheory.strong_law_ae X h_integrable h_independent h_identical

/-- Composition of the closed terminal machine obligation into the frozen root. -/
theorem strongLawRoot : ObligationTree.Root.{u, v} :=
  ObligationTree.root_of_terminal terminalStrongLaw

#print axioms terminalStrongLaw
#print axioms strongLawRoot

end Stage1Instances.THM_M_0984
