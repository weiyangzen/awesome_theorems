# THM-M-1065 rev-5.6 intake

This directory is the `planned` intake for the Komlos-Major-Tusnady (KMT) strong
approximation. It freezes the intended theorem family as the logarithmic-error coupling of
centered i.i.d. partial sums having a moment generating function near zero with a Gaussian random
walk (equivalently Brownian motion at integer times). It does not conflate that result with the
empirical-process KMT approximation or with an invariance principle having only an unspecified
`o(sqrt n)` error.

The precise primary-source formulation, constant convention, and Lean encoding remain work for the
statement phase. The manifest's historical `已验证` label is untrusted metadata and gives no proof
credit. No canonical Lean expression, mathlib anchor, or kernel proof is claimed. The provisional
root vector is `[H2, M4, R4]`; audit and theorem completion are false.

The included claim and exclusions are in `scope-map.md`; discovery-quality human-source anchors and
their row-level correspondence are in `source-statement-crosswalk.md`; `task-dag.json` leaves every
downstream phase open. The exact intake checks and their limits are recorded in `validation.md`.
