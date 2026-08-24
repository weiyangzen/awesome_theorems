# Machine-checked audit — S5-CLM-00003572

The local proof surface is organized as four typed nodes: a certificate boundary, preservation of
the lower component, preservation of the upper component, and the root composition. Every node is
a transparent Lean theorem or lemma with a body; there are no placeholders or claim-specific
oracles. `Audit.lean` repeats the two transports and their composition independently.

The task-local worker did not execute Lean because the immutable claim requires `--no-lean`.
Consequently, this receipt records a provisional `M0-L` candidate and the exact artifacts that the
Master must compile from source with trust zero. The release decision remains provisional and sets
`master_accepted` to false.
