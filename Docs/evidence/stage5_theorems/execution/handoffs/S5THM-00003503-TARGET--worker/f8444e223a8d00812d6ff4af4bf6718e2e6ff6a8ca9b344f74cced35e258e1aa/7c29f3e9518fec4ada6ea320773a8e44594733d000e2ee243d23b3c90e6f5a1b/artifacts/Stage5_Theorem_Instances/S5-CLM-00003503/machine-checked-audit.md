# Machine-checked audit — S5-CLM-00003503

The machine closure receipt is deliberately separate from the human proof
inventory.  It binds the canonical semantic-environment digest, records the
root declaration and dependency census, and leaves no machine cut-set item.

The claimed level is M0-L for this worker handoff.  `trust` is zero and
`cold_from_source_replay` is true as an evidence requirement; the worker does
not impersonate the canonical Master or claim that its result is accepted.

Observed axioms are empty in the claim-owned closure record.  The pinned
provider is statement-only and contributes no proof authority.  Master must
recompute elaboration, transitive declarations, declaration bodies, axiom
usage, and a cold offline replay from source before release.
