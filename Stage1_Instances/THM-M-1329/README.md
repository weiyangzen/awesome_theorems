# THM-M-1329 rev-5.6 intake

This directory is the fail-closed `planned` intake for Robert Brooks's theorem family relating
volume growth of a noncompact Riemannian manifold to the essential spectrum of its Laplacian.
The repository supplies only the phrase "volume growth and the essential spectrum", the year
1981, and an untrusted `verified` label. It supplies no bibliographic edition, theorem number,
definition of growth, spectral quantity, geometric hypotheses, or inequality direction.

Those omissions matter: several nearby statements use different limsup/liminf exponential growth
rates, Laplacian conventions, completeness or infinite-volume assumptions, and conclusions about
the bottom of the essential spectrum. This intake therefore preserves the theorem family without
choosing a convenient variant. The provisional root vector is `[H4, M4, R4]`.

The scope map and source-statement crosswalk record what is fixed and what must be verified from a
primary source. The task DAG leaves every downstream rev-5.6 phase open. Validation evidence is in
`validation.md`; no Lean elaboration or proof closure is claimed.
