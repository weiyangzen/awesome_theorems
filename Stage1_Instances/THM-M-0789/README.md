# THM-M-0789 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "measurable
cardinal theorem". The only supplied gloss is "measurable cardinals and ultrafilters", with Ulam
and 1930 as historical metadata. It does not say whether the target is a definition/equivalence,
an existence assertion, or a consequence such as inaccessibility.

The intake therefore freezes that ambiguity instead of choosing convenient mathematics. The root
remains `[H3, M4, R4]`. A pinned Lean probe confirms that mathlib has cardinals, ultrafilters, and
cardinal-complete filters from which candidate formulations could be built; it is not a canonical
statement or proof. Exact commands and results are recorded in `validation.md`.
