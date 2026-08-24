# Build validation — worker no-Lean preflight

The only authorized worker command is the claim-local validator with
`--no-lean`. It checks the frozen workset identity, semantic-environment
bindings, source-symbol shadowing, forbidden proof surfaces, exact M0/R0
evidence shapes, empty cut sets, and strict dominance over the pinned
THM-M-0387 negative fixture.

No Lean, Lake, Elan, network, clone, fetch, canonical repository read, or
cross-task read was used. A passing command outcome is recorded in
`receipts/current-validation.json` and in the task-root worker result. The
canonical Master remains responsible for the three trust-zero Lean builds and
for accepting or rejecting the proposed semantic hashes.
