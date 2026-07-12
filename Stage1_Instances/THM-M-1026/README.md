# THM-M-1026 rev-5.6 dossier

This is the `planned` intake for the generalized central limit theorem. The repository's literal
scope is "domains of attraction of stable distributions". That phrase denotes a theorem family,
not one uniquely quantified proposition: it may mean the necessity that every nondegenerate limit
of normalized iid sums is stable, the converse that every stable law occurs as such a limit, or a
characterization of the domain of attraction of a specified stable law.

The statement phase resolves the intake ambiguity by selecting the standard one-dimensional
equivalence: a nondegenerate Borel probability law is stable exactly when it is a weak limit of
positively scaled and centered convolution powers of some Borel probability law. This is the
law-level form of normalized iid sums. It does not silently substitute the ordinary Gaussian CLT
or the stronger tail/regular-variation characterization.

The exact target and its expanded transport elaborate in `Statement.lean` using the pinned Lean
environment. Lifecycle remains `planned`: source pinpointing, anchor audit, obligation expansion,
proof, release validation, and independent review are open. No audit or theorem completion is
claimed.
