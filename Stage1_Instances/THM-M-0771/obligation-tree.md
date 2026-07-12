# THM-M-0771 frozen obligation architecture

Item `S56-M-0771-OBLIGATION_TREE` freezes registry version 1 against the exact
`Statement.lean` and `anchor-audit.json` hashes. Its nine stable IDs are the
denominator for later machine, human-source, and readable coverage. Corrections,
splits, merges, exclusions, eligibility changes, or re-fingerprints require a
new version and append-only ID delta.

## Proof architecture

`M0771-L-WELLORDER-CONSTRUCTION` is the substantive leaf: for an arbitrary
type it must construct a binary relation and all `IsWellOrder` laws. The pinned
mathlib candidate realizes this through `WellOrderingRel`, itself pulled back
from cardinal order along a chosen embedding. Its eventual invocation may be
short, but the bridge remains explicit and owns the foundational and terminal
body audit.

`M0771-T-UNIVERSAL` generalizes the pointwise witness over every carrier.
`ObligationTree.lean` kernel-checks this child-to-parent composition while
retaining construction as an explicit premise, so this phase supplies no proof
credit. The interface, source, foundation, provenance, documentation, and
workflow boundaries are distinct nodes and distinct typed graphs. Every node
has a semantic ledger and a budget of at most 100 steps.

## Open boundary

The first open cut contains the well-order construction plus source,
foundation, provenance, readable-review, and workflow gates. The exact root
remains `M3`; H1 and R4 remain unchanged. No accepted proof state, H0, M0, R0,
audit completion, or theorem completion is claimed. Master acceptance remains
pending.
