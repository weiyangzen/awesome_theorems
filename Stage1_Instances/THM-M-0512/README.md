# THM-M-0512 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "Selberg trace
formula". The repository source supplies only the gloss "trace formula for automorphic forms",
an attribution to Atle Selberg, and the year 1956. It does not identify a version of the formula.

The label covers materially different identities: compact versus noncompact quotients, weight-zero
versus weighted forms, and spectral expansions with or without continuous and residual terms. The
geometric side likewise depends on the group, lattice, Haar normalization, and test-function
transform. Selecting one of these versions without a source passage would substitute invented
mathematics for the repository record.

The intake therefore freezes the ambiguity and explicit exclusions rather than a proposition. The
root remains `[H1, M4, R4]`. A pinned Lean probe confirms that nearby mathlib APIs for modular and
cusp forms, finite-dimensional linear-map trace, and Haar measure are available. Those ingredients
are not a Selberg trace formula statement or proof. Exact commands and results are recorded in
`validation.md`.
