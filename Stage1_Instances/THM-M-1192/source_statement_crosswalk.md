# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Repository wording: “heat kernel Gaussian-type upper bound” | `Docs/Stage0_Blueprint.md`, `THM-M-1192` | none | Insufficient to determine a proposition |
| Two-sided Gaussian estimates for fundamental solutions of uniformly parabolic equations | D. G. Aronson, “Bounds for the fundamental solution of a parabolic equation,” *Bulletin of the American Mathematical Society* 73 (1967), 890–896, DOI `10.1090/S0002-9904-1967-11830-5` | no declaration identified or credited | Plausible primary candidate; exact displayed theorem, assumptions, constants, and errata still require audit |
| Explicit Euclidean heat kernel | Standard solution formula for `partial_t u = Delta u` | no declaration identified or credited | A much narrower equality, not evidence that the intended general estimate was selected |
| Manifold Gaussian bounds | Distinct results depending on geometry, volume growth, and curvature assumptions | none | Excluded ambiguity class; no specific source supplied |

The source label does not say whether “heat kernel” means the Euclidean Laplacian kernel, a variable-
coefficient fundamental solution, a Laplace-Beltrami kernel, a domain kernel, or a discrete kernel.
These are not interchangeable encodings. Even within Aronson's setting, the coefficient class,
uniform-parabolicity constants, lower-order terms, time horizon, and dependence of constants are
part of the theorem and cannot be inferred from the label.

No `H0` claim is made. The Aronson citation is a discovery anchor, not an accepted source receipt.
Required follow-up is an immutable copy/hash, exact page and formula/theorem pinpoint, premise and
constant-dependency mapping, correction/errata search, and independent review. Lean anchor discovery
is intentionally deferred until the root is selected, so no unrelated Gaussian estimate can become
a substituted target by search convenience.
