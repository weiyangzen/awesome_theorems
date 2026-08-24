# Machine-checked audit — S5-CLM-00003536

The claim-owned Lean surfaces elaborate at trust zero against the pinned Lean
toolchain.  `Statement.lean` checks the exact proposition and both identity
transports.  `Proof.lean` checks the typed application boundary from an
unconditional root theorem to the requested instance.  `Audit.lean` checks
the exact root type independently.

The pinned provider declaration `Bugeaud06.furstenberg_two_three` is referenced
for semantic identity but deliberately not invoked by any local theorem body:
its source axiom census is `["sorryAx"]`.  Therefore it cannot establish M0.
The structured machine-closure record must enumerate only dependencies of an
independent proof body and must report an empty observed-axiom list before a
provisional release is valid.

The frozen validator additionally rejects source-symbol shadowing, parser
substitution, alternative provider imports, and any local oracle.  The
canonical Master still owes independent exact-expression recomputation,
dependency/body/source hash verification, cold offline replay, and mutation
testing after integration.
