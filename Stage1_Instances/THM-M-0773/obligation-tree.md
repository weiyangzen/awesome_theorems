# THM-M-0773 frozen obligation architecture

Item `S56-M-0773-OBLIGATION_TREE` freezes registry version 1 against the exact
`Statement.lean` and `anchor-audit.json` bytes. Its ten stable obligation IDs
are the denominator for later machine, human-source, and readable coverage.
Any correction, split, merge, exclusion, eligibility change, or re-fingerprint
requires a new version and an append-only ID delta.

## Proof architecture

`M0773-ROOT` preserves the exact nonempty-family target through
`M0773-S-INTERFACE`. `M0773-C-SEED` extracts a member from `F.Nonempty`.
`M0773-L-POINTED` is the substantive bridge: it extends that member to an
inclusion-maximal member of the finite-character family. The pinned mathlib
candidate implements this bridge using Zorn with a chain union; its short API
invocation does not collapse that semantic obligation. `M0773-T-FORGET`
composes the two steps and discards only the extension conjunct.

`ObligationTree.lean` checks that last composition with the pointed package as
an explicit premise. Thus it verifies the child-to-parent interface without
claiming the premise, the root, or the pinned candidate as accepted proof.
Separate source, trust, provenance, documentation, and workflow nodes prevent
citations or receipts from being counted as mathematical proof edges. Every
semantic ledger has a budget of at most 100 steps.

## Open boundary

The root remains `M3`. The frozen cut contains the pointed bridge and the
source, foundation, provenance, readable-review, and workflow overlays. The
anchor audit located an `M0-W` candidate, but proof acceptance, transitive
trust validation, primary-source `H0`, readable `R0`, independent replay, and
master acceptance are downstream gates. No theorem completion is claimed.
