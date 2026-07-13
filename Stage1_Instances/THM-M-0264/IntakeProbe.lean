import Mathlib.Topology.MetricSpace.Sequences

/-!
# THM-M-0264 discovery-only intake probe

These commands authenticate the direct Bolzano-Weierstrass interfaces in the pinned mathlib
snapshot. They do not select an exact source proposition, establish statement identity, or prove
the repository target.
-/

#check tendsto_subseq_of_bounded
#check tendsto_subseq_of_frequently_bounded
#check Bornology.IsBounded.isCompact_closure
#check IsCompact.tendsto_subseq
#check SeqCompactSpace.tendsto_subseq

#print axioms tendsto_subseq_of_bounded
#print axioms tendsto_subseq_of_frequently_bounded
