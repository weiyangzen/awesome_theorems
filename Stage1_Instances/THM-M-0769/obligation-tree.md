# THM-M-0769 frozen obligation architecture

Item `S56-M-0769-OBLIGATION_TREE` freezes registry version 1 against the exact
`Statement.lean` and `anchor-audit.json` content hashes. Its nine stable IDs are
the denominator for later machine, human-source, and readable coverage. Any
split, merge, exclusion, eligibility change, or re-fingerprint requires a new
registry version with an append-only delta.

## Proof architecture

The proof graph separates the sole substantive foundational step from its
logical packaging. `M0769-L-FIBER-CHOICE` must construct a dependent selector
`forall i, A i` from the witnesses `forall i, Nonempty (A i)`; this is where
the pinned `Classical.choice` anchor enters. `M0769-T-NONEMPTY` then packages
that selector as `Nonempty (forall i, A i)`. `ObligationTree.lean` kernel-checks
this child-to-parent composition while retaining the selector as an explicit
premise, so the architecture does not smuggle in proof credit.

The interface, source, foundation, provenance, readability, and workflow
boundaries remain separate nodes. The seven graph types prevent a primary
source citation, an axiom report, documentation, or a workflow receipt from
being mistaken for a proof edge. Each node has a substantive semantic ledger
and a local budget no greater than 100 steps. The bridge stays explicit even
though its eventual Lean implementation may be a short invocation.

## Open boundary

The frozen first open cut is the fiber-choice bridge plus source, foundation,
provenance, readable-review, and workflow gates. The exact root remains `M3`.
No accepted proof state, H0, M0, R0, audit completion, or theorem completion is
claimed. Master acceptance is also pending.
