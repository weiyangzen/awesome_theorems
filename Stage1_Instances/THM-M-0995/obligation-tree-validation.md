# THM-M-0995 obligation-tree amendment

Registry version 2 is an append-only correction produced during `S56-M-0995-PROOF`. It retains the
version-1 registry hash, denominator, inventory, and supersession reason. The v2 denominator is
`29fa162b68c22ecc1c0b1edb83306a411eb8ddea7a4b546fbeb082270a425b18`; it covers twenty
unique obligations plus one refutation certificate and records thirty-nine typed edges. The proof graph is reciprocal, acyclic,
and root-reachable, with explicit composition certificates for the individual MGF, sum MGF,
zero-variance branch, and exact root.

The amendment does not retroactively claim that v1 was valid. `Proof.not_optimizeExponentPackage`
kernel-refutes its optimizer. V2 replaces that route with a positive-variance optimizer and a
separate zero-variance branch, while preserving the exact statement fingerprint.

The deterministic builder and structural checker both exit zero. The full exact Lean result is
recorded separately in `proof-validation.md`; validation and release assurance remain downstream.
