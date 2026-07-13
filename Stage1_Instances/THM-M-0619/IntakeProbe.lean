import Mathlib.Topology.Sequences

/-!
# THM-M-0619 discovery-only intake probe

These checks authenticate pinned compactness and convergent-subsequence interfaces. They do not
select a canonical compact-metric formulation, provide a source-statement transport, or prove the
catalog target.
-/

#check CompactSpace.tendsto_subseq
#check IsCompact.tendsto_subseq
#check SeqCompactSpace.tendsto_subseq
#check isCompact_iff_isSeqCompact
#check compactSpace_iff_seqCompactSpace

#print axioms CompactSpace.tendsto_subseq
#print axioms IsCompact.tendsto_subseq
#print axioms SeqCompactSpace.tendsto_subseq
#print axioms isCompact_iff_isSeqCompact
#print axioms compactSpace_iff_seqCompactSpace
