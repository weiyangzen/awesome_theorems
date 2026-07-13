# THM-M-0941 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Freiman's theorem. The repository
catalog supplies only the slogan "structure of sets with small doubling," attributes it to Gregory
Freiman in 1964, and labels it `verified`. Under rev-5.6 that label is untrusted metadata and
provides no source or machine-proof credit.

The slogan does not determine a proposition. It does not choose integers, torsion-free abelian
groups, or arbitrary abelian groups; define the finite set and small-doubling hypothesis; specify a
generalized arithmetic progression or coset progression; or fix properness, rank, size, constants,
and dependence on the doubling parameter. Selecting a familiar version at intake would invent
missing mathematics. The canonical statement and Lean target therefore remain null pending an
independently reviewed source passage.

Green and Ruzsa's paper *Freiman's Theorem in an arbitrary abelian group*, arXiv
`math/0505198v2`, was inspected as a source-discrimination lead. Its introduction states the
classical integer form and its Theorem 1.1 states a distinct arbitrary-abelian-group coset-
progression extension. That distinction confirms rather than resolves the catalog ambiguity.
Freiman's cited monograph remains to be inspected and admitted with a pinpoint theorem map, and
the catalog's 1964 date remains unsupported by a locator. Source status is therefore `H1`.

`IntakeProbe.lean` checks adjacent pinned mathlib APIs for doubling constants, Plunnecke-Ruzsa
bounds, Freiman maps, and special structural classifications at very small doubling. The bounded
pinned search found no generalized-arithmetic-progression interface or exact theorem matching the
unresolved root. The provisional vector is `[H1, M4, R4]`. All six downstream phases remain open; no exact Lean
statement, H0, M0, R0, accepted execution state, audit completion, theorem completion, or master
acceptance is claimed.
