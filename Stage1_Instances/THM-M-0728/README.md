# THM-M-0728 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the theorem label `IP = PSPACE`.
The intended mathematical claim is the equality of the interactive-proof language class and
polynomial space, conventionally associated with Adi Shamir's theorem. The repository metadata
does not, however, provide the definitions or a pinpoint primary-source statement needed to freeze
an exact formal target.

The scope map records the model choices that affect `IP`: polynomially bounded interaction, a
probabilistic polynomial-time verifier, an all-powerful prover, private versus public coins,
completeness and soundness constants, amplification, encodings, and uniformity. `PSPACE` likewise
needs an exact machine, input, and space convention. These choices are often robustly equivalent,
but those equivalences must be stated and checked rather than silently assumed.

The provisional root vector is `[H4, M4, R4]`. A pinned Lean probe confirms only that mathlib has a
language type and deterministic Turing-machine polynomial-time vocabulary; a repository-local
search found no `IP`, `PSPACE`, or interactive-proof formalization in pinned mathlib. This is API
boundary evidence, not a statement or proof of the theorem. All later work remains open in
`task-dag.json`; no source fidelity, proof, audit completion, or theorem completion is claimed.
