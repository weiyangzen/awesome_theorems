# THM-M-0704 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "lambda
calculus". The source inventory supplies only the gloss "functional computation model", an
attribution to Alonzo Church, and the year 1936. A calculus is a formal system, not by itself a
proposition, and the inventory does not say which theorem about it is intended.

Several non-interchangeable targets fit the label: a definition of untyped syntax and beta
reduction, a substitution theorem, confluence, normalization for a typed calculus, an
expressiveness theorem, or equivalence with another computation model. The immediately following
repository item separately names the Church-Rosser confluence theorem, and another Stage0 item
separately names equivalence with Turing machines. Neither may silently replace this target.

The intake therefore freezes the ambiguity and exclusion boundary rather than inventing a
proposition. The root remains `[H3, M4, R4]`. A pinned Lean probe confirms that Lean exposes the
kernel expression constructors needed to represent variables, lambda abstraction, and application;
it is an API probe, not a formalization or proof of lambda calculus. Exact commands and results are
in `validation.md`.
