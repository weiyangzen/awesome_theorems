import Mathlib.Analysis.Complex.PhragmenLindelof

/-!
# THM-M-0244 discovery-only intake probe

These checks authenticate the pinned proof-bearing Phragmen-Lindelof declarations closest to the
catalog's angular-region wording. They neither select one declaration as the canonical target nor
prove an arbitrary-angle transport.
-/

#check PhragmenLindelof.horizontal_strip
#check PhragmenLindelof.vertical_strip
#check PhragmenLindelof.quadrant_I
#check PhragmenLindelof.quadrant_II
#check PhragmenLindelof.quadrant_III
#check PhragmenLindelof.quadrant_IV
#check PhragmenLindelof.right_half_plane_of_tendsto_zero_on_real
#check PhragmenLindelof.right_half_plane_of_bounded_on_real
#check Complex.norm_le_of_forall_mem_frontier_norm_le
