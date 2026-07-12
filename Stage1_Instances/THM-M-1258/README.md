# THM-M-1258 rev-5.6 intake

This directory began as the `planned` intake for the theorem commonly called Hormander's bracket
condition/theorem for sums of squares. The statement phase resolves the repository-level ambiguity
by respecting the neighboring rows: THM-M-1258 is the bracket-generating condition, while
THM-M-1259 is the separate subelliptic regularity theorem.

`Statement.lean` now freezes and elaborates the condition-valued declaration
`Stage1Instances.THM_M_1258.hormanderCondition`. No proof or analytic regularity conclusion is
claimed. Source-page fidelity remains open, and no downstream node is accepted by this worker.
