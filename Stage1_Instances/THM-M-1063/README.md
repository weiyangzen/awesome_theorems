# THM-M-1063 rev-5.6 statement

This directory is the `planned` intake for Donsker's invariance principle. It freezes the intended
claim as weak convergence in continuous path space of the polygonally interpolated, diffusively
rescaled partial-sum process of i.i.d. real random variables with mean zero and finite nonzero
variance to standard Brownian motion.

This is deliberately narrower and more exact than the Stage0 phrase "functional convergence of a
random walk." The statement phase has now frozen and elaborated the probability-space binders,
moment vocabulary, interpolation map, path-space topology, weak-convergence formulation, variance
normalization, and standard-Brownian characterization in `DonskerTarget.lean`; `statement.md`
records the exact conventions.

The manifest's historical `已验证` label is untrusted metadata and supplies no proof credit. No
canonical Lean expression, formal anchor, or kernel proof is claimed. The provisional root vector
is `[H2, M4, R4]`; audit and theorem completion are false.

`scope-map.md`, `source-statement-crosswalk.md`, and `task-dag.json` delimit the downstream work.
Exact statement checks and results appear in `validation.md`.
