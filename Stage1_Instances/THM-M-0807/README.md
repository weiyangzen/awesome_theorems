# THM-M-0807 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "analytic
determinacy". The source gloss says only "determinacy of analytic games". It does not state the
game convention, the meaning of analytic, parameters, or the set-theoretic hypothesis under which
determinacy is asserted.

The natural provisional reading is determinacy of every length-omega Gale-Stewart game on natural
numbers whose payoff is an analytic subset of Baire space. That reading is recorded as a candidate,
not frozen as the canonical theorem: analytic determinacy is foundation-sensitive, and omitting or
inventing a large-cardinal/determinacy hypothesis would materially change the claim.

The root therefore remains `[H3, M4, R4]`. A pinned Lean probe confirms only that mathlib exposes
descriptive trees, analytic sets, Polish spaces, and measurable sets as possible encoding
ingredients. It is not the theorem statement or a proof. Exact commands and results are in
`validation.md`.
