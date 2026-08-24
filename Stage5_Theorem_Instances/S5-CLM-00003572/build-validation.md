# Build validation — S5-CLM-00003572

Worker validation uses exactly the immutable claim's command
`check_stage5_theorem_item.py --claim-card …/claim.json --work-root …/work --no-lean`.

The preflight checks the complete owned-path set, frozen workset identity, provider source digest,
semantic-environment seal, absence of source shadowing and forbidden Lean declarations, exact M0
evidence shape, total injective R0 reconstruction, empty H/M/R cut sets, and strict dominance over
the `THM-M-0387` negative fixture. It deliberately does not invoke Lean, Lake, or Elan. Cold
trust-zero compilation of `Statement.lean`, `Proof.lean`, and `Audit.lean` remains a post-harvest
Master gate.
