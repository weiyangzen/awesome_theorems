# THM-M-0693 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "sequent
calculus". The repository describes a proof formalism with sequents of the form `Gamma |- Delta`
and lists identity, cut, and left/right rules. That identifies a subject and some design features,
but it does not state a theorem.

Several choices materially change even the definition: propositional versus first-order language,
classical versus intuitionistic logic, one-sided versus two-sided sequents, sets/multisets/lists of
formulae, and which structural and logical rules are primitive. A theorem would additionally need
an exact conclusion such as soundness, completeness, admissibility, or equivalence with another
calculus. The separately scheduled `THM-M-0692` already owns the generic cut-elimination label.

The intake therefore freezes these ambiguities and the no-substitution boundary rather than
inventing a proposition. A pinned Lean probe confirms only that mathlib exposes first-order
languages, formulae, theories, and list membership from which a particular calculus could later be
encoded. It is not a sequent calculus, statement, or proof. The root remains `[H3, M4, R4]`; no
audit or theorem completion is claimed.
