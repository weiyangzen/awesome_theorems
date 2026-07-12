import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.Topology.MetricSpace.Holder

/-!
Discovery-only checks for pinned APIs adjacent to the ambiguous THM-M-0303 catalog wording.

The Gagliardo-Nirenberg-Sobolev declarations below concern smooth functions and norm estimates.
The Holder declaration only turns already-established positive Holder control into continuity.
None states the source-selected Sobolev-space embedding or supplies a continuous representative.
-/

#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_one
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_le
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv
#check HolderOnWith
#check HolderOnWith.continuousOn
