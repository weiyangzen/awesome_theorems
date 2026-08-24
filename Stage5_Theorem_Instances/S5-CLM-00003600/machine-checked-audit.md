# Machine-checked audit

The package root is `AwesomeTheorems.Stage5.S5_CLM_00003600.erdos_1047_complete`. All three Lean surfaces import `FormalConjectures.ErdosProblems.1047` exactly. The provider theorem is mentioned only as the frozen semantic authority; its admitted body is not consumed by the claim-owned proof.

The frozen validator invokes the repository-pinned toolchain with `lean --trust=0` independently on `Statement.lean`, `Proof.lean`, and `Audit.lean`. The expected axiom census is the ordinary logical foundation (`propext`, `Classical.choice`, and `Quot.sound`), with no `sorryAx`, unsafe code, opaque oracle, or claim-specific axiom. A successful cold run establishes M0-P for the exact root expression; canonical Master replay is still required for acceptance.
