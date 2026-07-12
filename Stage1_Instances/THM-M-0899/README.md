# THM-M-0899 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label `Wilson定理`
(Wilson theorem). The repository attributes it to Richard Wilson in 1972 and gives only the gloss
`t-设计的存在性` (existence of `t`-designs), with no citation and an untrusted `已验证` status.

That metadata does not select one theorem. It leaves open whether `t` is fixed or quantified,
whether the intended objects are arbitrary `t-(v,k,lambda)` designs, `2`-designs/BIBDs, or pairwise
balanced designs, and whether the conclusion is exact existence, an eventual-existence result for
all sufficiently large admissible orders, or something else. Bibliographic discovery found
Wilson's 1972 pairwise-balanced-design papers and the 1975 paper whose title says it proves the
existence conjectures. Those titles make the catalog's arbitrary-`t` gloss, year, and theorem
boundary materially ambiguous; metadata alone cannot choose or reconstruct the result.

This intake therefore preserves the literal record without substituting a familiar Wilson, BIBD,
PBD, or later general `t`-design theorem. `instance.json` leaves the canonical mathematical and
Lean statements null and records `[H5, M4, R4]`: the current catalog record is not yet a stable
truth-valued proposition, no exact formal target is identified, and no readable proof can be mapped
to it. This does not classify any source-defined Wilson theorem as false or open.

`IntakeProbe.lean` checks only generic pinned fixed-cardinality-subset and binomial-coefficient APIs.
It does not define a design or state an existence theorem. All six downstream tasks remain open in
`task-dag.json`. No canonical statement, H0, M0, R0, accepted execution state, audit completion,
theorem completion, or master acceptance is claimed.
