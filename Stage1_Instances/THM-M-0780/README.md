# THM-M-0780 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "Cohen forcing
method". The only repository gloss is "a method for proving CH independent of ZFC". A method is
not itself a proposition, and the record does not decide whether the intended result is the
relative consistency of `not CH`, the full independence of CH, a forcing extension theorem, or a
metatheorem about a chosen formalization of ZFC.

The intake freezes that ambiguity rather than replacing it with a convenient theorem. In
particular, independence needs separate non-provability directions and explicit consistency or
model-existence assumptions; forcing also requires a selected ground-model theory, forcing notion,
genericity convention, extension construction, and preservation theorem. None is supplied by the
source inventory.

The root therefore remains `[H3, M4, R4]`. A pinned Lean probe confirms that mathlib provides
first-order languages, theories, models, sentences, and semantic consequence as possible encoding
ingredients. It is not a statement of Cohen forcing and receives no proof credit. Exact commands
and results are recorded in `validation.md`.
