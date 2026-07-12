# THM-M-0806 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "analytic set
theorem". The source gloss says only "the complement property of analytic sets", attributes it to
Mikhail Suslin, and dates it to 1917. That strongly suggests the classical Suslin theorem, but it
does not state the ambient space, sigma algebra, or either direction of a proposition.

Nearby non-interchangeable readings include: a set whose set and complement are analytic is Borel;
a Borel set and its complement are analytic; the biconditional in a Polish or standard Borel space;
or the observation that analytic sets are not generally closed under complement. Choosing among
these without a pinpoint source would silently replace the repository wording.

The intake therefore freezes that ambiguity and the scope boundary, not a canonical proposition.
The root remains `[H3, M4, R4]`. A pinned Lean probe confirms that mathlib contains the descriptive
set-theory `AnalyticSet` API and a declaration explicitly documented as Suslin's theorem. This is a
candidate for the later statement crosswalk and anchor audit, not accepted source identity or proof
credit. Exact commands and results are recorded in `validation.md`.
