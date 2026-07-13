import Mathlib.Algebra.Pointwise.Stabilizer
import Mathlib.Combinatorics.Additive.CauchyDavenport

/-!
# THM-M-0939 discovery-only intake probe

These checks authenticate adjacent pinned sumset and stabilizer APIs. They do not define critical
pairs or trios, beats, chords, continuations, or a Kemperman structure theorem, and they provide no
statement or proof credit for THM-M-0939.
-/

#check cauchy_davenport_minOrder_add
#check ZMod.cauchy_davenport
#check AddAction.stabilizer
#check AddAction.stabilizer_add_self
#check AddAction.mem_stabilizer_set_iff_subset_vadd_set
#check AddAction.mem_stabilizer_finset_iff_subset_vadd_finset
